# GitHub 国内网络连接超时解决方案 - 深度研究素材 (P2)

> 运行标识：github-network-timeout-solution
> 生成时间：2026-08-29
> 阶段：P2 深度收集（research-collector）
> 用途：供 outline-generator（阶段 3）与 chapter-writer（阶段 4）使用

## 1. Scope

覆盖「agent / 工具从大陆网络拉取 GitHub 包超时」的完整链路：诊断 → 根因 → 代理方案 → 国内镜像加速 → hosts/CDN 工具 → agent 场景落地。产出定位为「可落地的解决方案 + 原理」。

## 2. Source table

| ID | 标题 | URL | Tier | 日期 |
|----|------|-----|------|------|
| S1 | GitHub Status 官方状态页 | https://www.githubstatus.com/ | official | 实时（2026-08-29） |
| S2 | Git 官方手册 git(1) — 环境变量/跟踪 | https://git-scm.com/docs/git | official | 2.55.0 |
| S3 | git-config 官方文档 | https://git-scm.com/docs/git-config | official | 持续更新 |
| S4 | TUM 学术综述《Survey on the Chinese Government's Censorship Mechanisms》 | https://netintum.de/fileadmin/TUM/NET/NET-2023-06-1.pdf | official(学术) | 2023-06 |
| S5 | ipdodo《GitHub 无法访问？2026 开发者终极网络抢救指南》 | https://www.ipdodo.com/news/16580/ | blog | 2026-03-16 |
| S6 | StackOverflow Q15240815 — remote end hung up | https://stackoverflow.com/questions/15240815/ | community | 2013 起持续更新 |
| S7 | Docker Daemon proxy configuration | https://docs.docker.com/engine/daemon/proxy/ | official | 持续更新 |
| S8 | 清华 TUNA PyPI 镜像帮助 | https://mirrors.tuna.tsinghua.edu.cn/help/pypi/ | official(镜像) | 持续更新 |
| S9 | pip 官方配置文档 | https://pip.pypa.io/en/stable/topics/configuration/ | official | 持续更新 |
| S10 | goproxy.cn（七牛 Go 模块代理） | https://goproxy.cn/ | official | 持续更新 |
| S11 | libcurl-env(3) manpage | https://manpages.debian.org/experimental/libcurl4-doc/libcurl-env.3.en.html | official | 2026-08-27 |
| S12 | npm config 官方文档 | https://docs.npmjs.com/cli/v10/using-npm/config | official | 持续更新 |
| S13 | npmmirror（阿里 npm 镜像） | https://npmmirror.com/ | official | 2026 在线 |
| S14 | GitHub520（hosts 方案） | https://github.com/521xueweihan/GitHub520 | community | 2026-08-29 |
| S15 | gh-proxy（GitHub 反向代理前缀） | https://github.com/suiyueqingqian/gh-proxy | community | changelog 止 2020.04 |

**Tier 分布**：official/primary 11 · community/blog 4。抓取产物存于 `sources/`（SO 被 Cloudflare 拦截，S6 仅存为社区参考）。

## 3. Claim/source map（按主题）

### 3.1 诊断：超时发生在哪一环

- 排查前先看 GitHub 官方状态页确认非 GitHub 故障：Git Operations 90 天 100% 可用（S1）。2026-08 曾有两类官方故障：SSH Git 短时降级（仅 SSH，约 4 分钟）、全网大故障（codeload/archive 下载错误率约 50%）（S1）。
- 大陆用户超时绝大多数是「本地/跨境路径」问题，而非 GitHub 故障（S1+S4 推断）。
- Git 官方诊断手段（S2）：
  - `GIT_TRACE=1`：一般跟踪输出。
  - `GIT_TRACE_CURL=1`：完整 curl 级转储（等价 `curl --trace-ascii`），`GIT_TRACE_CURL_NO_DATA=1` 只留 info 与头。
  - `GIT_TRACE_PACKET=1`：packet 级，排查对象协商/协议问题。
  - `GIT_TRACE2` / `GIT_TRACE2_EVENT` / `GIT_TRACE2_PERF`：trace2 文本/JSON/列式。
  - 默认对 cookie/Authorization/Proxy-Authorization 打码（`GIT_TRACE_REDACT=false` 可关）。
- 低速中止判定（S3）：`http.lowSpeedLimit`+`http.lowSpeedTime` 定义「低于 X 字节/秒持续 Y 秒即中断」——正是「Writing objects 挂起后断连」的机制。
- `http.postBuffer` 默认 1 MiB，官方明示调高对多数 push 问题**无效**，仅对 HTTP/1.0 或不合规代理有效且增内存（S3）。
- 症状分层诊断（S5）：DNS 污染 → 浏览器报 `DNS_PROBE_FINISHED_NXDOMAIN`；SNI 阻断/CDN 干扰 → 页面样式/登录按钮失效；跨境链路丢包 → TCP 握手超时、clone/push 卡 Writing objects 后断开。

