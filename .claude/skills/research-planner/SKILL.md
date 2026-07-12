---
name: research-planner
description: 学习笔记需求澄清与引导。分析用户学习需求，引导明确学习目标和方向，调用 workflow-orchestrator 生成项目结构。触发词：想学、帮我整理、研究一下、了解一下、不知道从哪开始、research planning、explore topic。
---

# Research Planner - 学习笔记需求澄清与引导

分析用户学习需求，引导明确学习目标和方向。

## 核心职责

1. **意图澄清**: 通过提问和探测，帮用户明确学习方向
2. **调用编排器**: 调用 workflow-orchestrator 生成项目结构和 todo.md

## 触发条件

当用户提出以下类型的请求时，调用此技能:

- "我想学 XX"
- "帮我研究一下 XX"
- "不知道从哪开始学"
- "帮我整理 XX 相关的知识"
- 任何涉及学习新主题的请求

## 工作流程

### Step 1: 分析用户需求

**收集关键信息**:

```yaml
必填信息:
  - 学习主题: 要学什么？
  
可选信息 (如未提供，通过提问收集):
  - 学习深度: 入门/上手/精通
  - 现有基础: 零基础/有了解/熟悉
  - 学习目的: 实战/概念/心得/对比
  - 时间限制: 期望多久完成
  - 输出位置: 项目 output / 用户指定 Obsidian vault
  - MOC 目录: 是否需要同步到某个 MOC 文件
```

**需求分类**:
- 本 planner 专用于 **learning-note-flow** 工作流
- 其他类型需求（项目类/阅读类/调研类）由对应的 planner 处理
- orchestrator 根据 planner 传入的 `workflow` 参数决定使用哪个模板，无需在本 planner 内分类

---

### Step 2: 探测式引导

**场景判断**:

#### 场景 A: 信息充足
用户已经明确说明学习主题、深度、目的。

**操作**: 直接进入 Step 3

#### 场景 B: 方向模糊
用户有学习主题，但方向不明确。

**操作**:
1. 派发 2-3 个 subagent 并行探测
2. 每个 subagent 搜索不同角度:
   - Subagent 1: 搜索 "XX 入门教程"
   - Subagent 2: 搜索 "XX 最佳实践"
   - Subagent 3: 搜索 "XX 常见问题"
3. 汇总探测结果，展示方向菜单
4. 等待用户选择

#### 场景 C: 完全无方向
用户只有模糊的兴趣，不知道从哪开始。

**操作**:
1. 派发更多 subagent 进行深度探测
2. 搜索 "XX 是什么"、"XX 能做什么"、"XX 学习路线"
3. 提供完整选项菜单
4. 引导用户做出选择

---

### Step 3: 调用 workflow-orchestrator

**调用方式**:

```yaml
调用 /workflow-orchestrator 传入:
  workflow: "learning-note-flow"       # 本 planner 专用于此工作流
  topic: "{用户学习主题}"
  depth: "{学习深度}"
  level: "{用户基础}"
  purpose: "{学习目的}"
  output_target: "{project-output 或 obsidian}"
  vault_path: "{用户指定 vault 路径，可后续补}"
  note_folder: "{vault 内相对目录，可后续补}"
  moc_path: "{MOC 路径，可后续补}"
```

orchestrator 将根据 `workflow` 参数定位 `templates/learning-note-flow.md`（说明书）和 `templates/learning-note-todo.md`（todo 模板），生成 `${WORKSPACE_PATH:-./workspace}/{project_slug}/todo.md`。

---

### Step 4: 生成意图文件

基于用户确认的方向，生成意图文件:

```bash
# 文件路径
${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/00_intent.md
```

**意图文件格式**:

```markdown
# {主题} - 意图文件

## 基本信息

- **主题**: {topic}
- **项目标识**: {project_slug}
- **创建时间**: {date}
- **当前阶段**: 阶段 0
- **输出目标**: {project-output/obsidian}
- **Vault 路径**: {vault_path 或 待指定}
- **笔记目录**: {note_folder 或 待指定}
- **MOC 路径**: {moc_path 或 待指定}

## 学习目标

### 笔记类型
{实战笔记/概念笔记/心得笔记/对比笔记}

### 学习深度
{入门/上手/精通}

### 用户基础
{零基础/有了解/熟悉}

## 研究计划

### 探索方向
1. {方向 1}
2. {方向 2}
3. {方向 3}

### 重点收集
- **核心概念**: {列出需要理解的核心概念}
- **实战代码**: {列出需要的代码示例}
- **常见坑**: {列出需要避免的问题}
- **工具链**: {列出相关工具和生态}

### 信源偏好
- 官方文档: {是/否}
- 技术博客: {是/否}
- 社区讨论: {是/否}
- 学术论文: {是/否}

## 备注

{其他需要注意的事项}
```

---

### Step 5: 输出结果

**返回信息**:

```markdown
## ✅ 意图澄清完成

### 项目信息
- 主题: {topic}
- 目录: ${WORKSPACE_PATH:-./workspace}/{project_slug}/
- 工作流: learning-note-flow

### 意图文件
已生成: `${WORKSPACE_PATH:-./workspace}/{project_slug}/00_intent.md`

### todo.md
已生成: `${WORKSPACE_PATH:-./workspace}/{project_slug}/todo.md`

### 后续步骤
1. 系统将调用 `/research-collector` 收集资料
2. 按照 todo.md 执行各阶段任务
3. 每阶段完成后需要用户确认
```

## 与其他技能的关系

本技能负责意图澄清，完成后调用 workflow-orchestrator 生成 todo.md。完整编排流程见 `.claude/skills/workflow-orchestrator/SKILL.md`，阶段执行流见 `templates/learning-note-flow.md`。

核心链路：
```
research-planner → workflow-orchestrator → research-collector
→ outline-generator → chapter-writer → note-assembler → note-beautifier
```

## 调用示例

### 示例 1: 明确需求

```markdown
用户：我想学习 React Server Components，帮我整理一下

助手：
1. 分析用户需求
   - 学习主题: React Server Components
   - 学习深度: 待确认
   - 学习目的: 学习笔记

2. 调用 workflow-orchestrator
   - 选择 learning-note-flow 工作流
   - 生成 ./workspace/react-server-components/todo.md

3. 生成意图文件
   - ./workspace/react-server-components/00_intent.md

4. 返回后续步骤
```

### 示例 2: 模糊需求

```markdown
用户：我想学 React，不知道从哪开始

助手：
1. 分析用户需求
   - 学习主题: React
   - 学习深度: 不明确
   - 学习目的: 不明确

2. 探测式引导
   - 派发 subagent 探测不同方向
   - 展示方向菜单:
     A. React 基础入门
     B. React 状态管理
     C. React 性能优化
     D. React 项目实战

3. 等待用户选择后，继续执行 Step 3-5
```

## 注意事项

1. **必须调用 workflow-orchestrator**: 不要手动创建 todo.md
2. **保持意图文件简洁**: 只记录关键信息，不要过度详细
3. **等待用户确认**: 关键选择需要用户确认
4. **支持中断恢复**: 如果用户中途退出，下次可以继续
