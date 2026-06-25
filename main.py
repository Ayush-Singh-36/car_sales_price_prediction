# Importing all the libraries
import os
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Load the data
server_df = pd.read_csv('data/car data.csv')

# 2. Drop Car_Name immediately as it's not a reliable predictor column for this linear setup
df_cleaned = server_df.drop(columns=['Car_Name'])

# 3. Convert categorical text to dummy numerical variables manually with drop_first=True 
# This matches exactly what pd.get_dummies did, but excludes Car_Name and Selling_Price columns
categorical_cols = ['Fuel_Type', 'Seller_Type', 'Transmission']
encoded_df = pd.get_dummies(df_cleaned, columns=categorical_cols, drop_first=True)

# 4. CRITICAL FIX: Separate Features (X) and Target (y) BEFORE scaling!
X = encoded_df.drop(columns=['Selling_Price'])
y = encoded_df['Selling_Price']

# 5. Fit the scaler ONLY on your input features (X)
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

# 6. Divide dataset into training and test data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 7. Train the Linear Regression Model
print("Training model on Linear Regression...")
model = LinearRegression()
model.fit(X_train, y_train)
print("Training is complete.")

# 8. Evaluation Metrics
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.2f} lakhs")
print(f"Root Mean Squared Error: {rmse:.2f} lakhs")
print(f"Model R2 Score on test set: {r2*100:.3f}%")

# 9. Save ONLY the clean model and feature scaler into the bundle
model_artifacts = {
    'model': model,
    'scaler': scaler
}

with open('car_sale_price_prediction_bundle.pkl', 'wb') as f:
    pickle.dump(model_artifacts, f)

print("All updated production artifacts saved successfully!")