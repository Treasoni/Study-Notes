# 厚浪镜像（HLmirror）使用方法 - P2 深度素材

- **阶段**: P2（深度收集）
- **运行标识**: `houlang-mirror-usage`
- **选定方向**: 1 + 2（机制三分法 + 实操全链路），方向 3 降级为「常见坑」小节
- **精读时间**: 2026-09-13
- **本地全文缓存**: `workspace/houlang-mirror-usage/sources/`

> **引用规则**：本文件所有「原文」均为逐字引用，可在 `sources/` 对应文件中检索核对。凡标 `[推论]` 的为我的推理，笔记正文引用时必须同样标注。

---

## 一、来源表

| ID | 标题 | URL | 层级 | 本地缓存 |
| --- | --- | --- | --- | --- |
| S1 | 如何使用新版 HLmirror（官方教程） | https://home.houlang.cloud/archives/ru-he-shi-yong-xin-ban-hlmirror | 一手（厂商自述） | `04_home_houlang_cloud.md` |
| S1b | Mirror the Docker Hub library（Docker 官方） | https://docs.docker.com/docker-hub/image-library/mirror/ | 一手 | `01_docs_docker_com.md` |
| S1c | dockerd CLI 参考 | https://docs.docker.com/reference/cli/dockerd/ | 一手 | `02_docs_docker_com.md` |
| S5 | HLmirrors 产品页 | https://houlang.cloud/zh-CN/article/products/hlmirror | 一手 | `03_houlang_cloud.md` |
| S6 | 厚浪云系统状态页 | https://status.houlang.cloud/status/system | 一手 | `05_status_houlang_cloud.md` |
| S9 | containerd Registry Configuration (Hosts) | https://containerd.io/docs/1.7/hosts/ | 一手 | `06_containerd_io.md` |
| S10 | Kubernetes Images 概念页 | https://kubernetes.io/docs/concepts/containers/images/ | 一手 | `07_kubernetes_io.md` |
| S11 | DaoCloud 公开镜像加速 | https://docs.daocloud.io/community/mirror/ | 二手（同类厂商） | `01_docs_daocloud_io.md` |
| S12 | moby/moby Issue #42022 | https://github.com/moby/moby/issues/42022 | 一手（上游仓库） | `08_github_com.md` |
| S4 | mirror.houlang.cloud 前端 bundle | https://mirror.houlang.cloud/assets/index-BE1n8cWp.js | 一手（实现细节） | 未落盘（940KB，按需重取） |

**层级统计**：一手 8 / 二手 1。本轮**未采用任何社区来源**——方向 3 被降级后，CSDN / 什么值得买 / 掘金 / V2EX 四篇均未进入证据链。

---

## 二、Claim / Source 对照

### 2.1 registry-mirrors 的能力边界（本笔记的机制地基）

| # | 论断 | 来源 | 锚点 | 原文 |
| --- | --- | --- | --- | --- |
| C1 | **只有 Docker Hub 能被镜像**，其他私有 registry 不行 | S1b | "Alternatives" 段 | "It's currently not possible to mirror another private registry. Only the central Hub can be mirrored." |
| C2 | 镜像站仍受 Docker 公平使用政策约束 | S1b | 同上 | "Mirrors of Docker Hub are still subject to Docker's fair use policy." |
| C3 | pull-through cache 是"首次回源、后续本地命中，且带 tag 拉取时会回源校验" | S1b | "How does it work?" | "The first time you request an image from your local registry mirror, it pulls the image from the public Docker registry and stores it locally… When a pull is attempted with a tag, the Registry checks the remote to ensure if it has the latest version" |
| C4 | 配置点是 `daemon.json` 的 `registry-mirrors` 键或 `--registry-mirror` 启动参数 | S1b | "Configure the Docker daemon" | "Either pass the `--registry-mirror` option when starting `dockerd` manually, or edit `/etc/docker/daemon.json` … and add the `registry-mirrors` key and value" |
| C5 | dockerd 参考页对 `registry-mirrors` 只有一句描述，**没有**"仅 Docker Hub"的明文 | S1c | 配置项表格 | "`registry-mirrors` \| Specifies a list of registry mirrors." |

