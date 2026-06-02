---
title: "AI Agent 状态机工作流"
aliases:
  - "AI Agent State Machine"
  - "Agent 状态机"
  - "LangGraph 状态机"
tags:
  - AI/Agent
  - AI/Orchestration
  - AI/LangGraph
  - 概念/状态机
  - 实战/工程化
  - 进阶
created: 2026-06-02
updated: 2026-06-02
type: hybrid
subtypes:
  - concept
  - practice
sources_count: 25
status: published
difficulty: intermediate
related:
  - "[[AI-Agents]]"
  - "[[Agent智能体]]"
  - "[[SubAgent子代理]]"
  - "[[Skills 是什么]]"
  - "[[MCP协议]]"
  - "[[Harness-Engineering-系统治理工程]]"
  - "[[AI工程范式演进-Prompt到Harness]]"
  - "[[RAG技术入门指南]]"
---

# AI Agent 状态机工作流：用工程化结构把 Agent 拉回正轨

> [!info] 笔记定位
> 深度学习笔记 | 适用读者：有编程背景的开发者 / 应用 AI 工程师
> 范围：FSM 基础、Agent 范式对比、LangGraph 实战、防跑偏/持久化/可观测工程模式、选型决策
> 来源覆盖：25 篇文档（21 篇官方 + 2 篇博客 + 2 个演讲）

---

## Part A: 核心概念 (Core Concepts) #概念

### 1. 为什么需要状态机

> [!question] 为什么这节重要
> 搞清楚"agent 为什么跑偏"是设计正确工程结构的前提，否则后面所有模式都只是空中楼阁。

Agent 跑偏的根因是 **LLM 的本质属性** 与 **生产环境对可预测性、可审计性、可恢复性的要求** 之间存在结构性矛盾。Adam Terlson 在 AI Engineer 大会上精确地指出了这种对照——状态机擅长的所有特性（predictable / traceable / auditable / reliable / recoverable / declarative / low latency / testable）几乎就是 LLM 缺乏的所有特性 [来源: video-01.md]。

更深一层，Anthropic 的 "Building Effective Agents" 明确把系统分为两类：

- **Workflows**：通过**预定义代码路径**（predefined code paths）编排 LLM 调用
- **Agents**：让 LLM **动态**决定自己的行为和工具使用

关键洞察是：workflows 和 agents 的差别**不在于是否调用 LLM，而在于有没有显式的"脚手架"**。Workflows 是有边界的，LLM 在脚手架内被引导；Agents 把脚手架撤掉，LLM 自己决定下一步 [来源: doc-08.md, video-02.md]。

Lance Martin 在 LangChain 官方演讲中给出了一个实用经验："如果你**大致**知道工具调用的顺序，把它建模为 workflow 比放开给 agent 可靠性高得多" [来源: video-02.md]。这是工程上最重要的一条经验法则：先 workflow，不够再升级到 agent。

> [!tip] 实战要点
> 能写成 workflow 的不要写成 agent。Agent 适合开放式问题（步骤数无法先验确定），Workflow 适合定义清晰的任务。配合阅读 [[Harness-Engineering-系统治理工程]] 理解脚手架的工程意义。

---

### 2. FSM 基础

> [!question] 为什么这节重要
> 很多人用 LangGraph 但不知道它在底层就是 FSM + Actor Model。理解这一点能让你在选型、debug、调优时心里有底。

**有限状态机**（Finite State Machine, FSM）是一个五元组：状态（States）、事件（Events）、转移（Transitions）、守卫（Guards）、动作（Actions）[来源: video-01.md]。

| 元素 | 含义 | Agent 中的对应物 |
|------|------|------------------|
| States | 系统的离散模式 | 节点（如 `generate_joke`、`evaluate`）|
| Events | 触发转移的信号 | LLM 输出、工具返回结果、定时器 |
| Transitions | 状态间的有向边 | 静态边 / 条件边 |
| Guards | 转移前断言 | 条件边函数、状态守卫 |
| Actions | 转移时副作用 | 状态写入、日志、外部 API |

Terlson 还强调了一个常被忽略的扩展：**State Chart**。它比纯 FSM 多了层级状态（hierarchical）和并行状态（parallel），更接近真实应用。在演讲中他坦言严格意义上自己画的是 State Chart，但两个术语可以互换 [来源: video-01.md]。

下面是一个简单 FSM 的 Mermaid 视图：

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Generating: submit_topic
    Generating --> Evaluating: joke_produced
    Evaluating --> Generating: feedback("not funny")
    Evaluating --> Accepted: grade(pass)
    Accepted --> [*]
    Generating --> Failed: timeout
    Failed --> [*]
