# routes/assistance.py
from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from db.collections import get_collection
from models.user import UserModel
from utils.twilio_client import send_emergency_whatsapp_msg
from utils.jwt import get_current_user

router = APIRouter()

@router.get("/api/v1/assistance/users/")
async def get_user_timely_assistance(
    current_user: dict = Depends(get_current_user)
):
    current_user['_id']=str(current_user["_id"])
    user_model = UserModel(**current_user)

    if not user_model.emergency_contacts:
        raise HTTPException(status_code=404, detail="No emergency contacts found")

    errors = []
    for contact in user_model.emergency_contacts:
        try:
            send_emergency_whatsapp_msg(contact.phone, user_model.name)
        except Exception as e:
            errors.append({"phone": contact.phone, "error": str(e)})

    return {
        "message": "Emergency messages dispatched",
        "errors": errors if errors else None
    }
