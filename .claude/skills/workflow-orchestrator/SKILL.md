---
name: workflow-orchestrator
description: 工作流编排器。由各 planner 技能调用，接收工作流名称和参数，从模板生成 todo.md。不直接面向用户。
---

# Workflow Orchestrator - 工作流编排器

接收 planner 传入的工作流参数，定位模板，生成 todo.md 执行检查清单。

## 核心架构

```
各 planner 技能（research-planner / 未来 project-planner ...）
    │
    │  传入参数: workflow, topic, depth, level, purpose ...
    │
    ▼
workflow-orchestrator (本技能)
    │
    ├── 根据 workflow 参数定位模板
    │
    ├── sed 替换占位符
    │
    ├── 生成 todo.md
    │
    └── 返回项目路径
```

## 触发条件

**本技能不直接面向用户**，由 planner 技能调用：

- `research-planner` 完成意图澄清后，调用本技能生成 todo.md
- 未来新增的 planner（如 project-planner）同样调用本技能
- 用户不应直接触发 `/workflow-orchestrator`

## 核心功能

### 功能 1: 工作流模板管理

**模板存储位置**: `templates/` 目录

**每个工作流由两个文件组成**:

| 文件 | 命名 | 用途 | 谁来读 |
|------|------|------|--------|
| 工作流说明书 | `{workflow-name}.md` | 定义阶段、检查点、错误处理、技能依赖 | agent / 人（理解流程） |
| todo 模板 | `{workflow-name}-todo.md` | 带 `{topic}` 等占位符的执行清单 | orchestrator（sed 替换生成 todo.md） |

**当前可用工作流**:

| 工作流 | 说明书 | todo 模板 | 用途 | 阶段数 |
|-------|--------|----------|------|--------|
| learning-note-flow | learning-note-flow.md | learning-note-todo.md | 完整学习笔记生产 + Obsidian 发布 + MOC 同步 | 8 (阶段 0-7) |
| legacy-note-import-flow | legacy-note-import-flow.md | legacy-note-import-todo.md | 已有旧笔记批量导入、规范化、可选更新与 MOC 同步 | 6 (阶段 0-5) |
| batch-note-update-flow | batch-note-update-flow.md | batch-note-update-todo.md | 多篇既有笔记批量更新、逐篇局部 patch 与 MOC 同步 | 6 (阶段 0-5) |

**说明书格式要求**:
- 必须包含: 工作流名称、描述、各阶段定义
- 每个阶段必须包含: 名称、负责技能、检查项、输出文件、状态
- 支持自定义阶段数和检查项

**todo 模板格式要求**:
- 必须使用占位符: `{topic}` `{project_slug}` `{date}`
- 必须包含 YAML frontmatter: `workflow`、`topic`、`project_slug`、`created_at`、`last_updated`、`current_phase`、`current_status`、`mode`、`blocked_reason`
- 检查项必须与同名说明书各阶段一一对应
- 初始状态统一为 `⬜ 未开始`
- 阶段状态行必须使用唯一前缀 `> [PN] ...`，运行时通过 `.claude/scripts/todo-state.sh` 更新

### 功能 2: 接收 planner 参数

orchestrator 不负责选择工作流——调用方 planner 会明确传入 `workflow` 参数。

**planner 传入的参数结构**:
```yaml
必传:
  workflow: "learning-note-flow"    # 由 planner 指明要使用哪个工作流
  topic: "React Server Components"  # 主题

可选（各 planner 自行决定传哪些）:
  depth: "精通"          # 学习深度
  level: "有了解"        # 用户基础
  purpose: "实战"        # 目的
  output_target: "project-output"  # project-output 或 obsidian
  vault_path: ""         # 用户指定 Obsidian vault 根目录，可后续补
  note_folder: ""        # vault 内相对目录，可后续补
  moc_path: ""           # MOC 文件路径，可后续补
```

**orchestrator 的职责**: 收到参数 → 定位 workflow 对应的模板 → 生成 todo.md。

### 功能 3: 生成 todo.md

根据 workflow 参数定位说明书和 todo 模板，用 sed 替换占位符生成定制化 todo.md。

**生成逻辑**:

> 路径约定：模板位于本 skill 目录下，项目产物位于 `${WORKSPACE_PATH:-./workspace}` 下。不要写死 `/workspace`。

