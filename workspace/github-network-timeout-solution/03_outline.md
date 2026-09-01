---
title: "GitHub 国内网络连接超时解决方案"
笔记类型: 实战笔记
源素材引用: ["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13","S14","S15"]
tags:
  - github
  - 网络
  - 代理
  - 镜像
  - GFW
created: 2026-08-29
---

# GitHub 国内网络连接超时解决方案

> 笔记类型：实战笔记（可落地的解决方案 + 原理）
> 面向读者：会用 git / 命令行、懂基本网络概念，遇到「agent / 工具从大陆网络拉取 GitHub 包超时」问题的开发者
> 结构主线：现象与诊断 → 根因原理 → 三种解决方案（代理 / 国内镜像 / hosts·gh-proxy）→ Agent 场景落地 → 决策速查表

---

## 第 1 章：现象与诊断 — 先确定超时发生在哪一环

- **篇幅**：中
- **覆盖要点**：GitHub Status 排除故障、GIT_TRACE_CURL 等追踪命令、curl -vI 验证 TCP/TLS、症状分层、低速中止与 postBuffer 误区
- **素材引用**：S1, S2, S3, S5
- **代码示例**：git 追踪命令、curl -vI

### 1.1 先排除 GitHub 自身故障
- GitHub Status 官方状态页（S1）：Git Operations 90 天 100% 可用；2026-08 曾出现两类官方故障（SSH Git 短时降级、codeload/archive 下载错误率约 50%）。
- 判断要点：大陆超时绝大多数是「本地/跨境路径」问题，而非 GitHub 故障（S1+S4 推断）。

### 1.2 用 git 追踪命令定位卡点
- `GIT_TRACE=1` 一般跟踪；`GIT_TRACE_CURL=1` 完整 curl 级转储（旧名 `GIT_CURL_VERBOSE` 已更替）；`GIT_TRACE_CURL_NO_DATA=1` 只留 info 与头；`GIT_TRACE_PACKET=1` 看对象协商；`GIT_TRACE2*` 系列（S2）。
- 默认对 cookie/Authorization/Proxy-Authorization 打码；`GIT_TRACE_REDACT=false` 可关闭（S2）。

### 1.3 症状分层：三类典型表现
- DNS 污染 → 浏览器 `DNS_PROBE_FINISHED_NXDOMAIN`；SNI 阻断/CDN 干扰 → 页面样式/登录按钮失效；跨境链路丢包 → TCP 握手超时、clone/push 卡 Writing objects 后断开（S5）。

### 1.4 git 低速中止与 postBuffer 误区
- `http.lowSpeedLimit` + `http.lowSpeedTime` 定义「低于 X 字节/秒持续 Y 秒即中断」，正是 Writing objects 挂起断连的机制（S3）。
- `http.postBuffer` 默认 1 MiB，官方明示调高对多数 push 无效，仅对 HTTP/1.0 或不合规代理有效且增内存（S3 vs S6 社区共识）。

<!-- 篇幅:中 | 素材:S1,S2,S3,S5 | 代码:git 追踪命令、curl -vI -->

---

## 第 2 章：根因 — GFW 如何干扰大陆访问 GitHub

- **篇幅**：中
- **覆盖要点**：GFW 中间人模型、四种干扰机制、带宽限速、加密 DNS 的局限、hosts 失效原理
- **素材引用**：S4, S5
- **代码示例**：无

### 2.1 GFW 是「中间人」而非简单防火墙
- GFW 位于每个国际连接中间，可被动观察亦可主动修改连接（S4）。

### 2.2 四种干扰机制
- 子网屏蔽/重路由（null-route 或 BGP 劫持，易连带误伤）；DNS 污染（境内解析器返回不同 IP，对境外解析器伪装应答）；关键词过滤（对明文流量回发 TCP-RST）；SNI 过滤（依据 TLS 握手明文 SNI 过滤，ESNI 被直接丢包）（S4）。

### 2.3 带宽限速与加密 DNS 的局限
- 对国际连接普遍节流（S4）；DoH/DoT 可部分绕过污染，但 GFW 也能阻断加密 DNS，部分境内 DoH 解析器返回类似污染结果（S4）。

### 2.4 为什么改了 hosts 拿对 IP 仍会被阻断
- 因 IP 共享 + TLS 加密，SNI 过滤独立于 DNS 结果存在 → 解释了「hosts 已指向正确 IP，走 HTTPS 仍被阻断」（S4+S5）。

<!-- 篇幅:中 | 素材:S4,S5 | 代码:无 -->

---

## 第 3 章：方案一 — 走代理：环境变量与各工具配置

- **篇幅**：长
- **覆盖要点**：libcurl 环境变量语义、git http.proxy、npm proxy、docker daemon 代理、透明代理要求
- **素材引用**：S3, S7, S11, S12
- **代码示例**：export 代理环境变量、git config 代理、npm config 代理、docker systemd drop-in

