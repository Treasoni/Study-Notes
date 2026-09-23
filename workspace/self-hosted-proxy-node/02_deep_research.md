# 02 深度素材 - 自建代理节点

## 元信息

- **运行标识**: self-hosted-proxy-node
- **工作流 / 阶段**: learning-note-flow / P2 深度收集
- **选定方向**: B（内核直配，概念与字段对齐）
- **篇幅预期**: 中等（5-7 章，约 6000-9000 字）
- **精读日期**: 2026-09-23
- **信源构成**: **全部 tier-1**（官方文档 / 官方仓库 / 规范原文），**无 tier-2 / tier-3 混入**
- **信源数量**: 12 个来源 ID（13 个本地缓存文件；S-3 仅有 URL 未下载）
- **抽取方式**: 4 个抽取代理并行产出论断级笔记，每条带锚点；逐字引用与 inference 严格分离

## 覆盖范围

| 已覆盖 | 未覆盖（见「开放问题」） |
| --- | --- |
| 协议层 / 传输层 / 安全层的分层与组合约束 | 分享链接与订阅格式（无 tier-1 规范） |
| REALITY 的设计意图、鉴权与回落语义、字段 | 协议横向对比（无官方对照文档） |
| 官方 VLESS + XTLS Vision + REALITY 服务端与客户端配置结构 | 面板侧端到端首入站教程 |
| 单机 VPS 硬化的官方流程与工具定位 | 客户端 GUI 工具（未纳入本次方向） |

## 信源表（含本地缓存路径）

本地缓存根目录：`workspace/self-hosted-proxy-node/sources/`

| ID | 标题 | URL | tier | 本地文件 |
| --- | --- | --- | --- | --- |
| S-1 | Xray 传输配置（传输方式 / 传输安全 / 附加配置） | https://xtls.github.io/config/transport.html | tier-1 | `02_xtls_github_io.md`、`DOCSRC_transport.md`（仓库原文，权威） |
| S-2 | REALITY 官方配置文档 | https://xtls.github.io/config/transports/reality.html | tier-1 | `01_xtls_github_io.md`（代码块截断）、`DOCSRC_reality.md`（仓库原文，权威） |
| S-3 | RFC 8446: TLS 1.3 | https://www.rfc-editor.org/rfc/rfc8446.txt | tier-1 | 未下载（仅作背景引用，未精读） |
| S-6a | Xray-examples 服务端配置（VLESS-TCP-XTLS-Vision-REALITY） | https://github.com/XTLS/Xray-examples | tier-1 | `S6_..._config_server.jsonc` |
| S-6b | Xray-examples 客户端配置（同上目录） | https://github.com/XTLS/Xray-examples | tier-1 | `S6_..._config_client.jsonc` |
| S-6c | Xray-examples REALITY 设计说明（英文） | https://github.com/XTLS/Xray-examples | tier-1 | `S6_..._REALITY.ENG.md` |
| S-10 | Debian 管理员手册 第 14 章（总览 + 14.1） | https://debian-handbook.info/browse/stable/security.html | tier-1 | `04_debian-handbook_info.md` |
| S-10a | 同上 14.2 防火墙与包过滤 | https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html | tier-1 | `02_debian-handbook_info.md` |
| S-10b | 同上 14.3 监督：预防 / 检测 / 威慑 | https://debian-handbook.info/browse/stable/sect.supervision.html | tier-1 | `03_debian-handbook_info.md` |
| S-10c | 同上 14.7 处理被入侵的机器 | https://debian-handbook.info/browse/stable/sect.dealing-with-compromised-machine.html | tier-1 | `01_debian-handbook_info.md` |
| S-11 | fail2ban 官方仓库 README | https://github.com/fail2ban/fail2ban | tier-1 | `S11_fail2ban_README.md` |
| S-12 | Linux Kernel Documentation — IP Sysctl | https://docs.kernel.org/networking/ip-sysctl.html | tier-1 | `03_docs_kernel_org.md` |

