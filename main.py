from fastapi import FastAPI
import joblib
import pandas as pd
from schema import LoanInput

app = FastAPI(title="Loan Eligibility Prediction API")

@app.get("/health")
def health():
    return {"status": "ok"}

model = joblib.load("artifacts/model.pkl")

@app.post("/predict")
def predict_loan(data: LoanInput):
    try:
        df = pd.DataFrame([data.dict()])
        pred = model.predict(df)[0]
        return {"loan_status": "Approved" if pred == 1 else "Rejected"}
    except Exception as e:
        return {"error": str(e)}
