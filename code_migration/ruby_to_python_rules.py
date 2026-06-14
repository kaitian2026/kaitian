"""
Kaitian - Rule-Based Code Migration Engine (Enhanced v0.2)
Version 0.2.0

Converts Ruby source code to Python using multi-pass rule-based transformations.
Enhanced with indentation handling, @→self. conversion, string interpolation,
block structure cleanup, and method call mapping.

Design: Multiple passes, each handling one category of transformation.
"""

import re
import os
from typing import List, Tuple, Dict


TOKEN_RULES: List[Tuple[str, str, str]] = [
    ("elsif", "elif", "Ruby 'elsif' → Python 'elif'"),
    ("nil", "None", "Ruby 'nil' → Python 'None'"),
    ("true", "True", "Ruby 'true' → Python 'True'"),
    ("false", "False", "Ruby 'false' → Python 'False'"),
    ("unless", "if not", "Ruby 'unless' → Python 'if not'"),
]

METHOD_MAP = {
    ".length": "len(__SELF__)",
    ".size": "len(__SELF__)",
    ".empty?": "len(__SELF__) == 0",
    ".push(": ".append(",
    ".strip": ".strip()",
    ".close": ".close()",
    ".each ": "__SELF__",
}

GLOBAL_MAP = {
    "puts ": "print(",
    "Array.new": "[]",
}


