import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the cleaned data
cleaned_file_path = '1_data/cleaned_container_data.csv'
data = pd.read_csv(cleaned_file_path)

# Select numerical columns for normalization
numerical_features = ['storage_duration', 'buyingStorage', 'sellingStorage', 
                      'buying_cost_per_day', 'selling_cost_per_day']

# Initialize the MinMaxScaler
scaler = MinMaxScaler()

# Apply the scaler to numerical features
data[numerical_features] = scaler.fit_transform(data[numerical_features])

# Save the normalized data
normalized_file_path = '1_data/normalized_container_data.csv'
data.to_csv(normalized_file_path, index=False)

# Display a preview of the normalized data
print(f"Normalized data saved to {normalized_file_path}")
print(data.head())
