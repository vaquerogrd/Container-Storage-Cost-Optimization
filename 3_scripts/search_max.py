import pandas as pd
from datetime import datetime

# Load the data
file_path = '1_data/container_data_2024.xlsx'
data = pd.read_excel(file_path)

# Columns to drop
columns_to_drop = ['emptyRelease', 'datePOL', 'deliveryRef', 'confirmedAPP',
                   'appConfirmation', 'Created By', 'Modified', 'Modified By',
                   'contAviso', 'Item Type']
data = data.drop(columns=columns_to_drop, errors='ignore')

# Filter rows where essential fields are not empty
data = data[data['storageID'].notna() & data['dateTerminal'].notna() & data['dateDeparture'].notna()]

# Format date columns
data['dateTerminal'] = pd.to_datetime(data['dateTerminal'], format='%d.%m.%Y', errors='coerce')
data['dateDeparture'] = pd.to_datetime(data['dateDeparture'], format='%d.%m.%Y', errors='coerce')
data['Created'] = pd.to_datetime(data['Created'], errors='coerce')

# Add column with number of days between dateTerminal and dateDeparture
data['days_diff'] = (data['dateTerminal'] - data['dateDeparture']).dt.days.abs()

# Filter rows where days_diff > 1000
filtered_data = data[data['days_diff'] > 300]

# Print the results
if not filtered_data.empty:
    print("Rows where days_diff > 1000:")
    print(filtered_data[['ID', 'days_diff']])
else:
    print("No rows found where days_diff > 1000.")



