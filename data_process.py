
# app/data_processing.py

import pandas as pd
import os

# Build absolute path (works no matter where you run from)
base_dir = os.path.dirname(os.path.dirname(__file__))  # one level up from 'app'
file_path = os.path.join(base_dir, "data", "traffic_stops.csv")

print("Looking for file at:", file_path)

# Step 2: read the csv file
print("Reading dataset...")
data = pd.read_csv(file_path)
print("Dataset loaded successfully.")
print()

# Step 3: check basic info
print("---- Basic Info ----")
print(data.info())
print()

# Step 4: check missing values
print("---- Missing Values Before Cleaning ----")
print(data.isnull().sum())
print()

# Step 5: remove columns which are fully empty
data = data.dropna(axis=1, how='all')

# Step 6: handle missing values
# fill missing ages with median value
if 'driver_age' in data.columns:
    data['driver_age'] = data['driver_age'].fillna(data['driver_age'].median())

# fill other missing values with 'Unknown'
data = data.fillna('Unknown')

# Step 7: check again
print("---- Missing Values After Cleaning ----")
print(data.isnull().sum())
print()

# Step 8: save cleaned data
output_folder = os.path.join(base_dir, "data")
os.makedirs(output_folder, exist_ok=True)  # ensures folder exists
output_file = os.path.join(output_folder, "cleaned_stops.csv")

data.to_csv(output_file, index=False)
print("Cleaned data saved as:", output_file)
data.to_csv(output_file, index=False)
print("Cleaned data saved as:", output_file)

# Step 9: show few records
print("---- Sample Records ----")
print(data.head())
