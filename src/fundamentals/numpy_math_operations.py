import numpy as np

# Create arrays
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print("Array a:", a)
print("Array b:", b)

# Element-wise operations
print("\n--- Element-wise Operations ---")
print("Addition:", a + b)
print("Subtraction:", a - b)
print("Multiplication:", a * b)
print("Division:", a / b)

# Scalar operations
print("\n--- Scalar Operations ---")
print("Add 10:", a + 10)
print("Multiply by 2:", a * 2)

# Python list vs NumPy
print("\n--- List vs NumPy ---")
list1 = [1, 2, 3]
list2 = [4, 5, 6]
print("List addition:", list1 + list2)

# Shape checking
print("\n--- Shape Info ---")
print("Shape of a:", a.shape)
print("Shape of b:", b.shape)