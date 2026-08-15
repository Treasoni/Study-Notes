# 学习笔记工作流

## 工作流描述

完整的学习笔记生产流程，从意图澄清到 Obsidian 发布和 MOC 整理。适用于系统学习某个技术、概念或工具。

## 阶段定义

### 阶段 0: 意图澄清
- **负责技能**: /research-planner
- **前置条件**: 无
- **检查项**:
  - [ ] 用户输入已分析
  - [ ] 笔记类型已确定（实战/概念/心得/对比）
  - [ ] 学习深度已确定（入门/上手/精通）
  - [ ] 用户基础已确定（零基础/有了解/熟悉）
  - [ ] 输出位置策略已确定（项目 output / 用户指定 Obsidian vault）
  - [ ] 如发布到 Obsidian，已记录 vault_path、note_folder、moc_path（可后续补）
  - [ ] 意图文件已生成：`./00_intent.md`
- **输出文件**: `00_intent.md`
- **状态**: [P0] ⬜ 未开始

### 阶段 1: 探测式收集
- **负责技能**: /research-collector
- **前置条件**: 阶段 0 完成
- **检查项**:
  - [ ] 已派出 2-3 个 subagent 并行探测
  - [ ] 探测结果已汇总
  - [ ] 方向菜单已展示给用户
  - [ ] 用户已选择学习方向
  - [ ] 探测结果已保存：`./01_explore_result.md`
- **输出文件**: `01_explore_result.md`
- **状态**: [P1] ⬜ 未开始

### 阶段 2: 深度收集
- **负责技能**: /research-collector
- **前置条件**: 阶段 1 完成
- **检查项**:
  - [ ] 已根据用户选择的方向启动深度收集
  - [ ] 核心概念/理论素材已收集
  - [ ] 实战代码/项目案例已收集
  - [ ] 常见坑/最佳实践已收集
  - [ ] 工具链/生态已收集
  - [ ] 进阶路径/学习资源已收集
  - [ ] 素材质量已确认（官方文档数、教程数、深度文章数）
  - [ ] 深度素材已保存：`./02_deep_research.md`
- **输出文件**: `02_deep_research.md`
- **状态**: [P2] ⬜ 未开始

### 阶段 3: 大纲生成
- **负责技能**: outline-generator agent
- **前置条件**: 阶段 2 完成
- **检查项**:
  - [ ] 已读取意图文件和深度素材
  - [ ] 已根据笔记类型选择大纲结构
  - [ ] 大纲已生成（≤3级层级）
  - [ ] 每章已标注：篇幅、素材引用、代码示例
  - [ ] 大纲已展示给用户确认
  - [ ] 大纲已保存：`./03_outline.md`
- **输出文件**: `03_outline.md`
- **状态**: [P3] ⬜ 未开始

### 阶段 4: 逐章写作
- **负责技能**: chapter-writer agent
- **前置条件**: 阶段 3 完成
- **检查项**:
  - [ ] 第 1 章已写完并确认
  - [ ] 第 2 章已写完并确认
  - [ ] 第 3 章已写完并确认
  - [ ] ...（根据实际章节数添加）
  - [ ] 并行写作时各章过渡语自包含（按大纲），不读取上一章文件
  - [ ] 子 agent 未直接修改 workflow state file（章节状态由 orchestrator 集中更新）
- **输出文件**: `chapters/{N}_{章节名}.md`
- **状态**: [P4] ⬜ 未开始

### 阶段 5: 收尾组装
- **负责技能**: note-assembler agent
- **前置条件**: 阶段 4 完成
- **检查项**:
  - [ ] 所有章节文件已检查
  - [ ] 组装方式已确认（A: 按顺序拼接 / B: 重新排序 / C: 保持零散）
  - [ ] 过渡语已添加
  - [ ] 目录已生成
  - [ ] 标题层级已统一
  - [ ] 引用已检查
  - [ ] 脚注 ID 已命名空间化（`[^cN-...]`）并 grep 校验无重复
  - [ ] 产物大小已预判；>100KB 由父进程拆分合并
  - [ ] 完整笔记已保存：`./output/final_note.md`
