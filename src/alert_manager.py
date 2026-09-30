import os
from datetime import datetime

import pandas as pd


# --------------------------------------------------
# Create an alert
# --------------------------------------------------

def create_alert(metric, value, change):

    alert = {
        "metric": metric,
        "value": value,
        "change_percent": round(change, 2),
        "severity": determine_severity(change)
    }

    return alert


# --------------------------------------------------
# Determine alert severity
# --------------------------------------------------

def determine_severity(change):

    change = abs(change)

    if change >= 100:
        return "Critical"

    elif change >= 50:
        return "High"

    elif change >= 20:
        return "Medium"

    else:
        return "Low"


# --------------------------------------------------
# Save alert history
# --------------------------------------------------

def save_alert_history(alerts):

    history_file = "data/alert_history.csv"

    # No alerts
    if not alerts:

        print("No alerts to save.")

        return


    # Convert new alerts into DataFrame
    new_history = pd.DataFrame(alerts)


    # Make Date format consistent
    new_history["Date"] = (
        pd.to_datetime(
            new_history["Date"],
            errors="coerce"
        )
        .dt.strftime("%Y-%m-%d")
    )


    # Add monitoring timestamp
    new_history["monitoring_time"] = (
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )


    # If history file does not exist
    if not os.path.exists(history_file):

        new_history.to_csv(
            history_file,
            index=False
        )

        print(
            "Alert history created."
        )

        return


    # Load existing history
    old_history = pd.read_csv(
        history_file
    )


    # Make existing Date format consistent
    if "Date" in old_history.columns:

        old_history["Date"] = (
            pd.to_datetime(
                old_history["Date"],
                errors="coerce"
            )
            .dt.strftime("%Y-%m-%d")
        )


    # Combine old and new alerts
    updated_history = pd.concat(
        [
            old_history,
            new_history
        ],
        ignore_index=True
    )


    # Columns used to identify
    # the same alert
    duplicate_columns = [
        "Date",
        "metric",
        "value",
        "change_percent",
        "severity"
    ]


    # Remove duplicate alerts
    updated_history = (
        updated_history
        .drop_duplicates(
            subset=duplicate_columns,
            keep="last"
        )
    )


    # Save cleaned history
    updated_history.to_csv(
        history_file,
        index=False
    )


    print(
        "Alert history updated."
    )