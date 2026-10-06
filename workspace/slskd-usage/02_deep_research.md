# 02 深度研究：如何使用 slskd

- **workflow**: learning-note-flow / run_id `slskd-usage`
- **阶段**: P2 深度收集
- **日期**: 2026-09-14
- **版本锚点**: 最新稳定版 **0.26.0**（2026-07-19，据 `releases.atom` 首条与 releases 列表首位）
- **上游**: `workspace/slskd-usage/00_intent.md`、`workspace/slskd-usage/01_explore_result.md`
- **本地信源缓存**: `workspace/slskd-usage/sources/`

---

## 一、研究范围

用户已确认的三主线 + 一压缩章，排错并入各章：

1. **部署与运行** —— Docker / compose / 二进制；`--user` vs `PUID`/`PGID` 与权限；目录与 umask；50300；NAS 平台；known_issues 的 CoW 与网络文件系统陷阱；升级与数据库迁移
2. **账号与共享机制** —— 账号注册（官方无注册入口）；30 天回收；共享要求（官方 vs 民间）；内置 leechers 组；50300 入站 TCP；Relay 的 Controller/Agent 架构
3. **日常使用与配置详解** —— Web UI 功能面（**无官方操作文档，需显式声明**）；配置源优先级与合并陷阱；`transfers`/`groups`/`blacklist` 常用项
4. **安全与进阶速览**（压缩为末章）—— 默认凭据与 `remote_configuration`；JWT / API Key 与 CIDR 缺陷；反向代理；VPN 绑定；Swagger / metrics / MCP 生态

**收集方法说明**：`raw.githubusercontent.com` 与 `WebFetch(github.com / raw.githubusercontent.com / deepwiki.com)` 在本机不可用；`api.github.com` 可用但限流 60/h。实际主通道为
① `api.github.com/repos/.../contents`（早期）、② `cdn.jsdelivr.net/gh/slskd/slskd@master/...`（无速率限制，主力）、③ `curl` 直取 `slsknet.org`（WebFetch 对全域被拦截）、④ GitHub issue 页面内嵌 JSON payload（可绕过 API 限流取到完整评论时间线）。

---

## 二、信源表

层级：**T1** 官方一手（仓库文件 / release notes / 官方站点规则）｜**T2** 维护者本人发言或已合并 PR/issue 结论｜**T3** 社区（须标注，不单独承重）

| ID | 来源 | 位置 / 锚点 | 层级 |
| --- | --- | --- | --- |
| S1 | README.md | `sources/README.md` | T1 |
| S2 | docs/docker.md | `sources/docs_docker.md` | T1 |
| S3 | docs/config.md（85 KB） | `sources/docs_config.md` | T1 |
| S4 | docs/known_issues.md | `sources/docs_known_issues.md` | T1 |
| S5 | docs/vpn.md | `sources/docs_vpn.md` | T1 |
| S6 | docs/reverse_proxy.md | `sources/docs_reverse_proxy.md` | T1 |
| S7 | docs/relay.md | `sources/docs_relay.md` | T1 |
| S8 | docs/migrations.md | `sources/docs_migrations.md` | T1 |
| S9 | docs/system_requirements.md | `sources/docs_system_requirements.md` | T1 |
| S10 | docs/README.md | `sources/docs_README.md` | T1 |
| S11 | config/slskd.example.yml（335 行） | `sources/config_slskd.example.yml` | T1 |
| S12 | Dockerfile | `sources/Dockerfile` | T1 |
| S13 | SECURITY.md | `sources/SECURITY.md` | T1 |
| S14 | **src/slskd/Core/Options.cs** | `sources/Options.cs`（124 860 B，master） | T1 |
| S15 | 前端源码 `src/web/src/**` | jsDelivr `@master/src/web/...` | T1 |
| S16 | `.github/workflows/ci.yml` | jsDelivr `@master` | T1 |
| S17 | release 0.25.0 | `releases/tag/0.25.0` | T1 |
| S18 | release 0.26.0 | `releases/tag/0.26.0` | T1 |
| S19 | releases.atom | `releases.atom` | T1 |
| S20 | Soulseek 规则页 node/681 | slsknet.org | T1 |
| S21 | Soulseek FAQ node/748（用户名回收） | slsknet.org | T1 |
| S22 | node/523（空共享警告机制） | slsknet.org | T1 |
| S23 | node/1159（$5 捐款永不过期） | slsknet.org | T1 |
| S24 | Soulseek FAQ 页 faq-page | slsknet.org | T1 |
| S25 | node/263、node/551（协议混淆） | slsknet.org 发布说明 | T1 |
| S26 | SLSKPROTOCOL.md | nicotine-plus 仓库（**社区逆向**） | T3 |
| S27 | PR #1711 / issue #1707 | github.com | T2 |
| S28 | issue #1429 | github.com | T2 |
| S29 | issue #1805 | github.com | T2 |
| S30 | issue #1605 + PR #1606 + PR #1714 | github.com | T2 |
| S31 | hotio Unraid 模板 XML | `hotio/unraid-templates@master/hotio/slskd.xml` | T3（模板作者仓库） |
| S32 | hotio.dev/containers/slskd | hotio.dev | T3 |
| S33 | TrueNAS 官方文档 PR #4253 + apps 目录元数据 | truenas/documentation、apps.truenas.com | T1 |
| S34 | discussion #1289 | github.com | T2（维护者） |

---

## 三、P1 → P2 结论修正（**写作时必须按 P2 口径，不得沿用 P1**）

