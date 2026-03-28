# 1. HTTP / SOCKS 代理（强烈推荐）

> [!tip] 相关概念
> 如果你不确定**镜像加速器**和**代理**的区别，请先阅读 [[镜像加速器vs代理-概念对比]]

适合：

- 拉镜像
- API
- Web 应用
- LunaTV / NASTools / 刮削

## 1.1 宿主机已经有代理（如 Clash）

假设代理地址是：

`宿主机IP:7890`

Docker Compose：

```bash
services:
  app:
    image: xxx
    environment:
      - HTTP_PROXY=http://192.168.1.10:7890
      - HTTPS_PROXY=http://192.168.1.10:7890
      - ALL_PROXY=socks5://192.168.1.10:7891

```

⚠ 注意：

- **不能用 127.0.0.1**
- 要用宿主机真实 IP

## 1.2 验证是否成功

```bash
sudo docker exec -it app bash curl https://google.com
```

能通 ✔
# 2. 什么时候【不需要】账号密码（最常见）

## 2.1  Clash 默认情况

- Clash / Clash Meta
- 节点来自订阅
- 本地监听端口：
    - HTTP：`7890`
    - SOCKS5：`7891`

👉 **默认：没有账号密码**

你直接用就行：

```bash
environment:
  - HTTP_PROXY=http://宿主机IP:7890
  - HTTPS_PROXY=http://宿主机IP:7890
  - ALL_PROXY=socks5://宿主机IP:7891
```

✔ 不用填任何用户名密码  
✔ Docker 容器、curl、apt 都能用

## 2.2 如何快速确认「有没有鉴权」

在宿主机执行：
```bash
curl -x http://127.0.0.1:7890 https://www.google.com -I
```

- **能返回 HTTP 200 / 301 / 302**  
    👉 没有账号密码
- **返回 407 Proxy Authentication Required**  
    👉 有账号密码 ❗


## 2.3 什么时候【需要】账号密码？

### 2.3.1 你自己在 Clash 里**主动开了鉴权**

比如配置里有：

```yaml
authentication:
  - "user1:pass1"
```

或者：
```yaml
users:
  user1: pass1
```

👉 那就必须填账号密码

如何看账号密码[如何查看账号密码？](../外网如何使用代理进行翻墙.md#如何查看账号密码？)
## 2.4 如果需要账号密码，怎么写？

### 2.4.1 HTTP / HTTPS 代理写法

格式👇

`http://用户名:密码@IP:端口`

Docker Compose 示例：

```bash
environment:
  - HTTP_PROXY=http://user1:pass1@192.168.1.10:7890
  - HTTPS_PROXY=http://user1:pass1@192.168.1.10:7890
```


### 2.4.2 SOCKS5 代理写法

`socks5://用户名:密码@IP:端口`

```bash
environment:
  - ALL_PROXY=socks5://user1:pass1@192.168.1.10:7891
```

# 3. HTTP 代理 vs SOCKS5 代理，到底有什么区别？

**先给你一个选型结论**

> **Docker 容器里：优先用 HTTP / HTTPS 代理**  
> SOCKS5：只有在你明确知道“这个程序支持 SOCKS5”时再用


## 3.1 本质区别

|对比点|HTTP 代理|SOCKS5 代理|
|---|---|---|
|工作层级|应用层（HTTP）|传输层（TCP/UDP）|
|是否懂协议|**懂 HTTP / HTTPS**|**不关心是什么协议**|
|支持范围|HTTP / HTTPS|**几乎所有 TCP**|
|Docker 友好度|⭐⭐⭐⭐⭐|⭐⭐|
|常见端口|7890|7891|


## 3.2 HTTP 代理是怎么工作的？

HTTP 代理只干一件事：

> **“帮你转发 HTTP / HTTPS 请求”**

流程：

```
容器程序 → HTTP 请求 → HTTP 代理 → 目标网站
```

它能做的事：

- 识别 URL
- 处理 HTTPS CONNECT
- 自动适配 curl / apt / wget / npm / pip
- Docker 官方就支持它

👉 所以 **极其稳定**

**典型 Docker 使用场景（强烈推荐）**

- 拉 GitHub
- 访问 TMDB / TheMovieDB
- 拉 API
- Web 服务

`HTTP_PROXY=http://宿主机IP:7890 HTTPS_PROXY=http://宿主机IP:7890`

## 3.3 SOCKS5 是怎么工作的？

SOCKS5 是：

> **“我不管你是什么协议，只负责把 TCP 流量转出去”**

流程：

`容器程序 → TCP 数据 → SOCKS5 → 外网`

它的特点：

✔ 通用  
✔ 支持非 HTTP（如 BT、FTP）  
❌ **程序必须明确支持 SOCKS5**


## 3.4  一张“人话理解图”
```text
HTTP代理：
“你要访问这个网页？我懂，我帮你发”

SOCKS5：
“你给我一坨数据，我帮你扔出去”

```

# 4. 如何给【已经存在的容器】添加代理？

> 这个点很重要：  
> **Docker 容器一旦创建，环境变量是不能动态改的**

所以答案是：

> ❌ 不能直接“给运行中的容器加代理”  
> ✅ 必须 **重建容器**


## 4.1 方法一（推荐）：改 docker-compose，然后重建

### 1️⃣ 修改 compose 文件
```bash
services:
  app:
    image: xxx
    environment:
      - HTTP_PROXY=http://宿主机IP:7890
      - HTTPS_PROXY=http://宿主机IP:7890

```


### 2️⃣ 重建容器（⚠ 不是 restart）

```
docker compose down
docker compose up -d

```

### 3️⃣ 验证

```
docker exec -it app sh curl https://github.com
```

---

## 4.2 方法二：只对「拉镜像」生效（很多人会搞混）

如果你是：

> docker pull 失败

那你需要的是 **Docker 守护进程代理**，不是容器代理。

### 配置 Docker daemon 代理
```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo nano /etc/systemd/system/docker.service.d/proxy.conf
```

内容：
```bash
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
```

然后：

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

⚠ 这个**只影响 docker pull / build**

---