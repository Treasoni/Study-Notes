---
comet_change: update-note-workflow
role: technical-design
canonical_spec: openspec
archived-with: 2026-06-02-update-note-workflow
status: final
---

# Update Note Workflow — 设计文档

## 概述

新增 `update-workflow` skill 作为笔记更新的工作流编排层。包装现有 `update` skill（INSERT 模式），内部直接调度 mini collect→curate→write 研究循环（REFRESH 模式），并提供结构验证和用户确认。

## 架构

```
update-workflow skill (新增)
├── Step 1: 定位笔记 + 解析结构
├── Step 2: 意图检测 (INSERT / REFRESH)
├── Step 3: 执行更新
│   ├── INSERT → 委托 /update skill
│   └── REFRESH → 内部调度 mini research → 委托 /update skill 插入
├── Step 4: 结构验证
└── Step 5: 用户确认 diff
```

## 详细设计

### Step 1: 定位笔记 + 解析结构

**定位策略**：
1. `note_query` 是路径（含 `/` 或 `.md` 后缀）→ 直接定位
2. `note_query` 是名称 → 多级搜索：
   - 优先搜索用户配置的 `OUTPUT_PATH`（来自 `.obsidian-config.md`）
   - 再搜索 `3-published/`
   - 再搜索整个 vault 根目录
3. 找到多个匹配 → 列出候选让用户选择
4. 找不到 → 报错并建议用户指定路径

**结构解析**（定位后立即执行）：
- 读取 YAML frontmatter：`type`、`tags`、`created`、`updated`
- 扫描标题层级树（`#` → `##` → `###` ...）
- 识别 Callout 类型（`> [!note]`、`> [!tip]` 等）
- 识别表格格式和代码块语言
- 统计现有 wikilinks

产出：`note_context` 对象，传递给后续步骤。

### Step 2: 意图检测

**自动检测规则**：

| 关键词/模式 | → 意图 |
|-------------|--------|
| "加上"、"添加"、"补充"、"追加" + 用户提供内容 | INSERT |
| "过时"、"更新"、"刷新"、"替换" + 指定章节 | REFRESH |
| "在 XXX 章节后加"、"在末尾追加" | INSERT |
| 模糊不清 | → 询问用户 |

**REFRESH 二级决策**：
检测到 REFRESH 后，询问用户：
1. "直接替换此章节内容？" → 走 INSERT（用户提供替换内容）
2. "先重新搜集资料再更新？" → 走 mini research cycle

### Step 3: 执行更新

#### INSERT 模式

委托 `/update` skill，传入：
- 目标笔记路径
- 用户提供的新内容
- 目标位置（章节名或"追加到末尾"）

update skill 负责格式匹配、最小改动插入、frontmatter 更新。

#### REFRESH 模式（Mini Research Cycle）

```
┌──────────────────────────────────────────────────────────┐
│  REFRESH: Mini Research Cycle                            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. 创建 mini TODO.md（3 个阶段）                        │
│     - [ ] mini-collect                                   │
│     - [ ] mini-curate                                    │
│     - [ ] mini-write                                     │
│                                                          │
│  2. 目录隔离                                             │
│     0-inbox/{subtopic}/raw/                              │
│     1-curated/{subtopic}/                                │
│     2-drafts/{subtopic}/                                 │
│                                                          │
│  3. 传入父主题上下文                                     │
│     · 父主题名                                           │
│     · 父笔记类型 (concept/practice/...)                  │
│     · 目标章节标题层级 (###)                              │
│     · 格式约定 (callout类型、表格风格)                    │
│                                                          │
│  4. 调度顺序                                             │
│     /collect → /curate → /write                          │
│     （每步完成后标记 TODO.md [x]）                        │
│                                                          │
│  5. write 产出 → 纯章节正文（无 frontmatter）             │
│                                                          │
│  6. 委托 /update skill 插入父笔记                        │
│                                                          │
│  7. 清理 mini TODO.md                                    │
└──────────────────────────────────────────────────────────┘
```

**关键约束**：
- write skill 必须只生成目标章节的正文，不生成 frontmatter 或完整笔记结构
- mini 循环的 topic 参数使用子主题名（如 "useEffect cleanup"），搜索词附加父主题上下文

### Step 4: 轻量验证

**验证清单**：

| 检查项 | 方法 | 失败处理 |
|--------|------|----------|
| 标题层级连贯性 | 扫描所有 `#` 标题，检查是否跳级（如 `##` → `####`） | 报告具体位置，建议修正 |
| 双链完整性 | 提取所有 `[[wikilinks]]`，检查目标文件是否存在 | 报告断链，建议修复或删除 |
| frontmatter updated | 检查 `updated` 字段是否为当前日期 | 自动修正 |

**验证不阻塞**：验证发现问题时，向用户报告并询问是否继续。不自动阻止写入。

### Step 5: 用户确认

**Diff 摘要格式**：
```
📝 更新摘要
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
目标笔记: {note_path}
更新模式: {INSERT|REFRESH}
修改章节: {section_name}
内容变化: +{added_lines} 行 / ~{modified_lines} 行
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**确认流程**：
1. 展示 diff 摘要
2. 用户确认 → 保存文件，流程结束
3. 用户要求修改 → 调整后重新展示摘要
4. 用户取消 → 不保存，流程结束

## 测试策略

| 测试场景 | 覆盖步骤 | 验证点 |
|----------|----------|--------|
| INSERT: 按名称定位 + 插入 | Step 1, 2, 3 | 笔记找到、模式正确、内容插入、格式匹配 |
| INSERT: 按路径定位 + 追加到末尾 | Step 1, 3 | 直接定位、追加正确 |
| REFRESH: 直接替换 | Step 2, 3 | REFRESH 检测、替换正确 |
| REFRESH: mini research cycle | Step 2, 3, 4 | TODO.md 创建/清理、子目录隔离、上下文传递、研究循环完成 |
| 验证: 标题跳级检测 | Step 4 | 检测到跳级并报告 |
| 验证: 断链检测 | Step 4 | 检测到断链并报告 |
| 定位: 多个匹配候选 | Step 1 | 列出候选让用户选择 |
| 定位: 找不到笔记 | Step 1 | 报错并建议路径 |
| 模糊意图询问 | Step 2 | 自动检测失败时询问用户 |
| 用户取消 | Step 5 | 不保存文件 |

## 风险与权衡

- **[Risk] REFRESH mini 循环的上下文传递可能不完整** → Mitigation: 在调用各 skill 时显式传入父笔记信息（父主题名、笔记类型、标题层级、格式约定）
- **[Trade-off] INSERT 模式不追踪状态** → 单步操作不需要，但如果用户在插入过程中中断，需要重新开始（可接受）
- **[Trade-off] 不支持批量更新** → 聚焦核心场景，批量需求可通过多次调用满足
- **[Trade-off] 验证不阻塞** → 允许用户在验证失败时仍继续，依赖用户判断（灵活但有风险）