| # | P1 的说法 | P2 复核结论 | 依据 |
| --- | --- | --- | --- |
| C1 | 「`config.md` 键名三处不一致」 | **成立，且实际是四处**。另发现官方文档内部还有 `groups` 位置错误（见 C6）。且三处中有**一处根本不是冲突**（见 C3） | S14 / S11 / S3 |
| C2 | 「`logger` 的 `disk` / `no_disk` 冲突」 | **`no_disk` 为真，`docs/config.md` 的 YAML 块（`logger.disk`）是错的**，且语义反向 | S14:1461-1465 `NoDisk`；S11:198 |
| C3 | 「`flags.case_sensitive_reg_ex` vs `SLSKD_CASE_SENSITIVE_REGEX` 是冲突」 | **不是冲突**。这是同一选项的 **CLI / env / YAML 三套命名空间**：CLI `--case-sensitive-regex`、env `SLSKD_CASE_SENSITIVE_REGEX`、YAML `flags.case_sensitive_reg_ex`。唯一错误是 `docs/config.md` 散文在指代 YAML 选项时误用了 env 拼法 | S14:487-493 |
| C4 | 「`integration` vs `integrations`」 | **`integrations`（复数）为真**。单数是 `[Obsolete]` 哨兵属性 | S14:331-332 / 337-338 |
| C5 | 「`#1429` 与 `#1805` 关于 50300 的结论**相反**，必须并列呈现」 | **P1 判定有误，不存在相反结论**。两者是**不同场景**：#1429 是「自己浏览自己失败」（先决条件是入站可用），维护者定性为端口转发/防火墙并关闭；#1805 是「绑定成功但外部扫描显示关闭」，在**排除**了用户侧嫌疑（同端口 Python listener 可通）后仍 **OPEN**，维护者仍在做最小复现实验。→ 写作口径应为「已定性的环境问题」与「未定性的疑难」两种状态，而非两个互相矛盾的技术结论 | S28 / S29 |
| C6 | 未发现 | **主动新增**：`groups` 的位置也有官方文档错误。`docs/config.md` 的 User Blacklist 节把 `groups:` 写成**顶层键**，实为 `transfers.groups`；顶层 `groups` 是 `[Obsolete]` 哨兵 | S3:526 vs 466；S14:257-258；S11:83 |
| C7 | P0/P1 意图文件写「slskd 无注册 UI，**需 SoulseekQt** 注册」 | **前半句成立，后半句降级**。已证实：官方站点**不提供网页注册**（`/news/user/register` → HTTP 403 "Access denied"；全站导航无 Register 项；站点登录表单要的是「Soulseek username」）。但**官方从未说明账号创建发生在哪一步**，「必须先用 SoulseekQt 注册」是社区推断，**不是官方口径**，不得写成官方要求 | S20 / S24；S26（社区旁证） |
| C8 | 未发现 | **风险新增**：`soulseekqt.net` 域名**已被劫持**，现为越南博彩垃圾站。官方 FAQ 中的部分外链指向该域名。**笔记中禁止引用 `soulseekqt.net`**，一律改用 `slsknet.org` 对应 node | S24 采集记录 |

---

## 四、P1 待核对 9 条 —— 闭环结果

| # | 事项 | 结果 | 证据 |
| --- | --- | --- | --- |
| 1 | `config.md` 键名三处不一致 | **已裁决**：以 `Options.cs` + `example.yml` 为准 → `logger.no_disk`、`integrations`（复数）、`flags.case_sensitive_reg_ex`（env 另名不算冲突）；另主动发现第 4 处 `transfers.groups` | S14 / S11 |
| 2 | 首次登录是否自动建号 | **官方未证实**。官方无注册入口（403 反证）；官方文档从未说明账号创建步骤。社区旁证：协议文档把 `INVALIDPASS` 定义为「Password for existing user is incorrect」，暗示新用户名被直接接受。→ 写作口径：「官方未提供注册入口，也未说明账号创建发生在哪一步；实践中首次以未占用的用户名登录即被接受（社区旁证，非官方承诺）」 | S20 / S24 / S26 |
| 3 | 不共享是否被服务器主动踢 | **官方无此条文，且有反证**。官方规则页全文无最低共享数量/容量条款；node/523 中官方明言**反对**在客户端内置 autoban（"automatically banning users ... one I've always resisted strongly"），实现的是「空共享警告机制」。→ 必须区分三层：① 服务器规则（无强制共享门槛）② 对端客户端行为（用户自设 autoban 阈值）③ slskd 内置 `leechers` 组的限速 | S20 / S22 / S24 |
| 4 | `#1707` 是否已在 0.26.0 修复 | **已在 0.25.1 修复，不是 0.26.0**。状态 CLOSED / COMPLETED，关闭于 2026-04-20。PR #1711 描述含 "Closes #1707"，其 merge commit `7961741` 与 0.25.1 release 页标注的 commit 一致 | S27 |
| 5 | `latest` tag 升级语义 / 是否应 pin | **只能从 CI 源码推断**（官方无明文）。`Build and push Release` 条件为 `startsWith(github.ref, 'refs/tags/')`，才推 `:latest`；`Build and push Canary` 条件相反，只推 `:canary`。workflow 触发条件 `tags: "[0-9]+.[0-9]+.[0-9]+"`（无预发布）→ **`latest` 跟随稳定版**。两点注意：① release 发布时 `:canary` 被**同时**指向该 release 镜像，故发布后短期内 `latest == canary`，用 canary 判断「是否领先稳定版」会失效；② 精确 pin 用 `CONTAINER_VERSION`，格式 `<tag>.0-<short sha>`（release）/ `<tag>.65534-<short sha>`（canary）。**「pin 版本号」属社区惯例，官方文档无此建议**，全部示例统一用 `:latest` | S16 / S2 |
| 6 | Unraid hotio 模板变量、TrueNAS `568:568` | **Unraid 已取证**：CA app id `slskd-1ca6hh31pcfhq3`；模板 XML 实测 `Repository=ghcr.io/hotio/slskd:latest`，端口 Target 5030/5031，路径 `/config`(rw) + `/data`(rw)，**`PUID` 默认 99、`PGID` 默认 100、`UMASK` 默认 002**，`WebUI=http://[IP]:[PORT:5030]`，`ExtraParams=--hostname=slskd.internal --cap-add=NET_ADMIN`。**TrueNAS 已取证**：官方文档原文「Defaults to **568** (apps)」，apps 目录元数据 `"uid": 568, "gid": 568, "user_name": "Host user is [apps]"`。**但 `user: 568:568` 用于 slskd 的原始出处未取得**——唯一候选 `wiki.serversatho.me/soulseek` 全程 403（含浏览器 UA），Wayback 不可达。→ 只能表述为**组合推断**（官方 `user:` 写法 + TrueNAS apps=568），并标注「非被引用的 slskd 原始资料」。群晖**无任何 slskd 一手资料**，只有通用 Docker 教程外推 | S31 / S32 / S33 |
| 7 | obfuscated port 与 50300 的关系 | **有官方依据，但仅存在于发布说明**。node/263：「P2P communication between two clients of this version or higher will be obfuscated」；node/551：「usually it's the listening port number+1」；非强制，对端不支持时自动回退明文 P2P。**官方 FAQ 页完全没有该条目**（逐条核对无 `obfuscat` 匹配）→ 若写入笔记须注明「仅见于 release notes / 发布说明，FAQ 未收录」 | S25 / S24 |
| 8 | Web UI 筛选字段 / 快捷键 | **已源码取证**，见 §5.3.1。官方确实**无任何 UI 操作文档**：`/docs/` 仅含 build / config / docker / known_issues / README / relay / reverse_proxy / system_requirements | S15 / S10 |
| 9 | `#1429` 与 `#1805` 结论矛盾 | **修正为不矛盾**，见 C5 | S28 / S29 |

