# GitHub 国内网络连接超时解决方案 - 探测结果 (P1)

> 运行标识：github-network-timeout-solution
> 生成时间：2026-08-29
> 阶段：P1 探测式收集（research-collector）

## 方向菜单（3 镜头 × 5 方向）

| 镜头 | 覆盖意图方向 | 代表性候选 |
|------|------------|-----------|
| **A. 诊断与原理** | ① 超时环节诊断 + 大陆网络干扰根因 | GitHub Status、git 官方追踪、TUM 学术综述、ipdodo 指南 |
| **B. 工具级代理配置** | ② git/npm/pip/docker/go 代理 + ⑤ agent 代理 | git-config 官方、Docker daemon proxy、libcurl-env、npm config |
| **C. 镜像与 hosts 工具** | ③ 国内镜像加速 + ④ hosts/CDN 工具 | npmmirror、TUNA、goproxy.cn、GitHub520、gh-proxy |

## 候选源清单

### 镜头 A：诊断与原理

- **GitHub Status（官方状态页）** | https://www.githubstatus.com/ | official | 实时（2026-08 访问） | 排查前先确认 GitHub 侧无故障，区分「GitHub 宕机」与「本地/国内网络问题」 | 5
- **Git 官方手册 git(1) — GIT_TRACE / GIT_TRACE_CURL / GIT_TRACE_PACKET** | https://git-scm.com/docs/git | official | 更新至 2.55.0 | 定义现代诊断追踪变量（`GIT_CURL_VERBOSE` 为旧名），定位超时发生在 DNS/TCP/TLS 哪一环 | 5
- **TUM 技术报告 NET-2023-06-1《Survey on the Chinese Governments Censorship Mechanisms》** | https://netintum.de/fileadmin/TUM/NET/NET-2023-06-1.pdf | official（学术） | 2023-06 | 系统说明 DNS 污染、SNI 阻断、TCP RST 注入原理，解释 GitHub 为何在大陆被干扰 | 4
- **Stack Overflow — "Git, fatal: The remote end hung up unexpectedly"** | https://stackoverflow.com/questions/15240815/git-fatal-the-remote-end-hung-up-unexpectedly | community | 2013（持续更新） | 经典问答汇总 HTTPS clone 断线原因与 postBuffer/代理/DNS 排查经验 | 4
- **ipdodo《GitHub 无法访问？2026 开发者终极网络抢救指南》** | https://www.ipdodo.com/news/16580/ | community | 2026-03-16 | 按症状分层（DNS 污染/SNI 阻断/跨境丢包）定位失败环节，贴近国内排查路径 | 4

### 镜头 B：工具级代理配置

- **Git - git-config 官方文档** | https://git-scm.com/docs/git-config | official | 持续更新 | 权威说明 `http.proxy` 与 `remote.<name>.proxy`，并引用 `http_proxy`/`https_proxy`/`all_proxy` | 5
- **Docker Daemon proxy configuration（官方）** | https://docs.docker.com/engine/daemon/proxy/ | official | 持续更新 | systemd drop-in `HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY` 与 `daemon.json` `proxies` 字段，含 rootless | 5
- **清华 TUNA PyPI 镜像帮助** | https://mirrors.tuna.tsinghua.edu.cn/help/pypi/ | official | 持续更新 | pip 换源标准配置（`-i`、`pip config set global.index-url`、`extra-index-url`） | 5
- **goproxy.cn（七牛 Go 模块代理）** | https://github.com/goproxy/goproxy.cn | official | 持续更新 | 官方推荐 `go env -w GOPROXY=https://goproxy.cn,direct` | 4
- **libcurl-env(3) 环境变量参考** | https://manpages.debian.org/experimental/libcurl4-doc/libcurl-env.3.en.html | official | 2026-08-27 | `http_proxy` 小写识别、scheme 专属变量覆盖 `ALL_PROXY`、`NO_PROXY` 规则，解释 curl 系工具读取代理方式 | 4
- **npm config 官方文档（备用）** | https://docs.npmjs.com/cli/v10/using-npm/config | official | 持续更新 | `proxy`/`https-proxy` 配置键，可用 `npm config set` 或 `npm_config_*` 环境变量 | 4

### 镜头 C：镜像与 hosts 工具

- **npmmirror（阿里云 npm 官方镜像站）** | https://npmmirror.com/ | official | 2026 在线 | `registry.npmmirror.com` 与 cnpm 配置命令，npm 国内加速权威基准 | 5
- **goproxy.cn 官网** | https://goproxy.cn/ | official | 2026 在线 | `GOPROXY=https://goproxy.cn,direct`、CDN 全球加速与 sum.golang.org 校验 | 5
- **GitHub520** | https://github.com/521xueweihan/GitHub520 | community | 2026-08-29 | 29.5k star hosts 方案，Actions 自动测速更新最优 IP，SwitchHosts 自动更新 | 4
- **gh-proxy（GitHub 加速反向代理）** | https://github.com/suiyueqingqian/gh-proxy | community | changelog 止 2020.04 | ghproxy 前缀加速 clone/release/archive、私有仓库 Token 方式、Cloudflare Workers 自部署 | 4

## 去重与覆盖缺口

- **去重**：TUNA PyPI 帮助页在 B/C 双镜头命中，保留一份；goproxy.cn 以「官网」为主源（GitHub 仓库作引用）。
- **缺口 1**：Docker 国内公共 registry 加速器（中科大/网易等）2024 年后陆续下架，无仍可访问的官方帮助页；P2 建议改用阿里云个人专属加速器（需控制台登录获取地址）。
- **缺口 2**：Stack Overflow 页面直接抓取被 SO 反爬屏蔽（URL 已验证存在）；P2 抓取时可用 defuddle/缓存或转引社区经验。
- **缺口 3**：本次 MiniMax web_search MCP 配额不足，全部经 WebSearch 完成；中文长尾内容（如具体加速前缀最新可用性）P2 补充时需再验证。
- **时效注意**：ghproxy 类镜像/加速服务状态变动频繁，P2 需标注「2026-08 可用性」并提示用户此类工具的风险（第三方代理、账号安全）。

## P2 预估范围

- **核心抓取（约 6-8 个）**：Git 官方手册追踪变量、git-config、Docker daemon proxy、TUNA PyPI、npmmirror、goproxy.cn、GitHub520、gh-proxy。
- **补充（按需）**：ipdodo 分层诊断指南、npm config、TUM 学术综述（原理引用）。
- **产出物**：`02_deep_research.md`，含 scope、源表、claim/source 映射、矛盾点、实战指南、未决问题、下游交接摘要。
- **执行模式决策点**：P2 完成后询问用户「大纲模式（逐章写）」还是「随性模式（直接出笔记）」。
