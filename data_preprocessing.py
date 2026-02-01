import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

def preprocess_data(raw_path, processed_path):
    df = pd.read_csv(raw_path)

    df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})

    df.fillna({
        'Gender': 'Male',
        'Married': 'Yes',
        'Dependents': '0',
        'Self_Employed': 'No',
        'LoanAmount': df['LoanAmount'].median(),
        'Loan_Amount_Term': df['Loan_Amount_Term'].median(),
        'Credit_History': 1.0
    }, inplace=True)

    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    df.to_csv(processed_path, index=False)

    X = df.drop('Loan_Status', axis=1)
    y = df['Loan_Status']

    cat_cols = X.select_dtypes(include='object').columns
    num_cols = X.select_dtypes(exclude='object').columns

    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    joblib.dump(preprocessor, "artifacts/preprocessor.pkl")

    return X_train, X_test, y_train, y_test, preprocessor
