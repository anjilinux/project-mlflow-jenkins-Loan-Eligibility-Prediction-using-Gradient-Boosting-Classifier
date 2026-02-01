import joblib
from sklearn.metrics import classification_report, confusion_matrix
from data_preprocessing import preprocess_data

model = joblib.load("artifacts/model.pkl")

_, X_test, _, y_test, _ = preprocess_data(
    "data/raw/loan_data.csv",
    "data/processed/clean_data.csv"
)

preds = model.predict(X_test)

print(confusion_matrix(y_test, preds))
print(classification_report(y_test, preds))
