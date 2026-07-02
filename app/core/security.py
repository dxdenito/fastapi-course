import hashlib
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.core.config import Settings


def hash_password(password: str) -> str:
    sha = hashlib.sha256(password.encode("utf-8")).hexdigest()
    hashed = bcrypt.hashpw(sha.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    sha = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return bcrypt.checkpw(sha.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=Settings().access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Settings().secret_key, algorithm=Settings().algorithm)


def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token, Settings().secret_key, algorithms=[Settings().algorithm]
        )
        return payload
    except JWTError:
        return None
