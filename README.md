# 开天 (Kaitian)

> Make Chinese a native computing language. An open-source alternative to Mythos 5.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.3--alpha-orange.svg)]()
[![Status](https://img.shields.io/badge/status-proof--of--concept-lightgrey.svg)]()

**⚠️ Alpha / Proof of Concept.** The architecture is solid, but the AST migration engine has known bugs and several modules (game, drug design, genomics) are placeholder-only. See [Known Limitations](#known-limitations).

---

## What is Kaitian?

Kaitian is an open-source framework that aims to match the capabilities of closed-source intelligent agent platforms — adding two unique advantages:

1. **Chinese-native semantic mapping** — scan code → pinyin → hanzi → code, bypassing English intermediates
2. **Collatz convergence scheduler** — mathematically guaranteed task convergence, not random exploration

It demonstrates that agent capabilities can be built from **rules + protocols + lightweight models + task scheduling** rather than black-box cloud APIs.

---

## Capability Map

| Capability | Approach | Status |
|------------|----------|--------|
| Code migration (Ruby→Python) | Regex engine v0.2 + AST engine v0.3 (tree-sitter) | In progress |
| Game automation | Screenshot + YOLO + state machine + key mapping | Planned |
| Drug design | AlphaFold2 / AutoDock wrappers | Planned |
| Genomics | Feature engineering + XGBoost pipelines | Planned |
| Long-horizon tasks | Collatz convergence scheduler | Demo ready |
| Tool orchestration | Extensible executor layer | Design phase |
| Chinese semantics | Scan code → pinyin → hanzi → code pipeline | Core pipeline private; 50 surface mappings public |
| Local execution | Python 3.10+, no cloud dependency | Yes |

---

## Architecture (4 Layers)

```
Application Layer (User Commands)
        ↓
Scheduling Layer (Collatz Scheduler)
  Decompose → Execute → Verify
  Success: ÷2 (shrink)
  Failure: ×3+1 (expand) → converge to 1
        ↓
Execution Layer (Protocols & Tools)
  Code Migration | Vision + Input | Scientific Wrappers | File/Net/DB
        ↓
Semantic Layer (Mapping Table + Memory)
  Surface: 50 Chinese→Python public mappings
  Deep: scan code → pinyin → hanzi → semantic (private module, not in this repo)
```

---

## Quick Start

```bash
git clone https://github.com/kaitian2026/kaitian.git
cd kaitian
pip install -r requirements.txt

# Collatz scheduler demo — generates convergence path visualization
python collatz_scheduler/demo_visualization.py

# Code migration demo — converts 4 Ruby examples to Python
python code_migration/ruby_to_python_rules.py

# Keyboard scan code demo — PS/2 Set 1 → English letters
python keyboard_mapping/scan_to_english.py
```

See [USAGE_en.txt](USAGE_en.txt) or [USAGE_zh.txt](USAGE_zh.txt) for detailed walkthrough.

---

## Project Structure

```
kaitian/
├── README.md / README_CN.md
├── USAGE_en.txt / USAGE_zh.txt
├── LICENSE
├── ARCHITECTURE.md
├── QUICKSTART.md
├── index.html              Interactive showcase (open in browser)
├── requirements.txt
├── .gitignore
├── .github/
│   └── ISSUE_TEMPLATE.md
├── code_migration/
│   ├── ruby_to_python_rules.py   Regex engine v0.2
│   ├── ast_migration.py          AST engine v0.3 (tree-sitter)
│   ├── demo_examples/            4 Ruby test cases
│   └── demo_output_v2/           Converted Python output
├── collatz_scheduler/
│   ├── scheduler.py              Core Collatz scheduler
│   ├── demo_visualization.py     Convergence path plotter
│   └── real_workload_demo.py     Real workload test (4/4 explode = strategy switch needed)
├── keyboard_mapping/
│   └── scan_to_english.py        PS/2 scan code → English letters
└── mapping_table/
    └── chinese_mapping.json      50 Chinese → Python surface mappings
```

---

## Known Limitations

This is an **alpha** release. The following limitations are acknowledged:

1. **AST Engine (v0.3)**: Tree traversal is architecturally correct, but operator mapping, method call formatting, and parameter defaults have known bugs. Does not yet produce runnable Python output.

2. **Regex Engine (v0.2)**: Does not handle `begin/rescue/ensure`, `case/when`, `each_with_index`, `OptionParser`, block multi-variables, or `require` statements.

3. **No end-to-end migration success case**: There is no verified pipeline from "input Ruby project" to "output runnable Python project".

4. **Collatz scheduler**: Currently drives rule engines only, not connected to real LLMs. Functions as a strategy validity classifier.

5. **Game / Drug / Genomics modules**: Declared in architecture, zero implementation. Placeholder modules only.

6. **Semantic pipeline**: Only 50 surface-level Chinese→Python mappings are public. The full scan-code→pinyin→hanzi→semantic pipeline is loaded via private modules and not included in this repository.

---

## Roadmap

- [x] v0.1 — Core modules: mapping table, Collatz scheduler, code migration demo
- [x] v0.2 — Regex engine upgrade (10-pass pipeline), real-world Ruby project testing
- [x] v0.3 — AST engine (tree-sitter), real workload test, interactive HTML showcase ← **current**
- [ ] v0.4 — Fix AST engine bugs, end-to-end migration pipeline, Docker packaging
- [ ] v0.5 — Game automation demo, scientific tool wrappers
- [ ] v1.0 — Full capability parity target, plugin system, web UI

---

## Connect

- **GitHub Issues**: Bug reports, feature requests, ideas
- **Email**: [kaitian2026@proton.me](mailto:kaitian2026@proton.me)
- **Sponsor**: If this project interests you, consider [sponsoring on GitHub](https://github.com/sponsors/kaitian2026) to support development.

---

## License

MIT. See [LICENSE](LICENSE).

Independent implementation. No reverse engineering. No copied code from any closed-source platform. All capabilities are built from publicly documented principles and published research.
