# functions_demo.py

# --- Function Definition ---
def calculate_average(aqi_values):
    """Calculate average AQI from a list"""
    total = sum(aqi_values)
    count = len(aqi_values)
    return total / count


def classify_aqi(aqi):
    """Return AQI category based on value"""
    if aqi <= 100:
        return "Good"
    elif aqi <= 200:
        return "Moderate"
    else:
        return "Poor"


# --- Function Calls ---
aqi_list = [120, 200, 90]

avg = calculate_average(aqi_list)
print("Average AQI:", avg)

# Using function with arguments
for value in aqi_list:
    category = classify_aqi(value)
    print(f"AQI {value} is {category}")