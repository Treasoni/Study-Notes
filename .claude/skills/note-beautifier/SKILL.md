---
name: note-beautifier
description: Obsidian 笔记智能美化与发布。用于将最终学习笔记处理成 Obsidian Markdown，补 frontmatter、标签、Callout、双链，并保存到用户指定位置。触发词：美化、Obsidian、优化格式、笔记美化、发布到 vault、beautify。
---

# Note Beautifier - Obsidian 笔记智能美化与发布

将学习笔记处理成适合 Obsidian 的 Markdown。不要默认导出其他格式；本阶段面向 Obsidian vault。

## 核心架构

```
note-beautifier
    │
    ├── 分析笔记类型和内容特征
    ├── 应用 Obsidian Markdown 规则
    ├── 保存到用户指定 vault 或项目 output
    └── 如需 MOC，同步调用 moc-organizer
```

## 触发条件

当用户提出以下类型的请求时，调用此技能:

- "帮我美化一下这个笔记"
- "优化 Obsidian 笔记格式"
- "让笔记更好看"
- "笔记排版优化"
- "发布到 Obsidian vault"
- "保存到我的 Obsidian 目录"
- 任何涉及 Obsidian 笔记美化的请求

## 核心功能

### 功能 1: 笔记类型智能识别

自动分析笔记内容，识别类型并推荐相应的美化方案。

**识别维度**:
```yaml
内容类型:
  - 学习笔记 (教程、课程、学习总结)
  - 读书笔记 (书籍、文章、论文)
  - 项目笔记 (技术文档、方案设计)
  - 会议记录 (会议纪要、讨论记录)
  - 知识卡片 (概念、定义、公式)
  - 工作日志 (日报、周报、复盘)

结构特征:
  - 层级结构 (有无明确的章节划分)
  - 代码比例 (代码块占比)
  - 列表密度 (有序/无序列表数量)
  - 表格使用 (数据表格数量)
  - 引用内容 (引用块占比)
```

### 功能 2: 生成 Obsidian 美化任务清单

根据识别结果，生成需要调用的基础技能任务清单。

**任务清单格式**:
```yaml
美化任务:
  - 任务: 优化 Callout 块
    优先级: 高

  - 任务: 添加高价值双链
    优先级: 中

  - 任务: 完善 frontmatter 和标签
    优先级: 中

  - 任务: 保存到用户指定位置
    优先级: 高

  - 任务: 同步 MOC
    优先级: 中
```

### 功能 3: 输出位置

每次发布前必须确认：

```yaml
vault_path: "{用户指定 Obsidian vault 根目录}"
note_folder: "{vault 内相对目录}"
moc_path: "{可选 MOC 文件}"
publish_mode: copy | overwrite | patch
```

如果用户还没有指定位置，只保存到项目 `output/final_note.md`，并提示用户下一步指定 vault。

### 功能 4: 美化效果验证

在基础技能执行后，验证美化效果并生成报告。

**验证内容**:
```yaml
验证项:
  - Callout 块是否正确应用
  - 双链是否有效
  - 标签是否完整
  - Dataview 查询是否正确
  - 整体格式是否统一
```

## 工作流程

### Step 0: 读取项目信息和 todo.md 状态（必须执行）

**启动时必须确定项目文件夹并检查 todo.md：**

```bash
WORKSPACE_PATH="${WORKSPACE_PATH:-./workspace}"

# 从意图文件读取项目标识
PROJECT_SLUG=$(grep "项目标识" "${WORKSPACE_PATH}"/*/00_intent.md 2>/dev/null | head -1 | sed 's/.*：//')

# 如果有多个项目，提示用户选择
if [ -z "$PROJECT_SLUG" ]; then
  echo "找到以下项目："
  ls -d "${WORKSPACE_PATH}"/*/ 2>/dev/null | xargs -I {} basename {}
  echo "请指定项目名称"
  exit 1
fi

PROJECT_DIR="${WORKSPACE_PATH}/${PROJECT_SLUG}"

# 读取 todo.md
cat ${PROJECT_DIR}/todo.md 2>/dev/null || echo "不存在"
```

