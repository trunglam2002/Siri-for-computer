import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Provide the raw link to the CSV file
url = '''https://raw.githubusercontent.com/trunglam2002/datasets/main/classify%20duty.csv'''

# Read the CSV file from the URL
df = pd.read_csv(url)

# Specify the directory and filename to save the CSV file
save_path = './save_data/classify_duty.csv'

# Save the DataFrame to a CSV file
df.to_csv(save_path, index=False)

print(f"Data saved to {save_path}")
