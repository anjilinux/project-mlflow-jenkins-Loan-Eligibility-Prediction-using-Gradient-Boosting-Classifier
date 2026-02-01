from fastapi import FastAPI
import joblib
import pandas as pd
from schema import LoanInput

app = FastAPI(title="Loan Eligibility Prediction API")

model = joblib.load("artifacts/model.pkl")

@app.post("/predict")
def predict_loan(data: LoanInput):
    df = pd.DataFrame([data.dict()])
    pred = model.predict(df)[0]
    return {"loan_status": "Approved" if pred == 1 else "Rejected"}
