import pandas as pd
import os
import subprocess
import streamlit as st
import sys

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Anomaly Watcher",
    page_icon="🚨",
    layout="wide"
)


# ============================================================
# CUSTOM DASHBOARD STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       MAIN APPLICATION
       ====================================================== */

    .stApp {
        background-color: #F5F7FA;
    }

    .block-container { 
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ======================================================
       HEADER
       ====================================================== */

    .dashboard-header {
        background-color: #FFFFFF;
        padding: 26px 30px;
        border-radius: 16px;
        border: 1px solid #E5E7EB;
        margin-bottom: 28px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .dashboard-title {
        margin: 0;
        font-size: 36px;
        font-weight: 700;
        color: #111827 !important;
    }

    .dashboard-subtitle {
        margin: 8px 0 0 0;
        font-size: 16px;
        color: #4B5563 !important;
    }


    /* ======================================================
       SECTION HEADINGS
       ====================================================== */

    .section-title {
        color: #111827 !important;
        font-size: 25px;
        font-weight: 700;
        margin-top: 28px;
        margin-bottom: 16px;
    }


    /* ======================================================
       KPI CARDS
       ====================================================== */

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 20px 18px;
        border-radius: 14px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        min-height: 105px;
    }

    div[data-testid="stMetricLabel"] {
        color: #4B5563 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #111827 !important;
        font-size: 29px !important;
        font-weight: 700 !important;
    }


    /* ======================================================
       GENERAL TEXT
       ====================================================== */

    p {
        color: #1F2937;
    }

    label {
        color: #374151 !important;
        font-weight: 600 !important;
    }

    .stMarkdown {
        color: #1F2937;
    }


    /* ======================================================
       SELECTBOX
       ====================================================== */

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 10px !important;
    }


    /* ======================================================
       DATAFRAME
       ====================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #E5E7EB;
    }


    /* ======================================================
       ALERT BOX TEXT
       ====================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* ======================================================
       DIVIDERS
       ====================================================== */

    hr {
        border: none;
        border-top: 1px solid #E5E7EB;
        margin-top: 28px;
        margin-bottom: 28px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="dashboard-header">
    <h1 class="dashboard-title">🚨 AI Anomaly Watcher</h1>
    <p class="dashboard-subtitle">
        AI-powered business data monitoring and anomaly detection system
    </p>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# GENERATE REPORTS IF THEY DO NOT EXIST
# ============================================================

if not os.path.exists("data/alert_report.csv"):

    result = subprocess.run(
        [sys.executable, "src/anomaly_detector.py"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        st.error("Unable to generate anomaly reports.")
        st.code(result.stderr)
        st.stop()


if not os.path.exists("data/ml_anomaly_report.csv"):

    result = subprocess.run(
        [sys.executable, "src/ml_anomaly_detector.py"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        st.error("Unable to generate ML anomaly report.")
        st.code(result.stderr)
        st.stop()


# ============================================================
# LOAD ANOMALY REPORT
# ============================================================

alerts = pd.read_csv(
    "data/alert_report.csv"
)


# ============================================================
# LOAD ML REPORT
# ============================================================

ml_report = pd.read_csv(
    "data/ml_anomaly_report.csv"
)


# ============================================================
# CREATE READABLE ML STATUS
# ============================================================

ml_report["ML_Status"] = ml_report[
    "ML_Anomaly"
].apply(
    lambda x: "🤖 ML Detected"
    if str(x).lower() == "true"
    else "✓ Not Detected"
)


# ============================================================
# LOAD ALERT HISTORY
# ============================================================

history_file = "data/alert_history.csv"

try:

    alert_history = pd.read_csv(
        history_file
    )

except FileNotFoundError:

    alert_history = pd.DataFrame()


# ============================================================
# ANOMALY COUNTS
# ============================================================

total_anomalies = len(alerts)

critical_alerts = len(
    alerts[
        alerts["severity"] == "Critical"
    ]
)

high_alerts = len(
    alerts[
        alerts["severity"] == "High"
    ]
)

medium_alerts = len(
    alerts[
        alerts["severity"] == "Medium"
    ]
)

low_alerts = len(
    alerts[
        alerts["severity"] == "Low"
    ]
)


# ============================================================
# ANOMALY OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">📊 Anomaly Overview</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Total Anomalies",
        total_anomalies
    )


with col2:

    st.metric(
        "🚨 Critical",
        critical_alerts
    )


with col3:

    st.metric(
        "⚠️ High",
        high_alerts
    )


with col4:

    st.metric(
        "ℹ️ Medium",
        medium_alerts
    )


with col5:

    st.metric(
        "🟢 Low",
        low_alerts
    )


st.divider()


# ============================================================
# FILTER ANOMALIES
# ============================================================

st.markdown(
    '<div class="section-title">🔎 Filter Anomalies</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


with col1:

    severity_filter = st.selectbox(
        "Filter by Severity",
        [
            "All",
            "Critical",
            "High",
            "Medium",
            "Low"
        ]
    )


with col2:

    date_filter = st.selectbox(
        "Filter by Date",
        [
            "All"
        ]
        + sorted(
            alerts["Date"]
            .astype(str)
            .unique()
            .tolist()
        )
    )


# ============================================================
# APPLY SEVERITY FILTER
# ============================================================

if severity_filter == "All":

    filtered_alerts = alerts.copy()

else:

    filtered_alerts = alerts[
        alerts["severity"] == severity_filter
    ].copy()


# ============================================================
# APPLY DATE FILTER
# ============================================================

if date_filter != "All":

    filtered_alerts = filtered_alerts[
        filtered_alerts["Date"]
        .astype(str)
        == date_filter
    ].copy()


# ============================================================
# PREPARE ML STATUS
# ============================================================

ml_columns = ml_report[
    [
        "Date",
        "ML_Status"
    ]
].copy()


ml_columns["Date"] = (
    pd.to_datetime(
        ml_columns["Date"]
    )
    .dt.strftime("%Y-%m-%d")
)


# ============================================================
# STANDARDIZE ALERT DATE
# ============================================================

if not filtered_alerts.empty:

    filtered_alerts["Date"] = (
        pd.to_datetime(
            filtered_alerts["Date"]
        )
        .dt.strftime("%Y-%m-%d")
    )


# ============================================================
# MERGE ML STATUS
# ============================================================

if not filtered_alerts.empty:

    filtered_alerts = filtered_alerts.merge(
        ml_columns,
        on="Date",
        how="left"
    )


# ============================================================
# DETECTED ANOMALIES
# ============================================================

st.markdown(
    '<div class="section-title">🚨 Detected Anomalies</div>',
    unsafe_allow_html=True
)


if filtered_alerts.empty:

    st.info(
        "No anomalies found for the selected filters."
    )

else:

    display_columns = [
        "Date",
        "metric",
        "value",
        "change_percent",
        "severity",
        "ML_Status",
        "ML_Anomaly_Score",
        "Explanation"
    ]

    st.dataframe(
        filtered_alerts[
            display_columns
        ],
        width="stretch",
        hide_index=False
    )


# ============================================================
# BUSINESS IMPACT SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">📌 Business Impact Summary</div>',
    unsafe_allow_html=True
)


if filtered_alerts.empty:

    st.info(
        "No business impact detected for the selected filters."
    )

else:

    critical_metrics = (
        filtered_alerts[
            filtered_alerts["severity"] == "Critical"
        ]["metric"]
        .tolist()
    )

    high_metrics = (
        filtered_alerts[
            filtered_alerts["severity"] == "High"
        ]["metric"]
        .tolist()
    )


    if critical_metrics:

        st.error(
            "🚨 Critical metrics requiring attention: "
            + ", ".join(
                critical_metrics
            )
        )


    if high_metrics:

        st.warning(
            "⚠️ High-priority metrics: "
            + ", ".join(
                high_metrics
            )
        )


    st.write(
        f"**{len(filtered_alerts)}** "
        "anomaly/anomalies identified "
        "in the selected data."
    )


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">💡 Business Insights</div>',
    unsafe_allow_html=True
)


if filtered_alerts.empty:

    st.info(
        "No business insights available."
    )

else:

    for _, row in filtered_alerts.iterrows():

        direction = (
            "increased"
            if row["change_percent"] > 0
            else "decreased"
        )

        change = abs(
            row["change_percent"]
        )


        if row["severity"] == "Critical":

            st.error(
                f"🚨 Critical: "
                f"{row['metric']} "
                f"{direction} "
                f"by {change:.1f}%."
            )


        elif row["severity"] == "High":

            st.warning(
                f"⚠️ High: "
                f"{row['metric']} "
                f"{direction} "
                f"by {change:.1f}%."
            )


        elif row["severity"] == "Medium":

            st.info(
                f"ℹ️ Medium: "
                f"{row['metric']} "
                f"{direction} "
                f"by {change:.1f}%."
            )


        else:

            st.success(
                f"🟢 Low: "
                f"{row['metric']} "
                f"{direction} "
                f"by {change:.1f}%."
            )


        st.write(
            row["Explanation"]
        )


# ============================================================
# ANOMALY CHANGE CHART
# ============================================================

if not filtered_alerts.empty:

    st.markdown(
        '<div class="section-title">📈 Anomaly Change (%)</div>',
        unsafe_allow_html=True
    )


    chart_data = (
        filtered_alerts
        .set_index("metric")
        ["change_percent"]
    )


    st.bar_chart(
        chart_data
    )


# ============================================================
# ML ANOMALY DETECTION
# ============================================================

st.divider()


st.markdown(
    '<div class="section-title">🤖 ML Anomaly Detection</div>',
    unsafe_allow_html=True
)


ml_anomalies = ml_report[
    ml_report["ML_Anomaly"].astype(str).str.lower() == "true"
]


st.write(
    f"ML model detected "
    f"**{len(ml_anomalies)}** "
    f"anomalous record(s)."
)


if ml_anomalies.empty:

    st.success(
        "No anomalies were detected by the ML model."
    )

else:

    st.warning(
        "⚠️ ML model detected unusual business activity."
    )


    ml_display = ml_anomalies[
        [
            "Date",
            "ML_Anomaly_Score"
        ]
    ].copy()


    ml_display["Date"] = (
        pd.to_datetime(
            ml_display["Date"]
        )
        .dt.strftime("%Y-%m-%d")
    )


    st.dataframe(
        ml_display,
        width="stretch"
    )


# ============================================================
# ALERT HISTORY
# ============================================================

st.divider()


st.markdown(
    '<div class="section-title">📜 Alert History</div>',
    unsafe_allow_html=True
)


if alert_history.empty:

    st.info(
        "No alert history available."
    )

else:

    st.write(
        f"Total historical alerts: "
        f"**{len(alert_history)}**"
    )


    st.dataframe(
        alert_history,
        width="stretch"
    )