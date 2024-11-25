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
non_numerical_columns = ['type','number','booking','contSuttleRef','terminal', 'provider', 'gate_in', 'gate_out', 'cost', 'stoComment', 'Created', 'container_category']
X_train = X_train.drop(columns=non_numerical_columns)
X_test = X_test.drop(columns=non_numerical_columns)

# Ensure all features are numerical
print(X_train.info())  # Verify numerical columns


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
