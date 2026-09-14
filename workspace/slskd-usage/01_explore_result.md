# slskd 探测结果（Phase 1）

## 元信息

- **run_id**: slskd-usage
- **探测时间**: 2026-09-14
- **探测方式**: 3 个 subagent 并行探测（部署与运行 / 账号·共享·网络规则 / 日常使用与配置安全）
- **版本锚点**: 最新 release `0.26.0`（2026-07-19），open issue 174
- **硬性约束**: 每条结论必须附来源 URL；无法核对的标「待核对」；来源冲突时并列呈现，不单向取信

---

## 一、方向概览

| 方向 | 官方一手资料 | 社区/issue 补充 | 资料厚度 | 建议 |
| --- | --- | --- | --- | --- |
| ① 部署与运行 | 充足（docker.md / config.md / Dockerfile / CI / migrations.md / known_issues.md） | 充足（Unraid、TrueNAS、群晖、权限类 issue） | ★★★★★ | 作为主线第 1 部分 |
| ② 账号 / 共享 / 网络规则 | 中等（config.md 各节 + slsknet.org 官方规则/FAQ） | 中等（issue #330 / #532 / #908 / #440） | ★★★★ | 作为主线第 2 部分（差异化重点） |
| ③ 日常使用与配置安全 | 配置面充足（config.md / example.yml）；**Web UI 操作面几乎为零** | 充足（高频 issue 排行、反代、VPN、API/MCP） | ★★★★ | 配置详解放第 3 部分，UI 操作面需降级处理 |

**总体判断**：官方文档的**配置面**极强（`config.md` 85 KB + `example.yml`），但**操作面**（Web UI 怎么用）官方几乎没写 —— 这是本笔记必须直面的结构性缺口。

---

## 二、方向 ① 部署与运行

### 2.1 官方主路径

