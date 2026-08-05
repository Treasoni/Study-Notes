# Stale Map — Docker网络结构详解.md

> 运行标识：update-docker ｜ 批次：network ｜ 生成日期：2026-08-04
> 目标笔记：`C:\note\Study-Notes\docker\Docker网络结构详解.md`（44.6KB，未改动）
> 输出笔记：`updates/network/updated_note.md`

## 判定标准

- 依据来源库：`workspace/update-docker/shared_research/source_bank.md`（T1 版本现状：S1 / S2 / S3）。
- 网络核心概念（veth pair、bridge、iptables NAT、host/overlay 等）属稳定知识，判定为 keep。
- 本次只修版本基线、补 2026 新信息、规范化元数据，不改写正文。

## 变更清单

| 章节 | 位置 | 判定 | 内容 | 依据 |
|------|------|------|------|------|
| Frontmatter | 文件头部 | update | `updated` 2026-03-29 → 2026-08-04；补充 `title` / `status` / `source_project`；保留 `created` 与 `tags` | 输出规范 + S1 |
| 二、底层实现原理 / 2.4 iptables NAT | 「查看 iptables 规则」代码块之后 | add | 新增 `[!note] iptables 后端（2026 现状）`：Docker 支持 nftables 后端，新发行版可能存在 iptables-legacy/nft 差异，可用 `nft list ruleset` 排查 | 任务指引第 4 条 |
| 三、网络模式详解 / 3.2 Bridge 模式 | 「容器间通信」代码块之后 | add | 新增 `[!note] 2026 现状`：Docker Engine 29 为现行稳定版（29.6.2），IPv6 与 DNS 解析增强；Engine 28 已于 2026-05-13 EOL；自定义网络内置 DNS 仍推荐 | S1, S3 |
| 四、Docker 网络命令 / 4.3 端口映射 | 来源标注 | update | 「基于 Docker 25.0+」→「基于 Docker Engine 29.x（2026 现行稳定版）」 | S1, S3 |
| 页脚 | 全文末尾 | update | `**最后更新**：2026-03-29` → 2026-08-04 | 本次运行 |
| 全文末尾 | 追加 | add | `## 更新记录` 章节（日期 + 变更摘要） | 输出规范 |
| 一、架构概览 / 二、底层实现原理（veth、bridge、NAT）/ 三、网络模式（host、none、overlay、对比）/ 四、命令 / 五、实战 / 六、排查 / 七、知识关系 / 参考资料 | 全文 | keep | 核心概念、ASCII 图、代码示例、验证命令全部保持原样 | 稳定知识 |
| 删除项 | — | delete | 无 | 无过时内容需删除 |

## 关键 Keep 说明

- 2.2 veth pair、2.3 网桥、2.4 iptables NAT：原理与命令（`ip link`、`iptables -t nat -L`、`docker network inspect`）在 2026 仍有效，保留。
- 3.1 模式表（bridge/host/none/overlay/macvlan）、3.3-3.6：行为未变，保留。
- 5.1 / 5.2 docker-compose 示例：`version: '3.8'` 在新版 Compose 中已忽略但无害，按「保留代码示例」处理（见 update_report 风险项）。
- 原文 ASCII 图中 4 处历史 mojibake 字符（1.2 / 3.3 / 3.4 / 3.6 图边界）：为保持字节一致未修复，另记入 update_report 风险项。