```

注意每个转移都可以附加一个 `guard` 条件（例如 `feedback not None`）和 `action`（例如 `append_log`）。LangGraph 的条件边 + Command 模式正好映射这两个概念。

> [!note] 小结
> FSM 不是新事物。把 FSM 思想引入 agent 工程，核心目的是把 LLM 的"黑盒推理"显式化、可视化、可恢复。

---

### 3. Agent 范式对比：FSM vs ReAct vs Plan-and-Execute

> [!question] 为什么这节重要
> 选错范式 = 后期无法收敛。先理解每个范式的边界条件。

Lilian Weng 把 agent 系统抽象为三个组件：Planning（规划）、Memory（记忆）、Tool Use（工具使用）[来源: doc-11.md]。基于这个框架，主流范式的取舍如下：

| 范式 | 控制流决定者 | 适合场景 | 缺点 |
|------|-------------|---------|------|
| **ReAct** | LLM 在循环内 "Thought → Action → Observation" | 步骤未知、开放式问题 | 无状态边界，循环次数无法精确控制 [来源: doc-11.md] |
| **Plan-and-Execute** | 一次性 plan，机械执行 | 子任务可预先枚举 | 计划失误时代价高 |
| **FSM / Workflow** | 显式节点 + 守卫 | 任务结构化、可靠性优先 | 灵活性低，状态爆炸风险 [来源: video-01.md] |

Terlson 用一个很精辟的对照表总结：

> "FSM 的优势恰恰是 LLM 的劣势，FSM 的劣势（灵活性低）恰好是 LLM 的优势。两者结合，让 FSM 弥补 LLM 的不可控，让 LLM 弥补 FSM 的死板" [来源: video-01.md]。

工程经验上有一个简单判别：

- **任务步骤数 ≤ 10 且能画流程图** → FSM
- **步骤数动态、需要 LLM 自主探索** → Plan-and-Execute
- **完全开放式、工具可能 20+** → ReAct + 严格 guardrails

> [!warning] 实战要点
> ReAct 简单但 unbounded，生产环境必须有兜底机制。FSM 复杂但 predictable，永远要知道 agent 当前"在哪一格"。

---

### 4. 主流实现

> [!question] 为什么这节重要
> 不要重新发明轮子。选型时理解每个框架的设计哲学能省下 3 个月试错。

| 框架 | 设计哲学 | 适用场景 | 关键差异 |
|------|----------|----------|----------|
| **LangGraph** | "低层编排基础设施"——不抽象 prompt，不抽象架构 [来源: doc-01.md] | 需要细粒度控制的生产 agent | 灵感来自 Pregel 和 Apache Beam，channel/node 模型 [来源: doc-12.md] |
| **CrewAI** | "Crew（团队）" + 角色化 Agent + 顺序/层级流程 [来源: doc-09.md] | 业务场景多 agent 协作 | 内置 memory、checkpoint、cache |
| **AutoGen** | Actor Model + 消息路由 `@message_handler` [来源: doc-10.md] | 分布式 actor 风格的复杂协作 | AgentChat 套件封装常见模式 |
| **自研 FSM（XState/自写）** | 纯 FSM + Actor | 嵌入式、低延迟、特定业务 | 完全可控，但工程量大 |

LangGraph 官方明确表态："LangGraph 是一个低层编排框架和运行时"，核心价值是"持久化、流式传输、部署"这三件事 [来源: doc-01.md, video-02.md]。其设计哲学有两条铁律：**最小化对 AI 未来的假设** 和 **"It should feel like code"** [来源: doc-12.md]。

CrewAI 的"团队"心智模型对业务人员更友好（YAML 配置 + 角色），而 LangGraph 对工程师更友好（显式图 + Python 函数）。Lyft 案例显示，CrewAI 的 hidden state 对调试不友好，所以他们最终选择 LangGraph [来源: doc-14.md]。

> [!tip] 实战要点
> LangGraph = 工程深度，CrewAI = 上手速度，AutoGen = 分布式 actor。需要"既能工作又能 debug"，首选 LangGraph。

---

### 5. 状态机核心机制

> [!question] 为什么这节重要
> 这节是 LangGraph 的"ABC"。读懂这里，后面所有模式都只是这五个概念的组合。

LangGraph 把 FSM 的五个元素对应到以下 API [来源: doc-01.md, doc-07.md, doc-20.md]：

| FSM 元素 | LangGraph 概念 | API |
|----------|----------------|-----|
| States | **State**（schema + reducers）| `TypedDict` + `Annotated` reducer |
| Nodes | **Node**（执行单元）| `builder.add_node("name", fn)` |
| Edges (static) | **Edge**（静态转移）| `builder.add_edge(start, end)` |
| Edges (dynamic) | **Conditional Edge** | `builder.add_conditional_edges(src, routing_fn, mapping)` |
| Actions | **Command**（状态+控制流原子）| `return Command(update=..., goto=...)` |
| Guards | 条件边函数 / `interrupt()` | `routing_fn(state) -> Literal[...]` |

**State** 是带类型的容器，每个键都有 reducer——默认覆盖，自定义可累加（如 `Annotated[list, operator.add]` 用于消息累积）[来源: doc-07.md]。

**Command** 是 LangGraph 的"杀手锏"——它把"更新状态"和"决定下一步"合并成一个原子操作：

```python
from langgraph.types import Command
def my_node(state) -> Command[Literal["next_node", "__end__"]]:
    return Command(
        update={"key": "value"},  # 状态更新
        goto="next_node",          # 路由
    )