**状态检查：**
- 如果 todo.md 不存在：提示用户先运行 `/research-planner` 创建意图文件
- 如果 todo.md 存在但阶段 5 为 ⬜ 或 🔲：提示用户"笔记组装未完成，请先完成 `note-assembler`"
- 如果 todo.md 存在且阶段 5 为 ✅，阶段 6 为 ⬜：允许执行，更新阶段 6 为 🔲 进行中
- 如果 todo.md 存在且阶段 6 为 ✅：提示用户"美化已完成，是否要重新美化？"

**更新 todo.md 状态：**
```bash
# 将阶段 6 标记为进行中
.claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" start P6
```

**完成后更新状态：**
```bash
# 将阶段 6 标记为完成
.claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" complete P6
```

---

### Step 1: 读取笔记内容

1. 读取目标笔记文件
2. 分析内容结构和特征
3. 识别笔记类型

### Step 2: 智能分析并生成美化方案

**分析维度**:
```yaml
结构分析:
  - 标题层级深度
  - 章节划分清晰度
  - 内容组织逻辑

内容分析:
  - 代码块占比
  - 表格数量
  - 列表密度
  - 引用内容

元素分析:
  - 已有 Callout
  - 已有 Dataview
  - 已有双链
  - 已有标签
```

**生成美化方案**:
```markdown
## 美化方案

### 识别结果
- 笔记类型: 学习笔记
- 主要特征: 多代码块、有表格、概念密集

### 美化任务清单
1. [ ] 优化 Callout 块
2. [ ] 添加高价值双链
3. [ ] 完善 frontmatter 和标签系统
4. [ ] 优化表格和代码块格式
5. [ ] 保存到用户指定位置或项目 output
6. [ ] 如提供 MOC，同步索引
```

### Step 3: 执行 Obsidian 美化

**调用策略**:

#### 3.1 Markdown 语法美化

```markdown
1. **Callout 块优化**
   - 将重要概念用 `[!note]` 或 `[!abstract]` 包装
   - 将实用技巧用 `[!tip]` 标记
   - 将注意事项用 `[!warning]` 标记

2. **双链添加**
   - 识别笔记中的关键概念
   - 添加相关概念的 `[[双链]]`
   - 构建知识关联网络

3. **标签系统完善**
   - 添加 frontmatter 标签
   - 根据内容生成分类标签
   - 添加状态和优先级标签

4. **表格格式优化**
   - 统一对齐格式
   - 添加适当的 emoji 增强可读性
```

#### 3.2 Vault 发布

```markdown
1. 如果用户指定 vault_path 和 note_folder，将最终 Markdown 保存到该目录。
2. 如果未指定，保存到 `${PROJECT_DIR}/output/final_note.md`。
3. 发布前不要覆盖同名文件；除非 publish_mode 为 overwrite 或 patch。
```

#### 3.3 MOC 同步

```markdown
如果用户提供 moc_path，调用 `moc-organizer`：
- 将新笔记以 `[[笔记标题]] - 一句话说明 #tag` 加入 MOC
- 已存在则更新摘要/标签
- 不复制正文
```

### Step 4: 验证美化效果

```markdown
## 美化验证清单

### Callout 块
- [ ] 核心概念已用 `[!note]` 包装
- [ ] 实用技巧已用 `[!tip]` 标记
- [ ] 注意事项已用 `[!warning]` 标记

### 双链
- [ ] 关键概念已添加双链
- [ ] 链接目标存在且有效
- [ ] 提供了链接上下文

### 标签
- [ ] frontmatter 标签完整
- [ ] 分类标签准确
- [ ] 标签层级清晰

### 发布位置
- [ ] 已保存到用户指定位置，或项目 output
- [ ] 未误写到未确认 vault

### MOC（如适用）
- [ ] 新笔记已加入 MOC
- [ ] 未复制正文
```

### Step 5: 生成美化报告

```markdown
## ✅ Obsidian 笔记美化完成

### 文件信息
- 文件: Python学习笔记.md
- 美化时间: 2024-01-15 14:30

### 执行任务
| 任务 | 状态 |
|:-----|:-----|
| Callout 优化 | ✅ |
| 双链添加 | ✅ |
| frontmatter/标签完善 | ✅ |
| 保存到用户指定位置 | ✅ |
| MOC 同步 | ✅ |

