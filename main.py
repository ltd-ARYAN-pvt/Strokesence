from fastapi import FastAPI
from db.mongodb import connect_to_mongo, close_mongo_connection
from utils.error import mongodb_exception_handler
from pymongo.errors import PyMongoError
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from middleware import LoggingMiddleware, ProfilingMiddleware
from routes.users import router as users_router
from routes.assitance import router as assistance_router
from routes.auth import router as auth_router
from routes.detection import router as detection_router
from routes.patient import router as patient_router
from service.ml import load_model
from utils.gcs_downloader import download_folder
from config import settings
import os

MODEL_BUCKET = settings.MODEL_BUCKET
MODEL_PREFIX = settings.MODEL_PREFIX
MODEL_LOCAL_PATH = settings.MODEL_LOCAL_PATH

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load
    await connect_to_mongo()

    # ✅ Download model files from GCS if not already present
    if not os.path.exists(MODEL_LOCAL_PATH):
        print("📦 Model not found locally. Downloading from GCS...")
        download_folder(
            bucket_name=MODEL_BUCKET,
            prefix=MODEL_PREFIX,
            local_dir=MODEL_LOCAL_PATH
        )
    else:
        print("✅ Model already present locally.")
    # ✅ Load speech model once
    processor, model, device = load_model("outputs/wav2vec2_full_20250516-042720")
    app.state.processor = processor
    app.state.model = model
    app.state.device = device
    
    yield
    # Clean up
    await close_mongo_connection()

app = FastAPI(
    title="Stroke Detection Backend",
    version="v1.0.0",
    lifespan=lifespan
)

# 📌 Middlewares
app.add_middleware(LoggingMiddleware)
app.add_middleware(ProfilingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ❗Global Exception Handlers
app.add_exception_handler(PyMongoError, mongodb_exception_handler)

# 🔗 Routers
app.include_router(users_router)
app.include_router(assistance_router)
app.include_router(auth_router)
app.include_router(detection_router)
app.include_router(patient_router)

@app.get("/ping")
async def root():
    return {"message": "pong"}