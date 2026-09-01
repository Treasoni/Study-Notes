# Ubuntu Server 翻墙代理 + Docker 可用 - 深度素材

> 阶段：P2 深度收集（方案 A：基础全覆盖）
> 检索日期：2026-08-29
> 运行状态：`workspace/workflow-runs/ubuntu-server-proxy-docker.workflow.md`

---

## 一、范围（Scope）

笔记目标：在 Ubuntu Server 上安装 Clash/Mihomo 代理内核，通过**系统环境变量 + Docker 显式代理**让命令行工具、apt、git、Docker 拉镜像、Docker 容器全部走代理。不含 TUN/透明代理（已按用户 P1 选择排除，记为后续进阶方向）。

---

## 二、信源表（Source Table）

| ID | 来源 | 类型 | 等级 | 关键支撑点 |
|----|------|------|------|-----------|
| S1 | mihomo GitHub Releases | 官方 | official-doc | 内核二进制下载（amd64/arm64，.gz） |
| S2 | mihomo docs - General config | 官方 | official-doc | `allow-lan`/`bind-address`/`authentication`/`external-controller`/`mode`/`log-level` |
| S3 | mihomo docs - proxy-providers | 官方 | official-doc | 订阅导入 `type: http` + `url` + `path` + `interval` + `health-check` |
| S4 | mihomo docs - inbound | 官方 | official-doc | 顶层 `port`/`socks-port`/`mixed-port` 入站；`listen: 0.0.0.0` 安全警告 |
| S5 | mihomo docs - systemd service | 官方 | official-doc | `/etc/systemd/system/mihomo.service` 完整示例、`systemctl` 命令 |
| S6 | Docker Docs - daemon proxy | 官方 | official-doc | `daemon.json` `proxies` 段；systemd drop-in `Environment=`；`NO_PROXY` 规则；优先于环境变量 |
| S7 | Docker Docs - CLI proxy | 官方 | official-doc | `~/.docker/config.json` `proxies.default`；`--env`/`--build-arg`；构建用 ARG 而非 ENV |
| S8 | libcurl-env | 官方 | official-doc | `[scheme]_proxy` 环境变量规则；`http_proxy` 仅小写；`ALL_PROXY` 兜底；`NO_PROXY` |
| S9 | git-config | 官方 | official-doc | `http.proxy` 覆盖环境变量；`http.<url>.*` 按 URL；透明代理要求 |
| S10 | apt-transport-http(1) | 官方 | official-doc | `Acquire::http::Proxy`；支持 `socks5h`；`no_proxy` 环境变量；`DIRECT` 特殊值 |
| S11 | Docker Forums（反爬未取到正文） | 社区 | community | 容器内访问宿主机需 docker0 网关 IP / host-gateway（结合既有笔记交叉验证） |
| S12 | 既有笔记 `docker/docker进行代理.md` | 项目 | 内部 | 宿主机 Clash 7890 时容器 `HTTP_PROXY` 用宿主机 IP 不用 127.0.0.1 |

抓取缓存：`workspace/ubuntu-server-proxy-docker/.cache/sources/`

---

## 三、声明/信源映射（Claim/Source Map）

### 3.1 mihomo 内核安装
- **声明**：从 GitHub Releases 下载 `.gz` 二进制，改名 `mihomo` 放 `/usr/local/bin/`，配置放 `/etc/mihomo/config.yaml` → S1、S5
- **命令**（S5）：`cp mihomo /usr/local/bin` + `cp config.yaml /etc/mihomo`，`mihomo -d /etc/mihomo` 指定工作目录

### 3.2 systemd 守护
- **声明**：`Type=simple`，`ExecStart=/usr/local/bin/mihomo -d /etc/mihomo`，`ExecReload=/bin/kill -HUP $MAINPID`，`Restart=always`，`LimitNOFILE=1000000`，Capabilities 含 `CAP_NET_ADMIN CAP_NET_RAW` → S5
- **命令**（S5）：`systemctl daemon-reload && systemctl enable mihomo && systemctl start mihomo`
- **重载/查日志**：`systemctl reload mihomo`、`systemctl status mihomo`、`journalctl -u mihomo -ocat -e`

