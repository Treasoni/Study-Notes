---
title: "学习笔记大纲：slskd 自托管 Soulseek 客户端实战指南"
type: outline
workflow_id: learning-note-flow
run_id: slskd-usage
version_anchor: 0.26.0
created: 2026-09-14
---

# 学习笔记大纲：《slskd：自托管 Soulseek 客户端实战指南》

> 笔记类型：实战 · 操作指南
> 深度：入门 → 上手
> 读者：有 Docker 与自托管应用基础，新接触 slskd
> 版本锚点：0.26.0（2026-07-19）
> 预计总篇幅：约 4.2 万汉字（含分册 README）
> 章节数：4 章 + 分册 README 索引

---

## 分册规划

### 为什么要分册

最终笔记预计 4.2 万汉字，章节数 4 章，均超过「30 KB 或 3 章」的门槛，因此按分册发布，与既有 `docker/MusicTagWeb音乐标签/` 同构：一个子目录 + README 索引 + 一章一文件。

### 目标目录结构（本阶段只做规划，不写入 vault）

```text
docker/
├── Docker MOC.md                              # 既有 MOC，追加一条索引项
└── slskd自托管Soulseek客户端/                  # 分册根目录
    ├── README.md                              # 分册索引（MOC 指向此文件）
    ├── 01 部署与运行.md
    ├── 02 账号与共享机制.md
    ├── 03 日常使用与配置详解.md
    └── 04 安全与进阶速览.md
```

发布前先在项目工作区落 `output/`，用户确认后再复制到 `docker/slskd自托管Soulseek客户端/`。

### 文件命名与导航

| 文件 | 章 | 角色 |
| --- | --- | --- |
| `README.md` | — | 分册索引：本分册覆盖什么、四章一句话摘要、推荐阅读顺序、指向 `04` 章安全清单的直达链接 |
| `01 部署与运行.md` | 第 1 章 | 环境与首次启动 |
| `02 账号与共享机制.md` | 第 2 章 | 账号、共享、入站、Relay |
| `03 日常使用与配置详解.md` | 第 3 章 | Web UI 操作 + 配置体系 |
| `04 安全与进阶速览.md` | 第 4 章 | 公网化与集成 |

- **prev/next 导航**：每章文件在 frontmatter 之后、正文之前放一行导航条
  `[[README|目录]] · [[01 部署与运行|← 上一章]] · [[02 账号与共享机制|下一章 →]]`
  章末再放一次同样的导航条。首章省略 `← 上一章`，末章省略 `下一章 →`。
- **MOC 更新**：`docker/Docker MOC.md` 只追加**一条**索引项，不复制正文：
  `- [[slskd自托管Soulseek客户端/README|slskd：自托管 Soulseek 客户端]] - 一句话说明 #docker #slskd`
- **跨章引用**：章内互相引用用 wikilink，例如第 1 章讲端口时引 `[[02 账号与共享机制#2.4 入站连接与端口自检]]`；示例不重复粘贴，用 `见 [[03 日常使用与配置详解#EX-06]]` 形式指路。

### 分册边界（明确声明）

**本分册止于「能跑起来、能下到文件、知道哪些配置会咬人」这条线。**

- **在本分册内展开**：Docker / compose / 二进制部署、容器运行身份与权限、端口三线、系统要求与不兼容文件系统、升级与破坏性变更、NAS 平台可信度标注、账号官方口径、共享三层结构、入站连接与混淆端口、Relay 定位与配置骨架、Web UI 全流程、配置源优先级与合并陷阱、顶层键与用户组、目录/过滤/黑名单、安全与进阶速览（压缩）。
- **明确不展开（只给「是什么 + 入口在哪 + 去哪查」）**：Relay 的多 Agent 编排与故障转储、脚本集成的完整事件清单、webhook / ftp / pushbullet 的逐个事件参数、API 全量端点参考、Web UI 前端源码级的二次开发、MCP 与第三方生态评估、群晖部署。
- **预留命名空间**：若后续要展开上述内容，另开分册二，文件名从 `05` 起编号，不插队到 `01–04`。

---

## 第 1 章 部署与运行

### 章节目标

让读者从零把 slskd 容器跑起来并成功登入 Web UI，分清三条端口的各自职责，选对容器运行身份，并在升级前避开已知的不兼容文件系统与破坏性键名变更。

### 小节结构

