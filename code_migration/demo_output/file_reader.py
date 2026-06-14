# Example 2: File reader class
# Demonstrates: class conversion, initialize→__init__, each→for

class FileProcessor
  def initialize(filename):
    @filename = filename
    @lines = []
  end

  def read_file
    file = File.open(@filename, "r")
    file.each do |line|
      @lines.push(line.strip)
    end
    file.close
    return @lines.length
  end

  def get_lines
    return @lines
  end

processor = FileProcessor.new("data.txt")
count = processor.read_file
print "Read #{count} lines"
