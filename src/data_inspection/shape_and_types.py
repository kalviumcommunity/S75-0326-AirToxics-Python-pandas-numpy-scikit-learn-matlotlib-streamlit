# shape_and_types.py

import pandas as pd

# --- Load dataset ---
file_path = "data/raw/sample_air_quality.csv"
df = pd.read_csv(file_path)

# --- 1. Inspect Shape ---
print("DataFrame Shape:")
print(df.shape)

# Interpret shape
num_rows, num_columns = df.shape
print(f"\nNumber of rows (records): {num_rows}")
print(f"Number of columns (features): {num_columns}")

# --- 2. Inspect Column Data Types ---
print("\nColumn Data Types:")
print(df.dtypes)

# --- 3. Interpretation ---
print("\nInterpretation:")
print("Each row represents a city record.")
print("Each column represents a feature like AQI or PM2.5 levels.")

print("\nChecking for potential issues:")
for column, dtype in df.dtypes.items():
    print(f"{column} → {dtype}")