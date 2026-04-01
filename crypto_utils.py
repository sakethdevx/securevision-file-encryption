from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import hashlib
import json
import os
import struct
from typing import Dict, Optional, Tuple

PBKDF2_ITERATIONS = 150_000
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
MAGIC = b"SV01"


def _derive_key(password: str, salt: bytes, iterations: int = PBKDF2_ITERATIONS) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, dklen=KEY_SIZE)


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


def encrypt_with_password(data: bytes, password: str, original_filename: Optional[str] = None) -> bytes:
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = _derive_key(password, salt, PBKDF2_ITERATIONS)

    aes = AESGCM(key)
    ciphertext = aes.encrypt(nonce, data, None)
    file_hash = hashlib.sha256(data).hexdigest()
    ciphertext_hash = hashlib.sha256(ciphertext).hexdigest()

    metadata: Dict[str, object] = {
        "algorithm": "AES-256-GCM",
        "kdf": "PBKDF2-HMAC-SHA256",
        "kdf_iterations": PBKDF2_ITERATIONS,
        "salt": base64.b64encode(salt).decode("utf-8"),
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "file_hash_sha256": file_hash,
        "ciphertext_hash_sha256": ciphertext_hash,
    }
    if original_filename:
        metadata["filename"] = original_filename

    metadata_bytes = json.dumps(metadata, separators=(",", ":")).encode("utf-8")
    return MAGIC + struct.pack(">I", len(metadata_bytes)) + metadata_bytes + ciphertext


def decrypt_with_password(enc_data: bytes, password: str) -> Tuple[bytes, Dict[str, object]]:
    if len(enc_data) < 8 or enc_data[:4] != MAGIC:
        raise ValueError("Invalid encrypted file format")

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

    return plaintext, metadata