# Agent 调用规范

## 现有 Agent 列表

| Agent | 用途 | 调用方式 |
|-------|------|----------|
| `outline-generator` | 生成学习笔记大纲 | 读取 `.claude/agents/outline-generator.md` 后执行，或派发 subagent |
| `chapter-writer` | 逐章写作学习笔记 | 读取 `.claude/agents/chapter-writer.md` 后执行，或派发 subagent |
| `note-assembler` | 组装章节成完整笔记 | 读取 `.claude/agents/note-assembler.md` 后执行，或派发 subagent |

## 调用流程

```
用户输入学习主题
    │
    ▼
[环节 1] 资料收集 (skill: research-collector)
    │
    ▼
02_deep_research.md 生成
    │
    ▼
[环节 2] 大纲生成 (agent: outline-generator)
    │
    ▼
03_outline.md 生成 + 用户确认
    │
    ▼
[环节 3] 逐章写作 (agent: chapter-writer)
    │
    ▼
chapters/ 目录下的章节文件
    │
    ▼
[环节 4] 笔记组装 (agent: note-assembler)
    │
    ▼
output/final_note.md
```

## Agent 调用详情

### 1. outline-generator

**触发条件**：
- 用户说"素材收集完了，帮我生成大纲"
- 用户说"根据资料整理大纲"
- 用户说"生成大纲吧"
- 02_deep_research.md 已就绪

**前置依赖**：
- `${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/00_intent.md` ✅
- `${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/02_deep_research.md` ✅

**输出文件**：
- `${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/03_outline.md`

**调用示例**：
```markdown
用户：素材收集完了，帮我生成大纲
助手：我来使用 outline-generator agent，基于你的研究素材生成学习大纲。
```

**等待用户确认**：生成后需等待用户确认大纲顺序和深度

---

### 2. chapter-writer

**触发条件**：
- 用户说"逐章写作"
- 用户说"按大纲写笔记"
- 用户说"写第 N 章"
- 用户说"开始写学习笔记"
- 大纲已确认完成

**前置依赖**：
- `${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/00_intent.md` ✅
- `${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/02_deep_research.md` ✅
- `${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/03_outline.md` ✅

**输出文件**：
- `${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/chapters/{N}_{章节名}.md`

**调用示例**：
```markdown
用户：大纲已经好了，开始逐章写作吧，先从第1章开始
助手：我来使用 chapter-writer agent 开始写第1章。
```

**重要规则**：
- 每次只写一章，写完后等待用户确认
- 用户确认后才继续下一章
- 支持中途调整方向

---

### 3. note-assembler

**触发条件**：
- 用户说"所有章节都写完了，帮我组装成完整的笔记"
- 用户说"把章节合并一下，加上目录"
- 用户说"笔记写得差不多了，帮我整理成最终版本"

**前置依赖**：
- `${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/chapters/` 目录下有章节文件 ✅
- `${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/00_intent.md` ✅
- `${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/03_outline.md` (可选)

**输出文件**：
- `${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/output/final_note.md`

**调用示例**：
```markdown
用户：所有章节都写完了，帮我组装成完整的笔记
助手：我来使用 note-assembler agent，将所有章节组装成完整的笔记。
```

**组装选项**：
- A: 按当前顺序拼成随笔笔记
- B: 重新排序整理成结构化笔记
- C: 保持零散片段，仅加最小格式

## 调用规则

### ✅ 正确调用

```markdown
# 按流程调用
1. 先确认 02_deep_research.md 存在
2. 调用 /outline-generator 生成大纲
3. 等待用户确认大纲
4. 调用 /chapter-writer 逐章写作
5. 每章写完等待确认
6. 所有章节完成后调用 /note-assembler
```

### ❌ 错误调用

```markdown
# 缺少前置条件
直接调用 /chapter-writer 而没有大纲

# 跳过确认
生成大纲后直接开始写章节，不等用户确认

# 顺序颠倒
先写章节再生成大纲
```

## 错误处理

| 错误情况 | 处理方式 |
|----------|----------|
| 缺少 02_deep_research.md | 提示用户先完成资料收集 |
| 缺少 03_outline.md | 提示用户先生成大纲 |
| 缺少章节文件 | 提示用户先完成章节写作 |
| 大纲未确认 | 等待用户确认后再继续 |

## 与其他技能协作

| 技能 | 协作方式 |
|------|----------|
| `research-collector` | 提供 02_deep_research.md 作为输入 |
| `note-beautifier` | 处理 final_note.md 为 Obsidian Markdown 并发布到用户指定位置 |
| `workflow-orchestrator` | 编排整个流程 |

---

## 维护规则

### 更新时机

**必须更新本文件的情况**：
1. 添加新的 agent 到 `.claude/agents/` 目录
2. 删除或重命名现有 agent
3. 修改 agent 的触发条件或前置依赖
4. 调整 agent 的调用顺序或流程

### 更新步骤

当添加新 agent 时：

1. **读取 agent 定义文件**
   ```bash
   cat .claude/agents/{agent-name}.md
   ```

2. **提取关键信息**
   - name (名称)
   - description (触发条件和示例)
   - tools (可用工具)
   - 前置依赖文件
   - 输出文件

3. **更新本文件**
   - 在"现有 Agent 列表"表格中添加新行
   - 在"Agent 调用详情"中添加新章节
   - 更新"调用流程"图（如需要）
   - 更新"与其他技能协作"表格（如需要）

4. **检查依赖关系**
   - 新 agent 是否依赖其他 agent 的输出？
   - 其他 agent 是否需要新 agent 的输出？
   - 更新相关的错误处理表格

### 检查清单

添加新 agent 后，确认以下项目：

- [ ] Agent 列表表格已更新
- [ ] Agent 调用详情章节已添加
- [ ] 触发条件已列出
- [ ] 前置依赖已明确
- [ ] 输出文件已说明
- [ ] 调用示例已添加
- [ ] 调用流程图已更新（如适用）
- [ ] 错误处理表格已更新（如适用）
- [ ] 与其他技能协作表格已更新（如适用）

### 文件位置

- Agent 定义：`.claude/agents/*.md`
- 调用规范：`.claude/rules/common/agent-invocation.md`

### 示例：添加新 agent

假设添加一个 `review-agent` 用于审查笔记质量：

```markdown
## 现有 Agent 列表

| Agent | 用途 | 调用方式 |
|-------|------|----------|
| `outline-generator` | 生成学习笔记大纲 | `/outline-generator` |
| `chapter-writer` | 逐章写作学习笔记 | `/chapter-writer` |
| `note-assembler` | 组装章节成完整笔记 | `/note-assembler` |
| `review-agent` | 审查笔记质量 | `/review-agent` |  ← 新增

## Agent 调用详情

### 4. review-agent

**触发条件**：
- 用户说"帮我审查一下笔记质量"
- 用户说"检查一下有没有问题"
- 笔记组装完成后

**前置依赖**：
- `${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/output/final_note.md` ✅

**输出文件**：
- `${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/output/review_report.md`

**调用示例**：
```markdown
用户：帮我审查一下笔记质量
助手：我来使用 review-agent agent，审查笔记的质量和完整性。
```

**审查维度**：
- 内容完整性
- 格式一致性
- 引用准确性
- 代码示例正确性
```
