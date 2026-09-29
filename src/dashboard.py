import streamlit as st
import pandas as pd


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Anomaly Watcher",
    page_icon="🚨",
    layout="wide"
)


# --------------------------------------------------
# Dashboard title
# --------------------------------------------------

st.title("🚨 AI Anomaly Watcher")

st.write(
    "Business data monitoring and anomaly detection dashboard"
)


# --------------------------------------------------
# Load alert report
# --------------------------------------------------

alerts = pd.read_csv(
    "data/alert_report.csv"
)


# --------------------------------------------------
# Anomaly summary
# --------------------------------------------------

total_anomalies = len(alerts)

st.metric(
    "Total Anomalies",
    total_anomalies
)


# --------------------------------------------------
# Severity summary
# --------------------------------------------------

critical_alerts = len(
    alerts[alerts["severity"] == "Critical"]
)

high_alerts = len(
    alerts[alerts["severity"] == "High"]
)

medium_alerts = len(
    alerts[alerts["severity"] == "Medium"]
)


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Critical Alerts",
        critical_alerts
    )


with col2:
    st.metric(
        "High Alerts",
        high_alerts
    )


with col3:
    st.metric(
        "Medium Alerts",
        medium_alerts
    )


# --------------------------------------------------
# Severity filter
# --------------------------------------------------

severity_filter = st.selectbox(
    "Filter by Severity",
    ["All", "Critical", "High", "Medium"]
)


# --------------------------------------------------
# Date filter
# --------------------------------------------------

date_filter = st.selectbox(
    "Filter by Date",
    ["All"] + sorted(
        alerts["Date"].astype(str).unique().tolist()
    )
)


# --------------------------------------------------
# Apply severity filter
# --------------------------------------------------

if severity_filter == "All":

    filtered_alerts = alerts

else:

    filtered_alerts = alerts[
        alerts["severity"] == severity_filter
    ]


# --------------------------------------------------
# Apply date filter
# --------------------------------------------------

if date_filter != "All":

    filtered_alerts = filtered_alerts[
        filtered_alerts["Date"].astype(str) == date_filter
    ]


# --------------------------------------------------
# Check filtered data
# --------------------------------------------------

if filtered_alerts.empty:

    st.info(
        "No anomalies found for the selected filters."
    )

else:

    # --------------------------------------------------
    # Display detected anomalies
    # --------------------------------------------------

    st.subheader("Detected Anomalies")

    st.dataframe(
        filtered_alerts[
            [
                "Date",
                "metric",
                "value",
                "change_percent",
                "severity"
            ]
        ],
        width="stretch"
    )


    # --------------------------------------------------
    # Alert details
    # --------------------------------------------------

    st.subheader("Alert Details")

    st.dataframe(
        filtered_alerts[
            [
                "Date",
                "metric",
                "value",
                "change_percent",
                "severity"
            ]
        ],
        width="stretch"
    )


    # --------------------------------------------------
    # Business explanation
    # --------------------------------------------------

    st.subheader("Business Explanation")


    for _, row in filtered_alerts.iterrows():

        direction = (
            "increased"
            if row["change_percent"] > 0
            else "decreased"
        )


        # Severity message

        if row["severity"] == "Critical":

            st.error(
                "🚨 Critical Alert"
            )

        elif row["severity"] == "High":

            st.warning(
                "⚠️ High Alert"
            )

        else:

            st.info(
                "ℹ️ Medium Alert"
            )


        # Business explanation

        st.write(
            f"**{row['metric']}** {direction} by "
            f"{abs(row['change_percent']):.1f}% "
            f"from its average. "
            f"Current value: {row['value']}. "
            f"Severity: {row['severity']}."
        )


    # --------------------------------------------------
    # Anomaly change chart
    # --------------------------------------------------

    st.subheader("Anomaly Change (%)")


    chart_data = filtered_alerts.set_index(
        "metric"
    )["change_percent"]


    st.bar_chart(
        chart_data
    )