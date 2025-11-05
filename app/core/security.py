from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)

# def create_access_token(subject: str, expires_minutes: int | None = None):
#     if expires_minutes is None:
#         expires_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
#     expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
#     to_encode = {"sub": subject, "exp": expire}
#     encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
#     return encoded_jwt

def create_access_token(user_id: int, email: str, role: int | None = None, expires_delta: timedelta | None = None):
    to_encode = {"userId": int(user_id), "email": str(email)}
    if role is not None:
        to_encode["role"] = int(role)
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=1))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None