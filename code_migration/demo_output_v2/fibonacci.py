# Example 1: Fibonacci sequence
# Demonstrates: def conversion, if/else, puts→print, None→None

def fibonacci(n):
  if n <= 0
    return None
  elif n == 1
    return 0
  elif n == 2
    return 1
  else
    a = 0
    b = 1
    (n - 2).times do
      c = a + b
      a = b
      b = c

    return b

print(f("Fibonacci(10) = {fibonacci(10)}")
print(f("Fibonacci(0) = {fibonacci(0)}")
