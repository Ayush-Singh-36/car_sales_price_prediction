import pickle
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ML Model Production API")

# 1. Expected payload structure from Streamlit
class ModelInput(BaseModel):
    Car_Name: str
    Year: int
    Present_Price: float  
    Kms_Driven: int       
    Fuel_Type: str        
    Seller_Type: str      
    Transmission: str     
    Owner: int

# 2. Load the production bundle
with open("car_sale_price_prediction_bundle.pkl", "rb") as f:
    artifacts = pickle.load(f)

model = artifacts['model']
scaler = artifacts['scaler']

# Replace that broken home route with this clean one:
@app.get("/")
def home():
    return {"message": "API is running successfully!"}

@app.post("/predict")
def predict_features(data: ModelInput):
    # Convert incoming JSON to a dictionary
    input_data = data.model_dump()
    
    # Create the base DataFrame structure matching 'car data.csv' columns before encoding
    # We omit 'Car_Name' if your dummy columns don't track every individual car model string
    df = pd.DataFrame([{
        "Year": input_data["Year"],
        "Present_Price": input_data["Present_Price"],
        "Kms_Driven": input_data["Kms_Driven"],
        "Owner": input_data["Owner"],
        "Fuel_Type_Diesel": 1 if input_data["Fuel_Type"] == "Diesel" else 0,
        "Fuel_Type_Petrol": 1 if input_data["Fuel_Type"] == "Petrol" else 0,
        "Seller_Type_Individual": 1 if input_data["Seller_Type"] == "Individual" else 0,
        "Transmission_Manual": 1 if input_data["Transmission"] == "Manual" else 0
    }])
    
    # 3. Scale the input row using the saved scaler
    # Note: If your scaler in main.py included columns your model doesn't use, 
    # we need to make sure the shapes align perfectly.
    try:
        scaled_features = scaler.transform(df)
        prediction = model.predict(scaled_features)
        
        # If your scaler also scaled 'Selling_Price' in main.py, the prediction will be scaled!
        # For now, we return it directly as a float.
        return {"prediction": float(prediction[0])}
        
    except Exception as e:
        return {"error": f"Preprocessing alignment failed: {str(e)}"}