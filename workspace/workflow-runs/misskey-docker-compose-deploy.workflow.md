---
workflow_id: learning-note-flow
workflow_name: 学习笔记工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "misskey-docker-compose-deploy"
task: "使用 Docker Compose 部署 Misskey"
created_from: ".claude/workflows/learning-note-flow/state-template.md"
topic: "使用 Docker Compose 部署 Misskey"
project_slug: "misskey-docker-compose-deploy"
created_at: "2026-09-15"
last_updated: "2026-09-15"
current_phase: P7
current_status: ready
mode: outline
blocked_reason: ""
quality_gate: pending
quality_gate_owner: ""
quality_gate_due: ""
---

# 学习笔记工作流 - 执行检查清单

> 工作流：learning-note-flow
> 主题：使用 Docker Compose 部署 Misskey
> 运行标识：misskey-docker-compose-deploy
> 项目标识：misskey-docker-compose-deploy
> 创建时间：2026-09-15
> 当前阶段：阶段 7
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
- [ ] 已派出 2-3 个 subagent 并行探测
- [ ] 探测结果已汇总
- [ ] 方向菜单已展示给用户
- [ ] 用户已选择学习方向
- [ ] 探测结果已保存：`./01_explore_result.md`

> [P1] ✅ 已完成 {complete}

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

> [P2] ✅ 已完成 {complete}

---

## 阶段 3：大纲生成（大纲模式）
- [ ] 已读取意图文件和深度素材
- [ ] 已根据笔记类型选择大纲结构
- [ ] 大纲已生成（≤3级层级）
- [ ] 每章已标注：篇幅、素材引用、代码示例
- [ ] 大纲已展示给用户确认
- [ ] 大纲已保存：`./03_outline.md`

> [P3] ✅ 已完成 {complete}

---

## 阶段 4：逐章写作
- [x] 第 1 章已写完并确认 —— 部署前置与三份产物落位
- [x] 第 2 章已写完并确认 —— `compose.yml`：服务栈、依赖顺序、网络与挂载
- [x] 第 3 章已写完并确认 —— `.config/default.yml`：应用配置必改字段与不可变项
- [x] 第 4 章已写完并确认 —— `.config/docker.env`：数据库口令与变量注入
- [x] 第 5 章已写完并确认 —— 构建 → 初始化 → 启动：跑通链路
- [x] 第 6 章已写完并确认 —— 升级流程与 NAS 遗留约束

**进度**：6/6

> [P4] ✅ 已完成 {complete}

---

## 阶段 5：收尾组装
- [x] 所有章节文件已检查
- [x] 组装方式已确认（A: 按顺序拼接 / B: 重新排序 / C: 保持零散）
- [x] 过渡语已添加
- [x] 目录已生成
- [x] 标题层级已统一
- [x] 引用已检查
- [x] 完整笔记已保存：`./output/final_note.md`

> [P5] ✅ 已完成 {complete}

---

## 阶段 6：Obsidian 美化与发布
- [x] 已读取 Obsidian 输出规则
- [x] 用户已确认最终保存位置（vault_path + note_folder，或仅项目 output）
- [x] frontmatter、标签、Callout、双链已按 Obsidian 规则处理
- [x] 最终 Markdown 已保存到用户指定位置或 `./output/final_note.md`

> [P6] ✅ 已完成 {complete}

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
| P0 | 深度＝跑通+关键配置；基础＝有了解；环境＝NAS/自建（x86_64）；输出＝先放项目 output | 2026-09-15 |
| P2 | 范围＝A（最小闭环）+ C（NAS 与运维）；移除 S3 与邮件 | 2026-09-15 |
| P3 | 大纲确认，开始逐章写 | 2026-09-15 |
| P4 | 「全部写完」——确认第 1 章，并授权一次写完第 2–6 章（覆盖原「逐章确认」门） | 2026-09-15 |

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

- **笔记类型**：实战（部署跑通 + NAS 运维）
- **总字数**：约 7.7 万字符（中文按字符计；2025 行）
- **章节数**：6
- **输出格式**：Obsidian Markdown（frontmatter + Callout + 双链 + 脚注）
- **文件路径**：`workspace/output/final_note.md`
- **Obsidian Vault**：待用户指定（当前工作目录本身即 vault 根，候选目录 `docker/`）
- **MOC 路径**：待用户指定（vault 内已有 `docker/Docker MOC.md`）
