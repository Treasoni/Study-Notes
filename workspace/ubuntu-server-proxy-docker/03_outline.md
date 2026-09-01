## 学习笔记大纲：《在 Ubuntu Server 中配置翻墙（代理），并让 Docker 容器和其他应用正常使用》

> 笔记类型：实战笔记（上手实战，面向有 Linux/Docker 基础的用户）
> 预计总篇幅：约 24 页（短 1 章 + 中 3 章 + 长 2 章）
> 章节数：6
> 范围声明：方案 A 基础全覆盖（mihomo 内核 + systemd + config.yaml + 系统环境变量 + Docker daemon/CLI 代理）；**不含 TUN/透明代理**，作为进阶方向在第 6 章末尾备注。

---

### 第一章：总览与方案选型
- **篇幅**：短
- **产物**：无（规划/架构）
- **覆盖要点**：
  - 场景痛点：Ubuntu Server 上 apt 源、GitHub、Docker Hub 等被墙，命令行与 Docker 拉镜像受阻
  - 方案选型：为什么在服务器端用 mihomo/Clash 内核（轻量、订阅友好、可被 systemd 守护）；对比系统级环境变量代理 vs TUN/透明代理，明确本笔记走「显式代理」路线
  - 架构总览（ASCII 图）：mihomo mixed-port:7890 ← 系统命令 / apt / git / Docker daemon.json / Docker 容器
  - 前置准备清单：root/sudo 权限、已装 Docker、有标准 Clash 订阅链接、确认服务器架构（uname -m → amd64/arm64）、确认订阅格式（Clash 标准 vs sing-box，写作时提示向用户确认）
  - 与既有笔记衔接：`docker/docker进行代理.md`、`docker/镜像加速器vs代理-概念对比.md`、`外网如何使用代理进行翻墙.md`
- **素材引用**：S1, S2, S4, S5, S6, S7
- **代码示例**：无（含 ASCII 架构图）

### 第二章：安装 mihomo 内核
- **篇幅**：中
- **产物**：`/usr/local/bin/mihomo` + `/etc/systemd/system/mihomo.service`
- **覆盖要点**：
  - 从 GitHub Releases 下载 mihomo 二进制（.gz 压缩包）：如何按架构选包、`uname -m` 确认、下载命令示例
  - 解压、改名 `mihomo`、移动到 `/usr/local/bin/`、`chmod +x`、`mihomo -v` 验证
  - 创建配置目录 `/etc/mihomo/`（config.yaml 在第 3 章详写，本章可放最小占位）
  - systemd unit `mihomo.service` 完整示例：`Type=simple`、`ExecStart=/usr/local/bin/mihomo -d /etc/mihomo`、`ExecReload=/bin/kill -HUP $MAINPID`、`Restart=always`、`LimitNOFILE=1000000`、Capabilities（CAP_NET_ADMIN/CAP_NET_RAW）
  - 启动与管理：`systemctl daemon-reload`、`enable`、`start`、`status`、`journalctl -u mihomo -ocat -e`
  - 自检：`curl -I https://www.gstatic.com/generate_204` 应返回 200
- **素材引用**：S1, S5
- **代码示例**：有

### 第三章：配置 config.yaml
- **篇幅**：长
- **产物**：`/etc/mihomo/config.yaml`
- **覆盖要点**：
  - 顶层入站：`mixed-port`（HTTP+SOCKS5 混合，常用 7890）、`port`/`socks-port`、`allow-lan`、`bind-address`、`external-controller`、`mode: rule`、`log-level`
  - `allow-lan: true` + `bind-address: "*"` 的意义（让 Docker 容器可经 docker0 访问）与安全警告（暴露公网需加认证）
  - 订阅导入 `proxy-providers`：`type: http` + `url` + `path` + `interval` + `health-check`（完整 YAML 示例）
  - 节点分组 `proxy-groups`（`select` 手选 / `url-test` 自动测速）与 `rules` 规则简介
  - 最小可运行 config.yaml 完整示例（可直接复制）
  - 写作时提示占位：向用户确认订阅是 Clash 标准格式（proxies/proxy-groups/rules）；sing-box 格式需先转换；`path` 默认限制在 `-d` 目录内，其它位置需设 `SAFE_PATHS`
  - 改配置后 `systemctl reload` / `restart mihomo`
- **素材引用**：S2, S3, S4
- **代码示例**：有（完整 config.yaml）

