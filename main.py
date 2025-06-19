import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Get the current script's directory
current_dir = Path(__file__).parent

# Join paths in a safe, OS-independent way
static_dir = current_dir / "static"
print(static_dir)

app = FastAPI(title="Loan Approval API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Load model and scaler
model = joblib.load(f"{current_dir}/model/loan_approval_model.pkl")
scaler = joblib.load(f"{current_dir}/model/scaler.pkl")
feature_columns = joblib.load(f"{current_dir}/model/model_features.pkl")


class LoanApplication(BaseModel):
    name: str = Field(..., example="John Doe")
    Gender: int = Field(..., example=1)
    Married: int = Field(..., example=1)
    Dependents: int = Field(..., example=0)
    Education: int = Field(..., example=1)
    Self_Employed: int = Field(..., example=0)
    ApplicantIncome: float = Field(..., gt=0, example=5000.0)
    CoapplicantIncome: float = Field(..., ge=0, example=0.0)
    LoanAmount: float = Field(..., gt=0, example=200.0)
    Loan_Amount_Term: int = Field(..., gt=0, example=360)
    Credit_History: int = Field(..., ge=0, le=1, example=1)
    Property_Area: int = Field(..., example=2)


@app.get("/", include_in_schema=False)
def serve_homepage():
    return FileResponse("static/index.html")


@app.post("/apply-loan")
def predict_loan(application: LoanApplication):
    try:
        # Convert input to dict and DataFrame
        input_dict = application.dict()
        input_df = pd.DataFrame([input_dict], columns=feature_columns)

        # Drop name before prediction
        input_df.drop(columns=["name"], errors="ignore", inplace=True)

        # Scale input
        input_scaled = scaler.transform(input_df)

        # Predict
        prediction = model.predict(input_scaled)[0]
        result = "Approved" if prediction == 1 else "Rejected"

        return {"name": application.name, "result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