```

**Send** 用于动态 fan-out（map-reduce），适合 orchestrator-worker 等模式 [来源: doc-20.md]。

**Conditional Edge** 的核心是 routing 函数：接收当前 state，返回目标节点名（字符串）或 `Send` 对象。多个目标会**并行执行**在同一个 super-step 中 [来源: doc-07.md]。

> [!note] 小结
> State 是数据，Node 是函数，Edge 是控制流，Command 是"动作+转移"原子，Send 是动态 fan-out。记住这五个词就够了。

---

## Part B: 实战示例 (Practical Examples) #实战

### 6. 基础工作流模式

> [!question] 为什么这节重要
> Lance Martin 的视频用 LangGraph 把 Anthropic 博客里的 5 个模式从零实现了一遍 [来源: video-02.md]。这一节是整个笔记最浓缩的精华。

**1. Prompt Chaining（提示链）**——每一步 LLM 处理上一步输出

适用：可分解为固定步数的任务。例：笑话生成 → 检查有 punchline → 改进 → 润色 [来源: video-02.md, doc-13.md]。

**2. Parallelization（并行化）**——多个 LLM 同时跑

适用：sub-questioning（如 multi-query RAG）、不同视角、voting（多次执行投票）。Sectioning（独立子任务）和 voting（同一任务多次执行）两种变体 [来源: doc-08.md, video-02.md]。

**3. Routing（路由）**——LLM 分类器决定走哪条路

适用：意图分类（价格查询 vs 退款 vs 投诉）。结构化输出 + 条件边是最常见实现 [来源: video-02.md]。

**4. Orchestrator-Worker（编排者-工人）**——LLM 动态分解任务并分派

适用：报告生成（sections 数量未知）、deep research。LangGraph 用 `Send` API 实现动态 worker 创建 [来源: video-02.md, doc-13.md]。

**5. Evaluator-Optimizer（评估-优化）**——生成 + 评估循环

适用：RAG 幻觉检测、代码改写直到通过测试。常用 structured output 让 evaluator 输出 `grade` + `feedback` [来源: video-02.md]。

这五个模式**不是平行的**，而是**递进的复杂性阶梯**。从 chaining 起步，复杂问题用 evaluator-optimizer [来源: video-02.md]。

> [!tip] 实战要点
> 选模式前先问"步骤数我能先验确定吗？"能 → chaining；能并行 → parallelization；分支多 → routing；分支数动态 → orchestrator-worker；需要质量迭代 → evaluator-optimizer。

---

### 7. 完整 LangGraph 代码示例

> [!question] 为什么这节重要
> 概念看再多不如跑一遍。下面三个代码块覆盖了核心模式、Send API、evaluator loop——每一个都是生产可用的脚手架。

#### 示例 1：基础 StateGraph + 条件边

```python
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

# 1. 定义 State（带 reducer 的 TypedDict）
class JokeState(TypedDict):
    topic: str
    joke: str
    grade: Literal["funny", "not_funny", "unknown"]

# 2. 定义结构化输出
class Grade(BaseModel):
    score: Literal["funny", "not_funny"]
    feedback: str

# 3. 节点函数
llm = ChatOpenAI(model="gpt-4o")
llm_with_struct = llm.with_structured_output(Grade)

def generate_joke(state: JokeState) -> dict:
    """生成笑话节点"""
    prompt = f"写一个关于{state['topic']}的笑话"
    resp = llm.invoke(prompt)
    return {"joke": resp.content}

def evaluate_joke(state: JokeState) -> dict:
    """评估笑话节点"""
    grade = llm_with_struct.invoke(f"评估这个笑话是否有趣: {state['joke']}")
    return {"grade": grade.score}

# 4. 路由函数（守卫）
def route_after_grade(state: JokeState) -> Literal["accepted", "regenerate"]:
    return "accepted" if state["grade"] == "funny" else "regenerate"

# 5. 构建图
builder = StateGraph(JokeState)
builder.add_node("generate", generate_joke)
builder.add_node("evaluate", evaluate_joke)
builder.add_edge(START, "generate")
builder.add_edge("generate", "evaluate")
builder.add_conditional_edges("evaluate", route_after_grade, {
    "accepted": END,
    "regenerate": "generate",  # 循环回去
})
graph = builder.compile(checkpointer=MemorySaver())

