import pandas as pd
import os

def preprocess(raw_path: str, processed_path: str):
    """
    Reads raw loan data, cleans it, and saves clean_data.csv
    """

    # Load raw data
    df = pd.read_csv(raw_path)

    # Encode target
    df["Loan_Status"] = df["Loan_Status"].map({"Y": 1, "N": 0})

    # Handle missing values
    df["Gender"].fillna("Male", inplace=True)
    df["Married"].fillna("Yes", inplace=True)
    df["Dependents"].fillna("0", inplace=True)
    df["Self_Employed"].fillna("No", inplace=True)
    df["LoanAmount"].fillna(df["LoanAmount"].median(), inplace=True)
    df["Loan_Amount_Term"].fillna(df["Loan_Amount_Term"].median(), inplace=True)
    df["Credit_History"].fillna(1.0, inplace=True)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)

    # Save clean data
    df.to_csv(processed_path, index=False)

    print(f"✅ Clean data saved to {processed_path}")

    return df


if __name__ == "__main__":
    preprocess(
        raw_path="loan_data.csv",
        processed_path="clean_data.csv"
    )
