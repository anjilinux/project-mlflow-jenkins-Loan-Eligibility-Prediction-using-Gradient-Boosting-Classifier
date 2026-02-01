from fastapi import FastAPI
from schema import LoanInput  # <- Use the correct class name
from typing import Dict

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: LoanInput) -> Dict[str, str]:
    # Dummy logic: reject if ApplicantIncome < 6000
    status = "Approved" if data.ApplicantIncome >= 6000 else "Rejected"
    return {"loan_status": status}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8005)
