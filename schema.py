# schema.py
from pydantic import BaseModel, Field, conint, confloat

class LoanInput(BaseModel):
    Gender: str = Field(..., description="Gender of the applicant, e.g., Male/Female")
    Married: str = Field(..., description="Marital status, e.g., Yes/No")
    Dependents: str = Field(..., description="Number of dependents, e.g., 0, 1, 2, 3+")
    Education: str = Field(..., description="Education level, e.g., Graduate/Not Graduate")
    Self_Employed: str = Field(..., description="Whether self-employed, e.g., Yes/No")
    ApplicantIncome: confloat(ge=0) = Field(..., description="Applicant's monthly income")
    CoapplicantIncome: confloat(ge=0) = Field(..., description="Co-applicant's monthly income")
    LoanAmount: confloat(ge=0) = Field(..., description="Requested loan amount")
    Loan_Amount_Term: confloat(ge=0) = Field(..., description="Loan term in months")
    Credit_History: confloat(ge=0, le=1) = Field(..., description="Credit history: 1 = meets guidelines, 0 = does not")
    Property_Area: str = Field(..., description="Property area, e.g., Urban/Semiurban/Rural")
