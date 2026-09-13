# 厚浪镜像（HLmirror）使用方法 - P1 探测结果

- **阶段**: P1（探测式收集）
- **运行标识**: `houlang-mirror-usage`
- **探测时间**: 2026-09-13
- **透镜数**: 3（A 机制权威文档 / B 厚浪自有资产 / C 第三方实测与排错）
- **候选记录**: 16 条（去重后），其中一手 11、二手 1、社区 4

> 说明：本文件只登记「来源是什么」，不登记「来源说了什么」。任何带结论的表述都必须等 P2 回原文核对后才能进 `02_deep_research.md`。

---

## 一、候选来源表（按透镜分组，已按 canonical URL 去重）

### 透镜 A — 权威机制文档

| ID | 标题 | URL | 层级 | 相关性 | 日期 | 分 |
| --- | --- | --- | --- | --- | --- | --- |
| S8 | dockerd CLI 参考（daemon.json 选项） | https://docs.docker.com/reference/cli/dockerd/ | 一手 | Docker 官方 daemon 配置参考，`registry-mirrors` 语义与取回顺序的权威出处 | n/a | 5 |
| S9 | containerd Registry Configuration (Hosts) | https://containerd.io/docs/1.7/hosts/ | 一手 | containerd 官方 registry 配置：`config_path`、`certs.d/hosts.toml`、`server` 与 host 镜像项、CRI 行为 | n/a | 5 |
| S10 | Kubernetes Images 概念页 | https://kubernetes.io/docs/concepts/containers/images/ | 一手 | k8s 官方镜像名解析规则；未写 registry 前缀时默认仓库由容器运行时配置决定 | n/a | 4 |
| S11 | DaoCloud 公共镜像加速 | https://docs.daocloud.io/community/mirror/ | 二手 | 同类前缀重写式加速器的厂商官方说明，含"增加前缀 / 修改镜像仓库前缀"两种改写用法 | n/a | 4 |

### 透镜 B — 厚浪自有资产

| ID | 标题 | URL | 层级 | 相关性 | 日期 | 分 |
| --- | --- | --- | --- | --- | --- | --- |
| S5 | 厚浪云官网 HLmirrors 产品页 | https://houlang.cloud/zh-CN/article/products/hlmirror | 一手 | 官方产品页；公布 `mirror.houlang.cloud`、`all.hlmirror.com`、备案号；其"使用协议/知识库"链接指向已失效域名 | n/a | 5 |
| S1 | 知识库《如何使用新版 HLmirror》 | https://home.houlang.cloud/archives/ru-he-shi-yong-xin-ban-hlmirror | 一手（厂商自述） | 运营方教程；**经 sitemap 证实是该知识库唯一文章**，含上游后缀表与用户群号 | 2026-03-31 | 5 |
| S4 | mirror.houlang.cloud 前端 bundle | https://mirror.houlang.cloud/assets/index-BE1n8cWp.js | 一手 | 含大量中文 UI 文案，全部属于控制台/管理后台，**无 FAQ、无公开文档路由、无条款文案** | n/a | 5 |
| S6 | 厚浪云系统状态页 | https://status.houlang.cloud/status/system | 一手 | Uptime Kuma 状态页，含独立 HLmirror 分组（`all.hlmirror.com`、Docker 镜像、Google SSL API Proxy） | n/a | 4 |
| S7 | HLmirrors 通用镜像站 | https://all.hlmirror.com/ | 一手 | 网页代理型通用镜像站，自述基于开源 cf-proxy-ex；公布唯一联系/投诉邮箱 | n/a | 4 |

### 透镜 C — 第三方实测、排错与替代方案

| ID | 标题 | URL | 层级 | 相关性 | 日期 | 分 |
| --- | --- | --- | --- | --- | --- | --- |
| S12 | moby/moby Issue #42022: Docker Hub Credentials Leaking to Registry Mirrors | https://github.com/moby/moby/issues/42022 | 一手 | Docker 上游仓库 issue，讨论 `registry-mirrors` 场景下的凭据流向问题 | n/a | 5 |
| S13 | 2025 年 Docker 国内镜像源配置指南（CSDN） | https://blog.csdn.net/weixin_28702105/article/details/159822253 | 社区 | **迄今唯一点名 hlmirror 的第三方实测帖**；结论待 P2 回源核对，无原始数据 | 2025-03 | 4 |
| S14 | V2EX《国内有 ghcr.io 的镜像加速吗？》 | https://global.v2ex.co/t/799069 | 社区 | 讨论 GHCR 等第三方/私有仓库能否被加速，涉及前缀式改写路径与鉴权边界 | n/a | 4 |
| S15 | 什么值得买《实测 26 个加速地址》 | https://post.smzdm.com/p/anvq683p/ | 社区 | 单线程端到端横向实测多家加速地址，含 429 限流、403 仅校园网等状态 | 2026-08 | 5 |
| S16 | 掘金《NAS 用户必看：Docker 镜像拉取噩梦》 | https://juejin.cn/post/7627535950394916891 | 社区 | 梳理"变慢"归因线索（匿名限速、大文件低优先级、公益镜像下线） | n/a | 4 |

