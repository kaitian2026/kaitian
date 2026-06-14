---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 7b00c2a0d2c4daa4870ec1942a7c7142_6b52a4da67e411f1aa625254006c9bbf
    ReservedCode1: NC7SvMVwPmDNsmboU9dS2rW0CgNLRmluDz7nSpxeQd8Ss6h+z00tOdUrMM2ceosrwMiSaYy8vi57kLkcNbTKwVhVHVoXRcJ4uZ2PRXkvWn/UzMr+QfVEH2TShKQ6UiSMu6MjcwmtfO7duSN6D7RSdJDJBE2SSMBUCWlknPjkRAZZRCBuNOKeiGUOpeU=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 7b00c2a0d2c4daa4870ec1942a7c7142_6b52a4da67e411f1aa625254006c9bbf
    ReservedCode2: NC7SvMVwPmDNsmboU9dS2rW0CgNLRmluDz7nSpxeQd8Ss6h+z00tOdUrMM2ceosrwMiSaYy8vi57kLkcNbTKwVhVHVoXRcJ4uZ2PRXkvWn/UzMr+QfVEH2TShKQ6UiSMu6MjcwmtfO7duSN6D7RSdJDJBE2SSMBUCWlknPjkRAZZRCBuNOKeiGUOpeU=
---

# Architecture

Kaitian follows a four-layer architecture. Each layer is independently testable and replaceable.

---

## Layer 1: Application Layer

**What it does**: Receives user commands in natural language (Chinese or English).

**Input**: Text command from user.

**Output**: Parsed intent passed to the Scheduling Layer.

This layer is intentionally thin — it does not perform any execution. Its sole job is to normalize user input into a structured task descriptor.

---

## Layer 2: Scheduling Layer — Collatz Convergence Scheduler

**What it does**: Decomposes complex tasks into subtasks, schedules execution, and guarantees convergence.

**Algorithm**:
```
For each subtask:
  1. Execute
  2. If success: shrink task complexity (÷2)
  3. If failure: expand exploration scope (×3+1)
  4. Repeat until complexity converges to 1 (task complete)
```

**Why Collatz**: The 3n+1 conjecture provides a mathematical framework where every starting point eventually reaches 1. Applied to task scheduling, this means every task — no matter how complex — has a guaranteed path to completion. The scheduler doesn't guess; it follows a deterministic convergence protocol.

**Key properties**:
- No random exploration (unlike Mythos 5's stochastic approach)
- Deterministic backtracking on failure
- Complexity metric is task-specific and configurable

---

## Layer 3: Execution Layer

**What it does**: Executes subtasks dispatched by the scheduler, using protocol-encapsulated tools.

**Modules**:

| Module | Description |
|--------|-------------|
| Code Migration Engine | Rule-based AST transformation between programming languages |
| Vision + Input Engine | Screenshot capture, object detection (YOLO), state machine, keyboard/mouse simulation |
| Scientific Wrappers | Thin wrappers around AlphaFold2, AutoDock, and other open-source scientific tools |
| File / Network / DB | Standard I/O operations, HTTP requests, database queries |

Each module implements a uniform protocol interface, making them interchangeable and extensible.

---

## Layer 4: Semantic Layer

**What it does**: Maps between Chinese semantics, English programming constructs, and machine operations.

**Components**:
- **Mapping Table**: Chinese keywords → English equivalents (e.g., "如果" → "if"). This is the public interface. The full mapping rules (including pinyin, abbreviated input, and scan-code direct mapping) are documented separately.
- **External Memory Store**: Append-only knowledge base for long-horizon tasks. Never overwrites — only appends — ensuring auditability and traceability.

**Design principle**: The semantic layer is a bridge, not a translator. It doesn't convert Chinese to English and then execute — it maps directly from Chinese semantics to machine operations, with English equivalents provided only for compatibility with existing tools.

---

## Data Flow

```
User: "把这个Ruby项目转成Python"
        ↓
[Application Layer] → Task{type: "code_migration", source: "Ruby", target: "Python"}
        ↓
[Scheduling Layer]  → Subtask{files: [...]}, complexity: N
        ↓
[Execution Layer]   → Code Migration Engine processes each file
        ↓
[Semantic Layer]    → Chinese business semantics preserved in variable names and comments
        ↓
Result: Python project with original semantics intact
```

---

## Design Decisions

1. **Rules over Models**: Kaitian prefers explicit rules over black-box models whenever possible. Models are used only where rules are infeasible (e.g., visual recognition).

2. **Protocol over Integration**: Tools are wrapped in uniform protocols, not hard-coded integrations. Adding a new tool means implementing a protocol, not modifying the core.

3. **Determinism over Probability**: The Collatz scheduler guarantees convergence. No "probably works" — it either converges or reports exactly where it stopped and why.

4. **Chinese-First**: The entire pipeline is designed for Chinese as the primary language. English support is a compatibility layer, not the foundation.
*（内容由AI生成，仅供参考）*