---

## 五、核心知识域 claim / source 映射

### 5.1 部署与运行

**5.1.1 端口语义（最高频混淆点，必须三线区分）**

| 端口 | 用途 | 默认值 | 证据 |
| --- | --- | --- | --- |
| Web UI HTTP | 浏览器 / API | `5030` | S14:2019 `public int Port = 5030`（`WebOptions`） |
| Web UI HTTPS | 自签证书 | `5031` | S14:2319 `public int Port = 5031` |
| Soulseek 入站 | **接受对端 TCP 连接** | `50300` | S14:1770 `ListenPort = 50300`；env `SLSK_LISTEN_PORT`；容器内 `SLSKD_SLSK_LISTEN_PORT`（S12:75） |
| Soulseek 服务器 | 出站到服务器 | `2271`（`vps.slsknet.org`） | S14:1706/1716；env `SLSK_ADDRESS` / `SLSK_PORT` |

> 关键点：`SLSKD_SLSK_LISTEN_PORT` 这一「双 SLSK」命名来自 Dockerfile（S12），因为 `soulseek.*` 在 env 层缩写为 `SLSK_*`。**社区镜像常用的 `SLSKD_LISTEN_PORT` 不是官方命名**。

**5.1.2 三种容器运行身份（Dockerfile entrypoint 三分支，S12:97-192）**

| 模式 | 触发条件 | 行为 |
| --- | --- | --- |
| ① 现代 Docker | `--user` / compose `user:` | 容器以非 root 启动，**跳过**全部 usermod/chown，直接 `exec "$@"`。若同时给了 `PUID`/`PGID` → 打印 ERROR 并 **exit 1**（S12:107-113） |
| ② 传统 linuxserver 风格 | 未给 `--user`，给了 `PUID` 或 `PGID` | 以 root 启动 → `groupmod`/`usermod` 改内置 `slskd` 用户的 uid/gid → `mkdir -p /app` → **仅当** `/app` 属主不符时 `chown "${PUID}:${PGID}" "${SLSKD_APP_DIR}"`（**非递归，仅根目录**，S12:185-187）→ `exec gosu` 降权 |
| ③ 都不给 | 既无 `--user` 也无 `PUID`/`PGID` | **以 root 运行**（S12:137-148，注释明写 "same behavior as < 0.25.0"，即向后兼容） |

另：`SLSKD_APP_DIR` 不是 bind mount / volume 时，entrypoint 会打印 `WARNING: ... Configuration and data will be lost if the container is removed.`（S12:127-129、142-144）

**5.1.3 官方立场：优先 `user:`，不建议 PUID/PGID**

S2 原文：「Docker's built-in functionality is **objectively superior**; the container starts and runs as the user you specify, it never has root privileges.」官方示例为 `user: 1000:1000`。
S34（维护者本人）：「To change the user, run docker with the `--user` argument or set the file permission mode/umask」。

> P1 曾提到 quick-start 配置"doesn't include any shared directories, and any files that are downloaded will be owned by root"——该警告同样出自 S2，可引用。

**5.1.4 安装方式与镜像**

- 官方镜像 `slskd/slskd`，官方示例**统一使用 `:latest`**（S2）；另有 `ghcr.io/slskd/slskd`（S16）
- 容器内应用目录 `/app`（S12:76 `SLSKD_APP_DIR=/app`）；文档示例把宿主目录挂到 `/app`（S5、S2）
- 也提供二进制直接运行（S1）
- `HEALTHCHECK` 为 `wget -q -O - http://localhost:${SLSKD_HTTP_PORT}/health`，`start-period=60m`、`retries=3`（S12:63）——**60 分钟启动宽限期**，说明首次共享扫描可能极慢

**5.1.5 系统要求与已知不兼容（S9、S4）**

- 最低：Raspberry Pi 2 或同等；x86/x86_64/amd64/ARMv7+；≥512 MB RAM；≥150 MB 磁盘
- **ARMv6 及更早不支持**（.NET runtime 限制）；**所有 Raspberry Pi Zero 都是 ARMv6**
- **CoW 文件系统（BTRFS / ZFS）不适用**：slskd 用 SQLite 存 transfers/searches，这些读写 I/O 延迟过高。缓解：应用数据放独立磁盘/分区（不同文件系统）或 RAM disk；或启用 **volatile 模式**（`SLSKD_VOLATILE` / `flags.volatile: true`）改用内存 SQLite 表——**重启后搜索与传输记录全部丢失**
- **网络文件系统（NFS / SMB / Windows 文件共享）同因不适用**
- **AWS EC2 t3a.nano + Ubuntu**：约每 12 小时 OOM 崩溃；换 Amazon Linux 可运行但内存占用很高

**5.1.6 升级与数据库迁移（S8）**

- 迁移在启动时自动执行；失败会尝试用备份回滚
- 备份位于应用数据目录下 `backups/`，命名 `<database>.pre-migration-backup.<migration id>.db`
- 手工恢复：找到**第一次**失败尝试的 migration id（在日志里；找不到就取最旧）→ 把备份改名去掉 `.pre-migration-backup.<id>` 段、移出 `backups/` 放回数据目录根 → 重启
- 陷入重启循环时需重命名或删除现有数据库让其重建（旧数据只能手工恢复，官方要求开 issue 附日志）
- 预防：确保磁盘空间充足、**迁移中不要中断应用**、监控日志

**5.1.7 破坏性变更时间线（可直接做成升级检查清单）**

| 版本 | 变更 | 后果 | 证据 |
| --- | --- | --- | --- |
| 0.24.4（2026-02-16） | 非破坏：PR #1606 去掉 IPv4-mapped IPv6 的 `::ffff` 前缀 | 修 API key CIDR 解析 | S19 |
| **0.25.0**（2026-04-19） | `global` → `transfers`；limits 移入各 group 的 `upload` 下；`integration` → `integrations`；新增 PUID/PGID 支持（与 `--user` 互斥） | 旧键 → **启动失败早退** | S17 |
| **0.26.0**（2026-07-19） | 顶层 `permissions.file.mode` → `transfers.download.destination.permissions.mode`；同版内新选项 `retry.incomplete` 改名 `retry.partial`（PR #1743，对既有用户不构成破坏） | 官方原文："slskd should refuse to start informing them of this" | S18 |

