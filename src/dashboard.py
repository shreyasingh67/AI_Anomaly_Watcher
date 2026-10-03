import os
import sys
import subprocess
import pandas as pd
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Anomaly Watcher",
    page_icon="chart",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# PROFESSIONAL LIGHT THEME
# ============================================================

st.markdown(
    """
    <style>

    /* Main application */

    .stApp {
        background-color: #F5F7FA;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Text */

    h1, h2, h3, h4, h5, h6 {
        color: #111827 !important;
    }

    p {
        color: #374151 !important;
    }

    label {
        color: #374151 !important;
        font-weight: 600 !important;
    }

    /* Metric cards */

    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 14px !important;
        padding: 20px !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05) !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #4B5563 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #111827 !important;
        font-weight: 800 !important;
    }

    div[data-testid="stMetricDelta"] {
        color: #374151 !important;
    }

    /* Select boxes */

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] span {
        color: #111827 !important;
    }

    /* Input */

    input {
        color: #111827 !important;
        background-color: #FFFFFF !important;
    }

    /* Buttons */

    .stButton > button {
        border-radius: 8px;
        border: 1px solid #D1D5DB;
        background-color: #FFFFFF;
        color: #111827;
        font-weight: 600;
    }

    .stButton > button:hover {
        border-color: #6B7280;
        color: #111827;
    }

    /* Dataframe */

    div[data-testid="stDataFrame"] {
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        overflow: hidden;
    }

    /* Alerts */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Divider */

    hr {
        border-color: #E5E7EB !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.title("📊 AI Anomaly Watcher")

st.caption(
    "AI-powered Flipkart business data monitoring and anomaly detection dashboard"
)

st.divider()


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(BASE_DIR, "data")

DATA_FILE = os.path.join(
    DATA_DIR,
    "business_data.csv"
)

ALERT_FILE = os.path.join(
    DATA_DIR,
    "alert_report.csv"
)

ML_ALERT_FILE = os.path.join(
    DATA_DIR,
    "ml_anomaly_report.csv"
)

HISTORY_FILE = os.path.join(
    DATA_DIR,
    "alert_history.csv"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_columns(dataframe):

    dataframe = dataframe.copy()

    dataframe.columns = [
        str(column).strip().lower()
        for column in dataframe.columns
    ]

    return dataframe


def format_number(value):

    if pd.isna(value):
        return "0"

    return f"{value:,.0f}"


def format_currency(value):

    if pd.isna(value):
        return "₹0"

    return f"₹{value:,.0f}"


def load_csv(file_path):

    if not os.path.exists(file_path):
        return None

    try:

        dataframe = pd.read_csv(file_path)

        dataframe = normalize_columns(dataframe)

        return dataframe

    except Exception as error:

        st.error(
            f"Unable to read file: {error}"
        )

        return None


def convert_dates(dataframe):

    dataframe = dataframe.copy()

    possible_date_columns = [
        "date",
        "order_date"
    ]

    for column in possible_date_columns:

        if column in dataframe.columns:

            dataframe[column] = pd.to_datetime(
                dataframe[column],
                errors="coerce",
                dayfirst=True
            )

    return dataframe


# ============================================================
# LOAD BUSINESS DATA
# ============================================================

if not os.path.exists(DATA_FILE):

    st.error(
        "Business data file was not found."
    )

    st.info(
        "Please make sure data/business_data.csv exists."
    )

    st.stop()


data = load_csv(DATA_FILE)

if data is None or data.empty:

    st.error(
        "Business dataset is empty."
    )

    st.stop()


data = convert_dates(data)

# ============================================================
# GENERATE REPORTS IF THEY DO NOT EXIST
# ============================================================

if not os.path.exists(ALERT_FILE):

    try:

        result = subprocess.run(
            [
                sys.executable,
                os.path.join(
                    BASE_DIR,
                    "src",
                    "anomaly_detector.py"
                )
            ],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:

            st.error(
                "Unable to generate anomaly report."
            )

            st.code(
                result.stderr
            )

    except Exception as error:

        st.error(
            f"Anomaly detection failed: {error}"
        )
        
        
# ============================================================
# LOAD ALERT REPORT
# ============================================================

alerts = load_csv(ALERT_FILE)

if alerts is None:

    alerts = pd.DataFrame()


if not alerts.empty:

    alerts = convert_dates(alerts)


# ============================================================
# LOAD ML REPORT
# ============================================================

ml_alerts = load_csv(ML_ALERT_FILE)

if ml_alerts is None:

    ml_alerts = pd.DataFrame()


if not ml_alerts.empty:

    ml_alerts = convert_dates(ml_alerts)


# ============================================================
# LOAD ALERT HISTORY
# ============================================================

history = load_csv(HISTORY_FILE)

if history is None:

    history = pd.DataFrame()


if not history.empty:

    history = convert_dates(history)


# ============================================================
# DATASET INFORMATION
# ============================================================

st.subheader("📌 Dataset Overview")

overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)


with overview_col1:

    st.metric(
        "Total Records",
        format_number(len(data))
    )


with overview_col2:

    st.metric(
        "Total Columns",
        format_number(len(data.columns))
    )


with overview_col3:

    if "total_sales_inr" in data.columns:

        total_sales = data["total_sales_inr"].sum()

        st.metric(
            "Total Sales",
            format_currency(total_sales)
        )

    else:

        st.metric(
            "Total Sales",
            "N/A"
        )


with overview_col4:

    if "profit_inr" in data.columns:

        total_profit = data["profit_inr"].sum()

        st.metric(
            "Total Profit",
            format_currency(total_profit)
        )

    else:

        st.metric(
            "Total Profit",
            "N/A"
        )


st.divider()


# ============================================================
# ANOMALY KPI SECTION
# ============================================================

st.subheader("🚨 Anomaly Monitoring")


total_alerts = len(alerts)


critical_count = 0
high_count = 0
medium_count = 0
low_count = 0


if not alerts.empty and "severity" in alerts.columns:

    severity_series = (
        alerts["severity"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    critical_count = (
        severity_series == "critical"
    ).sum()

    high_count = (
        severity_series == "high"
    ).sum()

    medium_count = (
        severity_series == "medium"
    ).sum()

    low_count = (
        severity_series == "low"
    ).sum()


kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)


with kpi1:

    st.metric(
        "Total Anomalies",
        format_number(total_alerts)
    )


with kpi2:

    st.metric(
        "Critical",
        format_number(critical_count)
    )


with kpi3:

    st.metric(
        "High",
        format_number(high_count)
    )


with kpi4:

    st.metric(
        "Medium",
        format_number(medium_count)
    )


with kpi5:

    st.metric(
        "Low",
        format_number(low_count)
    )


st.divider()


# ============================================================
# FILTER SECTION
# ============================================================

st.subheader("🔎 Filter Anomalies")

if not alerts.empty:

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)


    # --------------------------------------------------------
    # Severity filter
    # --------------------------------------------------------

    with filter_col1:

        severity_options = [
            "All",
            "Critical",
            "High",
            "Medium",
            "Low"
        ]

        selected_severity = st.selectbox(
            "Severity",
            severity_options
        )


    # --------------------------------------------------------
    # Metric filter
    # --------------------------------------------------------

    with filter_col2:

        if "metric" in alerts.columns:

            metric_options = [
                "All"
            ] + sorted(
                alerts["metric"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

        else:

            metric_options = ["All"]


        selected_metric = st.selectbox(
            "Metric",
            metric_options
        )


    # --------------------------------------------------------
    # Category filter
    # --------------------------------------------------------

    with filter_col3:

        if "category" in alerts.columns:

            category_options = [
                "All"
            ] + sorted(
                alerts["category"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

        else:

            category_options = ["All"]


        selected_category = st.selectbox(
            "Category",
            category_options
        )


    # --------------------------------------------------------
    # Region filter
    # --------------------------------------------------------

    with filter_col4:

        if "region" in alerts.columns:

            region_options = [
                "All"
            ] + sorted(
                alerts["region"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

        else:

            region_options = ["All"]


        selected_region = st.selectbox(
            "Region",
            region_options
        )


    # ========================================================
    # APPLY FILTERS
    # ========================================================

    filtered_alerts = alerts.copy()


    if (
        selected_severity != "All"
        and "severity" in filtered_alerts.columns
    ):

        filtered_alerts = filtered_alerts[
            filtered_alerts["severity"]
            .astype(str)
            .str.lower()
            == selected_severity.lower()
        ]


    if (
        selected_metric != "All"
        and "metric" in filtered_alerts.columns
    ):

        filtered_alerts = filtered_alerts[
            filtered_alerts["metric"]
            .astype(str)
            == selected_metric
        ]


    if (
        selected_category != "All"
        and "category" in filtered_alerts.columns
    ):

        filtered_alerts = filtered_alerts[
            filtered_alerts["category"]
            .astype(str)
            == selected_category
        ]


    if (
        selected_region != "All"
        and "region" in filtered_alerts.columns
    ):

        filtered_alerts = filtered_alerts[
            filtered_alerts["region"]
            .astype(str)
            == selected_region
        ]


else:

    filtered_alerts = pd.DataFrame()

    st.info(
        "No anomaly report is currently available."
    )


# ============================================================
# FILTERED RESULT COUNT
# ============================================================

st.write(
    f"Showing **{len(filtered_alerts)}** anomaly records."
)


# ============================================================
# ANOMALY TABLE
# ============================================================

st.subheader("📋 Detected Anomalies")


if not filtered_alerts.empty:

    display_columns = [
        "date",
        "order_id",
        "metric",
        "value",
        "change_percent",
        "severity",
        "product",
        "category",
        "region",
        "z_score",
        "ml_anomaly",
        "explanation"
    ]


    available_columns = [
        column
        for column in display_columns
        if column in filtered_alerts.columns
    ]


    anomaly_table = filtered_alerts[
        available_columns
    ].copy()


    st.dataframe(
        anomaly_table,
        width="stretch",
        hide_index=True
    )

else:

    st.success(
        "No anomalies match the selected filters."
    )


st.divider()


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.subheader("💡 Business Insights")


if not filtered_alerts.empty:

    insight_col1, insight_col2 = st.columns(2)


    # --------------------------------------------------------
    # Most affected metric
    # --------------------------------------------------------

    with insight_col1:

        if "metric" in filtered_alerts.columns:

            metric_counts = (
                filtered_alerts["metric"]
                .value_counts()
            )


            if not metric_counts.empty:

                top_metric = metric_counts.index[0]

                top_metric_count = metric_counts.iloc[0]

                st.markdown(
                    f"### 📊 Most Affected Metric"
                )

                st.info(
                    f"{top_metric} has the highest number "
                    f"of detected anomalies with "
                    f"{top_metric_count} alerts."
                )


    # --------------------------------------------------------
    # Most affected category
    # --------------------------------------------------------

    with insight_col2:

        if "category" in filtered_alerts.columns:

            category_counts = (
                filtered_alerts["category"]
                .value_counts()
            )


            if not category_counts.empty:

                top_category = category_counts.index[0]

                top_category_count = category_counts.iloc[0]

                st.markdown(
                    f"### 🛍️ Most Affected Category"
                )

                st.info(
                    f"{top_category} has the highest number "
                    f"of detected anomaly records with "
                    f"{top_category_count} alerts."
                )


    # --------------------------------------------------------
    # Highest percentage change
    # --------------------------------------------------------

    if "change_percent" in filtered_alerts.columns:

        change_values = pd.to_numeric(
            filtered_alerts["change_percent"],
            errors="coerce"
        )


        if not change_values.dropna().empty:

            max_change_index = (
                change_values.abs()
                .idxmax()
            )


            max_change = (
                filtered_alerts
                .loc[max_change_index]
            )


            st.markdown(
                "### 📈 Largest Detected Change"
            )


            metric_name = max_change.get(
                "metric",
                "Unknown"
            )


            change_value = max_change.get(
                "change_percent",
                0
            )


            st.warning(
                f"{metric_name} recorded the largest "
                f"detected change of "
                f"{float(change_value):.2f}%."
            )


else:

    st.info(
        "Business insights will appear when anomaly records are available."
    )


st.divider()


# ============================================================
# ANOMALY CHANGE CHART
# ============================================================

st.subheader("📈 Anomaly Change Percentage")


if (
    not filtered_alerts.empty
    and "change_percent" in filtered_alerts.columns
):

    chart_data = filtered_alerts.copy()


    chart_data["change_percent"] = pd.to_numeric(
        chart_data["change_percent"],
        errors="coerce"
    )


    chart_data = chart_data.dropna(
        subset=["change_percent"]
    )


    if not chart_data.empty:

        if "metric" in chart_data.columns:

            chart_grouped = (
                chart_data
                .groupby("metric")["change_percent"]
                .mean()
                .sort_values(
                    ascending=False
                )
            )

            st.bar_chart(
                chart_grouped
            )

        else:

            st.bar_chart(
                chart_data[
                    ["change_percent"]
                ]
            )

else:

    st.info(
        "No anomaly change data available."
    )


st.divider()


# ============================================================
# SALES AND PROFIT ANALYSIS
# ============================================================

st.subheader("💰 Sales & Profit Analysis")


sales_col1, sales_col2 = st.columns(2)


# ------------------------------------------------------------
# Sales by category
# ------------------------------------------------------------

with sales_col1:

    if (
        "category" in data.columns
        and "total_sales_inr" in data.columns
    ):

        category_sales = (
            data.groupby("category")[
                "total_sales_inr"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
        )


        st.markdown(
            "### 🛍️ Sales by Category"
        )


        st.bar_chart(
            category_sales
        )

    else:

        st.info(
            "Category sales data is not available."
        )


# ------------------------------------------------------------
# Profit by category
# ------------------------------------------------------------

with sales_col2:

    if (
        "category" in data.columns
        and "profit_inr" in data.columns
    ):

        category_profit = (
            data.groupby("category")[
                "profit_inr"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
        )


        st.markdown(
            "### 💵 Profit by Category"
        )


        st.bar_chart(
            category_profit
        )

    else:

        st.info(
            "Category profit data is not available."
        )


st.divider()


# ============================================================
# MONTHLY SALES
# ============================================================

st.subheader("📅 Monthly Sales Trend")


if (
    "order_date" in data.columns
    and "total_sales_inr" in data.columns
):

    monthly_data = data.copy()


    monthly_data = monthly_data.dropna(
        subset=["order_date"]
    )


    monthly_data["year_month"] = (
        monthly_data["order_date"]
        .dt.to_period("M")
        .astype(str)
    )


    monthly_sales = (
        monthly_data
        .groupby("year_month")[
            "total_sales_inr"
        ]
        .sum()
    )


    st.line_chart(
        monthly_sales
    )

else:

    st.info(
        "Monthly sales data is not available."
    )


st.divider()


# ============================================================
# ML ANOMALY MONITORING
# ============================================================

st.subheader("🤖 Machine Learning Anomaly Detection")


if not ml_alerts.empty:

    ml_col1, ml_col2, ml_col3 = st.columns(3)


    # --------------------------------------------------------
    # Total ML anomalies
    # --------------------------------------------------------

    with ml_col1:

        ml_count = len(ml_alerts)

        st.metric(
            "ML Anomalies",
            format_number(ml_count)
        )


    # --------------------------------------------------------
    # ML anomaly rate
    # --------------------------------------------------------

    with ml_col2:

        if len(data) > 0:

            ml_rate = (
                len(ml_alerts)
                / len(data)
                * 100
            )

        else:

            ml_rate = 0


        st.metric(
            "ML Anomaly Rate",
            f"{ml_rate:.1f}%"
        )


    # --------------------------------------------------------
    # ML report columns
    # --------------------------------------------------------

    with ml_col3:

        st.metric(
            "Detection Method",
            "Isolation Forest"
        )


    st.markdown(
        "### ML Anomaly Records"
    )


    ml_display_columns = [
        "date",
        "order_id",
        "product",
        "category",
        "region",
        "ml_anomaly",
        "ml_anomaly_score"
    ]


    ml_available_columns = [
        column
        for column in ml_display_columns
        if column in ml_alerts.columns
    ]


    if ml_available_columns:

        st.dataframe(
            ml_alerts[
                ml_available_columns
            ],
            width="stretch",
            hide_index=True
        )

else:

    st.info(
        "ML anomaly report is not available yet."
    )


st.divider()


# ============================================================
# ALERT HISTORY
# ============================================================

st.subheader("🕒 Alert History")


if not history.empty:

    history_display = history.copy()


    history_columns = [
        "monitoring_time",
        "date",
        "order_id",
        "metric",
        "value",
        "change_percent",
        "severity"
    ]


    available_history_columns = [
        column
        for column in history_columns
        if column in history_display.columns
    ]


    if available_history_columns:

        st.dataframe(
            history_display[
                available_history_columns
            ],
            width="stretch",
            hide_index=True
        )

    else:

        st.dataframe(
            history_display,
            width="stretch",
            hide_index=True
        )

else:

    st.info(
        "No alert history is available yet."
    )


st.divider()


# ============================================================
# DATA PREVIEW
# ============================================================

with st.expander("📄 View Business Dataset"):

    st.dataframe(
        data,
        width="stretch",
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    "---"
)

st.caption(
    "AI Anomaly Watcher • Flipkart Business Data Monitoring • "
    "Statistical Z-Score + Machine Learning"
)

st.caption(
    "Developed by Shreya Singh | Data Analyst Aspirant"
)
