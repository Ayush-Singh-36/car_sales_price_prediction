import streamlit as st
import requests

# Set page title and layout
st.set_page_config(page_title="Car Price Predictor", layout="centered")

st.title("🚗 Car Selling Price Prediction")
st.write("Fill in the car details below to estimate its current market value.")

# 1. UI Input Form Elements
st.subheader("Car Specifications")

car_name = st.text_input("Car Model / Name", value="Maruti Swift")
year = st.number_input("Year of Manufacture", min_value=2000, max_value=2026, value=2018, step=1)
present_price = st.number_input("Present Price of Car (in Lakhs, e.g., 5.5)", min_value=0.0, value=6.0, step=0.1)
kms_driven = st.number_input("Total Distance Driven (in Kms)", min_value=0, value=40000, step=500)

# Dropdowns for categorical values based on common dataset parameters
fuel_type = st.selectbox("Fuel Type", options=["Petrol", "Diesel", "CNG"])
seller_type = st.selectbox("Seller Type", options=["Dealer", "Individual"])
transmission = st.selectbox("Transmission Type", options=["Manual", "Automatic"])
owner = st.selectbox("Number of Previous Owners", options=[0, 1, 2, 3])

st.markdown("---")

# 2. Prediction Handler
if st.button("Estimate Selling Price", type="primary"):
    # Create the payload strictly matching FastAPI's ModelInput structure
    payload = {
        "Car_Name": car_name,
        "Year": int(year),
        "Present_Price": float(present_price),
        "Kms_Driven": float(kms_driven),
        "Fuel_Type": fuel_type,
        "Seller_Type": seller_type,
        "Transmission": transmission,
        "Owner": int(owner)
    }
    
    # FastAPI's default endpoint URL for local execution
    # (Note: When we containerize via Docker, this endpoint might change depending on setup)
    api_url = "http://127.0.0.1:8000/predict"
    
    try:
        # Fire the POST request to FastAPI backend
        with st.spinner("Calculating market value..."):
            response = requests.post(api_url, json=payload)
            
        if response.status_code == 200:
            result = response.json()
            predicted_price = result["prediction"]
            
            # Display successful results nicely
            st.success(f"### Estimated Selling Price: ₹ {predicted_price:.2f} Lakhs")
        else:
            st.error(f"Backend API Error. Status Code: {response.status_code}")
            st.caption(f"Details: {response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("🚨 Connection Refused: Could not reach the backend API.")
        st.info("Make sure your FastAPI server is currently running on `http://127.0.0.1:8000` before triggering this request.")