**机制（S14:354-368，master 源码）**：四个旧键是 `[Obsolete] public object X { get; init; } = null;` 哨兵，靠「非 null 即存在」检测，在 `Validate()` 里添加 `ValidationResult` → 启动失败。三条可直接用作断言的原文：

```
The 'global' and 'groups' keys have been moved under a new 'transfers' key.  See https://github.com/slskd/slskd/pull/1672 for details, and make the necessary changes to remove this error
The 'integration' key has been renamed to 'integrations'.  Add an 's' to the end of the key to remove this error (no other changes were made)
The 'permissions' keys have been moved under a new 'destination' key under transfers -> download, and the behavior has changed.  See https://github.com/slskd/slskd/pull/1756 for details
```

> ⚠️ 注意 `[Obsolete("temporary sentinel to warn users about breaking change")]` 这个属性文本里的 "warn" **是属性注释用词，不是运行行为**；实际路径是 `ValidationResult` → 启动失败。P1/子代理 A 曾表述为「警告」，以本节为准。

**5.1.8 NAS 平台（T3 为主，须标注可信度）**

- **Unraid**：存在 hotio 官方 CA 模板（id `slskd-1ca6hh31pcfhq3`）。一手 XML 实测变量见 §4 第 6 条。另有 binhex 社区模板（仅命中论坛标题，未核 XML，标注待核对）
- **TrueNAS**：官方文档确认 UID 默认 568（apps）。`user: 568:568` 用于 slskd 属**组合推断**，非被引用原始资料
- **群晖**：**无 slskd 一手资料**，勿编造

---

### 5.2 账号、共享与网络规则

**5.2.1 账号（官方口径务必写准）**

- 官方站点**不提供注册入口**：`/news/user/register` → HTTP 403 "Access denied — You are not authorized to access this page."；全站导航仅 Home / About / Download / Forum / Changelog / FAQ / Rules / Donate，**无 Register 项**；站点登录页要求「Enter your Soulseek username」（即填 Soulseek 用户名，不是独立网站账号）（S20 / S24）
- TOS 有「注册表单」的条件式样板条款，但**页面上并无实际表单**（S20）
- **账号创建发生在哪一步，官方从未说明** → 不得写成官方要求
- **用户名 30 天不登录被回收**（官方 FAQ 明文）：「Soulseek recycles usernames after a full month of the person not logging in」；有 privileges 则保留至「30 天未登录」与「privileges 到期」二者较晚者（S21）
- **一次性捐款 $5+ 则用户名永不过期**：「your username will never expire」（S23）
- 密码**无法找回**（社区：协议文档「There is no mechanism to reset a forgotten password」，S26）
- 访问权可随时撤销：「Access to the SoulSeek® server is a privilege; not a right. It may be revoked at any time, for any reason.」（S20）
- 滥用后果：「Server or chatroom abuse will result in your connection being closed and your ISP notified.」（S20）

**5.2.2 共享要求（官方 vs 民间，是最容易被写错的一节）**

- **官方规则页全文无任何最低共享数量或容量条款**（逐句核对 S20）
- **官方明确拒绝在客户端内置 autoban**：node/523 中官方称 "automatically banning users ... one I've always resisted strongly"，实际实现的是「自动空共享**警告**机制」（S22）
- 官方 FAQ 立场：不共享有多种原因（S24）
- **「必须共享 X 文件 / X GB 才能下载」类阈值不是官方规则**：官方规则页与 FAQ 均无此条。用户 info 里显示的 autoban 阈值、社区客户端的 autoban 设置属**用户自设**（T3，须明确标注）
- **三层必须分开写**：① 服务器规则（无强制共享门槛）② 对端客户端的用户自设阈值 ③ slskd 内置 `leechers` 组的限速（见 §5.3.3）

**5.2.3 客户端政策（与 slskd 直接相关，需中性呈现）**

- **同一 IP 最多 5 个客户端连接**：「Users are allowed to connect up to a maximum 5 clients from the same IP.」（S20）→ 直接关系到 Relay 模式与「同时跑 slskd + 官方客户端」的场景
- **bot / 自动化客户端 / 残缺脚本禁止接入**：「automated clients (robot/bot) ... are not allowed to connect to the Soulseek® service」（S20）
- **第三方客户端「被容忍」但有条件**：「Alternative clients ... that implement the full range of features ... are tolerated」（S20，条件为非 Windows 平台）
- 管理员可无预警切断任意连接；官方鼓励使用官方客户端（S20）
- 禁止随机生成的用户名（S26，社区，其自引 S20）

> 写作口径：只作**客观技术/政策说明**，不做合规判断，不把「P2P 网络」「版权」写成劝诫。VPN 与合规属用户自身责任。

**5.2.4 入站连接与端口**

- 「The Soulseek client sets up a listening port to accept incoming TCP connections.」（S24）
- 路由器可能拦截；官方客户端用 UPnP 自动映射（S24）
- 官方承认存在「ISP 使连接无法接受入站 TCP」的情形（S24）
- 默认监听端口不再是 80；**首次运行时随机生成**（S25 changelog）；协议文档记 2234（S26，社区）
- **协议混淆（obfuscated port）**：官方功能，用于应对 ISP 流量整形；通常 = 监听端口 + 1；非强制，对端不支持则回退明文（S25）。FAQ 未收录

**5.2.5 Relay 模式（Controller / Agent，S7）**

- 定位：Controller 连 Soulseek 网络并作为客户端；Agent 连 Controller 而非 Soulseek 网络，只把文件中继给 Controller。可理解为「slskd 的远程存储」
- 适用场景：多地点供档但不想多个账号；不想用/不信 VPN；无法配好端口转发但想要完整功能；高流量分流；保持远程队列位置
- 安全设计：Controller↔Agent 之间（可选）HTTPS 端到端加密；**Agent 主动连 Controller**，故家庭网络无需开端口/入站流量；Controller 侧要求 API key，每个 Agent 另有共享 secret；Agent 配置与 API key 可按 IP / CIDR 限定
- 配置要点：Controller 侧 `relay.enabled: true` + `relay.mode: controller` + `relay.agents.<name>.secret` / `cidr`，并在 `web.authentication.api_keys.<name>` 建一个 `role: readwrite` 的 key；Agent 侧 `relay.mode: agent` + `relay.controller.address` / `api_key` / `secret` / `downloads`
- **Agent 的顶层 `instance_name` 必须与 Controller 上配置的 agent 名一致**
- 生成 secret：`./slskd --generate-secret 32`；长度 16–255
- 官方在示例中演示了自签证书 + `ignore_certificate_errors: true`