> **命名注意**：补抓导致 Debian 手册三个小节的本地文件序号与前缀与其他来源重排，上表路径为准，不要按文件名顺序推断内容。

---

## 一、概念层：三层分工与组合约束（S-1）

**分层总纲**

- `streamSettings` 只管「代理协议之外的数据传输部分」，分为**承载方式、安全机制、附加行为**三类，分属不同层次且可组合。引用：「它配置的是代理协议之外的数据传输部分，如承载方式、安全机制及附加行为。」（S-1 / 传输配置）
- 需要协商的传输配置**要求两端兼容**：「一端使用 WebSocket，另一端也必须使用 WebSocket，否则无法建立通信。」（S-1）——这是服务端与客户端配置必须对齐的根本原因。
- `streamSettings` 是 `InboundObject` / `OutboundObject` 的子项，「每一个入站或出站都可以分别配置不同的传输配置」（S-1）——所以服务端能给不同入站挂不同传输组合。
- 直接出站（Freedom）**不协商**，只控制本地发连接的行为，「此时只有 `sockopt` 可用」（S-1）。

**承载方式（method）**

- 取值域：`raw | xhttp | mkcp | grpc | websocket | httpupgrade | hysteria`，**默认 `raw`**（S-1）。
- 每种方式有专属 Settings 字段（`rawSettings` / `xhttpSettings` / `kcpSettings` / `grpcSettings` / `wsSettings` / `httpupgradeSettings` / `hysteriaSettings`），**只在对应 method 下生效，其余写了也被忽略**（S-1）。

**安全层（security）**

- 取值域：`none | reality | tls`，**默认 `none`**（S-1）。
- TLS 由 Golang 实现，通常协商为 TLS 1.3，不支持 DTLS；**与全部七种承载方式都能组合**，是兼容性最好的安全层（S-1）。
- 硬约束（据官方速查表归纳，inference / confidence: high）：
  - `hysteria` 承载下 security **必须为 `tls`**，`none` 与 `reality` 均不支持；
  - `raw` / `xhttp` / `grpc` 三者在 `none` / `tls` / `reality` 下均支持，是服务端最稳的组合；
  - REALITY 仅支持与 `RAW`、`XHTTP`、`gRPC` 组合（S-1 与 S-2 互相印证）。

**一条重要的官方注脚（对「为什么必须加密」很有用）**

- `security = none` 时，VLESS（未启用 Encryption）与 Trojan **仅允许连接私网**；且仅靠 VLESS Encryption 没有 TLS / REALITY 外观，不适合直接用于公网穿行（S-1 注 [3][4]）。

**附加配置层**

- 只有两个字段：`finalmask`（对流量的最终伪装）与 `sockopt`（底层网络行为），不参与两端协商，属本地行为控制（S-1，confidence: medium）。

---

## 二、REALITY 原理（S-2、S-6c）

**官方定义**

- 「REALITY 是对 TLS 的一种修改，通过借用目标站点的 TLS 外观与握手特征来完成伪装。」（S-2）——**不是新协议，而是 TLS 的变体**。
- 实现层面：服务端是 Go 1.19.5 标准库 `tls` 包的 fork（S-6c）；客户端参考实现是 Xray-core 的 `transport/internet/reality/reality.go`（S-6c）。

**替代 TLS 的官方收益**（S-6c，逐字引用）：

> By replacing TLS with REALITY, **you can eliminate server-side TLS fingerprint characteristics**, maintain forward secrecy, **and render certificate chain attacks ineffective**.

即：消除服务端 TLS 指纹特征、保持前向保密、使证书链攻击失效；并可**指向另一个网站而无需购买域名或配置 TLS 服务器**，在整个 TLS 握手过程中呈现指定 SNI（S-6c）。

**目标站要求**（S-6c）

- 最低要求：境外网站、支持 TLSv1.3 与 H2、域名不发生重定向（主域可能重定向到 www）。
- 加分项：IP 与目标站邻近（延迟更低、特征更相似）、Server Hello 之后的握手报文已加密（如 `dl.google.com`）、支持 OCSP Stapling。
- 官方提示：REALITY 对外表现如同端口转发，用于**不常见的目标 IP 可能更合适**。

