# 01 探测式收集结果 - VPS 自建节点零基础全流程（面板流）

- **运行标识**: vps-node-panel-tutorial
- **阶段**: P1（探测式收集）
- **检索日期**: 2026-09-23（子代理探测）／2026-09-24（父流程全量复核）
- **派发记录**: 3 个透镜 × 1 个子代理（并发 3，符合「≤3 delegates / ≤4 同类并发」约束）
- **数据来源**: 视频章节骨架（见 `00_intent.md`）+ 官方文档探测；视频本身无字幕，未产生任何"视频原话"类记录

---

## 一、透镜与探测结果

### 透镜 A：概念层 —— 基础名词与路线取舍的定义性来源
Subagent A（11 tool calls）。核心产出：Xray 官方协议文档、机场生态学术研究、3x-ui 官方仓库、Shadowsocks 规范。

### 透镜 B：落地层 —— 从买 VPS 到面板建节点的可照做路径
Subagent B（14 tool calls）。核心产出：3x-ui 安装 wiki、三家 VPS 厂商官方产品页、FinalShell 官网、作者配套 Notion 文档。

### 透镜 C：域名与运维层 —— 带域名搭建、节点被封、最小安全加固
Subagent C（13 tool calls）。核心产出：Cloudflare 代理状态与限制官方页、fail2ban、sshd_config 手册、厂商重建实例流程。

---

## 二、来源表（已按 canonical URL 去重）

> tier 口径：`official` = 项目官方文档/官方仓库/厂商官网；`primary-research` = 同行评议或预印本一手研究；
> `community` = 第三方教程/经验帖，仅可作操作性经验并须标注层级。

### 概念层

| ID | 标题 | URL | Tier | 相关性 | 日期 | 分 |
|---|---|---|---|---|---|---|
| A-1 | Xray 官方文档：出站代理协议配置（VLESS / VMess / Trojan / Shadowsocks） | https://xtls.github.io/config/outbound.html | official | 四种常见代理协议的权威定义与字段来源 | 常青页 | 5 |
| A-2 | Understanding the "Airport" Censorship Circumvention Ecosystem in China | https://arxiv.org/abs/2606.18427 | primary-research | 首个机场生态系统系统性研究，含使用比例与性能测量 | 2026-06-16 | 5 |
| A-3 | MHSanaei/3x-ui 官方仓库 | https://github.com/MHSanaei/3x-ui | official | 3x-ui 面板的官方定义来源，说明其为 Xray 的 Web 管理面板 | 常青页 | 4 |
| A-4 | Shadowsocks 官方规范 SIP022（Shadowsocks 2022） | https://shadowsocks.org/doc/sip022.html | official | Shadowsocks 协议与 URI 的规范定义来源 | 常青页 | 4 |
| A-5 | 机场、VPN、VPS 自建到底有什么区别？ | https://kejilaowang.com/how-to-choose-vps-for-proxy/ | community | 中文对照文，区分机场/VPN/自建三种路线的成本与维护取舍 | 2025-12 | 3 |

### 落地层

| ID | 标题 | URL | Tier | 相关性 | 日期 | 分 |
|---|---|---|---|---|---|---|
| B-1 | 3x-ui 官方 Installation 文档 | https://github.com/MHSanaei/3x-ui/wiki/Installation | official | 面板一键安装脚本、Docker 与手动部署的官方步骤 | 常青页 | 5 |
| B-2 | RackNerd KVM VPS 官方产品页 | https://racknerd.com/kvm-vps | official | 厂商官方套餐与计费页，可核对配置、价格与机房 | 常青页 | 4 |
| B-3 | BandwagonHost（搬瓦工）官方 VPS Hosting | https://bandwagonhost.com/vps-hosting.php | official | 官方套餐选购入口，购买后经 KiwiVM 取 IP、SSH 端口与 root 密码 | 常青页 | 4 |
| B-4 | FinalShell 官网下载与版本页（HostBuf） | https://www.hostbuf.com/t/988.html | official | SSH 客户端官方下载与版本说明 | 2025-05 | 4 |
| B-5 | 作者配套搭建文档（Notion，InfiCheesy 空间） | https://wise-vegetarian-da6.notion.site/VPS-2daacc0097d38077a769e8a98051fec1 | community | 视频作者自建图文步骤，可作操作顺序参考 | 无标识 | 3 |
| B-6 | CloudCone 官方 VPS 产品页（缺口补录） | https://cloudcone.com/vps/ | official | 厂商官方 VPS 产品与计费页 | 常青页 | 3 |

### 域名与运维层