# 6. 首次运行
config = {"configurable": {"thread_id": "1"}}
result = graph.invoke({"topic": "程序员", "joke": "", "grade": "unknown"}, config)
print(result["joke"])
```

#### 示例 2：Orchestrator-Worker（Send API）

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
import operator

class ReportState(TypedDict):
    topic: str
    sections: list[str]                         # 编排者生成
    completed_sections: Annotated[list[str], operator.add]  # worker 并行写入
    final_report: str

class WorkerState(TypedDict):
    section: str

def orchestrator(state: ReportState) -> dict:
    """用 LLM 决定要写哪些章节"""
    sections = llm.invoke(f"列出关于{state['topic']}报告的 3-5 个章节名").content
    return {"sections": [s.strip() for s in sections.split("\n") if s.strip()]}

def worker(state: WorkerState) -> dict:
    """每个 worker 写一个章节"""
    content = llm.invoke(f"写章节: {state['section']}").content
    return {"completed_sections": [f"## {state['section']}\n{content}"]}

def synthesizer(state: ReportState) -> dict:
    return {"final_report": "\n\n".join(state["completed_sections"])}

def fan_out_workers(state: ReportState):
    """动态 fan-out：每个 section 启动一个 worker"""
    return [Send("worker", {"section": s}) for s in state["sections"]]

builder = StateGraph(ReportState)
builder.add_node("orchestrator", orchestrator)
builder.add_node("worker", worker)
builder.add_node("synthesizer", synthesizer)
builder.add_edge(START, "orchestrator")
builder.add_conditional_edges("orchestrator", fan_out_workers, ["worker"])
builder.add_edge("worker", "synthesizer")
builder.add_edge("synthesizer", END)
graph = builder.compile()
print(graph.invoke({"topic": "LangGraph", "sections": [], "completed_sections": [], "final_report": ""})["final_report"])
```

> [!warning] 实战要点
> worker 返回的 `completed_sections` 用了 `operator.add` reducer，否则并行写入会互相覆盖 [来源: video-02.md]。

#### 示例 3：Evaluator-Optimizer Loop

```python
class LoopState(TypedDict):
    topic: str
    answer: str
    critique: str
    iteration: int

def generate(state: LoopState) -> dict:
    feedback = state.get("critique", "")
    prompt = f"回答: {state['topic']}"
    if feedback:
        prompt = f"基于反馈改写: {state['answer']}\n反馈: {feedback}"
    answer = llm.invoke(prompt).content
    return {"answer": answer, "iteration": state.get("iteration", 0) + 1}

def evaluate(state: LoopState) -> dict:
    grade = llm_with_struct.invoke(f"评估: {state['answer']}")
    if grade.score == "good":
        return {"critique": ""}
    return {"critique": grade.feedback}

def should_continue(state: LoopState) -> Literal["end", "improve"]:
    if state.get("iteration", 0) >= 3 or not state.get("critique"):
        return "end"
    return "improve"

builder = StateGraph(LoopState)
builder.add_node("generate", generate)
builder.add_node("evaluate", evaluate)
builder.add_edge(START, "generate")
builder.add_edge("generate", "evaluate")
builder.add_conditional_edges("evaluate", should_continue, {"end": END, "improve": "generate"})
graph = builder.compile()
```

> [!note] 小结
> 三个示例展示了从单步（示例 1）到并行 fan-out（示例 2）到反馈循环（示例 3）的演进。生产中你可能要把它们嵌套组合。

---

### 8. 多 Agent 协作：Subgraphs

> [!question] 为什么这节重要
> 复杂业务几乎一定要拆成多个子图。理解父子图通信模式是构建可维护系统的关键。

LangGraph 用 **subgraph**（子图）做模块化：子图本身是一个完整的 `Pregel` 实例，可以作为另一个图的节点。两种通信模式 [来源: doc-17.md]：

**模式 A：State Schema 不同（隔离模式）**

适合子图有自己独立的领域状态。父图通过 wrapper 函数做状态转换：

```python
def call_subgraph(state: ParentState) -> dict:
    """手动转换：父状态 → 子图输入 → 子图输出 → 父状态"""
    sub_out = subgraph.invoke({"internal_key": state["public_key"]})
    return {"public_key": sub_out["result_key"]}

builder.add_node("wrapper", call_subgraph)
```

**模式 B：State Schema 共享（透传模式）**

父图和子图有重叠键（如都读 `messages`），直接把编译好的子图作为节点：

```python
builder.add_node("research_agent", research_subgraph)  # 直接传 compiled 图
```

**Subgraph 的持久化模式**决定了子图的状态保留行为 [来源: doc-17.md]：

| 模式 | `checkpointer=` | 行为 |
|------|-----------------|------|
| Per-invocation（默认）| `None` | 每次调用都新状态，interrupts 仍支持 |
| Per-thread | `True` | 同 thread 内累积记忆 |
| Stateless | `False` | 完全无状态，interrupts 不支持 |

Lyft 的生产案例展示了生产级 subgraph 模式：每个 subagent 有统一的"前置 safety check → LLM reasoning → 工具调用"节点模板；agent 间 handoff 用 `Command(goto=..., graph=Command.PARENT)` 回到 meta agent 重新路由 [来源: doc-14.md]。

下面用 Mermaid 展示 Lyft 风格的 multi-agent 架构：

