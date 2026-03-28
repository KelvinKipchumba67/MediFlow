from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import hashlib
import time
import os
from fastapi.middleware.cors import CORSMiddleware

# 1. Initialize the API
app = FastAPI(title="MediFlow Intelligence API", version="1.0")

# 2. Define the expected incoming data (Patient Symptoms)
class PatientData(BaseModel):
    patient_id: str
    age: int
    fever_duration_days: int
    cough_duration_days: int
    weight_loss_kg: float
    night_sweats: int
    hemoptysis: int
#this allows the communication between the frontend and the FASTApi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load the AI Brain on startup
MODEL_PATH = "models/rf_tb_model.pkl"
try:
    rf_model = joblib.load(MODEL_PATH)
    print("SUCCESS: Random Forest Model Loaded.")
except Exception as e:
    print(f"CRITICAL ERROR: Could not load model at {MODEL_PATH}. Did you run train_model.py?")
    rf_model = None

# 4. The Core Triage Endpoint
@app.post("/triage")
async def triage_patient(data: PatientData):
    if rf_model is None:
        raise HTTPException(status_code=500, detail="AI Model not initialized.")

    # --- TIER 1: Deterministic Rule-Based Guardrails (WHO Standards) ---
    if data.hemoptysis == 1 or data.cough_duration_days >= 21:
        triage_result = "HIGH RISK - CRITICAL"
        methodology = "Rule-Based Override (Red Flag Symptoms)"
        confidence = "100%"
    
    # --- TIER 2: Probabilistic Random Forest ML ---
    else:
        # Format the data exactly as the model expects it
        features = np.array([[
            data.age, 
            data.fever_duration_days, 
            data.cough_duration_days, 
            data.weight_loss_kg, 
            data.night_sweats, 
            data.hemoptysis
        ]])
        
        # Get the probability (Index 1 is the 'High Risk' class)
        probabilities = rf_model.predict_proba(features)[0]
        high_risk_prob = probabilities[1]
        
        confidence = f"{high_risk_prob * 100:.1f}%"
        triage_result = "HIGH RISK" if high_risk_prob > 0.5 else "LOW RISK"
        methodology = "Random Forest Classifier"

    # --- TIER 3: Cryptographic Accountability (The Blockchain Hash) ---
    # We hash the prediction with the patient ID and a timestamp to make it immutable
    timestamp = str(time.time())
    raw_string = f"{data.patient_id}:{triage_result}:{confidence}:{timestamp}"
    prediction_hash = hashlib.sha256(raw_string.encode()).hexdigest()

    # Return the structured payload to the frontend
    return {
        "status": "success",
        "triage_result": triage_result,
        "confidence_score": confidence,
        "methodology": methodology,
        "blockchain_payload": {
            "prediction_hash": prediction_hash,
            "timestamp": timestamp
        }
    }