from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Load model and scaler

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

app = FastAPI(
    title="Bank Churn Prediction API"
)

# Input Schema


class CustomerData(BaseModel):

    CreditScore: int
    Geography: int
    Gender: int
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float


@app.get("/")
def home():

    return {
        "message": "Bank Churn Prediction API Running"
    }


@app.post("/predict")
def predict(data: CustomerData):

    features = np.array([[
        data.CreditScore,
        data.Geography,
        data.Gender,
        data.Age,
        data.Tenure,
        data.Balance,
        data.NumOfProducts,
        data.HasCrCard,
        data.IsActiveMember,
        data.EstimatedSalary
    ]])

    # Scale data

    scaled_data = scaler.transform(features)

    prediction = model.predict(scaled_data)[0]

    if prediction == 1:

        result = "Customer will Leave"

    else:

        result = "Customer will Stay"

    return {
        "Prediction": int(prediction),
        "Result": result
    }