---
title: "第 5 章：Docker 走代理"
tags:
  - ubuntu
  - linux
  - 代理
  - 翻墙
  - docker
  - mihomo
created: 2026-08-29
updated: 2026-08-29
status: 已完成
source_project: ubuntu-server-proxy-docker
---

> [[04_系统级代理接管|← 上一章]] · [[README|🏠 首页]] · [[06_验证清单与常见坑|下一章 →]]

# 第 5 章：Docker 走代理

> 本章目标：让 Docker 的两类"上网"行为——`docker pull` 拉镜像、容器内应用出网——都走前面搭好的 mihomo 代理。[^c5-1] [^c5-2]

镜像仓库（Docker Hub、ghcr.io、registry.k8s.io）和国内直连一样会被墙，而容器里的程序（npm、pip、爬虫、各色服务）也要访问外网。很多人在这一步最困惑：为什么配了代理，`docker pull` 还是超时？为什么容器里 curl 又没走代理？答案只有一个——**Docker 有两条互相独立的网路，配置位置完全不同**。

## 5.1 先分清两条路径

| 对比项 | 拉镜像 | 容器内应用出网 |
| --- | --- | --- |
| 谁负责 | dockerd（Docker 守护进程） | 容器进程本身 |
| 配置位置 | `/etc/docker/daemon.json` 或 systemd drop-in | `~/.docker/config.json` 或 `docker run --env` |
| 生效时机 | 重启 dockerd 后 | 只对新容器/新构建生效 |
| 代理地址 | 宿主机 `127.0.0.1:7890` 即可 | 必须用**宿主机局域网 IP**，不能用 `127.0.0.1` |

> [!tip] 大白话
> 把 dockerd 想成**仓库管理员**，容器是**在仓库里租了办公室的住户**。拉镜像是管理员"进货"，要走管理员的专用进货通道（daemon.json）；容器里应用出网是住户"自己出门办事"，得给住户发门禁卡（config.json / --env）。两条通道互不相通——配好了进货通道，不代表住户也能出门。

**关键结论**：先确认你要解决的是"拉镜像"还是"容器出网"，再去对应的位置配置。

## 5.2 路径一：让 dockerd 走代理（拉镜像）

### 5.2.1 推荐：daemon.json 的 proxies 段

先睹为快，完整文件 `/etc/docker/daemon.json`：

```json
{
  "proxies": {
    "http-proxy": "http://127.0.0.1:7890",
    "https-proxy": "http://127.0.0.1:7890",
    "no-proxy": "*.local,localhost,127.0.0.1"
  }
}
```

逐段拆讲：

- `http-proxy` / `https-proxy`：dockerd 拉镜像时走的代理。这里用 `127.0.0.1` 是**对的**——dockerd 和 mihomo 同在宿主机网络，不属于容器网络。
- `no-proxy`：**直连白名单**，逗号分隔。`.local` 匹配所有 `.local` 域（含子域）；`localhost,127.0.0.1` 保证访问本机时绕过代理。

写完后**必须重启 Docker 才生效**（易错点之一）：[^c5-1]

```bash
sudo systemctl restart docker
```

> [!warning] 优先级
> daemon.json 的 proxies **优先级高于环境变量**。如果你同时用了下面的 systemd drop-in 环境变量方式，以 daemon.json 为准；两者二选一即可，不要同时维护两处。[^c5-1]

### 5.2.2 替代方案：systemd drop-in

不想碰 JSON，或想用环境变量的，可以给 dockerd 注入环境变量。完整文件 `/etc/systemd/system/docker.service.d/http-proxy.conf`：

```conf
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1,.local"
```

