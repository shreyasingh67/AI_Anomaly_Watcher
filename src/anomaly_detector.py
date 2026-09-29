import pandas as pd
from explanation_generator import generate_explanation
from alert_manager import create_alert


# --------------------------------------------------
# Load business data
# --------------------------------------------------

data = pd.read_csv(
    "data/business_data.csv",
    parse_dates=["Date"]
)

print(data)


# --------------------------------------------------
# List of business metrics
# --------------------------------------------------

metrics = [
    "Revenue",
    "Orders",
    "Conversion_Rate",
    "Traffic",
    "Cost",
    "Refunds"
]


# --------------------------------------------------
# Check each metric
# --------------------------------------------------

for metric in metrics:

    print(
        "Checking metric:",
        metric
    )


# --------------------------------------------------
# Calculate average of each metric
# --------------------------------------------------

for metric in metrics:

    average = data[metric].mean()

    print(
        f"{metric} Average:",
        average
    )


# --------------------------------------------------
# Calculate anomaly thresholds
# --------------------------------------------------

thresholds = {}

for metric in metrics:

    average = data[metric].mean()

    thresholds[metric] = average * 1.5


print("Metric Thresholds:")
print(thresholds)


# --------------------------------------------------
# Detect high and low anomalies
# --------------------------------------------------

for metric in metrics:

    average = data[metric].mean()

    upper_threshold = average * 1.5

    lower_threshold = average * 0.6

    data[f"{metric}_Anomaly"] = (
        (data[metric] > upper_threshold) |
        (data[metric] < lower_threshold)
    )


# --------------------------------------------------
# Display all metric anomalies
# --------------------------------------------------

print("All Metric Anomalies:")

print(
    data[
        ["Date"] +
        [f"{metric}_Anomaly" for metric in metrics]
    ]
)


# --------------------------------------------------
# Revenue anomaly detection
# --------------------------------------------------

normal_revenue = data["Revenue"].mean()

print(
    "Average Revenue:",
    normal_revenue
)


revenue_threshold = normal_revenue * 1.5

print(
    "Revenue Threshold:",
    revenue_threshold
)


data["Revenue_Anomaly"] = (
    data["Revenue"] > revenue_threshold
)


print(
    data[
        ["Date", "Revenue", "Revenue_Anomaly"]
    ]
)


# --------------------------------------------------
# Get detected Revenue anomalies
# --------------------------------------------------

anomalies = data[
    data["Revenue_Anomaly"]
]


print("Detected Revenue Anomalies:")

print(
    anomalies[
        ["Date", "Revenue"]
    ]
)


# --------------------------------------------------
# Calculate Revenue change percentage
# --------------------------------------------------

data["Revenue_Change_Percent"] = (
    (data["Revenue"] - normal_revenue)
    / normal_revenue
) * 100


print(
    data[
        [
            "Date",
            "Revenue",
            "Revenue_Change_Percent"
        ]
    ]
)


# --------------------------------------------------
# Generate Revenue explanation
# --------------------------------------------------

anomalies = data[
    data["Revenue_Anomaly"]
]


for _, row in anomalies.iterrows():

    print(
        f"Revenue anomaly detected on "
        f"{row['Date'].date()}: "
        f"Revenue was ₹{row['Revenue']:,}, "
        f"which is "
        f"{row['Revenue_Change_Percent']:.1f}% "
        f"above the average."
    )


# --------------------------------------------------
# Display all detected anomalies
# --------------------------------------------------

print("\nDetected Anomalies:")


for metric in metrics:

    anomaly_column = f"{metric}_Anomaly"

    detected = data[
        data[anomaly_column]
    ]

    if not detected.empty:

        print(
            f"\n{metric} Anomalies:"
        )

        print(
            detected[
                ["Date", metric]
            ]
        )


# --------------------------------------------------
# Calculate percentage change for all metrics
# --------------------------------------------------

print("\nAnomaly Percentage Changes:")


for metric in metrics:

    average = data[metric].mean()

    data[
        f"{metric}_Change_Percent"
    ] = (
        (data[metric] - average)
        / average
    ) * 100

    anomaly_column = (
        f"{metric}_Anomaly"
    )

    detected = data[
        data[anomaly_column]
    ]

    if not detected.empty:

        print(
            f"\n{metric}:"
        )

        for _, row in detected.iterrows():

            print(
                f"{row['Date'].date()} -> "
                f"{row[metric]} "
                f"({row[f'{metric}_Change_Percent']:.1f}% "
                f"from average)"
            )


# --------------------------------------------------
# Business-friendly explanations
# --------------------------------------------------

print("\nBusiness Explanations:")

alerts = []


for metric in metrics:

    anomaly_column = (
        f"{metric}_Anomaly"
    )

    change_column = (
        f"{metric}_Change_Percent"
    )

    detected = data[
        data[anomaly_column]
    ]

    for _, row in detected.iterrows():

        change = row[change_column]

        alert = create_alert(
            metric,
            row[metric],
            change
        )

        # Add anomaly date to alert
        alert["Date"] = row["Date"].date()

        alerts.append(alert)

        print(
            "Alert:",
            alert
        )

        explanation = generate_explanation(
            metric,
            row[metric],
            change
        )

        print(
            f"{metric} anomaly detected on "
            f"{row['Date'].date()}: "
            f"{explanation}"
        )


# --------------------------------------------------
# Anomaly summary
# --------------------------------------------------

print("\nAnomaly Summary:")


anomaly_columns = [
    f"{metric}_Anomaly"
    for metric in metrics
]


data["Total_Anomalies"] = (
    data[anomaly_columns].sum(axis=1)
)


print(
    data[
        ["Date", "Total_Anomalies"]
    ]
)


# --------------------------------------------------
# Show dates with anomalies
# --------------------------------------------------

print("\nDates with anomalies:")


anomaly_dates = data[
    data["Total_Anomalies"] > 0
]


print(
    anomaly_dates[
        ["Date", "Total_Anomalies"]
    ]
)


# --------------------------------------------------
# Save anomaly report
# --------------------------------------------------

anomaly_report = data[
    data["Total_Anomalies"] > 0
]


anomaly_report.to_csv(
    "data/anomaly_report.csv",
    index=False
)


# --------------------------------------------------
# Save alert report
# --------------------------------------------------

alert_report = pd.DataFrame(alerts)


alert_report.to_csv(
    "data/alert_report.csv",
    index=False
)


print(
    "Alert report saved successfully!"
)


print(
    "\nAnomaly report saved successfully!"
)