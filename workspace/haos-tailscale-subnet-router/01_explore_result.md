# 如何用 HAOS 部署的 Home Assistant 中的 Tailscale 插件实现内网穿透和子路由 - P1 探测结果

- **运行标识**: haos-tailscale-subnet-router
- **阶段**: P1 探测式收集
- **探测日期**: 2026-09-12
- **探测方式**: 3 个独立视角并行派发子代理，各 3–8 次检索；本轮只读搜索摘要，**未打开任何正文页面**
- **原始记录**: 55 条 → 按 canonical URL 去重后 **46 条**

> ⚠️ 本轮所有记录均来自搜索结果摘要（子代理已逐条标注）。文中出现的选项名、issue 结论、版本变化在 P2 必须回原文核对后采信。

---

## 1. 去重来源表

### A. 官方文档 / 官方博客（15 条）

| ID | 标题 | URL | 层级 | 评分 | 来源视角 |
| --- | --- | --- | --- | --- | --- |
| S1 | Home Assistant Community App: Tailscale — DOCS.md | https://raw.githubusercontent.com/hassio-addons/app-tailscale/refs/heads/main/tailscale/DOCS.md | 插件官方仓库文档 | 5 | A1,B12,C5 |
| S2 | Home Assistant Add-on: Tailscale — DOCS.md（hass-tailscale 版，走 auth_key） | https://raw.githubusercontent.com/hass-tailscale/hass-addons/refs/heads/main/tailscale/DOCS.md | 插件官方仓库文档 | 4 | A2 |
| S3 | Access Home Assistant Remotely with Tailscale（Tailscale 官方博客） | https://tailscale.com/blog/remotely-access-home-assistant | official | 5 | A3 |
| S4 | Tailscale 集成（Home Assistant 官方集成页） | https://www.home-assistant.io/integrations/tailscale/ | official | 4 | A4 |
| S5 | Site-to-site networking | https://tailscale.com/docs/features/site-to-site | official | 5 | B1 |
| S6 | Subnet routers | https://tailscale.com/docs/features/subnet-routers | official | 5 | B2 |
| S7 | Configure a subnet router（Linux tab） | https://tailscale.com/docs/features/subnet-routers/how-to/setup?tab=linux | official | 5 | B3 |
| S8 | Route injection | https://tailscale.com/docs/reference/route-injection | official | 5 | B4 |
| S9 | Manage client preferences（Use Tailscale subnets / --accept-routes） | https://tailscale.com/docs/features/client/manage-preferences | official | 5 | B5 |
| S10 | Route traffic（subnet router vs exit node） | https://tailscale.com/docs/route | official | 4 | B7 |
| S11 | Kernel vs. netstack subnet routing & exit nodes | https://tailscale.com/docs/reference/kernel-vs-userspace-routers | official | 3 | B8 |
| S12 | Access your VPC（含 firewalld masquerade） | https://tailscale.com/docs/how-to/connect-vpc | official | 4 | B6 |
| S13 | Introducing auto approvers | https://tailscale.com/blog/auto-approvers | official | 4 | B10 |
| S14 | 4via6 subnet routers（网段重叠） | https://tailscale.com/docs/features/subnet-routers/4via6-subnets | official | 2 | B9 |
| S15 | Subnet routers and traffic relay nodes（KB 1019 存档） | https://web.archive.org/web/20240115023447/https://tailscale.com/kb/1019/subnets | official（存档） | 3 | B11 |

### B. 一手 issue / discussion / 仓库源码（8 条）