class RubyToPythonConverterV2:

    def __init__(self):
        self.applied_rules: List[str] = []

    def convert(self, ruby_code: str) -> str:
        code = ruby_code
        self.applied_rules = []
        lines = code.split('\n')

        # Pass 1: Token replacements
        for old, new, desc in TOKEN_RULES:
            new_lines = []
            for line in lines:
                new_line = re.sub(r'\b' + old + r'\b', new, line)
                if new_line != line and old not in self.applied_rules:
                    self.applied_rules.append(old)
                new_lines.append(new_line)
            lines = new_lines

        # Pass 2: @variable → self.variable
        new_lines = []
        for line in lines:
            if '@' in line and not line.strip().startswith('#'):
                new_line = re.sub(r'@(\w+)', r'self.\1', line)
                if new_line != line and '@ivar' not in self.applied_rules:
                    self.applied_rules.append('@ivar→self.ivar')
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        lines = new_lines

        # Pass 3: def/class → add colon, remove end
        new_lines = []
        for line in lines:
            stripped = line.strip()
            if re.match(r'^\s*def\s+\w+', stripped) and not stripped.endswith(':'):
                line = re.sub(r'(def\s+\w+(\([^)]*\))?)', r'\1:', line)
                if 'def:' not in self.applied_rules:
                    self.applied_rules.append('def→def:')
            if re.match(r'^\s*class\s+\w+', stripped) and not stripped.endswith(':'):
                line = re.sub(r'(class\s+\w+)', r'\1:', line)
                if 'class:' not in self.applied_rules:
                    self.applied_rules.append('class→class:')
            new_lines.append(line)
        lines = new_lines

        # Pass 4: Method call transformations
        new_lines = []
        for line in lines:
            for ruby_method, py_replacement in METHOD_MAP.items():
                if ruby_method in line:
                    m = re.match(r'(\s*)(.*?)' + re.escape(ruby_method), line)
                    if m:
                        indent = m.group(1)
                        receiver = m.group(2).strip()
                        rest = line[m.end():]
                        new_line = indent + py_replacement.replace('__SELF__', receiver) + rest
                        line = new_line
                        if ruby_method not in self.applied_rules:
                            self.applied_rules.append(ruby_method)
            for ruby_global, py_replacement in GLOBAL_MAP.items():
                if ruby_global in line:
                    line = line.replace(ruby_global, py_replacement)
                    if ruby_global not in self.applied_rules:
                        self.applied_rules.append(ruby_global)
            new_lines.append(line)
        lines = new_lines

        # Pass 5: String interpolation #{expr} → {expr}
        new_lines = []
        for line in lines:
            if '#{' in line and ('"' in line or "'" in line):
                line = re.sub(r'#\{([^}]+)\}', r'{\1}', line)
                line = re.sub(r'(print\s*)', r'\1(f', line)
                if '#{}' not in self.applied_rules:
                    self.applied_rules.append('#{}→f-string')
            new_lines.append(line)
        lines = new_lines

        # Pass 6: .times do → for _ in range()
        new_lines = []
        for line in lines:
            m = re.match(r'(\s*)\(?(\d+|[a-z_]\w*)\)?\s*\.times\s+do\b', line)
            if m:
                indent, count = m.group(1), m.group(2)
                line = f"{indent}for _ in range({count}):"
                if '.times' not in self.applied_rules:
                    self.applied_rules.append('.times→range')
            new_lines.append(line)
        lines = new_lines

        # Pass 7: .each do |var| → for var in ...:
        new_lines = []
        for line in lines:
            m = re.match(r'(\s*)(\S+)\.each\s+do\s+\|(\w+)\|', line)
            if m:
                indent, obj, var = m.group(1), m.group(2), m.group(3)
                line = f"{indent}for {var} in {obj}:"
                if '.each' not in self.applied_rules:
                    self.applied_rules.append('.each→for')
            new_lines.append(line)
        lines = new_lines

        # Pass 8: Remove bare 'end' lines
        new_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped == 'end':
                line = ''
            new_lines.append(line)
        lines = new_lines

        # Pass 9: .new(...) → ClassName(...)
        new_lines = []
        for line in lines:
            m = re.search(r'(\w+)\.new\(', line)
            if m:
                line = re.sub(r'(\w+)\.new\(', r'\1(', line)
                if '.new' not in self.applied_rules:
                    self.applied_rules.append('.new→constructor')
            new_lines.append(line)
        lines = new_lines

        # Pass 10: File.open → open
        new_lines = []
        for line in lines:
            if 'File.open(' in line:
                line = line.replace('File.open(', 'open(')
                if 'File.open' not in self.applied_rules:
                    self.applied_rules.append('File.open→open')
            new_lines.append(line)
        lines = new_lines

        # Pass 11: Fix print( → print(f for interpolated strings
        new_lines = []
        for line in lines:
            if 'print(f' in line and not line.rstrip().endswith(')'):
                line = line.rstrip() + ')'
            if line.strip().startswith('print ') and not line.strip().endswith(')') and 'print(f' not in line:
                line = re.sub(r'(print\s+)(.+)', r'\1(\2)', line)
                idx = line.rfind('"')
                if idx > 0:
                    line = line[:idx+1] + ')'
            new_lines.append(line)
        lines = new_lines

        # Collapse blank lines
        result_lines = []
        prev_blank = False
        for line in lines:
            is_blank = line.strip() == ''
            if is_blank and prev_blank:
                continue
            result_lines.append(line)
            prev_blank = is_blank

        return '\n'.join(result_lines)

    def convert_file(self, input_path: str, output_path: str) -> Dict:
        with open(input_path, 'r', encoding='utf-8') as f:
            ruby_code = f.read()
        python_code = self.convert(ruby_code)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(python_code)
        return {
            "input": input_path,
            "output": output_path,
            "rules_applied": self.applied_rules,
            "ruby_lines": len(ruby_code.splitlines()),
            "python_lines": len(python_code.splitlines()),
        }


if __name__ == "__main__":
    converter = RubyToPythonConverterV2()
    demo_dir = os.path.join(os.path.dirname(__file__), "demo_examples")
    output_dir = os.path.join(os.path.dirname(__file__), "demo_output_v2")
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print("Kaitian Code Migration Engine v0.2 — Multi-Pass Rules")
    print("=" * 60)

    for filename in sorted(os.listdir(demo_dir)):
        if filename.endswith(".rb"):
            input_path = os.path.join(demo_dir, filename)
            output_name = filename.replace(".rb", ".py")
            output_path = os.path.join(output_dir, output_name)
            result = converter.convert_file(input_path, output_path)
            print(f"\n{'─'*60}")
            print(f"  {filename} → {output_name}")
            print(f"  Rules: {result['rules_applied']}")
            print(f"  Lines: {result['ruby_lines']} → {result['python_lines']}")
            with open(output_path, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    print(f"  | {line.rstrip()}")