---

### 5.3 日常使用与配置详解

**5.3.1 Web UI 实际功能面（源码取证，官方无操作文档）**

导航项（`src/web/src/components/App.jsx`）：Dashboard `/dashboard`、Search `/searches`、Downloads `/downloads`、Uploads `/uploads`、Rooms `/rooms`、Chat `/chat`、Users `/users`、Browse `/browse`；右组 Theme、连接状态、System `/system`、Log Out。**Agent 模式下整组导航被替换，只渲染 System。**

| 视图 | 可核实的实际功能 |
| --- | --- |
| Dashboard | 历史区间 24h / 7d / 30d / 90d / 180d / 1y / All；数据块 summary、histogram、leaderboard(upload/download)、directories、exceptions(pareto/recent) |
| Search 列表 | 列：状态、Search、Files、Locked、Responses、Ended、操作；操作为 Completed→trash，否则→stop |
| 结果卡片头部 | 折叠箭头；绿/黄圆点 = 有免费槽位；用户名；X 隐藏该用户 |
| 结果卡片元信息 | Upload Speed、Free Upload Slot YES/NO、Queue Length |
| 结果文件表 | 勾选、File、Size、Attributes、Length |
| 下载按钮 | `Download` + 「N files, size」标签；含 progress / complete / error 三态 |
| 目录补全 | 「Search for Additional Files in This Directory」按钮 |
| 分页 | 初始显示 5 条，每次 +5，「Show N More Results」 |
| Downloads / Uploads | 同一组件按 `direction` 区分；批量操作：Retry All{Errored/Cancelled/All}、Cancel All{All/Queued/In Progress}、Remove All{Succeeded/Errored/Cancelled/Completed} |
| 传输表 | 列：勾选、File、Progress、Size、详情图标；单文件可重试 / 排队中可插队 |
| Chat | 会话列表、时间戳/用户名/正文、5 秒轮询、acknowledge、回复 |
| Browse | 目录树；结果缓存在 IndexedDB `slskd-browse`；分隔符 `\\`；500ms 轮询状态 |
| Users | 用户名查询；`localStorage` 记忆 |
| System | 页签 Info、Options、Shares、Files、Data、Events、Logs |
| 主题 | 切换 + `localStorage['slskd-theme']`；新版本可用时弹窗链到 releases |

**搜索结果排序 / 筛选（`SearchDetail.jsx` + `lib/searches.js`）**

- **排序只有 2 项**：`uploadSpeed`（默认，降序）、`queueLength`（升序）
- **三个开关**：`hideLocked` 默认 **true**、`hideNoFreeSlots` 默认 **false**、`foldResults` 默认 **false**
- **筛选语法**（不区分大小写）：

| 语法 | 别名 | 语义 |
| --- | --- | --- |
| `minbitrate:N` | `minbr:` | 剔除 `bitRate < N` |
| `minbitdepth:N` | `minbd:` | 剔除 `bitDepth < N` |
| `minfilesize:N` | `minfs:` | 剔除 `size < N` |
| `minlength:N` | `minlen:` | 剔除 `length < N`（秒） |
| `minfilesinfolder:N` | `minfif:` | 比较 `fileCount + lockedFileCount`，命中则整条结果置空 |
| `isvbr` | — | 保留 `isVariableBitRate` 为真 |
| `iscbr` | — | 剔除 undefined 或为真者 |
| `islossless` | — | 保留同时有 `sampleRate` 与 `bitDepth` |
| `islossy` | — | 保留两者皆无 |
| `词` | — | 文件名 **AND** 包含 |
| `-词` | — | 文件名包含则剔除 |

- Attributes 列渲染规则：有 `sampleRate`+`bitDepth` → `位深/采样率kHz`；`isVariableBitRate` → `N Kbps, VBR`；否则 `N Kbps`
- ⚠️ 两处已知边界（源码可读、真实交互需实测）：`minfilesinfolder` 比较的是文件数而非「目录内文件数」，**命名与行为不一致**；且 `hideLocked=true`（默认）时 `lockedFileCount` 被置 0 后再参与计算，导致该过滤在默认开关下被静默削弱

**5.3.2 配置源优先级与合并陷阱（S3）**

```
Default Values < Environment Variables < YAML Configuration File < Command Line Arguments < Run-Time Overlay
```

- 默认值来自 `Options.cs`；env 一律加 `SLSKD_` 前缀；YAML 默认读 `<应用目录>/slskd.yml`（可用 `SLSKD_CONFIG` 或 `--config` 改）
- 应用**监视 YAML 变更并热重载**，实时推送到 Web UI；需要重连/重启才生效的项会置标志
- 启动时若无 YAML 文件，会把 `/config/slskd.example.yml` 复制过去
- **列表合并陷阱（必须写进正文）**：.NET 对列表**既追加又覆盖**。env 给 `one;two;three`，YAML 给 `[foo, bar]`，结果会是 `foo, bar, three`。→ 列表型选项（`shares.directories`、`shares.filters`、`filters.search.request`、`rooms` 等）不要跨源混设
- env 表示列表用分号 `;` 分隔；CLI 表示列表用重复参数
- **Run-Time Overlay 目前只支持 `soulseek.listenPort` 与 `soulseek.listenIpAddress`**，且是「sticky 但 volatile」——重启即丢；改 `listenPort` 后**无需重连**，服务器会被自动更新
- `app_dir` / `config` 不能在 YAML 里设（`[JsonIgnore][YamlIgnore]`）

**5.3.3 顶层键与分组（已用源码交叉核对）**

**21 个有效顶层键**：`debug`、`headless`、`remote_configuration`、`remote_file_management`、`instance_name`、`flags`、`relay`、`directories`、`shares`、`transfers`、`blacklist`、`filters`、`rooms`、`web`、`retention`、`throttling`、`logger`、`metrics`、`feature`、`soulseek`、`integrations`。

