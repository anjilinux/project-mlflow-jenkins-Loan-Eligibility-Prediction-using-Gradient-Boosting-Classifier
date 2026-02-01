import joblib
import pandas as pd

model = joblib.load("artifacts/model.pkl")

def predict(input_dict):
    df = pd.DataFrame([input_dict])
    return int(model.predict(df)[0])
