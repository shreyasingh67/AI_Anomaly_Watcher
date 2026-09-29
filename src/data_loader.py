import pandas as pd

# Load business data
data = pd.read_csv(
    "data/business_data.csv",
    parse_dates=["Date"]
)

# Display the data
print(data)

# Check data information
print(data.info())

# Check for missing values
print(data.isnull().sum())