```text
### 1.1 先分清三条线：端口语义
    #### 5030 / 5031 —— Web UI（HTTP / HTTPS 自签）
    #### 50300 —— Soulseek 入站监听（别人来敲的门）
    #### 2271 —— 出站到 Soulseek 服务器
    #### 容器内环境变量命名：为什么是 SLSKD_SLSK_LISTEN_PORT
    #### [!tip] 大白话 + 类比（Web UI = 自己家的门；50300 = 邻居来敲门；2271 = 打给总台的电话）
### 1.2 产物一：docker-compose.yml（推荐路径）
    #### 最小可用 compose（官方镜像 + user:）
    #### 端口映射段落逐行说明（三线对应）
    #### 卷挂载：为什么必须挂 /app
    #### 环境变量段落（监听端口 / umask / volatile）
    #### 两种用户写法对照（user: vs PUID/PGID）—— 二选一
    #### [!tip] 大白话 + 类比（user: 是"以谁的身份上班"；PUID/PGID 是"上班后再换工牌"）
### 1.3 产物二：slskd.yml（首次启动自动生成）
    #### 文件从哪来：无 YAML 时从示例复制
    #### 应用目录与配置文件位置
    #### 【EX-06】全文唯一一份完整 slskd.yml 综合样例（后续所有片段都从它截取）
    #### 本分册会改到的顶层键速查（指向第 3 章）
### 1.4 产物三：docker run 命令行（与 compose 等价）
    #### --user 写法
    #### -p 三条端口映射
    #### -v 应用目录挂载
### 1.5 产物四：二进制运行
    #### 与容器路径的差异点（无 entrypoint 身份逻辑）
    #### 何时才考虑二进制
### 1.6 三种容器运行身份（entrypoint 三分支）
    #### ① 现代 Docker：给了 --user / user:
    #### ② 传统风格：给了 PUID 或 PGID
    #### ③ 都不给：以 root 运行（向后兼容行为）
    #### 同时给 --user 与 PUID/PGID 的后果
    #### chown 的作用范围（非递归，仅根目录）意味着什么
    #### [!tip] 大白话 + 类比（三种身份 = 三种入职方式，第 3 种是没人管你）
### 1.7 官方立场：为什么推荐 user:
### 1.8 镜像、健康检查与启动宽限期
    #### 镜像来源与 registry 选择
    #### HEALTHCHECK 的实现与 60 分钟 start-period 的含义
    #### 首次共享扫描可能很慢 → 对应第 2 章 §2.3
### 1.9 系统要求与已知不兼容
    #### 最低配置与 ARMv6 / Raspberry Pi Zero
    #### CoW 文件系统（BTRFS / ZFS）
    #### 网络文件系统（NFS / SMB / Windows 共享）
    #### volatile 模式：换来的稳定与丢掉的记录
    #### 云主机 OOM 案例
    #### [!tip] 大白话 + 类比（把数据库放在会被快照的文件系统上 = 在流水席上记账）
### 1.10 首次启动与首次登录
    #### 默认凭据与登入地址
    #### 健康检查地址与判定
    #### 日志里应该看到什么
    #### 端口可达性自测（EX-10）
### 1.11 升级与数据库迁移
    #### 迁移自动执行与 backups/ 命名规则
    #### 手工回滚的分步操作
    #### 陷入重启循环时的处理
    #### 预防动作清单
### 1.12 破坏性变更时间线（升级检查清单）
    #### 0.25.0：四个旧键
    #### 0.26.0：permissions 迁移与 retry 改名
    #### 哨兵的检测机制（非 null 即存在 → ValidationResult → 启动失败）
    #### 三条启动失败提示原文（引用块）
### 1.13 NAS 与平台模板（须标注可信度）
    #### Unraid 官方 CA 模板实测变量
    #### TrueNAS 的 UID 与"组合推断"标注
    #### 群晖：无一手资料，不写
### 1.14 本章常见坑（汇总 §七 1–5、§八 O6/O7/O8，并指路第 3 章键名错误）
```

### 素材映射

| 小节 | 信源 ID | 本地路径 / 锚点 |
| --- | --- | --- |
| 1.1 | S14, S12, S11 | `workspace/slskd-usage/sources/Options.cs:2019`、`:2319`、`:1770`、`:1706`、`:1716`；`sources/Dockerfile:75`；`sources/config_slskd.example.yml` |
| 1.2 | S1, S2, S12, S11 | `sources/README.md`（Quick Start 段）；`sources/docs_docker.md`；`sources/Dockerfile:97-192` |
| 1.3 | S3, S11, S14, S2 | `sources/docs_config.md`；`sources/config_slskd.example.yml`；`sources/Options.cs`；`sources/docs_docker.md` |
| 1.4 | S1, S2 | `sources/README.md`；`sources/docs_docker.md` |
| 1.5 | S1 | `sources/README.md`（binaries 段） |
| 1.6 | S12 | `sources/Dockerfile:97-192`、`:107-113`、`:185-187`、`:137-148`、`:127-129`、`:142-144` |
| 1.7 | S2, S34 | `sources/docs_docker.md`（user: 段原文）；discussion #1289（无本地副本，按 ID 回溯 github.com） |
| 1.8 | S2, S16, S12 | `sources/docs_docker.md`；`.github/workflows/ci.yml`（jsDelivr `@master`）；`sources/Dockerfile:63`、`:76` |
| 1.9 | S9, S4 | `sources/docs_system_requirements.md`；`sources/docs_known_issues.md` |
| 1.10 | S12, S3 | `sources/Dockerfile:63`；`sources/docs_config.md` |
| 1.11 | S8 | `sources/docs_migrations.md` |
| 1.12 | S17, S18, S19, S14 | `releases/tag/0.25.0`、`releases/tag/0.26.0`、`releases.atom`（无本地副本）；`sources/Options.cs:354-368` |
| 1.13 | S31, S32, S33 | `hotio/unraid-templates@master/hotio/slskd.xml`；`hotio.dev/containers/slskd`；truenas/documentation PR #4253 + apps 目录元数据（均无本地副本） |
| 1.14 | §七 1–5、§八 O6/O7/O8；§六 M2/M3/M4（仅指路） | 见 `02_deep_research.md` §七 / §八 / §六 |

### 示例清单

| 编号 | 示例 | 类型 | 一句话说明 |
| --- | --- | --- | --- |
| EX-01 | `docker-compose.yml`：官方推荐最小可用 | yaml | 官方镜像 + `user:` + `/app` 挂载 + 三条端口映射 |
| EX-02 | `docker-compose.yml`：`PUID`/`PGID` 变体 | yaml | 与 EX-01 并列展示的另一种身份写法，标注「二选一」 |
| EX-03 | `docker-compose.yml`：环境变量补充版 | yaml | 监听端口、umask、volatile 三个环境变量的写法 |
| EX-04 | `docker run` 等价命令 | bash | 与 EX-01 等价的单行命令形态 |
| EX-05 | 二进制启动命令 | bash | 非容器路径的最小启动方式 |
| EX-06 | **全文唯一一份完整 `slskd.yml` 综合样例** | yaml | 后续所有 slskd.yml 片段都从它截取，禁止另起变体 |
| EX-07 | `slskd.yml`：volatile 模式片段 | yaml | 取自 EX-06 对应段落 |
| EX-08 | 升级前旧键检查命令 | bash | 扫出四个会直接导致启动失败的旧键 |
| EX-09 | 迁移回滚操作序列 | bash | 定位首次失败的 migration id → 改名 → 移回数据目录 → 重启 |
| EX-10 | 端口可达性自测序列 | bash | 本机 `/health` + 外部 50300 TCP 触达；由 `Dockerfile` HEALTHCHECK 推导，非信源原文，须标注 |
| EX-33 | 官方启动失败提示原文（引用块，三条） | 引用 | 非代码块，直接引用 `Options.cs` 内的提示字符串 |

