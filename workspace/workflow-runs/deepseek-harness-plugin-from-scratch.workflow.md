---
workflow_id: learning-note-flow
workflow_name: 学习笔记工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "deepseek-harness-plugin-from-scratch"
task: "DeepSeek-Harness 从零写插件（空目录手写全文件）"
created_from: ".claude/workflows/learning-note-flow/state-template.md"
topic: "DeepSeek-Harness 从零写插件（空目录手写全文件）"
project_slug: "deepseek-harness-plugin-from-scratch"
created_at: "2026-08-15"
last_updated: "2026-08-15"
current_phase: P1
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
> 主题：DeepSeek-Harness 从零写插件（空目录手写全文件）
> 运行标识：deepseek-harness-plugin-from-scratch
> 项目标识：deepseek-harness-plugin-from-scratch
> 创建时间：2026-08-15
> 当前阶段：阶段 1
> 状态图例：⬜ 未开始 | 🔲 进行中 | ✅ 已完成 | ⏭️ 跳过

---

## 阶段 0：意图澄清
- [x] 用户输入已分析（「写一个新的，从零开始」）
- [x] 笔记类型已确定（实战教学分册 / learning-note）
- [x] 学习深度已确定（上手：写→配→验证→打包→安装）
- [x] 用户基础已确定（有了解：理论已读、源码环境已跑通、读过《插件实战》）
- [x] 输出位置策略已确定（Obsidian vault：AI学习/DeepSeek-Harness 教程/）
- [x] 如发布到 Obsidian，vault_path、note_folder、moc_path 已确认（AI学习 / DeepSeek-Harness 教程 / DeepSeek-Harness MOC.md）
- [x] 意图文件已生成：`./00_intent.md`

> [P0] ✅ 已完成 {complete}

---

## 阶段 1：探测式收集
- [ ] 已派出 2-3 个 subagent 并行探测
- [ ] 探测结果已汇总
- [ ] 方向菜单已展示给用户
- [ ] 用户已选择学习方向
- [ ] 探测结果已保存：`./01_explore_result.md`

> [P1] 🔲 进行中 {in_progress}

---

## 阶段 2：深度收集
- [ ] 已根据用户选择的方向启动深度收集
- [ ] 核心概念/理论素材已收集
- [ ] 实战代码/项目案例已收集
- [ ] 常见坑/最佳实践已收集
- [ ] 工具链/生态已收集
- [ ] 进阶路径/学习资源已收集
- [ ] 素材质量已确认（官方文档数、教程数、深度文章数）
- [ ] 深度素材已保存：`./02_deep_research.md`

> [P2] ⬜ 未开始

---

## 阶段 3：大纲生成（大纲模式）
- [ ] 已读取意图文件和深度素材
- [ ] 已根据笔记类型选择大纲结构
- [ ] 大纲已生成（≤3级层级）
- [ ] 每章已标注：篇幅、素材引用、代码示例
- [ ] 大纲已展示给用户确认
- [ ] 大纲已保存：`./03_outline.md`

> [P3] ⬜ 未开始

---

## 阶段 4：逐章写作
- [ ] 第 1 章已写完并确认
- [ ] 第 2 章已写完并确认
- [ ] 第 3 章已写完并确认
- [ ] ...（根据实际章节数添加）

**进度**：0/待大纲确定

> [P4] ⬜ 未开始

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
| P0 | 用户确认意图：新写一篇「从零写 dsh 插件」教学分册；「从零」=空目录手写所有文件、不用 example-plugin 脚手架；Obsidian 输出到 AI学习/DeepSeek-Harness 教程/；示范工具沿用 git_log 与《插件实战》可对照 | 2026-08-15 |

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