- Quick Start 给 `docker run` 与 compose 两种写法，固定暴露三端口：`5030`(HTTP UI)、`5031`(HTTPS 自签)、`50300`(Soulseek 入站)；默认账号密码均为 `slskd`/`slskd` —— [README#quick-start](https://github.com/slskd/slskd#quick-start)
- 官方 docker.md 开篇列**四个必做决策**：Web UI 端口、50300 入站端口、应用数据目录、**容器以什么用户运行**（直接影响下载文件属主）—— [docs/docker.md](https://github.com/slskd/slskd/blob/master/docs/docker.md)
- 容器内应用目录默认 `/app`（镜像内写死）；`APP_DIR` **只能经环境变量/命令行设置，不能写在 YAML 里** —— [config.md](https://github.com/slskd/slskd/blob/master/docs/config.md)
- 下载/未完成目录默认 `APP_DIR/downloads` 与 `APP_DIR/incomplete`，可被 `SLSKD_DOWNLOADS_DIR` / `SLSKD_INCOMPLETE_DIR` 覆盖，但**这两个目录必须预先存在且可写，程序不会创建** —— 同上
- 镜像平台 `linux/amd64,linux/arm64,linux/arm/v7`；稳定 tag 为 `latest`/版本号/`<版本>-<sha>`，master 分支 tag 为 `canary` —— [ci.yml](https://github.com/slskd/slskd/blob/master/.github/workflows/ci.yml)
- 二进制覆盖 10 个 runtime（win/linux/musl/macos × x64/arm/arm64），zip 分发 —— 同上
- 系统要求：Pi 2 级别 / 512MB RAM / 150MB 磁盘；**不支持 ARMv6（含所有 Pi Zero）** —— [system_requirements.md](https://github.com/slskd/slskd/blob/master/docs/system_requirements.md)、[known_issues.md](https://github.com/slskd/slskd/blob/master/docs/known_issues.md)

### 2.2 `--user 1000:1000` vs `PUID`/`PGID`（本方向最大的坑）

- 官方下判断：Docker 内置方式「objectively superior」——容器以指定用户启动、**从不拥有 root 权限**；PUID/PGID 方式以 root 启动、改 built-in `slskd` 用户 ID、并 chown 挂载的 app 目录 —— [docs/docker.md](https://github.com/slskd/slskd/blob/master/docs/docker.md)
- PUID/PGID 是 **0.25.0 才加入的兼容层**，动机是大量用户按 *arr 习惯误用 PUID/PGID 却发现无效 —— [PR #1695](https://github.com/slskd/slskd/pull/1695)
- 两种方式**互斥**：同时设置会打印 ERROR 并 `exit 1` —— [Dockerfile](https://github.com/slskd/slskd/blob/master/Dockerfile)
- entrypoint 三种分支：① `--user` 模式（非 root 启动，app 目录不可读写则报错退出并提示 `chown -R <uid>:<gid> <挂载目录>`）；② PUID/PGID 模式（root 启动 → groupmod/usermod → **仅 chown app 目录根部，不递归** → gosu 降权）；③ 都没给则完全以 root 运行 —— 同上
- 0.25.0 的 entrypoint 曾在未指定用户时默认 `1000:1000`，导致原本以 root 运行的存量用户升级后崩溃（`Directory /app/data is not writeable`），0.25.1 修复 —— [issue #1706](https://github.com/slskd/slskd/issues/1706)
- PUID/PGID 会改写挂载的 `/app` 属主；TrueNAS 用户报告目录属主被改成 `1001:65533` 后写入失败 —— [issue #1752](https://github.com/slskd/slskd/issues/1752)
- 文件权限由**进程 umask** 决定（默认 022 → 644），容器内用 `SLSKD_UMASK` 覆盖；另有 `transfers.download.destination.permissions.mode` 可创建后 chmod；两者对 Windows 无效 —— [config.md#permissions](https://github.com/slskd/slskd/blob/master/docs/config.md)
- **0.26.0 破坏性变更**：旧 `permissions.file.mode` / `--file-permission-mode` / `SLSKD_FILE_PERMISSION_MODE` 已迁到 `transfers.download.destination.permissions.mode`，**旧配置会让程序拒绝启动** —— [release 0.26.0](https://github.com/slskd/slskd/releases/tag/0.26.0)
- **0.25.0 另一处破坏性变更**：配置里 `global` → `transfers`、`integration` → `integrations`，未改会启动即报错退出 —— [release 0.25.0](https://github.com/slskd/slskd/releases/tag/0.25.0)

### 2.3 50300 端口

- 官方症状描述：搜索命中差、无法浏览或获取部分用户信息；建议同时配好 listen port 与端口转发 —— [config.md#listen-ip-address-and-port](https://github.com/slskd/slskd/blob/master/docs/config.md)
- 典型案例：compose 已映射、路由器已转发，但 `slsknet.org/porttest.php` 仍显示 closed，且**同一端口换 Nicotine+ 就正常**；维护者判定为环境的端口转发/VPN/软件防火墙问题并关闭 —— [issue #1429](https://github.com/slskd/slskd/issues/1429)
- 反常未解案例：slskd 本地 bind 成功、外部不可达，但同一端口用 Python socket listener 测试却对外可达（怀疑 socket 管理方式），至今 open —— [issue #1805](https://github.com/slskd/slskd/issues/1805)
- **无内置开放端口自检功能**，feature request 仍 open —— [issue #440](https://github.com/slskd/slskd/issues/440)
- ⚠️ **#1429 与 #1805 结论相反**，笔记须并列呈现，不可单向取信

### 2.4 NAS 平台现实经验

- Unraid 主流路径：Community Applications 的 hotio 模板（`ghcr.io/hotio/slskd`），变量 PUID/PGID/UMASK(002)/TZ/WEBUI_PORTS，路径 `/config` + `/data` —— [CA 模板](https://ca.unraid.net/apps/slskd-1ca6hh31pcfhq3)（变量清单来自搜索摘要，未抓原始 XML，**待核对**）
- binhex `binhex/arch-slskd`：端口改 `8980/8990`，支持 `SLSKD_LISTEN_PORT`、`SHARED_PATHS`、Gluetun 端口转发变量 —— [Docker Hub](https://hub.docker.com/r/binhex/arch-slskd/)
- 群晖**无官方部署文档**；主要障碍是 **SMB/CIFS 挂载 + 容器 UID/GID 映射**，社区建议之一是改用内置 FTP 投递已完成文件绕开 SMB/NFS 权限问题 —— [discussion #938](https://github.com/slskd/slskd/discussions/938)、[issue #1133](https://github.com/slskd/slskd/issues/1133)
- TrueNAS SCALE 常用 `user: 568:568` 而非 PUID/PGID —— [issue #1752](https://github.com/slskd/slskd/issues/1752)（社区 compose 原文被 Cloudflare 拦截，**待核对**）
- **CoW / 网络文件系统陷阱**：BTRFS/ZFS 及 NFS/SMB/Windows 共享上 SQLite I/O 延迟过高会拖垮程序；缓解办法是把应用数据放别的文件系统，或启用 `volatile` 模式（内存表，重启即丢搜索与传输记录）—— [known_issues.md](https://github.com/slskd/slskd/blob/master/docs/known_issues.md)

### 2.5 升级与迁移

- 数据库迁移在启动时自动执行，迁移前把每个 db 备份到应用数据目录下的 `backups/`，失败自动回滚；手工恢复是把 `<database>.pre-migration-backup.<migration id>.db` 改名回正并放回数据目录根部；卡在重启循环可删库重建；官方提醒磁盘空间要够、不要中断进程 —— [migrations.md](https://github.com/slskd/slskd/blob/master/docs/migrations.md)

### 2.6 缺口

- 群晖 Container Manager 的具体挂载与 ACL 步骤无一手来源
- Windows 二进制「安装为系统服务」无官方说明、未找到可靠社区方案
- `latest` tag 的升级语义（是否随稳定版回退 / 是否应 pin 版本号）官方未明说，**待核对**

---

## 三、方向 ② 账号 / 共享 / 网络规则

### 3.1 账号层（官方 Quick Start 完全没写）

- slskd **没有任何注册 UI/接口**；Soulseek 凭据（username/password）是**唯一必填配置项**，写进 `slskd.yml` 或 `SLSKD_SLSK_USERNAME`/`SLSKD_SLSK_PASSWORD`；Web UI 的 `slskd`/`slskd` 与此**完全无关** —— [config.md](https://github.com/slskd/slskd/blob/master/docs/config.md)
- 官方推荐路径：**先用官方客户端（SoulseekQt）注册账号**，再把凭据填进 slskd —— [slsknet.org 下载页](https://www.slsknet.org/news/node/1)
- 账号**无密码找回机制**；协议文档明确「不接受随机生成的用户名」（自动化脚本违反服务器规则）—— [SLSKPROTOCOL.md](https://github.com/nicotine-plus/nicotine-plus/blob/master/doc/SLSKPROTOCOL.md)
- **用户名 30 天不登录会被服务器回收**（有 privileges 者除外）—— [官方 FAQ](http://slsknet.org/news/faq-page)
- 官方规则：同一 IP 最多 5 个客户端连接；容忍第三方客户端但禁止未实现完整功能的机器人 —— [官方规则页](https://www.slsknet.org/news/node/681)

### 3.2 共享要求（官方 vs 民间，必须区分）

- **官方规则里没有任何「最低共享文件数」要求**；原文只把访问权定性为 "a privilege; not a right" —— [官方规则页](https://www.slsknet.org/news/node/681)
- 共享压力来自**对端用户的自定义规则**。「共享少于 5000 文件就被 ban」这类阈值是**那个用户自己设的**，属社区惯例 —— [社区来源](https://www.lemmy.ml/post/51641793/27356946)
- slskd 自身不强制共享，而是用内置 `leechers` 分组反制：**默认阈值「至少共享 1 个目录 + 1 个文件」**，低于此进入 leecher 组（默认 priority 99、slots 1、限速 100 KiB/s）—— [config.md](https://github.com/slskd/slskd/blob/master/docs/config.md)
- 维护者明确拒绝做「不共享即永久封禁」：理由是「临时/无意的配置问题不该被永久惩罚」，改用分组限速 + 配额 —— [issue #330](https://github.com/slskd/slskd/issues/330)
- 不共享对自身下载的反噬：启动后若共享尚未扫描完成就连接服务器，对端重新请求文件会收到 "file not shared" 被拒 —— [issue #532](https://github.com/slskd/slskd/issues/532)

### 3.3 监听端口 50300

- 默认 `soulseek.listen_port: 50300`，监听地址 `0.0.0.0`；**必须容器与路由器两层都放通** —— [config.md](https://github.com/slskd/slskd/blob/master/docs/config.md)、[docker.md](https://github.com/slskd/slskd/blob/master/docs/docker.md)
- 网络侧原因：浏览用户需能建立入站 TCP；官方客户端靠 UPnP 自动配置，但**部分路由器（尤其 Apple）不支持 UPnP**，ISP 也可能禁止入站 TCP —— [官方 FAQ](http://slsknet.org/news/faq-page)
- **slskd 无内置 UPnP/NAT-PMP**：维护者以 UPnP 有安全顾虑为由搁置 —— [issue #908](https://github.com/slskd/slskd/issues/908)
- **slskd 未实现 obfuscated port**（`Options.cs` 与 `config.md` 均无该项）—— [Options.cs](https://github.com/slskd/slskd/blob/master/src/slskd/Core/Options.cs)（属否定证据，表述应为「当前版本不支持」）
- 端口封闭典型报错：`Failed to establish a direct or indirect message connection to [user] ([ip]:50300)` —— [issue #1429](https://github.com/slskd/slskd/issues/1429)
- 官方检测工具：`https://www.slsknet.org/porttest.php?port=50300`

### 3.4 Relay

- 定义：多个 slskd 实例作为一个客户端协同；一个 **Controller** 连 Soulseek 网络，多个 **Agent** 只把文件中继给 Controller —— [relay.md](https://github.com/slskd/slskd/blob/master/docs/relay.md)
- 四大场景之一就是「**想要完整功能但无法正确配置端口转发**」；另含多地点共享、不想多开账号、需要常在线客户端保住远程队列位置
- 方向性：**Agent 主动连 Controller，家庭网络无需转发任何端口**；Controller 需一个 `readwrite` API key + 每 Agent 一个 16–255 字符 shared secret，可用 `cidr` 限制来源，强建议 HTTPS —— 同上
- ⚠️ **Relay 不是「单机免端口」方案**：Controller 本身仍要连 Soulseek 网络、仍有监听端口要求。价值在于把「必须暴露端口的机器」收敛到一台。不可过度承诺 —— 同上

### 3.5 配置位置速查

| 内容 | 节 |
| --- | --- |
| 账号 | `soulseek.username` / `soulseek.password` |
| 监听端口 | `soulseek.listen_port` |
| 服务器 | `soulseek.address`（默认 `vps.slsknet.org:2271`） |
| 共享 | `shares.directories` / `shares.filters` / `shares.cache` |
| 分组与黑名单 | `groups` / `groups.user_defined` / `blacklist` |
| VPN 动态端口 | `integrations`（System-Defined） |

### 3.6 缺口

- **首次登录是否自动建号**：社区普遍称「用户名未占用即自动创建」，但无官方文档背书 → 成稿应写「实践中首次用未占用用户名登录即建立账号，但官方未明文承诺」
- **不共享是否被服务器主动踢下线**：官方规则只说访问权可被撤销、管理员可随时 kill，**未发现「因不共享被服务器 ban」的官方条款**；实际后果主要来自对端客户端 → 必须区分清楚
- CGNAT / 无公网 IPv4 场景未逐条核实
- obfuscated port 与 50300 的关系多为社区经验，属 folklore 概率较高

---

## 四、方向 ③ 日常使用与配置安全

### 4.1 Web UI 操作面（官方几乎空白）

- `docs/` 仅 10 个文件，**没有独立的 Web UI 操作手册**；UI 用法只能从根 README 的 Features 段落取 —— [docs/README.md](https://github.com/slskd/slskd/blob/master/docs/README.md)
- 官方描述：搜索（便于连续输入多个搜索）、结果（排序筛选、dismiss、几次点击下载）、下载（按用户和文件夹分组、点进度条查排队位次、cancel/retry/clear completed）、browse 用户共享 + 聊天室 + 私聊 —— [README](https://github.com/slskd/slskd)
- ⚠️ 搜索结果排序/筛选的**具体字段清单、快捷键、批量交互**官方只字未提 → 要么断言「官方未文档化」，要么读前端源码（**待核对**）

### 4.2 顶层配置键（纠正了一个常见误解）

- 顶层 YAML 键为：`debug`、`headless`、`remote_configuration`、`remote_file_management`、`instance_name`、`flags`、`relay`、`directories`、`shares`、`transfers`、`groups`、`blacklist`、`filters`、`rooms`、`web`、`retention`、`throttling`、`logger`、`metrics`、`feature`、`soulseek`、`integrations` —— [slskd.example.yml](https://github.com/slskd/slskd/blob/master/config/slskd.example.yml)
- 配置源优先级：`默认值 < 环境变量 < YAML 文件 < 命令行参数 < 运行时覆盖`；环境变量统一 `SLSKD_` 前缀，列表用分号 `;` 分隔 —— [config.md](https://github.com/slskd/slskd/blob/master/docs/config.md)
- **合并陷阱**：多来源合并列表时 .NET 不是纯追加而是「覆盖 + 追加」。env `one;two;three` + YAML `foo`/`bar` → 结果 `foo, bar, three` —— 同上
- YAML 运行时被 watch，热加载并推给 Web UI；需重连/重启才生效的项会被打标记 —— 同上

### 4.3 关键默认值（实际会改的部分）

| 键 | 默认值 |
| --- | --- |
| `shares.directories` | `~`（空） |
| `shares.filters` | `\.ini$`、`Thumbs.db$`、`\.DS_Store$` |
| `shares.cache.storage_mode` | `memory`（大库 OOM 时改 `disk`） |
| `transfers.upload` | `slots: 20`、`speed_limit: 1000` KiB/s |
| `transfers.download` | `slots: 500`、`speed_limit: 1000` KiB/s |
| `transfers.download.retry` | `partial: resume`、`attempts: 3`、`delay: 5000`、`max_delay: 60000` ms |
| `transfers.download.destination.subdirectory` | `${SOURCE_DIRECTORY}` |
| `transfers.download.destination.exists` | `rename` |
| `groups` | 内置 `default` / `leechers` / `privileged` / `blacklisted` |
| `soulseek.listen_port` | `50300` |
| `soulseek.distributed_network.child_limit` | `25` |
| `web.url_base` | `/` |
| `web.authentication.jwt.ttl` | `604800000` ms（7 天） |
| `remote_configuration` | `false` |
| `remote_file_management` | `false` |
| `feature.swagger` | `false` |
| `headless` | `false` |

- `groups.blacklisted` 支持 `members`（用户名）、`cidrs`（IP 段）、`patterns`（用户名正则）；被拉黑者不返回搜索结果、不可 browse、不可入队，私聊与聊天室消息也被忽略 —— [config.md](https://github.com/slskd/slskd/blob/master/docs/config.md)
- `blacklist.enabled` / `blacklist.file`：托管黑名单（P2P / DAT / CIDR 三种格式）；**格式识别失败或运行中变坏会导致应用退出**，内容全量载入内存 —— 同上

### 4.4 认证与安全

- 默认 Web UI 账号密码均 `slskd`/`slskd`，认证默认开启；官方强烈建议首次配置就同时改掉 —— [config.md](https://github.com/slskd/slskd/blob/master/docs/config.md)
- `remote_configuration` **默认 `false`**。官方警告：面向互联网的部署要慎重开启；一旦攻击者拿到应用访问权并取走 YAML，**文件里所有密钥都会泄露** —— 同上
- `remote_file_management` 默认 `false`；开启后 API 可**删除** Incomplete/Downloads 内文件 —— 同上
- JWT：默认每次启动随机生成密钥，**重启会让已签发 JWT 全部失效**；可自设 ≥16 字符密钥 —— 同上
- API Key：需名字 + 16~255 字符值，经 `X-API-Key` 头传入；可选 CIDR 白名单（默认不限）；`--generate-secret` 生成；普通 key 默认 `ReadOnly`，主 key 默认 `Administrator` —— 同上
- **CIDR 过滤在反代/ingress/LB 后面可能失效**（看到的是入口设备 IP）；slskd **刻意不支持** `X-Forwarded-For`（可伪造），这类场景必须把过滤做在网络入口 —— 同上
- 明文 HTTP 下用 API Key **不被推荐**（走 header，SignalR 场景还走 query）—— 同上
- ⚠️ **已知真实缺陷**：API 认证的 CIDR 过滤自 0.24.3.0 起失效，加 `::ffff:` 前缀可**完全绕过**（等于没配），连 `0.0.0.0/0` 都不生效 —— [issue #1605](https://github.com/slskd/slskd/issues/1605)
- 脚本集成存在**远程代码执行风险**：`$SLSKD_SCRIPT_DATA` 来自 Soulseek 网络，可能含恶意文件名/用户名；官方给了 ✅/❌ 最佳实践清单（禁止 shell 命令替换、禁止裸传参、先解析 JSON 再校验字段）—— [config.md](https://github.com/slskd/slskd/blob/master/docs/config.md)
- 官方安全策略文件仅一行「漏洞邮件报告到 security@slskd.org」，**无威胁模型文档** —— [SECURITY.md](https://github.com/slskd/slskd/blob/master/SECURITY.md)

### 4.5 反向代理

- 官方给 NGINX / SWAG / Apache / IIS 四种，**没有 Caddy 官方示例** —— [reverse_proxy.md](https://github.com/slskd/slskd/blob/master/docs/reverse_proxy.md)
- 因同时用 websocket(SignalR)，NGINX 必须设 `Upgrade` 与 `Connection "Upgrade"` 头，并建议 `proxy_request_buffering off`、`client_max_body_size 0` —— 同上
- 子路径部署：设 `URL_BASE`（`SLSKD_URL_BASE` / `--url-base`）为 `/slskd` 即可 —— 同上
- 社区反馈 Caddy/NGINX 下**认证可能失效、websocket 会断**，需补 `X-Real-IP` 等头与长超时（`proxy_read_timeout 86400s`）—— [issue #1502](https://github.com/slskd/slskd/issues/1502)
- Caddy 常见故障：全局 www 重定向或 `redir` 抢在反代前返回 302；子路径 matcher 应写 `/slskd*` —— [Caddy 社区](https://caddy.community/t/reverse-proxy-to-websocket-always-fails/25460/4)

### 4.6 VPN 绑定

- 官方推荐选**支持端口转发**的 VPN；文档里唯一 referral 是 Proton VPN，gluetun 之外无内置支持 —— [vpn.md](https://github.com/slskd/slskd/blob/master/docs/vpn.md)
- ⚠️ **最重要的认知纠正**：官方用 CAUTION 明确说明「配置 VPN 集成**不会改变**到 Soulseek 服务器或其他 peer 的流量路由」，用户必须自己保证走 VPN 网络接口。该集成只提供可见性、自动应用动态转发端口，以及在没有 kill switch 时的一点点保护 —— [config.md](https://github.com/slskd/slskd/blob/master/docs/config.md)
- 关键配置：`SLSKD_VPN=true`、`SLSKD_VPN_PORT_FORWARDING=true`、`SLSKD_VPN_GLUETUN_URL`、`SLSKD_VPN_GLUETUN_API_KEY`；gluetun 侧需开 control server —— [vpn.md](https://github.com/slskd/slskd/blob/master/docs/vpn.md)
- 行为：首启先轮询 VPN 并延迟连接 Soulseek；VPN 报未连接时 slskd **主动断开** Soulseek 连接，恢复后自动重连 —— [config.md](https://github.com/slskd/slskd/blob/master/docs/config.md)
- 社区最高频痛点之一：VPN passthrough 下的端口转发（尤其 Mullvad，38 条评论）—— [issue 排行](https://github.com/slskd/slskd/issues?q=is%3Aissue+sort%3Acomments-desc)

### 4.7 高频 issue 排行（截至抓取）

VPN 端口转发/passthrough（38）、下载卡死无法取消（31）、FreeBSD 不支持（29）、`wait timed out after 5000 milliseconds`（24）、大库用户无法 browse（22）、大共享扫描 OOM（21）、搜索卡死（20）、**下载文件属主为 root（19）**、启动 OOM（18）、共享扫描失败（17）、内存持续飙升（16）、inotify watch 泄漏（16）—— 同上

- 与配置安全直接相关：`Any update to slskd.yml after 0.25.0 results in ERR`（保存 Options 抛 NullReferenceException，配置仍生效但每次保存都报错）、`'Options (re)configuration rejected'`、`Edits to config 'shares - directories - cache' not taking effect`、`Significantly few search results` —— 同上
- `SQLite is a major performance bottleneck ... unfixable bugs on copy-on-write filesystems` —— [issue #1468](https://github.com/slskd/slskd/issues/1468)
- 官方 known issues 共 5 条：ARMv6 不支持 / Pi Zero 全部不行 / CoW 文件系统 / 网络文件系统 / AWS t3a.nano 约每 12h OOM —— [known_issues.md](https://github.com/slskd/slskd/blob/master/docs/known_issues.md)

### 4.8 API / 集成生态

- Swagger(OpenAPI) 与 `/swagger` UI **默认关闭**，需 `--swagger` / `SLSKD_SWAGGER=true`；YAML 键 `feature.swagger` —— [config.md](https://github.com/slskd/slskd/blob/master/docs/config.md)
- 内置 Prometheus 指标 `/metrics`（默认关闭；开启后默认账号仍是 `slskd`/`slskd`，公网建议关闭）—— 同上
- 集成：webhook（POST + JSON，可自定义 headers/超时/重试）、脚本（`SLSKD_SCRIPT_DATA`）、FTP 上传、Pushbullet、Grafana Loki —— 同上
- MCP 生态**均为第三方、非官方**：`abl030/slskd-mcp`（1 star，README 自称 AI 生成）、`ldgnu/mcp-slskd`（0 star 无 license）、`voidtype/slsk_mcp` 与 `mihai9-lab/slsk-mcp`（直连 Soulseek，不经 slskd）—— 可信度需打折，**不宜作为推荐方案**
- 另有 `crmne/slskd-python-client`、n8n 节点 `n8n-nodes-slskd` —— 同上

### 4.9 缺口

- Web UI 无官方操作文档（见 4.1）
- **config.md 内部键名不一致，写作时不能照抄**：`logger` 在 config.md 写 `disk`、example.yml 写 `no_disk`、环境变量叫 `SLSKD_NO_DISK_LOGGER`；`flags.case_sensitive_reg_ex` vs `SLSKD_CASE_SENSITIVE_REGEX`；`integration` vs `integrations` → **一律以 `example.yml` 为准并标注待核对**
- issue #1707（0.25.0 配置保存 ERR）当前是否已修复未核实，需查 0.26.0 changelog
- 无中文一手资料：已有的中文来源（zeabur 模板、Basar 论坛）均为二手搬运且部分过时 → **不建议作为正式引用**
- `SLSKD_REMOTE_CONFIGURATION` 的完整攻击链是外推（官方只说「所有密钥都会泄露」）→ 笔记保留保守表述

---

## 五、跨方向的重大发现（直接影响大纲结构）

### 5.1 官方 README 与 config.md 存在分歧 —— 必须显式处理

README Quick Start 直接给出 `SLSKD_REMOTE_CONFIGURATION=true` 作为启动参数；而 `config.md` 中该项**默认 `false`**，且官方警告「面向互联网的部署要慎重考虑开启，一旦被取走 YAML，文件里所有密钥都会泄露」。

→ 笔记不能照抄 README 就完事，必须说明：**这是「方便」与「安全」的取舍开关**，本地/内网开、公网关。

### 5.2 端口语义极易混淆

`5030` / `5031` 是 **Web UI**（HTTP/HTTPS 自签），`50300` 是 **Soulseek 入站监听**，`2271` 是 **Soulseek 服务器**。官方文档分处两节，写笔记的人常弄混 → 需要一张显式对照表。

### 5.3 破坏性变更时间线（实用价值高）

- `0.25.0`：引入 PUID/PGID；配置 `global` → `transfers`、`integration` → `integrations`（不改则启动报错）
- `0.25.1`：修复未指定用户时默认 `1000:1000` 导致的权限崩溃
- `0.26.0`：`permissions.file.mode` → `transfers.download.destination.permissions.mode`（旧配置拒绝启动）

→ 可归纳为一张「升级前检查清单」，这是官方没有的**差异化产出**。

### 5.4 中文一手资料为零

探测确认：CSDN/知乎/NodeSeek/少数派等均未命中一手部署教程，现有中文内容为二手搬运且部分过时。→ 本笔记的**差异化切入点**：把英文一手资料（尤其权限与端口两块）整理成中文可执行版本。

### 5.5 Web UI 操作面是结构性缺口

官方只文档化了「配置」，没文档化「操作」。→ 大纲对 UI 操作部分应降级为「基于官方 README 描述 + 截图说明」，并显式声明「官方未文档化」，而非编造细节。

---

## 六、待核对清单（进入 Phase 2 / 写作前必须复核）

| # | 事项 | 处理方式 |
| --- | --- | --- |
| 1 | config.md 键名三处不一致（`logger` / `case_sensitive_reg_ex` / `integration`） | 以 `config.md` 为准，必要时查 `Options.cs` 源码 |
| 2 | 首次登录是否自动建号 | 表述为「实践中……但官方未明文承诺」 |
| 3 | 不共享是否被服务器主动踢 | 区分「服务器规则」与「对端客户端行为」 |
| 4 | issue #1707 是否已在 0.26.0 修复 | 查 0.26.0 changelog |
| 5 | `latest` tag 升级语义 / 是否应 pin 版本号 | 查官方文档或 issue |
| 6 | Unraid hotio 模板变量、TrueNAS `568:568` compose | 抓原始 XML / 换源验证 |
| 7 | obfuscated port 与 50300 的关系 | 标注为社区经验，非官方 |
| 8 | Web UI 筛选字段/快捷键 | 断言「官方未文档化」，或读前端源码 |
| 9 | `#1429` 与 `#1805` 结论矛盾 | 笔记中并列呈现 |

---

## 七、方向菜单（供用户选择，Phase 2 依据）

| 选项 | 范围 | 资料支撑 | 推荐 |
| --- | --- | --- | --- |
| **1. 部署与运行**（含权限、端口、NAS、升级迁移） | 方向 ① 全量 | 官方一手充足，坑点具体 | ✅ 强烈推荐 |
| **2. 账号与共享机制**（注册、共享规则、leech 限速、50300、Relay） | 方向 ② 全量 | 官方规则 + config.md，**差异化最大** | ✅ 强烈推荐 |
| **3. 日常使用与配置详解**（Web UI 操作 + config.md 常用配置） | 方向 ③ 的 4.2/4.3 | 配置面强，**UI 操作面官方空白** | ✅ 推荐（UI 部分降级处理） |
| **4. 安全与进阶**（认证、反代、VPN、API/MCP、黑名单） | 方向 ③ 的 4.4–4.8 | 充足，但偏进阶 | ⭕ 建议压缩为 1 章或速览小节 |
| **5. 排错专项**（端口不通、权限报错、OOM、扫描失败） | 跨方向 | issue 素材极丰富 | ⭕ 建议并入各章「常见坑」 |
