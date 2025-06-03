The core MongoDB collections and corresponding Pydantic models (schemas):

1. `users` – core user account info
2. `patients` – patient-specific data including audio/image (stored in MongoDB)
3. `detections` – logs of stroke detection results
4. `tokens` – refresh tokens
5. `logs` – backend logs for requests/responses/errors
6. `profiling` – backend system performance info

---

### ✅ MongoDB Collections & Pydantic Models (Step-by-step)

#### 1. `users` Collection

**Document:**

```json
{
  "_id": ObjectId,
  "name": "John Doe",
  "email": "john@example.com",
  "password_hash": "...",
  "role": "patient",  // or "admin"
  "created_at": ISODate,
  "emergency_contacts": [
    {
      "name": "Jane",
      "relation": "Wife",
      "phone": "+911234567890"
    }
  ]
}
```

**Pydantic Model:**

```python
# models/user_model.py
from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal, Optional
from datetime import datetime
from bson import ObjectId

class EmergencyContact(BaseModel):
    name: str
    relation: str
    phone: str

class UserModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    email: EmailStr
    password_hash: str
    role: Literal["patient", "admin"] = "patient"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    emergency_contacts: List[EmergencyContact] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
```

---

#### 2. `patients` Collection

**New Note:** Storing photo/audio **as binary data** (base64 or GridFS)

**Document:**

```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "photo": Binary,
  "voice_sample": Binary,
  "bmi": {
    "height_cm": 175,
    "weight_kg": 70
  },
  "medical_history": [
    {
      "condition": "Hypertension",
      "diagnosed_at": ISODate("2020-01-01"),
      "notes": "Stable"
    }
  ]
}
```

**Pydantic Model:**

```python
# models/patient_model.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

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
```

---

#### 3. `detections` Collection

**Document:**

```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "detected_at": ISODate,
  "result": "stroke_detected",
  "model_version": "v1.0",
  "input_type": "voice",
  "confidence_score": 0.92,
  "notes": "Slurred speech detected"
}
```

**Pydantic Model:**

```python
# models/detection_model.py
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class DetectionModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    result: Literal["stroke_detected", "normal"]
    model_version: str
    input_type: Literal["voice", "balance"]
    confidence_score: float
    notes: Optional[str] = ""

    class Config:
        arbitrary_types_allowed = True
```

---

#### 4. `tokens` Collection

**Document:**

```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "refresh_token": "jwt...",
  "expires_at": ISODate,
  "created_at": ISODate,
  "revoked": false
}
```

**Pydantic Model:**

```python
# models/token_model.py
from pydantic import BaseModel, Field
from datetime import datetime

class TokenModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    refresh_token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    revoked: bool = False

    class Config:
        arbitrary_types_allowed = True
```

---

#### 5. `logs` Collection (Backend Logs)

**Document:**

```json
{
  "_id": ObjectId,
  "timestamp": ISODate,
  "level": "INFO",
  "message": "User logged in",
  "user_id": ObjectId,
  "path": "/login",
  "ip": "192.168.1.1"
}
```

**Pydantic Model:**

```python
# models/log_model.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

class LogModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    level: Literal["INFO", "WARNING", "ERROR", "DEBUG"]
    message: str
    user_id: Optional[str] = None
    path: Optional[str] = None
    ip: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
```

---

#### 6. `profiling` Collection (System Profiling)

**Document:**

```json
{
  "_id": ObjectId,
  "timestamp": ISODate,
  "cpu_usage": 57.4,
  "memory_usage": 68.2,
  "latency_ms": 123,
  "endpoint": "/detect/voice"
}
```

**Pydantic Model:**

```python
# models/profiling_model.py
from pydantic import BaseModel, Field
from datetime import datetime

class ProfilingModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    cpu_usage: float
    memory_usage: float
    latency_ms: float
    endpoint: str

    class Config:
        arbitrary_types_allowed = True
```

---
