import mlflow
import mlflow.sklearn
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
import joblib
import os

from data_preprocessing import preprocess_data

mlflow.set_experiment("Loan_Eligibility_GBC")

X_train, X_test, y_train, y_test, preprocessor = preprocess_data(
    "loan_data.csv",
    "clean_data.csv"
)

model = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=3,
    random_state=42
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])

with mlflow.start_run():
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    acc = accuracy_score(y_test, preds)
    mlflow.log_metric("accuracy", acc)

    if y_test.nunique() > 1:
        roc = roc_auc_score(y_test, preds)
        mlflow.log_metric("roc_auc", roc)

    mlflow.log_params({
        "n_estimators": 200,
        "learning_rate": 0.05,
        "max_depth": 3
    })

    os.makedirs("artifacts", exist_ok=True)
    joblib.dump(pipeline, "artifacts/model.pkl")

    mlflow.sklearn.log_model(
        pipeline,
        artifact_path="model",
        registered_model_name="LoanEligibilityPipeline"
    )

print(f"Accuracy: {acc}")
