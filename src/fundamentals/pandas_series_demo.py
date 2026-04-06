# pandas_series_demo.py

import pandas as pd
import numpy as np

# --- 1. Create Series from Python List ---
aqi_list = [120, 200, 90]

series_from_list = pd.Series(aqi_list)

print("Series from Python List:")
print(series_from_list)

# --- Inspect index and values ---
print("\nIndex:", series_from_list.index)
print("Values:", series_from_list.values)


# --- 2. Create Series from NumPy Array ---
aqi_array = np.array([80, 150, 220])

series_from_array = pd.Series(aqi_array)

print("\nSeries from NumPy Array:")
print(series_from_array)

# --- Inspect index and values ---
print("\nIndex:", series_from_array.index)
print("Values:", series_from_array.values)


# --- 3. Custom Index (to show labels matter) ---
cities = ["Chennai", "Delhi", "Mumbai"]

series_with_labels = pd.Series(aqi_list, index=cities)

print("\nSeries with Custom Labels:")
print(series_with_labels)

# Access using label
print("\nAQI of Chennai:", series_with_labels["Chennai"])