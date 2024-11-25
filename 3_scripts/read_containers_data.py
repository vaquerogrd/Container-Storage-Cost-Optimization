import pandas as pd
from datetime import datetime

# Load the data
file_path = '1_data/container_data_2024.xlsx'
data = pd.read_excel(file_path)
data = data.drop(columns=['emptyRelease','datePOL','deliveryRef',
                          'confirmedAPP','appConfirmation','Created By','Modified',
                          'Modified By','contAviso','Item Type','Path'])


# ________________________________________________________FILTER ROWS WHERE storageID IS NOT EMPTY
data = data[data['storageID'].notna() & data['booking'].notna() & data['number'].notna()
          & data['dateTerminal'].notna() & data['dateDeparture'].notna()]


# ________________________________________________________FORTMAT COLUMNS
data['dateTerminal'] = pd.to_datetime(data['dateTerminal'], format='%d.%m.%Y', errors='coerce')
data['dateDeparture'] = pd.to_datetime(data['dateDeparture'], format='%d.%m.%Y', errors='coerce')
data['Created'] = pd.to_datetime(data['Created'], errors='coerce')

# Ensure numerical and text formats
data['size'] = data['size'].fillna(0).astype(int)
data['buyingStorage'] = data['buyingStorage'].fillna(0.0).astype(float)
data['sellingStorage'] = data['sellingStorage'].fillna(0.0).astype(float)
data['booking'] = data['booking'].fillna('Unknown').astype(str)
data['type'] = data['type'].fillna('Unknown').astype(str)
data['number'] = data['number'].fillna('Unknown').astype(str)
data['terminal'] = data['terminal'].fillna('Unknown').astype(str)
data['provider'] = data['provider'].fillna('Unknown').astype(str)

# ________________________________________________________FILL MISSING VALUES
data['buyingStorage'] = data['buyingStorage'].fillna(0)  # Numerical
data['sellingStorage'] = data['sellingStorage'].fillna(0)
data['terminal'] = data['terminal'].fillna('Unknown')  # Categorical
# Replace negative values with 0 in buyingStorage and sellingStorage
data.loc[data['buyingStorage'] < 0, 'buyingStorage'] = 0
data.loc[data['sellingStorage'] < 0, 'sellingStorage'] = 0

# ________________________________________________________RENAME COLUMNS
data.rename(columns={'dateTerminal': 'gate_in', 'dateDeparture': 'gate_out'}, inplace=True)

# ________________________________________________________FILTER OUT INCONSISTENT DATES
# Remove rows where gate_in (dateTerminal) is later than gate_out (dateDeparture)
data = data[data['gate_in'] <= data['gate_out']]

# ________________________________________________________ADD COLUMNS
data['storage_duration'] = (data['gate_out'] - data['gate_in']).dt.days
#__________________________________________________________
# Set a custom threshold (e.g., 0 to 365 days)
filtered_data = data[(data['storage_duration'] >= 0) & (data['storage_duration'] <= 100)]

print(f"Original data size: {len(data)}")
print(f"Filtered data size: {len(filtered_data)}")

#__________________________________________________________FEATURED ENGINEERING
# Define peak months (adjust according to your data context)
peak_months = [6, 7, 8, 12]  # Example: June, July, August, December

# Add a feature to indicate whether the storage falls within peak months
data['is_peak_period'] = data['gate_in'].dt.month.isin(peak_months).astype(int)

# Inspect the new feature
print(data[['gate_in', 'is_peak_period']].head())

#__________________________________________________________
# Categorize container types based on size and type
def categorize_container(row):
    if row['size'] == 20 and row['type'] == 'DV':
        return 'Small Dry'
    elif row['size'] == 40 and row['type'] == 'DV':
        return 'Large Dry'
    elif row['size'] == 40 and row['type'] == 'HC':
        return 'High Cube'
    elif row['size'] == 20 and row['type'] == 'RF':
        return 'Small Reefer'
    elif row['size'] == 40 and row['type'] == 'RF':
        return 'Large Reefer'
    else:
        return 'Other'

# Apply the categorization function to create a new column
data['container_category'] = data.apply(categorize_container, axis=1)

# Display the first few rows to verify
print(data[['size', 'type', 'container_category']].head())

#__________________________________________________________
# Calculate Storage Cost Per Day
# Replace storage_duration = 0 with NaN
data['storage_duration'] = data['storage_duration'].replace({0: pd.NA})

# Calculate cost per day for buying and selling
data['buying_cost_per_day'] = data['buyingStorage'] / data['storage_duration']
data['selling_cost_per_day'] = data['sellingStorage'] / data['storage_duration']

# Fill NaN values and infer object types
data['buying_cost_per_day'] = data['buying_cost_per_day'].fillna(0)
data['selling_cost_per_day'] = data['selling_cost_per_day'].fillna(0)

# Infer objects to ensure proper data types
data['buying_cost_per_day'] = data['buying_cost_per_day'].infer_objects().astype(float)
data['selling_cost_per_day'] = data['selling_cost_per_day'].infer_objects().astype(float)

# Display the first few rows to verify
print(data[['buyingStorage', 'sellingStorage', 'storage_duration', 'buying_cost_per_day', 'selling_cost_per_day']].head())

# List of public holidays in Austria for 2024
public_holidays = [
    '2024-01-01', '2024-01-06', '2024-04-01', '2024-05-01', '2024-05-09',
    '2024-05-20', '2024-05-30', '2024-08-15', '2024-10-26', '2024-11-01',
    '2024-12-08', '2024-12-25', '2024-12-26'
]
public_holidays = pd.to_datetime(public_holidays)

#__________________________________________________________
# Function to check if a date is a weekend or public holiday
def is_weekend_or_holiday(date):
    if pd.isna(date):
        return False  # Handle missing dates
    return date.weekday() >= 5 or date in public_holidays

# Add weekend/holiday indicator columns for gate_in and gate_out
data['gate_in_weekend_or_holiday'] = data['gate_in'].apply(is_weekend_or_holiday)
data['gate_out_weekend_or_holiday'] = data['gate_out'].apply(is_weekend_or_holiday)

# Verify the new columns
print(data[['gate_in', 'gate_in_weekend_or_holiday', 'gate_out', 'gate_out_weekend_or_holiday']].head())

#_________________________________________________________FILTER RELEVANT COLUMNS
relevant_data = filtered_data[['number', 'size', 'type', 
                      'gate_in', 'gate_out', 'storage_duration',
                      'buyingStorage','sellingStorage']]

# Inspect the first few rows
#print(f"Filtered dataset shape: {data.shape}")
print(relevant_data.head())
print("_____________________________________________________")
# Display column names and types
print(relevant_data.info())
#print(relevant_data.describe())
print("_____________________________________________________")
print(relevant_data[['buyingStorage', 'sellingStorage']].describe())

# Save the cleaned and filtered data
cleaned_file_path = '1_data/cleaned_container_data.csv'
data.to_csv(cleaned_file_path, index=False)
print(f"Cleaned data saved to {cleaned_file_path}")