**鉴权与回落语义（概念章的关键难点）**

- 「为了伪装的效果考虑，Xray 对于鉴权失败（非合法 REALITY 请求）的流量，会**直接转发**至 `target`。」（S-2）——即**不拒绝，而是替你转发**，这正是伪装成立的原因。
- 代价（inference / confidence: medium）：若 `target` 是 Cloudflare 这类 CDN，本机相当于替其做端口转发，可能被扫描而偷跑流量；缓解方式是前置 Nginx 按 SNI 过滤，或用 `limitFallbackUpload` / `limitFallbackDownload` 限速（S-2）。
- 官方同时提醒：**回落限速本身是一种特征，不建议启用**，面板类工具应随机化这些参数（S-2）。
- 客户端三种证书分支（S-6c）：
  1. 收到**临时可信证书**（由临时认证密钥签发，服务端通过鉴权后自行生成）→ 连接正常可用；
  2. 收到**真实证书**（服务端拒绝了 Client Hello 并把流量转到目标站 / 中间人转发 / 证书链攻击）→ 客户端**进入 spider 模式**；
  3. 收到**无效证书** → 触发 TLS alert 并终止连接。

**兼容性警告（S-6c）**

> REALITY can also be used in conjunction with proxy protocols other than XTLS, but it is **not recommended** as they exhibit clear **TLS-in-TLS** characteristics that have already been targeted.

即：REALITY 可与 XTLS 之外的协议组合，但**不推荐**——会呈现明显的 TLS-in-TLS 特征且已被针对。

**路线图（S-6c）**：REALITY 的下一目标 `prebuilt mode`（预先收集目标网站特征）；XTLS 的下一目标是 0-RTT。

---

## 三、首入站配置：VLESS + XTLS Vision + REALITY（S-2、S-6a、S-6b）

**服务端必要字段（S-2，逐字引用见括号）**

| 字段 | 要求 | 语义 |
| --- | --- | --- |
| `target` | 必填 | 格式同 VLESS fallbacks 的 `dest`，旧称 `dest`（互为别名）。**Xray 以该字段是否存在区分客户端/服务端配置，客户端绝不能填**：「不要在客户端填写，否则会造成识别异常。」 |
| `serverNames` | 必填 | 允许客户端使用的 serverName 列表，「不支持 `*` 通配符」；一般与 target 一致或取 target 证书的 SAN；列表可含空值表示接受无 SNI 连接。 |
| `privateKey` | 必填 | 「执行 `./xray x25519` 生成」；其对应公钥即客户端 `password`，两侧必须配对。 |
| `shortIds` | 必填 | 用于区分不同客户端；列表含空值时客户端 `shortId` 可为空。 |

**客户端必要字段（S-2、S-6b）**

| 字段 | 要求 | 语义 |
| --- | --- | --- |
| `password` | 必填 | 「服务端私钥对应的公钥」，用 `./xray x25519 -i 服务器私钥` 生成；**旧称 `publicKey`**，为防误解更名。 |
| `serverName` | 必填 | 取服务端 `serverNames` 之一；「客户端可以将其设置为任意 IP 地址，Xray 将会发送无 SNI 扩展的 Client Hello」，前提是服务端 `serverNames` 中含空值。 |
| `shortId` | 必填 | 必须是服务端 `shortIds` 列表中的一项；取值 0-f，「长度为 2 的倍数，最大长度 16」，奇数位报错（`aa1234` 自动补 0 为 `aa12340000000000`，`aaa1234` 报错）。 |
| `fingerprint` | 必填 | 作用同 TLSObject 的指纹选项；**REALITY 下不支持用 `unsafe` 禁用 uTLS**：「因为 REALITY 协议实现使用了该库以操作底层 TLS 参数。」 |
| `spiderX` | — | 爬虫初始路径与参数；dest 为 `1.1.1.1:443` 时可填 `/dns-query/` 或留空。 |

