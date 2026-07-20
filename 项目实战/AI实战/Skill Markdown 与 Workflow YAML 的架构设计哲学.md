---
title: Skill Markdown 与 Workflow YAML 的架构设计哲学
tags:
  - 架构设计
  - skill设计
  - workflow
  - YAML
  - Markdown
  - Agent系统
created: 2026-07-20
updated: 2026-07-20
status: completed
source_project: AI实战
---

# Skill Markdown 与 Workflow YAML 的架构设计哲学

## 核心问题

Skill 和工作流映射表在 Agent 系统中承担不同的角色。**Skill 不是单纯的"配置数据"，而是给模型阅读和执行的操作说明书；工作流映射表则更接近程序要读取的结构化路由配置。**

> [!abstract] 一句话总结
> **Markdown 适合 Agent 的语义指令，YAML 适合 Agent 系统的确定性配置。**

---

## Skill 为什么常用 Markdown

一个 Skill 往往包含这些内容：

- 这个 Skill 用来做什么
- 什么时候应该调用
- 什么时候**不应该**调用
- 执行时要遵循哪些步骤
- 遇到异常如何判断
- 有哪些注意事项
- 输入输出示例

这类内容包含大量**语义、解释、边界条件和示例**，Markdown 很适合表达：

```markdown
# Code Review Skill

## 适用场景

当用户要求检查代码质量、安全问题或潜在 Bug 时使用。

## 不适用场景

如果用户明确要求直接修改代码，应调用 implementation skill。

## 执行步骤

1. 理解改动目标。
2. 检查正确性。
3. 检查安全风险。
4. 输出按严重程度排序的问题。

## 注意事项

不要只给出笼统评价。每个问题必须指出具体位置和影响。
```

LLM 对自然语言指令理解得很好，而且 Markdown 的标题、列表、代码块可以帮助模型区分不同层次的信息。

### 如果全部用 YAML

```yaml
name: code-review
applicable_when:
  - user requests code review
  - user requests security analysis
not_applicable_when:
  - user requests direct implementation
steps:
  - understand goal
  - inspect correctness
  - inspect security
  - report issues
constraints:
  - do not provide vague feedback
  - every issue must include location and impact
```

它也可以工作，但复杂 Skill 很快会遇到问题：

- 长文本需要大量转义
- 多层逻辑不容易读
- 示例代码嵌在 YAML 中很难维护
- 条件、例外、解释会显得僵硬
- 修改提示词时可读性较差

因此 **Markdown 更适合表达"如何思考和执行"**。

---

## YAML 为什么适合工作流映射

工作流映射表通常要求系统**明确解析**：

- 匹配哪个意图
- 调用哪个 workflow
- 优先级是多少
- 版本是多少
- fallback 是什么
- 是否启用
- 传递哪些参数

例如：

```yaml
routes:
  - id: code-review
    priority: 90
    match:
      intent: code_review
    workflow: code-review-v2
    fallback: general-coding
```

这些字段必须：

- 名称固定
- 类型固定
- 可以校验
- 可以排序
- 可以由程序直接读取
- 出错时能够明确报错

这是 YAML 的优势。

---

## 本质区别

> [!note] 核心区分
> - **Markdown**：告诉 Agent **应该怎样做**
> - **YAML**：告诉系统 **应该调用什么**

或者更精确地说：

- **Skill Markdown = 行为规范和语义知识**
- **Workflow YAML = 执行配置和结构化数据**

两者并不矛盾。

---

## Skill 其实也不应该只有 Markdown

更成熟的 Skill 通常是 **"Markdown + 元数据"** 的组合：

```
skills/
└── code-review/
    ├── SKILL.md              # 给模型看：如何执行
    ├── manifest.yaml         # 给系统看：如何加载
    ├── input.schema.json     # 输入校验
    ├── output.schema.json    # 输出约束
    └── examples/             # 示例
```

### SKILL.md — 给模型看

```markdown
# Code Review

## Objective

检查代码正确性、安全性和可维护性。

## Procedure

1. 阅读需求和变更。
2. 优先寻找会导致错误的具体问题。
3. 按严重程度输出结果。
```

### manifest.yaml — 给系统看

```yaml
id: code-review
version: "2.1.0"
description: Review code for correctness and security

allowed_tools:
  - filesystem.read
  - repository.search

required_permissions:
  - repo.read

input_schema: input.schema.json
output_schema: output.schema.json

timeout_seconds: 600
max_retries: 2
```

### output.schema.json — 约束输出

```json
{
  "type": "object",
  "properties": {
    "issues": {
      "type": "array"
    },
    "summary": {
      "type": "string"
    }
  },
  "required": ["issues", "summary"]
}
```

这样职责最清楚：

| 文件 | 作用 |
|------|------|
| `SKILL.md` | 模型理解如何执行 |
| `manifest.yaml` | Runtime 理解如何加载和限制 |
| `schema.json` | 系统验证输入输出 |

---

## 为什么不建议把 Skill 全部写成 YAML

例如，一个复杂 Skill 需要表达：

> 当证据不足时，不要直接下结论；先指出缺少什么信息。如果可以通过已有工具获得信息，应先调用工具，而不是询问用户。

放在 Markdown 中很自然。如果强行结构化：

```yaml
rules:
  - condition:
      evidence: insufficient
      obtainable_with_tools: true
    action:
      call_tool: true
      ask_user: false
  - condition:
      evidence: insufficient
      obtainable_with_tools: false
    action:
      describe_missing_information: true
      ask_user: true
```

