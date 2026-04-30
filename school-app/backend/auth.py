import os
import re
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


def validate_nhps_email(email: str) -> tuple[bool, str]:
    """
    Returns (is_valid, role)
    Valid formats:
      - 123456@nhps.net         -> student
      - firstname.lastname@nhps.net -> staff
    """
    if not email.lower().endswith("@nhps.net"):
        return False, ""

    local = email.split("@")[0]

    # Student: exactly 6 digits
    if re.match(r"^\d{6}$", local):
        return True, "student"

    # Staff: letters.letters (no numbers, no special chars)
    if re.match(r"^[a-zA-Z]+\.[a-zA-Z]+$", local):
        return True, "staff"

    return False, ""
