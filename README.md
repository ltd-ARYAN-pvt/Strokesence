# StrokeSense.AI

StrokeSense.AI is an AI-powered backend system for early stroke detection using sensor data, speech analysis, and patient profiling. Built with FastAPI and MongoDB, it provides secure APIs for user management, patient data, and detection analytics.

---

## Features

- **User Authentication & Management**: Secure registration, login, and role-based access.
- **Patient Profiles**: Store patient details, medical history, photos, and voice samples.
- **Stroke Detection**:
  - **Balance Test**: Analyze accelerometer and gyroscope data.
  - **Speech Analysis**: Detect slurred speech from audio samples.
  - **Eye Test**: (Planned/Optional) Eye movement analysis.
- **Detection History**: Retrieve and review past detection results.
- **Admin & Assistance APIs**: For emergency contacts and timely help.
- **Profiling & Logging**: System performance and error tracking.

---

## Project Structure

```
.
├── app.py                  # (Legacy) FastAPI app entrypoint
├── main.py                 # Main FastAPI app with routers and middleware
├── config.py               # Configuration and settings
├── middleware.py           # Custom logging and profiling middleware
├── check_route.py          # (Optional) Route checks
├── openapi.json            # OpenAPI schema
├── README.md               # Project documentation
├── db/
│   ├── collections.py      # MongoDB collection helpers
│   └── mongodb.py          # MongoDB connection logic
├── deps/
│   └── mongo.py            # Dependency injection for MongoDB
├── models/
│   ├── detection.py        # Detection schemas
│   ├── patient.py          # Patient schemas
│   ├── profilier.py        # Profiling schemas
│   ├── token.py            # Token schemas
│   └── user.py             # User schemas
├── routes/
│   ├── assitance.py        # Assistance endpoints
│   ├── detection.py        # Detection endpoints (balance, speech, etc.)
│   ├── patient.py          # Patient endpoints
│   └── users.py            # User endpoints
├── service/
│   └── ...                 # ML and business logic
├── utils/
│   └── ...                 # Utility functions (JWT, ML, error handling)
├── outputs/
│   └── wav2vec2_full_.../  # Model outputs/artifacts
└── .env.local              # Environment variables
```

---

## API Overview

- **Auth**: `/api/v1/auth/`
- **Users**: `/api/v1/users/`
- **Patients**: `/api/v1/patients/`
- **Detection**: `/api/v1/analyze_balance`, `/api/v1/analyze_speech`
- **Assistance**: `/api/v1/assistance/`

See [openapi.json](openapi.json) for the full schema.

---

## Models

- **User**: Name, email, password hash, role, emergency contacts.
- **Patient**: User link, photo, voice sample, BMI, medical history.
- **Detection**: User, timestamp, input type, result, confidence, notes.
- **Token**: Refresh tokens for authentication.
- **Profiling/Logs**: System and error logs.

See [models/models.md](models/models.md) for detailed schemas.

---

## Setup & Running

1. **Clone the repo**  
   ```sh
   git clone https://github.com/ltd-ARYAN-pvt/Strokesence.git
   cd Strokesence
   ```

2. **Install dependencies**  
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure environment**  
   - Create `.env.local` and set MongoDB URI and secrets.

4. **Run the server**  
   ```sh
   fastapi dev main.py
   ```

5. **API Docs**  
   - Visit `http://localhost:8000/docs` for Swagger UI.

---

## Contributing

- Fork, branch, and submit PRs.
- Follow PEP8 and add docstrings.
- Write tests for new features.

---

## License

MIT License

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [PyTorch](https://pytorch.org/) (for ML models)