- **输出文件**: `output/final_note.md`
- **状态**: [P5] ⬜ 未开始

### 阶段 6: Obsidian 美化与发布
- **负责技能**: /note-beautifier
- **前置条件**: 阶段 5 完成
- **检查项**:
  - [ ] 已读取 Obsidian 输出规则
  - [ ] 用户已确认最终保存位置（vault_path + note_folder，或仅项目 output）
  - [ ] frontmatter、标签、Callout、双链已按 Obsidian 规则处理
  - [ ] 最终 Markdown 已保存到用户指定位置或 `./output/final_note.md`
- **输出文件**: 用户指定的 Obsidian 笔记路径，或 `output/final_note.md`
- **状态**: [P6] ⬜ 未开始

### 阶段 7: MOC 同步
- **负责技能**: /moc-organizer
- **前置条件**: 阶段 6 完成，且用户提供或确认 MOC 路径
- **检查项**:
  - [ ] 已定位或创建 MOC 文件
  - [ ] 新笔记双链已加入 MOC
  - [ ] 已去重并更新摘要/标签
  - [ ] MOC 只保留索引，不复制正文
- **输出文件**: 用户指定的 MOC 文件
- **状态**: [P7] ⬜ 未开始

## 目录结构

```
${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/
├── 00_intent.md              # 意图文件（阶段 0）
├── 01_explore_result.md      # 探测结果（阶段 1）
├── 02_deep_research.md       # 深度素材（阶段 2）
├── 03_outline.md             # 大纲文件（阶段 3）
├── workflow-runs/{topic}.workflow.md # 运行状态文件（位于 workspace/workflow-runs/）
├── chapters/                 # 章节目录（阶段 4）
│   ├── 01_xxx.md
│   ├── 02_xxx.md
│   └── ...
└── output/                   # 项目内暂存产物（阶段 5-6）
    ├── final_note.md
    └── final_note.{format}
```

## 状态流转

状态通过 `[PN]` 阶段标记和 YAML frontmatter 共同记录。每次阶段切换都调用 `.claude/scripts/todo-state.sh`，避免各 skill 手写 `sed` 导致状态漂移：

```
[PN] ⬜ 未开始  →  [PN] 🔲 进行中  →  [PN] ✅ 已完成
                  └── [PN] ⏭️ 跳过
```

每个阶段的状态行由唯一的 `[P0]`～`[P7]` 前缀标识。状态脚本会同时更新阶段行、`current_phase`、`current_status`、`last_updated`、`blocked_reason` 和确认记录。阶段只有在用户确认后才能完成；跳过阶段必须先启动并记录原因：
```bash
.claude/scripts/todo-state.sh "$RUN_STATE_FILE" start P2
.claude/scripts/todo-state.sh "$RUN_STATE_FILE" mode P2 freeform "用户选择随性模式"
.claude/scripts/todo-state.sh "$RUN_STATE_FILE" confirm P2 "用户确认研究方向"
.claude/scripts/todo-state.sh "$RUN_STATE_FILE" complete P2
.claude/scripts/todo-state.sh "$RUN_STATE_FILE" start P3
.claude/scripts/todo-state.sh "$RUN_STATE_FILE" skip P3 "随性模式不生成大纲"
```

## 执行模式

工作流支持两种执行模式，在**阶段 2（深度收集）完成前**选择分支：

### 大纲模式（默认）
适用场景：需要结构化笔记输出的场景。流程：
```
阶段 0-2（资料收集）→ 阶段 3（生成大纲）→ 用户确认大纲
→ 阶段 4（逐章写作）→ 阶段 5（组装）→ 阶段 6（Obsidian 美化发布）→ 阶段 7（MOC 同步）
```