**官方示例的服务端骨架（S-6a）**

- `inbounds[0]`：只写 `port: 443`（无 `listen`，默认监听全部地址）、`protocol: "vless"`；`streamSettings` 为 `network: "tcp"`、`security: "reality"`。
- `settings.decryption` 固定 `"none"`（VLESS 服务端必填占位值）。
- `settings.clients[0]`：`id` 为 UUID（注释给出 `xray uuid` 生成）、`flow: "xtls-rprx-vision"`。
- `realitySettings.dest`：注释写明「A website that support TLS1.3 and h2. You can also use `1.1.1.1:443` as dest」。
- `realitySettings.serverNames`：必须是 dest 站点证书里的名字（SAN）；dest 用 `1.1.1.1:443` 时可留空。
- `sniffing`：开启 `destOverride: [http, tls, quic]` 且 **`routeOnly: true`**（只用嗅探结果做路由，不改写目标地址）。
- `outbounds`：只有一个 `freedom` 出站（`tag: "direct"`）——伪装与回落不依赖额外出站配置。

**官方示例的客户端骨架（S-6b）**

- `inbounds[0]`：本地 SOCKS，`listen: 127.0.0.1`、`:10808`，`settings.udp: true`。
- `outbounds[0]`：`protocol: "vless"`，填 `address` / `port` / `id` / `encryption: "none"` / `flow: "xtls-rprx-vision"`，`tag: "proxy"`。
- `id` 注释写明「Needs to match server side」——必须与服务端 `clients[0].id` 一致。
- 传输层与服务端**结构对称**（`network: tcp` + `security: reality`），差异只在 `realitySettings` 内用哪一组字段（服务端用 target/privateKey/serverNames，客户端用 serverName/publicKey/shortId/fingerprint/spiderX）。

**flow 的约束（S-6c）**：`flow: "xtls-rprx-vision"` 为可选，「if specified, clients must enable XTLS」——一旦指定，客户端必须启用 XTLS。

**官方进阶字段（S-2，未在示例出现）**：`mldsa65Seed` / `mldsa65Verify`（后量子签名）、`xver`、`maxClientVer` / `minClientVer` / `maxTimeDiff`（版本与时间校验）、`show`。

---

## 四、VPS 硬化与运维（S-10 系列、S-11、S-12）

**安全策略先行（S-10 / 14.1）**

- 风险模型三要素：**要保护什么、要防止什么发生、谁会尝试使其发生**；三者回答清楚后才谈策略。
- 「Security is a process, not a product」——受保护资产、威胁与攻击者手段随时间变化，策略必须演进。
- 分而治之：信息系统可切分为基本独立的一致子系统，各自需求与约束分别评估。
- 「A short and well-defined perimeter is easier to defend than a long and winding frontier.」——敏感服务集中在少量机器、只经最少检查点访问。
- 官方立场（inference / confidence: medium）：对单台 VPS，**优先让服务不监听不该开放的接口、直接停用并卸载不需要的服务**，包过滤只作为补充手段，而非唯一防线。

**防火墙（S-10a / 14.2）**

- 「Since Debian Buster, the nftables framework is used by default.」——旧 `iptables` 命令已改用 nftables 内核 API。
- nftables **没有默认表**，由用户自建；每个表必须且只能属于 `ip` / `ip6` / `inet` / `arp` / `bridge` 五个 family 之一，未指定时默认 `ip`。
- 链分两类：**base chain** 是网络栈的数据包入口（注册进 Netfilter hook 才看得到流量）；**regular chain** 不挂 hook，只能作为 `jump` 目标用于组织规则。
- verdict 取值：`accept`、`drop`、`queue`、`continue`、`return`、`jump chain`、`goto chain`。
- **持久化**：「The executed `nft` commands do not make permanent changes to the configuration, so they are lost if they are not saved.」规则文件在 `/etc/nftables.conf`，`nft list ruleset > /etc/nftables.conf` 可保存。
- **开机装载**：「To enable a default firewall in Debian, you need to store the rules in `/etc/nftables.conf` and execute `systemctl enable nftables` as root.」
- 临时停用防火墙：`nft flush ruleset`。
- 语法：`nft add rule [family] table chain handle handle statement`；`add` 追加到链尾，`insert` 插到链首或指定 handle 之前。
- 迁移：`iptables-translate` / `ip6tables-translate` 翻译单条命令；`iptables-save` + `iptables-restore-translate` 整份迁移；`iptables-nft` 等「these tools should only be used for backwards compatibility」。

