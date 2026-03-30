# basic_analysis.py

# Sample AQI data
cities = ["Chennai", "Delhi", "Mumbai"]
aqi_values = [120, 200, 90]

# Calculate average AQI
average_aqi = sum(aqi_values) / len(aqi_values)

# Print results
print("Air Quality Analysis")
print("---------------------")

for city, aqi in zip(cities, aqi_values):
    print(f"{city}: AQI = {aqi}")

print("---------------------")
print(f"Average AQI: {average_aqi}")

# Simple classification
for city, aqi in zip(cities, aqi_values):
    if aqi <= 100:
        category = "Good"
    elif aqi <= 200:
        category = "Moderate"
    else:
        category = "Poor"

    print(f"{city} is in {category} category")