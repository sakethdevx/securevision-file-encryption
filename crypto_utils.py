from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def encrypt_bytes(data: bytes, key: bytes):
    aes = AESGCM(key)
    nonce = os.urandom(12)
    encrypted = aes.encrypt(nonce, data, None)
    return nonce + encrypted

def decrypt_bytes(enc_data: bytes, key: bytes):
    nonce = enc_data[:12]
    data = enc_data[12:]
    aes = AESGCM(key)
    return aes.decrypt(nonce, data, None)