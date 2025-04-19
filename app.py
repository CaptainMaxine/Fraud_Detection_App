import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model and selected features
model = joblib.load("model.pkl")
selected_features = joblib.load("selected_features.pkl")

st.title("🚨 Fraud Detection App")

# Create input widgets for selected features
user_input = {}
for feature in selected_features:
    if "amount" in feature or "claim" in feature or "limit" in feature:
        user_input[feature] = st.number_input(f"{feature.replace('_', ' ').capitalize()}", min_value=0.0, value=1000.0)
    elif "number" in feature or "witness" in feature:
        user_input[feature] = st.slider(f"{feature.replace('_', ' ').capitalize()}", 0, 10, 1)
    elif "hour" in feature:
        user_input[feature] = st.slider(f"{feature.replace('_', ' ').capitalize()}", 0, 23, 12)
    else:
        user_input[feature] = st.number_input(f"{feature.replace('_', ' ').capitalize()}", value=0.0)

# Prediction button
if st.button("Predict Fraud"):
    input_df = pd.DataFrame([user_input])[selected_features]
    prediction = model.predict(input_df)[0]
    st.success("Fraudulent" if prediction == 1 else "Not Fraudulent")
