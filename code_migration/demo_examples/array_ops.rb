# Example 3: Array operations with blocks
# Demonstrates: .each, .map-like patterns, unless

def process_numbers(numbers)
  results = Array.new

  unless numbers.empty?
    numbers.each do |num|
      if num % 2 == 0
        results.push(num * 2)
      else
        results.push(num * 3)
      end
    end
  end

  return results
end

test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
output = process_numbers(test_data)
puts "Input: #{test_data}"
puts "Output: #{output}"
