---
type: experience
topic: "Agent与Skills架构设计"
tags: [Agent, Skills, Claude-Code, 架构设计]
created: 2026-05-12
updated:
project: ""
---

# Agent与Skills架构设计

## 背景

在使用 Claude Code 构建自动化工作流时，遇到了一个典型的架构设计问题：**当一个 Skill 和一个 Subagent 实现了相同的功能时，它们之间是层级调用关系还是权限争夺关系？**

这个问题源于实际工作流中的经验教训，而非外部研究。

## 过程

### 情况一：糟糕的设计——争夺使用权（路由冲突）

如果主干流程（Claude Code）同时能看到这个 Skill 和这个 Subagent，且它们的描述高度重合，就会发生"打架"现象。

**问题根源**：`[待验证]` 当面对两个都能完成任务的选项时，大模型的选择行为缺乏官方文档明确说明。根据社区经验观察，可能出现：
- 倾向选择列表中靠前的工具（"顺序偏好"而非真正的"随机"）
- 反复横跳，试图同时使用两个工具
- 甚至触发幻觉，凭空捏造一个不存在的调用路径

**具体表现**：
- 想让 Skill 快速执行确定性任务，却唤醒了啰嗦的 Subagent，导致时间翻倍
- Subagent 被唤醒后，不知道该自己动手还是指挥 Skill 干活

### 情况二：理想的设计——层级调用（Agent 调用 Skill）

正确的设计模式是：**将 Skill 从主流程的视线中隐藏，只将其作为"专属武器"暴露给 Subagent**。

**运作方式**：
1. 主流程只知道 Subagent 的存在
2. 任务下达时，主流程唤醒 Subagent
3. Subagent 负责复杂推理和规划
4. 当需要执行具体动作时，由 Subagent 调用对应的 Skill

> 打个比方：Skill 是一把"电钻"，Subagent 是"装修工人"。主流程（老板）不应该同时对着电钻和工人下指令。老板只需把任务交给工人，工人自己知道什么时候该拿起电钻。

### 层级调用的实现方式

**核心语法**：在 Subagent 的 prompt 中声明 Skill 调用权限：

```markdown
## 可用工具
- 你可以调用 `write_log` 技能记录结论：`Skill({skill: "write_log"})`
- 你可以调用 `beautify` 技能进行排版：`Skill({skill: "beautify"})`
```

**层级角色分工**：

| 层级 | 角色 | 可见范围 |
|------|------|----------|
| 主流程 | 指挥者 | 只知道 Subagent，不知道底层 Skill |
| Subagent | 规划者 | 既知道任务目标，也知道何时调用哪个 Skill |
| Skill | 执行者 | 被动等待 Subagent 调用，执行确定性任务 |

**关键原则**：
1. **主流程隐藏 Skill**：从主流程的 `CLAUDE.md` 中移除 Skill 的暴露
2. **Subagent 声明依赖**：在 Subagent 的 description 或 prompt 中写明可用的 Skill
3. **单向调用**：Subagent → Skill，而不是主流程 → Subagent + Skill

## 心得

### 果断取舍是核心原则

出现"功能完全相同的 Skill 和 Subagent"通常是架构冗余，**必须二选一**。

### 保留 Skill 的场景

任务是**确定性的**，例如：
- 单纯抓取网页
- 处理 Markdown 排版
- 写入本地文件

这些任务不需要"自由意志"和反复思考，直接调用脚本最快最稳。Subagent 介入纯属大材小用，只会徒增延迟。

### 保留 Subagent 的场景

任务需要**推理和容错**，例如：
- 抓取资料后发现缺漏，自动换关键词重新搜索
- 自我复盘评估

将 Skill 的调用入口从主流程删除，只写进 Subagent 的系统提示词。

## 踩坑

> [!warning] 坑点
> **现象**：主流程同时暴露 Skill 和 Subagent，导致任务执行时随机选择工具
> **原因**：`[待验证]` 两个工具对主模型可见且功能描述重合，选择行为不可预测（可能顺序偏好而非随机）
> **解决**：明确职责分工——Subagent 规划决策，Skill 执行具体操作，通过 prompt 声明隐藏关系

## 代码/示例

```markdown
# 错误写法（主流程 CLAUDE.md）
## 可用工具
- `collect`：收集资料
- `curate`：整理资料
- `my-agent`：执行复杂任务的代理

# 正确写法（主流程 CLAUDE.md）
## 可用工具
- `my-agent`：执行复杂任务的代理（它内部会调用 collect、curate 等技能）

# Subagent 的 prompt
## 可用工具
- `collect`：`Skill({skill: "collect"})` 收集学习资料
- `curate`：`Skill({skill: "curate"})` 整理资料
```

## 延伸

- 还需深入了解：实际工作流中 Subagent 与 Skill 的性能对比数据
- 下一步计划：在实际项目中验证层级调用模式的延迟和稳定性
- 相关笔记：[[Claude-Code-工作流设计]]

---

> [来源: 个人经验]
