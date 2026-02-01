# main.py
from fastapi import FastAPI
import joblib
import pandas as pd
from schema import LoanInput
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Loan Eligibility Prediction API")

# ✅ Enable CORS (optional, useful if frontend calls API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load trained model and preprocessor
model = joblib.load("artifacts/model.pkl")
preprocessor = joblib.load("artifacts/preprocessor.pkl")  # must match your training preprocessing

# ✅ Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# ✅ Prediction endpoint with preprocessing and error handling
@app.post("/predict")
def predict_loan(data: LoanInput):
    try:
        # Convert Pydantic model to DataFrame
        df = pd.DataFrame([data.dict()])

        # Apply the same preprocessing used during training
        X_processed = preprocessor.transform(df)

        # Make prediction
        pred = model.predict(X_processed)[0]

        return {"loan_status": "Approved" if pred == 1 else "Rejected"}

    except Exception as e:
        return {"error": str(e)}