> C1 是 G1 缺口的填补答案，且是逐字官方原文。**这正是"厚浪不能填进 `daemon.json`"的根因**：填了也只能加速 Docker Hub，ghcr / quay / nvcr 一个都覆盖不到。

### 2.2 registry-mirrors 的凭据副作用

| # | 论断 | 来源 | 原文 |
| --- | --- | --- | --- |
| C6 | 配置 registry mirrors 后，**登录 Docker Hub 的凭据会被发送给镜像站** | S12 | "If dockerd has registry mirrors configured, when you log into Docker Hub the mirrors start receiving the credentials on image pulls. This is a security risk, as mirrors shouldn't have access to your Docker Hub tokens." |
| C7 | 副作用：某些镜像站拿着 Hub 凭据认证失败，导致所有请求返回 unauthorized | S12 | "GCR for example tries to authenticate with the Docker Hub credentials sent and fails, making all requests return an unauthorized error response." |
| C8 | 复现方式 | S12 | "Run dockerd with `--debug` and `--registry-mirror=https://mirror.gcr.io` … `docker pull docker` … The authorization header of the request contains the Docker Hub credential" |
| C9 | Issue 自 2021-02-13 起处于开启状态 | S12 | 页面元信息 "opened on Feb 13, 2021" |

> 这条是"为什么前缀重写式在凭据上更干净"的论据：**前缀重写不把镜像站注册成 Hub 镜像**，因此不存在"Hub 令牌被转发给第三方"这条路径。注意这是 `[推论]`，issue 本身没说这句话。

### 2.3 containerd / Kubernetes 侧的等价能力

| # | 论断 | 来源 | 原文 |
| --- | --- | --- | --- |
| C10 | containerd 的新写法是 `config_path` 指向 `hosts.toml` 目录；旧的 `registry.mirrors` 写法已废弃 | S9 | "The old CRI config pattern for specifying registry.mirrors and registry.configs has been **DEPRECATED**. You should now point your registry `config_path` to the path where your `hosts.toml` files are" |
| C11 | `hosts.toml` 里可用 `[host."…"]` 声明镜像源，并用 `capabilities` 区分能力 | S9 | `capabilities = ["pull"]  # Requires less trust, won't resolve tag to digest from this host` |
| C12 | 省略 `server = "…"` 可禁用上游 | S9 | `server = "https://registry-1.docker.io"    # Exclude this to not use upstream` |
| C13 | 不写 registry 主机名时，k8s 默认去 Docker 公共仓库，且该行为可配置 | S10 | "If you don't specify a registry hostname, Kubernetes assumes that you mean the [Docker public registry]… You can change this behavior by setting a default image registry" |
| C14 | k8s 官方**没有**"镜像前缀重写"这个 API | 缺口 G8 | 未找到一手出处，**不得写成 k8s 原生能力** |

> `[推论]` 这解释了为什么 k8s 场景下的加速手段分两派：改容器运行时配置（containerd `hosts.toml`），或在 manifest 里直接写全限定镜像地址（即用厚浪的前缀写法）。后者不需要改节点配置，是厚浪这类服务在 k8s 下的主要用法。

### 2.4 厚浪镜像的实际用法（方向 2 主体）