**4 个 `[Obsolete]` 哨兵键（写入即启动失败）**：`permissions`、`global`、`groups`（顶层）、`integration`。

> `example.yml` 的顶层键与上述 21 个**完全一致**（无多余、无缺失），可作交叉验证。

**用户组（`transfers.groups`）**

- `default`：未被显式分组、非 privileged、非 leechers 的用户
- `leechers`：共享文件数与目录数低于 `thresholds`（默认各为 1，即**至少共享一个目录且其中至少一个文件**才不算 leecher）
- `privileged`：在 Soulseek 网络购买了 privileges 的用户。**不可配置**，priority 0（最高），策略 `FirstInFirstOut`，可用任意多槽位至全局上限，**不受任何 limits 约束**
- `blacklisted`：`members`（用户名）/ `patterns`（用户名正则）/ `cidrs`
- `user_defined.*`：自定义组，可含 `members` 与 `upload` 设置
- 组 `priority` 从 1 起，**数字越小优先级越高**；队列策略 `firstinfirstout` 或 `roundrobin`
- 组级 `slots` / `speed_limit` 默认 `int.MaxValue`，即可延后到全局限制；若组级超过全局，则**全局成为约束**
- 组级 upload limits 可覆盖全局默认；两者都未设则**上传不限**；想对某组不设限就设为 `int.MaxValue` 或 `2147483647`

**常用默认值（代码真值，与官方文档示例不同处已标注）**

| 键 | 代码默认 | 文档写法（若不同） |
| --- | --- | --- |
| `logger.no_disk` | `false`（**默认写盘**） | docs/config.md YAML 块写 `disk: false`，**错** |
| `web.port` / `web.https.port` | `5030` / `5031` | — |
| `web.authentication.username` / `password` | `slskd` / `slskd` | — |
| `web.authentication.jwt.ttl` | `604800000` ms（7 天） | — |
| `web.authentication.jwt.key` | `null` → **每次启动随机生成** | — |
| `web.authentication.api_keys.*.role` | `readonly`（primary key 为 `administrator`） | — |
| `web.authentication.api_keys.*.cidr` | `0.0.0.0/0,::/0` | config.md 散文写 `0.0.0.0/0,::0`，**漏斜杠** |
| `soulseek.address` / `port` / `listen_port` | `vps.slsknet.org` / `2271` / `50300` | — |
| `soulseek.diagnostic_level` | `info`（小写） | 文档示例写 `Info`，大小写敏感性未验证 |
| `soulseek.distributed_network.child_limit` | `25` | — |
| `shares.cache.storage_mode` | `memory` | — |
| `shares.cache.workers` | `Environment.ProcessorCount` | 文档示例 4 / example.yml 16，**均非默认** |
| `shares.cache.retention` | `null`（不自动重扫） | — |
| `transfers.upload.slots` | **`10`** | 文档与 example.yml 均写 20，**均非默认** |
| `transfers.upload.speed_limit` | `int.MaxValue` | example.yml 示例 1000 |
| `transfers.download.slots` / `speed_limit` | `int.MaxValue` / `int.MaxValue` | example.yml 示例 500 / 1000 |
| `transfers.download.retry.partial` | `resume` | — |
| `transfers.download.destination.subdirectory` | `${SOURCE_DIRECTORY}` | — |
| `transfers.download.destination.exists` | `rename` | — |
| `transfers.download.destination.permissions.mode` | `null`（不 chmod） | — |
| `transfers.groups.<g>.upload.priority` | `1` | 内置组 priority 真值**未裁决**，见 §8 |
| `retention.search` | `null`（永久保留） | config.md 写 1440 / example.yml 写 10080，**均非默认** |
| `retention.logs` | **`30` 天** | 文档散文与 example.yml 均写 180，**与代码不符** |
| `throttling.search.incoming.concurrency` | `10` | — |
| `throttling.search.incoming.circuit_breaker` | `500` | — |
| `throttling.search.incoming.response_file_limit` | `500` | — |
| `metrics.enabled` / `url` | `false` / `/metrics` | — |
| `feature.swagger` | `false` | — |
| `blacklist.enabled` / `file` | `false` / `null` | — |
| `flags.optimistic_relay_file_info` | `false` | config.md 漏载 |
| `flags.no_sqlite_pooling` | `false` | **两份文档均漏载** |

**5.3.4 目录、过滤与黑名单**

- `directories.incomplete` / `directories.downloads` 默认 `APP_DIR/incomplete`、`APP_DIR/downloads`，启动时自动创建
- `shares.filters` 默认 `\.ini$`、`Thumbs.db$`、`\.DS_Store$`（正则，加 `$` 锚定）
- `blacklist.enabled` 默认 `true`；`blacklist.file` 指向一个装 CIDR 的文件（托管黑名单）。**注意**：该文件不存在、格式无法识别、或运行中被修改时，**应用会退出**
- `filters.search.request` 默认示例 `^.{1,2}$`（过滤过短搜索词）

---

### 5.4 安全与进阶速览

**5.4.1 默认凭据与远程配置（S3、S14）**

- Web UI 与底层 API **默认启用认证**，默认账号密码均为 `slskd` / `slskd` → 面向公网必须改
- `remote_configuration` 默认 **`false`**（S14:185；S3:95）。官方警告：「If an attacker were to gain access to the application and retrieve the YAML file, any secrets contained within it will be exposed.」
- `remote_file_management` 默认 `false`：**列目录始终允许，删除默认禁用**
- README（S1）与 config.md（S3）在 `SLSKD_REMOTE_CONFIGURATION` 上的推荐口径不同——**README 的 quick-start 里出现 `SLSKD_REMOTE_CONFIGURATION=true`，而 config.md 的默认值是 `false` 并附安全警告**。写作时须并列呈现，不做单向取信

**5.4.2 认证细节（S3）**

- API key 认证**不配合 HTTPS 时不推荐**（"NOT RECOMMENDED"）
- JWT 会过期，API key 不会
- **本应用不支持 `X-Forwarded-For`**（或类似头），理由是「a bad actor can easily fake it」→ **反向代理后面按 CIDR 过滤可能失效**
- 自定义 JWT key 可被用于伪造有效 JWT，必须保密；默认每次启动随机生成，故重启会使已签发 JWT 失效

**5.4.3 API Key CIDR 绕过缺陷 #1605（已修复，但分两处、版本区间不同）**