生效需要两步：

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo systemctl daemon-reload    # 重新读取 drop-in 文件
sudo systemctl restart docker
```

验证 dockerd 实际拿到的环境变量：

```bash
systemctl show --property=Environment docker
```

> [!warning] systemd 特殊字符
> 代理 URL 里若含 `# ? ! ( ) [ ] { }` 等特殊字符（常见于带密码的代理），systemd 会把它当指令解析，需要**双重转义**：`%` 写成 `%%`。例如密码 `pa%ss` 应写成 `Environment="HTTP_PROXY=http://user:pa%%ss@127.0.0.1:7890"`。[^c5-1]

## 5.3 路径二：让容器内应用走代理（出网）

### 5.3.1 推荐：~/.docker/config.json 的 proxies.default

先睹为快，完整文件 `~/.docker/config.json`：

```json
{
  "proxies": {
    "default": {
      "httpProxy": "http://192.168.1.100:7890",
      "httpsProxy": "http://192.168.1.100:7890",
      "noProxy": "*.local,localhost,127.0.0.1"
    }
  }
}
```

逐段拆讲：

- 键名是**驼峰**（`httpProxy`/`httpsProxy`/`noProxy`），和 daemon.json 的 kebab-case（`http-proxy`）不同。
- **必须把 `192.168.1.100` 换成你宿主机的局域网 IP**（`ip addr` 可查），不能用 `127.0.0.1`，原因见 5.4。[^c5-3] [^c5-4]

保存即生效，**不需要重启 Docker**。但关键点是：**只对新创建的容器和新构建生效，已存在的容器不受影响**（易错点之一）。[^c5-2] 它会在创建容器/构建时自动注入一组环境变量：`HTTP_PROXY` / `HTTPS_PROXY` / `NO_PROXY`（大小写都会注入）。

> [!tip] 大白话
> config.json 像是**入职时发的门禁卡**：只发给"之后入职的新员工"，老员工拿不到。所以改完 config.json 后，想让某个老容器走代理，唯一的办法是**重建**它（`docker compose down && up -d`），而不是 `docker restart`。

### 5.3.2 单容器临时指定：docker run --env

不想改全局配置，只想让某一个容器走代理：

```bash
docker run --rm -it \
  --env HTTP_PROXY=http://192.168.1.100:7890 \
  --env HTTPS_PROXY=http://192.168.1.100:7890 \
  alpine sh
```

`--env` 是单次覆盖，不写进任何配置文件，适合临时测试。

### 5.3.3 构建镜像时：docker build --build-arg

构建阶段（`RUN` 步骤里的 npm、pip 等）要走代理，用 `--build-arg` 传入：

```bash
docker build \
  --build-arg HTTP_PROXY=http://192.168.1.100:7890 \
  --build-arg HTTPS_PROXY=http://192.168.1.100:7890 \
  .
```

`HTTP_PROXY` / `HTTPS_PROXY` / `NO_PROXY` 是 Docker **预定义构建参数**，无需在 Dockerfile 里额外 `ARG` 声明，`RUN` 阶段即可读到。

> [!warning] 不要在 Dockerfile 里用 ENV 硬编码代理
> `ENV HTTP_PROXY=http://...` 会把代理地址（含可能的账号密码）**永久写进镜像的配置层**，任何拿到镜像的人都能看到，换台机器也会失效。正确做法就是上面的 `--build-arg`，只在构建时临时传入，不固化进镜像。[^c5-2]

## 5.4 最容易踩的坑：容器内访问宿主机代理

容器是**隔离的网络命名空间**，容器内的 `127.0.0.1` 指向容器自己，而不是宿主机。所以在容器里把代理配成 `127.0.0.1:7890`，连的是一个容器内不存在的端口，自然不通。[^c5-3] [^c5-4]

> [!tip] 大白话
> 每个容器是一间**独立的酒店房间**，`127.0.0.1` 是"这间房自己"的门牌。mihomo 在宿主机，相当于**酒店前台**。你在房间里拨 `127.0.0.1`，只会打到房间内部的分机，永远打不到前台。要联系前台，得拨前台的外线号码（宿主机 IP）。

容器内访问宿主机代理，三种正确写法任选其一：