### 本章常见坑

以**指向条目**形式写，不转述结论；写作时回 `02_deep_research.md` 对应条目 + 信源原文件逐条比对。

| 坑 | 出处 |
| --- | --- |
| 三种身份模式混用 | §七-1 + S12:107-113 |
| 没挂 `/app` | §七-2 + S12:127-129、`:142-144` |
| 权限不一致（root 属主 / umask） | §七-3 + S12:185-187 |
| 端口映射漏项 | §七-4 + S14:1770、`:2019`、`:2319` |
| 升级前未跑旧键检查 | §七-5 + S14:354-368、S17、S18 |
| 用 CoW / 网络文件系统放应用数据 | §七-6 + S4、S9 |
| 把 `user: 568:568` 写成原始资料 | §八 O6 + S33 |
| 写入 binhex Unraid 模板细节 | §八 O7 |
| 写群晖部署 | §八 O8 |
| NAS 平台可信度标注缺失 | §5.1.8 + S31 / S32 / S33 |
| **键名以 `Options.cs` + `example.yml` 为准；本分册涉及的三处官方文档错误见第 3 章 §3.10**（本章只在 EX-06 附近挂一行指路） | §六 M2 / M3 / M4 + §九 强制约束 2 |

### 预估篇幅

约 **12,000 汉字**。

- 1.1 端口语义 ~800（核心概念，配大白话 callout + 类比）
- 1.2–1.5 四类产物 ~3,400（每类产物一个顶级小节，字段收进 `####`）
- 1.6–1.8 身份 / 官方立场 / 镜像与健康检查 ~2,800
- 1.9–1.10 系统要求与首次启动 ~1,900
- 1.11–1.13 升级、破坏性变更、NAS ~2,600
- 1.14 本章常见坑 ~500

---

## 第 2 章 账号与共享机制

### 章节目标

讲清 Soulseek 账号从哪来（以及官方从未说明的部分）、共享要求的三层真实结构、客户端政策与入站连接的排错口径，最后给 Relay 的定位与配置骨架。

### 小节结构

```text
### 2.1 账号：官方口径与官方未说明的部分
    #### 官方站点无注册入口的证据
    #### 账号创建发生在哪一步：官方未说明（社区旁证单独标注为旁证）
    #### 用户名回收规则与捐款永不过期
    #### 密码无法找回
    #### 访问权可撤销 / 滥用后果（客观引述，不作劝诫）
    #### [!tip] 大白话 + 类比（Soulseek 账号更像"网络会员号"，不是网站注册账号）
### 2.2 共享要求：必须分三层写
    #### 第一层 —— 服务器规则层面
    #### 第二层 —— 对端客户端里用户自设的阈值（社区，须明确标注）
    #### 第三层 —— slskd 内置 leechers 组的限速
    #### 官方对"客户端内置 autoban"的立场
    #### 三层如何互相作用（一张对照表）
    #### [!tip] 大白话 + 类比（商场不查消费 / 店主自己挑客 / 你的店给常客留位）
### 2.3 共享目录怎么配（操作面）
    #### 共享目录键与首次扫描
    #### 默认排除项
    #### 扫描慢与第 1 章 HEALTHCHECK 宽限期的呼应
    #### 在哪看共享状态（Web UI System → Shares，详见证第 3 章 §3.3）
### 2.4 入站连接与端口自检
    #### 监听端口语义（回指 §1.1 的 50300，不复述 5030/5031）
    #### issue #1429：已定性的环境问题
    #### issue #1805：未定性的疑难（状态仍 OPEN）
    #### 两者的正确表述方式：两种状态，不是两个相反结论
    #### 自检方法与判定顺序
    #### 协议混淆端口（仅见于发布说明，FAQ 未收录）
### 2.5 客户端政策（客观技术说明）
    #### 同一 IP 的连接数上限 → 对 Relay / 双客户端场景的影响
    #### bot / 自动化客户端 / 残缺脚本
    #### 第三方客户端"被容忍"的条件
    #### 写作口径声明：只作技术说明，不作合规判断
### 2.6 Relay 中继模式
    #### 定位：Controller / Agent 各做什么
    #### 适用场景清单
    #### 安全设计：Agent 主动外连、API key + 每 Agent secret、按 IP/CIDR 限定
    #### Controller 侧配置
    #### Agent 侧配置
    #### instance_name 必须与 Controller 上的 agent 名一致
    #### secret 生成命令与长度约束
### 2.7 本章常见坑
```

### 素材映射

| 小节 | 信源 ID | 本地路径 / 锚点 |
| --- | --- | --- |
| 2.1 | S20, S24, S21, S23, S26 | slsknet.org node/681、faq-page、node/748、node/1159（均无本地副本，按 ID 回溯）；`SLSKPROTOCOL.md`（nicotine-plus 仓库，T3，须标注社区逆向） |
| 2.2 | S20, S22, S24, S14, S11 | slsknet.org node/681、node/523、faq-page；`sources/Options.cs`（`transfers.groups` / `thresholds`）；`sources/config_slskd.example.yml` |
| 2.3 | S3, S11, S14, S12 | `sources/docs_config.md`；`sources/config_slskd.example.yml`；`sources/Options.cs`；`sources/Dockerfile:63` |
| 2.4 | S24, S25, S28, S29, S14 | slsknet.org faq-page、node/263、node/551；issue #1429、#1805；`sources/Options.cs:1770` |
| 2.5 | S20, S26 | slsknet.org node/681（无本地副本）；`SLSKPROTOCOL.md`（T3） |
| 2.6 | S7, S3, S11, S14 | `sources/docs_relay.md`；`sources/docs_config.md`；`sources/config_slskd.example.yml`；`sources/Options.cs` |
| 2.7 | §七-10、§八 O7、§三 C5、§四 2–3、§六 M9 | 见 `02_deep_research.md` 对应条目 |

### 示例清单