- 受影响区间：用户报告自 **0.24.3.0** 起
- 根因（维护者原文）：写带 `::ffff:` 前缀的 CIDR 时，解析库会把它转成 `::/0`——即**匹配一切**，等于放行全部
- 修复分两处：**API 鉴权侧** PR #1606 随 **0.24.4** 发布；**relay 登录侧**的遗漏部分由 PR #1714 修复，维护者 2026-08-12 原文「**This was released in 0.26.0**」
- → 对 Relay + CIDR 白名单用户，**0.26.0 是安全底线**

**5.4.4 反向代理（S6）**

- 因为用了 websocket，除 `proxy_pass` 外必须设 `Upgrade` / `Connection "Upgrade"` / `Host` 头，并 `proxy_request_buffering off`
- 子目录部署时 `URL_BASE` 必须设为对应前缀（如 `/slskd`）；根路径部署则保持默认 `/`
- 文档给出 NGINX（子目录 / 根 / SWAG）、Apache（`upgrade=websocket`）、IIS（URL Rewrite + `web.config`）四套配置

**5.4.5 VPN 绑定（官方口径必须写准，S5、S3）**

> 官方原文：「**Configuring a VPN integration does not change how network traffic to the Soulseek server or other peers is routed**.」

- 该集成**不改变流量路由**，只提供：① 可见性 ② 便于应用动态转发的端口 ③ 对未用 kill switch 的用户的极轻量保护
- 机制：轮询外部服务获取 VPN 状态（连通性、转发端口等），据此连接或断开与 Soulseek 服务器的连接
- gluetun 侧需开控制服务器：`GLUETUN_HTTP_CONTROL_SERVER_ENABLE=on`，`HTTP_CONTROL_SERVER_AUTH_DEFAULT_ROLE='{"auth":"apikey","apikey":"abcd123"}'`
- slskd 侧：`SLSKD_VPN=true`、`SLSKD_VPN_PORT_FORWARDING=true`（强制等待 gluetun 给出端口）、`SLSKD_VPN_GLUETUN_URL=http://localhost:8000`、`SLSKD_VPN_GLUETUN_API_KEY=...`
- 配置键在 `integrations.vpn.*`（含 `polling_interval` 默认 `2500`、`gluetun.url` / `timeout` / `auth` / `api_key`）
- 官方提供 Proton VPN 推荐链接 + 完整参考 compose（`network_mode: service:gluetun`）
- → **实际路由由用户自行确保**（例如与 gluetun 共享网络命名空间）。写作时不得表述为「绑定 VPN 后流量就会走 VPN」

**5.4.6 脚本集成的 RCE 风险（S3）**

> 官方原文：「**Remote Code Execution Risk**: The event data in `$SLSKD_SCRIPT_DATA` originates from the Soulseek network and may contain malicious content.」

正确用法是**读环境变量**；**禁止**命令替换与直接传参。事件数据来自网络，属不可信输入。

**5.4.7 其他集成与特性**

- `integrations` 下有 `vpn`、`webhooks`、`scripts`、`ftp`、`pushbullet`
- webhook 事件示例 `DownloadFileComplete`；可设 headers、超时、重试
- `metrics.enabled` 默认 false，启用后 `/metrics`，默认凭据同 Web UI（`slskd`/`slskd`）→ 官方建议公网保持禁用或改凭据，因为会暴露操作系统、架构、磁盘等系统配置
- `feature.swagger` 默认 false，启用后 `/swagger` 提供 OpenAPI，是开发对接与「哪些选项支持 Run-Time Overlay」的唯一权威入口
- `throttling.search.incoming` 官方标注为 **Application Stability Risk**，是宿主性能边界的调节项
- MCP / 第三方生态：P1 记为「第三方低星，需打折」，本轮未补充一手证据 → 保持打折口径或省略

---

## 六、矛盾与不一致汇总（写作时必须并列或按裁决标注）

| # | 冲突面 | 双方说法 | 处理方式 |
| --- | --- | --- | --- |
| M1 | `remote_configuration` 推荐值 | README quick-start 出现 `=true`；config.md 默认 `false` + 安全警告；Options.cs 默认 `false` | **并列呈现**，说明「README 的 quick-start 场景」与「公网部署的安全建议」是两个语境 |
| M2 | `logger` 磁盘日志键名 | docs/config.md YAML 块 `logger.disk`；example.yml `logger.no_disk`；Options.cs `NoDisk` | **按 `no_disk` 写**，并在「常见坑」里点明官方文档此处有误 |
| M3 | `integrations` 单复数 | docs/config.md 自身不一致（Webhooks 用复数，Scripts/VPN/FTP/Pushbullet 用单数）；example.yml 全用复数；Options.cs `IntegrationsOptions` | **按 `integrations` 写**，注明单数是 `[Obsolete]` 哨兵，写了会**启动失败** |
| M4 | 顶层 `groups` 位置 | docs/config.md User Blacklist 节用顶层 `groups:`；Groups 节用 `transfers.groups`；example.yml + Options.cs 均为 `transfers.groups` | **按 `transfers.groups` 写**；顶层 `groups` 写了会**启动失败** |
| M5 | 内置组 priority | docs/config.md `default:1` / `leechers:99`；example.yml `default:500` / `leechers:999`；Options.cs 类默认 `1` | **未裁决**，见 §8。正文只讲「数字越小优先级越高」与「privileged 固定为 0」，不给具体数字 |
| M6 | `retention.logs` 默认 | docs/config.md + example.yml 均写 180；Options.cs `= 30` | **按代码 30 写**，并注明文档写的是示例值 |
| M7 | `transfers.upload.slots` 默认 | 文档 + example.yml 均写 20；Options.cs `= 10` | **按代码 10 写** |
| M8 | #1429 vs #1805 | P1 误判为「结论相反」 | 按 §3 C5 修正后的口径写 |
| M9 | 账号创建方式 | 官方无注册入口（已证）；「需 SoulseekQt」为社区推断 | 按 §4 第 2 条口径写，**不得标为官方** |

---

## 七、实操指引（可直接进正文的结论）

