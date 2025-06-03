# models/detection.py

from datetime import datetime, timezone
from typing import Optional, Literal, List
from bson import ObjectId
from pydantic import BaseModel, Field

# Input Schemas
class BalanceInput(BaseModel):
    accel: List[List[float]]
    gyro: List[List[float]]

class SpeechInput(BaseModel):
    user_id: str

class DetectionIn(BaseModel):
    user_id: str
    input_type: Literal["balance", "slurred_speech", "eye"]

# Result Block
class DetectionResult(BaseModel):
    confidence_score: float
    result: Literal["stroke_detected", "normal"]
    notes: Optional[str] = None

# Stored Schema
class Detection(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    username: str
    detected_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    model_version: str = "v1.0"
    input_type: Literal["balance", "slurred_speech", "eye"]

    test_result: Optional[DetectionResult]

    overall_result: Optional[Literal["stroke_detected", "normal"]]
    additional_notes: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
        }

class DetectionOut(BaseModel):
    user_id: str
    username: str
    input_type: str
    detected_at: datetime
    model_version: str
    test_result: DetectionResult
    overall_result: str
    additional_notes: Optional[str] = None

class SlurredSpeechDetectionOut(BaseModel):
    user_id: str
    username: str
    input_type: str
    detected_at: datetime
    model_version: str
    test_result: DetectionResult
    overall_result: str
    additional_notes: Optional[str] = None

