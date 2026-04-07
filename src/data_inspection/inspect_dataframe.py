# inspect_dataframe.py

import pandas as pd

# --- Load dataset ---
# Use a small sample CSV (already in repo or create one in data/raw/)
file_path = "data/raw/sample_air_quality.csv"

df = pd.read_csv(file_path)

# --- 1. Preview Data ---
print("Preview of Data (head):")
print(df.head())

# --- 2. Inspect Structure ---
print("\nDataFrame Info:")
df.info()

# --- 3. Statistical Summary ---
print("\nStatistical Summary:")
print(df.describe())