**监控（S-10b / 14.3）**

- `logcheck`：默认**每小时**检查日志并以邮件发异常；文件清单在 `/etc/logcheck/logcheck.logfiles`；三种模式 paranoid / **server（默认，推荐多数服务器）** / workstation。规则目录：`cracking.d/`（判定入侵尝试）、`cracking.ignore.d/`、`violations.d/`、`violations.ignore.d/`。
- 实时排查：`top` 显示进程，「An unknown process running as the `www-data` user should really stand out and be investigated」——重点看资源占用是否与机器已知承载的服务相符。
- **AIDE**：以基线库 `/var/lib/aide/aide.db` 比对文件指纹 / 权限 / 时间戳；`aideinit` 初始化，`/etc/cron.daily/aide` 每日校验，变化写 `/var/log/aide/*.log` 并邮件通知；新库在 `aide.db.new`。局限：「a thorough attacker will therefore update these files」——拿到 root 的攻击者可替换基线库掩盖痕迹，缓解办法是把参考数据放在只读介质上。
- `dpkg --verify`（`dpkg -V`）：可找出被改动的已安装包文件，但校验和取自本机 `/var/lib/dpkg/info/*.md5sums`，**有 root 的攻击者会同步更新**，结果需谨慎对待。
- `suricata`（NIDS）：监听网络发现渗透与敌意行为（含 DoS），日志在 `/var/log/suricata`；配置 `/etc/suricata/suricata.yaml` 最小要求设 `HOME_NET` 与监控 `interface`，建议设 `LISTENMODE=pcap`（默认 `nfqueue` 还需在 netfilter 上配 NFQUEUE 转发）。**有效性受限于被监控网卡实际看到的流量**。

**fail2ban（S-10b 权威 + S-11 安装说明）**

- 官方定位（S-10b）：「The best way to stop a brute-force attack is to limit the number of login attempts coming from the same origin, usually by temporarily banning an IP address.」这正是 Fail2Ban 的定位——监控任何把登录尝试写入日志的服务。
- 机制（S-11）：「Fail2Ban scans log files like `/var/log/auth.log` and bans IP addresses conducting too many failed login attempts.」实现方式是更新系统防火墙规则拒绝来自这些 IP 的新连接；开箱即用支持 sshd、Apache 等标准日志。自 v0.10 起支持 IPv6。
- 能力边界（S-11）：「Though Fail2Ban is able to reduce the rate of incorrect authentication attempts, it cannot eliminate the risk presented by weak authentication.」原文建议真要保护服务就用双因素或公私钥认证。S-10b 另指出它**无法应对分布式暴力破解**。
- 配置文件四类（S-10b，均在 `/etc/fail2ban/`）：`fail2ban.conf`（全局）、`filter.d/*.conf`（如何识别认证失败）、`action.d/*.conf`（封禁/解封命令）、`jail.conf`（filter + action 的组合即 jail）。
- **运维约定（S-10b）**：「the main configuration file `/etc/fail2ban/jail.conf` is not supposed to be altered」——启用/配置 jail 要写在 `/etc/fail2ban/jail.d/defaults-debian.conf` 或同目录文件，以免升级被覆盖。
- **默认参数语义（S-10b，示例为 sshd jail）**：`bantime = 10m`（封禁时长）、`findtime = 10m`（统计窗口）、`maxretry = 5`（触发阈值）——「If Fail2Ban detects five failed login attempts within 10 minutes, it will ban the IP address where those attempts originated for 10 minutes.」检测正则在 `filter.d/sshd.conf`，日志路径取变量 `sshd_log`。
- 安装（S-11）：多数发行版已打包；源码安装要求 Python >= 3.5 或 PyPy3。可执行脚本装到 `/usr/bin`，配置在 `/etc/fail2ban`。验证用 `fail2ban-client -h`、`fail2ban-client version`。**「You should always use fail2ban-client and never call fail2ban-server directly.」**
- **安装方式冲突（重要，见「矛盾与注意点」）**：S-11 面向源码安装（init.d 步骤、需手动复制 service 脚本）；S-10b 面向 Debian 包（apt + systemd）。笔记必须区分，否则照抄会得到过时步骤。

