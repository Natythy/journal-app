import os
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# SECURITY CONFIGURATION
# ==========================================

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-fallback-key-for-dev-only")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# ==========================================
# PASSWORD HASHING
# ==========================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if a provided password matches the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) ->str:
    """Scrambles a plain text password into a secure hash."""
    return pwd_context.hash(password)

# ==========================================
# TOKEN GENERATION (LOGIN)
# ==========================================

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Generates a JWT that acts as the user's temporary ID card."""
    to_encode = data.copy()

    # Set the token's expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt