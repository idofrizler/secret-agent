# Test script to demonstrate code execution examples

print("=== Code Execution Test Examples ===\n")

# Example 1: Simple calculation
print("1. Simple Math:")
result = 2 + 2 * 3
print(f"2 + 2 * 3 = {result}")

# Example 2: String manipulation
print("\n2. String Operations:")
text = "Hello, World!"
print(f"Original: {text}")
print(f"Uppercase: {text.upper()}")
print(f"Length: {len(text)}")

# Example 3: List comprehension
print("\n3. List Comprehension:")
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(f"Numbers: {numbers}")
print(f"Squares: {squares}")

# Example 4: Simple function
print("\n4. Function Definition:")
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(f"Fibonacci sequence (first 8): {[fibonacci(i) for i in range(8)]}")

# Example 5: File operations (safe)
print("\n5. Working with data:")
import json
data = {"name": "Agent", "version": "1.0", "tools": ["hello", "weather", "search", "code"]}
json_str = json.dumps(data, indent=2)
print("JSON data:")
print(json_str)

print("\n=== All tests completed successfully! ===")