**拥塞控制（S-12）**

- `tcp_congestion_control`（STRING）：设置新连接使用的拥塞控制算法；「The algorithm `reno` is always available, but additional choices may be available based on kernel configuration.」默认值由内核配置阶段决定。
- 被动连接（入站）**继承监听套接字的选择**：「For passive connections, the listener congestion control choice is inherited.」
- `tcp_available_congestion_control`（STRING，只读）：显示**已注册**的可用算法；「More congestion control algorithms may be available as modules, but not loaded.」
- `tcp_allowed_congestion_control`（STRING）：显示/设置**非特权进程**可用的选项，是上者的子集。
- 切换算法的前提（inference / confidence: medium）：目标算法须出现在 `tcp_available_congestion_control`（模块已加载）中；若非特权进程选择，还须在 `tcp_allowed_congestion_control` 白名单内。
- **内核文档全文未点名 BBR**，选型依据需另找信源（见开放问题）。
- `tcp_ecn`（INTEGER）：仅在连接两端都表示支持时使用，作用是让支持的路由器在不得不丢包前发出拥塞信号；协商选择双方都支持的最高反馈变体。
- `tcp_slow_start_after_idle`（BOOLEAN）：启用时按 RFC2861 行为，空闲期后使拥塞窗口超时（空闲期以当前 RTO 界定）；关闭则空闲后不重置窗口。

**被入侵后的处置（S-10c / 14.7）——处置顺序**

1. **发现线索**（14.7.1）：入侵常在影响正常服务后才被发现（连接变慢、用户连不上）；典型线索是不该存在的进程（例：进程名 `apache` 而非标准的 `/usr/sbin/apache2`）。用 `ls -al /proc/<pid>/exe` 看真实可执行文件路径——官方示例中符号链接指向 `/var/tmp/.bash_httpd/psybnc` 却以 `www-data` 身份运行，即可断定被入侵。其他迹象：命令选项突然失效、命令自称版本与 `dpkg` 记录不符、会话欢迎信息显示最后连接来自未知服务器。
2. **断网**（14.7.2）：「Unplugging the computer from the network will prevent the attacker from reaching these targets」——攻击者需要可用网络才能达成目标（窃取数据、分享非法文件、把机器当跳板）。物理不可达（异地托管）时，顺序是**先采集重要信息**，再尽量关停服务（通常除 `sshd` 外全部停掉）；该场景仍棘手，因为不能排除攻击者与管理员一样拥有 SSH 访问权。
3. **保全证据**（14.7.3）：至少三类——硬盘内容、全部运行进程列表、全部开放连接列表。在受感染机器上检查应限于最小命令集（`netstat -tupan`、`ps auxf`、`ls -alR /proc/[0-9]*`），且每条命令都要记录——「Every command is potentially subverted and can erase pieces of evidence.」避免在运行中的系统做「热分析」：「quite simply you can't trust the programs currently installed on the compromised system」（被替换的 `ps` 可隐藏进程、`ls` 可隐藏文件，甚至内核也可能被篡改）。磁盘镜像前必须先只读重挂载，最简做法是 `sync` 后强行关机并从救援 CD 启动，各分区用 `dd` 复制。
4. **重装**（14.7.4）：「The server should not be brought back on line without a complete reinstallation.」若已取得管理员权限，几乎只有重装才能清除一切（尤其后门），并须打齐安全更新。「Care should be taken not to reinstall the machine from backups taken later than the compromise.」理想情况是只恢复数据，软件从安装介质重装。
5. **取证分析**（14.7.5）：挂载镜像必须带 `ro,nodev,noexec,noatime` 以免改变内容（含访问时间戳）或误运行被篡改程序。入手点是查「被修改与被执行」的一切：`.bash_history`、近期创建/修改/访问的文件、用 `strings` 提取二进制文本串、`/var/log` 重建时间线、`sleuthkit`（配 Autopsy）恢复被删文件。**分析目标是定位漏洞**，从而确认新装确实修复了它。

