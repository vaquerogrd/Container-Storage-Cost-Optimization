import matplotlib.pyplot as plt
import pandas as pd

# Load the cleaned data
cleaned_file_path = '1_data/cleaned_container_data.csv'
data = pd.read_csv(cleaned_file_path)
print(data.head())

# Create boxplots for numerical columns
plt.figure(figsize=(12, 6))

# Storage duration
plt.subplot(1, 3, 1)
plt.boxplot(data['storage_duration'], vert=False)
plt.title('Storage Duration')
plt.xlabel('Days')

# Buying storage
plt.subplot(1, 3, 2)
plt.boxplot(data['buyingStorage'], vert=False)
plt.title('Buying Storage')
plt.xlabel('Cost (€)')

# Selling storage
plt.subplot(1, 3, 3)
plt.boxplot(data['sellingStorage'], vert=False)
plt.title('Selling Storage')
plt.xlabel('Cost (€)')

plt.tight_layout()
plt.show()
