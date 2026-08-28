---
tags: [docker, 排错, DNS, registry-mirrors, 镜像加速, systemd-resolved]
created: 2026-08-28
updated: 2026-08-28
---

# Docker 镜像拉取 DNS 解析超时排错

> [!summary] 一句话结论
> 报错**不是镜像源返回错误**，而是 Ubuntu 的本地 DNS 解析器（`systemd-resolved`，监听 `127.0.0.53:53`）查询超时，导致 Docker 连第一个镜像源的 IP 都解析不出来；整个拉取卡在 DNS 阶段 160s 后直接中断。解决方法是：在 `/etc/docker/daemon.json` 里给 dockerd 显式指定公共 DNS，并移除已失效、排在第一个的 `docker.1ms.run`。

---

## 一、错误现场

环境：Ubuntu 服务器（`~/docker/hermes-stack`），执行 `docker compose up -d` 拉取 `nousresearch/hermes-agent:latest`。

```text
$ sudo docker compose up -d
[+] up 1/1
 ✘ Image nousresearch/hermes-agent:latest Error failed to resolve reference
   "docker.io/nousresearch/hermes-agent:latest": failed to do request:
   Head "https://docker.1ms.run/v2/nousresearch/hermes-agent/manifests/latest?ns=docker.io":
   dial tcp: lookup docker.1ms.run on 127.0.0.53:53:
   read udp 127.0.0.1:55494->127.0.0.53:53: i/o timeout
```

> [!note] 关键信息
> 整个操作耗时 **160.2s** 后报错退出，而不是快速失败。

当时的镜像加速配置 `/etc/docker/daemon.json`：

```json
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.m.daocloud.io",
    "https://hub-mirror.c.163.com",
    "https://dockerproxy.link",
    "https://docker.xuanyuan.me"
  ]
}
```

---

## 二、根本原因拆解

### 2.1 报错链条

```
docker compose up -d
  → 需要拉取镜像，走第一个 registry-mirror：docker.1ms.run
  → 向 https://docker.1ms.run/v2/... 发起 HEAD 请求
  → 需要把域名 docker.1ms.run 解析成 IP
  → 走系统 DNS：127.0.0.53:53（systemd-resolved）
  → UDP 查询超时：read udp ... i/o timeout
```

### 2.2 `127.0.0.53` 是什么

- Ubuntu 22.04+ 默认用 **systemd-resolved** 作为本地 DNS 缓存/转发器，监听 `127.0.0.53:53`。
- 它本身**不直接查根服务器**，而是把查询转发给上游 DNS（来自 `/etc/systemd/resolved.conf` 或 DHCP 下发）。
- 当上游不可用、网络不通或本地 DNS 服务异常时，这里就会表现为 **`i/o timeout`**。

### 2.3 为什么配了多个镜像源还是失败

Docker 的 `registry-mirrors` **按顺序尝试**，但：

> [!warning] 误区：多个镜像源 ≠ 快速回退
> 当**第一个**源在 **DNS 解析阶段**就卡住（160s 超时）时，整个请求直接中断退出，**不会继续轮询后面的源**。
> 只有「连接已建立但拉取失败」这类情况才会自动尝试下一个源；**域名都解析不出来**属于致命错误。

### 2.4 两个叠加问题

1. **系统 DNS 层故障**：`127.0.0.53:53` 查询超时，所有域名解析都受影响。
2. **排第一的 `docker.1ms.run` 已失效/不可达**：它既解析不出 IP，又占着第一的位置「堵路」，让后面的可用源根本没机会被尝试。

---

## 三、解决步骤

### 3.1 修改 daemon.json：指定公共 DNS + 移除失效源

```bash
sudo nano /etc/docker/daemon.json
```

```json
{
  "dns": [
    "223.5.5.5",
    "114.114.114.114",
    "8.8.8.8"
  ],
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://hub-mirror.c.163.com",
    "https://dockerproxy.link",
    "https://docker.xuanyuan.me"
  ]
}
```

> [!note] 字段说明
> - `dns`：让 dockerd 使用公共 DNS 解析镜像域名，**绕过故障的系统 DNS**。
> - 删掉 `docker.1ms.run`：避免失效源继续排在第一位「堵死」整个拉取。

### 3.2 重启 Docker 使配置生效

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

### 3.3 测试 DNS 与镜像源连通性（拉取前先自测）

```bash
# 验证公共 DNS 能正常解析镜像源域名
nslookup docker.m.daocloud.io 223.5.5.5

# 验证镜像源本身可达（401/200=可用；000/超时=不可用）
curl -s -o /dev/null -w "%{http_code}\n" -m 10 https://docker.m.daocloud.io/v2/
```

### 3.4 重新拉取并启动

```bash
sudo docker compose up -d
```

---

## 四、诊断命令速查

```bash
# 看系统当前 DNS 配置（指向 127.0.0.53 说明在用 systemd-resolved）
cat /etc/resolv.conf

# 看 systemd-resolved 状态与上游 DNS
resolvectl status

# 逐个测试镜像源的域名解析（找出哪个源「活着」）
nslookup docker.1ms.run
nslookup docker.m.daocloud.io
nslookup docker.xuanyuan.me

# 用公共 DNS 直接查（绕过系统 DNS，判断是不是系统 DNS 的锅）
dig @223.5.5.5 docker.m.daocloud.io +short

# 确认 daemon 配置已加载的镜像源
docker info | grep -A 10 "Registry Mirrors"
```

---

## 五、经验教训

> [!tip] 防坑清单
> 1. **看到 `lookup xxx on 127.0.0.53:53: read udp ... i/o timeout`**，先判断是「系统 DNS 层」问题，不是镜像源 403/404，别急着换源。
> 2. **失效源不要排在第一位**：镜像源可用性变化很快，失效源占首位会导致后续源没机会被尝试。
> 3. **registry-mirrors 按顺序尝试 ≠ 快速回退**：DNS 解析阶段超时是致命错误，会直接中断整个拉取。
> 4. **配置前自测**：`curl -s -o /dev/null -w "%{http_code}" -m 10 https://<镜像源>/v2/`，返回 401/200 表示可达。
> 5. **配置后验证**：`docker info | grep "Registry Mirrors"` 确认源已生效。
> 6. **长期方案**：也可以直接修复宿主机 systemd-resolved 的上游 DNS（`/etc/systemd/resolved.conf`），让系统全局恢复解析，而不只是 Docker 层面绕过。

---

## 相关文档

- [[Docker MOC]] - Docker 知识索引
- [[DockerDesktop镜像加速器配置]] - 镜像加速器配置方法、可用源列表、常见误区
- [[镜像加速器vs代理-概念对比]] - 镜像加速器与代理的区别与选择
- [[Linux-Docker与DockerCompose安装指南-国内网络版]] - Linux 安装 Docker/Compose（国内网络版）

---

**最后更新**：2026-08-28
