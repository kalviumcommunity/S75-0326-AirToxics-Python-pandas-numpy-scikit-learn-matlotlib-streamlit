# readable_code_demo.py

# --- Poor Naming Example (Bad Practice) ---
x = [120, 200, 90]  # unclear what x represents
s = sum(x) / len(x)
print("Avg:", s)

# --- Improved Version (Good Practice) ---

# AQI values for selected cities
aqi_values = [120, 200, 90]

# Calculate average AQI to understand overall air quality
total_aqi = sum(aqi_values)
number_of_readings = len(aqi_values)
average_aqi = total_aqi / number_of_readings

print("\nImproved Readability:")
print("Average AQI:", average_aqi)


# --- Function with Clear Naming and Comments ---

def classify_aqi(aqi_value):
    """
    Determine AQI category based on standard thresholds.
    This helps interpret raw AQI numbers into meaningful labels.
    """
    if aqi_value <= 100:
        return "Good"
    elif aqi_value <= 200:
        return "Moderate"
    else:
        return "Poor"


# Apply classification to each AQI value
for aqi_value in aqi_values:
    category = classify_aqi(aqi_value)
    print(f"AQI {aqi_value} falls under '{category}' category")