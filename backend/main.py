import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Loan Approval API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and preprocessor
model = joblib.load("models/loan_approval_model.pkl")
scaler = joblib.load("models/scaler.pkl")
feature_columns = joblib.load("models/model_features.pkl")


class LoanApplication(BaseModel):
    name: str = Field(..., example="John Doe")
    income: float = Field(..., gt=0, example=5000.0)
    loanAmount: float = Field(..., gt=0, example=200.0)
    employment: str = Field(..., example="Employed")
    creditHistory: int = Field(..., ge=0, le=1, example=1)


@app.get("/")
def root():
    return {"message": "Loan Approval API is running."}


@app.post("/apply-loan")
def predict_loan(application: LoanApplication):
    try:
        # Map employment to one-hot encoded columns
        employment_map = {
            "Employed": [1, 0, 0],
            "Self-Employed": [0, 1, 0],
            "Unemployed": [0, 0, 1],
        }
        employment_encoded = employment_map.get(application.employment, [1, 0, 0])

        # Build input dictionary aligned with training columns
        input_dict = {
            "ApplicantIncome": application.income,
            "LoanAmount": application.loanAmount,
            "Credit_History": application.creditHistory,
            "Self_Employed": employment_encoded[1],
            "Unemployed": employment_encoded[2],
            "Employed": employment_encoded[0],
        }

        # Fill missing feature columns with 0
        for col in feature_columns:
            if col not in input_dict:
                input_dict[col] = 0

        # Reorder according to training columns
        input_data = np.array([input_dict[col] for col in feature_columns]).reshape(
            1, -1
        )

        # Scale input
        input_scaled = scaler.transform(input_data)

        # Predict
        prediction = model.predict(input_scaled)[0]
        result = "Approved" if prediction == 1 else "Rejected"

        return {"name": application.name, "result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