### 3.2 根因：为什么大陆访问 GitHub 慢/超时

- GFW 位于每个国际连接中间，如同 MitM，可被动观察亦可主动修改连接（S4）。
- 四种机制（S4）：
  - **子网屏蔽/重路由**：null-route 或 BGP 劫持封锁 IP 子网，易连带误伤。
  - **DNS 污染**：境内解析器被要求返回不同 IP；对境外解析器伪装应答。2013 年 github.com 曾被 DNS 阻断，后因社区抗议解除。
  - **关键词过滤**：检查明文流量并回发 TCP-RST；对 HTTP 有专门检测。
  - **SNI 过滤**：因 IP 共享 + TLS 加密，GFW 依据 TLS 握手明文 SNI 主机名过滤；ESNI 被直接丢包。→ 这解释了「改了 hosts 拿到正确 IP，走 HTTPS 仍可能被阻断」。
  - **带宽限速**：对国际连接普遍节流。
- 加密 DNS（DoH/DoT）可部分绕过污染，但 GFW 也能阻断加密 DNS；部分境内 DoH 解析器返回与污染类似的结果（S4）。
- 大陆访问失败的三种典型（S5）：DNS 污染、SNI 阻断/CDN 干扰、跨境链路晚高峰丢包。

### 3.3 代理配置（各工具）

- **git**（S3）：`http.proxy` 优先于 `http_proxy`/`https_proxy`/`all_proxy` 环境变量；语法 `[protocol://][user[:password]@]proxyhost[:port][/path]`；`remote.<name>.proxy` 按仓库覆盖、空串禁用；`core.gitProxy` 针对 `git://`；文档要求代理必须**完全透明**，不得改包。
- **环境变量语义**（S11）：按 URL scheme 选变量（https URL 用 `http_proxy`）；**`http_proxy` 只认小写**，其余变量大写也生效；scheme 专属变量覆盖 `ALL_PROXY`；`NO_PROXY` 逗号分隔（IP 前缀、域名含子域、前导 `.` 仅子域、`*` 全直连）。
- **npm**（S12）：`proxy` / `https-proxy` 配置键；`HTTPS_PROXY`/`https_proxy`/`HTTP_PROXY`/`http_proxy` 环境变量会被采用；`noproxy` 默认取 `NO_PROXY`；`npm_config_*` 前缀环境变量全部视为配置参数。优先级：命令行 > 环境变量 > npmrc。
- **pip**（S8+S9）：临时 `pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple <pkg>`；默认 `pip config set global.index-url ...`；多镜像 `extra-index-url`；配置优先级：命令行 > 环境变量 > 配置文件（`~/.config/pip/pip.conf` 等）。
- **docker daemon**（S7）：两种方式——systemd drop-in（`/etc/systemd/system/docker.service.d/http-proxy.conf`，`Environment="HTTPS_PROXY=..."`，reload+restart，`systemctl show --property=Environment docker` 验证）与 `daemon.json` 的 `"proxies"` 块；daemon.json/CLI 显式配置优先于环境变量；rootless 用 `~/.config/systemd/user/` + `systemctl --user`；**Docker Desktop 忽略 daemon.json 代理，需在设置里配**。
- **go**（S10）：`go env -w GO111MODULE=on` + `go env -w GOPROXY=https://goproxy.cn,direct`；sumdb 自动代理。

### 3.4 国内镜像加速

- **npm**（S13）：`npm config set registry https://registry.npmmirror.com`；或装 cnpm（`npm install -g cnpm --registry=https://registry.npmmirror.com`）；支持 `cnpm sync <pkg>` 触发同步。
- **pip**（S8）：TUNA `index-url=https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple`（`simple` 不能少、必须 https）；备用域名 `pypi.tuna.tsinghua.edu.cn`；PDM/Poetry/uv 亦有官方配置段。
- **go**（S10）：`GOPROXY=https://goproxy.cn,direct`，缓存超 5268 万模块版本，七牛 CDN，无带宽限制。
- **Docker registry 加速器现状**（推断，未在抓取源验证）：2024 年后国内公共 registry 加速器多数关停/收紧；阿里云个人专属加速器需登录控制台获取，无通用公共地址。

### 3.5 hosts / CDN 工具

- **GitHub520**（S14）：改 hosts 将 GitHub 域名解析到较快 IP；数据源 `https://raw.hellogithub.com/hosts`（不依赖访问 GitHub）；hosts 位置 Win `C:\Windows\...\hosts` / Linux、Mac `/etc/hosts`；刷新 DNS（Win `ipconfig /flushdns` / Mac `sudo killall -HUP mDNSResponder`）；SwitchHosts 远程源 + 1 小时自动刷新；macOS 一键命令见工具摘要。
  - **可用性注意**：服务器 2026-12-31 到期、续费 831 元/年靠赞助；hosts 内容为社区实测 IP，可能随 GitHub 变更失效。