| ID | 标题 | URL | 层级 | 评分 | 来源视角 |
| --- | --- | --- | --- | --- | --- |
| S16 | Issue #430：Cannot access tailscale subnet with this addon（本地网段与目标网段冲突） | https://github.com/hassio-addons/app-tailscale/issues/430 | 一手 issue | 5 | C1 |
| S17 | Issue #415：Routing traffic from LAN to Tailscale not working | https://github.com/hassio-addons/app-tailscale/issues/415 | 一手 issue | 5 | A7,B13,C2 |
| S18 | Issue #216：Using addon for site-to-site with 2 HA instances do not work（容器网络限制） | https://github.com/hassio-addons/app-tailscale/issues/216 | 一手 issue | 5 | C3 |
| S19 | Issue #462：userspace_networking 需先启用再禁用（UI 陷阱） | https://github.com/hassio-addons/app-tailscale/issues/462 | 一手 issue | 5 | A5,C4 |
| S20 | Issue #96：Only one of two subnets is advertised | https://github.com/hassio-addons/app-tailscale/issues/96 | 一手 issue | 4 | A6,B14,C17 |
| S21 | tailscale#8370：site-to-site with 2 Home Assistant Addon nodes（上游仓库） | https://github.com/tailscale/tailscale/issues/8370 | 一手 issue | 4 | C9 |
| S22 | Discussion #449：MagicDNS 与 hassio_dns 解析冲突 | https://github.com/hassio-addons/app-tailscale/discussions/449 | 一手 discussion | 5 | A8,C10 |
| S23 | tailscale#13911：容器内 /proc/sys 只读，需 compose sysctls 设 ip_forward | https://github.com/tailscale/tailscale/issues/13911 | 一手 issue | 3 | B18 |

### C. 社区实操（HA 社区 / Tailscale 官方论坛，14 条）

| ID | 标题 | URL | 评分 | 来源视角 |
| --- | --- | --- | --- | --- |
| S24 | HAOS + Tailscale app subnet router（路由已批准、HA 终端仍不发包） | https://community.home-assistant.io/t/home-assistant-os-tailscale-app-subnet-router/1011394/3 | 5 | C6 |
| S25 | How to announce routes with Tailscale add-on（含控制台批准流程） | https://forum.tailscale.com/t/how-to-announce-routes-with-tailscale-add-on-in-home-assistant/4374/3 | 4 | A11,B16,C12 |
| S26 | Tailscale add-on - exit node & subnet access（完整 YAML 示例） | https://community.home-assistant.io/t/tailscale-add-on-exit-node-subnet-access/670635/12 | 4 | A12,B15,C18 |
| S27 | Tailscale + Subnets: How to access a different subnet? | https://community.home-assistant.io/t/tailscale-subnets-how-to-access-a-different-subnet/574372/10 | 3 | A15,C11 |
| S28 | HAOS + Subnets + Exit Node：ping 通但 HTTP 不通 | https://forum.tailscale.com/t/hoassio-tailscale-subnets-exit-node-not-passing-http-traffic-to-lan-cameras/3832 | 4 | C13 |
| S29 | Tailscale activated and not able to ping lan ip addresses | https://community.home-assistant.io/t/tailscale-activated-and-not-able-to-ping-lan-ip-addresses/826732 | 4 | C14 |
| S30 | Tailscale not working as expected?（accept_routes 解法） | https://community.home-assistant.io/t/tailscale-not-working-as-expected/452026/7 | 4 | C15 |
| S31 | 从 HA 侧用 MagicDNS 短名解析失败 | https://community.home-assistant.io/t/cannot-access-other-tailnet-device-from-ha-using-magicdns-name-tailscale/825664/3 | 4 | C19 |
| S32 | Companion app 内外网地址配置 | https://community.home-assistant.io/t/tailscale-ha-companion-app-internal-and-external-ip/912476/4 | 3 | A14 |
| S33 | Tailscale + HTTPS HA instance（serve 用法） | https://community.home-assistant.io/t/how-do-you-setup-tailscale-https-ha-instance/839023/9 | 4 | A13 |
| S34 | HAOS, Tailscale and ESPhome together（宿主机通、容器内不通） | https://community.home-assistant.io/t/home-assistant-os-tailscale-and-esphome-together/917118 | 3 | B17 |
| S35 | iOS App 经子路由访问 HA 失败（Safari/SSH 正常） | https://community.home-assistant.io/t/cant-access-ha-through-tailscale-subnet-router-with-ios-app-while-safari-and-ssh-are-ok/936707/6 | 4 | C7 |
| S36 | Home Assistant Addon: Tailscale（插件发布/讨论主帖） | https://community.home-assistant.io/t/home-assistant-addon-tailscale/965714/2 | 2 | A19 |
| S37 | [求助] HA 能远程访问，如何访问家里局域网 | https://bbs.hassbian.com/forum.php?mod=viewthread&tid=21702 | 3 | C21 |

### D. 博客 / 教程 / 分支实现（9 条）

