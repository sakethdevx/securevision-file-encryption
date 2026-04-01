from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import hashlib
import hmac
import json
import os
import struct
from typing import Dict, Optional, Tuple

PBKDF2_ITERATIONS = 150_000
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
MAC_SIZE = 32
MAGIC = b"SV02"
LEGACY_MAGIC = b"SV01"


def _derive_key(password: str, salt: bytes, iterations: int = PBKDF2_ITERATIONS, dklen: int = KEY_SIZE) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, dklen=dklen)


def encrypt_bytes(data: bytes, key: bytes) -> bytes:
    aes = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    encrypted = aes.encrypt(nonce, data, None)
    return nonce + encrypted


def decrypt_bytes(enc_data: bytes, key: bytes) -> bytes:
    nonce = enc_data[:NONCE_SIZE]
    data = enc_data[NONCE_SIZE:]
    aes = AESGCM(key)
    return aes.decrypt(nonce, data, None)


def encrypt_with_password(
    data: bytes,
    password: str,
    original_filename: Optional[str] = None,
    mime_type: Optional[str] = None,
) -> bytes:
    salt_kek = os.urandom(SALT_SIZE)
    salt_mac = os.urandom(SALT_SIZE)
    nonce_data = os.urandom(NONCE_SIZE)
    nonce_wrap = os.urandom(NONCE_SIZE)

    kek = _derive_key(password, salt_kek, PBKDF2_ITERATIONS)
    mac_key = _derive_key(password, salt_mac, PBKDF2_ITERATIONS)

    data_key = os.urandom(KEY_SIZE)
    data_aes = AESGCM(data_key)
    ciphertext = data_aes.encrypt(nonce_data, data, None)

    wrap_aes = AESGCM(kek)
    wrapped_key = wrap_aes.encrypt(nonce_wrap, data_key, None)

    file_hash = hashlib.sha256(data).hexdigest()
    ciphertext_hash = hashlib.sha256(ciphertext).hexdigest()
    wrapped_key_hash = hashlib.sha256(wrapped_key).hexdigest()

    metadata: Dict[str, object] = {
        "format": "SV02-multilevel",
        "algorithm": "AES-256-GCM (Layered)",
        "layers": [
            "Layer 1: PBKDF2-HMAC-SHA256 key derivation",
            "Layer 2: AES-256-GCM data encryption with random data key",
            "Layer 3: AES-256-GCM key wrapping + HMAC-SHA256 package authentication",
        ],
        "kdf": "PBKDF2-HMAC-SHA256",
        "kdf_iterations": PBKDF2_ITERATIONS,
        "salt_kek": base64.b64encode(salt_kek).decode("utf-8"),
        "salt_mac": base64.b64encode(salt_mac).decode("utf-8"),
        "nonce_data": base64.b64encode(nonce_data).decode("utf-8"),
        "nonce_wrap": base64.b64encode(nonce_wrap).decode("utf-8"),
        "wrapped_key_len": len(wrapped_key),
        "mac_len": MAC_SIZE,
        "file_hash_sha256": file_hash,
        "ciphertext_hash_sha256": ciphertext_hash,
        "wrapped_key_hash_sha256": wrapped_key_hash,
    }
    if original_filename:
        metadata["filename"] = original_filename
    if mime_type:
        metadata["mime_type"] = mime_type

    metadata_bytes = json.dumps(metadata, separators=(",", ":")).encode("utf-8")
    body = wrapped_key + ciphertext
    package_without_mac = MAGIC + struct.pack(">I", len(metadata_bytes)) + metadata_bytes + body
    package_mac = hmac.new(mac_key, package_without_mac, hashlib.sha256).digest()
    return package_without_mac + package_mac


