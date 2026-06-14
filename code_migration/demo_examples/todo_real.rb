require 'json'
require 'fileutils'
require 'pathname'
require 'optparse'

def get_data_file
  script_path = Pathname.new(__FILE__).realpath
  script_dir = script_path.dirname
  script_dir.join('todo_list.json').to_s
end

def load_tasks
  data_file = get_data_file
  begin
    JSON.parse(File.read(data_file))
  rescue Errno::ENOENT, JSON::ParserError
    []
  end
end

def save_tasks(tasks)
  data_file = get_data_file
  FileUtils.mkdir_p(File.dirname(data_file))
  File.write(data_file, JSON.pretty_generate(tasks))
end

def add_task(description)
  tasks = load_tasks
  tasks << { 'description' => description, 'completed' => false }
  save_tasks(tasks)
  puts "Task added: #{description}"
end

def list_tasks
  tasks = load_tasks
  if tasks.empty?
    puts 'No tasks found.'
    return
  end

  tasks.each_with_index do |task, index|
    status = task['completed'] ? '[x]' : '[ ]'
    puts "#{index + 1}. #{status} #{task['description']}"
  end
end

def complete_task(task_number)
  tasks = load_tasks
  if task_number.between?(1, tasks.length)
    tasks[task_number - 1]['completed'] = true
    save_tasks(tasks)
    puts "Task #{task_number} completed."
  else
    puts 'Invalid task number.'
  end
end

def delete_task(task_number)
  tasks = load_tasks
  if task_number.between?(1, tasks.length)
    deleted_task = tasks.delete_at(task_number - 1)
    save_tasks(tasks)
    puts "Task '#{deleted_task['description']}' deleted."
  else
    puts 'Invalid task number.'
  end
end

def clear_tasks
  save_tasks([])
  puts "All tasks cleared."
end

def main
  options = {}
  OptionParser.new do |opts|
    opts.banner = 'Usage: todo.rb [options]'
    opts.on('-a', '--add DESCRIPTION', 'Add a new task') { |description| options[:add] = description }
    opts.on('-l', '--list', 'List all tasks') { options[:list] = true }
    opts.on('-c', '--complete TASK_NUMBER', Integer, 'Mark a task as complete') { |task_number| options[:complete] = task_number }
    opts.on('-d', '--delete TASK_NUMBER', Integer, 'Delete a task') { |task_number| options[:delete] = task_number }
    opts.on('--clear', 'Clear all tasks') { options[:clear] = true }
    opts.on_tail('-h', '--help', 'Show this help message') { puts opts; exit }
  end.parse!

  case
  when options[:add] then add_task(options[:add])
  when options[:list] then list_tasks
  when options[:complete] then complete_task(options[:complete])
  when options[:delete] then delete_task(options[:delete])
  when options[:clear] then clear_tasks
  else puts 'Please provide a command. Use -h for help.'
  end
end

main if __FILE__ == $PROGRAM_NAME
