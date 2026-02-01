from fastapi import FastAPI
import joblib
import pandas as pd
from schema import LoanRequest

app = FastAPI(title="Loan Eligibility API")

# Load artifacts at startup
model = joblib.load("artifacts/model.pkl")
preprocessor = joblib.load("artifacts/preprocessor.pkl")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(request: LoanRequest):
    # Convert request to DataFrame
    input_df = pd.DataFrame([request.dict()])

    # Apply preprocessing
    X = preprocessor.transform(input_df)

    # Predict
    prediction = model.predict(X)[0]

    return {
        "loan_status": "Approved" if prediction == 1 else "Rejected"
    }


# 🔴 MANDATORY: Explicit port 8005
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8005,
        reload=False
    )
