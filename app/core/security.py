import hashlib

import bcrypt


def hash_password(password: str) -> str:
    sha = hashlib.sha256(password.encode("utf-8")).hexdigest()
    hashed = bcrypt.hashpw(sha.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    sha = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return bcrypt.checkpw(sha.encode("utf-8"), hashed_password.encode("utf-8"))


if __name__ == "__main__":
    hashed = hash_password("mypassword123")
    print(f"Hash: {hashed}")
    print(f"Verify correct: {verify_password('mypassword123', hashed)}")
    print(f"Verify wrong:   {verify_password('wrongpassword', hashed)}")
