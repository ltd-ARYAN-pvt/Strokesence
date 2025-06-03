# routes/detection.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime, timezone
from db.collections import get_collection
import numpy as np
from utils.mlmodel import analyze_balance
from service.ml import analyze_speech_file
from utils.jwt import get_current_user
from bson import Binary
from models.detection import DetectionOut, SlurredSpeechDetectionOut
from fastapi import Request

router = APIRouter(prefix="/api/v1", tags=["Detection"])

# 📈 Balance Analysis
class SensorData(BaseModel):
    accel: List[List[float]]
    gyro: List[List[float]]


# ⚖️ Balance Test Analysis
@router.post("/analyze_balance",response_model=DetectionOut)
async def analyze_balance_endpoint(
    data: SensorData,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user["_id"])
    username = current_user.get("email", "unknown")
    result_data = analyze_balance(np.array(data.accel), np.array(data.gyro))

    detection_doc = {
        "user_id": user_id,
        "username": username,
        "detected_at": datetime.now(timezone.utc),
        "model_version": "v1.0",
        "input_type": "balance",
        "test_result": {
            "confidence_score": result_data["confidence_score"],
            "result": result_data["result"],
            "notes": result_data.get("notes",None),
        },
        "overall_result": result_data["result"],
        "additional_notes": result_data.get("notes",None),
    }

    # try:
    #     parsed_doc=Detection(**detection_doc)
    # except Exception as e:
    #     print("Error", e)

    result=await get_collection("detections").insert_one(detection_doc)
    detection_doc["_id"] = str(result.inserted_id)
    del detection_doc["_id"]
    return detection_doc


# 🎤 Slurred Speech Analysis
@router.post("/analyze_speech",response_model=SlurredSpeechDetectionOut)
async def analyze_speech_endpoint(
    request: Request,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user["_id"])
    username = current_user.get("email", "unknown")
    audio_bytes = await file.read()
    processor = request.app.state.processor
    model = request.app.state.model
    device = request.app.state.device
    result_data = analyze_speech_file(audio_bytes,processor, model, device)

    detection_doc = {
        "user_id": user_id,
        "username": username,
        "detected_at": datetime.now(timezone.utc),
        "model_version": "v1.0",
        "input_type": "slurred_speech",
        "test_result": {
            "confidence_score": result_data["confidence_score"],
            "result": result_data["result"],
            "notes": result_data.get("notes",None),
        },
        "overall_result": result_data["result"],
        "additional_notes": result_data.get("notes",None),
    }

    # try:
    #     parsed_doc=Detection(**detection_doc)
    # except Exception as e:
    #     print("Error", e)

    result=await get_collection("detections").insert_one(detection_doc)
    detection_doc["_id"] = str(result.inserted_id)
    del detection_doc["_id"]
    return detection_doc