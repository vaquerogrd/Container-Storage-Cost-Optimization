import pandas as pd
from sklearn.model_selection import train_test_split

# Load the normalized data
normalized_file_path = '1_data/normalized_container_data.csv'
data = pd.read_csv(normalized_file_path)

# Define the target variable (y) and features (X)
X = data.drop(columns=['buyingStorage', 'sellingStorage'])  # Drop the target columns
y = data[['buyingStorage', 'sellingStorage']]  # Target variables

# Split the data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save the split datasets
X_train.to_csv('1_data/X_train.csv', index=False)
X_test.to_csv('1_data/X_test.csv', index=False)
y_train.to_csv('1_data/y_train.csv', index=False)
y_test.to_csv('1_data/y_test.csv', index=False)

# Print confirmation
print("Data split into training and testing sets:")
print(f"X_train: {X_train.shape}, X_test: {X_test.shape}")
print(f"y_train: {y_train.shape}, y_test: {y_test.shape}")
