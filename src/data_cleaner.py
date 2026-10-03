import os
import pandas as pd


# --------------------------------------------------
# Required Flipkart dataset columns
# --------------------------------------------------

REQUIRED_COLUMNS = [
    "order_id",
    "product_name",
    "category",
    "price_inr",
    "quantity_sold",
    "total_sales_inr",
    "order_date",
    "payment_method",
    "customer_rating",
    "month",
    "year",
    "profit_inr",
    "discount_percent",
    "customer_segment",
    "region"
]


# --------------------------------------------------
# Load Flipkart data
# Supports CSV and Excel files
# --------------------------------------------------

def load_data(file_path):

    # Check whether file exists
    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    # Check file format
    if file_path.lower().endswith(".csv"):

        data = pd.read_csv(
            file_path
        )

    elif file_path.lower().endswith(".xlsx"):

        data = pd.read_excel(
            file_path
        )

    else:

        raise ValueError(
            "Unsupported file format. "
            "Please use CSV or Excel (.xlsx) file."
        )

    # Check empty dataset
    if data.empty:

        raise ValueError(
            "The input file is empty."
        )

    return data


# --------------------------------------------------
# Validate required columns
# --------------------------------------------------

def validate_required_columns(data):

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )


# --------------------------------------------------
# Clean Flipkart data
# --------------------------------------------------

def clean_data(data):

    # Validate columns first
    validate_required_columns(data)

    # Work on a copy
    data = data.copy()

    # Remove duplicate rows
    data = data.drop_duplicates()

    # --------------------------------------------------
    # Convert order date
    # Dataset uses DD-MM-YYYY format
    # --------------------------------------------------

    data["order_date"] = pd.to_datetime(
        data["order_date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    # Check invalid dates
    invalid_dates = data["order_date"].isnull().sum()

    if invalid_dates > 0:

        raise ValueError(
            f"Found {invalid_dates} invalid date value(s) "
            "in order_date."
        )

    # --------------------------------------------------
    # Flipkart numeric columns
    # --------------------------------------------------

    numeric_columns = [
        "price_inr",
        "quantity_sold",
        "total_sales_inr",
        "customer_rating",
        "year",
        "profit_inr",
        "discount_percent"
    ]

    # Convert numeric columns
    for column in numeric_columns:

        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    # --------------------------------------------------
    # Check invalid numeric values
    # --------------------------------------------------

    for column in numeric_columns:

        invalid_values = data[column].isnull().sum()

        if invalid_values > 0:

            raise ValueError(
                f"Found {invalid_values} invalid "
                f"value(s) in {column}."
            )

    # --------------------------------------------------
    # Fill missing numeric values
    # --------------------------------------------------

    for column in numeric_columns:

        if data[column].isnull().any():

            data[column] = data[column].fillna(
                data[column].mean()
            )

    # --------------------------------------------------
    # Check if dataset became empty
    # --------------------------------------------------

    if data.empty:

        raise ValueError(
            "No valid data remains after cleaning."
        )

    return data


# --------------------------------------------------
# Validate Flipkart data
# --------------------------------------------------

def validate_data(data):

    print(
        "\n========== DATA VALIDATION =========="
    )

    # Required columns
    validate_required_columns(data)

    print(
        "\nRequired Columns:"
    )

    print(
        "All required Flipkart columns are present."
    )

    # Missing values
    print(
        "\nMissing Values:"
    )

    print(
        data.isnull().sum()
    )

    # Duplicate rows
    print(
        "\nDuplicate Rows:"
    )

    print(
        data.duplicated().sum()
    )

    # Data types
    print(
        "\nData Types:"
    )

    print(
        data.dtypes
    )

    # Dataset shape
    print(
        "\nDataset Shape:"
    )

    print(
        data.shape
    )


# --------------------------------------------------
# Test the module
# --------------------------------------------------

if __name__ == "__main__":

    try:

        # Load CSV data
        data = load_data(
            "data/business_data.csv"
        )

        print(
            "\n========== ORIGINAL DATA =========="
        )

        print(
            data.head()
        )

        # Clean data
        data = clean_data(
            data
        )

        print(
            "\n========== CLEANED DATA =========="
        )

        print(
            data.head()
        )

        # Validate cleaned data
        validate_data(
            data
        )

        print(
            "\nFlipkart data cleaning and validation "
            "completed successfully."
        )

    except Exception as error:

        print(
            "\nERROR:",
            error
        )