| ID | 标题 | URL | 评分 | 来源视角 |
| --- | --- | --- | --- | --- |
| S38 | Tailscale Subnet Router and Asymmetric Routing on a Home LAN（系统化排错步骤） | https://docs.dev-eric.work/home-lab/tailscale-subnet-router-asymmetric-routing | 5 | C8 |
| S39 | lmagyar/homeassistant-addon-tailscale README + config.yaml（功能增强分支） | https://github.com/lmagyar/homeassistant-addon-tailscale/blob/main/README.md | 4 | A9,A10,C16 |
| S40 | Tailscale for Home Assistant（分步教程） | https://michal.cwiklin.ski/posts/Tailscale-for-Home-Assistant/ | 4 | A16 |
| S41 | 不露端口、拒绝云服务：用 Tailscale 远程控制 HomeAssistant（中文） | https://cloud.tencent.cn/developer/article/2705184 | 3 | C20 |
| S42 | Tailscale VPN to Access Your Home Assistant Server Remotely（MakeUseOf） | https://www.makeuseof.com/tailscale-vpn-access-home-assistant-server-remotely/ | 3 | A17 |
| S43 | Access HAOS remotely via Tailscale | https://medioker.utveckla.re/stuff/haos-tailscale/ | 3 | A18 |
| S44 | rayanamal/app-tailscale（派生插件仓库） | https://github.com/rayanamal/app-tailscale | 2 | A20 |
| S45 | Home Assistant: Sicheren Remote-Zugriff mit Tailscale（heise，德语） | https://www.heise.de/ratgeber/Home-Assistant-Sicheren-Remote-Zugriff-kostenlos-mit-Tailscale-einrichten-11196636.html | 3 | A21 |
| S46 | 外出先から自宅の HomeAssistant にアクセス（Qiita，日文） | https://qiita.com/NaNaRin/items/e16a71582a582e02e97b | 2 | A22 |

**层级分布**: 官方文档 15 / 一手 issue 与仓库源码 8 / 社区实操 14 / 博客教程与分支实现 9。

---

## 2. 三个视角的要点

### 视角 A｜HAOS 装插件 + 登录授权 + 内网穿透
- **存在两套并存插件**，授权方式不同：`hassio-addons/app-tailscale`（网页登录，社区常装的那套，S1）与 `hass-tailscale/hass-addons`（填 `auth_key`，S2）。零基础读者极易混用，P2 必须先确认「当前默认安装的是哪一套、登录是开网页授权还是填 key」。
- 官方正面材料偏薄：HA 官方站点只有 **集成页**（S4，只监控 tailnet 状态，**不能**做远程访问），插件文档实际托管在仓库（S1/S2），最接近的官方教程是 Tailscale 官方博客（S3）。
- 远程访问本身通常只需装插件 + 登录 + 用 `100.x:8123`（或 MagicDNS 名）即可，属于「内网穿透」部分；真正的难点全部集中在子路由（视角 C）。
- 手机 App 需分别填内网与外网地址（S32）；用 `serve` 可免端口访问（S33）。

### 视角 B｜Tailscale 子路由的官方机制
- 官方把子路由拆成四个必要条件：`advertise` → **控制台授权** → 控制面分发 → **客户端接受**（S8），任何一环缺失都表现为「配了没生效」，这是排错章节的骨架。
- 客户端接受侧：UI 的 **Use Tailscale subnets** 对应 CLI `--accept-routes`，**Linux 客户端默认不接受，Windows/macOS 默认接受**（S9）。
- subnets vs exit node 的边界清晰：子路由只暴露特定网段，exit node 捕获全部出站（S10）。
- **「1024 条路由限制」查无出处** —— 4 次定向检索（含精确关键词）均未在官方文档、GitHub issue 或 Headscale 文档中找到依据，只有无关的并发端口数 1024。**P2 不要采信该说法**，如需提及只能写成「官方未记载的软限制」。
- 内核态 vs 用户态路由的能力差异（S11）与 HAOS 插件的 `userspace_networking` 之间的实际关系，仍是空白。

