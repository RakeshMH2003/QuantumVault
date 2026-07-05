"""
QuantumVault — Encryption Service
Uses Fernet (AES-128-CBC + HMAC-SHA256) for symmetric encryption.
A persistent key is stored in secret.key at project root.
"""
import os
from cryptography.fernet import Fernet

_KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'secret.key')


def _load_or_create_key() -> bytes:
    path = os.path.abspath(_KEY_FILE)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            key = f.read().strip()
        try:
            Fernet(key)
            return key
        except Exception:
            pass
    key = Fernet.generate_key()
    with open(path, 'wb') as f:
        f.write(key)
    print(f'[QuantumVault] New encryption key generated: {path}')
    return key


_FERNET = Fernet(_load_or_create_key())


def encrypt_data(raw_bytes: bytes) -> bytes:
    """Encrypt raw bytes → Fernet token (bytes)."""
    return _FERNET.encrypt(raw_bytes)


def decrypt_data(token: bytes) -> bytes:
    """Decrypt Fernet token → original raw bytes."""
    return _FERNET.decrypt(token)
