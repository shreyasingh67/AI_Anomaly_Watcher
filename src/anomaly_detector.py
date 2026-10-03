import os
import pandas as pd
from sklearn.ensemble import IsolationForest

from data_cleaner import load_data, clean_data, validate_data
from explanation_generator import generate_explanation
from alert_manager import create_alert, save_alert_history


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "data/business_data.csv"
ANOMALY_REPORT = "data/anomaly_report.csv"
ALERT_REPORT = "data/alert_report.csv"

metrics = [
    "price_inr",
    "quantity_sold",
    "total_sales_inr",
    "profit_inr"
]


# ============================================================
# LOAD DATA
# ============================================================

print("\n========== DATA LOADING ==========")

try:
    data = load_data(INPUT_FILE)

    print("Dataset loaded successfully.")
    print(f"Rows: {len(data)}")
    print(f"Columns: {len(data.columns)}")

except Exception as error:
    print("\nERROR WHILE LOADING DATA:")
    print(error)
    raise SystemExit


# ============================================================
# CLEAN DATA
# ============================================================

print("\n========== DATA CLEANING ==========")

try:
    data = clean_data(data)

    print("Data cleaning completed successfully.")

except Exception as error:
    print("\nERROR WHILE CLEANING DATA:")
    print(error)
    raise SystemExit


# ============================================================
# VALIDATE DATA
# ============================================================

try:
    validate_data(data)

except Exception as error:
    print("\nERROR WHILE VALIDATING DATA:")
    print(error)
    raise SystemExit


# ============================================================
# CHECK METRICS
# ============================================================

missing_metrics = [
    metric
    for metric in metrics
    if metric not in data.columns
]

if missing_metrics:

    print("\nERROR:")
    print("Missing anomaly detection metrics:")

    for metric in missing_metrics:
        print("-", metric)

    raise SystemExit


# ============================================================
# CONVERT METRICS TO NUMERIC
# ============================================================

for metric in metrics:

    data[metric] = pd.to_numeric(
        data[metric],
        errors="coerce"
    )


data = data.dropna(
    subset=metrics
).copy()


# ============================================================
# MACHINE LEARNING ANOMALY DETECTION
# ============================================================

print(
    "\n========== MACHINE LEARNING ANOMALY DETECTION =========="
)

try:

    model = IsolationForest(
        contamination=0.15,
        random_state=42
    )

    model.fit(
        data[metrics]
    )

    predictions = model.predict(
        data[metrics]
    )

    scores = model.decision_function(
        data[metrics]
    )

    data["ML_Anomaly"] = (
        predictions == -1
    )

    data["ML_Anomaly_Score"] = scores

    print(
        "Isolation Forest anomaly detection completed."
    )

    print(
        "ML anomalies detected:",
        int(data["ML_Anomaly"].sum())
    )

except Exception as error:

    print(
        "\nWARNING: ML detection failed."
    )

    print(error)

    data["ML_Anomaly"] = False
    data["ML_Anomaly_Score"] = 0.0


# ============================================================
# STATISTICAL ANALYSIS
# ============================================================

print(
    "\n========== STATISTICAL ANALYSIS =========="
)

statistics = {}

for metric in metrics:

    series = pd.to_numeric(
        data[metric],
        errors="coerce"
    )

    average = float(
        series.mean()
    )

    std = float(
        series.std()
    )

    statistics[metric] = {
        "average": average,
        "std": std
    }

    data[f"{metric}_Average"] = average
    data[f"{metric}_Std"] = std


# ============================================================
# Z-SCORE CALCULATION
# ============================================================

print(
    "\n========== Z-SCORE CALCULATION =========="
)

for metric in metrics:

    average = statistics[
        metric
    ]["average"]

    std = statistics[
        metric
    ]["std"]

    if std == 0 or pd.isna(std):

        data[
            f"{metric}_ZScore"
        ] = 0.0

    else:

        data[
            f"{metric}_ZScore"
        ] = (
            data[metric] - average
        ) / std

    data[
        f"{metric}_Anomaly"
    ] = (
        data[
            f"{metric}_ZScore"
        ].abs() >= 2
    )


# ============================================================
# PERCENTAGE CHANGE
# ============================================================

print(
    "\n========== PERCENTAGE CHANGE =========="
)

for metric in metrics:

    average = statistics[
        metric
    ]["average"]

    if average == 0 or pd.isna(average):

        data[
            f"{metric}_Change_Percent"
        ] = 0.0

    else:

        data[
            f"{metric}_Change_Percent"
        ] = (
            (
                data[metric] - average
            )
            / average
        ) * 100


# ============================================================
# CREATE ALERTS
# ============================================================

print(
    "\n========== ANOMALY DETECTION =========="
)

all_alerts = []