### 美化内容
| 美化项 | 数量 | 说明 |
|:-------|:-----|:-----|
| Callout 块 | +5 | 核心概念、技巧、注意事项 |
| 双链 | +8 | 相关概念、扩展阅读 |
| 标签 | +4 | 分类标签、优先级标签 |
| MOC 索引 | +1 | 加入目录型笔记 |

### 美化效果
- ✅ 内容层次更清晰
- ✅ 核心概念更突出
- ✅ 知识关联更紧密
- ✅ 视觉效果更美观

### 文件位置
- 原始文件: `${PROJECT_DIR}/output/final_note.md`
- 美化后: `{用户指定路径 或 PROJECT_DIR/output/final_note.md}`

### 后续建议
1. 在 Obsidian 中预览确认效果
2. 根据需要微调美化内容
3. 保持标签系统一致性
```

**Update todo.md status after beautification:**
```bash
# Mark Phase 6 as complete (all phases done!)
.claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" complete P6
```

## 美化模板库

> **注意**: 本项目直接按 `.claude/rules/obsidian/note-system.md` 执行 Obsidian Markdown 规则，不依赖全局 Obsidian 插件技能。

### 美化方案模板

#### 学习笔记美化方案
```yaml
美化重点:
  - Callout: 核心概念、实用技巧、注意事项
  - 双链: 相关概念、扩展阅读
  - 标签: 学习、学科、难度等级
  - MOC: 目录索引

处理:
  - Callout、双链、标签、frontmatter、MOC
```

#### 读书笔记美化方案
```yaml
美化重点:
  - Callout: 核心观点、章节要点、个人思考
  - 表格: 书籍信息、章节对比
  - 标签: 读书、书名、作者
  - 任务列表: 阅读进度

处理:
  - Callout、表格、任务列表、frontmatter
```

#### 项目笔记美化方案
```yaml
美化重点:
  - Callout: 项目简介、模块说明、技术决策
  - 表格: 项目信息、进度追踪
  - 标签: 项目、技术栈、状态
  - 代码块: 项目结构、核心代码

处理:
  - Callout、表格、代码块、frontmatter
```

## 美化规则

> **重要**: 以下规则由本项目直接执行，详见 `.claude/rules/obsidian/note-system.md`。

### 1. Callout 使用规范

**适用场景**:
- `[!note]` - 概念定义、重要说明
- `[!tip]` - 实用技巧、经验分享
- `[!warning]` - 注意事项、常见错误
- `[!example]` - 示例说明、代码演示
- `[!abstract]` - 核心摘要、总结提炼
- `[!question]` - 思考问题、讨论点

### 2. 双链使用规范

**适用场景**:
- 相关概念引用
- 知识网络构建
- 扩展阅读链接
- 脚注和补充说明

### 3. 标签使用规范

**标签结构**:
```yaml
主标签:
  - 学习
  - 项目
  - 读书
  - 工作

子标签:
  - {学科}/{具体领域}
  - {项目名}/{模块}
  - {书名}/{章节}

状态标签:
  - 进行中
  - 已完成
  - 待复习
  - 暂停

优先级标签:
  - 重要
  - 紧急
  - 普通
```

## 与其他技能的关系

note-beautifier 是 Obsidian 发布阶段（阶段 6），接收 note-assembler 的输出，并可触发阶段 7 的 MOC 同步：

```
note-assembler (阶段 5 - 组装)
    ↓ 输出 output/final_note.md
note-beautifier (本技能 - 阶段 6)
    ↓ 应用 Obsidian Markdown 规则
    ↓ 保存到用户指定位置或项目 output
    ↓
moc-organizer (阶段 7，可选/按用户配置)
```

## 调用示例

### 示例 1: 美化学习笔记

```markdown
用户：帮我美化这个学习笔记

助手：
1. 读取笔记内容
2. 分析笔记类型（学习笔记，多代码块）
3. 生成美化方案
4. 优化 Callout 块
5. 添加高价值双链
6. 完善 frontmatter 和标签
7. 保存到用户指定位置
8. 如提供 MOC，同步索引
9. 生成美化报告
```

### 示例 2: 美化读书笔记

```markdown
用户：优化这个读书笔记的格式

助手：
1. 读取笔记内容
2. 分析笔记类型（读书笔记，章节结构）
3. 生成美化方案
4. 优化 Callout 块
5. 完善表格格式
6. 添加任务列表
7. 保存到用户指定位置
8. 生成美化报告
```