---

## 五、矛盾、别名与注意点

1. **字段新旧命名（写作必须交代，否则读者对不上旧教程）**
   - 服务端：`target` ↔ 旧称 `dest`（互为 alias）
   - 客户端：`password` ↔ 旧称 `publicKey`（为防误解更名）
   - 官方示例文件（S-6a/S-6b）仍用 `dest` / `publicKey`；xtls 文档（S-2）用 `target` / `password`。**两处都出现在 tier-1 官方来源里**，不是错误，是改名过渡。
2. **抓取版 vs 文档仓库原文的字段缺失**：爬取 `reality.html` 得到的 `01_xtls_github_io.md` 中 `RealityObject` 示例代码块被截断；改取仓库 markdown 原文（`DOCSRC_reality.md`）后完整，并暴露出抓取版**漏掉的字段**：`show`、`mldsa65Seed`、`minClientVer` / `maxClientVer` / `maxTimeDiff`。**字段表一律以 `DOCSRC_*.md` 为准。**
3. **fail2ban 安装方式的两种口径**：S-11 README 面向**源码安装**（需手动复制 init 脚本、`update-rc.d`）；S-10b 面向 **Debian 包**（apt 安装 + systemd）。结论：**笔记按 apt + systemd 写，并把 README 的 init.d 步骤明确标注为源码安装路径**，避免读者照抄到过时步骤。
4. **处置顺序的官方交叠**（S-10c）：14.7.4「重装」在 14.7.5「取证分析」之前，但 14.7.5 分析的是磁盘镜像——两部分次序有交叠。写作时须显式说明：**先成像保全，再重装恢复服务，分析可在成像后并行进行**，不要机械按小节号排序。
5. **`security=none` 的限制 vs REALITY 的必要性**：S-1 指出 `none` 时 VLESS（无 Encryption）与 Trojan 仅允许私网；S-6c 指出非 XTLS 协议配 REALITY 会呈现 TLS-in-TLS 特征。两条合起来正好解释「为什么当前主线是 VLESS + XTLS Vision + REALITY」。
6. **回落限速是双刃剑**：`limitFallbackUpload` / `limitFallbackDownload` 能防偷跑，但官方明说**限速本身是特征、不建议启用**（S-2）。写作时不能只讲「建议开启限速」。

## 六、开放问题与缺口

