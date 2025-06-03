# models/token_model.py
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId

class TokenModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id", exclude=True)
    user_id: str
    refresh_token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    revoked: bool = False

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
