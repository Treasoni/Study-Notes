# Ubuntu Server 翻墙代理 + Docker 可用 - 探测结果

> 阶段：P1 探测式收集
> 检索日期：2026-08-29
> 状态：待用户选择学习方向

---

## 一、候选来源汇总（去重后 14 条）

### 镜头 1：Clash/Mihomo 服务器安装配置（5 条）

| # | 标题 | 来源 | URL | 等级 | 评分 |
|---|------|------|-----|------|------|
| 1.1 | mihomo GitHub Releases（官方内核发布页） | 官方 | https://github.com/MetaCubeX/mihomo/releases | official-doc | 5 |
| 1.2 | mihomo 官方文档 - Configuration 配置索引 | 官方 | https://wiki.metacubex.one/en/config/ | official-doc | 5 |
| 1.3 | mihomo 官方文档 - Create a running service（systemd） | 官方 | https://wiki.metacubex.one/en/startup/service/ | official-doc | 5 |
| 1.4 | Linux 服务器使用 Mihomo 内核实现流量转发 | 博客 | https://www.juyaohuang.com/blog/webfullstack/linux/clash-mihomo-linux | reputable-report | 4 |
| 1.5 | Ayanami0 mihomo 自用配置分享（含覆写脚本） | 社区 | https://linux.do/t/topic/1426518 | community | 3 |

### 镜头 2：Docker 走代理三路径（4 条）

| # | 标题 | 来源 | URL | 等级 | 评分 |
|---|------|------|-----|------|------|
| 2.1 | Docker Daemon proxy configuration | 官方 | https://docs.docker.com/engine/daemon/proxy/ | official-doc | 5 |
| 2.2 | Docker CLI proxy（容器/构建注入代理） | 官方 | https://docs.docker.com/engine/cli/proxy/ | official-doc | 5 |
| 2.3 | 容器内访问宿主机（127.0.0.1 指向自身） | 社区 | https://forums.docker.com/t/cannot-curl-a-local-webserver-on-host-from-inside-container/141190/5 | community | 4 |
| 2.4 | 利用 mihomo 实现多容器无感透明代理 | 社区 | https://lala.im/10165.html | community | 3 |

### 镜头 3：系统级代理接管（5 条）

| # | 标题 | 来源 | URL | 等级 | 评分 |
|---|------|------|-----|------|------|
| 3.1 | libcurl-env - curl 环境变量代理规则 | 官方 | https://curl.se/libcurl/c/libcurl-env.html | official-doc | 5 |
| 3.2 | git-config（http.proxy / http.proxyAuthMethod） | 官方 | https://git-scm.com/docs/git-config | official-doc | 5 |
| 3.3 | apt-transport-http - apt HTTP 代理 | 官方 | https://manpages.debian.org/bookworm/apt/apt-transport-http.1.en.html | official-doc | 5 |
| 3.4 | Mihomo 官方文档 - TUN 入站配置 | 官方 | https://wiki.metacubex.one/en/config/inbound/tun/ | official-doc | 5 |
| 3.5 | darkk/redsocks - iptables 透明代理源头实现 | 项目 | https://github.com/darkk/redsocks | primary | 4 |

**信源构成**：official-doc ×10，primary ×1，reputable-report ×1，community ×2 → 官方为主，质量良好。

---

## 二、方向菜单（请选择）

P0 已定「方案 A：Clash/Mihomo 客户端」。探测结果进一步揭示两条可选的**覆盖深度**路线：

```
A. 基础全覆盖（推荐 ⭐）
   内核安装 + systemd 常驻 → 系统环境变量（bash/apt/git/curl）
   → Docker daemon.json 拉镜像 + 容器 HTTP_PROXY
   优点：覆盖 90% 场景、步骤直接、与既有 docker 代理笔记衔接最顺
   素材：1.1-1.3 + 2.1-2.3 + 3.1-3.3

B. 进阶透明代理（TUN 全局接管）
   A 的全部 + Clash TUN / iptables 透明代理章节
   让所有容器自动走代理，无需逐个配环境变量
   优点：一劳永逸；缺点：复杂度高、易踩网卡/DNS 冲突
   素材：A 全部 + 1.5 + 2.4 + 3.4 + 3.5

C. A + B 完整手册
   两套都写，篇幅最长，适合系统性掌握
```

---

## 三、覆盖缺口（P2 需补充）

1. **mihomo 订阅导入的具体格式**：`proxy-providers` 的 type/url/interval 写法（官方文档索引页未展开，需 P2 深读）
2. **容器内代理地址选择**：`docker0` 网关 IP（172.17.0.1）vs `host.docker.internal`，需 P2 从 2.3 + 2.2 交叉验证
3. **`NO_PROXY` 排除规则**：内网/局域网地址如何不走代理（3.1 有依据）
4. **TUN 模式的 DNS hijack 与 strict-route** 若选方案 B，需深读 3.4

---

## 四、P2 深度收集预估

- **方案 A**：深读 7 条核心来源（1.1-1.3、2.1-2.3、3.1-3.3），产出 `02_deep_research.md`
- **方案 B/C**：额外深读 3 条（2.4、3.4、3.5），章节加「透明代理」
- 预计产出：核心概念 + 完整命令序列 + 常见坑位