| # | 论断 | 来源 | 锚点 |
| --- | --- | --- | --- |
| C15 | 服务定位：把 Cloudflare 节点换成自有节点并加国内缓存 | S1 | "新版 HLmirror 将原有 Cloudflare 节点全部替换为了厚浪云自有节点，增加了国内缓存加速。" |
| C16 | 使用三步：访问站点注册登录 → 「访问令牌」选项卡新建令牌 → 复制登录命令到目标机器执行 | S1 | "首次使用" / "添加令牌" / "登录机器" 三节 |
| C17 | 成功标志是 `Login Succeeded` | S1 | "看到" _Login Succeeded_ "即代表登录成功" |
| C18 | 用法本质是**地址替换**，不是配置镜像源 | S1 | "将你原有的镜像地址替换为 HLmirror 即可高速拉取！" |
| C19 | 官方给出 **9** 个上游后缀 | S1 | 后缀表（见下） |
| C20 | 登录命令的形态 | S4（bundle，实现细节） | `docker login -u ${email} -p ${token} ${host}`；令牌前缀 `hlm_` |
| C21 | 存在"月度配额"与"下载限速"两个字段，但**公开页面无任何面向用户的数值承诺** | S4 / 缺口 G3 | `monthly_quota_bytes`、`download_rate_limit_bps`；后台配置项文案"启用下载限速" |
| C22 | 缓存按 tag 拉取时会先向上游校验 digest，上游不可用时可在一定时长内回退旧缓存 | S4（后台配置项提示文案，**会随版本变化**） | — |
| C23 | 产品页公布另一个服务 `all.hlmirror.com`（通用网页镜像，非 Docker 镜像） | S5 | "🔗 镜像地址：all.hlmirror.com" |
| C24 | 状态页含独立 HLmirror 分组 | S6 | "## HLmirror" 分组 |

**官方后缀表（S1 原文，逐字）**

| 上游 | 后缀代号 | 替换地址 |
| --- | --- | --- |
| Docker Hub | `dh` | `mirror.houlang.cloud/dh/` |
| Google Container Registry | `gcr` | `mirror.houlang.cloud/gcr/` |
| Github Container Registry | `ghcr` | `mirror.houlang.cloud/ghcr/` |
| NVDIA NGC | `nvcr` | `mirror.houlang.cloud/nvcr/` |
| Kubernetes Registry | `k8s` | `mirror.houlang.cloud/k8s/` |
| Microsoft Container Registry | `mcr` | `mirror.houlang.cloud/mcr/` |
| Elastic Docker Registry | `elastic` | `mirror.houlang.cloud/elastic/` |
| registry.gitlab.com | `gitlab` | `mirror.houlang.cloud/gitlab/` |
| Quay | `quay` | `mirror.houlang.cloud/quay/` |

**官方示例（S1 原文，逐字）**

```
原镜像地址：ghcr.io/immich-app/immich-server:v2.6.1
替换为 HLmirror：mirror.houlang.cloud/ghcr/immich-app/immich-server:v2.6.1
拉取命令示例：docker pull mirror.houlang.cloud/ghcr/immich-app/immich-server:v2.6.1

原镜像地址：library/nginx:latest
替换为 HLmirror：mirror.houlang.cloud/dh/library/nginx:latest
拉取命令示例：docker pull mirror.houlang.cloud/dh/library/nginx:latest
```

**上游 URL 映射（S4 bundle 常量，官方教程未给 URL，仅供参考）**：`dh→registry-1.docker.io`、`gcr→gcr.io`、`ghcr→ghcr.io`、`nvcr→nvcr.io`、`quay→quay.io`、`k8s→registry.k8s.io`、`mcr→mcr.microsoft.com`、`elastic→docker.elastic.co`（**无 gitlab**）。

### 2.5 同类方案对照（S11，用于机制对比章）

| 写法 | 示例 | 特点 |
| --- | --- | --- |
| 增加前缀（S11 标注"推荐"） | `k8s.gcr.io/coredns/coredns` → `m.daocloud.io/k8s.gcr.io/coredns/coredns` | **保留**原始上游主机名，镜像站域名插在最前面 |
| 修改镜像仓库的前缀 | `k8s.gcr.io/coredns/coredns` → `k8s-gcr.m.daocloud.io/coredns/coredns` | 上游主机名被换成专属子域 |

