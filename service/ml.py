# service/analyze_speech.py

import os
import torch
import numpy as np
import librosa
from typing import Dict
from transformers import Wav2Vec2Processor, Wav2Vec2ForSequenceClassification
import io

# Constants
MODEL_PATH = "outputs/wav2vec2_full_20250516-042720"
TARGET_DURATION = 4.2
TARGET_SR = 16000
MAX_LENGTH = int(TARGET_DURATION * TARGET_SR)

# Disable advisory warnings
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "true"

def load_model(model_path: str):
    processor = Wav2Vec2Processor.from_pretrained(model_path)
    model = Wav2Vec2ForSequenceClassification.from_pretrained(model_path)
    model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    print("✅ Model loaded successfully")
    return processor, model, device


# === Preprocess audio ===
def preprocess_audio(audio_path: str) -> np.ndarray:
    # Load and resample to 16kHz

    audio, sr = librosa.load(audio_path, sr=None)
    if sr != TARGET_SR:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=TARGET_SR)

    # Pad or truncate to fixed length
    if len(audio) < MAX_LENGTH:
        padding = MAX_LENGTH - len(audio)
        audio = np.pad(audio, (0, padding), mode="constant")
    else:
        audio = audio[:MAX_LENGTH]

    return audio

def preprocess_audio_from_bytes(audio_bytes: bytes) -> np.ndarray:
    # Load from bytes and resample to 16kHz
    audio_stream = io.BytesIO(audio_bytes)
    audio, sr = librosa.load(audio_stream, sr=None)

    if sr != TARGET_SR:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=TARGET_SR)

    # Pad or truncate to fixed length
    if len(audio) < MAX_LENGTH:
        padding = MAX_LENGTH - len(audio)
        audio = np.pad(audio, (0, padding), mode="constant")
    else:
        audio = audio[:MAX_LENGTH]

    return audio


# === Predict function ===
def analyze_speech_file(audio_bytes: bytes, processor, model, device) -> Dict:
    audio_input = preprocess_audio_from_bytes(audio_bytes)

    inputs = processor(audio_input, sampling_rate=TARGET_SR, return_tensors="pt", padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)
        pred_class = torch.argmax(probs, dim=-1).item()
        confidence = round(probs[0, pred_class].item(), 4)

    label = "stroke_detected" if pred_class == 1 else "normal"

    return {
        "result": label,
        "confidence_score": confidence
    }