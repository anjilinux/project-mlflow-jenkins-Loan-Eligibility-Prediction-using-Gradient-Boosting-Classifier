import pandas as pd

def add_features(df):
    df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']
    df['Loan_Income_Ratio'] = df['LoanAmount'] / df['Total_Income']
    return df