```mermaid
flowchart TD
    User([用户]) --> Meta[Meta Agent<br/>意图分类]
    Meta -->|rider| RiderRouter{Rider Router}
    Meta -->|driver| DriverRouter{Driver Router}
    RiderRouter -->|lost_items| Sub1[Sub-agent A<br/>失物]
    RiderRouter -->|refund| Sub2[Sub-agent B<br/>退款]
    DriverRouter -->|earnings| Sub3[Sub-agent C<br/>收益]
    DriverRouter -->|dispute| Sub4[Sub-agent D<br/>争议]
    Sub1 --> Safety[Safety Check<br/>并行 fan-out]
    Sub2 --> Safety
    Sub3 --> Safety
    Sub4 --> Safety
    Safety --> Meta
```

> [!tip] 实战要点
> 能复用就拆 subgraph；subgraph 的 checkpointer 选 `None`（默认）还是 `True` 取决于是否需要跨调用记忆。配合 [[SubAgent子代理]] 阅读理解多智能体模式。

---

## Part C: 三大工程实战板块 #工程

### 9. 防跑偏机制

> [!question] 为什么这节重要
> 这是本笔记用户最关心的部分。Terlson 演讲的核心论点是：状态机为 agent 提供 predictability / traceability / recoverability [来源: video-01.md]。

防跑偏 = 多层防御。每一层解决不同类型的"跑偏"。

**Layer 1：递归限制（Recursion Limit）**

LangGraph 默认 recursion_limit=25 步（在 graph API 中可配），超过会抛 `GraphRecursionError` [来源: doc-20.md]。这是兜底——正常设计不应触发。

**Layer 2：RemainingSteps 主动感知**

```python
from langgraph.managed.shared import RemainingSteps
def fallback_node(state):
    """当 RemainingSteps 接近 0 时主动降级"""
    if state["remaining_steps"] < 3:
        return {"status": "fallback_summary"}
    # 正常逻辑
```

`RemainingSteps` 是 managed value，让节点能"看到"自己还有多少步预算 [来源: doc-20.md]。

**Layer 3：状态守卫（State Guard）**

条件边本身就是守卫。更严格的做法是给每个 state key 加校验函数：

```python
def validate_state(state) -> bool:
    """每次 state 更新前调用"""
    if len(state.get("messages", [])) > 50:
        return False  # 拒绝更新
    return True
```

**Layer 4：HITL（Human-in-the-Loop）**

`interrupt()` 可以在任何节点暂停，等待人类批准 [来源: doc-03.md]：

```python
from langgraph.types import interrupt, Command

def sensitive_tool_node(state) -> Command:
    # 暂停并请求人工审批
    approved = interrupt({
        "question": "是否执行 send_email?",
        "details": state["pending_action"],
    })
    if approved:
        return Command(goto="execute_email")
    return Command(goto="cancel_path")

# 用户在前端审查后恢复
graph.invoke(Command(resume=True), config=config)
```

**Layer 5：约束 prompt**

Lyft 案例的最重要教训：**最难的不是基础设施，而是 prompt 质量** [来源: doc-14.md]。他们的解决方案是结构化 prompt 模板（5 部分：身份 / 目标 / 范围 / 阶段工作流 / 内容指南）+ Git CI（静态检查 + LLM 检查，违规阻断 merge）。核心原则："Treat prompts like product specs, not code comments"。

**Layer 6：超时回滚**

`@task` 函数天然支持超时（用 `asyncio.wait_for` 包装）。超时时状态保留到上一个 checkpoint，可重试或人工介入 [来源: doc-05.md]。

下面用 Mermaid 展示一个完整的防跑偏栈：

```mermaid
sequenceDiagram
    participant U as User
    participant G as Graph
    participant L as LLM Node
    participant T as Tool Node
    participant H as Human

    U->>G: invoke()
    G->>L: 节点执行
    L-->>G: 输出
    alt 敏感操作
        G->>H: interrupt(批准?)
        H-->>G: Command(resume=True/False)
    end
    G->>T: 调用工具
    T-->>G: 结果
    G-->>U: 状态
    Note over G: RemainingSteps < 3 → 触发 fallback
    Note over G: 步数 > recursion_limit → 抛错
```

> [!warning] 实战要点
> 单层防御不够。生产级 agent 至少要 recursion_limit + 关键节点 interrupt + prompt CI 三件套。

---

### 10. 持久化与错误恢复

> [!question] 为什么这节重要
> LLM 调用是 flaky 的（超时、限流、幻觉），agent 又可能是长时任务（小时级）。没有持久化层，任何失败都是从头开始。

LangGraph 的持久化层在每个 **super-step**（执行 tick）保存 state 作为 checkpoint [来源: doc-02.md]。

**核心数据结构**：
- **Thread**：`thread_id` 是主键，累积一个 sequence of runs 的 state
- **Checkpoint**：`StateSnapshot` 包含 values / next / config / metadata / parent_config
- **Store**：跨 thread 共享的长期记忆（与 checkpointer 独立）

**三种 Durability 模式**（持久化时机）[来源: doc-02.md]：

| 模式 | 行为 | 适用 |
|------|------|------|
| `"exit"` | 仅完成/interrupt 时持久化 | 性能优先，损失小 |
| `"async"` | 异步持久化 | 平衡，主流默认 |
| `"sync"` | 同步持久化 | 强一致，慢 |

