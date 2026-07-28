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