| ID | 标题 | URL | Tier | 相关性 | 日期 | 分 |
|---|---|---|---|---|---|---|
| C-1 | Cloudflare DNS — Proxy status（代理状态） | https://developers.cloudflare.com/dns/proxy-status/ | official | 代理状态定义，橙云解析到 CF 泛播 IP 并隐藏源站 | 常青页 | 5 |
| C-2 | Cloudflare DNS — Proxying limitations（代理限制） | https://developers.cloudflare.com/dns/proxy-status/limitations/ | official | 仅 HTTP(S) 可代理；SSH/非标端口须 DNS-only；官方建议激活后轮换源站 IP | 常青页 | 5 |
| C-3 | Fail2ban 官方文档 | https://fail2ban.readthedocs.io/en/latest/ | official | jail 配置与 sshd 暴力破解封禁参数 | 常青页 | 4 |
| C-4 | OpenSSH sshd_config(5) 手册页 | https://man.openbsd.org/sshd_config | official | SSH 最小加固一手来源：Port / PasswordAuthentication / PermitRootLogin | 常青页 | 4 |
| C-5 | DigitalOcean — How to Rebuild Droplets | https://docs.digitalocean.com/products/droplets/how-to/rebuild/ | official | 官方重建实例流程；重建保留原 IP，换 IP 需借快照或 Floating IP | 常青页 | 3 |
| C-6 | 阿里云 ECS 产品概览（VPS 定义，缺口补录） | https://help.aliyun.com/zh/ecs/product-overview/what-is-ecs | official | 权威的「什么是云服务器/VPS」定义来源 | 常青页 | 4 |
| C-7 | Vultr — How to configure networking（缺口补录） | https://docs.vultr.com/how-to-configure-networking-on-vultr-cloud-servers | official | 厂商网络配置官方说明，用于换 IP 结论的对照 | 常青页 | 3 |

### 去重说明

- `github.com/MHSanaei/3x-ui`（A-3）与 `.../wiki/Installation`（B-1）**同属一个官方项目但 canonical URL 不同**，语义互补：A-3 供「这是什么」，B-1 供「怎么装」，两者都保留，不视为重复。
- `developers.cloudflare.com/dns/proxy-status/`（C-1）与 `.../limitations/`（C-2）为同一官方站的两个独立页，前者定义、后者给限制与风险，均保留。
- C-6 / C-7 / B-6 为子代理报告覆盖缺口后由父流程补录，均已 curl 复核返回 200。
- 本表 **19 条候选全部经父流程 curl 独立复核**（其中 Notion B-5 首次返回 `000`，重试后 200）。

---

## 三、覆盖缺口（P2 需正面处理）

1. **「代理节点」「订阅链接」缺官方或权威定义来源** —— 现有材料均为社区科普，未达可引用标准。P2 只能标为「行业通用说法」，不得伪装成官方口径。
2. **「如何判定本机 IP 被封」无官方文档** —— 相关说明散见于厂商 abuse 政策与第三方经验，缺一手来源。P2 须明示为经验判断，不得写成官方判定标准。
3. **厂商换 IP 结论不一致** —— DigitalOcean 重建保留原 IP（C-5），Vultr 快照部署分配新 IP，两者不可合并成一句通论，必须分厂商分别引用。
4. **FinalShell 无官方使用手册** —— 官网仅有下载与更新日志，连接步骤只能依赖第三方教程，引用时须降层标注。
5. **自建 vs 机场的成本/维护取舍仅 1 篇社区文章** —— 但 A-2 提供了量化对照（使用比例、性能测量），可部分替代，但两者口径不同，不可混用成一句结论。
6. **3x-ui 无官方中文零基础教程** —— 中文分步内容均来自第三方社区站。
7. **作者配套 Notion 文档（B-5）无法独立核对版本** —— 该页为前端渲染 SPA，需 JS 渲染方可取正文；且原文无更新日期，不能作为"最新步骤"的唯一依据。

---

## 四、P2 建议核心来源与预算

**核心 5 篇（必抓）**：A-1、A-2、B-1、C-2、A-4
—— 覆盖「协议定义 / 机场对照数据 / 面板安装 / 域名与源站风险 / SS 规范」四类骨架事实。

**缺口补抓（按需）**：B-2、B-3、B-6、B-4、C-1、C-3、C-4、C-5、C-7、C-6、B-5

**预算估计**：
- 抓取篇数：核心 5 篇 + 缺口约 6 篇 ≈ **11 篇**
- 派发：**≤3 个深度阅读子代理**（按来源组分批：协议与概念组 / 面板与厂商组 / 域名与加固组），禁止一源一代理
- `02_deep_research.md` 预期体量：**约 15–20 KB**，含来源表、claim/source 映射、矛盾点、开放问题、下游交接说明
- 环境：crawl4ai 环境已就绪（`crawl.sh --help` 退出 0）；**B-5 Notion 必须用默认 JS 渲染模式**抓取

---

## 五、方向确认菜单（P1 → P2 用户关卡）

学习方向已由视频章节结构锁定，此处确认的是 **P2 的取材侧重**：

```
[1] 全流程均衡取材（推荐）
    概念（VPS/协议/面板/机场 vs 自建）约 25% + 落地主线约 50% + 域名/被墙/安全约 25%
    对应视频 9 个章节一一覆盖，零基础读者单篇可通读

[2] 只要「能跑通」
    压缩概念与运维，重心全放在 购买 → 登录 → 装面板 → 建节点 → 使用
    被墙与安全只作一节提示

[3] 加强运维与风险权重
    概念适度，显著加重 带域名、节点被封的应对、最小安全加固
    适合你已决定长期自用、更关心稳定性和安全
```

**另需你确认一项**：A-2 是 arXiv 学术论文（一手研究，提供机场使用比例与性能测量数据）。
放进一篇零基础教程里会让行文偏重，但它是本主题**唯一的高可信量化来源**。

- **纳入（推荐）**：在「机场 vs 自建」一节用一两句给出测量结论并标注引用，其余不展开
- **不纳入**：概念层只保留官方定义，放弃量化对照

直接回「1 + 纳入」或「按推荐」即可，我据此进 P2。若选 [2] 或 [3] 请一并说明。