原文补充："DaoCloud 目前收录了 600+ 国外镜像"——**它是白名单制**（只能在已收录清单内拉取）。

`[推论]` 与厚浪的差别：厚浪用**短后缀替换**上游主机名（`ghcr.io/...` → `mirror.houlang.cloud/ghcr/...`），且**没有白名单**（任意该上游下的镜像都能透传）。这是"后缀代号"设计的由来，也是三家里最好记的一种。

---

## 三、矛盾与不一致（必须在笔记中显式处理）

| # | 矛盾 | 证据 | 处理方式 |
| --- | --- | --- | --- |
| D1 | 官方教程列 **9** 个后缀（含 `gitlab`），前端 bundle 内置常量只有 **8** 个（无 `gitlab`） | S1 后缀表 vs S4 `[dh,gcr,ghcr,nvcr,quay,k8s,mcr,elastic]` | 笔记写 9 个并**注明"以后缀以控制台镜像源列表为准"**；不把 bundle 常量当权威 |
| D2 | 官方教程只有上游**名称**（如 "Kubernetes Registry"），没有上游 URL | S1 表格 | 上游 URL 一律标注来源为 S4（实现细节），或干脆不写 URL 只写后缀 |
| D3 | 服务条款链接指向已失效域名 | S5 产品页 → `home.houlangs.com`；本机 DNS 复核：阿里 DoH 返回 `Status: 3`（NXDOMAIN） | 笔记可写"条款链接当前已失效"，**不要**引导用户去点 |

---

## 四、实操指引（可直接支撑章节写作）

### 4.1 标准路径（S1 + S4）

```
1. 访问 mirror.houlang.cloud 注册并登录
2. 控制台「访问令牌」→ 新建令牌
3. 复制生成的登录命令
4. 在需要拉镜像的机器上执行该登录命令 → 看到 "Login Succeeded"
5. 把镜像地址按后缀表改写，然后 docker pull
```

### 4.2 关键区别（本笔记的核心论点）

| | registry-mirrors | 前缀重写式（厚浪） |
| --- | --- | --- |
| 配置位置 | `daemon.json` / Desktop GUI（C4） | **不配置**，直接改写镜像地址（C18） |
| 覆盖上游 | **仅 Docker Hub**（C1） | Docker Hub + GHCR + quay + nvcr + k8s + mcr + elastic + gitlab（C19） |
| 凭据流向 | Hub 令牌会发给镜像站（C6） | 走 `docker login` 登录镜像站本身（C20） |
| 对 compose / k8s manifest | 无需改动 | **需要改写每一处 `image:`** |
| k8s 节点侧 | 不适用 | 要么改 manifest，要么用 containerd `hosts.toml`（C10–C12） |

> 最后一行是实际的取舍点：前缀重写对 `docker pull` 最省事，但对 k8s / compose 意味着要改文件。笔记里必须写清这个代价，否则用户会以为它"全局生效"。

### 4.3 可直接写进「常见坑」的条目

1. **把它填进 `daemon.json` 的 `registry-mirrors`** —— 机制上不成立，见 C1/C18。
2. **把令牌当账号密码到处贴** —— 令牌是 `docker login` 用的凭据（C20），泄露面等于账号。
3. **以为配置后 compose / k8s 自动生效** —— 两处都要显式改写 `image:`。
4. **`latest` 与缓存** —— 按 tag 拉取会回源校验 digest（C3、C22），所以"加速器里是旧版"通常不是原因。
5. **拿免费服务的限速当故障** —— 配额/限速数值无公开口径（C21，缺口 G3），不能编数字。

---

## 五、开放问题（保持未解决，不要写成结论）

