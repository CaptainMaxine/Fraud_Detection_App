import streamlit as st
import pandas as pd
import joblib

# Load model and selected features
model = joblib.load("model.pkl")
selected_features = joblib.load("selected_features.pkl")

st.title("🚨 Insurance Fraud Detection App")
st.markdown("Enter claim details to predict if a case is potentially fraudulent.")

# Human-readable dropdowns for encoded features
incident_severity = st.selectbox("Incident Severity", [
    "Minor Damage", "Major Damage", "Total Loss", "Trivial Damage"])

occupation = st.selectbox("Insured's Occupation", [
    "exec-managerial", "priv-house-serv", "craft-repair", "sales", "tech-support"])

# Map dropdowns to one-hot format
severity_map = {
    "Minor Damage": {"incident_severity_Minor Damage": 1, "incident_severity_Total Loss": 0},
    "Total Loss": {"incident_severity_Minor Damage": 0, "incident_severity_Total Loss": 1},
    "Major Damage": {"incident_severity_Minor Damage": 0, "incident_severity_Total Loss": 0},
    "Trivial Damage": {"incident_severity_Minor Damage": 0, "incident_severity_Total Loss": 0},
}
occupation_onehot = {col: 0 for col in selected_features if "insured_occupation" in col}
occupation_col = f"insured_occupation_{occupation}"
if occupation_col in occupation_onehot:
    occupation_onehot[occupation_col] = 1

# Config for numeric fields
user_input_numeric = {}
scale_config = {
    "vehicle_claim": {"min": 0, "max": 50000, "step": 500, "default": 10000},
}

for feature in selected_features:
    if feature in severity_map[incident_severity] or feature in occupation_onehot:
        continue
    config = scale_config.get(feature, {"min": 0, "max": 100, "step": 1, "default": 0})
    user_input_numeric[feature] = st.number_input(
        feature.replace('_', ' ').capitalize(),
        min_value=config["min"],
        max_value=config["max"],
        value=config["default"],
        step=config["step"]
    )

# Merge all input into one vector
final_input = {
    **user_input_numeric,
    **severity_map[incident_severity],
    **occupation_onehot
}

# Predict
if st.button("Predict Fraud"):
    input_df = pd.DataFrame([final_input])[selected_features]
    prediction = model.predict(input_df)[0]
    if prediction == 1:
        st.error("⚠️ Predicted: Fraudulent Claim")
    else:
        st.success("✅ Predicted: Legitimate Claim")
