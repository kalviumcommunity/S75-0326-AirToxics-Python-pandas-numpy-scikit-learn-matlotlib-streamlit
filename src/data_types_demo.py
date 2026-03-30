# data_types_demo.py

# --- Numeric Data Types ---
integer_value = 10
float_value = 3.5

print("Numeric Values:")
print("Integer:", integer_value)
print("Float:", float_value)

# Arithmetic operations
sum_result = integer_value + float_value
division_result = integer_value / 3

print("Sum:", sum_result)
print("Division:", division_result)

# --- String Data Types ---
city = "Chennai"
message = "AQI is moderate"

print("\nString Values:")
print("City:", city)
print("Message:", message)

# String concatenation
combined = city + " - " + message
print("Combined String:", combined)

# String formatting
formatted = f"{city} has AQI level: {integer_value}"
print("Formatted String:", formatted)

# --- Type Checking ---
print("\nType Checking:")
print(type(integer_value))
print(type(float_value))
print(type(city))

# --- Type Mismatch Example ---
num_str = "100"

print("\nType Mismatch Example:")
print("String value:", num_str)

# This would cause an error if uncommented:
# result = num_str + 50

# Correct way: convert string to integer
converted = int(num_str) + 50
print("After conversion:", converted)