| # | 问题 | 现状 |
| --- | --- | --- |
| Q1 | 拉公开镜像是否**必须**先 `docker login` | 教程把登录写成步骤（C16），但未说明匿名能否拉取。**未实测** |
| Q2 | 免费账号的月度配额与下载限速具体数值 | 无公开口径（C21）。**禁止编造** |
| Q3 | GHCR **私有**镜像能否经前缀加速、如何鉴权 | 公开渠道零验证记录 |
| Q4 | 上游不可用时"回退旧缓存"的具体时长 | 仅见后台配置项文案（C22），无公开数值 |
| Q5 | `docker logout` / 令牌吊销后的行为 | 未取证 |
| Q6 | 服务条款/隐私政策原文 | 托管域名已 NXDOMAIN（D3） |

---

## 六、下游交付（给 outline-generator / chapter-writer）

**笔记类型**：实战（practice）+ 速查（cheat_sheet）混合
**推荐章节骨架**（3–4 章，控制单文件可读性）：

1. **它到底是什么**——前缀重写式加速器；三分类对照表（registry-mirrors / 代理 / 前缀重写）；为什么不能填 `daemon.json`（C1 原文 + C18）
2. **怎么用**——注册 → 令牌 → `docker login` → 改写地址 → `docker pull`；9 后缀速查表；Docker Hub / GHCR 两个官方示例；Docker Desktop 与 Linux 服务器的差异
3. **进阶场景与常见坑**——compose 与 k8s manifest 的改写代价；containerd `hosts.toml` 路线（C10–C12）；坑 1–5；配额/限速"以控制台为准"
4. （可选）**同类方案对照**——与 DaoCloud 两种写法的差异（S11）；厚浪无白名单 vs DaoCloud 白名单

**必须遵守**：
- 每个核心概念补 `[!tip] 大白话` + 打比方
- 表格不嵌套在列表项内
- 代码块带语言标识 + 执行位置
- C1 / C6 等官方原文引用时**逐字**，不改写
- `[推论]` 与未实测项（Q1–Q6）必须显式标注，**不得升格为结论**
- D1 矛盾必须写出来，不允许只挑 9 个后缀的版本照抄

**阶段 6 交叉引用动作（已确认要做）**：

已用 `ls` 核实以下目标**全部存在**（注意：本 vault 下 `Glob` 工具返回空，改用 `ls` / 绝对路径核实）：

| 目标文件 | 关系 | 动作 |
| --- | --- | --- |
| `docker/镜像加速器vs代理-概念对比.md` | 概念前置 | **回链 + 修正定义**，见下 |
| `docker/DockerDesktop镜像加速器配置.md` | 同主题兄弟篇 | 回链 |
| `docker/docker镜像拉取DNS解析超时排错.md` | 排错衔接 | 回链 |
| `docker/GHCR 推送镜像权限配置.md` | 直接对口 ghcr 后缀节 | 回链（对 Q3 有参考价值） |
| `docker/Docker MOC.md` | 索引 | 追加一条索引项 |

**修正 `docker/镜像加速器vs代理-概念对比.md` 的具体位置**（已逐行核对，行号为 2026-09-13 版本）：
- 第 18 行「一句话定义：Docker Hub 的镜像缓存服务器」
- 第 22 行「工作方式：只缓存 Docker Hub 的镜像」
- 第 127 行「❌ 镜像加速器只对 "docker pull" 生效」（ASCII 示意图内）
- 第 2.1 节（第 29 行起）把"镜像加速器"整体等同于 `registry-mirrors`

该笔记写于 `created: 2026-03-28 / updated: 2026-08-08`，其定义在 2026 年已不完整：它没区分 **registry-mirrors（原地镜像）** 与 **前缀重写式（改写镜像地址）** 这两类都叫"加速器"的东西。且它举的示例 `docker.m.daocloud.io` 恰好是 S11 里支持前缀模式的厂商，本身就是反例。
建议最小改动：在该笔记顶部加一个 `[!warning]`，说明"镜像加速器"实为三类（registry-mirrors / 前缀重写 / 代理），并链到本篇新笔记；**不要重写它的正文**，避免破坏用户既有结构。

- 加双链前逐条 `os.path.exists` 核实目标存在