### 3.3 config.yaml 关键项
- **allow-lan**：`true` 允许其他设备（含 Docker 容器）通过代理端口访问 → S2
- **bind-address**：`"*"` 绑定所有 IP，容器才可经 docker0 网桥访问 → S2
- **mixed-port**：顶层入站选项，HTTP+SOCKS5 混合端口（常见 7890）→ S4
- **external-controller**：RESTful API，`127.0.0.1:9090`；改 `0.0.0.0` 可远程控制（注意安全）→ S2
- **mode**：`rule`（规则分流，默认）→ S2
- **authentication / skip-auth-prefixes**：代理端口鉴权，`127.0.0.1/8` 默认跳过 → S2
- **订阅导入**（S3）：
  ```yaml
  proxy-providers:
    provider1:
      type: http
      url: "订阅链接"
      path: ./proxy_providers/provider1.yaml
      interval: 3600
      health-check:
        enable: true
        url: https://www.gstatic.com/generate_204
        interval: 300
  ```
  - `path` 默认限制在 HomeDir（`-d` 指定目录）；其它位置需设 `SAFE_PATHS` 环境变量 → S3
  - 支持 `filter`/`exclude-filter`/`exclude-type` 筛选节点 → S3

### 3.4 系统级代理接管
- **curl/环境变量**（S8）：
  - `http_proxy` **仅小写**生效（大写 `HTTP_PROXY` 不被 libcurl 用于 http scheme）
  - `https_proxy` 大小写均可；`ALL_PROXY` 兜底所有 scheme；`NO_PROXY` 逗号分隔排除
  - 例：`export http_proxy=http://127.0.0.1:7890` + `https_proxy` + `all_proxy=socks5://127.0.0.1:7891`（mihomo mixed-port 则用同一端口）
- **apt**（S10）：
  - 推荐 `/etc/apt/apt.conf.d/proxy.conf`：
    ```
    Acquire::http::Proxy "http://127.0.0.1:7890";
    Acquire::https::Proxy "http://127.0.0.1:7890";
    ```
  - 支持 `socks5h://`（远端 DNS）；`DIRECT` 表示不走代理；也读 `http_proxy`/`no_proxy` 环境变量
- **git**（S9）：`git config --global http.proxy http://127.0.0.1:7890`（语法 `[protocol://][user[:password]@]proxyhost[:port][/path]`）；或继承环境变量；`http.<url>.proxy` 可按远程仓库覆盖
- **验证命令**：`curl -I https://www.google.com`（走代理）、`curl -I https://www.baidu.com`（应直连，由规则分流）、`apt update`、`git ls-remote https://github.com/...`

### 3.5 Docker 拉镜像代理（daemon 级）
- **daemon.json**（推荐，S6）：
  ```json
  {
    "proxies": {
      "http-proxy": "http://127.0.0.1:7890",
      "https-proxy": "http://127.0.0.1:7890",
      "no-proxy": "*.local,localhost,127.0.0.1"
    }
  }
  ```
  改后 `sudo systemctl restart docker`
- **systemd drop-in 替代**（S6）：`/etc/systemd/system/docker.service.d/http-proxy.conf`
  ```
  [Service]
  Environment="HTTP_PROXY=http://127.0.0.1:7890"
  Environment="HTTPS_PROXY=http://127.0.0.1:7890"
  Environment="NO_PROXY=localhost,127.0.0.1,.local"
  ```
  需 `systemctl daemon-reload && systemctl restart docker`；用 `systemctl show --property=Environment docker` 验证
- **优先级**：daemon.json > 环境变量（S6）；Docker Desktop **忽略** daemon.json（本笔记是 Linux Server，不适用）

### 3.6 Docker 容器走代理（CLI 级）
- **~/.docker/config.json**（推荐，S7）：
  ```json
  {
    "proxies": {
      "default": {
        "httpProxy": "http://宿主机IP:7890",
        "httpsProxy": "http://宿主机IP:7890",
        "noProxy": "*.local,localhost,127.0.0.1"
      }
    }
  }
  ```
  - 保存即生效，但**只对新容器/新构建生效**，不影响已存在容器（S7）
  - 自动注入 `HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY` 环境变量（S7 有 `docker run alpine` 验证示例）
- **单容器临时指定**：`docker run --env HTTP_PROXY=http://宿主机IP:7890 ...`（S7）
- **构建指定**：`docker build --build-arg HTTP_PROXY=http://宿主机IP:7890 .`；**不要用 Dockerfile `ENV` 写代理**（会嵌入镜像，含敏感信息风险）→ S7

### 3.7 关键坑位
1. **容器内不能用 `127.0.0.1` 访问宿主机代理**：容器内 127.0.0.1 是容器自身 → S11、S12。应使用：
   - 宿主机局域网 IP（如 `192.168.x.x`），或
   - docker0 网关 IP（默认 `172.17.0.1`），或
   - `--add-host=host.docker.internal:host-gateway` 后用 `host.docker.internal`
   - 前提：mihomo `allow-lan: true` + `bind-address: "*"`（S2）
