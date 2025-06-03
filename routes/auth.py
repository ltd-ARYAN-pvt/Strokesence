# routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.user import UserLogin, UserCreate, UserOut
from models.token import TokenModel
from deps.mongo import get_users_collection, get_tokens_collection
from pymongo.asynchronous.collection import AsyncCollection
from utils.jwt import create_access_token, verify_password, hash_password
from datetime import datetime, timedelta, timezone
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

# 🔐 Login
@router.post("/login")
async def login(
    credentials: UserLogin,
    users_col: AsyncCollection = Depends(get_users_collection),
    tokens_col: AsyncCollection = Depends(get_tokens_collection)
):
    user = await users_col.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user_id = str(user["_id"])
    access_token_expires = timedelta(minutes=30)
    refresh_token_expires = datetime.now(timezone.utc) + timedelta(days=7)

    access_token = create_access_token(data={"sub": user_id}, expires_delta=access_token_expires)
    refresh_token = create_access_token(data={"sub": user_id}, expires_delta=timedelta(days=7))

    # Store refresh token in DB
    token_doc = TokenModel(
        user_id=user_id,
        refresh_token=refresh_token,
        expires_at=refresh_token_expires
    ).model_dump(by_alias=True)
    await tokens_col.insert_one(token_doc)

    user["_id"]=str(user["_id"])

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": UserOut(**user)
    }