**Checkpointer 后端** [来源: doc-16.md]：

| 库 | 用途 |
|----|------|
| `langgraph-checkpoint` | 抽象 + `InMemorySaver` |
| `langgraph-checkpoint-sqlite` | 本地开发 |
| `langgraph-checkpoint-postgres` | 生产（已优化） |
| 自定义（Lyft 的 `DynamoDBSaver`）| 对接公司基础设施 [来源: doc-14.md] |

**Time Travel**：基于 checkpoint 历史的两种操作 [来源: doc-19.md]：
- **Replay**：从某 checkpoint 重新执行（不是从缓存读）
- **Fork**：在 checkpoint 上 `update_state()` 创建新分支，不影响原 thread

下面是一个带持久化 + 断点续跑的完整示例：

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from typing import TypedDict

class LongTaskState(TypedDict):
    step: int
    results: list[str]
    status: str  # "running", "failed", "completed"

def step_node(state: LongTaskState) -> dict:
    """可能失败的节点"""
    try:
        result = f"step_{state['step']}_done"
        return {"step": state["step"] + 1, "results": [result]}
    except Exception as e:
        return {"status": "failed", "results": [f"error: {e}"]}

def should_continue(state: LongTaskState) -> str:
    if state.get("status") == "failed":
        return "end"
    if state["step"] >= 5:
        return "end"
    return "continue"

builder = StateGraph(LongTaskState)
builder.add_node("step", step_node)
builder.add_edge(START, "step")
builder.add_conditional_edges("step", should_continue, {"continue": "step", "end": END})
graph = builder.compile()