for index, row in data.iterrows():

    for metric in metrics:

        statistical_anomaly = bool(
            row[
                f"{metric}_Anomaly"
            ]
        )

        ml_anomaly = bool(
            row["ML_Anomaly"]
        )

        # ----------------------------------------------------
        # Only create alert when anomaly is detected
        # ----------------------------------------------------

        if not statistical_anomaly:
          continue


        value = float(
            row[metric]
        )

        change_percent = float(
            row[
                f"{metric}_Change_Percent"
            ]
        )

        z_score = float(
            row[
                f"{metric}_ZScore"
            ]
        )

        ml_score = float(
            row["ML_Anomaly_Score"]
        )


        # ----------------------------------------------------
        # CREATE ALERT
        # ----------------------------------------------------

        alert = create_alert(
            metric,
            value,
            change_percent
        )


        # ----------------------------------------------------
        # SAFETY: MAKE SURE ALERT IS A DICTIONARY
        # ----------------------------------------------------

        if not isinstance(
            alert,
            dict
        ):

            alert = {
                "Metric": metric,
                "Value": value,
                "Change_Percent": change_percent,
                "Severity": "Low"
            }


        # ----------------------------------------------------
        # SAFETY: ENSURE SEVERITY EXISTS
        # ----------------------------------------------------

        if (
            "Severity" not in alert
            or pd.isna(
                alert["Severity"]
            )
        ):

            absolute_change = abs(
                change_percent
            )

            if absolute_change >= 100:
                severity = "Critical"

            elif absolute_change >= 50:
                severity = "High"

            elif absolute_change >= 20:
                severity = "Medium"

            else:
                severity = "Low"

            alert["Severity"] = severity


        # ----------------------------------------------------
        # BUSINESS EXPLANATION
        # ----------------------------------------------------

        try:

            explanation = generate_explanation(
                metric,
                value,
                change_percent
            )

        except Exception:

            explanation = (
                f"{metric} shows an unusual "
                f"change of "
                f"{change_percent:.2f}% "
                f"from its average."
            )


        # ----------------------------------------------------
        # ADD DATASET INFORMATION
        # ----------------------------------------------------

        alert["Date"] = row[
            "order_date"
        ]

        alert["Order_ID"] = row[
            "order_id"
        ]

        alert["Product"] = row[
            "product_name"
        ]

        alert["Category"] = row[
            "category"
        ]

        alert["Region"] = row[
            "region"
        ]

        alert["Z_Score"] = z_score

        alert["ML_Anomaly"] = ml_anomaly

        alert[
            "ML_Anomaly_Score"
        ] = ml_score

        alert[
            "Statistical_Anomaly"
        ] = statistical_anomaly

        alert[
            "Explanation"
        ] = explanation


        all_alerts.append(
            alert
        )


# ============================================================
# CREATE ALERT DATAFRAME
# ============================================================

alert_columns = [
    "Metric",
    "Value",
    "Change_Percent",
    "Severity",
    "Date",
    "Order_ID",
    "Product",
    "Category",
    "Region",
    "Z_Score",
    "ML_Anomaly",
    "ML_Anomaly_Score",
    "Statistical_Anomaly",
    "Explanation"
]


if all_alerts:

    alerts = pd.DataFrame(
        all_alerts
    )

else:

    alerts = pd.DataFrame(
        columns=alert_columns
    )


# ============================================================
# GUARANTEE REQUIRED COLUMNS
# ============================================================

for column in alert_columns:

    if column not in alerts.columns:

        alerts[column] = None


alerts = alerts[
    alert_columns
]


# ============================================================
# REMOVE DUPLICATE ALERTS
# ============================================================

duplicate_columns = [
    "Date",
    "Order_ID",
    "Metric"
]

available_duplicate_columns = [
    column
    for column in duplicate_columns
    if column in alerts.columns
]


if not alerts.empty:

    alerts = alerts.drop_duplicates(
        subset=available_duplicate_columns,
        keep="first"
    )


# ============================================================
# SAVE ALERT HISTORY
# ============================================================

try:

    if not alerts.empty:

        save_alert_history(
            alerts
        )

        print(
            "\nAlert history updated successfully."
        )

    else:

        print(
            "\nNo alerts to save."
        )

except Exception as error:

    print(
        "\nWARNING: Could not save alert history."
    )

    print(error)


# ============================================================
# SAVE ANOMALY REPORT
# ============================================================

try:

    data.to_csv(
        ANOMALY_REPORT,
        index=False
    )

    print(
        "\nAnomaly report saved:"
    )

    print(
        ANOMALY_REPORT
    )

except Exception as error:

    print(
        "\nERROR SAVING ANOMALY REPORT:"
    )

    print(error)


# ============================================================
# SAVE ALERT REPORT
# ============================================================

try:

    alerts.to_csv(
        ALERT_REPORT,
        index=False
    )

    print(
        "\nAlert report saved:"
    )

    print(
        ALERT_REPORT
    )

except Exception as error:

    print(
        "\nERROR SAVING ALERT REPORT:"
    )

    print(error)


# ============================================================
# FINAL SUMMARY
# ============================================================

print(
    "\n=============================================="
)

print(
    "       ANOMALY DETECTION COMPLETED"
)

print(
    "=============================================="
)

print(
    f"Total dataset rows: {len(data)}"
)

print(
    f"Total alerts generated: {len(alerts)}"
)


# ============================================================
# SEVERITY SUMMARY
# ============================================================

print(
    "\n========== ALERT SEVERITY SUMMARY =========="
)


if (
    not alerts.empty
    and "Severity" in alerts.columns
):

    severity_counts = (
        alerts["Severity"]
        .value_counts()
    )

    for severity, count in (
        severity_counts.items()
    ):

        print(
            f"{severity}: {count}"
        )

else:

    print(
        "No alerts available."
    )


# ============================================================
# SAMPLE DETECTED ANOMALIES
# ============================================================

print(
    "\n========== SAMPLE DETECTED ANOMALIES =========="
)


if not alerts.empty:

    display_columns = [
        "Date",
        "Order_ID",
        "Product",
        "Metric",
        "Value",
        "Change_Percent",
        "Severity"
    ]

    available_columns = [
        column
        for column in display_columns
        if column in alerts.columns
    ]

    print(
        alerts[
            available_columns
        ]
        .head(10)
        .to_string(index=False)
    )

else:

    print(
        "No anomalies detected."
    )


print(
    "\nProcessing completed successfully."
)