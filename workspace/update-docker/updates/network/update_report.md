# Update Report — Docker网络结构详解.md

> 运行标识：update-docker ｜ 批次：network ｜ 日期：2026-08-04

## 变更摘要

| # | 变更 | 位置 | 类型 |
|---|------|------|------|
| 1 | Frontmatter：`updated` → 2026-08-04，补充 `title` / `status` / `source_project` | 文件头 | 元数据更新 |
| 2 | 版本标注「基于 Docker 25.0+」→「基于 Docker Engine 29.x（2026 现行稳定版）」 | 4.3 来源 | 版本刷新 |
| 3 | 新增 `[!note] 2026 现状`（Engine 29 IPv6/DNS 增强、28 EOL） | 3.2 Bridge 模式 | 新增说明 |
| 4 | 新增 `[!note] iptables 后端`（nftables 后端 / legacy-nft 差异排查） | 2.4 iptables NAT | 新增提示 |
| 5 | 页脚 `最后更新` → 2026-08-04；追加 `## 更新记录` | 全文末尾 | 记录 |
| 6 | 核心原理 / ASCII 图 / 代码示例 / 验证命令 | 全文 | 保持不变 |

原笔记 44.6KB 中约 97% 内容字节级保持不变，仅以上 5 处局部 patch。

## 使用的来源（shared_research/source_bank.md）

- S1 — Docker Engine 29 release notes（官方）：29.x 为 2026 现行稳定版、最新补丁 29.6.2、容器网络 IPv6 与 DNS 解析增强、Engine 28 已于 2026-05-13 EOL。
- S3 — Docker Engine 支持周期（社区汇总）：确认版本基线至少 29.x。
- S2 — Docker Desktop release notes（官方）：Engine v29.6.2 佐证版本号（未直接引用 Desktop/Compose 细节）。

未重新联网检索；按任务指引只使用共享来源库。

## 验证命令（未改动，仍有效）

- `ip link show | grep veth`
- `sudo iptables -t nat -L -n` / `sudo iptables -t nat -L DOCKER -n`
- `docker network inspect bridge` / `docker network ls` / `docker network create`

## 未解决风险

1. **docker-compose `version: '3.8'`（5.1 / 5.2）**：新版 Compose（v2 / v5.x）已忽略 `version` 键，该字段过时但无害。按任务指引「保留代码示例」未修改；如需彻底 2026 化，可在后续批次删除 `version` 行并注明 Compose v2 不再需要。
2. **nftables 提示**：来源库未直接收录 nftables 细节，属任务指引明确允许补充的普遍事实；措辞谨慎（「可能涉及」「辅助排查」），未编造具体版本或规则。
3. **原有 ASCII 图存在 4 处历史 mojibake 字符**（1.2 / 3.3 / 3.4 / 3.6 图边界，如 `├─��`、`��点` 等）：为保持字节一致未修复，建议后续单独清理。
4. **来源库 S5 镜像源 / T2、T3、T4 内容**：与本笔记（网络结构原理）无关，未引用。
5. **`brctl show docker0`（2.3）**：新发行版中 brctl 已被 iproute2 的 `bridge link` 取代，命令可能不可用；来源库未涉及且非本次范围，保留原样。

## 结论

更新完成。输出文件：
- `updates/network/stale_map.md`
- `updates/network/update_plan.md`
- `updates/network/updated_note.md`
- `updates/network/update_report.md`

原 vault 文件 `C:\note\Study-Notes\docker\Docker网络结构详解.md` 未改动。
