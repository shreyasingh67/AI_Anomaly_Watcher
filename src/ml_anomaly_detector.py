import pandas as pd

from sklearn.ensemble import IsolationForest

from data_cleaner import load_data
from data_cleaner import clean_data


# -----------------------------------------
# Load and clean business data
# -----------------------------------------

data = load_data(
    "data/business_data.csv"
)

data = clean_data(
    data
)


# -----------------------------------------
# Select business metrics for ML model
# -----------------------------------------

features = [
    "Revenue",
    "Orders",
    "Conversion_Rate",
    "Traffic",
    "Cost",
    "Refunds"
]

X = data[features]


# -----------------------------------------
# Create Isolation Forest model
# -----------------------------------------

model = IsolationForest(
    contamination=0.15,
    random_state=42
)


# -----------------------------------------
# Train the model
# -----------------------------------------

model.fit(X)


# -----------------------------------------
# Predict anomalies
# -----------------------------------------

data["ML_Prediction"] = model.predict(X)


# Isolation Forest:
#  1  = Normal
# -1  = Anomaly

data["ML_Anomaly"] = (
    data["ML_Prediction"] == -1
)


# -----------------------------------------
# Anomaly Score
# -----------------------------------------

data["ML_Anomaly_Score"] = (
    model.decision_function(X)
)


# -----------------------------------------
# Display results
# -----------------------------------------

print(
    "\n========== ML ANOMALY DETECTION =========="
)

for index, row in data.iterrows():

    status = (
        "ANOMALY"
        if row["ML_Anomaly"]
        else "Normal"
    )

    print(
        f"{row['Date'].date()} | "
        f"{status} | "
        f"Score: "
        f"{row['ML_Anomaly_Score']:.4f}"
    )


# -----------------------------------------
# Save ML report
# -----------------------------------------

data.to_csv(
    "data/ml_anomaly_report.csv",
    index=False
)


print(
    "\nML anomaly report saved successfully."
)