1. **三种身份模式选一个，别混**：官方推荐 `user:`（ex. `user: 1000:1000`）；用 `PUID`/`PGID` 会走 root → usermod → gosu 的老路径，且**不递归** chown；两者同时给会直接 `exit 1`
2. **一定挂载 `/app`**：否则配置与数据随容器删除丢失（entrypoint 会警告）
3. **权限不一致的典型症状**：下载文件属主为 root 或宿主机无法读写 → 检查 `user:` / `PUID`/`PGID` 与 `SLSKD_UMASK`（默认 `0022` → 文件 644）
4. **端口映射**：Web UI `5030`（+`5031` HTTPS）必须映射；Soulseek 入站 `50300` 需 **TCP 入站**可达，否则只能主动下载、无法被他人连接
5. **升级前先跑一遍旧键检查**：`global` / `groups`（顶层）/ `integration` / `permissions` 任一存在 → 直接启动失败，按 §5.1.7 的三条原文提示改
6. **不要用 CoW 或网络文件系统放应用数据**；必须用时开 volatile 模式并接受重启丢失
7. **配置合并**：列表型选项不要跨源混设（env 分号 + YAML 列表 = 追加半截）
8. **改完配置**：多数项热重载生效；标记 `RequiresRestart` 的需重启；`RequiresReconnect` 的需重连
9. **公网部署最小动作**：改默认账密 → 保持 `remote_configuration=false` → `metrics` 保持禁用 → 反代时注意 CIDR 过滤失效
10. **用 Relay 时**：Agent 顶层 `instance_name` 必须等于 Controller 上配置的 agent 名；CIDR 白名单请确保 ≥0.26.0

---

## 八、开放问题（转入写作时的处理约定）

| # | 问题 | 处理约定 |
| --- | --- | --- |
| O1 | 内置 `default`/`leechers` 组的实际生效 priority（代码类默认 1，两文档给 500/999） | 正文**不给具体数字**，只讲语义（越小越优先、privileged 固定 0） |
| O2 | 0.26.0 是否真的会因 `--file-permission-mode` / `SLSKD_FILE_PERMISSION_MODE` 拒绝启动（release note 说是，master 源码只见顶层 `permissions` 哨兵） | 正文只写「顶层 `permissions` 已迁移，旧写法会启动失败」；env / CLI 形态不展开 |
| O3 | `flags.no_sqlite_pooling` 是否属有意不公开的内部开关 | 不写入正文（避免把未文档化开关当推荐项） |
| O4 | `soulseek.diagnostic_level` 大小写敏感性 | 正文按示例写 `Info`，不宣称大小写规则 |
| O5 | YAML 键名到属性名的下划线约定**未找到显式配置点**（`Program.cs` / `OptionsBuilder.cs` 均未 grep 到 `NamingConvention`），结论由「属性名 ↔ example.yml 键」实证反推 | 不影响正文；仅作方法学备注 |
| O6 | `user: 568:568` 用于 slskd 的原始出处（wiki.serversatho.me 全程 403） | 若写入，必须标「组合推断：官方 `user:` 写法 + TrueNAS apps=568」，不得标为原始资料 |
| O7 | binhex Unraid 模板变量细节（仅命中论坛标题） | 不写入，或标明「未核实」 |
| O8 | 群晖部署 | **不写**，无一手资料 |
| O9 | Web UI 筛选的两处边界行为（`minfilesinfolder` 语义、`hideLocked` 静默削弱） | 可作为「进阶技巧 + 已知怪癖」写入，标注「源码可读，实际效果需自测」 |
| O10 | MCP / 第三方 Web UI 生态 | 保持「第三方项目，成熟度需自行评估」的打折口径 |

---

## 九、下游交接（outline-generator / chapter-writer）

**交接原则**：下游拿到的是**来源 ID + 本地路径 + 锚点**，不是本文件的转述。凡本文件出现「官方原文」「官方口径」「官方说明」之处，写作时**必须回 `sources/` 原文件逐条比对**，不得直接采信本文件的措辞。

- **本地信源根**：`workspace/slskd-usage/sources/`
- **可直接引用的 T1 文件**：`README.md`(S1)、`docs_docker.md`(S2)、`docs_config.md`(S3)、`docs_known_issues.md`(S4)、`docs_vpn.md`(S5)、`docs_reverse_proxy.md`(S6)、`docs_relay.md`(S7)、`docs_migrations.md`(S8)、`docs_system_requirements.md`(S9)、`config_slskd.example.yml`(S11)、`Dockerfile`(S12)、`Options.cs`(S14)
- **无本地副本、需按 ID 回溯**：S15–S35（前端源码走 `cdn.jsdelivr.net/gh/slskd/slskd@master/src/web/...`；slsknet.org 各 node；GitHub issue/PR/release）
- **建议章节骨干**（对应用户已确认的三主线 + 一压缩章）
  - 第 1 章 部署与运行：§5.1.1 端口 → §5.1.2 三种身份 → §5.1.3 官方推荐 → §5.1.4 镜像/健康检查 → §5.1.5 系统要求与不兼容 → §5.1.6 升级迁移 → §5.1.7 破坏性变更 → §5.1.8 NAS
  - 第 2 章 账号与共享：§5.2.1 账号 → §5.2.2 共享（三层分开）→ §5.2.3 客户端政策 → §5.2.4 入站与混淆端口 → §5.2.5 Relay
  - 第 3 章 日常使用与配置：§5.3.1 Web UI（**开篇即声明官方无操作文档，功能面由前端源码取证**）→ §5.3.2 配置源与合并陷阱 → §5.3.3 顶层键与分组 → §5.3.4 目录/过滤/黑名单
  - 第 4 章 安全与进阶速览（压缩）：§5.4.1–§5.4.7
  - 各章末尾附「常见坑」小节，素材取 §七 与各节 ⚠️ 标注
- **强制约束（写入每一章）**
  1. 端口三线区分：`5030/5031` = Web UI，`50300` = Soulseek 入站，`2271` = Soulseek 服务器
  2. 键名一律以 `Options.cs` + `example.yml` 为准；遇到 M2/M3/M4 三处官方文档错误，在「常见坑」里显式点出
  3. `#1429` / `#1805` 按 §3 C5 修正口径，不写「结论相反」
  4. 账号创建按 §4 第 2 条口径，不得写成「官方要求用 SoulseekQt 注册」
  5. 共享要求分三层，不得把社区 autoban 阈值写成官方规则
  6. VPN 一节必须写「不改变流量路由」
  7. **禁止引用 `soulseekqt.net`**
  8. Soulseek P2P / 版权 / VPN 合规只做客观技术说明，不作劝诫或法务判断
**版本锚点**：0.26.0（2026-07-19）。凡涉及「最新版本」的表述以本锚点为准，并注明日期。
