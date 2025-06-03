# utils/storage.py
import os
from datetime import datetime, timezone

SAVE_DIR = "uploads/audio"
os.makedirs(SAVE_DIR, exist_ok=True)

async def save_audio_file(user_id: str, audio_bytes: bytes) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    filename = f"{user_id}_{timestamp}.wav"
    path = os.path.join(SAVE_DIR, filename)
    with open(path, "wb") as f:
        f.write(audio_bytes)
    return path