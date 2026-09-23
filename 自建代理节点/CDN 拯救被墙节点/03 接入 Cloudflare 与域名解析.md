---
title: "第 3 章 接入 Cloudflare 与域名解析"
tags:
  - 自建节点
  - 代理
  - VPS
  - CDN
  - Cloudflare
  - 网络
  - 学习
created: 2026-09-24
updated: 2026-09-24
status: 完成
source_project: vps-node-cdn-rescue
chapter: 3
---

# 第 3 章 接入 Cloudflare 与域名解析

第二章的原理都压在一个前提上：**你的域名真的由 Cloudflare 接管**。这一步的坑比想象中多。本章不讲填法（见面板流 [[07 搭建节点（带域名与 Cloudflare）]]），只补三件事：**套餐门槛、接入期行为、怎么验证生效**。

## 3.1 免费版只有一条路

Cloudflare 有四种 zone 接法，对免费用户开放的只有一种（来源：B-5 | `DNS setups`、`Common use cases and availability`；B-6、B-7 | `Availability`）：

| DNS setup | 门槛 | 解决什么 |
|---|---|---|
| Primary (Full) | **Free 起全套餐** | Cloudflare 作主权威 DNS，记录全托管在此 |
| CNAME (Partial) | **Business 起** | 保留原权威 DNS，只把个别子域交它反代 |
| Zone transfers | **仅 Enterprise** | 与另一家 DNS 并用，记录以 AXFR / IXFR 互传 |
| Subdomain setup | **仅 Enterprise** | 被委派子域的设置独立成另一个 zone |

所以结论很干脆：**改 NS，把整个 zone 交给 Cloudflare**。Cloudflare 自持顶级域（TLD）名称服务器，NS 切过去后解析直接落到它自己，**省去若干中间步骤**（来源：D-2 | §3.2）；另有差别：DNS 基础设施的 DDoS 防护只覆盖 full setup（来源：B-7 | `DDoS protection`）。但**官方在这一步没有 NS 接入的操作细则**，只有 setup 定义与可用性数据，改 NS / 加记录属 [[07 搭建节点（带域名与 Cloudflare）]]（来源：B-5 | `DNS setups`）。

还有个歧义：**`CNAME flattening` 指两回事**——Cloudflare 侧指被代理 CNAME **默认被展平**、返回 anycast 地址（来源：B-1 | `### CNAME records`）；权威 DNS 侧指「把 apex 的 CNAME 展平」的能力，CNAME (partial) 下**只有支持它才能把 apex 代理到 Cloudflare**（来源：B-7 | `CNAME flattening`）。

## 3.2 速查表：代理状态与记录类型

> **以下已在面板流第 7 章展开，此处仅速查**（详见 [[07 搭建节点（带域名与 Cloudflare）]]）。

| 项目 | 结论 | 来源 |
|---|---|---|
| 橙云（Proxied） | DNS 答 anycast IP；HTTP/HTTPS 经 Cloudflare，套用 DDoS 防护、缓存与 WAF 规则 | B-1 \| `### Benefits` |
| 灰云（DNS only） | 答**源站真实 IP**，暴露源站 | B-1 \| `## DNS-only records` |
| 哪些记录能被代理 | **仅承载 HTTP/HTTPS 的 A / AAAA / CNAME**（B-2 严口径；B-1 宽口径并列，**以 B-2 为准**） | B-2 \| `## Proxy eligibility`；B-1 |
| 同名多条 A/AAAA | 一条橙云，**整组按橙云处理** | B-1 \| `### Mix proxied and unproxied` |
| CNAME 链 | 链上任一主机名被代理，请求即被代理 | B-1 \| `### Mix proxied and unproxied` |
| 被代理 CNAME | 默认展平，返回 Cloudflare anycast IP | B-1 \| `### CNAME records` |
| 代理记录 TTL | 固定 **Auto = 300 秒**，不可修改 | B-1 \| `### Predefined time to live` |
| 接入期（pending） | 先按灰云处理、**返回源站 IP**；激活后建议**轮换源站 IP** | B-2 \| `## Pending domains` |