### 第四章：系统级代理接管
- **篇幅**：中
- **产物**：`/etc/profile.d/proxy.sh` + `/etc/apt/apt.conf.d/proxy.conf` + `~/.gitconfig`
- **覆盖要点**：
  - 为什么非 TUN 模式下系统命令需要环境变量才能走代理
  - `/etc/profile.d/proxy.sh` 写 `http_proxy`/`https_proxy`/`all_proxy`/`no_proxy`；**大小写坑**：libcurl 只认小写 `http_proxy`（大写 HTTP_PROXY 对 http scheme 不生效），建议小写+大写都写
  - apt 代理：`/etc/apt/apt.conf.d/proxy.conf` 写 `Acquire::http::Proxy` / `Acquire::https::Proxy`；支持 `socks5h://`（远端 DNS）与 `DIRECT` 直连
  - git 代理：`git config --global http.proxy`；`http.<url>.proxy` 可按远程仓库覆盖
  - 验证命令：`curl -I https://www.google.com`（走代理）、`curl -I https://www.baidu.com`（规则分流直连）、`apt update`、`git ls-remote https://github.com/...`
- **素材引用**：S8, S9, S10
- **代码示例**：有

### 第五章：Docker 走代理
- **篇幅**：长
- **产物**：`/etc/docker/daemon.json` + `~/.docker/config.json`
- **覆盖要点**：
  - 先区分两条路径：**拉镜像**（daemon 级）vs **容器内应用出网**（CLI 级），两者配置位置不同
  - daemon.json `proxies` 段完整示例（http-proxy/https-proxy/no-proxy），改后必须 `sudo systemctl restart docker`
  - systemd drop-in 替代方案：`/etc/systemd/system/docker.service.d/http-proxy.conf` 写 `Environment=`；用 `systemctl show --property=Environment docker` 验证；优先级 daemon.json > 环境变量
  - `~/.docker/config.json` `proxies.default` 完整示例（**用宿主机 IP** 而非 127.0.0.1）；只对新容器/新构建生效，不影响已存在容器
  - 单容器临时指定 `docker run --env`；构建用 `docker build --build-arg`，**不要用 Dockerfile `ENV` 写代理**（会嵌入镜像、含敏感信息风险）
  - 容器内宿主机 IP 陷阱：容器内 `127.0.0.1` 是容器自身；正确用宿主机局域网 IP / docker0 网关 `172.17.0.1` / `--add-host=host.docker.internal:host-gateway`（前提：mihomo `allow-lan: true` + `bind-address: "*"`）
  - 验证：`docker pull` 被墙镜像、`docker run alpine` 容器内 curl 外网
- **素材引用**：S6, S7, S11, S12
- **代码示例**：有

### 第六章：验证清单与常见坑
- **篇幅**：中
- **产物**：无（检查单）
- **覆盖要点**：
  - 端到端验证清单（按序）：mihomo 进程状态 → `generate_204` 200 → curl google/baidu → apt update → git ls-remote → docker pull → 容器内 curl
  - NO_PROXY 匹配规则：`example.com` 匹配自身+子域，`.example.com` 只匹配子域，`*` 全部直连
  - 常见坑汇总（表格）：daemon.json 改后需重启 docker；config.json 只对新容器生效；`http_proxy` 大小写；systemd 代理 URL 中 `#?!()[]{}` 等特殊字符需 `%%` 双重转义；订阅 `path` 需在 `-d` 目录内或设 `SAFE_PATHS`
  - 安全注意：`listen: 0.0.0.0` 暴露公网必须加 `authentication` 否则易被代理劫持；ufw 放行 `7890/tcp` 提示；不建议公网开放代理端口
  - 进阶方向备注：TUN/透明代理（本笔记不含），给出可后续扩展的线索
- **素材引用**：S6, S8, S2, S4, S11, S12
- **代码示例**：有（验证命令集合）

---

## 学习路径说明

### 前置要求
- 有 Linux 命令行基础，能以 root 或 sudo 执行命令
- 已安装 Docker 并了解基本命令（pull/run/build）
- 有一个可用的 Clash 标准格式代理订阅链接
- 知道服务器的 CPU 架构（`uname -m` 可查）与局域网 IP
- 服务器已配置公网 DNS（如 8.8.8.8），保证 mihomo 启动后能解析订阅域名

### 学完能做什么
- 服务器上所有命令行工具（curl/wget 等）经 mihomo 走代理，可访问被墙站点
- `apt update` 可正常拉取被墙的软件源
- `git clone` / `git ls-remote` 可访问 GitHub
- `docker pull` 可拉取 Docker Hub 等被墙镜像
- `docker run` / `docker build` 创建的容器可经宿主机代理出网
- 掌握一套排查顺序与常见坑位，能自己判断代理链路哪里断了

### 建议学习顺序
1. 按 第一章 → 第六章 顺序顺序阅读（每章依赖前一章产物，不可跳步）
2. 第二章+第三章合起来约 60-90 分钟（装好内核并跑通最小配置）
3. 第四章约 30 分钟（系统命令走代理）
4. 第五章约 45 分钟（Docker 两条路径分别验证）
5. 第六章作为自查清单随时回查
6. 若订阅为 sing-box 格式，先在第 3 章前完成格式转换再开始写作确认
