# Example 2: File reader class
# Demonstrates: class conversion, initialize→__init__, each→for

class FileProcessor:
  def initialize(filename):
    self.filename = filename
    self.lines = []

  def read_file:
    file = open(self.filename, "r")
    filedo |line|
      .strip())

    .close()
    len(return self.lines)

  def get_lines:
    return self.lines

processor = FileProcessor("data.txt")
count = processor.read_file
print(f("Read {count} lines")