### 去重记录

- 官方教程在透镜 A 与透镜 B 各被命中一次（A 判为「社区」、B 判为「一手」）。**合并为 S1，层级定为「一手（厂商自述）」**——它确实是运营方自己发布的一手材料，但只对"该服务如何被使用"这一事实成立，对"该服务有多好"属自述而非独立验证。
- 其余 15 条无重复。

---

## 二、方向菜单（请选 1 个作为 P2 深挖主线）

### 方向 1：机制三分法 —— 前缀重写 / registry-mirrors / 代理

> 回答"为什么厚浪不能填进 `daemon.json`"，并把 vault 现有笔记里"镜像加速器=registry-mirrors"的旧定义升级为三分法。

- 核心来源：S8、S9、S10、S11、S12、S1
- 产出重心：机制对比表 + 各自适用边界 + containerd / Kubernetes 侧对应配置点
- 价值：**修正既有笔记的不完整结论**，可复用性最高

### 方向 2：实操全链路 —— 从注册到成功 pull

> 注册 → 建令牌 → 目标机器 `docker login` → 改写镜像地址 → `docker pull`，覆盖 Docker Desktop / Linux / containerd / k8s 各场景。

- 核心来源：S1、S5、S4、S8、S9
- 产出重心：可复现步骤 + 9 个后缀对照速查表 + 各场景写法差异
- 价值：最贴"如何使用"的字面诉求

### 方向 3：排错与选型 —— 故障模式与同类方案对照

> 鉴权失败、令牌失效、限速导致的"变慢"误判、私有镜像、与 DaoCloud / 南大 / 中科大 / 1Panel 等对照选型。

- 核心来源：S12、S13、S14、S15、S16、S6、S11
- 产出重心：故障排查表 + 选型对照表
- 价值：排错场景命中率最高，但**社区来源占比高，需逐条降级标注**

**推荐：1 + 2 组合**（机制讲透 + 步骤可复现），方向 3 作为"常见坑"小节压缩进方向 2，不单独成章——因为方向 3 的一手来源最薄。

---

## 三、覆盖缺口（P2 需补，或明确标注为"未取证"）

| # | 缺口 | 现状 | P2 处理建议 |
| --- | --- | --- | --- |
| G1 | `registry-mirrors` **仅对 Docker Hub 生效**的官方明文措辞 | 未取证，仅有机制侧证；`docs.docker.com` 多次返回 000（需 `--http1.1` 重试），`image-library/mirror` 专页全程未取到 | 重试取原文；取不到则只写机制推论并标「推论」 |
| G2 | hlmirror 是否**必须登录**才能拉公开镜像 | 教程未说明，前端无相关文案 | 实测或明确标注"以控制台为准" |
| G3 | 免费**配额与限速数值** | 公开页面无任何面向用户的数值承诺；bundle 内仅见后台配置项文案 | 标注"以账号实际为准"，**禁止编造数字** |
| G4 | **GHCR 私有镜像**能否经前缀加速 | 公开渠道零验证记录 | 列为 open question，不写成结论 |
| G5 | 服务条款 / 隐私政策原文 | 托管域名 `home.houlangs.com` 解析为 NXDOMAIN | 标注"条款链接已失效" |
| G6 | 同类方案（南大、中科大、腾讯云）官方一手说明页 | 南大帮助页为 Vue SPA 未提取正文；A 透镜受 5 条上限未纳入中科大 | 按需补取 |
| G7 | 针对 hlmirror 的**独立第三方端到端基准** | 不存在；仅 S13 有定性评价，无数据、无复现方法 | 明确写"无独立基准" |
| G8 | Kubernetes 原生"镜像前缀重写"能力 | 官方无此 API；能力落在 containerd hosts.toml 或社区 mutating webhook | 按 S9 的一手口径写，不杜撰 k8s 原生支持 |

---

## 四、P2 预估范围

- **核心来源**：5 篇（S1、S8、S9、S1 同类需要的 S11/S12 视方向取舍）
- **补充来源**：≤3 篇（按缺口 G1、G6 临时补取）
- **不建议纳入 P2**：S13、S15、S16 三篇社区实测——除非方向 3 被选中；纳入时必须整篇降级标注为社区来源，且不得把其结论与官方口径混写
- **预计耗时**：1 轮精读 + 1 轮缺口补取

---

## 五、环境记录

- `crawl.sh --help` 退出码 0，crawl4ai 环境就绪，P2 无需 bootstrap。
- WebFetch 对 `mirror.houlang.cloud` / `home.houlang.cloud` 被拦截，全程改用 `curl`。
- `docs.docker.com` 对本机不稳，建议 `--http1.1` 重试。
