import pandas as pd
import os

def preprocess(raw_path: str, processed_path: str):
    df = pd.read_csv(raw_path)

    # Encode target
    df["Loan_Status"] = df["Loan_Status"].map({"Y": 1, "N": 0})

    # Handle missing values (NO inplace=True)
    df["Gender"] = df["Gender"].fillna("Male")
    df["Married"] = df["Married"].fillna("Yes")
    df["Dependents"] = df["Dependents"].fillna("0")
    df["Self_Employed"] = df["Self_Employed"].fillna("No")

    df["LoanAmount"] = df["LoanAmount"].fillna(df["LoanAmount"].median())
    df["Loan_Amount_Term"] = df["Loan_Amount_Term"].fillna(
        df["Loan_Amount_Term"].median()
    )
    df["Credit_History"] = df["Credit_History"].fillna(1.0)

    # ✅ Create directory ONLY if path exists
    output_dir = os.path.dirname(processed_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    df.to_csv(processed_path, index=False)
    print(f"✅ Clean data saved to {processed_path}")

    return df


if __name__ == "__main__":
    preprocess(
        raw_path="loan_data.csv",
        processed_path="clean_data.csv"
    )
