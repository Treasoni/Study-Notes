# Learnings

<!-- 每次追加新条目，超 100 行触发压缩 -->

## [LRN-20260728-001] best_practice

**Logged**: 2026-07-28T15:45:00+08:00
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
更新旧笔记时必须审计全部内联 URL 的有效性、上下文匹配和协议兼容性。

### Details
在更新 `linux/Linux换源.md` 时：
1. 初次只检查了 wikilink（双链），未检查代码块中的内联 URL
2. 用户指出 FAQ 中的 `curl https://mirrors.tuna.tsinghua.edu.cn/archlinux/lastupdate` 是 Arch Linux 专用端点，放在通用 FAQ 中会导致 Ubuntu 用户困惑
3. 进一步全量 URL 审计发现一键换源脚本的 `sed` 只匹配 `http://` 协议，但 Ubuntu 22.04 后期默认已改用 `https://`，导致脚本在较新系统上静默失败

### Suggested Action
每次 `note-updater` 执行后，对笔记中所有 URL 做三层检查：
1. **可达性** — `curl -sI` 验证 HTTP 状态码
2. **上下文匹配** — URL 所属发行版/工具是否与所在章节一致
3. **协议兼容** — 配置示例中的 URL 协议是否覆盖新旧系统（如同时匹配 http/https）

---

## [LRN-20260728-002] best_practice

**Logged**: 2026-07-28T15:45:00+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
处理多发行版笔记时，每个操作示例必须标注适用的发行版范围，避免跨发行版误用。

### Details
更新 `Linux换源.md` 时发现多处命令/配置示例没有显式标注发行版范围：
- FAQ 中的同步状态检查命令未标注「仅 Arch Linux」
- `netselect-apt` 测试命令未标注「仅 Ubuntu/Debian」
- GPG 密钥添加方式在不同发行版间差异大，需要区分说明

### Suggested Action
在多发行版笔记中，每条代码块/命令前用注释或 `>` 标注目标发行版，格式统一：`# Ubuntu/Debian`、`# Arch Linux`。

---


## [LRN-20260729-001] best_practice

**Logged**: 2026-07-29T00:20:00+08:00
**Priority**: medium
**Status**: active
**Area**: obsidian

### Summary
大笔记应拆分为多个主题独立的单篇笔记，放入一个专用文件夹

### Details
本次 "Linux 常用命令实战手册" 初始产出为 5423 行单一笔记，用户反馈太大。改为按章节拆分为 9 篇独立笔记 + 1 篇索引页，放入 `linux/linux常用命令/` 文件夹。每篇 300-800 行，按需查阅。

拆分要点：
- 每篇添加独立 YAML frontmatter（title/created/updated/tags/status）
- 创建轻量索引页汇总所有子篇的链接和说明
- MOC 中每个子篇独立一条索引项，链接路径用文件夹前缀
- 原有的旧笔记（如 linux的文件权限.md）保持不动

### Suggested Action
产出综合型笔记时，优先考虑"一个主题文件夹 + 多篇独立笔记 + 索引页"结构，而非单一长篇笔记。写入 CLAUDE.md 或 note-system.md 作为规范。

---

## [LRN-20260729-002] tool_limitation

**Logged**: 2026-07-29T00:20:30+08:00
**Priority**: low
**Status**: active
**Area**: research

### Summary
WebFetch 无法访问 cloud.tencent.com 和 blog.csdn.net 等国内技术站点

### Details
深度收集阶段尝试用 WebFetch 精读腾讯云和 CSDN 的文章，全部返回 "Unable to verify if domain is safe to fetch"。改用 WebSearch 获取摘要信息，结合自身知识库完成内容编写。

### Suggested Action
遇到 WebFetch 无法访问的站点时，优先用 WebSearch + 自身知识库的组合方案，或尝试 defuddle skill。

---

## [LRN-20260729-003] best_practice

**Logged**: 2026-07-29T15:40:00+08:00
**Priority**: high
**Status**: active
**Area**: beautify

### Summary
发布笔记到目标目录后必须验证文件编码，确保 CJK 内容未被破坏。

### Details
本次 `Linux网络信息获取与概念` 笔记发布后，所有 10 个章节文件的正文出现 mojibake（如"网络"变成"缃戠粶"），但 YAML frontmatter 是正常的。工作区的源文件编码正确，问题出在发布/复制阶段的编码转换。

排查耗时较长，因为一开始误以为用户说的"显示有问题"是格式问题（BOM、callout），忽略了编码问题这一首要疑点。在 CJK 内容处理中，编码问题应作为最优先排查项。

### Suggested Action
发布步骤（note-beautifier 或 publish 流程）完成后，抽样验证目标文件的编码：
1. 用 `python3 -c "open('file.md','rb').read().decode('utf-8')"` 确认无解码错误
2. 从前 10 行中提取几个中文字符检查是否与预期一致
3. 优先对比工作区源文件和目标文件的正文内容，而非仅看格式

---

## [LRN-20260729-004] debug_order

**Logged**: 2026-07-29T15:40:00+08:00
**Priority**: medium
**Status**: active
**Area**: general

### Summary
用户反馈中文笔记"显示有问题"时，编码问题（mojibake）应作为首要排查项，优先于格式问题（BOM、callout、wikilink 等）。

### Details
本次会话中用户报告"笔记显示有问题"，我首先检查了 BOM 和 callout 格式，花了一轮才发现用户实际说的是"乱码"（编码问题）。在 CJK 内容的生产/发布流程中，编码损坏是最常见且影响最严重的显示问题，应在排查的第一轮就检查。

### Suggested Action
当用户报告中文笔记"显示有问题"或"乱码"时，排查优先级：
1. 第一轮：用 `xxd` 或 `python3` 检查文件编码、对比源文件和目标文件
2. 第二轮：检查 YAML frontmatter 是否可被正常解析
3. 第三轮：检查 callout、表格、代码块等格式问题

---