| 编号 | 示例 | 类型 | 一句话说明 |
| --- | --- | --- | --- |
| EX-11 | `slskd.yml`：共享目录与排除项片段 | yaml | 取自 EX-06 对应段落，不新增键 |
| EX-12 | `slskd.yml`：leechers 组阈值片段 | yaml | 取自 EX-06 对应段落 |
| EX-13 | `slskd.yml`：Relay Controller 侧片段 | yaml | relay 开关 / 模式 / agents 下的 secret 与 cidr + 一个 readwrite 角色的 API key |
| EX-14 | `slskd.yml`：Relay Agent 侧片段 | yaml | 回连地址 / api_key / secret / downloads |
| EX-15 | `--generate-secret` 命令 | bash | 生成 Relay secret，含长度约束说明 |
| EX-16 | Relay 场景的 compose 端口差异 | yaml | 展示 Agent 侧无需开放入站端口 |
| EX-10b | 50300 入站可达性自测序列 | bash | 与 EX-10 同源，此处只保留 50300 部分，写作时合并为 EX-10 一节，不新起编号 |
| EX-34 | 官方规则页原文（引用块） | 引用 | 同 IP 连接数上限、自动化客户端两条 |
| EX-35 | node/523 官方原文（引用块） | 引用 | 关于客户端内置 autoban 的立场 |

### 本章常见坑

| 坑 | 出处 |
| --- | --- |
| 把社区 autoban 阈值写成官方规则 | §九 强制约束 5 + §四-3 + S20 / S22 |
| 把「必须先用官方客户端注册」写成官方要求 | §九 强制约束 4 + §四-2 + §六 M9 |
| 把 #1429 与 #1805 写成「两个结论相反」 | §九 强制约束 3 + §三 C5 + S28 / S29 |
| 引用已被劫持的 `soulseekqt.net` 域名 | §三 C8；**全文一律改用 `slsknet.org` 对应 node** |
| Agent 的 `instance_name` 与 Controller 上的 agent 名不一致 | §七-10 + S7 |
| 把 Relay 当 VPN 用 / 以为 Relay 改变流量归属 | §九 强制约束 8 + S7（只作技术说明） |
| 同 IP 连接数上限与「同时跑官方客户端 + slskd」冲突未提示 | S20 + §5.2.3 |
| 协议混淆端口当成官方 FAQ 条目写 | §四-7 + S25（仅发布说明，FAQ 未收录） |
| 把 P2P / 版权 / VPN 合规写成劝诫或法务判断 | §九 强制约束 8 |

### 预估篇幅

约 **9,000 汉字**。

- 2.1 账号 ~2,000（官方口径与「官方未说明」的边界要写足）
- 2.2 共享三层 ~2,400（全篇最容易被写错的一节，必须给对照表）
- 2.3 共享目录操作面 ~700
- 2.4 入站连接与端口自检 ~1,700
- 2.5 客户端政策 ~800
- 2.6 Relay ~1,000（压缩：定位 + 两段配置骨架）
- 2.7 本章常见坑 ~400

---

## 第 3 章 日常使用与配置详解

### 章节目标

让读者能用 Web UI 走完搜索 → 筛选 → 下载 → 队列 → 上传的全流程，并真正理解配置源优先级、列表合并陷阱、顶层键与用户组、目录/过滤/黑名单。

### 小节结构

```text
### 3.0 开篇声明：官方无 Web UI 操作文档
    #### 官方文档目录实际包含哪些文件
    #### 本章功能面的取证方式与可信度标注
### 3.1 搜索与结果筛选（核心工作流）
    #### 发起搜索与结果卡片读法
    #### 排序：只有两项及各自方向
    #### 三个开关与各自默认值
    #### 筛选语法全表（含别名与语义）
    #### Attributes 列的渲染规则
    #### 两处已知边界行为（标注"源码可读，实际效果需自测"）
    #### [!tip] 大白话 + 类比（筛选语法 = 电商筛选器，但只认英文缩写）
### 3.2 下载、上传与队列管理
    #### Downloads / Uploads 视图与批量操作分组
    #### 传输表列与单文件操作（重试 / 插队）
    #### 目录内补全文件的入口
    #### 分页行为
    #### 断点续传相关键
    #### [!tip] 大白话 + 类比（队列 = 医院挂号；插队 = 加号；免费槽位 = 有没有空诊室）
### 3.3 其余视图速览
    #### Dashboard：区间与数据块
    #### Browse：目录树与本地缓存
    #### Users / Rooms / Chat
    #### System 的七个页签（本章多个自查入口都落在这里）
    #### 主题切换
    #### Agent 模式下导航被替换
### 3.4 配置文件：slskd.yml
    #### 配置源优先级五层
    #### 环境变量前缀与列表分隔符
    #### CLI 的列表写法
    #### 应用目录与默认配置文件位置
    #### 热重载、RequiresRestart、RequiresReconnect
    #### Run-Time Overlay：只支持两项，且重启即丢
    #### 不能在 YAML 里设置的键
### 3.5 列表合并陷阱（单列一节）
    #### 追加 + 覆盖的真实语义
    #### 受影响的选项清单
    #### 规避做法
    #### [!tip] 大白话 + 类比（两个购物车往一个袋子里塞，最后一格被整格覆盖）
### 3.6 顶层键总览
    #### 21 个有效顶层键
    #### 4 个哨兵键：写入即启动失败
    #### 与 example.yml 的交叉验证
### 3.7 用户组与优先级（transfers.groups）
    #### 四类内置组各自的定义与来源
    #### 自定义组
    #### priority 的语义方向
    #### 队列策略的两种取值
    #### 组级 slots / speed_limit 与全局限制的关系
    #### [!tip] 大白话 + 类比（优先级 = 安检通道等级；数字小 = 排前面）
### 3.8 常用配置键与默认值
    #### 按域分组的默认值总表（代码真值 / 文档写法对照）
    #### 文档与代码不一致处逐条标注
    #### 未裁决项：内置组 priority（只讲语义，不给数字）
### 3.9 目录、过滤与黑名单
    #### 两个默认目录与自动创建
    #### 默认排除正则
    #### 黑名单开关与托管黑名单文件（含"文件异常会导致应用退出"）
    #### 搜索请求过滤
### 3.10 本章常见坑（M1–M9 全部落点 + §七 7–9 + §八 O1/O4/O9/O10）
```

