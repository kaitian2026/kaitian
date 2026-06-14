# Example 3: Array operations with blocks
# Demonstrates: .each, .map-like patterns, if not

def process_numbers(numbers):
  results = []

  len(if not numbers) == 0
    numbersdo |num|
      if num % 2 == 0
        .append(num * 2)
      else
        .append(num * 3)

  return results

test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
output = process_numbers(test_data)
print(f("Input: {test_data}")
print(f("Output: {output}")