```bash
# 0. planner 传入的参数
WORKFLOW="${1:-learning-note-flow}"   # 工作流名称
TOPIC="${2}"                          # 主题

# 1. 生成项目 slug
PROJECT_SLUG=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

# 2. 定位模板文件（以 workflow 名称匹配）
FLOW_DOC=".claude/skills/workflow-orchestrator/templates/${WORKFLOW}.md"
case "$WORKFLOW" in
  learning-note-flow) TODO_TEMPLATE=".claude/skills/workflow-orchestrator/templates/learning-note-todo.md" ;;
  legacy-note-import-flow) TODO_TEMPLATE=".claude/skills/workflow-orchestrator/templates/legacy-note-import-todo.md" ;;
  batch-note-update-flow) TODO_TEMPLATE=".claude/skills/workflow-orchestrator/templates/batch-note-update-todo.md" ;;
  *) TODO_TEMPLATE=".claude/skills/workflow-orchestrator/templates/${WORKFLOW}-todo.md" ;;
esac

# 3. 验证模板存在
if [ ! -f "$TODO_TEMPLATE" ]; then
    echo "错误: 工作流 '${WORKFLOW}' 的 todo 模板不存在"
    echo "请确保 templates/ 下有 ${WORKFLOW}-todo.md"
    exit 1
fi

# 4. 创建项目目录
WORKSPACE_PATH="${WORKSPACE_PATH:-./workspace}"
PROJECT_DIR="${WORKSPACE_PATH}/${PROJECT_SLUG}"
mkdir -p "${PROJECT_DIR}"

# 5. 读取 todo 模板并替换占位符，生成 todo.md
sed -e "s/{topic}/${TOPIC}/g" \
    -e "s/{project_slug}/${PROJECT_SLUG}/g" \
    -e "s/{date}/$(date +%Y-%m-%d)/g" \
    -e "s/{completed_chapters}/0/g" \
    -e "s/{total_chapters}/待大纲确定/g" \
    "${TODO_TEMPLATE}" > "${PROJECT_DIR}/todo.md"

# 注：{total_chapters} 和 {completed_chapters} 会在运行时由对应阶段更新：
# - 阶段 3 (outline-generator): 根据大纲统计章节数 → 替换 {total_chapters}
# - 阶段 4 (chapter-writer): 每完成一章 → 递增 {completed_chapters}
```

## 工作流程

### Step 1: 接收 planner 传入的参数

orchestrator 从调用方 planner 接收结构化参数：

```yaml
必传:
  workflow: "learning-note-flow"      # 指明使用哪个工作流

强烈建议:
  topic: "React Server Components"    # 主题/标题

可选:
  project_slug: "react-server-components"  # 如不传，由 orchestrator 根据 topic 自动生成
  depth: "精通"       # 学习深度
  level: "有了解"     # 用户基础
  purpose: "实战"     # 目的/类型
  output_target: "project-output" | "obsidian"
  vault_path: "{用户指定 vault 路径，可后续补}"
  note_folder: "{vault 内相对目录，可后续补}"
  moc_path: "{MOC 路径，可后续补}"
```

### Step 2: 定位模板

根据 `workflow` 参数定位说明书和 todo 模板：

```bash
# 根据 workflow 参数定位模板
FLOW_DOC=".claude/skills/workflow-orchestrator/templates/${WORKFLOW}.md"
case "$WORKFLOW" in
  learning-note-flow) TODO_TEMPLATE=".claude/skills/workflow-orchestrator/templates/learning-note-todo.md" ;;
  legacy-note-import-flow) TODO_TEMPLATE=".claude/skills/workflow-orchestrator/templates/legacy-note-import-todo.md" ;;
  batch-note-update-flow) TODO_TEMPLATE=".claude/skills/workflow-orchestrator/templates/batch-note-update-todo.md" ;;
  *) TODO_TEMPLATE=".claude/skills/workflow-orchestrator/templates/${WORKFLOW}-todo.md" ;;
esac

# 验证存在
if [ ! -f "$TODO_TEMPLATE" ]; then
    echo "错误: 工作流 '${WORKFLOW}' 未配置"
    ls -1 .claude/skills/workflow-orchestrator/templates/*-todo.md | sed 's/.*\///;s/-todo.md//'
    echo "以上为可用工作流"
    exit 1
fi
```

### Step 3: 生成 todo.md

sed 替换占位符，从 todo 模板生成项目特定的 todo.md（具体 sed 逻辑见"功能 3"）。

### Step 4: 创建项目目录

```bash
WORKSPACE_PATH="${WORKSPACE_PATH:-./workspace}"
PROJECT_DIR="${WORKSPACE_PATH}/${PROJECT_SLUG}"
mkdir -p ${PROJECT_DIR}
```

### Step 5: 输出结果

**返回信息**:
- 项目目录路径
- todo.md 内容预览
- 可用工作流列表
- 后续步骤提示

**输出格式**:
```markdown
## ✅ 项目已创建

### 项目信息
- 主题: {topic}
- 目录: ${WORKSPACE_PATH:-./workspace}/{project_slug}/
- 工作流: learning-note-flow

### todo.md 已生成
[预览 todo.md 内容]

### 后续步骤
1. 运行 `/research-planner` 进行意图澄清
2. 系统将自动调用 workflow-orchestrator 生成 todo.md
3. 按照 todo.md 执行各阶段任务
```

## 模板格式规范

每个模板文件必须包含以下结构:

