---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 7b00c2a0d2c4daa4870ec1942a7c7142_6ba128a067e411f18805525400d9a7a1
    ReservedCode1: oXrwTOwUNfxbj7EKvd23z/5P09rdzZTUil2735Ecl8xgUP+64ji4BiNr2N1yhlx5pKj7fpGAwCYyQ2Fc59ZjGk5rHL8ZZMGFCoi6YuJgbqvjnFhVq69gjSHodpnGlCWP2/lShLjdMXPPZEVAmh+T5RJTdfb/r1qXnAyZB6Gy/LzVicjT9jq0QDP/Fzc=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 7b00c2a0d2c4daa4870ec1942a7c7142_6ba128a067e411f18805525400d9a7a1
    ReservedCode2: oXrwTOwUNfxbj7EKvd23z/5P09rdzZTUil2735Ecl8xgUP+64ji4BiNr2N1yhlx5pKj7fpGAwCYyQ2Fc59ZjGk5rHL8ZZMGFCoi6YuJgbqvjnFhVq69gjSHodpnGlCWP2/lShLjdMXPPZEVAmh+T5RJTdfb/r1qXnAyZB6Gy/LzVicjT9jq0QDP/Fzc=
---

# Quick Start

Get Kaitian running in 5 minutes.

---

## Prerequisites

- Python 3.10+
- pip
- Git

---

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/kaitian.git
cd kaitian

# Install dependencies
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist yet (v0.1), install manually:

```bash
pip install matplotlib
```

---

## Run the Demos

### 1. Collatz Scheduler Visualization

See the convergence algorithm in action:

```bash
python collatz_scheduler/demo_visualization.py
```

This generates a convergence path chart for sample task complexities. Each point shows how the scheduler shrinks or expands task scope until reaching completion.

### 2. Code Migration Demo

Convert a Ruby snippet to Python:

```bash
python code_migration/ruby_to_python_rules.py
```

This applies rule-based transformations to the example files in `code_migration/demo_examples/`. Check the output to see before/after comparisons.

### 3. Keyboard Mapping Demo

See how keyboard scan codes map to characters:

```bash
python keyboard_mapping/scan_to_english.py
```

This demonstrates the scan-code-to-character pipeline that powers Kaitian's input layer. (v0.1 maps to English letters only; Chinese mapping is in development.)

---

## Explore the Mapping Table

```bash
python -c "import json; data=json.load(open('mapping_table/chinese_mapping.json')); print(f'{len(data)} entries loaded')"
```

---

## What's Next

- Try modifying the rule set in `code_migration/ruby_to_python_rules.py` to add your own language pairs
- Experiment with different complexity starting values in `collatz_scheduler/scheduler.py`
- Read `ARCHITECTURE.md` for the full design rationale

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | `pip install matplotlib` |
| Chinese characters display as gibberish | Set terminal encoding to UTF-8 |
| Demo produces no output | Check Python version (`python --version`), need 3.10+ |
*（内容由AI生成，仅供参考）*
