# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import joblib
import pandas as pd

from schema import LoanInput  # <--- updated

app = FastAPI(title="Loan Eligibility Prediction API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"
PIPELINE_PATH = ARTIFACTS_DIR / "model.pkl"

if not PIPELINE_PATH.exists():
    raise FileNotFoundError(f"Pipeline not found at {PIPELINE_PATH}")

pipeline = joblib.load(PIPELINE_PATH)

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# Prediction endpoint
@app.post("/predict")
def predict(data: LoanInput):  # <--- updated
    df = pd.DataFrame([data.dict()])
    pred = pipeline.predict(df)[0]
    return {"loan_status": "Approved" if pred == 1 else "Rejected"}

# Optional: run locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8005)
