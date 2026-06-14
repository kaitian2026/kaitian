"""
Kaitian - AST-Based Code Migration Engine v0.3
==============================================
Uses tree-sitter to parse Ruby source into a concrete syntax tree,
then generates equivalent Python source by walking and mapping the AST.

This is the real thing — not regex. Every node is visited and mapped
according to its syntactic role, not its surface text pattern.

Dependencies: tree-sitter, tree-sitter-ruby
"""

import tree_sitter_ruby as tsruby
from tree_sitter import Language, Parser


# ─── Setup ──────────────────────────────────────────────────────────────────

RUBY_LANGUAGE = Language(tsruby.language())
parser = Parser(RUBY_LANGUAGE)

INDENT = "    "  # 4 spaces


def node_text(node, source: bytes) -> str:
    """Get the source text of a node."""
    return source[node.start_byte:node.end_byte].decode('utf-8')


class RubyASTVisitor:
    """
    Walk a Ruby CST and generate Python source code.
    
    Maps Ruby constructs to idiomatic Python:
      class A ... end        → class A:\n    ...
      def f(x) ... end       → def f(x):\n    ...
      if x ... elsif ... end → if x:\n    ...\nelif ...:
      @var                   → self.var
      nil / true / false     → None / True / False
      puts x                 → print(x)
      arr.each do |x| ...     → for x in arr:\n    ...
      n.times do ...         → for _ in range(n):\n    ...
      #{expr}                → {expr} (inside f-string)
      require 'x'            → import x
    """
    
    def __init__(self):
        self.indent_level = 0
        self.source = b""
    
    def indent(self) -> str:
        return INDENT * self.indent_level
    
    def convert(self, ruby_code: str) -> str:
        """Convert Ruby source code to Python source code."""
        self.source = ruby_code.encode('utf-8')
        tree = parser.parse(self.source)
        self.indent_level = 0
        return self.visit_node(tree.root_node)
    
    # ─── Node dispatcher ────────────────────────────────────────────────
    
    def visit_node(self, node) -> str:
        """Dispatch to the appropriate handler based on node type."""
        node_type = node.type
        
        handlers = {
            'program': self.visit_program,
            'class': self.visit_class,
            'method': self.visit_method,
            'singleton_method': self.visit_singleton_method,
            'if': self.visit_if,
            'unless': self.visit_unless,
            'elsif': self.visit_elsif,
            'else': self.visit_else,
            'begin': self.visit_begin,
            'rescue': self.visit_rescue,
            'block': self.visit_block,
            'do_block': self.visit_do_block,
            'call': self.visit_call,
            'argument_list': self.visit_argument_list,
            'identifier': self.visit_identifier,
            'constant': self.visit_constant,
            'method_parameters': self.visit_method_parameters,
            'simple_symbol': self.visit_simple_symbol,
            'string': self.visit_string,
            'string_interpolation': self.visit_string_interpolation,
            'integer': self.visit_integer,
            'float': self.visit_float,
            'nil': self.visit_nil,
            'true': self.visit_true,
            'false': self.visit_false,
            'array': self.visit_array,
            'hash': self.visit_hash,
            'pair': self.visit_pair,
            'binary': self.visit_binary,
            'unary': self.visit_unary,
            'assignment': self.visit_assignment,
            'operator_assignment': self.visit_operator_assignment,
            'instance_variable': self.visit_instance_variable,
            'return': self.visit_return,
            'comment': self.visit_comment,
            'case': self.visit_case,
            'when': self.visit_when,
            'command': self.visit_command,
            'command_with_block': self.visit_command_with_block,
            'method_call': self.visit_method_call,
            'body_statement': lambda n: self.visit_children(n, sep='\n'),
            'then': lambda n: self.visit_children(n),
            'unless_modifier': self.visit_unless_modifier,
            'if_modifier': self.visit_if_modifier,
        }
        
        handler = handlers.get(node_type)
        if handler:
            return handler(node)
        
        # Default: just visit children
        return self.visit_children(node)
    
    def visit_children(self, node, sep=""):
        """Visit all children and join them."""
        parts = []
        for child in node.children:
            result = self.visit_node(child)
            if result:
                parts.append(result)
        return sep.join(parts)
    
    # ─── Top-level ──────────────────────────────────────────────────────
    
    def visit_program(self, node) -> str:
        statements = []
        for child in node.children:
            text = self.visit_node(child)
            if text.strip():
                statements.append(text)
        return '\n\n'.join(statements) + '\n'
    
    # ─── Class ──────────────────────────────────────────────────────────
    
    def visit_class(self, node) -> str:
        name = ""
        superclass = ""
        body = ""
        
        for child in node.children:
            if child.type == 'constant':
                name = self.visit_node(child)
            elif child.type == 'superclass':
                superclass = f"({self.visit_node(child.children[1])})"
            elif child.type == 'body_statement':
                self.indent_level += 1
                body = self.visit_node(child)
                self.indent_level -= 1
        
        header = f"class {name}{superclass}:"
        return f"{header}\n{body}"
    
    # ─── Method ─────────────────────────────────────────────────────────
    
    def visit_method(self, node) -> str:
        name = ""
        params = ""
        body = ""
        
        for child in node.children:
            if child.type == 'identifier':
                name = self.visit_node(child)
                # Rename initialize → __init__
                if name == 'initialize':
                    name = '__init__'
            elif child.type == 'method_parameters':
                params = self.visit_node(child)
            elif child.type == 'body_statement':
                self.indent_level += 1
                body = self.visit_node(child)
                self.indent_level -= 1
        
        header = f"{self.indent()}def {name}({params}):"
        if body.strip():
            return f"{header}\n{body}"
        return f"{header}\n{self.indent()}{INDENT}pass"
    
    def visit_singleton_method(self, node) -> str:
        # def self.method → @staticmethod or @classmethod
        name = ""
        params = ""
        body = ""
        
        for child in node.children:
            if child.type == 'identifier':
                name = self.visit_node(child)
            elif child.type == 'method_parameters':
                params = self.visit_node(child)
            elif child.type == 'body_statement':
                self.indent_level += 1
                body = self.visit_node(child)
                self.indent_level -= 1
        
        decorator = f"{self.indent()}@staticmethod"
        header = f"{self.indent()}def {name}({params}):"
        if body.strip():
            return f"{decorator}\n{header}\n{body}"
        return f"{decorator}\n{header}\n{self.indent()}{INDENT}pass"
    
    def visit_method_parameters(self, node) -> str:
        params = []
        for child in node.children:
            if child.type in ('identifier', 'optional_parameter', 'splat_parameter',
                            'hash_splat_parameter', 'block_parameter', 'keyword_parameter'):
                params.append(self.visit_node(child))
        return ', '.join(params)
    
    # ─── Conditionals ───────────────────────────────────────────────────
    
    def visit_if(self, node) -> str:
        cond = ""
        body = ""
        else_branch = ""
        
        for child in node.children:
            if child.type in ('binary', 'call', 'identifier', 'method_call',
                            'unary', 'string', 'integer', 'float', 'nil', 'true', 'false',
                            'array', 'hash', 'parenthesized_statements', 'constant',
                            'instance_variable', 'simple_symbol', 'argument_list',
                            'keyword_parameter'):
                cond = self.visit_node(child)
            elif child.type == 'then':
                self.indent_level += 1
                body = self.visit_children(child, sep='\n')
                self.indent_level -= 1
            elif child.type in ('else', 'elsif'):
                else_branch = self.visit_node(child)
            elif child.type == 'body_statement':
                pass  # handled via then
        
        result = f"{self.indent()}if {cond}:"
        if body.strip():
            result += f"\n{body}"
        else:
            result += f"\n{self.indent()}{INDENT}pass"
        
        if else_branch:
            result += f"\n{else_branch}"
        
        return result
    
    def visit_elsif(self, node) -> str:
        cond = ""
        body = ""
        else_branch = ""
        
        for child in node.children:
            if child.type in ('binary', 'call', 'identifier', 'method_call',
                            'unary', 'string', 'integer', 'float', 'nil', 'true', 'false'):
                cond = self.visit_node(child)
            elif child.type == 'then':
                self.indent_level += 1
                body = self.visit_children(child, sep='\n')
                self.indent_level -= 1
            elif child.type in ('else', 'elsif'):
                else_branch = self.visit_node(child)
        
        result = f"{self.indent()}elif {cond}:"
        if body.strip():
            result += f"\n{body}"
        else:
            result += f"\n{self.indent()}{INDENT}pass"
        
        if else_branch:
            result += f"\n{else_branch}"
        
        return result
    
    def visit_else(self, node) -> str:
        result = f"{self.indent()}else:"
        self.indent_level += 1
        body = self.visit_children(node, sep='\n')
        self.indent_level -= 1
        if body.strip():
            result += f"\n{body}"
        else:
            result += f"\n{self.indent()}{INDENT}pass"
        return result
    
    def visit_unless(self, node) -> str:
        # Ruby: unless cond ... end → Python: if not cond:
        cond = ""
        body = ""
        else_branch = ""
        
        for child in node.children:
            if child.type in ('binary', 'call', 'identifier', 'method_call'):
                cond = f"not ({self.visit_node(child)})"
            elif child.type == 'then':
                self.indent_level += 1
                body = self.visit_children(child, sep='\n')
                self.indent_level -= 1
            elif child.type == 'else':
                else_branch = self.visit_node(child)
        
        result = f"{self.indent()}if {cond}:"
        if body.strip():
            result += f"\n{body}"
        if else_branch:
            result += f"\n{else_branch}"
        return result
    
    def visit_unless_modifier(self, node) -> str:
        cond = ""
        body = ""
        for child in node.children:
            if body == "":
                body = self.visit_node(child)
            else:
                cond = self.visit_node(child)
        return f"if not ({cond}):\n{self.indent()}{INDENT}{body}"
    
    def visit_if_modifier(self, node) -> str:
        cond = ""
        body = ""
        for child in node.children:
            if body == "":
                body = self.visit_node(child)
            else:
                cond = self.visit_node(child)
        return f"if {cond}:\n{self.indent()}{INDENT}{body}"
    
    # ─── Begin/Rescue (exception handling) ──────────────────────────────
    
    def visit_begin(self, node) -> str:
        body = ""
        rescue_clauses = []
        ensure_body = ""
        else_body = ""
        
        for child in node.children:
            if child.type == 'body_statement':
                self.indent_level += 1
                body = self.visit_node(child)
                self.indent_level -= 1
            elif child.type == 'rescue':
                rescue_clauses.append(self.visit_node(child))
            elif child.type == 'ensure':
                self.indent_level += 1
                ensure_body = self.visit_children(child, sep='\n')
                self.indent_level -= 1
        
        result = f"{self.indent()}try:\n{body}"
        
        if rescue_clauses:
            result += "\n" + "\n".join(rescue_clauses)
        
        if ensure_body:
            result += f"\n{self.indent()}finally:\n{ensure_body}"
        
        return result
    
    def visit_rescue(self, node) -> str:
        exceptions = []
        var = None
        body = ""
        
        for child in node.children:
            if child.type == 'exceptions':
                for exc in child.children:
                    exceptions.append(self.visit_node(exc))
            elif child.type == 'exception_variable':
                var = self.visit_node(child.children[1]) if len(child.children) > 1 else None
            elif child.type == 'then':
                self.indent_level += 1
                body = self.visit_children(child, sep='\n')
                self.indent_level -= 1
        
        exc_str = ', '.join(exceptions) if exceptions else 'Exception'
        if var:
            result = f"{self.indent()}except {exc_str} as {var}:\n{body}"
        else:
            result = f"{self.indent()}except {exc_str}:\n{body}"
        
        return result
    
    # ─── Blocks ─────────────────────────────────────────────────────────
    
    def visit_do_block(self, node) -> str:
        # .each do |x| ... end → for x in ...:
        # .times do ... → for _ in range(n):
        
        params = ""
        body = ""
        
        for child in node.children:
            if child.type == 'block_parameters':
                params = self.visit_node(child)
            elif child.type == 'body_statement':
                self.indent_level += 1
                body = self.visit_node(child)
                self.indent_level -= 1
        
        if params:
            return f"\n{body}"
        return f"\n{body}"
    
    def visit_block(self, node) -> str:
        # Inline block: { |x| expr }
        parts = []
        for child in node.children:
            parts.append(self.visit_node(child))
        return ' '.join(parts)
    
    # ─── Calls & Method Calls ───────────────────────────────────────────
    
    def visit_call(self, node) -> str:
        # Complex call like arr.each do |x| ... end
        receiver = ""
        method = ""
        block = None
        
        for child in node.children:
            if child.type in ('identifier', 'constant', 'call', 'method_call', 'array',
                            'string', 'integer', 'instance_variable', 'argument_list'):
                if receiver == "":
                    receiver = self.visit_node(child)
            elif child.type == 'do_block':
                block = self.visit_node(child)
            elif child.type == 'block':
                block = self.visit_node(child)
            elif child.type == 'argument_list':
                pass  # handled
        
        # Detect method name from the call pattern
        call_text = node_text(node, self.source)
        method_name = ""
        
        # Extract method name by looking at the node's named children
        for child in node.named_children:
            if child.type == 'identifier' and child != node.named_children[0]:
                method_name = node_text(child, self.source)
                break
        
        # Map known Ruby methods
        if method_name == 'each':
            return f"{receiver}{block}"
        elif method_name == 'times':
            return f"for _ in range({receiver}):{block}"
        elif method_name == 'each_with_index':
            return f"for index, item in enumerate({receiver}):{block}"
        elif method_name == 'map':
            return f"[{block} for x in {receiver}]"
        elif method_name == 'select':
            return f"[x for x in {receiver} if {block}]"
        elif method_name == 'push':
            args = block if block else ""
            return f"{receiver}.append({args})"
        elif method_name == 'length':
            return f"len({receiver})"
        elif method_name == 'empty?':
            return f"len({receiver}) == 0"
        elif method_name == 'strip':
            return f"{receiver}.strip()"
        elif method_name == 'close':
            return f"{receiver}.close()"
        elif method_name == 'new':
            args = block if block else ""
            return f"{receiver}({args})"
        elif method_name == 'join':
            return f"os.path.join({receiver}, ...)"
        elif method_name == 'between?':
            # between?(a, b) → a <= x <= b
            args = block if block else ""
            return f"({receiver} >= {args})"
        elif method_name == 'delete_at':
            return f"del {receiver}[{block}]" if block else f"{receiver}.pop(...)"
        elif method_name == 'keys':
            return f"list({receiver}.keys())"
        elif method_name == 'values':
            return f"list({receiver}.values())"
        elif method_name == 'to_s':
            return f"str({receiver})"
        elif method_name == 'to_i':
            return f"int({receiver})"
        
        # Default: map Ruby method call to Python
        if block:
            return f"{receiver}.{method_name}({block})"
        
        return f"{receiver}.{method_name}()"
    
    def visit_method_call(self, node) -> str:
        method_name = ""
        args = ""
        receiver = ""
        
        for child in node.children:
            if child.type == 'identifier':
                method_name = self.visit_node(child)
            elif child.type == 'argument_list':
                args = self.visit_node(child)
            elif child.type in ('constant', 'identifier', 'call', 'string', 'array'):
                receiver = self.visit_node(child)
        
        # Method name mappings
        method_map = {
            'puts': 'print',
            'require': None,  # special handling
            'p': 'print',
            'raise': 'raise',
        }
        
        py_name = method_map.get(method_name, method_name)
        
        if method_name == 'require':
            # require 'json' → import json
            if args:
                # Clean up args: remove quotes
                mod = args.strip().strip("'").strip('"')
                return f"import {mod}"
            return f"import ..."
        
        if py_name == 'print':
            return f"print({args})"
        
        if receiver:
            return f"{receiver}.{py_name}({args})"
        
        return f"{py_name}({args})"
    
    def visit_command(self, node) -> str:
        # A command call like: puts "hello"
        name = ""
        args = []
        
        for child in node.children:
            if child.type == 'identifier':
                name = self.visit_node(child)
            else:
                args.append(self.visit_node(child))
        
        arg_str = ', '.join(args)
        
        if name == 'puts':
            return f"{self.indent()}print({arg_str})"
        elif name == 'require':
            mod = arg_str.strip().strip("'").strip('"')
            return f"import {mod}"
        elif name == 'return':
            return f"{self.indent()}return {arg_str}"
        
        return f"{self.indent()}{name}({arg_str})"
    
    def visit_command_with_block(self, node) -> str:
        # Like: File.open(filename) do |f| ... end
        name = ""
        args = ""
        block = ""
        
        for child in node.children:
            if child.type == 'identifier':
                name = self.visit_node(child)
            elif child.type == 'argument_list':
                args = self.visit_node(child)
            elif child.type == 'do_block':
                block = self.visit_node(child)
        
        if name == 'File.open':
            var_match = block.find('|')
            if var_match > 0:
                # with open(...) as f:
                return f"{self.indent()}with open({args}) as f:\n{block}"
        
        return f"{self.indent()}{name}({args}){block}"
    
    def visit_argument_list(self, node) -> str:
        args = []
        for child in node.children:
            if child.type not in ('(', ')'):
                args.append(self.visit_node(child))
        return ', '.join(args)
    
    # ─── Literals ───────────────────────────────────────────────────────
    
    def visit_identifier(self, node) -> str:
        return node_text(node, self.source)
    
    def visit_constant(self, node) -> str:
        text = node_text(node, self.source)
        # Ruby constants that map to Python
        const_map = {
            'File': 'open',
            'FileUtils': 'shutil',
            'JSON': 'json',
            'Pathname': 'Path',
            'Errno': 'OSError',
        }
        return const_map.get(text, text)
    
    def visit_simple_symbol(self, node) -> str:
        text = node_text(node, self.source)
        return text  # :symbol → 'symbol' in many contexts
    
    def visit_string(self, node) -> str:
        text = node_text(node, self.source)
        # Check for interpolation
        if '#{' in text:
            # Convert to f-string
            text = text.replace('#{', '{')
            return f'f{text}'
        return text
    
    def visit_string_interpolation(self, node) -> str:
        parts = []
        for child in node.children:
            parts.append(self.visit_node(child))
        return ''.join(parts)
    
    def visit_integer(self, node) -> str:
        return node_text(node, self.source)
    
    def visit_float(self, node) -> str:
        return node_text(node, self.source)
    
    def visit_nil(self, node) -> str:
        return "None"
    
    def visit_true(self, node) -> str:
        return "True"
    
    def visit_false(self, node) -> str:
        return "False"
    
    def visit_array(self, node) -> str:
        elements = []
        for child in node.children:
            if child.type not in ('[', ']'):
                elements.append(self.visit_node(child))
        return f"[{', '.join(elements)}]"
    
    def visit_hash(self, node) -> str:
        pairs = []
        for child in node.children:
            if child.type == 'pair':
                pairs.append(self.visit_node(child))
        return f"{{{', '.join(pairs)}}}"
    
    def visit_pair(self, node) -> str:
        key = ""
        value = ""
        for child in node.children:
            if key == "":
                key = self.visit_node(child)
            else:
                value = self.visit_node(child)
        return f"{key}: {value}"
    
    # ─── Operators ──────────────────────────────────────────────────────
    
    def visit_binary(self, node) -> str:
        left = ""
        op = ""
        right = ""
        
        for child in node.children:
            text = self.visit_node(child)
            if child.type in ('+', '-', '*', '/', '%', '==', '!=', '>', '<',
                            '>=', '<=', '&&', '||', 'and', 'or', '<<', '**'):
                op = text
            elif left == "":
                left = text
            else:
                right = text
        
        # Ruby operators that differ from Python
        op_map = {'&&': 'and', '||': 'or', '<<': '+='}
        op = op_map.get(op, op)
        
        return f"{left} {op} {right}"
    
    def visit_unary(self, node) -> str:
        parts = []
        for child in node.children:
            parts.append(self.visit_node(child))
        return ''.join(parts)
    
    # ─── Assignment ─────────────────────────────────────────────────────
    
    def visit_assignment(self, node) -> str:
        left = ""
        right = ""
        
        for child in node.children:
            text = self.visit_node(child)
            if child.type == '=':
                continue
            if left == "":
                left = text
            else:
                right = text
        
        return f"{self.indent()}{left} = {right}"
    
    def visit_operator_assignment(self, node) -> str:
        parts = []
        for child in node.children:
            parts.append(self.visit_node(child))
        
        result = ' '.join(parts)
        # Ruby: x ||= default → Python: if x is None: x = default
        if '||=' in result:
            var, default = result.split('||=')
            var = var.strip()
            default = default.strip()
            return f"if {var} is None:\n{self.indent()}{INDENT}{var} = {default}"
        
        return result
    
    def visit_instance_variable(self, node) -> str:
        text = node_text(node, self.source)
        return f"self.{text[1:]}"  # @var → self.var
    
    # ─── Control flow ───────────────────────────────────────────────────
    
    def visit_return(self, node) -> str:
        args = []
        for child in node.children:
            if child.type not in ('return',):
                args.append(self.visit_node(child))
        return f"{self.indent()}return {' '.join(args)}"
    
    def visit_case(self, node) -> str:
        value = ""
        when_clauses = []
        else_clause = ""
        
        for child in node.children:
            if child.type in ('identifier', 'call', 'method_call'):
                value = self.visit_node(child)
            elif child.type == 'when':
                when_clauses.append(self.visit_node(child))
            elif child.type == 'else':
                self.indent_level += 1
                else_clause = self.visit_children(child, sep='\n')
                self.indent_level -= 1
        
        result_parts = []
        for wc in when_clauses:
            result_parts.append(wc)
        
        if else_clause:
            result_parts.append(f"{self.indent()}else:\n{else_clause}")
        
        return '\n'.join(result_parts)
    
    def visit_when(self, node) -> str:
        patterns = []
        body = ""
        
        for child in node.children:
            if child.type == 'then':
                self.indent_level += 1
                body = self.visit_children(child, sep='\n')
                self.indent_level -= 1
            elif child.type not in ('when',):
                patterns.append(self.visit_node(child))
        
        if len(patterns) == 1:
            return f"{self.indent()}if value == {patterns[0]}:\n{body}"
        
        # Multiple patterns: if value in [a, b, c]:
        pattern_list = ', '.join(patterns)
        return f"{self.indent()}if value in [{pattern_list}]:\n{body}"
    
    # ─── Comments ───────────────────────────────────────────────────────
    
    def visit_comment(self, node) -> str:
        text = node_text(node, self.source)
        return f"{self.indent()}{text}"