### 素材映射

| 小节 | 信源 ID | 本地路径 / 锚点 |
| --- | --- | --- |
| 3.0 | S10, S15 | `sources/docs_README.md`；前端源码（jsDelivr `@master/src/web/src/**`，无本地副本） |
| 3.1 | S15, S14 | `src/web/src/components/App.jsx`、`SearchDetail.jsx`、`lib/searches.js`（jsDelivr `@master`）；`sources/Options.cs`（检索相关选项） |
| 3.2 | S15, S14 | 前端源码 `src/web/src/**`（jsDelivr）；`sources/Options.cs`（`transfers.download.retry.*`） |
| 3.3 | S15 | 前端源码（jsDelivr `@master/src/web/src/**`） |
| 3.4 | S3, S14, S11 | `sources/docs_config.md`（配置优先级段）；`sources/Options.cs`（`[JsonIgnore][YamlIgnore]` 处）；`sources/config_slskd.example.yml` |
| 3.5 | S3 | `sources/docs_config.md`（列表合并说明段） |
| 3.6 | S14, S11, S3 | `sources/Options.cs:257-258`、`:354-368`；`sources/config_slskd.example.yml`（顶层键清单）；`sources/docs_config.md:526`、`:466` |
| 3.7 | S14, S11, S3 | `sources/Options.cs`（`transfers.groups.*` 与 `thresholds`）；`sources/config_slskd.example.yml:83`；`sources/docs_config.md:466`、`:526` |
| 3.8 | S14, S11, S3 | `sources/Options.cs`（逐键默认值）；`sources/config_slskd.example.yml`；`sources/docs_config.md` |
| 3.9 | S3, S14, S11 | `sources/docs_config.md`；`sources/Options.cs`（`directories.*` / `shares.filters` / `blacklist.*` / `filters.search.request`）；`sources/config_slskd.example.yml` |
| 3.10 | §六 M1–M9、§七 7–9、§八 O1/O4/O9/O10 | 见 `02_deep_research.md` 对应条目 |

### 示例清单

| 编号 | 示例 | 类型 | 一句话说明 |
| --- | --- | --- | --- |
| EX-06 | 完整 `slskd.yml` 综合样例（**定义在第 1 章**） | yaml | 本章只截取片段，不再定义新样例 |
| EX-17 | `slskd.yml`：黑名单片段 + CIDR 清单文件 | yaml | 清单文件的具体格式须回 S3 复核后再落笔，未取证前不写死 |
| EX-18 | 默认值对照表（键 / 代码默认 / 文档写法） | 表格 | 不是代码块；不一致项加粗标注 |
| EX-19 | 搜索筛选语法速查表 + 组合示例 | 表格 + 文本 | 组合示例由语法表拼接，须标注「非信源原文」 |
| EX-20 | 环境变量写法集 | bash | 本分册涉及的全部 `SLSKD_*` 变量集中一处 |
| EX-21 | 列表合并对比例 | bash + yaml | 同一选项两种源的输入与最终结果 |
| EX-36 | 用户组配置片段（内置 + 自定义 + priority/slots/speed_limit） | yaml | 取自 EX-06 对应段落，不新增键 |
| EX-37 | 配置热重载日志示例 | text | 展示热重载与「需重启才生效」标志在日志里的样子；须回源确认日志原文后再写 |
| EX-22 | 顶层键清单（21 有效 + 4 哨兵） | 表格 | 与 example.yml 做交叉验证的一栏 |

### 本章常见坑

