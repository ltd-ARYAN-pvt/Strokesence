# routes/patients.py

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from models.patient import PatientModel, BMI, MedicalHistoryEntry,PatientOut
from pymongo.asynchronous.collection import AsyncCollection
from deps.mongo import get_patients_collection, get_detections_collection
from bson import ObjectId
from models.detection import Detection
from typing import List
from utils.jwt import get_current_user
from typing import Optional
import json

router = APIRouter(prefix="/api/v1/patients", tags=["Patients"])

@router.post("/", response_model=PatientOut)
async def create_patient_profile(
    photo: UploadFile = File(...),
    voice_sample: UploadFile = File(...),
    height_cm: float = Form(...),
    weight_kg: float = Form(...),
    medical_history: Optional[str] = Form("[]"),
    patients_col: AsyncCollection = Depends(get_patients_collection),
    current_user: dict = Depends(get_current_user)  # 🔐 Protected
):
    photo_bytes = await photo.read()
    voice_bytes = await voice_sample.read()

    try:
        parsed_medical_history = json.loads(medical_history)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid medical_history format. Must be JSON.")

    user_id = str(current_user["_id"])
    patient_data = {
        "user_id": user_id,
        "photo": photo_bytes,
        "voice_sample": voice_bytes,
        "bmi": {
            "height_cm": height_cm,
            "weight_kg": weight_kg
        },
        "medical_history": parsed_medical_history
    }

    existing = await patients_col.find_one({"user_id": user_id})
    if existing:
        await patients_col.update_one({"user_id": user_id}, {"$set": patient_data})
        updated = await patients_col.find_one({"user_id": user_id})
        return PatientOut(
            _id=str(updated["_id"]),
            user_id=user_id,
            bmi=updated['bmi'],
            medical_history=updated['medical_history']
        )

    result = await patients_col.insert_one(patient_data)
    patient_data["_id"] = str(result.inserted_id)
    return PatientOut(
        _id=patient_data["_id"],
        user_id=user_id,
        bmi=patient_data['bmi'],
        medical_history=patient_data['medical_history']
    )

@router.get("/me", response_model=PatientModel)
async def get_patient_profile(
    patients_col: AsyncCollection = Depends(get_patients_collection),
    current_user: dict = Depends(get_current_user)  # 🔐 Protected
):
    user_id = current_user["_id"]
    profile = await patients_col.find_one({"user_id": user_id})
    if not profile:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return PatientModel(**profile)


@router.get("/history/me", response_model=List[Detection])
async def get_detection_history(
    detections_col: AsyncCollection = Depends(get_detections_collection),
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user["_id"])
    cursor = detections_col.find({"user_id": user_id}).sort("detected_at", -1)
    history = await cursor.to_list(length=50)

    cleaned = []

    for doc in history:
        doc["_id"] = str(doc["_id"])
        doc["user_id"] = str(doc["user_id"])

        cleaned.append(Detection(**doc))

    return cleaned