### 视角 C｜HAOS 下的限制与排错（**本轮信息密度最高，也最关键**）
- **核心争议点**：HAOS 插件到底能不能当子路由？
  - 反面：S24（社区实测：路由已批准、Windows 能 ping 通，但 **HA 终端本身不发包**，结论是「HAOS 本身不做跨网段转发」）、S34（宿主机 ping 通、容器内 ping 不通）、S18（容器网络模式的限制）。
  - 正面：S17（维护者答复：`snat_subnet_routes: true` 时 LAN→tailnet 方向「just works」）、S38（不对称路由可系统性排查）。
  - **该问题直接决定笔记的章节结构，是 P2 必须先拍板的第一优先级。**
- 高频失败点清单（均有一手来源，待 P2 核实细节）：本地网段与目标网段冲突且可能软砖 HA（S16）、`userspace_networking` 的 UI 显示与实际配置不一致（S19）、只广播第一个子网（S20）、控制台未批准路由（S25）、MagicDNS 与 `hassio_dns` 解析冲突/环路（S22、S31）、ping 通但 HTTP 不通（S28）、客户端侧权限问题（S35）、容器内无 `tailscale` 命令（S27）。
- **替代方案**已浮现：换用功能增强分支（S39）、由另一台 Linux/Windows 节点承接子路由（S28）、改用 HAOS 虚拟机 + Supervised 迁移（S24）。

---

## 3. 方向菜单（待选择）

| 方向 | 内容 | 结构预估 | 适合 |
| --- | --- | --- | --- |
| **A. 全链路实战主线**（推荐） | 插件安装与登录授权 → 内网穿透（远程访问 HA 与内网服务）→ 子路由（含能力边界判定与替代方案）→ 失败点排查清单 | 约 6 章 | 与已确认的「实战 / 上手 / 零基础」定位一致，交付一份能照做的完整文档 |
| **B. 聚焦子路由能力边界** | 只回答一个问题：HAOS 插件能否做子路由、在什么条件下可以、不行时怎么办（含上游 issue 与社区争议、替代架构） | 约 4 章，深度更高 | 若你更关心「这件事到底行不行」而不是安装步骤 |
| **C. 排错手册优先** | 以失败点清单为主线组织（约 10–15 条 → 逐条排查），安装步骤压缩为附录 | 约 5 章 | 若你接下来要动手调试，需要一份对照表 |

**可组合**：A + C（主线 + 附录式排错表）是常见做法，也是 fnOS 那篇的形态。

---

## 4. 覆盖缺口与 P2 必查项

1. **HAOS 插件 manifest 层面的网络模式**（host 网络 vs 独立容器网段、能否看见家庭 LAN 网段）——无一手证据，只有 S18 的间接描述。
2. **「HAOS 不做跨网段转发」这一结论的适用范围**——S24/S34 是个案还是普遍限制？与 S17 维护者说法是否矛盾？
3. **当前默认插件的确定身份与版本**：S1 与 S2 谁是主流？HA 2026.8 将「Add-ons 改名为 Apps、HTTP 代理设置迁移」的说法**只出现在搜索摘要中**，必须回 S3 与 HA 官方 release notes 复核。
4. **重启/升级后路由丢失**——仅社区单一说法，无 issue 或 changelog 佐证。
5. **与 HA `http` / `use_x_forwarded_for` / `trusted_proxies` 的交互**——只找到 Funnel/Serve 场景，缺「子路由 + 反代」组合下 400 的一手记录。
6. **中文一手材料近乎缺位**（S37/S41 信息密度低）。
7. 本轮 46 条**全部只读搜索摘要**，`advertise_routes` / `snat_subnet_routes` / `userspace_networking` 等选项名的准确拼写与行为必须回 S1/S39 原文核对。

---

## 5. P2 深度收集预估范围

**核心必取（T1，约 6 条）**：S1（插件官方文档，最贴合本场景的一手配置口径）、S6 + S8 + S9（子路由机制与四个必要条件）、S17 + S24（「能不能做子路由」的正反两面一手证据）、S38（不对称路由系统化排错）。

**补充取用（T2，约 4–6 条）**：S3（官方安装教程 + 版本变化复核）、S16/S19/S20/S22（四个高频失败点各取一手 issue）、S25 或 S26（社区配置写法交叉验证）、S39（功能增强分支作为替代方案）。

**规模预估**：10–12 条核心来源，覆盖官方文档 5–6 条 + 一手 issue 5–6 条 + 社区实操 2–3 条。预计 `02_deep_research.md` 产出 8–12 个主题块（其中「HAOS 能否做子路由」单列一块，含正反证据与判定条件）。
