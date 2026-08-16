---
workflow_id: learning-note-flow
workflow_name: 学习笔记工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "deepseek-harness-hook-plugin"
task: "如何写 DeepSeek-Harness hook 扩展点插件"
created_from: ".claude/workflows/learning-note-flow/state-template.md"
topic: "如何写 DeepSeek-Harness hook 扩展点插件"
project_slug: "deepseek-harness-hook-plugin"
created_at: "2026-08-16"
last_updated: "2026-08-16"
current_phase: P4
current_status: in_progress
mode: outline
confirmed_phases: ""
skippable_phases: "P7"
mode_dependent_skips: "P3,P4"
allowed_modes: "outline,freeform"
mode_change_phase: "P2"
blocked_reason: ""
---

# 学习笔记工作流 - 执行检查清单

> 工作流：learning-note-flow
> 主题：如何写 DeepSeek-Harness hook 扩展点插件
> 运行标识：deepseek-harness-hook-plugin
> 项目标识：deepseek-harness-hook-plugin
> 创建时间：2026-08-16
> 当前阶段：阶段 4
> 状态图例：⬜ 未开始 | 🔲 进行中 | ✅ 已完成 | ⏭️ 跳过

---

## 阶段 0：意图澄清
- [ ] 用户输入已分析
- [ ] 笔记类型已确定（实战/概念/心得/对比）
- [ ] 学习深度已确定（入门/上手/精通）
- [ ] 用户基础已确定（零基础/有了解/熟悉）
- [ ] 输出位置策略已确定（项目 output / 用户指定 Obsidian vault）
- [ ] 如发布到 Obsidian，vault_path、note_folder、moc_path 已确认或标记待补
- [ ] 意图文件已生成：`./00_intent.md`

> [P0] ✅ 已完成 {complete}

---

## 阶段 1：探测式收集
- [x] 已派出 2-3 个 subagent 并行探测（3 透镜：语义模型 / 实战代码 / 迁移对照）
- [x] 探测结果已汇总（去重后 9 源：5 官方 + 4 社区；确认 github.io 镜像 404，docs 以仓库内 raw 路径为准）
- [x] 方向菜单已展示给用户（A 语义模型 / B 实战 / C 迁移对照 / D 组合）
- [x] 用户已选择学习方向（D. 组合 A→B→C）
- [x] 探测结果已保存：`./01_explore_result.md`

> [P1] ✅ 已完成 {complete}

---

## 阶段 2：深度收集
- [x] 已根据用户选择的方向启动深度收集（D 组合 A→B→C，3 并行深研代理）
- [x] 核心概念/理论素材已收集（流水线顺序 + 5 扩展点语义 + PreToolDecision/PostToolDecision）
- [x] 实战代码/项目案例已收集（S2 permission-gate 官方示例 + S7 dsh-guardian 佐证；guard/post-execute/result 无官方示例→标注依 S1 构造）
- [x] 常见坑/最佳实践已收集（pre-execute 不能改 exec.arguments；guard 单调否决；CC updatedInput 无对应能力；验证链复用 08 章）
- [x] 工具链/生态已收集（dsh-hooks-claude-code 桥、@deepseek-ai/dsh-tools 类型、DSH 0.1.0-rc.6）
- [x] 进阶路径/学习资源已收集（S2 选择规则 + S7 社区样板 + 开放问题 4 项）
- [x] 素材质量已确认（9 源：5 官方 + 4 社区；6 核心深读带锚点；2 矛盾已记录）
- [x] 深度素材已保存：`./02_deep_research.md`

> [P2] ✅ 已完成 {complete}

---

## 阶段 3：大纲生成（大纲模式）
- [x] 已读取意图文件和深度素材（00_intent.md + 02_deep_research.md + 系列 README 与 01 章格式参照）
- [x] 已根据笔记类型选择大纲结构（实战教学分册，方向 D：A 语义模型→B 实战→C 迁移对照）
- [x] 大纲已生成（≤3级层级，8 内部章 `### 第 N 章`）
- [x] 每章已标注：篇幅、素材引用、代码示例（篇幅占比 5–20%，素材 S1–S9，代码示例标注）
- [x] 大纲已展示给用户确认（用户授权「直接写完」）
- [x] 大纲已保存：`./03_outline.md`

> [P3] ✅ 已完成 {complete}

---

## 阶段 4：逐章写作
- [ ] 第 1 章已写完并确认
- [ ] 第 2 章已写完并确认
- [ ] 第 3 章已写完并确认
- [ ] ...（根据实际章节数添加）

**进度**：0/8

> [P4] 🔲 进行中 {in_progress}

---

## 阶段 5：收尾组装
- [ ] 所有章节文件已检查
- [ ] 组装方式已确认（A: 按顺序拼接 / B: 重新排序 / C: 保持零散）
- [ ] 过渡语已添加
- [ ] 目录已生成
- [ ] 标题层级已统一
- [ ] 引用已检查
- [ ] 完整笔记已保存：`./output/final_note.md`

> [P5] ⬜ 未开始

---

## 阶段 6：Obsidian 美化与发布
- [ ] 已读取 Obsidian 输出规则
- [ ] 用户已确认最终保存位置（vault_path + note_folder，或仅项目 output）
- [ ] frontmatter、标签、Callout、双链已按 Obsidian 规则处理
- [ ] 最终 Markdown 已保存到用户指定位置或 `./output/final_note.md`

> [P6] ⬜ 未开始

---

## 阶段 7：MOC 同步
- [ ] 已定位或创建 MOC 文件
- [ ] 新笔记双链已加入 MOC
- [ ] 已去重并更新摘要/标签
- [ ] MOC 只保留索引，不复制正文

> [P7] ⬜ 未开始

---

## 用户确认记录

| 阶段 | 确认内容 | 时间 |
|------|----------|------|
| P0 | 用户确认意图文件与研究计划：如何写 dsh hook 扩展点插件（实战·上手·中量 12-15k 字·Obsidian 发布到插件开发教程分册·MOC 同步） | 2026-08-16 |
| P1 | 用户确认探测结果与方向：9 源（5 官方 + 4 社区）通过验证，选方向 D（组合 A→B→C：语义模型→实战→迁移对照） | 2026-08-16 |
| P2 | 用户确认深度素材质量（9 源 5官方+4社区，6 核心深读）并选择执行模式：大纲模式 | 2026-08-16 |
| P3 | 用户确认大纲（8 内部章，方向 D：语义模型→实战→迁移对照；guard/post-execute/result 依 S1 构造已标注）并授权「直接写完」不再逐章确认 | 2026-08-16 |

---

## 跳过记录

| 阶段 | 确认内容 | 原因 | 时间 |
|------|----------|------|------|
| | | | |

---

## 异常记录

| 时间 | 阶段 | 问题描述 | 处理方式 |
|------|------|---------|---------|
| | | | |

---

## 方向调整记录

| 时间 | 原方向 | 新方向 | 是否需要补充收集 |
|------|--------|--------|-----------------|
| | | | |

---

## 最终产出

- **笔记类型**：
- **总字数**：
- **章节数**：
- **输出格式**：
- **文件路径**：
- **Obsidian Vault**：
- **MOC 路径**：