| 坑 | 出处 |
| --- | --- |
| M2：logger 磁盘日志键名（文档 YAML 块与 example.yml / Options.cs 不一致） | §六 M2 + S14:1461-1465、S11:198、S3 |
| M3：`integration` 与 `integrations` 单复数（文档自身不一致；单数是哨兵，写入即启动失败） | §六 M3 + S14:331-338 |
| M4：顶层 `groups` 的位置（文档把 `transfers.groups` 写成顶层；顶层是哨兵，写入即启动失败） | §六 M4 + S3:526、S14:257-258、S11:83 |
| M6：`retention.logs` 文档值与代码值不同 | §六 M6 + S14 |
| M7：`transfers.upload.slots` 文档值与代码值不同 | §六 M7 + S14 |
| 默认值被误当成文档示例值（`shares.cache.workers` / `retention.search` / `transfers.download.slots`） | §5.3.3 表内「文档写法」列 |
| 列表型选项跨源混设 | §七-7 + S3 |
| `app_dir` / `config` 试图写在 YAML 里 | §5.3.2 + S14 |
| Run-Time Overlay 被当成通用覆盖手段 | §5.3.2 + S14 |
| 内置组 priority 被写成具体数字 | §八 O1（只讲语义方向 + privileged 固定值） |
| `diagnostic_level` 被宣称大小写规则 | §八 O4 |
| Web UI 筛选两处边界行为被写成确定结论 | §八 O9（标注「源码可读，需自测」） |
| MCP / 第三方生态被写成成熟方案 | §八 O10（保持打折口径） |
| 把 M1 单向取信（`remote_configuration` 的两种口径） | §六 M1；**本章只指路，并列呈现落点在 [[04 安全与进阶速览#4.1]]** |

### 预估篇幅

约 **13,500 汉字**。

- 3.0 开篇声明 ~400
- 3.1 搜索与筛选 ~3,000（全篇操作密度最高的一节）
- 3.2 下载上传队列 ~2,000
- 3.3 其余视图 ~1,600
- 3.4 配置文件与配置源 ~2,200
- 3.5 列表合并陷阱 ~1,100
- 3.6 顶层键总览 ~900
- 3.7 用户组与优先级 ~1,400
- 3.8 默认值总表 ~1,300（以表格为主，正文从简）
- 3.9 目录/过滤/黑名单 ~900
- 3.10 本章常见坑 ~700

---

## 第 4 章 安全与进阶速览（压缩）

### 章节目标

让读者在把 slskd 暴露到公网之前知道必须改什么，理解反代与 VPN 集成的官方口径边界，并知道每个进阶集成各自的安全代价；每一项只到「够用 + 知道去哪查」的深度。

### 小节结构

```text
### 4.1 默认凭据与远程配置（M1 并列呈现的唯一落点）
    #### 默认凭据与公网暴露风险
    #### remote_configuration 的默认值与官方警告
    #### 两种口径并列：快速上手语境 vs 公网部署语境
    #### remote_file_management 的默认粒度（列目录 vs 删除）
    #### [!tip] 大白话 + 类比（默认密码 + 开远程配置 = 把钥匙挂在门上还留了配方）
### 4.2 认证机制细节
    #### JWT 与 API Key 的过期语义
    #### 默认 JWT key 每次启动随机生成 → 重启使已签发 JWT 失效
    #### 不支持转发类请求头 → 反代后按 CIDR 过滤可能失效
### 4.3 API Key CIDR 绕过缺陷
    #### 受影响版本区间
    #### 根因（前缀被解析成匹配一切）
    #### 两处修复分别落在哪个版本
    #### 对 Relay + CIDR 白名单用户的安全底线
### 4.4 反向代理要点
    #### websocket 必需的请求头与缓冲设置
    #### 子目录部署的前缀设置
    #### 官方四套配置的指路
### 4.5 VPN 集成（官方口径必须写准）
    #### 官方原文：配置集成不改变流量路由
    #### 它实际提供什么
    #### 轮询机制
    #### gluetun 侧需要开什么
    #### slskd 侧配置项
    #### 实际路由由用户自行确保
### 4.6 脚本集成的 RCE 风险
    #### 官方原文
    #### 正确用法与禁止用法对照
### 4.7 其他集成与特性速览
    #### integrations 下的五个子项
    #### webhook 的事件与重试设置
    #### metrics：默认关闭、默认凭据、暴露的信息
    #### swagger 与「哪些选项支持 Run-Time Overlay」的权威入口
    #### 搜索侧限流：官方标注的风险等级
    #### MCP / 第三方生态（打折口径）
### 4.8 公网部署最小动作清单
### 4.9 本章常见坑
```

### 素材映射

| 小节 | 信源 ID | 本地路径 / 锚点 |
| --- | --- | --- |
| 4.1 | S3, S14, S1 | `sources/docs_config.md:95`；`sources/Options.cs:185`；`sources/README.md`（Quick Start 段） |
| 4.2 | S3 | `sources/docs_config.md`（认证段） |
| 4.3 | S30, S19 | issue #1605 + PR #1606 + PR #1714（无本地副本，按 ID 回溯）；`releases.atom` |
| 4.4 | S6 | `sources/docs_reverse_proxy.md` |
| 4.5 | S5, S3 | `sources/docs_vpn.md`；`sources/docs_config.md`（`integrations.vpn.*`） |
| 4.6 | S3 | `sources/docs_config.md`（Scripts 段） |
| 4.7 | S3, S14, S15 | `sources/docs_config.md`（integrations / metrics / feature / throttling 段）；`sources/Options.cs`；前端源码中的 System → Options（jsDelivr） |
| 4.8 | §七-9 | 见 `02_deep_research.md` §七 |
| 4.9 | §六 M1、§八 O10、§九 强制约束 6/8 | 见 `02_deep_research.md` 对应条目 |

### 示例清单

| 编号 | 示例 | 类型 | 一句话说明 |
| --- | --- | --- | --- |
| EX-23 | NGINX 反向代理片段（子目录部署） | nginx | websocket 头 + 缓冲关闭 + 前缀设置 |
| EX-24 | NGINX 反向代理片段（根路径 / SWAG） | nginx | 与 EX-23 并列，标注两种部署形态的差异 |
| EX-25 | Apache 片段 | apache | websocket 升级写法 |
| EX-26 | IIS `web.config` | xml | URL Rewrite 配置 |
| EX-27 | gluetun 侧控制服务器 compose 片段 | yaml | 开启控制服务器与鉴权角色变量 |
| EX-28 | slskd + gluetun 共享网络命名空间 compose + `integrations.vpn.*` | yaml | 展示「实际路由靠共享网络命名空间保证」，配置项本身不改变路由 |
| EX-29 | 脚本集成环境变量正确 / 错误用法对照 | bash | 读环境变量 vs 命令替换 / 直接传参 |
| EX-30 | `slskd.yml`：metrics 启用片段 | yaml | 取自 EX-06 对应段落 |
| EX-31 | `slskd.yml`：swagger 启用片段 | yaml | 取自 EX-06 对应段落 |
| EX-32 | 公网部署最小动作清单 | 复选框列表 | 每项一句话，附指向详情节的 wikilink |
| EX-37b | 采集的官方原文引用块（VPN 路由 / RCE 风险） | 引用 | 非代码块；写作时回 `sources/docs_vpn.md`、`sources/docs_config.md` 逐字比对 |

### 本章常见坑

| 坑 | 出处 |
| --- | --- |
| 以为「配置了 VPN 集成，流量就会走 VPN」 | §九 强制约束 6 + S5（官方原文） |
| metrics 默认凭据直接用、或公网保持开启 | S3 + §5.4.7 |
| 反代之后仍指望按 CIDR 白名单过滤 | S3 + §5.4.2 |
| 自定义 JWT key 泄露后可伪造 JWT | S3 + §5.4.2 |
| 脚本集成里做命令替换 / 直接传参 | S3 + §5.4.6 |
| 在低于 0.26.0 的版本上用 Relay + CIDR 白名单 | S30 + §5.4.3 |
| M1 被单向取信（两种口径只留一种） | §六 M1（本处为并列呈现的唯一落点） |
| MCP / 第三方生态被写成成熟方案 | §八 O10 |
| 把 P2P / 版权 / VPN 合规写成劝诫或法务判断 | §九 强制约束 8 |

### 预估篇幅

约 **7,000 汉字**（本章整体压缩）。

- 4.1 默认凭据与远程配置 ~1,100
- 4.2 认证细节 ~900
- 4.3 CIDR 绕过缺陷 ~900
- 4.4 反向代理 ~1,100（以配置片段为主，正文从简）
- 4.5 VPN 集成 ~1,300
- 4.6 脚本 RCE ~600
- 4.7 其他集成速览 ~900
- 4.8–4.9 清单与常见坑 ~600

---

## 全文示例总清单

写作时**只认这份清单里的编号**。已在别处出现过的示例，只允许 wikilink 指路，不允许换个写法再写一遍。

### 编写约定

1. 所有代码块**必须带语言标识**：`yaml` / `bash` / `nginx` / `apache` / `xml` / `text`。
2. 所有**文件型代码块**首行必须是文件路径注释头，例如
   `# 文件：docker-compose.yml` 或 `# 文件：slskd.yml`；
   `docker-compose.yml` 用 `#`，YAML 用 `#`，IIS 用 `<!-- 文件：web.config -->` 形式的等效注释。
3. **EX-06 是全文唯一一份完整 `slskd.yml`**。所有其他 `slskd.yml` 片段（EX-07 / EX-11 / EX-12 / EX-13 / EX-14 / EX-17 / EX-30 / EX-31 / EX-36）都必须标注「取自 EX-06 对应段落」，且不得出现 EX-06 里没有的键。
4. 引用块（官方原文）不算代码块，不写语言标识，但必须逐字回源比对。

### 编号总表

| 编号 | 示例 | 归属章节 | 说明 |
| --- | --- | --- | --- |
| EX-01 | compose：官方推荐最小可用 | 1.2 | `user:` + `:latest` + `/app` + 三端口 |
| EX-02 | compose：PUID/PGID 变体 | 1.2 | 与 EX-01 二选一 |
| EX-03 | compose：环境变量补充版 | 1.2 | 监听端口 / umask / volatile |
| EX-04 | `docker run` 等价命令 | 1.4 | 命令形态 |
| EX-05 | 二进制启动命令 | 1.5 | 非容器路径 |
| EX-06 | **完整 `slskd.yml` 综合样例（唯一真源）** | 1.3 | 后续所有片段从它截取 |
| EX-07 | `slskd.yml`：volatile 片段 | 1.3 | 取自 EX-06 |
| EX-08 | 升级前旧键检查命令 | 1.11 | 扫四个哨兵键 |
| EX-09 | 迁移回滚操作序列 | 1.11 | 三步 |
| EX-10 | 端口可达性自测序列 | 1.10 | 含 5030 `/health` 与 50300 TCP；**由 Dockerfile HEALTHCHECK 推导，须在正文标注非信源原文** |
| EX-11 | `slskd.yml`：共享目录与排除项 | 2.3 | 取自 EX-06 |
| EX-12 | `slskd.yml`：leechers 阈值 | 2.3 | 取自 EX-06 |
| EX-13 | `slskd.yml`：Relay Controller | 2.6 | 含 API key 角色 |
| EX-14 | `slskd.yml`：Relay Agent | 2.6 | 回连配置 |
| EX-15 | `--generate-secret` 命令 | 2.6 | 含长度约束 |
| EX-16 | Relay 场景 compose 端口差异 | 2.6 | Agent 侧不入站 |
| EX-17 | `slskd.yml`：黑名单 + CIDR 清单文件 | 3.9 | 清单文件格式须回 S3 复核后再定 |
| EX-18 | 默认值对照表 | 3.8 | 表格 |
| EX-19 | 搜索筛选语法速查表 + 组合示例 | 3.1 | 组合示例标注非原文 |
| EX-20 | 环境变量写法集 | 3.4 | 全部分册涉及的 `SLSKD_*` 集中一处 |
| EX-21 | 列表合并对比例 | 3.5 | 输入 → 结果 |
| EX-22 | 顶层键清单（21 + 4） | 3.6 | 表格，含 cross-check 栏 |
| EX-23 | NGINX：子目录部署 | 4.4 | websocket + 前缀 |
| EX-24 | NGINX：根路径 / SWAG | 4.4 | 与 EX-23 并列 |
| EX-25 | Apache | 4.4 | websocket 升级 |
| EX-26 | IIS `web.config` | 4.4 | URL Rewrite |
| EX-27 | gluetun 控制服务器 compose | 4.5 | 鉴权角色变量 |
| EX-28 | slskd + gluetun 共享网络命名空间 | 4.5 | 含 `integrations.vpn.*` |
| EX-29 | 脚本集成用法对照（正确 / 错误） | 4.6 | 读环境变量 vs 命令替换 |
| EX-30 | `slskd.yml`：metrics 启用 | 4.7 | 取自 EX-06 |
| EX-31 | `slskd.yml`：swagger 启用 | 4.7 | 取自 EX-06 |
| EX-32 | 公网部署最小动作清单 | 4.8 | 复选框列表 |
| EX-33 | 官方启动失败提示原文（三条） | 1.12 | 引用块 |
| EX-34 | 官方规则页原文（引用块） | 2.5 | 逐字回源 |
| EX-35 | node/523 官方原文（引用块） | 2.2 | 逐字回源 |
| EX-36 | `slskd.yml`：用户组配置 | 3.7 | 取自 EX-06 |
| EX-37 | 配置热重载日志示例 | 3.4 | 须回源确认日志原文后再写 |
| EX-37b | VPN 路由 / RCE 官方原文（引用块） | 4.5、4.6 | 逐字回源 |

> 说明：EX-10b（50300 单端口自测）与 EX-10 合并，不单列编号，见第 2 章 §2.4 的说明。

---

## 覆盖核对

### A. §九 建议章节骨干覆盖

| `02_deep_research.md` §九 骨干 | 落点 | 状态 |
| --- | --- | --- |
| §5.1.1 端口 | 1.1 | ✅ |
| §5.1.2 三种身份 | 1.6 | ✅ |
| §5.1.3 官方推荐 | 1.7 | ✅ |
| §5.1.4 镜像 / 健康检查 | 1.8 | ✅ |
| §5.1.5 系统要求与不兼容 | 1.9 | ✅ |
| §5.1.6 升级迁移 | 1.11 | ✅ |
| §5.1.7 破坏性变更 | 1.12 | ✅ |
| §5.1.8 NAS | 1.13 | ✅ |
| §5.2.1 账号 | 2.1 | ✅ |
| §5.2.2 共享（三层分开） | 2.2 | ✅ |
| §5.2.3 客户端政策 | 2.5 | ✅ |
| §5.2.4 入站与混淆端口 | 2.4 | ✅ |
| §5.2.5 Relay | 2.6 | ✅ |
| §5.3.1 Web UI（开篇声明无官方操作文档） | 3.0 + 3.1 + 3.2 + 3.3 | ✅ |
| §5.3.2 配置源与合并陷阱 | 3.4 + 3.5 | ✅ |
| §5.3.3 顶层键与分组 | 3.6 + 3.7 + 3.8 | ✅ |
| §5.3.4 目录 / 过滤 / 黑名单 | 3.9 + EX-11 + EX-17 | ✅ |
| §5.4.1–§5.4.7 安全与进阶（压缩） | 4.1–4.7 | ✅ |
| 各章末「常见坑」（素材取 §七 与 ⚠️ 标注） | 1.14 / 2.7 / 3.10 / 4.9 | ✅ |

### B. 8 项强制约束的章节归属

| # | 强制约束 | 主责章节 | 交叉落点 |
| --- | --- | --- | --- |
| 1 | 端口三线区分（5030/5031 = Web UI，50300 = Soulseek 入站，2271 = Soulseek 服务器） | **1.1** | 1.2（compose 逐行）、1.10（自测）、2.4（入站语义）、4.4（反代只代理 Web UI） |
| 2 | 键名以 `Options.cs` + `example.yml` 为准；M2/M3/M4 三处官方文档错误须在「本章常见坑」显式点出 | **3.10** | 1.14 挂一行指路；EX-06 首行注释声明「以代码 + example.yml 为准」 |
| 3 | #1429 / #1805 按 §三 C5 修正口径写，不得写成「两个结论相反」 | **2.4** | 1.1 / 1.14 提到入站可达性时指路，不复述 |
| 4 | 账号创建：官方无注册入口（已证）；「必须先用 SoulseekQt 注册」是社区推断，不得写成官方要求 | **2.1** | 2.7 常见坑 |
| 5 | 共享要求分三层（服务器规则 / 对端用户自设 autoban / slskd 内置 leechers 组），不得把社区 autoban 阈值写成官方规则 | **2.2** | 3.7（`leechers` 组配置）、2.7 常见坑 |
| 6 | VPN 一节必须写明「配置 VPN 集成不改变流量路由」 | **4.5** | 3.8（`integrations.vpn.*` 默认值处指路）、4.9 常见坑 |
| 7 | 禁止引用 `soulseekqt.net`（已被劫持），一律用 `slsknet.org` | **全文约束**，落点：2.1 / 2.4 素材映射处显式标注 | 「全文示例总清单 → 编写约定」另加一条：引用块回源时如遇该域名，一律替换为 `slsknet.org` 对应 node |
| 8 | Soulseek P2P / 版权 / VPN 合规只作客观技术说明，不作劝诫、不作法务判断 | **2.5** | 4.5、4.9 |

### C. §六 矛盾与 §八 开放问题的落点

| 条目 | 处理方式 | 落点 |
| --- | --- | --- |
| M1 `remote_configuration` 推荐值 | **并列呈现**（唯一一处平行口径必须并列的条目，不得单向取信） | 4.1；3.8 只指路 |
| M2 `logger` 磁盘日志键名 | 按代码 + example.yml 写，常见坑点明文档有误 | 3.10；EX-06 注释 |
| M3 `integrations` 单复数 | 按复数写，注明单数是哨兵 | 3.10；3.6 哨兵清单 |
| M4 顶层 `groups` 位置 | 按 `transfers.groups` 写，注明顶层是哨兵 | 3.10；3.6、3.7 |
| M5 内置组 priority | **未裁决** → 只讲语义方向与 privileged 固定值，不给数字 | 3.7；3.8 |
| M6 `retention.logs` 默认 | 按代码写，注明文档写的是示例值 | 3.8；3.10 |
| M7 `transfers.upload.slots` 默认 | 按代码写 | 3.8；3.10 |
| M8 #1429 vs #1805 | 按 §三 C5 修正口径 | 2.4 |
| M9 账号创建方式 | 按 §四-2 口径 | 2.1 |
| O1 内置组 priority 具体数字 | 不给数字 | 3.7 |
| O2 `permissions` 的 env / CLI 形态 | 只写「顶层 permissions 已迁移，旧写法启动失败」，env / CLI 形态不展开 | 1.12 |
| O3 `flags.no_sqlite_pooling` | **不写入正文** | — |
| O4 `diagnostic_level` 大小写 | 按示例写，不宣称大小写规则 | 3.8 |
| O5 YAML 键名下划线约定 | 不影响正文，仅方法学备注 | — |
| O6 `user: 568:568` 原始出处 | 若写入，必须标「组合推断」，不得标为原始资料 | 1.13 |
| O7 binhex Unraid 模板 | 不写，或标「未核实」 | 1.13 |
| O8 群晖部署 | **不写** | 1.13（只写一句「无一手资料」） |
| O9 Web UI 筛选两处边界行为 | 作为「进阶技巧 + 已知怪癖」写，标注需自测 | 3.1 |
| O10 MCP / 第三方生态 | 保持打折口径 | 4.7 |

### D. 篇幅合计

| 部分 | 汉字 |
| --- | --- |
| 分册 README 索引 | ~1,200 |
| 第 1 章 | ~12,000 |
| 第 2 章 | ~9,000 |
| 第 3 章 | ~13,500 |
| 第 4 章 | ~7,000 |
| **合计** | **~42,700** |

落在 3–5 万汉字的目标区间内。