- **gh-proxy**（S15）：GitHub URL 前加前缀 `https://gh.api.99988866.xyz/`；私有仓库 `git clone https://user:TOKEN@ghproxy.com/...` **Token 会经第三方代理传输，有泄露风险**；公共实例域名频繁变动、演示站不堪重负，大量使用建议自部署（CF Worker 或 Python 版）；CF 免费版日 10 万次请求。
- **ipdodo 轻量修复**（S5）：查真实 IP 写 hosts + 刷新 DNS，或换公共 DNS 8.8.8.8/1.1.1.1；服务器硬编码 hosts 会因 IP 动态轮换数天失效，不适用于自动化构建。

### 3.6 Agent 拉包场景

- Agent 走系统环境变量或 git 全局配置均可（S11+S3）：`export http_proxy=https://127.0.0.1:7890`（注意 libcurl 只认小写 http_proxy）+ `git config --global http.proxy`。
- 浏览器能开但终端 git 超时 → git 未走系统代理，需显式 `git config --global http.proxy`（S5）。
- Docker 场景注意 daemon 不读 shell 环境变量，必须 systemd/daemon.json（S7）；agent 用 docker build/pull 拉镜像时同样适用。

## 4. 矛盾点与注意事项

| 主题 | 注意 |
|------|------|
| `http.postBuffer` | 官方明示调高**对多数 push 无效**，社区仍常见此建议（S3 vs S6 社区共识） |
| 代理环境变量 | libcurl `http_proxy` 只认小写（S11）；npm 大写也认（S12）——不同工具语义不一致 |
| `GIT_CURL_VERBOSE` | 旧名，现代 git 用 `GIT_TRACE_CURL`（S2 更正） |
| 公共 DNS | 8.8.8.8 可能被 UDP 劫持；DoH 部分可用（S4+S5） |
| hosts 方案 | 社区 IP 时效短、服务器到期（S14）；厂商指南含营销成分需打折（S5） |
| gh-proxy 类 | 第三方代理传输 Token 有泄露风险；域名变动频繁（S15） |
| Docker 加速器 | 公共加速器多已下架（推断，需标注） |

## 5. 实战指南（决策流程草案）

1. **先排除 GitHub 自身故障**：看 https://www.githubstatus.com/（S1）。
2. **定位环节**：`GIT_TRACE_CURL=1 git fetch` 观察卡在 connect/TLS/transfer（S2）；`curl -vI https://github.com` 看 TCP/TLS 是否完成。
3. **快速分类**：
   - DNS 解析错误/污染 → hosts 或换 DNS（S5/S14）。
   - 能开网页但 git 超时 → git 未走代理，配置 `http.proxy`（S5/S3）。
   - Writing objects 挂起断连 → 跨境丢包，走代理或镜像（S5）。
4. **首选代理**（有代理时）：环境变量 + git/npm/pip/docker/go 显式配置（S3/S7/S10/S11/S12）。
5. **无代理时**：包管理器镜像（npmmirror/TUNA/goproxy.cn）+ GitHub 克隆加速前缀；hosts 作为临时手段（S13/S8/S10/S14/S15）。
6. **Agent 场景**：统一导出代理环境变量 + 按工具落配置；Docker daemon 单独配（S7）。

## 6. Open questions（未决问题）

- 用户侧是否已有可用代理、代理端口是什么？（决定方案 4 vs 5）
- Docker 公共加速器 2026-08 的实际可用清单（需实测，本文仅推断）。
- pnpm 与 npm 共用 .npmrc proxy 键是否仍成立（社区惯例，未在本轮官方源验证）。
- `git://` 协议（core.gitProxy）在 2022 年 GitHub 移除 git:// 支持后是否还有现实意义。

## 7. Downstream handoff（下游交接摘要）

- 笔记建议结构（供大纲参考）：
  1. 现象与诊断（GitHub Status / GIT_TRACE_CURL / 症状分层）
  2. 根因原理（GFW 机制：DNS/SNI/RST/限速）
  3. 方案一：代理（环境变量 + git/npm/pip/docker/go 逐一配置 + agent 场景）
  4. 方案二：国内镜像（npm/pip/go + Docker 加速器现状）
  5. 方案三：hosts 与 gh-proxy 工具（含风险）
  6. 决策流程 / 对照速查表
- 每节需附可复制命令与来源标注；第三方工具须标注时效与安全风险。
- 已缓存全文：`sources/`（S6 除外）。