```markdown
# {工作流名称}

## 工作流描述

{简要描述工作流的用途}

## 阶段定义

### 阶段 0: {阶段名称}
- **负责技能**: /skill-name 或 agent-name
- **前置条件**: {阶段 N 完成} (可选)
- **检查项**:
  - [ ] 检查项 1
  - [ ] 检查项 2
- **输出文件**: `filename.md`
- **状态**: ⬜ 未开始

### 阶段 1: {阶段名称}
...

## 目录结构

```
${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/
├── file1.md
├── file2.md
└── ...
```

## 状态流转

```
⬜ 未开始 → 🔲 进行中 → ✅ 已完成
               └── ⏭️ 跳过 / blocked_reason
```

状态更新统一调用项目脚本，避免各 skill 手写 `sed`：

```bash
.claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" start P1
.claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" complete P1
.claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" skip P3 "用户选择随性模式"
.claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" block P2 "来源质量不足"
```

## 与其他技能的关系

```
各 planner（领域特异性）
    │
    │  research-planner ──→ workflow="learning-note-flow"
    │  legacy-note-importer ──→ workflow="legacy-note-import-flow"
    │  batch-note-updater ──→ workflow="batch-note-update-flow"
    │  project-planner  ──→ workflow="project-flow" (未来)
    │
    ▼
workflow-orchestrator (本技能)
    │
    ├── 读 templates/{workflow}.md (说明书)
    ├── 读 templates/{workflow}-todo.md (todo 模板)
    ├── sed 替换占位符
    └── 生成 ${WORKSPACE_PATH:-./workspace}/{slug}/todo.md
         │
         ▼
按 todo.md 各阶段执行:
research-collector → outline-generator → chapter-writer → note-assembler → note-beautifier
legacy-note-importer → note-beautifier → note-updater（可选） → moc-organizer
batch-note-updater → note-updater → moc-organizer（可选）
```

## 调用示例

### 示例 1: research-planner 调用

```markdown
research-planner 完成意图澄清后:

调用 workflow-orchestrator:
  参数:
    workflow: learning-note-flow
    topic: React Server Components
    depth: 上手
    level: 有了解
    purpose: 实战

orchestrator:
  1. 定位模板:
     templates/learning-note-flow.md (说明书)
     templates/learning-note-todo.md (todo 模板)
  2. sed 替换生成 ./workspace/react-server-components/todo.md
  3. 返回项目路径
```

### 示例 2: 查看可用工作流

```markdown
查看 orchestrator templates/ 目录即可:

  templates/
    learning-note-flow.md       ← 说明书
    learning-note-todo.md       ← todo 模板
    legacy-note-import-flow.md  ← 说明书
    legacy-note-import-todo.md  ← todo 模板
    batch-note-update-flow.md   ← 说明书
    batch-note-update-todo.md   ← todo 模板

每个工作流一对文件。规划添加新工作流时，同时创建这俩文件 + 对应的 planner 或入口 skill。
```

## 扩展指南

### 添加新工作流（完整流程）

1. **创建模板文件对**:
   ```bash
   WORKFLOW="project-flow"
   touch .claude/skills/workflow-orchestrator/templates/${WORKFLOW}.md        # 说明书
   touch .claude/skills/workflow-orchestrator/templates/${WORKFLOW}-todo.md   # todo 模板
   ```

2. **写说明书**: 定义阶段、检查项、技能依赖（格式见"模板格式规范"）

3. **写 todo 模板**: 带 `{topic}` `{project_slug}` `{date}` 占位符，并包含恢复用 YAML frontmatter

4. **创建对应 planner 或入口 skill**: 在 `.claude/skills/` 下新建 skill，负责该领域的意图澄清，完成后调用 orchestrator 并传入 `workflow="project-flow"`

5. **更新项目路由文档**: 在 `AGENTS.md` 和 `.claude/rules/common/skill-invocation.md` 中添加触发规则

6. **测试**: 通过对应 planner 触发，验证 todo.md 生成正确

## 注意事项

1. **模板兼容性**: 新模板必须遵循格式规范
2. **阶段依赖**: 确保前置条件正确设置
3. **输出文件**: 使用固定命名，方便下游读取
4. **状态管理**: 通过 `.claude/scripts/todo-state.sh` 维护 ⬜/🔲/✅/⏭️ 状态和恢复元数据
5. **用户确认**: 关键阶段需要用户确认后才继续
6. **输出位置**: 最终笔记发布位置由用户指定；未指定时只写项目 `output/`
7. **旧笔记导入**: 用户已有一批笔记要接入项目时调用 `legacy-note-importer`
8. **多篇旧笔记更新**: 用户要批量更新多篇笔记时调用 `batch-note-updater`
9. **单篇旧笔记更新**: 用户要更新一篇已有笔记内容时调用 `note-updater`，不要从阶段 0 重跑
