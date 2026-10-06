## 第 5 章 安装面板 3x-ui 与放行端口

上一章你拿到了命令行提示符，但机器上还什么都没有。这一章把 3x-ui 面板装上去，并放行它的 Web 端口。做完这章，你能在浏览器里打开一个登录页——但里面还没有可用节点，那要留到第 6 章。先提醒一个高频坑：面板端口不通，多半是"云厂商安全组"和"系统防火墙"只开了一道，5.4 专讲这件事。

### 5.1 3x-ui 是什么：一个管配置的 Web 面板

一句话定位：3x-ui 是一个开源的 Web 控制面板，用来管理 Xray-core 服务器（来源：A-3 | Features 前导段）。它不是协议，而是替你"点选式"地生成、下发并监控协议配置的界面——这正是本篇"面板流"的立足点。

**实体产物**：面板默认用 SQLite 存储，就是一个单文件，路径 `/etc/x-ui/x-ui.db`（来源：A-3 | Database Options）。这意味着面板装好后，你所有的入站、客户端、流量记录都落在这一个文件里。

**能力范围**：它支持的入站协议覆盖 VLESS、VMess、Trojan、Shadowsocks、WireGuard、AmneziaWG、TUIC v5、Hysteria2、MTProto、HTTP、SOCKS 等；内置订阅服务器，可输出 raw / JSON / Clash 三种格式，并会按客户端的 User-Agent 自动选择（来源：A-3 | Features）。

> [!warning] 降级表述
> 3x-ui **没有官方中文零基础教程**。本章的中文表述由本项目按官方英文文档（B-1、A-3）撰写，不假托官方中文口径；英文原文以官方 wiki 与仓库为准。

> [!note] 项目自述的使用定位
> 项目方明确写着"仅供个人使用，请勿用于非法用途或生产环境"（来源：A-3 | Important）。需要如实指出的是，这与它提供的多节点、多用户、配额、订阅等面向团队/商业的功能清单之间存在张力（素材 §5 冲突 2）——怎么用由你决定，但项目自述的定位是"个人使用"。

### 5.2 两条安装路径，凭据语义完全不同

这是本章最容易踩坑的地方：**一键脚本和 Docker 两种装法，登录凭据的来源完全是两码事，绝不能混着记**（素材 §5 冲突 4）。

**路径一：一键脚本（官方推荐）**

```bash
bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)
```

安装过程中，脚本会**随机生成用户名、随机密码、随机访问路径**，并在安装结束后打印出来（来源：B-1 | Install in one-line；A-3 | Quick Start）。这三个值要立刻记下来。

**路径二：Docker Compose**

```bash
mkdir panel
cd panel
# 用编辑器创建 docker-compose.yml，内容见下
docker compose up -d
```

其中 `docker-compose.yml` 的关键段落是：

```yaml
# panel/docker-compose.yml（节选）
services:
  3xui:
    image: ghcr.io/mhsanaei/3x-ui:latest
    container_name: 3xui_app
    ports:
      - "2053:2053"
    restart: unless-stopped
```

容器起来后访问 `http://<your-ip>:2053`，默认凭据是 **用户名 `admin`、密码 `admin`**（来源：B-1 | Using Docker Compose）。这是固定的默认口令，不是随机生成。

> [!warning] Docker 默认口令必须立即改
> Docker 部署的 `admin / admin` 是公开写死在文档里的默认值。官方要求在登录后**立即**在面板设置（`Panel Settings > Authentication`）里改掉管理员凭据，并建议同时开启两步验证、配置自定义面板路径（来源：B-1 | Using Docker Compose）。

| 对比项 | 一键脚本 | Docker Compose |
| --- | --- | --- |
| 初始用户名 | 随机生成 | 固定 `admin` |
| 初始密码 | 随机生成 | 固定 `admin`（**必须立即改**） |
| 访问路径 | 随机生成 web base path | 默认 `/`（可自定义） |
| 面板默认端口 | 安装时确认 | 2053（compose 里 `2053:2053`） |
| 入站端口是否自动暴露 | 是（随面板配置监听） | **否**，见 5.5 |

**路径三：手动安装**（不推荐，此处只标注存在）。它需先判断架构再下对应压缩包，架构用 `uname -m` 查看，官方支持 amd64、arm64、armv7、armv6、armv5、s390x；Alpine Linux 用 OpenRC 而非 systemd，官方建议 Alpine **改用一键脚本**（来源：B-1 | Manual installation）。

### 5.3 装完怎么进面板

装完后的访问地址由三部分拼成：

```text
http://<your-ip>:<your-port>/<your-path>
```

`<your-path>` 就是 5.2 提到的随机 web base path（Docker 用默认路径时可省略）。一键安装后随时运行 `x-ui` 可重新打开管理菜单，在那里能启停服务、查看或重置凭据、管理 SSL 证书（来源：B-1 | Install in one-line）。登录后第一件事不是建节点，而是**处理凭据**：改掉默认口令、能开两步验证就开。

### 5.4 放行端口是两件事，漏一件就访问不通

**云厂商安全组放行**和**系统防火墙放行**是两道独立的门，必须同时打开。

```bash
# 系统防火墙侧（Ubuntu/Debian 常见）
ufw allow 2053/tcp

# 若机器没有 ufw，用 iptables 直接插一条规则
iptables -I INPUT -p tcp --dport 2053 -j ACCEPT
```

另一道门在云厂商控制台：进入实例的**安全组 / 防火墙**页，把同一端口按 TCP 放行。两处端口号必须一致。

### 5.5 Docker 的隐藏坑：入站端口不会自动暴露

用 Docker Compose 时，`ports` 块**只发布了面板端口 2053**，你在面板里新建的**入站代理端口不会自动暴露**（来源：B-1 | Using Docker Compose）。这是第 6 章建完节点却连不通的最常见原因。官方给的两条解法：每建一个入站端口就往 `ports` 里加一条 `"<端口>:<端口>"` 再 `docker compose up -d`；或把 `ports` 块整体换成 `network_mode: host`，让面板打开的所有端口都直接暴露（来源：B-1 | Using Docker Compose）。

> [!tip] 大白话
> 把面板想成"装修公司前台"：一键脚本像前台随机发了一张工牌（随机账号密码），Docker 则像前台出厂贴了一张写着 `admin/admin` 的临时工牌——不换掉，等于谁都能进。而"放行端口"就是给这间办公室开两道门（云安全组 + 系统防火墙），只开一道，人还是进不来。

**本章小结**

- 3x-ui 是管理 Xray-core 的开源 Web 面板，默认 SQLite 存储 `/etc/x-ui/x-ui.db`。
- 一键脚本 = 随机凭据；Docker = 固定 `admin/admin` 且**必须立即改**，两者不能混记。
- 访问地址形如 `http://<your-ip>:<your-port>/<your-path>`；`x-ui` 命令可重开管理菜单。
- 放行端口是两件事：云厂商安全组 + 系统防火墙，缺一不可。
- Docker 默认只发布面板端口 2053，入站端口需手动加进 `ports` 或改用 `network_mode: host`。

**下一章预告**：面板能打开了，第 6 章就进到面板里"建第一个节点"——按字段顺序讲清协议、端口、身份凭据与传输安全，并告诉你哪些字段留空会直接导致连不上。内核层原理（手写 Xray JSON、REALITY 等）属于内核直配范畴，超出本篇范围，不展开。
