import pandas as pd

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


# Set a custom threshold (e.g., 0 to 365 days)
filtered_data = data[(data['storage_duration'] >= 0) & (data['storage_duration'] <= 100)]

print(f"Original data size: {len(data)}")
print(f"Filtered data size: {len(filtered_data)}")

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
relevant_data.to_csv(cleaned_file_path, index=False)
print(f"Cleaned data saved to {cleaned_file_path}")