2. **daemon.json 修改必须重启 docker** 才生效（S6）
3. **`~/.docker/config.json` 只影响新容器**（S7）
4. **`http_proxy` 大小写**：libcurl 只认小写 `http_proxy`；大写可能被忽略（S8）→ 设置时两个都写或用 `ALL_PROXY`
5. **NO_PROXY 规则**：`example.com` 匹配自身+子域，`.example.com` 只匹配子域；`*` 全部直连（S6）
6. **systemd 特殊字符**：代理 URL 中 `#?!()[]{}` 等需用 `%%` 双重转义（S6）
7. **订阅 path 安全限制**：mihomo 默认只允许 `-d` 目录内写文件，其它路径需 `SAFE_PATHS`（S3）
8. **HTTP/SOCKS 明文入站**：`listen: 0.0.0.0` 暴露到公网必须加 `authentication`，否则易被代理劫持（S4、S2；呼应既有笔记《外网如何使用代理进行翻墙》）

---

## 四、矛盾与注意（Contradictions）

| 主题 | 说法 A | 说法 B | 结论 |
|------|--------|--------|------|
| Docker 代理优先级 | daemon.json（S6） | systemd drop-in（S6） | 二选一；daemon.json 推荐且优先级更高；同用时 daemon.json 生效 |
| 容器代理注入位置 | `~/.docker/config.json`（S7） | `docker run --env`（S7） | config.json 全局默认；--env 单次覆盖；都只对新容器生效 |
| `HTTP_PROXY` 大小写 | libcurl 只认小写 http_proxy（S8） | Docker 文档用大写示例（S6/S7） | 系统命令设小写+大写双份；容器内 Docker 会同时注入大小写（S7 示例可见） |
| apt 代理配置 | `/etc/apt/apt.conf.d/proxy.conf`（S10） | 环境变量 `http_proxy`（S10） | 两者都支持；conf 文件更持久明确 |

---

## 五、实操指引（Practical Guidance）

推荐落地顺序（方案 A）：

```
1. 装内核    → S1/S5：下载 mihomo → /usr/local/bin/mihomo，/etc/mihomo/config.yaml
2. systemd   → S5：mihomo.service，enable + start
3. 自检      → curl -I https://www.gstatic.com/generate_204 应 200
4. 系统代理  → S8：/etc/profile.d/proxy.sh 写 http_proxy/https_proxy/all_proxy/no_proxy
5. apt 代理  → S10：/etc/apt/apt.conf.d/proxy.conf
6. git 代理  → S9：git config --global http.proxy
7. Docker 拉镜像 → S6：daemon.json proxies → systemctl restart docker
8. Docker 容器   → S7：~/.docker/config.json proxies.default（宿主机 IP）
9. 验证      → docker pull、docker run alpine curl 外网
```

示例 mihomo 最小 config.yaml（供大纲章节使用）：

```yaml
mixed-port: 7890
allow-lan: true
bind-address: "*"
mode: rule
log-level: info
external-controller: 127.0.0.1:9090

proxy-providers:
  provider1:
    type: http
    url: "YOUR_SUBSCRIBE_URL"
    path: ./proxy_providers/provider1.yaml
    interval: 3600
    health-check:
      enable: true
      url: https://www.gstatic.com/generate_204
      interval: 300

proxy-groups:
  - name: PROXY
    type: select
    use: [provider1]
```

---

## 六、开放问题（Open Questions）

1. 用户订阅是否为标准 Clash 订阅格式（含 `proxies`+`proxy-groups`+`rules`）？若为 sing-box 格式需转换 → 写入 P3 大纲时留占位，写作时提示用户确认订阅格式
2. 是否需要 `external-controller` 配合 Web UI（metacubexd）？方案 A 可加可不加 → 默认仅 CLI，备注可选
3. 服务器是否已有防火墙（ufw）？mihomo 端口需放行 → 写作时给 `ufw allow 7890/tcp` 提示
4. Docker 容器要代理的是「拉镜像」还是「容器内运行应用」？两者配置不同（daemon vs CLI），笔记均覆盖，但用户实际场景影响示例侧重

---

## 七、下游交接（Handoff）

- **大纲生成**：以下游 `03_outline.md` 为输入。素材覆盖：安装（S1/S5）→ 配置（S2/S3/S4）→ 系统代理（S8/S9/S10）→ Docker（S6/S7）→ 验证与坑位（S11/S12）。建议章节结构见 `01_explore_result.md` 方案 A。
- **缓存**：抓取正文保留在 `.cache/sources/`（01-08_*.md），供章节写作引用锚点；无需重复抓取。
- **删除项**：TUN/透明代理（S11 论坛原文未取到，且用户已选 A）→ 放入「进阶方向」备注，不展开。
