from fastapi import FastAPI
from dotenv import load_dotenv
import os
import numpy as np
from config import SensorData
from service import balance, ml
from middleware import LoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware
from auth_routes import router as auth_router

load_dotenv()

model=ml.load_model()

app = FastAPI(title="Stroke Detection Backend", version="1.0.0")

#--> MiddleWares
app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#--> Auth
app.include_router(auth_router, prefix="/api/v1/auth")

@app.get("/")
async def root():
    return {"message": "Stroke detection backend is live"}

#--> User detail related api endpoints
@app.get('/api/v1/users/{user_id}')
async def get_user(user_id:int):
    pass

@app.post('/api/v1/users')
async def create_user():
    pass

@app.put('/api/v1/users/{user_id}')
async def update_user():
    pass

@app.delete('/api/v1/users/{user_id}')
async def delete_user():
    pass

#--> Timely Assistance API Endpoint
@app.get('/api/v1/assistance/users/{user_id}')
async def get_user_timely_assistance(user_id:int):
    pass

#--> Balance api endpoint
@app.get('/api/v1/analyze_balance')
async def analyze_balance(data: SensorData):
    accel = np.array(data.accel)
    gyro = np.array(data.gyro)
    result = balance.analyze_balance(accel, gyro)
    return result

#--> Detect Slurred Speeech API Endpoint
@app.get('/api/v1/analyze_speech')
async def analyze_speech():
    pass