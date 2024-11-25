import pandas as pd
import statsmodels.api as sm
import plotly.express as px

# Load the cleaned data
cleaned_file_path = '1_data/cleaned_container_data.csv'
data = pd.read_csv(cleaned_file_path)

# ________________________________________________________ 1. Correlation Analysis
print("Correlation Matrix:")
correlation_matrix = data[['storage_duration', 'buyingStorage', 'sellingStorage']].corr()
print(correlation_matrix)

# ________________________________________________________ 2. Summary Statistics
print("\nSummary Statistics:")
summary_stats = data[['storage_duration', 'buyingStorage', 'sellingStorage']].describe()
print(summary_stats)

# ________________________________________________________ 3. Regression Analysis
# Define dependent and independent variables
X = data['storage_duration']  # Independent variable
y = data['buyingStorage']     # Dependent variable

# Add constant to predictor
X = sm.add_constant(X)

# Perform regression
print("\nRegression Analysis: Storage Duration vs Buying Storage")
model = sm.OLS(y, X).fit()
print(model.summary())

# ________________________________________________________ 4. Visualizations
# Scatter plot: Storage Duration vs Buying Storage with Trendline
fig1 = px.scatter(data, x='storage_duration', y='buyingStorage',
                  title='Regression: Storage Duration vs Buying Storage',
                  labels={'storage_duration': 'Storage Duration (Days)', 'buyingStorage': 'Buying Storage (€)'},
                  trendline='ols')  # Adds a trendline
fig1.show()

# Scatter plot: Storage Duration vs Selling Storage with Trendline
fig2 = px.scatter(data, x='storage_duration', y='sellingStorage',
                  title='Regression: Storage Duration vs Selling Storage',
                  labels={'storage_duration': 'Storage Duration (Days)', 'sellingStorage': 'Selling Storage (€)'},
                  trendline='ols')  # Adds a trendline
fig2.show()