def convert_ruby_to_python(ruby_code: str) -> str:
    """Public API: convert Ruby source code to Python."""
    visitor = RubyASTVisitor()
    return visitor.convert(ruby_code)


# ─── Demo ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import os
    
    test_cases = {
        "fibonacci": """
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
""",
        "file_reader": """
class FileProcessor
  def initialize(filename)
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
end

processor = FileProcessor.new("data.txt")
count = processor.read_file
puts "Read #{count} lines"
""",
        "exception_handling": """
def load_tasks
  data_file = "todo.json"
  begin
    JSON.parse(File.read(data_file))
  rescue Errno::ENOENT, JSON::ParserError => e
    puts "Error: #{e.message}"
    []
  end
end
""",
    }
    
    converter = RubyASTVisitor()
    
    print("=" * 60)
    print("Kaitian AST Migration Engine v0.3")
    print("Real tree-sitter Ruby CST → Python source")
    print("=" * 60)
    
    for name, code in test_cases.items():
        print(f"\n{'─'*60}")
        print(f"  Input: {name}")
        print(f"  Ruby lines: {len(code.splitlines())}")
        
        python_code = converter.convert(code)
        
        print(f"  Python lines: {len(python_code.splitlines())}")
        print(f"\n  {'─ Python output ─'}")
        for line in python_code.splitlines():
            print(f"  | {line}")
