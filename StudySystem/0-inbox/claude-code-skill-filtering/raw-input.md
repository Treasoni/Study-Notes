# Claude Code 技能 (Skill) 过滤机制设计

- 标签：#AI工作流 #ClaudeCode #Token优化 #架构设计
- 日期：2026-06-02

## 1. 背景与痛点

> 现状备注：`StudySystem` 已通过 `.study-config.yaml` 中的 `skills.mode: project | dev | all` 实现粗粒度过滤，但**目录范围匹配、Glob 通配符、公共池机制**均未支持。

在 Claude Code 工作流项目中，用于"开发/调试"的 skills 与"项目核心逻辑"（如学习、解题）的 skills 混杂在一起。主 Agent 在 Resource Discovery 阶段会把所有 skill 加载进上下文，导致：

- **Token 严重浪费**：消耗大量不必要的输入 Token。
- **Context Window 污染**：增加了大模型产生"幻觉"或执行偏离核心任务的概率。

## 2. 解决方案：基于 YAML 的预过滤机制

在 `.skill.yaml` 中新增配置项，主 Agent 在 Resource Discovery 阶段读取文件内容之前，根据配置的运行模式过滤 skill 列表。

### 核心优势

- **精确阻击 Token 浪费**：在文件读取前进行拦截，真正实现降本。
- **零迁移成本**：不移动现有的 Skill 文件，不破坏原本的 Obsidian 链接或硬编码路径。
- **配置驱动**：灵活性高，可随时按需调整。

## 3. 配置文件设计 (.skill.yaml)

建议将 Agent 的状态划分为不同模式（如 `dev` 和 `project`），并引入 `common` 公共池存放通用技能（如基础文件操作、Markdown 格式化规范）。

```yaml
# .skill.yaml 配置示例（文件名均为示意占位，不代表真实 skill）
current_mode: "project" # 运行模式切换：dev | project

skills:
  # 1. 公共技能：无论什么模式都加载
  common:
    - "core_file_ops.md"      # 示意占位
    - "standard_format.md"    # 示意占位

  # 2. 开发模式：用于调试、Prompt 调优、MCP 开发
  dev:
    - "mcp_debug.md"          # 示意占位
    - "dev_*.md"              # 建议支持 Glob 通配符，靠前缀区分
    - "scripts/**/*.md"       # 建议支持按目录范围匹配

  # 3. 生产/项目模式：核心业务流程（如考研学习流程）
  project:
    - "math_solver.md"        # 示意占位
    - "circuit_analysis.md"   # 示意占位
    - "todo_state_machine.md" # 示意占位
```

## 4. 实现与优化建议

- 支持 **Glob 通配符**
- 主 Agent 读取逻辑：解析 YAML 规则 → 展开为具体 File List → 去重 → 提交给 LLM。这样可以避免每次新增 Skill 都需要修改配置文件。
