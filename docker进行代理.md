# 1. HTTP / SOCKS 代理（强烈推荐）

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

## 2.3.1 你自己在 Clash 里**主动开了鉴权**

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

如何看账号密码[如何查看账号密码？](外网如何使用代理进行翻墙.md#如何查看账号密码？)
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