# models/patient_model.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class BMI(BaseModel):
    height_cm: float
    weight_kg: float

class MedicalHistoryEntry(BaseModel):
    condition: str
    diagnosed_at: datetime
    notes: Optional[str] = ""

class PatientModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    photo: bytes  # binary data
    voice_sample: bytes  # binary data
    bmi: BMI
    medical_history: List[MedicalHistoryEntry] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PatientOut(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    bmi: BMI
    medical_history: List[MedicalHistoryEntry] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
