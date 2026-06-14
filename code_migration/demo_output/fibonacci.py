# Example 1: Fibonacci sequence
# Demonstrates: def conversion, if/else, print→print, None→None

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
    end
    return b
  end

print "Fibonacci(10) = #{fibonacci(10)}"
print "Fibonacci(0) = #{fibonacci(0)}"
