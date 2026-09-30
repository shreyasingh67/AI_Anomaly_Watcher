import pandas as pd
from sklearn.ensemble import IsolationForest

from data_cleaner import load_data
from data_cleaner import clean_data
from data_cleaner import validate_data

from explanation_generator import generate_explanation

from alert_manager import create_alert
from alert_manager import save_alert_history


# -----------------------------------------
# Load and clean business data
# -----------------------------------------

data = load_data(
    "data/business_data.csv"
)

data = clean_data(
    data
)

validate_data(
    data
)


# -----------------------------------------
# Business metrics
# -----------------------------------------

metrics = [
    "Revenue",
    "Orders",
    "Conversion_Rate",
    "Traffic",
    "Cost",
    "Refunds"
]


# -----------------------------------------
# ML-based anomaly detection
# -----------------------------------------

ml_features = data[metrics]

ml_model = IsolationForest(
    contamination=0.15,
    random_state=42
)

ml_model.fit(
    ml_features
)

data["ML_Prediction"] = ml_model.predict(
    ml_features
)

data["ML_Anomaly"] = (
    data["ML_Prediction"] == -1
)

data["ML_Anomaly_Score"] = (
    ml_model.decision_function(
        ml_features
    )
)


# -----------------------------------------
# Calculate averages and standard deviation
# -----------------------------------------

for metric in metrics:

    data[f"{metric}_Average"] = (
        data[metric].mean()
    )

    data[f"{metric}_Std"] = (
        data[metric].std()
    )


# -----------------------------------------
# Calculate Z-Scores
# -----------------------------------------

for metric in metrics:

    data[f"{metric}_ZScore"] = (
        (
            data[metric]
            - data[f"{metric}_Average"]
        )
        / data[f"{metric}_Std"]
    )

    data[f"{metric}_Anomaly"] = (
        data[f"{metric}_ZScore"].abs() >= 2
    )


# -----------------------------------------
# Calculate percentage change
# -----------------------------------------

for metric in metrics:

    data[f"{metric}_Change_Percent"] = (
        (
            data[metric]
            - data[f"{metric}_Average"]
        )
        / data[f"{metric}_Average"]
    ) * 100


# -----------------------------------------
# Detect anomalies
# -----------------------------------------

print(
    "\n========== DETECTED ANOMALIES =========="
)

alerts = []


for index, row in data.iterrows():

    for metric in metrics:

        anomaly_column = (
            f"{metric}_Anomaly"
        )

        if row[anomaly_column]:

            change = row[
                f"{metric}_Change_Percent"
            ]

            # ---------------------------------
            # Create alert
            # ---------------------------------

            alert = create_alert(
                metric,
                row[metric],
                change
            )

            # ---------------------------------
            # Add ML detection information
            # ---------------------------------

            alert["ML_Detected"] = bool(
                row["ML_Anomaly"]
            )

            alert["ML_Anomaly_Score"] = round(
                row["ML_Anomaly_Score"],
                4
            )

            # ---------------------------------
            # Add date
            # ---------------------------------

            alert["Date"] = (
                row["Date"].date()
            )

            # ---------------------------------
            # Generate business explanation
            # ---------------------------------

            alert["Explanation"] = (
                generate_explanation(
                    metric,
                    row[metric],
                    change
                )
            )

            # ---------------------------------
            # Store alert
            # ---------------------------------

            alerts.append(
                alert
            )

            # ---------------------------------
            # Display anomaly
            # ---------------------------------

            print(
                f"{metric}: "
                f"{row[metric]} | "
                f"Z-Score: "
                f"{row[f'{metric}_ZScore']:.2f} | "
                f"Change: "
                f"{change:.2f}% | "
                f"ML Detected: "
                f"{row['ML_Anomaly']}"
            )

            print(
                "ML Anomaly Score:",
                f"{row['ML_Anomaly_Score']:.4f}"
            )

            print(
                "Explanation:",
                alert["Explanation"]
            )

            print(
                "----------------------------------"
            )


# -----------------------------------------
# Total anomalies
# -----------------------------------------

print(
    "\nTotal Anomalies:",
    len(alerts)
)


# -----------------------------------------
# Save alert history
# -----------------------------------------

save_alert_history(
    alerts
)


# -----------------------------------------
# Save complete anomaly report
# -----------------------------------------

data.to_csv(
    "data/anomaly_report.csv",
    index=False
)


# -----------------------------------------
# Save alert report
# -----------------------------------------

alert_report = pd.DataFrame(
    alerts
)

alert_report.to_csv(
    "data/alert_report.csv",
    index=False
)


print(
    "\nReports saved successfully."
)