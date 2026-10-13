---
workflow_id: learning-note-flow
workflow_name: 学习笔记工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "rea-reverse-engineering"
task: "REA: Reverse Engineer Anything（morluto/rea，把逆向工程能力通过 MCP/CLI 接给 AI agent 的工具）"
created_from: ".claude/workflows/learning-note-flow/state-template.md"
topic: "REA: Reverse Engineer Anything（morluto/rea，把逆向工程能力通过 MCP/CLI 接给 AI agent 的工具）"
project_slug: "rea-reverse-engineering"
created_at: "2026-10-13"
last_updated: "2026-10-13"
current_phase: done
current_status: complete
mode: "outline"
blocked_reason: ""
quality_gate: passed
quality_gate_owner: ""
quality_gate_due: ""
---

# 学习笔记工作流 - 执行检查清单

> 工作流：learning-note-flow
> 主题：REA: Reverse Engineer Anything（morluto/rea，把逆向工程能力通过 MCP/CLI 接给 AI agent 的工具）
> 运行标识：rea-reverse-engineering
> 项目标识：rea-reverse-engineering
> 创建时间：2026-10-13
> 当前阶段：完成
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
- [ ] 第 1 章已写完并确认
- [ ] 第 2 章已写完并确认
- [ ] 第 3 章已写完并确认
- [ ] ...（根据实际章节数添加）
- [ ] 并行写作 ≥2 章时：已冻结跨章口径表并写进每个 dispatch
- [ ] 全部章节交付后：已做跨章一致性比对三类全覆盖（可照抄的配置块 / 同一来源的散文式转述与定性 / 定义与判据句对冻结语义框架自洽）

**进度**：0/待大纲确定

> [P4] ✅ 已完成 {complete}

---

## 阶段 5：收尾组装
- [ ] 所有章节文件已检查
- [ ] 组装方式已确认（A: 按顺序拼接 / B: 重新排序 / C: 保持零散）
- [ ] 过渡语已添加
- [ ] 目录已生成
- [ ] 标题层级已统一
- [ ] 引用已检查
- [ ] 完整笔记已保存：`./output/final_note.md`

> [P5] ✅ 已完成 {complete}

---

## 阶段 6：Obsidian 美化与发布
- [ ] 已读取 Obsidian 输出规则
- [ ] 用户已确认最终保存位置（vault_path + note_folder，或仅项目 output）
- [ ] frontmatter、标签、Callout、双链已按 Obsidian 规则处理
- [ ] 最终 Markdown 已保存到用户指定位置或 `./output/final_note.md`

> [P6] ✅ 已完成 {complete}

---

## 阶段 7：MOC 同步
- [ ] 已定位或创建 MOC 文件
- [ ] 新笔记双链已加入 MOC
- [ ] 已去重并更新摘要/标签
- [ ] MOC 只保留索引，不复制正文

> [P7] ✅ 已完成 {complete}

---

## 用户确认记录

| 阶段 | 确认内容 | 时间 |
|------|----------|------|
| P7 | MOC 同步完成：AI学习/REA 逆向工程/REA 逆向工程 MOC.md 建立并登记入父级 AI学习/00-索引/AI学习 MOC.md（新增分节 + mermaid 目录节点）；索引仅一行、无正文复制 | 2026-10-13 19:52 |
| P6 | P6 分册发布完成：vault 新建 AI学习/REA 逆向工程/（MOC + 8 章 + sortspec）；逐字一致断言/结构自检/引文校验(V+S+C,11副本0差异)/校验器自检 7 用例 全绿 | 2026-10-13 19:51 |
| P5 | 组装确认：8 章顺序拼接为 output/final_note.md（20319 字/95KB）；目录+标题层级统一；引文 46/46、多副本 C 0 差异、结构 0 可疑。发布方式选 ②B 拆分到 vault AI学习/REA 逆向工程入门/ | 2026-10-13 19:47 |
| P4 | 全 8 章交付确认通过（20144 字）；引文逐字回源 46/46、结构自检 0 可疑、跨章一致性三类全覆盖完成 | 2026-10-13 19:41 |
| P3 | 大纲确认：8 章/约2.0万字/两实战独立章/正式第8章；命令保留原文+加 macOS 提示；进阶三件套轻量处理 | 2026-10-13 18:58 |
| P2 | 方向 C 深度收集完成：22 目标表/接入/两条零引擎实战/provider 限制/安全边界，引文逐字回源 29/29 | 2026-10-13 17:48 |
| P1 | 用户选择方向 C：概念+实战混合（与 00_intent 一致） | 2026-10-13 17:42 |
| P0 | 用户采纳推荐默认：入门→上手/概念+实战、零基础会命令行、先写项目 output、走零原生引擎实战路径 | 2026-10-13 17:39 |

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

> **取数纪律**：下表的体积 / 字数 / 章数 / 锚点数 / Callout 数必须**当场重新运行取数或重新计数**，并把命令留在「取数命令」一行；不要从上下文里的历史输出誊抄，也不要手算合计。产物在记录之后又被改动时，grep 同一数字的**所有**出现处一并更新（同一组数字常同时出现在阶段段落与本节）。

- **笔记类型**：概念 + 实战混合（含速查附录）
- **总字数**：正文 `final_note.md` 20319 汉字（约 2.0 万字）；vault 分册 8 章合计 20542 汉字（含各章 frontmatter/导航行）
- **章节数**：8
- **输出格式**：Markdown（Obsidian）；分册 = MOC + 8 章 + sortspec
- **取数命令**：`python3.12 -c "import re,os;print(len(re.findall(r'[一-鿿]',open('workspace/rea-reverse-engineering/output/final_note.md',encoding='utf-8').read())))"`；分册逐文件同一正则求和
- **文件路径**：`workspace/rea-reverse-engineering/output/final_note.md`（组装稿）；`workspace/rea-reverse-engineering/chapters/*.md`（分章源）
- **Obsidian Vault**：`/Users/zhqznc/Documents/项目`（本仓库即 vault）
- **MOC 路径**：`AI学习/REA 逆向工程/REA 逆向工程 MOC.md`（本主题 MOC）；已登记入父级 `AI学习/00-索引/AI学习 MOC.md`