### 3.1 代理环境变量的通用语义（libcurl 规则）
- 按 URL scheme 选变量（https URL 用 `http_proxy`）；`http_proxy` 只认小写，其余变量大写也生效；scheme 专属变量覆盖 `ALL_PROXY`；`NO_PROXY` 逗号分隔规则（IP 前缀、域名含子域、前导 `.`、`*`）（S11）。
- 适用范围：curl/git/pip/go 等基于 libcurl 或遵循该惯例的工具都读这组变量。

### 3.2 git 代理配置与优先级
- `http.proxy` 优先于 `http_proxy`/`https_proxy`/`all_proxy` 环境变量；语法 `[protocol://][user[:password]@]proxyhost[:port][/path]`；`remote.<name>.proxy` 按仓库覆盖、空串禁用；`core.gitProxy` 针对 `git://`（S3）。
- 代理必须完全透明，不得改包（S3）。

### 3.3 npm 代理配置
- `proxy` / `https-proxy` 配置键；`HTTPS_PROXY`/`https_proxy`/`HTTP_PROXY`/`http_proxy` 环境变量均被采用；`noproxy` 默认取 `NO_PROXY`；`npm_config_*` 前缀环境变量全部视为配置参数（S12）。
- 与 libcurl 不一致：npm 大写也认（S12 vs S11）。

### 3.4 docker daemon 代理配置
- systemd drop-in（`/etc/systemd/system/docker.service.d/http-proxy.conf` + reload + restart + `systemctl show --property=Environment docker` 验证）；`daemon.json` 的 `"proxies"` 块；daemon.json/CLI 显式配置优先于环境变量（S7）。
- rootless 用 `~/.config/systemd/user/` + `systemctl --user`；Docker Desktop 忽略 daemon.json 代理，需在设置里配（S7）。

### 3.5 透明代理要求与常见坑
- 代理不得修改包；`http.postBuffer` 误区；环境变量大小写语义在 git/npm 间不一致。

<!-- 篇幅:长 | 素材:S3,S7,S11,S12 | 代码:export http_proxy、git config --global http.proxy、npm config set proxy、docker systemd drop-in -->

---

## 第 4 章：方案二 — 国内镜像加速

- **篇幅**：中
- **覆盖要点**：npmmirror、TUNA PyPI、goproxy.cn、Docker 加速器现状、混合源风险
- **素材引用**：S8, S9, S10, S13
- **代码示例**：npm config set registry、pip config set global.index-url、go env -w GOPROXY

### 4.1 npm：npmmirror 与 cnpm
- `npm config set registry https://registry.npmmirror.com`；或 `npm install -g cnpm --registry=...`；`cnpm sync <pkg>` 触发同步（S13）。

### 4.2 pip：TUNA 与配置优先级
- 临时 `-i`、默认 `pip config set global.index-url`、多镜像 `extra-index-url`；`simple` 不能少、必须 https；备用域名 `pypi.tuna.tsinghua.edu.cn`（S8, S9）。
- 配置优先级：命令行 > 环境变量 > 配置文件（`~/.config/pip/pip.conf` 等）（S9）；PDM/Poetry/uv 亦有官方配置段（S8）。

### 4.3 go：GOPROXY 与 sumdb
- `go env -w GO111MODULE=on` + `go env -w GOPROXY=https://goproxy.cn,direct`；sumdb 自动代理（S10）。

### 4.4 Docker 镜像加速器现状（推断）
- 2024 年后国内公共 registry 加速器多数关停/收紧；阿里云个人专属加速器需登录控制台获取，无通用公共地址（推断，需标注未验证）。

### 4.5 常见坑
- 混合源导致依赖锁问题（如 npm lock 中 registry 地址不一致）、pip 缓存旧包。

<!-- 篇幅:中 | 素材:S8,S9,S10,S13 | 代码:npm config set registry、pip config set global.index-url、go env -w GOPROXY -->

---

## 第 5 章：方案三 — hosts 与 gh-proxy 工具

- **篇幅**：中
- **覆盖要点**：GitHub520 hosts 方案、gh-proxy 反代前缀、时效与安全风险
- **素材引用**：S5, S14, S15
- **代码示例**：hosts 修改与 DNS 刷新、gh-proxy 前缀 git clone

### 5.1 hosts 方案：GitHub520 原理与使用
- 改 hosts 将 GitHub 域名解析到较快 IP；数据源 `https://raw.hellogithub.com/hosts`（不依赖访问 GitHub）；hosts 位置 Win `C:\Windows\...\hosts` / Linux、Mac `/etc/hosts`；刷新 DNS（Win `ipconfig /flushdns` / Mac `sudo killall -HUP mDNSResponder`）；SwitchHosts 远程源 + 1 小时自动刷新（S14）。

