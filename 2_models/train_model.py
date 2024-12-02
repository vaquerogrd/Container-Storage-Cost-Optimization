import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Load the training and testing data
X_train = pd.read_csv('1_data/X_train.csv')
X_test = pd.read_csv('1_data/X_test.csv')
y_train = pd.read_csv('1_data/y_train.csv')
y_test = pd.read_csv('1_data/y_test.csv')

# Drop non-numerical columns and irrelevant features
non_numerical_columns = ['type', 'number', 'booking', 'contSuttleRef', 'terminal', 
                         'provider', 'gate_in', 'gate_out', 'cost', 'stoComment', 
                         'Created', 'container_category']
X_train = X_train.drop(columns=non_numerical_columns, errors='ignore')
X_test = X_test.drop(columns=non_numerical_columns, errors='ignore')

# Ensure all features are numerical and handle missing values
X_train = X_train.select_dtypes(include=[np.number]).replace([np.inf, -np.inf], np.nan).dropna()
X_test = X_test.select_dtypes(include=[np.number]).replace([np.inf, -np.inf], np.nan).dropna()

# Align y_train with X_train by index
y_train = y_train.loc[X_train.index]
y_test = y_test.loc[X_test.index]

# Ensure y_train and y_test are clean
y_train = y_train.replace([np.inf, -np.inf], np.nan).dropna()
y_test = y_test.replace([np.inf, -np.inf], np.nan).dropna()

# Check shapes of aligned data
print(f"Aligned X_train shape: {X_train.shape}")
print(f"Aligned y_train shape: {y_train.shape}")

# Initialize the Linear Regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# Print evaluation metrics
print("Model Evaluation:")
print(f"Mean Absolute Error (MAE): {mae}")
print(f"Root Mean Squared Error (RMSE): {rmse}")

# Save the model predictions
y_pred_df = pd.DataFrame(y_pred, columns=['predicted_buyingStorage', 'predicted_sellingStorage'])
y_pred_df.to_csv('1_data/y_pred.csv', index=False)
print("Predictions saved to 1_data/y_pred.csv")