这种设计看起来更严格，但很快就会演变成**你自己发明一套 DSL**。随后你还需要解决：

- 条件表达式语法
- 优先级
- 规则冲突
- 嵌套逻辑
- 否定条件
- 模糊语义
- 版本兼容

> [!tip] 自然语言本来就是 LLM 擅长处理的部分
> 不需要把所有东西都结构化。应该**只结构化那些必须由程序确定性处理的部分**。

---

## 推荐的设计

采用以下分工：

```
rules/
└── routes.yaml                           # 工作流选择

workflows/
└── feature-development.yaml              # 状态、节点和转移

skills/
└── implementation/
    ├── SKILL.md                          # 描述 Skill 的执行方式
    ├── manifest.yaml                     # 运行约束
    └── output.schema.json                # 输出校验
```

### routes.yaml

```yaml
routes:
  - intent: feature_development
    workflow: feature-development
```

### feature-development.yaml

```yaml
initial_state: planning

states:
  planning:
    agent: planner
    transitions:
      success: implementation
      failure: failed
```

### 最终链路

```
Routes YAML
    ↓ 选择
Workflow YAML
    ↓ 编排
Skill Markdown
    ↓ 指导模型行为
Skill Manifest / Schema
    ↓ 约束运行和输出
```

---

## 一个简单判断原则

> [!question] 遇到一个内容时，问：
> **这个内容需要程序精确解析，还是需要模型理解语义？**

### 需要程序精确解析 → 使用 YAML 或 JSON

- ID
- 版本
- 超时
- 优先级
- 状态转移
- 工具权限
- 输入输出 Schema
- 重试次数

### 需要模型理解 → 使用 Markdown

- 任务目标
- 判断原则
- 执行方法
- 注意事项
- 异常情况
- 正反例
- 输出质量标准

---

## 为什么有的 Skills 有 manifest.yaml 有的没有

有没有 manifest.yaml 取决于**谁在加载 Skill**，而不是 Skill 本身。

### 第一类：OpenAI 官方 Skills（很多没有 manifest）

```
skills/
    code-review/
        SKILL.md
```

因为 ChatGPT 的 Runtime 已经知道如何加载 Skill：

- 文件夹名字就是 Skill ID
- `SKILL.md` 就是入口
- 不需要声明 version、author、timeout

> 这属于 **Convention over Configuration（约定优于配置）**。

### 第二类：Anthropic Claude Code Skills

Claude Code 官方很多 Skill 也是：

```
my-skill/
    SKILL.md
```

没有 manifest。因为 Claude Code Loader 也是固定的：

```
扫描 skill 目录 → 找到 SKILL.md → 读取 → 完成
```

它根本不用解析 `id`、`version`、`description`。

### 第三类：真正的 Plugin / Extension

如果 Skill 可以安装、升级、下载、上 Marketplace、多版本、权限控制——那几乎都会有 Manifest：

```
code-review/
    manifest.yaml
    SKILL.md
```

Manifest 可能长这样：

```yaml
id: code-review
version: 1.2.0
author: Chloe
description: Review code
entry: SKILL.md
permissions:
  - filesystem.read
requires:
  - git
timeout: 300
```

因为 Loader **不认识**你的 Skill，必须告诉它：

- 我是谁？
- 我在哪里？
- 我的版本是多少？
- 我的入口是什么？
- 我需要什么权限？

---

## 本质区别（加载 vs 执行）

> [!note]
> - **Markdown**：回答 **如何执行**
> - **Manifest**：回答 **如何加载**

这是两件完全不同的事情。

---

## 为什么很多 Agent Framework 后来都加了 Manifest

因为 Skill 数量越来越多：

```
skills/
    search/
    coding/
    planner/
    reviewer/
    researcher/
    sql/
    ui/
    deployment/
```

如果没有 Manifest，Runtime 只能：读整个目录 → 读所有 SKILL.md → 猜哪个能用，效率越来越差。

于是开始有：

```yaml
tags:
capabilities:
priority:
cost:
required_tools:
supported_models:
```

这样 Runtime 可以：

```
Query → 找 capability == coding → 直接加载
```

而不是把几十个 Markdown 全读一遍。

---

## 统一的组件设计

所有组件都可以有 `manifest.yaml`，只有执行逻辑不同：

```
components/
    workflows/
        feature/
            manifest.yaml
            workflow.yaml
    skills/
        coding/
            manifest.yaml
            SKILL.md
    subagents/
        researcher/
            manifest.yaml
            AGENT.md
    hooks/
        validate/
            manifest.yaml
            hook.py
```

这样整个 Runtime 会非常统一：

```
加载组件 → 读取 manifest → 根据 type → 加载对应入口
```

这是很多成熟 Agent 平台最终都会演化到的方向。

---

## 总结

| 维度 | Markdown | YAML/JSON |
|------|----------|-----------|
| 目标读者 | LLM / 模型 | Runtime / 系统 |
| 表达内容 | 行为规范、语义知识 | 确定性配置、结构化数据 |
| 适合场景 | 如何思考、如何执行 | 如何加载、如何路由 |
| 灵活性 | 高（自然语言） | 低（固定字段） |
| 可校验性 | 低 | 高 |
| 复杂度上限 | 无上限 | 需要避免引入 DSL |

> [!warning] 核心原则
> **只结构化那些必须由程序确定性处理的部分，其余交给自然语言。**
