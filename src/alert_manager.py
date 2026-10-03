import os
from datetime import datetime
import pandas as pd


def get_severity(change_percent):
    change_percent = abs(float(change_percent))

    if change_percent >= 100:
        return "Critical"
    elif change_percent >= 50:
        return "High"
    elif change_percent >= 20:
        return "Medium"
    else:
        return "Low"


def create_alert(metric, value, change_percent):
    severity = get_severity(change_percent)

    return {
        "Metric": metric,
        "Value": float(value),
        "Change_Percent": float(change_percent),
        "Severity": severity
    }


def normalize_columns(data):
    """
    Standardize column names so old and new alert history
    files cannot create duplicate columns.
    """

    data = data.copy()

    # Remove accidental spaces
    data.columns = [str(column).strip() for column in data.columns]

    # Convert all column names to lowercase
    data.columns = [column.lower() for column in data.columns]

    # Remove duplicate columns
    data = data.loc[:, ~data.columns.duplicated()]

    return data


def save_alert_history(alerts):
    history_file = "data/alert_history.csv"

    # Convert alerts to DataFrame
    if isinstance(alerts, pd.DataFrame):
        alerts_df = alerts.copy()

    elif isinstance(alerts, list):
        if len(alerts) == 0:
            return

        alerts_df = pd.DataFrame(alerts)

    else:
        alerts_df = pd.DataFrame(alerts)

    # Check if DataFrame is empty
    if alerts_df.empty:
        return

    # Normalize new alert columns
    alerts_df = normalize_columns(alerts_df)

    # Add monitoring timestamp
    alerts_df["monitoring_time"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Create data folder if needed
    os.makedirs("data", exist_ok=True)

    # Load existing history
    if os.path.exists(history_file):

        try:
            existing_history = pd.read_csv(history_file)

            # Normalize old history columns too
            existing_history = normalize_columns(existing_history)

        except Exception:
            existing_history = pd.DataFrame()

    else:
        existing_history = pd.DataFrame()

    # Combine old and new alerts
    if existing_history.empty:

        combined_history = alerts_df

    else:

        combined_history = pd.concat(
            [existing_history, alerts_df],
            ignore_index=True
        )

    # Remove duplicate alerts
    duplicate_columns = [
        "date",
        "order_id",
        "metric",
        "value",
        "change_percent"
    ]

    available_columns = [
        column
        for column in duplicate_columns
        if column in combined_history.columns
    ]

    if available_columns:

        combined_history = combined_history.drop_duplicates(
            subset=available_columns,
            keep="last"
        )

    # Save cleaned alert history
    combined_history.to_csv(
        history_file,
        index=False
    )

    print("\nAlert history saved successfully:")
    print(history_file)