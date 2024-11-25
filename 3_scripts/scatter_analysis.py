import pandas as pd
import plotly.express as px

# Load the cleaned data
cleaned_file_path = '1_data/cleaned_container_data.csv'
data = pd.read_csv(cleaned_file_path)

# Scatter plot: Storage Duration vs Buying Storage
fig1 = px.scatter(data, x='storage_duration', y='buyingStorage', 
                  title='Storage Duration vs Buying Storage', 
                  labels={'storage_duration': 'Storage Duration (Days)', 'buyingStorage': 'Buying Storage (€)'},
                  trendline='ols')  # Adds a trendline
fig1.show()

# Scatter plot: Storage Duration vs Selling Storage
fig2 = px.scatter(data, x='storage_duration', y='sellingStorage', 
                  title='Storage Duration vs Selling Storage', 
                  labels={'storage_duration': 'Storage Duration (Days)', 'sellingStorage': 'Selling Storage (€)'},
                  trendline='ols')  # Adds a trendline
fig2.show()
