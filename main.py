from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import mlflow.pyfunc
import os

# Load model once
model_path = "artifacts/loan_model"  # adjust path if needed
model = mlflow.pyfunc.load_model(model_path)

app = FastAPI()

class LoanRequest(BaseModel):
    Gender: str
    Married: str
    Dependents: str
    Education: str
    Self_Employed: str
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: int
    Property_Area: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(request: LoanRequest):
    data = request.dict()

    # Predict using your model
    prediction = model.predict([list(data.values())])[0]

    # Log prediction in MLflow
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5555"))
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "Loan_Eligibility_GBC"))

    with mlflow.start_run(run_name="FastAPI Prediction") as run:
        mlflow.log_params(data)
        mlflow.log_metric("loan_status", 1 if prediction == "Approved" else 0)

    return {"loan_status": prediction}
