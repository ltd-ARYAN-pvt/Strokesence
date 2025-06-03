import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from typing import Optional
from config import settings
from utils import hashing
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from deps.mongo import get_users_collection
from pymongo.asynchronous.collection import AsyncCollection
from bson import ObjectId, errors as bson_errors

# Settings
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return hashing(password)

# Utility to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT utilities
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        # print(token)
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print("✅ Token decoded payload:", decoded)
        return decoded
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    users_col: AsyncCollection = Depends(get_users_collection)
):
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        print(user_id)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        try:
            user = await users_col.find_one({"_id": ObjectId(user_id)})
        except bson_errors.InvalidId:
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid credentials, error :- {e}")