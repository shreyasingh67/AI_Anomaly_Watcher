import os
import pandas as pd


# --------------------------------------------------
# Required business columns
# --------------------------------------------------

REQUIRED_COLUMNS = [
    "Date",
    "Revenue",
    "Orders",
    "Conversion_Rate",
    "Traffic",
    "Cost",
    "Refunds"
]


# --------------------------------------------------
# Load business data
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
# Clean business data
# --------------------------------------------------

def clean_data(data):

    # Validate columns first
    validate_required_columns(data)

    # Work on a copy
    data = data.copy()

    # Remove duplicate rows
    data = data.drop_duplicates()

    # Convert Date column
    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )

    # Check invalid dates
    invalid_dates = data["Date"].isnull().sum()

    if invalid_dates > 0:

        raise ValueError(
            f"Found {invalid_dates} invalid date value(s). "
            "Please check the Date column."
        )

    # Business metric columns
    numeric_columns = [
        "Revenue",
        "Orders",
        "Conversion_Rate",
        "Traffic",
        "Cost",
        "Refunds"
    ]

    # Convert numeric columns
    for column in numeric_columns:

        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    # Check invalid numeric values
    for column in numeric_columns:

        invalid_values = data[column].isnull().sum()

        if invalid_values > 0:

            raise ValueError(
                f"Found {invalid_values} invalid "
                f"value(s) in {column}."
            )

    # Fill missing numeric values
    for column in numeric_columns:

        if data[column].isnull().any():

            data[column] = data[column].fillna(
                data[column].mean()
            )

    # Check if dataset became empty
    if data.empty:

        raise ValueError(
            "No valid data remains after cleaning."
        )

    return data


# --------------------------------------------------
# Validate business data
# --------------------------------------------------

def validate_data(data):

    print("\n========== DATA VALIDATION ==========")

    # Required columns
    validate_required_columns(data)

    print("\nRequired Columns:")
    print("All required columns are present.")

    # Missing values
    print("\nMissing Values:")
    print(data.isnull().sum())

    # Duplicate rows
    print("\nDuplicate Rows:")
    print(data.duplicated().sum())

    # Data types
    print("\nData Types:")
    print(data.dtypes)

    # Dataset shape
    print("\nDataset Shape:")
    print(data.shape)


# --------------------------------------------------
# Test the module
# --------------------------------------------------

if __name__ == "__main__":

    try:

        # Load CSV data
        data = load_data(
            "data/business_data.csv"
        )

        print("\n========== ORIGINAL DATA ==========")
        print(data)

        # Clean data
        data = clean_data(
            data
        )

        print("\n========== CLEANED DATA ==========")
        print(data)

        # Validate cleaned data
        validate_data(
            data
        )

        print(
            "\nData cleaning and validation "
            "completed successfully."
        )

    except Exception as error:

        print(
            "\nERROR:",
            error
        )