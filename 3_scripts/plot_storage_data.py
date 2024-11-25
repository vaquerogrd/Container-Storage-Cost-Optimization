import pandas as pd
import plotly.express as px

# Load the cleaned data
cleaned_file_path = '1_data/cleaned_container_data.csv'
data = pd.read_csv(cleaned_file_path)

# Create box plots
fig = px.box(data, y='storage_duration', title='Storage Duration')
fig.show()

