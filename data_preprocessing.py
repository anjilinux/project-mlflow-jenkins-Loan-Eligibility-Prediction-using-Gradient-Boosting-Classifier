import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from collections import Counter


def preprocess_data(raw_path: str, processed_path: str):
    # Load data
    df = pd.read_csv(raw_path)

    # Encode target if needed
    if df["Loan_Status"].dtype == "object":
        df["Loan_Status"] = df["Loan_Status"].map({"Y": 1, "N": 0})

    X = df.drop("Loan_Status", axis=1)
    y = df["Loan_Status"]

    categorical_cols = [
        "Gender", "Married", "Dependents",
        "Education", "Self_Employed", "Property_Area"
    ]

    numerical_cols = [
        "ApplicantIncome", "CoapplicantIncome",
        "LoanAmount", "Loan_Amount_Term", "Credit_History"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
        ]
    )

    # ✅ SAFE stratified split
    class_counts = Counter(y)
    use_stratify = y if min(class_counts.values()) >= 2 else None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=use_stratify
    )

    # ✅ SAFE directory creation
    output_dir = os.path.dirname(processed_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    df.to_csv(processed_path, index=False)

    return X_train, X_test, y_train, y_test, preprocessor
