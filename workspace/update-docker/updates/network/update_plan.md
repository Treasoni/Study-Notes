# Update Plan — Docker网络结构详解.md

> 运行标识：update-docker ｜ 批次：network ｜ 日期：2026-08-04

## 目标

将 Docker 网络深度笔记从「Docker 25.0 时代」局部刷新到 2026 现状（Docker Engine 29.x）。核心网络原理保持不变，只修正版本基线、补充 2026 新信息、规范化 frontmatter 与更新记录。

## 变更明细

### 1. Frontmatter 规范化
- 变更：`updated` 2026-03-29 → 2026-08-04；补充 `title: Docker 网络结构详解`、`status: 已更新`、`source_project: update-docker`。
- 原因：满足 YAML frontmatter 键要求（title/tags/created/updated/status/source_project）；保留原 `created`（2026-03-29）与 `tags`。

### 2. 版本基线刷新（4.3 来源标注）
- 变更：「基于 Docker 25.0+」→「基于 Docker Engine 29.x（2026 现行稳定版）」。
- 原因：S1 / S3 明确 Docker Engine 29.x 为 2026 现行稳定版，28.x 已于 2026-05-13 EOL；原文 25.0 已过时。

### 3. 新增 Engine 29 网络增强说明（3.2 Bridge 模式）
- 变更：在「容器间通信」代码块后新增 `[!note] 2026 现状`，注明 Docker Engine 29（29.6.2）对容器网络 IPv6 与 DNS 解析的增强、Engine 28 EOL，并确认自定义网络内置 DNS（容器名/服务名互访）仍为推荐做法。
- 原因：S1 记录 Engine 29「容器网络 IPv6 与 DNS 解析增强」；该节恰好讨论网络通信与 DNS，插入位置自然。

### 4. 新增 iptables / nftables 提示（2.4 iptables NAT）
- 变更：在「查看 iptables 规则」代码块后新增 `[!note] iptables 后端（2026 现状）`，提示 Docker 已支持 nftables 后端，默认 nftables 的新发行版上可能存在 iptables-legacy/nft 差异，可用 `nft list ruleset` 辅助排查。
- 原因：任务指引第 4 条；帮助新发行版用户排查「`iptables -L` 看不到规则」的问题。表述谨慎，未引入来源库之外的具体版本或细节。

### 5. 页脚与更新记录
- 变更：`**最后更新**` 2026-03-29 → 2026-08-04；追加 `## 更新记录` 章节（日期 + 变更摘要）。
- 原因：输出规范要求以日期 + 摘要记录本次变更。

## 明确不做

- 不改写 veth pair / 网桥 / iptables NAT / host / none / overlay 原理及代码示例（稳定知识）。
- 不重写 docker-compose 示例（保留代码示例原样；`version: '3.8'` 过时风险写入 update_report）。
- 不重排章节结构、不删除参考资料、不改动 ASCII 图（含原有几处 mojibake 字符，保持字节一致）。
- 不触碰原 vault 文件（`C:\note\Study-Notes\docker\Docker网络结构详解.md`）。

## 实施方式

拷贝原文件到输出目录后逐点局部 patch；非过时段落保持字节级一致（原文件 44.6KB，仅 5 处局部修改）。
