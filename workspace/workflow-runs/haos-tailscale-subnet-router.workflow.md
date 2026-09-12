---
workflow_id: learning-note-flow
workflow_name: 学习笔记工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "haos-tailscale-subnet-router"
task: "如何用 HAOS 部署的 Home Assistant 中的 Tailscale 插件实现内网穿透和子路由（Subnet Router）"
created_from: ".claude/workflows/learning-note-flow/state-template.md"
topic: "如何用 HAOS 部署的 Home Assistant 中的 Tailscale 插件实现内网穿透和子路由（Subnet Router）"
project_slug: "haos-tailscale-subnet-router"
created_at: "2026-09-12"
last_updated: "2026-09-12"
current_phase: P3
current_status: in_progress
mode: outline
blocked_reason: ""
quality_gate: pending
quality_gate_owner: ""
quality_gate_due: ""
---

# 学习笔记工作流 - 执行检查清单

> 工作流：learning-note-flow
> 主题：如何用 HAOS 部署的 Home Assistant 中的 Tailscale 插件实现内网穿透和子路由（Subnet Router）
> 运行标识：haos-tailscale-subnet-router
> 项目标识：haos-tailscale-subnet-router
> 创建时间：2026-09-12
> 当前阶段：阶段 3
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
- [x] 已派出 2-3 个 subagent 并行探测（3 lens × 1 subagent，2026-09-12）
- [x] 探测结果已汇总（55 条 → 去重 46 条：官方 15 / 一手 issue 8 / 社区实操 14 / 博客 9）
- [x] 方向菜单已展示给用户（A 全链路主线 / B 聚焦子路由边界 / C 排错优先 / A+C 组合）
- [x] 用户已选择学习方向（方向 A：全链路实战主线；补充环境：标准 192.168.1.0/24 单层路由，HAOS 主机与目标设备同网段）
- [x] 探测结果已保存：`./01_explore_result.md`

> [P1] ✅ 已完成 {complete}

---

## 阶段 2：深度收集
- [x] 已根据用户选择的方向启动深度收集（方向 A 全链路主线；14 个核心 URL 投喂 crawl4ai）
- [x] 核心概念/理论素材已收集（路由注入四条件、SNAT 语义、userspace 两种模式、tailnet/CGNAT）
- [x] 实战代码/项目案例已收集（插件完整 YAML 默认值 + 同网段推荐配置；Serve 前置设置）
- [x] 常见坑/最佳实践已收集（三条「别照抄」警告；snat=false 的两个失败复现）
- [x] 工具链/生态已收集（`ha dns options`、`tailscale debug prefs/netmap`、`tailscale set --accept-routes`、管理端 Edit route settings）
- [x] 进阶路径/学习资源已收集（site-to-site 五条件、exit node、Tailscale Services、Taildrop/Taildrive）
- [x] 素材质量已确认（官方文档数、教程数、深度文章数）——用户已确认，12 条成功素材质量足够
- [x] 深度素材已保存：`./02_deep_research.md`

**P2 采集结果**：14 个 URL → 12 条成功（T1 官方 5 / T2 维护者与一手复现 3 / T3 社区 4）+ 2 条失败（S13 Cloudflare 反爬、S14 404，已派后台恢复任务，结果未回）。
**争议收敛**：同网段场景 → 保持 `snat_subnet_routes: true`（默认值）；关 SNAT 属进阶 site-to-site，需额外补 `100.64.0.0/10` 回程路由。

> [P2] ✅ 已完成 {complete}

---

## 阶段 3：大纲生成（大纲模式）
- [ ] 已读取意图文件和深度素材
- [ ] 已根据笔记类型选择大纲结构
- [ ] 大纲已生成（≤3级层级）
- [ ] 每章已标注：篇幅、素材引用、代码示例
- [ ] 大纲已展示给用户确认
- [ ] 大纲已保存：`./03_outline.md`

> [P3] 🔲 进行中 {in_progress}

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
| P0 | 确认意图文件与研究计划：笔记类型=实战笔记（可直接照做），深度=上手，基础=零基础（尚未安装 Tailscale 插件，从零开始）；四个探索方向（插件安装授权 / 内网穿透 / 子路由 / 验证排错）无需增删；输出=项目 output，阶段 6 再定 Obsidian 位置；阶段 7 需同步 MOC | 2026-09-12 |
| P1 | 确认 P1 探测结果（46 条去重来源）并选择 P2 方向：**方向 A 全链路实战主线**（安装授权 → 内网穿透 → 子路由 → 排错清单）；补充环境：标准 `192.168.1.0/24` 单层路由，**HAOS 主机网段 = 要访问的网段**（同网段场景，需重点回答 SNAT 与否） | 2026-09-12 |
| P2 | 确认 P2 深度素材质量（12 条成功来源，T1 官方 5 / T2 维护者 3 / T3 社区 4；2 条失败已记录原因）。接受争议收敛结论：同网段场景保持 `snat_subnet_routes: true`；接受 G1–G3 三条未核验标记不写入正文 | 2026-09-12 |

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
