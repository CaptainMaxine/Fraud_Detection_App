# Insurance Fraud Detection App — Feature Overview & Transformation Roadmap

This document summarizes feature selection, input transformations, and meaning of each model feature used in the deployed insurance fraud detection app.

---

## ✅ Selected Model Features & Interpretations
The model uses the top 5 features identified by XGBoost based on predictive importance:

1. **`incident_severity_Total Loss`** *(one-hot)*  
   Indicates whether the reported incident resulted in a total loss of the vehicle. A total loss means the cost of repair exceeds the vehicle's value.

2. **`incident_severity_Minor Damage`** *(one-hot)*  
   Indicates whether the incident involved only minor damage. Useful to contrast low severity with high claim amounts.

3. **`vehicle_claim`** *(continuous)*  
   The monetary amount claimed by the insured party for vehicle damage. Higher values may suggest increased fraud risk.

4. **`insured_occupation_exec-managerial`** *(one-hot)*  
   Indicates whether the insured works in an executive or managerial role. Occupation may correlate with claim patterns.

5. **`insured_occupation_priv-house-serv`** *(one-hot)*  
   Indicates whether the insured is employed in private household service. Used to detect potential fraud trends across occupations.

---

## Feature Transformation in the App
To enhance user experience, complex one-hot encoded features are derived from dropdown selections and numeric input.

### ⬇️ Dropdown Inputs (Mapped Internally)

#### ▼ **Incident Severity** → Maps to two one-hot features:
- **Minor Damage** → `incident_severity_Minor Damage = 1`, `incident_severity_Total Loss = 0`
- **Total Loss** → `incident_severity_Minor Damage = 0`, `incident_severity_Total Loss = 1`
- **Major Damage / Trivial Damage** → both = 0

#### ▼ **Insured's Occupation** → Maps to one-hot encoding:
- **exec-managerial** → `insured_occupation_exec-managerial = 1`
- **priv-house-serv** → `insured_occupation_priv-house-serv = 1`
- **Other** → both = 0

Only one occupation feature is marked `1`; all others default to `0`.

---

### ➕ Numeric Input

#### ▶ **Vehicle Claim Amount**
- User inputs the total dollar amount claimed for vehicle damage.
- If no claim was filed, the value should be `0`.
- This is passed to the model directly as `vehicle_claim`.

---

## ⚖️ Example Input Vector Sent to Model:
```json
{
  "vehicle_claim": 6500,
  "incident_severity_Minor Damage": 1,
  "incident_severity_Total Loss": 0,
  "insured_occupation_exec-managerial": 0,
  "insured_occupation_priv-house-serv": 1
}
```

---

## \U0001F4CA Model Prediction Flow
1. User selects values via dropdowns or numeric fields
2. App transforms inputs into one-hot encoded vector
3. Model receives the feature-aligned vector and returns a fraud prediction

---

## ⚠️ Ethics Note
- Categorical features like occupation may carry historical bias; use predictions with care.
- This model provides a probability-based suggestion — not a final decision.
- Always supplement with manual review and contextual information.

