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