def _decrypt_legacy_sv01(enc_data: bytes, password: str) -> Tuple[bytes, Dict[str, object]]:
    metadata_len = struct.unpack(">I", enc_data[4:8])[0]
    metadata_start = 8
    metadata_end = metadata_start + metadata_len

    if metadata_end > len(enc_data):
        raise ValueError("Corrupted encrypted file metadata")

    metadata = json.loads(enc_data[metadata_start:metadata_end].decode("utf-8"))
    ciphertext = enc_data[metadata_end:]

    expected_ciphertext_hash = metadata.get("ciphertext_hash_sha256")
    current_ciphertext_hash = hashlib.sha256(ciphertext).hexdigest()
    if expected_ciphertext_hash and expected_ciphertext_hash != current_ciphertext_hash:
        raise ValueError("Integrity verification failed: encrypted payload hash mismatch")

    salt = base64.b64decode(metadata["salt"])
    nonce = base64.b64decode(metadata["nonce"])
    iterations = int(metadata.get("kdf_iterations", PBKDF2_ITERATIONS))

    key = _derive_key(password, salt, iterations)
    aes = AESGCM(key)
    plaintext = aes.decrypt(nonce, ciphertext, None)

    expected_hash = metadata.get("file_hash_sha256")
    current_hash = hashlib.sha256(plaintext).hexdigest()
    if expected_hash and current_hash != expected_hash:
        raise ValueError("Integrity verification failed: file hash mismatch")

    metadata["format"] = "SV01-legacy"
    return plaintext, metadata


def decrypt_with_password(enc_data: bytes, password: str) -> Tuple[bytes, Dict[str, object]]:
    if len(enc_data) < 8:
        raise ValueError("Invalid encrypted file format")

    if enc_data[:4] == LEGACY_MAGIC:
        return _decrypt_legacy_sv01(enc_data, password)

    if enc_data[:4] != MAGIC:
        raise ValueError("Invalid encrypted file format")

    metadata_len = struct.unpack(">I", enc_data[4:8])[0]
    metadata_start = 8
    metadata_end = metadata_start + metadata_len

    if metadata_end > len(enc_data):
        raise ValueError("Corrupted encrypted file metadata")

    metadata = json.loads(enc_data[metadata_start:metadata_end].decode("utf-8"))
    wrapped_key_len = int(metadata.get("wrapped_key_len", 0))
    mac_len = int(metadata.get("mac_len", MAC_SIZE))

    if wrapped_key_len <= 0 or mac_len <= 0:
        raise ValueError("Corrupted encrypted file metadata")

    if len(enc_data) < metadata_end + wrapped_key_len + mac_len:
        raise ValueError("Corrupted encrypted payload")

    body_end = len(enc_data) - mac_len
    body = enc_data[metadata_end:body_end]
    wrapped_key = body[:wrapped_key_len]
    ciphertext = body[wrapped_key_len:]
    package_mac = enc_data[body_end:]

    salt_kek = base64.b64decode(metadata["salt_kek"])
    salt_mac = base64.b64decode(metadata["salt_mac"])
    nonce_data = base64.b64decode(metadata["nonce_data"])
    nonce_wrap = base64.b64decode(metadata["nonce_wrap"])
    iterations = int(metadata.get("kdf_iterations", PBKDF2_ITERATIONS))

    kek = _derive_key(password, salt_kek, iterations)
    mac_key = _derive_key(password, salt_mac, iterations)

    package_without_mac = enc_data[:body_end]
    expected_mac = hmac.new(mac_key, package_without_mac, hashlib.sha256).digest()
    if not hmac.compare_digest(expected_mac, package_mac):
        raise ValueError("Integrity verification failed: HMAC mismatch")

    expected_wrapped_hash = metadata.get("wrapped_key_hash_sha256")
    current_wrapped_hash = hashlib.sha256(wrapped_key).hexdigest()
    if expected_wrapped_hash and expected_wrapped_hash != current_wrapped_hash:
        raise ValueError("Integrity verification failed: wrapped key hash mismatch")

    expected_ciphertext_hash = metadata.get("ciphertext_hash_sha256")
    current_ciphertext_hash = hashlib.sha256(ciphertext).hexdigest()
    if expected_ciphertext_hash and expected_ciphertext_hash != current_ciphertext_hash:
        raise ValueError("Integrity verification failed: encrypted payload hash mismatch")

    wrap_aes = AESGCM(kek)
    data_key = wrap_aes.decrypt(nonce_wrap, wrapped_key, None)

    data_aes = AESGCM(data_key)
    plaintext = data_aes.decrypt(nonce_data, ciphertext, None)

    expected_hash = metadata.get("file_hash_sha256")
    current_hash = hashlib.sha256(plaintext).hexdigest()
    if expected_hash and current_hash != expected_hash:
        raise ValueError("Integrity verification failed: file hash mismatch")

    return plaintext, metadata