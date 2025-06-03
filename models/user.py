from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal, Optional
from datetime import datetime, timezone
from bson import ObjectId

# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid ObjectId")
#         return ObjectId(v)

#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type="string")


class EmergencyContact(BaseModel):
    name: str
    relation: str
    phone: str

# Full model for DB use
class UserModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id", exclude=True)
    name: str
    email: EmailStr
    password_hash: str
    role: Literal["patient", "admin"] = "patient"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    emergency_contacts: List[EmergencyContact] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Model for user creation (password required)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["patient", "admin"] = "patient"
    emergency_contacts: List[EmergencyContact] = []


# Model for user update (all fields optional)
class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[Literal["patient", "admin"]] = None
    emergency_contacts: Optional[List[EmergencyContact]] = None


# Model for sending user data back (safe output)
class UserOut(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    email: EmailStr
    role: str
    created_at: datetime
    emergency_contacts: List[EmergencyContact] = []

    class Config:
        json_encoders = {ObjectId: str}

# Model for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str