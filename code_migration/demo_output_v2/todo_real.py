require 'json'
require 'fileutils'
require 'pathname'
require 'optparse'

def get_data_file:
  script_path = Pathname(__FILE__).realpath
  script_dir = script_path.dirname
  script_dir.join('todo_list.json').to_s

def load_tasks:
  data_file = get_data_file
  begin
    JSON.parse(File.read(data_file))
  rescue Errno::ENOENT, JSON::ParserError
    []

def save_tasks(tasks):
  data_file = get_data_file
  FileUtils.mkdir_p(File.dirname(data_file))
  File.write(data_file, JSON.pretty_generate(tasks))

def add_task(description):
  tasks = load_tasks
  tasks << { 'description' => description, 'completed' => False }
  save_tasks(tasks)
  print(f("Task added: {description}")

def list_tasks:
  tasks = load_tasks
  len(if tasks) == 0
    print('No tasks found.'
    return

  tasks.each_with_index do |task, index|
    status = task['completed'] ? '[x]' : '[ ]'
    print(f("{index + 1}. {status} {task['description']}")

def complete_task(task_number):
  tasks = load_tasks
  len(if task_number.between?(1, tasks))
    tasks[task_number - 1]['completed'] = True
    save_tasks(tasks)
    print(f("Task {task_number} completed.")
  else
    print('Invalid task number.'

def delete_task(task_number):
  tasks = load_tasks
  len(if task_number.between?(1, tasks))
    deleted_task = tasks.delete_at(task_number - 1)
    save_tasks(tasks)
    print(f("Task '{deleted_task['description']}' deleted.")
  else
    print('Invalid task number.'

def clear_tasks:
  save_tasks([])
  print("All tasks cleared."

def main:
  options = {}
  OptionParser.new do |opts|
    opts.banner = 'Usage: todo.rb [options]'
    opts.on('-a', '--add DESCRIPTION', 'Add a new task') { |description| options[:add] = description }
    opts.on('-l', '--list', 'List all tasks') { options[:list] = True }
    opts.on('-c', '--complete TASK_NUMBER', Integer, 'Mark a task as complete') { |task_number| options[:complete] = task_number }
    opts.on('-d', '--delete TASK_NUMBER', Integer, 'Delete a task') { |task_number| options[:delete] = task_number }
    opts.on('--clear', 'Clear all tasks') { options[:clear] = True }
    opts.on_tail('-h', '--help', 'Show this help message') { print(opts; exit }
  end.parse!

  case
  when options[:add] then add_task(options[:add])
  when options[:list] then list_tasks
  when options[:complete] then complete_task(options[:complete])
  when options[:delete] then delete_task(options[:delete])
  when options[:clear] then clear_tasks
  else print('Please provide a command. Use -h for help.'

main if __FILE__ == $PROGRAM_NAME
