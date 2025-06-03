# models/profiling_model.py
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId

class ProfilingModel(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    cpu_usage: float
    memory_usage: float
    latency_ms: float
    endpoint: str

    class Config:
        arbitrary_types_allowed = True
