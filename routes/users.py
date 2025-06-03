# routes/users.py

from fastapi import APIRouter, HTTPException, status, Depends
from models.user import UserCreate, UserOut, UserUpdate, UserModel
from deps.mongo import get_users_collection
from pymongo.asynchronous.collection import AsyncCollection
from utils.hashing import hash_password
from bson import ObjectId, errors as bson_errors
from utils.jwt import get_current_user

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

# ➕ Create user
@router.post("/", response_model=UserOut)
async def create_user(
    user: UserCreate, 
    users_col: AsyncCollection = Depends(get_users_collection)
):
    existing = await users_col.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a UserModel instance
    user_model = UserModel(
        name=user.name,
        email=user.email,   
        password_hash=hash_password(user.password),
        role=user.role,
        emergency_contacts=user.emergency_contacts
    )

    result = await users_col.insert_one(user_model.model_dump(by_alias=True,exclude_none=True))

    user_model.id = str(result.inserted_id)  
    return UserOut(
        _id=user_model.id,
        name=user_model.name,
        email=user_model.email,
        role=user_model.role,
        created_at=user_model.created_at,
        emergency_contacts=user_model.emergency_contacts
    )


# 📥 Get user by ID
@router.get("/me", response_model=UserOut)
async def get_user(
    users_col: AsyncCollection = Depends(get_users_collection),
    current_user: dict = Depends(get_current_user)  # 🔐 Protected
):
    user_id = current_user["_id"]
    user = await users_col.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**user)

# ✏️ Update user
@router.put("/me", response_model=UserOut)
async def update_user(
    data: UserUpdate,
    users_col: AsyncCollection = Depends(get_users_collection),
    current_user: dict = Depends(get_current_user)  # 🔐 Protected
):
    user_id = current_user["_id"]
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    result = await users_col.update_one({"_id": user_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    updated = await users_col.find_one({"_id": user_id})
    return UserOut(**updated)


# ❌ Delete user
@router.delete("/me")
async def delete_user(
    users_col: AsyncCollection = Depends(get_users_collection),
    current_user: dict = Depends(get_current_user)  # 🔐 Protected
):
    user_id = current_user["_id"]
    result = await users_col.delete_one({"_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
