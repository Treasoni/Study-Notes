---
url: "https://openwrt.org/docs/guide-user/perf_and_log/flow_offloading"
title: "Flow Offloading (OpenWrt Wiki)"
publisher: "OpenWrt project (wiki)"
last_modified: "2026/08/17 18:49 by phinn"
scraped_at: 2026-09-23
retrieval_method: "WebFetch (crawl4ai blocked: openwrt.org serves an Anubis proof-of-work bot challenge, HTTP 200 with ~4307-byte challenge page)"
note: "以下为官方页面关键表述的逐字引用摘录，非全文。引号内为原文英文。"
---

# Flow Offloading — 官方页面关键引文摘录

## 定义 / 机制

- Linux flow offloading "bypasses the CPU-intensive Netfilter stack (firewall processing) for established traffic flows"，并 "significantly increases network throughput"。
- SFO（Software Flow Offloading）："typically increases bandwidth by 2-3x over firewall filtering each packet"；"often relieves fully loaded CPUs improving latency/jitter too"；"Since SFO is a software feature it is widely supported on all CPUs"。
- HFO（Hardware Flow Offloading）："requires specialized SoC hardware to bypass QoS traffic controls at high priority"。
- HFO 容量限制："handles a limited number of concurrent connections (64 queues is typical)"，超出的连接 "returning surplus connections to the software flow offload pool"，因此 "will not significantly help some applications including p2p"。
- HFO 与 QoS："also incompatible with QoS features such as SQM"。
- 开启 HFO 时同时启用 SFO："SFO will still be needed to handle extra concurrent connections"。
- 适用范围："applies to forwarded connections"，"including those to containers like LXC or podman, but not locally running web-server"。
- 与网卡卸载区分：flow offloading "is not directly related to network adapter offload functions controlled by `ethtool -k/-K`"。

## 平台支持

- HFO "officially supported by small number of platforms, primarily MediaTek Filogic SoCs"。
- MediaTek 自 mt7621 起在 mt76 平台提供 HFO 与 WED 的开源 Linux 支持，可用 "/sys/kernel/debug/ppe0/entries" 观察。
- WED："WED will bypass QoS AQL and stale connections/freezes can occur when changing or roaming"，且 "WED is not available on 2.4 GHz"。
- Qualcomm NSS 走闭源驱动："there is no official OpenWrt that support for NSS offloading"。

## UCI / LuCI

- `firewall.@defaults[0].flow_offloading=1`（软件）
- `firewall.@defaults[0].flow_offloading_hw=1`（硬件）
- 配置文件等价写法：`option flow_offloading '1'`、`option flow_offloading_hw '1'`（位于 `config defaults`），随后 `/etc/init.d/firewall restart`。
- LuCI：Network → Firewall，选择 "Software flow offloading" 或 "Hardware flow offloading"。

## 关键词出现情况（用于 A4 缺口判定）

- netfilter：出现（作为被绕过的栈，并引用 Netfilter flowtable 基础设施文档）。
- flowtable：出现。
- nftables：未出现。
- **NFQUEUE：未出现**（页面全文无此词）。
- QoS/SQM：出现（HFO 与 SQM 不兼容；WED 绕过 QoS AQL）。
- 包检测（packet inspection）：无明确表述，仅有 "firewall filtering each packet"。

## 同站点另一官方页：firewall_configuration

- 来源：https://openwrt.org/docs/guide-user/firewall/firewall_configuration （`defaults` 选项表）
- `flow_offloading`（boolean，默认 0）："Enable software flow offloading for connections. (decrease cpu load / increase routing throughput)"
- `flow_offloading_hw`（boolean，默认 0）："Enable hardware flow offloading for connections. (depends on flow_offloading and hw capability)"
- 该页无 flow offloading 专节；未出现 NFQUEUE / flowtable；netfilter/nftables 仅出现在无关段落。
