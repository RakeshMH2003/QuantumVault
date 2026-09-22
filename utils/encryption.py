"""
QuantumVault — Encryption Service
Uses Fernet (AES-128-CBC + HMAC-SHA256) for symmetric encryption.
A persistent key is stored in secret.key at project root.
"""
import os
from cryptography.fernet import Fernet

_KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'secret.key')


def _load_or_create_key() -> bytes:
    # 1. Check Environment Variable (Vercel / Production)
    env_key = os.environ.get('ENCRYPTION_KEY')
    if env_key:
        return env_key.encode('utf-8')

    # 2. Check Local File
    path = os.path.abspath(_KEY_FILE)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            key = f.read().strip()
        try:
            Fernet(key)
            return key
        except Exception:
            pass
            
    # 3. Generate New Key
    key = Fernet.generate_key()
    
    try:
        # Works locally and on Render
        with open(path, 'wb') as f:
            f.write(key)
        print(f'[QuantumVault] New encryption key generated: {path}')
    except OSError:
        # Fallback for Vercel's Read-Only File System
        import tempfile
        fallback_path = os.path.join(tempfile.gettempdir(), 'secret.key')
        with open(fallback_path, 'wb') as f:
            f.write(key)
        print(f'[QuantumVault] New encryption key generated (fallback): {fallback_path}')
        print('WARNING: On Vercel, you should set ENCRYPTION_KEY in your Environment Variables.')

    return key


_FERNET = Fernet(_load_or_create_key())


def encrypt_data(raw_bytes: bytes) -> bytes:
    """Encrypt raw bytes → Fernet token (bytes)."""
    return _FERNET.encrypt(raw_bytes)


def decrypt_data(token: bytes) -> bytes:
    """Decrypt Fernet token → original raw bytes."""
    return _FERNET.decrypt(token)
