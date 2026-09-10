# Rules

Compressed, deduplicated learnings from past Study System sessions.
Read before starting any new Study System task.

## Do

- 长篇笔记（>30KB 或多于 3 章）组装后主动建议拆分：独立章节文件 + 前后导航双链 + MOC 索引页
- Phase 4 beautify 前主动询问用户是否需要 Canvas/Base 配置
- GitHub 项目类主题，先通过 API 获取基本信息再进 Phase 0 提问
- 混合笔记 concept + cheat_sheet 适合"入门+速查"场景
- 工具对比/迁移类主题优先用 practice + compare 混合类型，每个领域同时提供步骤指南和对比表
- 每个学习笔记为核心概念添加 `[!tip] 大白话` 通俗解释 + 打比方类比（临时工牌 / 门禁卡 / 保险箱 / 双保险 / 岗位说明书 / 料理包 / 千层饼 等）；写作新笔记与 update 旧笔记时都补，用户偏好（3x）
- 教程类笔记「一章一节一文件」：顶级小节对应一个文件/产物；同一文件的字段（package.json 的 name/deps/files 等）收进该文件小节的 `####` 子节，不升格为顶级小节
- 教程代码块用文件头注释标注所属路径，并先展示完整文件（先睹为快）再逐段拆讲
- 用户报命令/路径错误时，先读源码核实路径解析基准与文件真实位置，一次改对再写入笔记；改完全文 grep 确认无残留旧表述
- 用户决策点用紧凑文本菜单 + 推荐默认值，不要用多问题 AskUserQuestion 对话框（用户会拒绝）
- 合并多篇独立章节前/后按章命名空间化脚注 ID（`[^cN-…]`），并 grep 校验无重复
- GitHub 项目取文档优先 `raw.githubusercontent.com/{owner}/{repo}/{branch}/...`；github.io 镜像可能 404
- 本机 `python3` **可用**（原生 CPython 3.14，非微软商店存根；2026-09-11 复核）——中文文本处理优先 python；若用 perl 兜底，必须 `use utf8;` + `use open ":std", ":encoding(UTF-8)"`，否则字符类正则静默 no-op
- 写 OpenWrt/iStoreOS 第三方插件安装步骤前，先用 GitHub API（`curl api.github.com/.../contents`、`/releases/tags/{tag}`）核实软件源 feed 内容与 release 真实文件名，再写命令；示例 URL 必须来自实际存在的文件
- 用户明确说「删掉」误导内容时，直接删除整节并重排编号，不要加 warning 补丁保留
- 解释抽象概念按「它是什么/解决什么问题 → 具体产物长什么样 → 带具体值的可代入例子（目录树/路径/命令输出）→ 对比表 → 大白话类比」落地；正文去掉类比后仍要能让「没懂」的读者靠表格/例子读懂，不只抛抽象结论（默认写作标准，用户当日连续两次明确要求「都要这样」）
- 给子 agent 派活时**不要转述来源论断**：只传来源 ID + 检索位置，要求「先回原文核对再落笔」；确需带结论必须成对标注（原文加引号 / 概述标「待核对」）。章节验收对每处「官方口径是 / 官方说明 / 原文」逐条回源比对，不只看有没有挂来源 ID
- 中文文本的组装、拆分、统计一律走 python（`re.findall(r'[一-鿿]', t)` 计字数）；批量文本改写脚本必须打印「本次改动 N 处」，N=0 时人工复核，不许静默通过

## Don't

- 不要把表格嵌套在列表项内（带缩进），Obsidian 无法渲染列表内的表格

## Domain

- GitHub Packages / GHCR 认证只支持 Classic PAT（`write:packages` 等 scope）；Fine-grained PAT 无 packages 权限项，遇到"expected scopes"报错先认 `github_pat_` 前缀换 classic

## Watch For

- YAML frontmatter 的 sources 字段中所有含特殊字符（`[]`, `:`）的值必须正确引用，否则 Obsidian 解析失败
- 并行派发 chapter-writer 时，章节过渡语必须自包含（按大纲），不要依赖读取上一章文件；`todo-state.sh` 只有 `start|complete|skip|block`（**没有 `confirm`**），固定走 `start PN` → `complete PN`；**最后一个阶段**还需 frontmatter 写 `quality_gate: passed`（走豁免则同时补 `quality_gate_owner` + `quality_gate_due`）
- note-assembler 等 writer 子 agent 无 Bash/Edit 且 Write 有输出上限；>100KB 长文档由父进程 python 合并；反向扫描定位插入点时必须**同时跳过空行和 `---` 分隔线**，否则扫描停错位置且静默不生效
- 并行子 agent 不得直接修改共享 workflow state file；状态推进由 orchestrator 集中经 todo-state.sh 处理
- P6 发布前校验最终产物并**建议**拆分：>30KB 或多于 3 章时给出「分册子目录 + README + 每章独立文件 + 前后导航 + MOC 指向 README」方案，但**用户明确选单文件就按单文件发布**（2026-09-11 一篇 43k 汉字 / 228KB 笔记经用户确认单文件落地，非违规）
- iStoreOS 官方 iStore 商店不含代理插件；Passwall SourceForge 源只含 passwall_luci/passwall_packages/passwall2（不含 OpenClash）；OpenClash `.run` 包 `+core` 表示内置内核
- WebFetch 拦截的域名（raw.githubusercontent.com、github.com）改用 `curl api.github.com` 替代
- 往 Obsidian 笔记加双链前，先核实目标笔记**真实存在**（逐条 `os.path.exists` 断言），不要给 vault 里不存在的概念词埋死链；章级锚点**避开含反引号/箭头/竖线的标题**（如 `2.7.3 主路径：导出 \`.reg\` → …`），改链到不含特殊字符的上级标题
