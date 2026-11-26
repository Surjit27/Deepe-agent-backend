import base64
import hashlib

from app.config import get_settings


def _key_material() -> bytes:
    settings = get_settings()
    secret = settings.token_cipher_secret or settings.internal_api_key or "dev-insecure"
    return hashlib.sha256(secret.encode("utf-8")).digest()


def encrypt_secret(plain: str) -> str:
    if not plain:
        return ""
    key = _key_material()
    data = plain.encode("utf-8")
    xored = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
    return base64.urlsafe_b64encode(xored).decode("ascii")


def decrypt_secret(cipher: str) -> str:
    if not cipher:
        return ""
    key = _key_material()
    raw = base64.urlsafe_b64decode(cipher.encode("ascii"))
    plain = bytes(b ^ key[i % len(key)] for i, b in enumerate(raw))
    return plain.decode("utf-8")