"""
Kaitian - Collatz Scheduler: Real Workload Demo
===============================================
Drives the actual code migration engine through the Collatz convergence protocol.
Each step is a real Ruby → Python conversion with syntax validation.

Protocol:
  Syntax-valid output → Collatz success → complexity ÷ 2
  Syntax error        → Collatz failure  → complexity × 3 + 1
  Repeat until complexity converges to 1.
"""

import os
import sys
import ast as py_ast
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code_migration"))

from scheduler import CollatzScheduler


def main():
    scheduler = CollatzScheduler(max_iterations=50)

    demo_dir = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "code_migration", "demo_examples")
    )

    # Gather Ruby files
    rb_files = {}
    for fn in sorted(os.listdir(demo_dir)):
        if fn.endswith(".rb"):
            filepath = os.path.join(demo_dir, fn)
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
            rb_files[fn] = (filepath, lines)

    # Decompose into subtasks
    task_list = [(f"Migrate {fn}", lines) for fn, (_, lines) in rb_files.items()]
    scheduler.decompose(task_list)

    from ruby_to_python_rules import RubyToPythonConverterV2
    converter = RubyToPythonConverterV2()

    def executor(description, complexity):
        """Execute migration attempt. Returns True on syntax-valid output."""
        fn = description.replace("Migrate ", "")
        filepath = rb_files[fn][0]

        with open(filepath, 'r', encoding='utf-8') as f:
            ruby_code = f.read()

        python_code = converter.convert(ruby_code)

        try:
            py_ast.parse(python_code)
            return True
        except SyntaxError:
            return False

    print("=" * 60)
    print("Kaitian Collatz Scheduler — Real Migration Test")
    print("=" * 60)
    print(f"  Tasks: {len(rb_files)} Ruby files")
    print(f"  Protocol: Success → ÷2 | Failure → ×3+1\n")

    subtasks = scheduler.run(executor)
    print(scheduler.summary())

    converged = sum(1 for s in subtasks if s.status.value == "converged")
    print(f"\n  Overall: {converged}/{len(subtasks)} converged")


if __name__ == "__main__":
    main()
