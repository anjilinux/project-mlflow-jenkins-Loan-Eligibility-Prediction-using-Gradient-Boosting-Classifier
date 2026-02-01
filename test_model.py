import joblib
from sklearn.metrics import accuracy_score
from data_preprocessing import preprocess_data

def test_model_accuracy():
    # Load trained pipeline
    model = joblib.load("artifacts/model.pkl")

    # Preprocess data
    X_train, X_test, y_train, y_test, _ = preprocess_data(
        "loan_data.csv",
        "clean_data.csv"
    )

    # Make predictions
    preds = model.predict(X_test)

    # Handle tiny test set
    if len(X_test) < 2:
        print("⚠️ Test set too small, skipping accuracy assertion")
    else:
        assert accuracy_score(y_test, preds) > 0.70
