import joblib
from sklearn.metrics import accuracy_score
from src.data_preprocessing import preprocess_data

def test_model_accuracy():
    model = joblib.load("artifacts/model.pkl")
    X_train, X_test, y_train, y_test, _ = preprocess_data(
        "data/raw/loan_data.csv",
        "data/processed/clean_data.csv"
    )
    preds = model.predict(X_test)
    assert accuracy_score(y_test, preds) > 0.70