| # | 缺口 | 影响 | 处理建议 |
| --- | --- | --- | --- |
| 1 | **分享链接与订阅格式无 tier-1 规范原文**（`vless://` 参数集、base64 订阅列表） | 客户端导入章节若要写，无权威依据 | 按已确认方案**标注为 tier-2/3 且非规范**；或从笔记剔除该节 |
| 2 | **BBR 未在内核文档中独立出现** | 「开启 BBR」章节缺权威依据 | 内核侧只用 S-12 讲清三个拥塞控制字段语义；BBR 本身标注为待补 tier-2 信源，或只给参数名不给性能断言 |
| 3 | **`tcp_ecn` 取值表数值列在抓取中丢失** | 无法断言各数值语义 | 只写可从文件确认的「Default: 3」与作用描述；数值语义回原文核对后再写 |
| 4 | **Debian 手册未给面向 VPS 的现成规则集**（S-10a 只有语法与装载方式） | 无法直接引用一份「官方推荐规则」 | 规则集按最小开放原则自行编写，并**标为 inference**；或补 tier-2 信源 |
| 5 | **fail2ban 默认值的官方出处**：S-11 README 未给默认 jail / maxretry / findtime / bantime | — | **已由 S-10b 补上**（10m / 10m / 5），无需再用 README |
| 6 | **协议横向对比无官方对照文档** | 概念章无法引用对比表 | 若需要，只能从各协议页面分别汇总，**标为 inference** |
| 7 | **「脏 IP」判定无 tier-1 规范原文** | 选购章节的依据不足 | 标为经验性判断；引用黑名单运营方工具页（Spamhaus）时说明其偏邮件信誉视角 |
| 8 | **面板侧无端到端首入站官方教程** | 本次方向 B 不涉及面板，暂不影响 | 若后续想加面板章节需跨源拼合 |
| 9 | **S-3（RFC 8446）未精读** | 概念章讲 TLS 1.3 握手时无逐字引用 | 只作背景引用；如需展开须先精读对应小节 |
| 10 | **Marzban 生态变动**：主仓 2026-06 后趋于停滞，`Marzban-node` 已被维护者明示不再支持，指向 `M03ED/gozargah-node` | 若笔记涉及多节点方案会过时 | 本次方向 B 不涉及；若涉及须按当前状态描述，不得沿用旧教程 |

## 七、给下游写作的交接

**给 outline-generator（阶段 3）**

- 概念章素材充足且全部有 tier-1 依据（S-1 分层与组合约束、S-2/S-6c REALITY 原理与回落语义）。用户明确要求「先讲概念再实战」，**概念章可支撑 2 章**。
- 实战章建议按官方示例的真实结构展开：服务端 → 客户端 → 连通校验。所有字段名以 `DOCSRC_reality.md` / `DOCSRC_transport.md` 与 `S6_*` 示例为准。
- 硬化/运维建议压缩为 1 章（S-10 系列素材量大，按需取用，不必全塞）。
- 中等篇幅目标 5-7 章、6000-9000 字。

**给 chapter-writer（阶段 4）**

- 引用规则：`type: quote` 的内容可逐字引用；`type: inference` 的内容**必须显式标为「据官方文档归纳」或「推断」**，不得写成官方口径。
- 字段表格直接引自本文件的字段表；**不要从抓取版 `01_xtls_github_io.md` 抄字段**（有缺失）。
- 涉及新旧命名的章节，必须在首次出现时说明 `target`/`dest`、`password`/`publicKey` 的别名关系。
- 不确定的版本行为标"未核实"，不要补全。

**禁止事项（全流程适用）**

- 不提供具体获取渠道、订阅链接、机场推荐或任何规避网络监管的操作指引。
- 不做性能断言（吞吐/延迟/存活期数字），除非有可引用信源；本轮实测类数据一律未采纳。

**本地信源路径（写作时按需定点读，不要整篇加载）**

```text
workspace/self-hosted-proxy-node/sources/DOCSRC_reality.md      # REALITY 字段权威（完整）
workspace/self-hosted-proxy-node/sources/DOCSRC_transport.md    # 传输三层与兼容表（完整）
workspace/self-hosted-proxy-node/sources/S6_..._config_server.jsonc
workspace/self-hosted-proxy-node/sources/S6_..._config_client.jsonc
workspace/self-hosted-proxy-node/sources/S6_..._REALITY.ENG.md  # 设计意图与回落语义
workspace/self-hosted-proxy-node/sources/02_debian-handbook_info.md  # 14.2 防火墙
workspace/self-hosted-proxy-node/sources/03_debian-handbook_info.md  # 14.3 监控
workspace/self-hosted-proxy-node/sources/01_debian-handbook_info.md  # 14.7 入侵处置
workspace/self-hosted-proxy-node/sources/03_docs_kernel_org.md       # IP Sysctl（只读 TCP variables 节）
```
