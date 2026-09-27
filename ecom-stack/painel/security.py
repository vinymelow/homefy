"""Primitivas stdlib para senha, sessão, CSRF e TOTP."""
import base64
import hashlib
import hmac
import os
import secrets
import struct
import time
from urllib.parse import quote


def hash_password(password: str) -> str:
    if len(password) < 12:
        raise ValueError("A senha deve ter pelo menos 12 caracteres")
    salt = os.urandom(16)
    derived = hashlib.scrypt(password.encode(), salt=salt, n=2**15, r=8, p=1, dklen=32)
    return "scrypt$32768$8$1$%s$%s" % (
        base64.urlsafe_b64encode(salt).decode().rstrip("="),
        base64.urlsafe_b64encode(derived).decode().rstrip("="),
    )


def verify_password(password: str, encoded: str) -> bool:
    try:
        _, n, r, p, salt_s, digest_s = encoded.split("$", 5)
        pad = lambda value: value + "=" * (-len(value) % 4)
        salt = base64.urlsafe_b64decode(pad(salt_s))
        expected = base64.urlsafe_b64decode(pad(digest_s))
        actual = hashlib.scrypt(password.encode(), salt=salt, n=int(n), r=int(r), p=int(p), dklen=len(expected))
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def new_secret(nbytes: int = 32) -> str:
    return secrets.token_urlsafe(nbytes)


def new_totp_secret() -> str:
    return base64.b32encode(os.urandom(20)).decode().rstrip("=")


def totp_code(secret: str, timestamp: int | None = None) -> str:
    timestamp = int(timestamp or time.time())
    key = base64.b32decode(secret + "=" * (-len(secret) % 8), casefold=True)
    counter = struct.pack(">Q", timestamp // 30)
    digest = hmac.new(key, counter, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    number = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1_000_000
    return f"{number:06d}"


def verify_totp(secret: str, code: str) -> bool:
    clean = "".join(ch for ch in code if ch.isdigit())
    now = int(time.time())
    return len(clean) == 6 and any(hmac.compare_digest(totp_code(secret, now + delta), clean) for delta in (-30, 0, 30))


def totp_uri(secret: str, email: str) -> str:
    return f"otpauth://totp/Homefy:{quote(email)}?secret={secret}&issuer=Homefy&digits=6&period=30"