**触发规则**：阶段 3 正常执行完毕后，workflow state file 中阶段 3 状态标记为 ✅，阶段 4 开始执行。

### 随性模式（跳过阶段 3-4）
适用场景：快速笔记、心得、或用户明确表示"不需要大纲"。

**触发规则**：
1. 用户在阶段 2 进行中选择"跳过，直接出笔记"。
2. 调用状态脚本将运行模式持久化为 `freeform`，再确认并完成阶段 2：
   ```bash
   .claude/scripts/todo-state.sh "$RUN_STATE_FILE" mode P2 freeform "用户选择随性模式"
   .claude/scripts/todo-state.sh "$RUN_STATE_FILE" confirm P2 "用户确认直接组装"
   .claude/scripts/todo-state.sh "$RUN_STATE_FILE" complete P2
   ```
3. 依次启动并跳过阶段 3 和阶段 4；脚本会把选择写入方向调整记录和跳过记录：
   ```bash
   .claude/scripts/todo-state.sh "$RUN_STATE_FILE" start P3
   .claude/scripts/todo-state.sh "$RUN_STATE_FILE" skip P3 "随性模式不生成大纲"
   .claude/scripts/todo-state.sh "$RUN_STATE_FILE" start P4
   .claude/scripts/todo-state.sh "$RUN_STATE_FILE" skip P4 "随性模式不逐章写作"
   ```
4. 直接跳入阶段 5（使用自由组装模式 C：保持零散片段）。

**决策点**：阶段 2 结束时，`research-collector` 询问用户："是进入大纲模式（逐章写），还是随性模式（直接出笔记）？"

### 运行时章节数（阶段 4）

阶段 4 的实际章节数由阶段 3 的大纲决定，非固定值。`{total_chapters}` 占位符在阶段 3 完成后由 `outline-generator` 替换：
```bash
# 从大纲文件统计章节数
WORKSPACE_PATH="${WORKSPACE_PATH:-./workspace}"
TOTAL_CHAPTERS=$(grep -c "^### 第.*章" "${WORKSPACE_PATH}/${PROJECT_SLUG}/03_outline.md")
perl -0pi -e "s/\\{total_chapters\\}/${TOTAL_CHAPTERS}/g" "${RUN_STATE_FILE}"
```

## 阶段完成检查点

每阶段结束都必须让用户确认后才进入下一阶段:

| 阶段 | 检查点内容 |
|------|-----------|
| 0 → 1 | 用户确认意图文件和研究计划 |
| 1 → 2 | 用户确认素材质量 |
| 2 → 3 | 用户确认大纲顺序和深度 |
| 3 → 4 | 用户确认大纲（大纲模式） |
| 4 → 5 | 所有章节写作完成 |
| 5 → 6 | 用户确认组装结果和 Obsidian 输出位置 |
| 6 → 7 | 用户确认是否同步 MOC |

## 错误处理

| 情况 | 处理方式 |
|------|---------|
| 缺少意图文件 | 重新调用 `/research-planner` |
| 缺少素材文件 | 重新调用 `/research-collector` |
| 缺少大纲文件 | 重新调用 `outline-generator` |
| 缺少章节文件 | 重新调用 `chapter-writer` |
| 缺少输出位置 | 先保存到项目 `output/`，等待用户指定 Obsidian 位置 |
| 旧笔记过时 | 调用 `note-updater`，不要重跑完整新笔记流程 |

## 技能依赖关系

```
research-planner (阶段 0)
    │
    ▼
research-collector (阶段 1-2)
    │
    ▼
outline-generator (阶段 3)
    │
    ▼
chapter-writer (阶段 4)
    │
    ▼
note-assembler (阶段 5)
    │
    ▼
note-beautifier (阶段 6: Obsidian)
    │
    ▼
moc-organizer (阶段 7)
```
