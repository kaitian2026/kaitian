# 开天

> 让中文成为计算的原生语言。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.3--alpha-orange.svg)]()
[![Status](https://img.shields.io/badge/status-proof--of--concept-lightgrey.svg)]()

**⚠️ Alpha 阶段 / 概念验证。** 架构设计已到位，但 AST 迁移引擎有已知 bug，游戏/药物/基因组学模块为零实现。详见[已知限制](#已知限制)。

---

## 开天是什么

开天是一个开源智能体框架，目标是对标闭源平台的公开能力，并增加两项独特优势：

1. **中文原生语义映射** — 键盘扫描码 → 拼音 → 汉字 → 代码语义，不经过英文中间层
2. **科拉茨收敛调度器** — 任务拆解后有数学保证的收敛路径，不是随机探索

它证明了一件事：**智能体能力可以用规则 + 协议 + 轻量模型 + 任务调度来构建**，不需要黑盒云 API。

---

## 能力对标

| 能力 | 实现方式 | 状态 |
|------|---------|------|
| 代码迁移 (Ruby→Python) | 正则引擎 v0.2 + AST 引擎 v0.3 (tree-sitter) | 开发中 |
| 游戏操作 | 截图 + YOLO + 状态机 + 按键映射 | 规划中 |
| 药物设计 | AlphaFold2 / AutoDock 封装 | 规划中 |
| 基因组学 | 特征工程 + XGBoost 流程 | 规划中 |
| 长周期无监督任务 | 科拉茨收敛调度器 | Demo 就绪 |
| 工具调用 | 可扩展执行层 | 设计阶段 |
| 中文语义理解 | 扫描码 → 拼音 → 汉字 → 语义管道 | 核心管道私有加载；50 条表面映射公开 |
| 本地运行 | Python 3.10+，无需网络 | 是 |

---

## 四层架构

```
应用层（用户指令）
        ↓
调度层（科拉茨收敛器）
  拆解 → 执行 → 验证
  成功 ÷2（收缩资源）
  失败 ×3+1（扩展探索）→ 收敛到 1
        ↓
执行层（协议封装 & 工具调用）
  代码迁移 | 视觉识别+按键 | 科学计算 | 文件/网络/数据库
        ↓
语义层（中文映射表 + 外置记忆库）
  表层：50 条中文→Python 公开映射
  深层：扫描码→拼音→汉字→语义（私有模块加载，不在此仓库）
```

---

## 为什么叫"开天"

盘古开天辟地。不是中文编程语言，不是汉化版 Python，而是从键盘扫描码到语义映射，让中文成为计算的第一公民。

---

## 快速开始

```bash
git clone https://github.com/kaitian2026/kaitian.git
cd kaitian
pip install -r requirements.txt

# 科拉茨调度器 Demo — 生成收敛路径可视化图
python collatz_scheduler/demo_visualization.py

# 代码迁移 Demo — 转换 4 个 Ruby 示例到 Python
python code_migration/ruby_to_python_rules.py

# 键盘扫描码 Demo — PS/2 Set 1 → 英文字母
python keyboard_mapping/scan_to_english.py
```

详细使用说明见 [USAGE_zh.txt](USAGE_zh.txt) 或 [USAGE_en.txt](USAGE_en.txt)。

---

## 项目结构

```
开天/
├── README.md / README_CN.md
├── USAGE_en.txt / USAGE_zh.txt
├── LICENSE
├── ARCHITECTURE.md
├── QUICKSTART.md
├── index.html              交互式展示页（浏览器直接打开）
├── requirements.txt
├── .gitignore
├── .github/
│   └── ISSUE_TEMPLATE.md
├── code_migration/
│   ├── ruby_to_python_rules.py   正则引擎 v0.2
│   ├── ast_migration.py          AST 引擎 v0.3（tree-sitter）
│   ├── demo_examples/            4 个 Ruby 测试案例
│   └── demo_output_v2/           转换后的 Python 输出
├── collatz_scheduler/
│   ├── scheduler.py              科拉茨核心调度器
│   ├── demo_visualization.py     收敛路径绘图
│   └── real_workload_demo.py     真实负载测试（4/4 爆炸 = 需策略切换）
├── keyboard_mapping/
│   └── scan_to_english.py        PS/2 扫描码 → 英文字母
└── mapping_table/
    └── chinese_mapping.json       50 条中文 → Python 表面映射
```

---

## 已知限制

当前为 **Alpha** 版本，以下限制已如实标明：

1. **AST 引擎 (v0.3)**：树遍历架构正确，但操作符映射、方法调用格式、参数默认值有已知 bug。尚未产出可运行 Python。

2. **正则引擎 (v0.2)**：不处理 `begin/rescue/ensure`、`case/when`、`each_with_index`、`OptionParser`、块多变量、`require` 语句。

3. **无端到端迁移成功案例**：尚未验证「输入 Ruby 项目 → 输出可运行 Python 项目」全流程。

4. **科拉茨调度器**：目前仅驱动规则引擎，未接入真实 LLM。当前仅作为策略有效/无效判定器使用。

5. **游戏/药物/基因组学模块**：架构中声明，实际零实现，仅为预留模块。

6. **语义映射管道**：仅 50 条表面中文→Python 映射公开。完整的扫描码→拼音→汉字→语义管道通过私有模块加载，不在此仓库中。

---

## 路线图

- [x] v0.1 — 核心模块：映射表、科拉茨调度器、代码迁移 Demo
- [x] v0.2 — 正则引擎升级（10-pass 管道）、真实 Ruby 项目测试
- [x] v0.3 — AST 引擎（tree-sitter）、真实负载测试、交互式 HTML 展示 ← **当前**
- [ ] v0.4 — 修复 AST 引擎 bug、端到端迁移管道、Docker 打包
- [ ] v0.5 — 游戏自动化 Demo、科学工具封装
- [ ] v1.0 — 全能力对标目标、插件系统、Web UI

---

## 许可证

MIT。详见 [LICENSE](LICENSE)。

独立实现，未逆向工程，未复制任何闭源平台代码。所有能力均基于公开文档原理和已发表研究构建。