# 1. 启动 Postgres checkpointer
DB_URI = "postgresql://user:pass@localhost/langgraph"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    graph = builder.compile(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": "long_task_001"}}

    # 2. 第一次运行（可能中途失败）
    try:
        graph.invoke({"step": 0, "results": [], "status": "running"}, config)
    except Exception:
        pass

    # 3. 恢复（从上次 checkpoint 继续）
    state = graph.get_state(config)
    print(f"已执行到 step {state.values['step']}, 恢复...")
    graph.invoke(None, config)  # None = 从当前 state 继续

    # 4. 查看历史
    for snapshot in graph.get_state_history(config):
        print(f"checkpoint {snapshot.config['configurable']['checkpoint_id']}: step {snapshot.values['step']}")

    # 5. Fork：从历史中某个 checkpoint 分叉
    history = list(graph.get_state_history(config))
    past = history[-2]  # 倒数第二个
    new_config = graph.update_state(past.config, {"step": 0})  # 重置
    graph.invoke(None, new_config)  # 在新分支重跑
```

> [!danger] 实战要点
> 永远不要用 `InMemorySaver` 跑生产。它是测试用的。Postgres 是默认选择。云上想脱 Postgres 可以用 Lyft 的 `DynamoDBSaver` 模式自己实现 `BaseCheckpointSaver` 接口。

---

### 11. 可观测与调试

> [!question] 为什么这节重要
> 生产 agent 失败时，**没有 trace = 没有调试**。LLM 调用链长、并行、条件分支，缺少 trace 几乎无法定位问题。

LangGraph 与 LangSmith 深度集成。LangSmith 的核心价值：可视化执行 trace + 监控 + 评估 [来源: doc-06.md, doc-15.md]。

> [!info] 术语对照
> 可观测（Observability）= 在生产环境中**追踪、测量、理解**系统内部状态的能力，包含 trace / metrics / logs 三大支柱。

**启用追踪**（最小化配置）：

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=lsv2_xxx
export LANGSMITH_PROJECT=my-agent  # 自定义项目
```

**附加元数据**（用于过滤、监控）：

```python
config = {
    "configurable": {"thread_id": "user_123"},
    "metadata": {
        "user_type": "premium",
        "environment": "prod",
        "agent_version": "v2.3",
    },
    "tags": ["customer_support", "refund_flow"],
}
graph.invoke(input, config=config)
```

Lyft 在生产环境附加：user_type、agent_name、intent、conversation_id。然后用这些字段做监控仪表盘和告警 [来源: doc-14.md]。

**数据脱敏（Anonymizer）**：

```python
from langsmith.anonymizer import create_anonymizer
import re

# 创建脱敏器：匹配 SSN 模式
anonymizer = create_anonymizer([
    (re.compile(r"\d{3}-\d{2}-\d{4}"), "[REDACTED_SSN]"),
])

# 在 trace 上应用
with ls.tracing_context(enabled=True, anonymizer=anonymizer):
    graph.invoke(input, config)  # trace 中的 SSN 会被脱敏
```

**状态可视化**：LangGraph 的 `get_graph().draw_mermaid_png()` 能直接生成 Mermaid 图（生产中可以集成到 CI）[来源: doc-13.md]。

**测试模式**（Pytest）[来源: doc-21.md]：

```python
import pytest
from langgraph.checkpoint.memory import MemorySaver

@pytest.fixture
def graph():
    """每个 test 独立的 checkpointer，避免状态污染"""
    saver = MemorySaver()
    return builder.compile(checkpointer=saver)

def test_node_in_isolation(graph):
    """直接测单个节点"""
    state_in = {"topic": "AI", "joke": "", "grade": "unknown"}
    result = graph.nodes["generate"].invoke(state_in)
    assert "joke" in result

def test_partial_execution(graph):
    """测从某个节点恢复"""
    config = {"configurable": {"thread_id": "test_partial"}}
    # 先跑到 evaluate 节点
    graph.invoke({"topic": "AI", ...}, config)
    # 模拟从 evaluate 节点恢复并断言路由
    graph.update_state(config, {"grade": "funny"}, as_node="evaluate")
    state = graph.get_state(config)
    assert state.next == ()  # 已到 END
```

下面用 Mermaid 时序图展示一个生产环境的可观测流：

```mermaid
sequenceDiagram
    participant App as Application
    participant G as Graph
    participant LS as LangSmith
    participant DB as Postgres

    App->>G: invoke(input, config)
    G->>G: 执行 super-step
    G->>LS: 上报 trace (节点输入/输出/token/latency)
    G->>DB: checkpoint 持久化
    Note over LS: 脱敏器过滤敏感数据
    LS-->>App: 仪表盘 + 告警<br/>(PagerDuty: 错误率>5% 触发)
    App->>G: get_state_history(config)
    G-->>App: 完整执行历史（用于 time travel / fork）
```

> [!tip] 实战要点
> trace + 监控告警 + 测试，三件套缺一不可。Lyft 的 PagerDuty 告警阈值：错误率 >5% 或 p95 latency >10 秒持续 15 分钟 [来源: doc-14.md]。

---

## Part D: 选型速查 (Decision Framework) #速查

### 12. 框架对比表

| 特性 | LangGraph | CrewAI | AutoGen | 自研 FSM |
|------|-----------|--------|---------|----------|
| 抽象层级 | 低（不抽象 prompt）[来源: doc-01.md] | 高（YAML 配置）| 中（消息路由）| N/A |
| 状态可见性 | 显式 state schema | 内部 memory class | message history | 完全可控 |
| Checkpointing | 多后端（Postgres/SQLite/自写）[来源: doc-16.md] | 内置（`checkpoint=True`）[来源: doc-09.md] | 需自接 | 需自接 |
| HITL | `interrupt()` + Command[来源: doc-03.md] | 回调钩子 | 需自写 | 完全可控 |
| 持久化粒度 | 每 super-step | task 完成时 | 无内置 | 自定义 |
| Time travel | Replay + Fork[来源: doc-19.md] | 无 | 无 | 自实现 |
| 多 agent 模式 | Subgraphs（父子图）[来源: doc-17.md] | Crew 协作 | Actor Model | 自定义 |
| 学习曲线 | 中（FSM 基础）| 低（YAML 友好）| 中（actor 思维）| 高 |
| 生产案例 | Klarna, Replit, Elastic, Lyft[来源: doc-23.md, doc-14.md] | 业务场景多 | 微软生态 | 嵌入式 |

---

### 13. 决策树

```mermaid
flowchart TD
    Q1{任务步骤能先验画图吗?}
    Q1 -->|是| Q2{需要状态持久化?}
    Q1 -->|否| Q3{工具数?}
    Q2 -->|是| LG[LangGraph<br/>首选]
    Q2 -->|业务人员配置| CA[CrewAI]
    Q2 -->|嵌入式/极致性能| SELF[自研 FSM<br/>XState]
    Q3 -->|< 10| LG2[LangGraph + ReAct 模板]
    Q3 -->|> 10| LG3[LangGraph + 严格 routing]
    Q3 -->|分布式 actor| AG[AutoGen]

    MUST[生产必备]
    MUST --> M1[必须有 checkpointer]
    MUST --> M2[风险操作必须有 interrupt]
    MUST --> M3[必须接 LangSmith 监控]
```

---

### 14. 常见坑点与最佳实践

| 坑点 | 表现 | 修复 |
|------|------|------|
| **Recursion limit 触发** | 任务跑到一半抛 `GraphRecursionError` | 用 `RemainingSteps` 提前 fallback；或调大 limit（治标）|
| **InMemorySaver 用在生产** | 重启后状态全丢 | 换 PostgresSaver 或自实现 `BaseCheckpointSaver` |
| **Side effect 写在 interrupt 前** | 重试时副作用重复执行 | 把副作用放进 `@task` 函数，或确保 idempotent [来源: doc-05.md] |
| **interrupt 包了 try/except** | 异常被吞，pause 失效 | 永远不要包 `interrupt()`，让异常正常传播 [来源: doc-03.md] |
| **interrupt 顺序不一致** | resume 时路由错乱 | 同一节点的所有 `interrupt()` 调用顺序必须稳定 [来源: doc-03.md] |
| **Send API 缺 reducer** | 并行 worker 写入互相覆盖 | 共享 key 用 `Annotated[list, operator.add]` [来源: video-02.md] |
| **Subgraph 状态泄漏** | 父图能看到子图内部 key | 用模式 A（独立 schema + wrapper）做隔离 [来源: doc-17.md] |
| **Prompt 漂浮** | behavior 不可控、跨人改冲突 | 借鉴 Lyft：5 部分结构化 prompt + Git CI [来源: doc-14.md] |
| **没设脱敏** | trace 泄露 PII | 用 `create_anonymizer()` [来源: doc-06.md] |
| **Pydantic 默认值冲突** | state reducer 默默覆盖 | 显式用 `Annotated[list, add]` 标注累积字段 [来源: doc-07.md] |

> [!warning] 实战要点
> 上面 10 个坑在 Lyft、Anthropic、LangChain 官方都明确点过。**生产前先把这个清单过一遍**。

---

### 15. 未来趋势

> [!question] 为什么这节重要
> Terlson 在 2025 年 AI Engineer 大会上描绘了一个清晰的前进方向 [来源: video-01.md]。理解趋势能帮你选对长期生态。

**趋势 1：AI-Authored State Machines（Chartering）**

Terlson 自创术语 **Chartering**——把整个 state chart 交给 LLM，让它"发明"流程。例如给一篇 Privacy Rights 的退订文章让 o1 生成退订流程的 state chart，零样本就做出可用结果 [来源: video-01.md]。

**趋势 2：State Chart + Actor + LLM 三件套**

Terlson 的核心论点：未来 agent 系统的"乐高积木"是 **FSM（结构） + Actor（通信） + LLM（智能）**。三者结合，FSM 补 LLM 的不可控，LLM 补 FSM 的死板，Actor 补分布式并发 [来源: video-01.md]。

**趋势 3：可视化作为一等公民**

State chart 70 年的视觉语言 + LLM 视觉理解能力 = "Visualization Agent" 给 Chartering Agent 反馈 [来源: video-01.md]。

**趋势 4：低层框架胜出**

LangGraph 团队明确表态："the biggest competitor to any framework is no framework" [来源: doc-12.md]。因此 LangGraph 选择**不抽象**——把基础设施（持久化/流式/部署）做好，让用户写"几乎就是 Python"的代码。这意味着未来几年 LangGraph 类低层框架比 CrewAI 类高层框架更有可能存活。

> [!tip] 实战要点
> 短期学 LangGraph，中期关注 Chartering，长期用低层基础设施 + 多个高层 SDK（Deep Agents、CrewAI）组合。配合 [[AI工程范式演进-Prompt到Harness]] 理解范式迁移。

---

## 思考题

> [!question] 思考题 1 - 概念理解
> 为什么说"workflow 是脚手架，agent 把脚手架撤掉"？试举例：同一个客服任务，写成 workflow 和 agent 在可预测性、灵活性上各有什么代价？

> [!question] 思考题 2 - 应用场景
> 你的团队要做一个"长篇研报自动生成"agent，应该选 LangGraph 的哪个模式（chaining / parallelization / orchestrator-worker / evaluator-optimizer）？为什么？如果要加入"质量不达标重写"的兜底，应该怎么改？

> [!question] 思考题 3 - 边界情况思考
> 当 `recursion_limit=25` 真的触发了，应该如何**优雅降级**？是把已完成的中间结果回给用户，还是抛错让人介入？两种策略各适合什么业务？

> [!question] 思考题 4 - 工程取舍
> HITL 的 `interrupt()` 加在哪里最有效？太少 → 风险大；太多 → 体验差。你会用什么原则决定"哪些节点必须人工审批"？

> [!question] 思考题 5 - 架构决策
> 为什么 Lyft 选择 LangGraph 而不是 CrewAI？他们的核心考量（prompt 质量、debug 友好、状态可见）对你的项目选型有什么启示？

---

## 参考资料索引

按引用频次排序的核心来源：

- 官方文档：LangGraph Overview (doc-01)、Graph API (doc-07)、Persistence (doc-02)、Interrupts (doc-03)、Subgraphs (doc-17)、Time Travel (doc-19)、Testing (doc-21)、Workflows & Agents (doc-13)、State Machine Patterns (doc-20)
- 设计哲学：Anthropic "Building Effective Agents" (doc-08)、Building LangGraph (doc-12)
- 实战案例：Lyft Customer Support Platform (doc-14)
- 视频：Lance Martin "Building Effective Agents with LangGraph" (video-02)、Adam Terlson "Multi-agent Systems with FSM" (video-01)
- 框架对比：CrewAI Crews (doc-09)、AutoGen (doc-10)、Lilian Weng Agent Patterns (doc-11)

## 相关笔记

- [[AI-Agents]] - AI Agent 总览
- [[Agent智能体]] - Agent 基础概念
- [[SubAgent子代理]] - 多代理模式
- [[Skills 是什么]] - Skills 编排
- [[MCP协议]] - Agent 基础设施
- [[Harness-Engineering-系统治理工程]] - 系统治理工程
- [[AI工程范式演进-Prompt到Harness]] - 范式演进
- [[RAG技术入门指南]] - RAG 应用
