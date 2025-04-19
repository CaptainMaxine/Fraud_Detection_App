import streamlit as st
import pandas as pd
import joblib

# Load model and selected features
model = joblib.load("model.pkl")
selected_features = joblib.load("selected_features.pkl")

st.title("🚨 Insurance Fraud Detection App")
st.markdown("Enter claim details to predict if a case is potentially fraudulent.")

# Feature input config based on data distribution
scale_config = {
    "months_as_customer": {"min": 32, "max": 430, "step": 8, "default": 206},
    "policy_deductable": {"min": 500, "max": 2000, "step": 30, "default": 1161},
    "policy_annual_premium": {"min": 848, "max": 1653, "step": 16, "default": 1253},
    "umbrella_limit": {"min": 0, "max": 6000000, "step": 120000, "default": 1202303},
    "capital-gains": {"min": 0, "max": 71205, "step": 1424, "default": 25336}
}

# Collect user input with integer-scaled widgets
user_input = {}
for feature in selected_features:
    config = scale_config.get(feature, {"min": 0, "max": 100, "step": 1, "default": 0})
    label = feature.replace("_", " ").capitalize()

    if config["max"] - config["min"] <= 10 and config["step"] == 1:
        user_input[feature] = st.selectbox(label, [0, 1])
    else:
        user_input[feature] = st.number_input(
            label,
            min_value=config["min"],
            max_value=config["max"],
            value=config["default"],
            step=config["step"]
        )

# Predict button
if st.button("Predict Fraud"):
    input_df = pd.DataFrame([user_input])[selected_features]
    prediction = model.predict(input_df)[0]
    if prediction == 1:
        st.error("⚠️ Predicted: Fraudulent Claim")
    else:
        st.success("✅ Predicted: Legitimate Claim")
