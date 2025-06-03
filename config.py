from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import List
import numpy as np

class SensorData(BaseModel):
    accel: List[List[float]]  # [[x, y, z], [x, y, z], ...]
    gyro: List[List[float]]   # [[x, y, z], [x, y, z], ...]


class Settings(BaseSettings):
    MONGODB_URL: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    ACC_SID: str
    Auth_token: str
    MT_Num: str
    MT_Whatsapp: str
    MODEL_BUCKET: str
    MODEL_PREFIX: str
    MODEL_LOCAL_PATH: str

    class Config:
        env_file = ".env.local"
        env_file_encoding = 'utf-8'
        case_sensitive = False

settings = Settings()