# test_schema.py
from schema import LoanInput
import pytest

def test_loan_input_schema():
    data = {
        "Gender": "Male",
        "Married": "Yes",
        "Dependents": "0",
        "Education": "Graduate",
        "Self_Employed": "No",
        "ApplicantIncome": 5000,
        "CoapplicantIncome": 2000,
        "LoanAmount": 150,
        "Loan_Amount_Term": 360,
        "Credit_History": 1,
        "Property_Area": "Urban"
    }
    loan = LoanInput(**data)
    assert loan.Gender == "Male"
    assert loan.LoanAmount == 150