## 3.3 接入期与 zone 状态

zone 添加后先进入 **pending** 验证所有权，**最长约 24 小时**；期间**即使记录已设为橙云，也按灰云处理、返回源站 IP**——这段窗口会暴露源站，故官方建议**激活后轮换源站 IP**（来源：B-2 | `## Pending domains`）。zone 状态（来源：B-5 | `## Zone status`）：

| 状态 | 含义 |
|---|---|
| Initializing / Pending | 初始化 / 待验证所有权 |
| Active | 已激活，可代理 |
| Moved / Deleted / Purged | 已迁出 / 已删除 / 已清除 |

## 3.4 解析是否生效怎么验

验证只看一件事：**同一条记录查出来的答案属于哪一边**（来源：B-1 | `### Example`）：

```bash
# 橙云：答案应落在 Cloudflare 地址段
$ dig +short your-domain.example
104.16.x.x
172.67.x.x

# 灰云：直接返回源站真实 IP
$ dig +short your-domain.example
203.0.113.7
```

答案是 Cloudflare 地址段，说明「解析已到 Cloudflare」，正是 [[04 把节点套上 CDN]] 要接的那一半；若仍是源站 IP，先看 zone 是否还在 pending。

> [!note] `dig` 与在线 DNS 检查是**通用工具**，非本文素材来源
> 地址段形态出自官方 `### Example`；命令本身**无官方锚点**。

## 3.5 前置条件：域名与 NS（只做指路）

> [!note] 「前置」指前置条件，与 [[02 为什么 CDN 能救被墙节点]] 的 domain fronting 无关
> 本节说的「前置」是**前置条件**（先得有域名、能改 NS）；[[02 为什么 CDN 能救被墙节点]] 讲的 **domain fronting** 是另一种手法，两者不是一回事。

本章默认你**已有域名、能改 NS**；若还没有，本系列「低价域名获取」「托管与解析域名」两期更细。

## 3.6 大白话

> [!tip] 大白话
> 把 DNS 想成「门牌登记处」：**NS 接入 = 把整个登记处交给 Cloudflare 管**，门牌都由它发；**CNAME 接入 = 只在自己门口挂块转接牌**指向它那台机器——但要 Business 起，且登记处得能「把转接牌挂到楼顶（apex）」，多数人用不了。

### 本章小结

- Free / Pro 只有 primary (full)；CNAME (partial) 要 Business 起，zone transfers 与 subdomain setup 仅 Enterprise（来源：B-5 | `Common use cases and availability`；B-6、B-7 | `Availability`）。
- 官方在此只给定义与可用性，**没有 NS 接入的操作细则**；填法见面板流 [[07 搭建节点（带域名与 Cloudflare）]]（来源：B-5 | `DNS setups`）。
- 可代理记录采用 B-2 严口径「仅承载 HTTP/HTTPS 的 A/AAAA/CNAME」，B-1 宽口径仅并列参考（来源：B-2 | `## Proxy eligibility`；B-1）。
- 接入期（pending，最长 24h）记录按灰云处理并返回源站 IP（来源：B-2 | `## Pending domains`）。
- `CNAME flattening` 一词两义：Cloudflare 侧默认展平被代理 CNAME；权威 DNS 侧需具该能力才能代理 apex（来源：B-1 | `### CNAME records`；B-7 | `CNAME flattening`）。

### 下一章预告

域名侧通了，只解决了「请求能到 Cloudflare」。还差一半——Cloudflare 能不能顺利把请求交回你的源站。

---

> 上一篇：[[02 为什么 CDN 能救被墙节点]] ｜ 返回索引：[[00 CDN 拯救被墙节点]] ｜ 下一篇：[[04 把节点套上 CDN]]