1. **宿主机局域网 IP**：`http://192.168.1.100:7890`（最直观，5.3 的 config.json 用的就是它）
2. **docker0 网关**：默认桥接网络的网关就是宿主机，`http://172.17.0.1:7890`
3. **host-gateway 魔法域名**：
   ```bash
   docker run --add-host=host.docker.internal:host-gateway \
     --env HTTP_PROXY=http://host.docker.internal:7890 alpine sh
   ```

> [!warning] 前提：mihomo 必须允许局域网访问
> 以上三种方式能通，是因为第 3 章的 config.yaml 里开了 `allow-lan: true` + `bind-address: "*"`。如果没开，宿主机代理端口只监听 `127.0.0.1`，容器从外部网段访问会被拒绝。安全起见，确认该端口没有暴露到公网（详见下一章安全注意）。

## 5.5 端到端验证

按顺序跑一遍，全部通过说明两条路径都通了：

```bash
# 1) 拉镜像：找一个被墙仓库的镜像，能拉下来就说明 daemon 代理生效
docker pull registry.k8s.io/pause:3.9

# 2) 查看容器内自动注入的代理环境变量（config.json 生效的标志）
docker run --rm alpine sh -c 'env | grep -i proxy'
# 预期输出（IP 换成你的宿主机 IP）：
# HTTP_PROXY=http://192.168.1.100:7890
# HTTPS_PROXY=http://192.168.1.100:7890
# NO_PROXY=*.local,localhost,127.0.0.1
# 以及对应的小写 http_proxy / https_proxy / no_proxy

# 3) 容器内访问外网（alpine 自带 wget；要 curl 可用 curlimages/curl 镜像）
docker run --rm --env HTTP_PROXY=http://192.168.1.100:7890 \
  alpine sh -c 'wget -qO- https://www.google.com | head -c 200'
```

如果第 1 步失败：检查 daemon.json 是否已重启、`no-proxy` 是否误伤了目标域名。如果第 2/3 步失败：多半是代理地址用了 `127.0.0.1`，或 mihomo 没开 `allow-lan`。

## 本章小结

- Docker 有两条独立网路：**拉镜像（daemon 级）**和**容器出网（CLI 级）**，配置位置、生效时机都不同，先定位问题再动手。
- 拉镜像用 `/etc/docker/daemon.json` 的 `proxies` 段（或 systemd drop-in 环境变量），改完必须 `systemctl restart docker`；daemon.json 优先级高于环境变量。
- 容器出网用 `~/.docker/config.json` 的 `proxies.default`（写**宿主机 IP**），只对新容器/新构建生效，老容器要重建；单容器临时用 `docker run --env`，构建用 `docker build --build-arg`。
- **绝不要**在 Dockerfile 用 `ENV` 写代理地址——会固化进镜像、泄露敏感信息。
- 容器内访问宿主机代理：用宿主机局域网 IP / `172.17.0.1` / `host.docker.internal`，前提是 mihomo 开了 `allow-lan` + `bind-address: "*"`。

下一章把整条链路（mihomo → 系统命令 → apt/git → Docker）串成一份端到端验证清单，并把所有易错点汇总成一张速查表，方便以后随时回查。

## 脚注

[^c5-1]: Docker Docs — Configure the Docker daemon to use a proxy. <https://docs.docker.com/engine/daemon/proxy/>
[^c5-2]: Docker Docs — Configure proxy using the CLI. <https://docs.docker.com/engine/cli/proxy/>
[^c5-3]: Docker Forums 社区讨论：容器内访问宿主机代理需用 docker0 网关 / host-gateway（结合既有笔记交叉验证）。
[^c5-4]: 既有笔记 [[docker/docker进行代理]] — 宿主机已有 Clash 时，容器 HTTP_PROXY 要用宿主机 IP 而非 127.0.0.1。

> [[04_系统级代理接管|← 上一章]] · [[README|🏠 首页]] · [[06_验证清单与常见坑|下一章 →]]
