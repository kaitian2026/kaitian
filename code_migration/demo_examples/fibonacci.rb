# Example 1: Fibonacci sequence
# Demonstrates: def conversion, if/else, puts→print, nil→None

def fibonacci(n)
  if n <= 0
    return nil
  elsif n == 1
    return 0
  elsif n == 2
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
end

puts "Fibonacci(10) = #{fibonacci(10)}"
puts "Fibonacci(0) = #{fibonacci(0)}"
