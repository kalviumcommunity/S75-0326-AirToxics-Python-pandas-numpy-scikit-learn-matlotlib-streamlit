# functions_data_flow.py

# --- Function 1: Calculate AQI Category ---
def get_aqi_category(aqi):
    if aqi <= 100:
        return "Good"
    elif aqi <= 200:
        return "Moderate"
    else:
        return "Poor"


# --- Function 2: Calculate Average AQI ---
def calculate_average(aqi_list):
    total = sum(aqi_list)
    return total / len(aqi_list)


# --- Function 3: Combine Results ---
def generate_report(city, aqi):
    category = get_aqi_category(aqi)  # using another function
    return f"{city} has AQI {aqi} ({category})"


# --- Main Execution ---
aqi_values = [120, 200, 90]
cities = ["Chennai", "Delhi", "Mumbai"]

# Use returned values
average = calculate_average(aqi_values)
print("Average AQI:", average)

print("\nCity Reports:")
for city, aqi in zip(cities, aqi_values):
    report = generate_report(city, aqi)  # capturing return
    print(report)