### 5.2 反代前缀：gh-proxy 用法与自部署
- GitHub URL 前加前缀 `https://gh.api.99988866.xyz/`；公共实例域名频繁变动、演示站不堪重负，大量使用建议自部署（CF Worker 或 Python 版）；CF 免费版日 10 万次请求（S15）。

### 5.3 时效与安全风险
- 私有仓库 `git clone https://user:TOKEN@ghproxy.com/...` 的 Token 会经第三方代理传输，有泄露风险（S15）；hosts 服务器 2026-12-31 到期、社区 IP 可能随 GitHub 变更失效、不适合自动化构建（S14, S5）。

<!-- 篇幅:中 | 素材:S5,S14,S15 | 代码:hosts 修改 + ipconfig/flushdns、killall -HUP mDNSResponder、gh-proxy 前缀 clone -->

---

## 第 6 章：Agent 场景落地 — 给拉包工具配好网络

- **篇幅**：短
- **覆盖要点**：环境变量 + git 全局配置组合、浏览器能开但 git 超时、docker build/pull 场景
- **素材引用**：S3, S5, S7, S11
- **代码示例**：export http_proxy + git config --global http.proxy 组合

### 6.1 环境变量 + git 全局配置的组合
- Agent 走系统环境变量或 git 全局配置均可：`export http_proxy=https://127.0.0.1:7890`（注意 libcurl 只认小写）+ `git config --global http.proxy`（S11, S3）。

### 6.2 浏览器能开但 git 超时的排查
- 浏览器能开但终端 git 超时 → git 未走系统代理，需显式 `git config --global http.proxy`（S5）。

### 6.3 Docker build/pull 的代理配置
- Docker daemon 不读 shell 环境变量，必须 systemd/daemon.json；agent 用 docker build/pull 拉镜像时同样适用（S7）。

<!-- 篇幅:短 | 素材:S3,S5,S7,S11 | 代码:export http_proxy + git config --global http.proxy -->

---

## 第 7 章：决策速查表与常见坑

- **篇幅**：短
- **覆盖要点**：五步决策流程、方案对照速查表、常见坑清单、未决问题
- **素材引用**：S1-S15（综合）
- **代码示例**：无

### 7.1 五步决策流程
- ① 排除 GitHub 自身故障（S1）→ ② 定位环节（`GIT_TRACE_CURL=1` / `curl -vI`）（S2）→ ③ 快速分类（DNS 污染 / git 未走代理 / 跨境丢包）（S5）→ ④ 有代理走代理（S3/S7/S11/S12）→ ⑤ 无代理走镜像 + hosts 临时手段（S13/S8/S10/S14/S15）。

### 7.2 方案对照速查表
- 代理 / npm·pip·go 镜像 / Docker 加速器 / hosts(GitHub520) / gh-proxy：各自适用场景、持久性、风险、是否适合自动化构建。

### 7.3 常见坑清单与未决问题
- postBuffer 误区（S3 vs S6）；环境变量大小写语义不一致（S11 vs S12）；`GIT_CURL_VERBOSE` 旧名（S2）；公共 DNS 8.8.8.8 可能被 UDP 劫持（S4+S5）；Docker Desktop 忽略 daemon.json（S7）。
- 未决问题：用户侧是否有可用代理及端口、Docker 公共加速器 2026-08 实际可用清单、pnpm 与 npm 共用 .npmrc proxy 键、`git://` 现实意义（S6/S15 相关）。

<!-- 篇幅:短 | 素材:S1-S15 | 代码:无 -->

---

## 学习路径说明

### 前置要求
- 会用 git / 命令行，懂基本网络概念（DNS、TCP、TLS 常识）
- 了解 GitHub 基本操作（clone/push/pull）
- （可选）有一台可用代理客户端（Clash/v2ray 类），用于第 3、6 章实操

### 学完能做什么
- 能独立诊断 GitHub 超时发生在哪一环（GitHub 故障 / DNS / TCP / TLS / 传输）
- 能为 git、npm、pip、docker、go 分别配置代理或国内镜像
- 能判断何时用 hosts、gh-proxy，并了解其时效与安全风险
- 能给 agent 运行环境统一配置好拉包网络（含 docker daemon 场景）

### 建议学习顺序
- 按章节顺序阅读：1 诊断 → 2 原理 → 3 代理 → 4 镜像 → 5 hosts/gh-proxy → 6 Agent 场景 → 7 速查表
- 第 1、2 章以理解为主，建议对照实际超时现象阅读
- 第 3、4、6 章是核心实操，建议在真实环境逐条执行并验证
- 第 5 章涉及第三方工具，重点阅读「时效与安全风险」小节
- 第 7 章可随时回查，作为日常速查

---

## 章节统计

- **章节数**：7
- **预计总篇幅**：中（约 20-28 页 / 约 1.0-1.4 万字）
- **篇幅分布**：短 ×2（第 6、7 章）· 中 ×4（第 1、2、4、5 章）· 长 ×1（第 3 章）
- **核心实操章节**：第 3、4、6 章
