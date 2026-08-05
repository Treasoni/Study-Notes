---
title: "第二章 国内镜像链与 Docker 基础设施准备"
type: chapter
chapter: 2
tags:
  - Home-Assistant
  - Docker
  - 国内镜像
  - 部署
created: 2026-08-05
updated: 2026-08-05
status: 已完成
source_project: ai-smart-home-system
---

# 第二章 国内镜像链与 Docker 基础设施准备

> 笔记类型：实战构建指南（practice）｜学习深度：精通
> 素材来源：`02_deep_research.md` §2（国内镜像链）、§6（时效性修正 #3）、§7（#1、#7）
> 前置关联：[[01_系统架构与部署选型|第一章 系统架构与部署选型]]

> [!summary] 本章回答三个问题
> 1. 为什么 `daemon.json` 的 `registry-mirrors` 对 `ghcr.io` 无效？
> 2. ghcr 镜像怎么用「前缀整体替换 + 回退链」稳定拉下来？
> 3. Docker Hub 加速、阿里云 ACR、前置环境清单怎么配？

第一章选定了「Container 为主」的部署路线，第一脚就会踩到一个真实卡点：在国内家庭宽带下，`docker pull ghcr.io/home-assistant/home-assistant:stable` 经常超时甚至拉不动。这一章把「镜像拉不动」这个卡点拆掉——先讲清楚为什么惯用的 daemon.json 加速对 ghcr 无效，再给出一条实测过的 ghcr 回退链和可直接复用的 `pull_with_fallback` 脚本，最后补上 Docker Hub 加速、ACR 定位和前置环境清单。配好这一层，第 3 章的 `install.sh` 才能真的「一条命令」跑通。

## 2.1 关键认知：registry-mirrors 只对 Docker Hub 生效，对 ghcr.io 无效

很多人在国内拉镜像遇到卡顿，第一反应是去 `/etc/docker/daemon.json` 配 `registry-mirrors`。这个操作对 Docker Hub（`docker.io`）下的镜像有效，但对 `ghcr.io`（GitHub Container Registry）**完全无效**。

原因在于 `registry-mirrors` 的工作机制：它只改写**默认 registry**（Docker Hub）的拉取请求，Docker 不会对 `ghcr.io`、`quay.io` 这类第三方 registry 做镜像改写。你配再多 mirror，`docker pull ghcr.io/...` 还是会直连 GitHub 的 registry，而它在国内就是慢 / 易超时[深度收集 §2](../02_deep_research.md)。

所以正确的做法只有一个：**把镜像名里的 registry 前缀整体替换成可用的代理地址**。例如：

| 原镜像名 | 替换后的镜像名（示例） |
|----------|------------------------|
| `ghcr.io/home-assistant/home-assistant:stable` | `ghcr.nju.edu.cn/home-assistant/home-assistant:stable` |
| 同上 | `docker.m.daocloud.io/ghcr.io/home-assistant/home-assistant:stable` |
| 同上 | `ghcr.1ms.run/home-assistant/home-assistant:stable` |

替换前缀有两种形态，对应不同代理源的写法[深度收集 §2](../02_deep_research.md)：

| 形态 | 规则 | 例子 |
|------|------|------|
| 直接替换 | 把 `ghcr.io/` 整段换成新主机名 | `ghcr.io/...` → `ghcr.nju.edu.cn/...` |
| 追加前缀 | 在新主机名后保留 `/ghcr.io/` 路径段 | `ghcr.io/...` → `docker.m.daocloud.io/ghcr.io/...` |

写错形态是最常见的坑：把「直接替换」用在 DaoCloud 上（写成 `docker.m.daocloud.io/home-assistant/...`），或者把「追加前缀」用在 nju 上（写成 `ghcr.nju.edu.cn/ghcr.io/home-assistant/...`），都会拉到一个不存在的地址。动手前先确认你要用哪种形态。

配回退链之前，可以用一条命令先探测候选源是否可达——registry 的 `/v2/` 端点能连通（返回 200 或 401）说明主机可达：

```bash
curl -sI -m 10 https://ghcr.nju.edu.cn/v2/ | head -n 1
```

替换前缀之后，拉到的镜像内容和官方完全一致（同一个 registry 里的同一个 repo），只是网络路径不同。为了让 `docker-compose.yml` 里统一写官方名，拉完后用 `docker tag` 把代理名打回原始名即可（见 2.2 的脚本）。

> [!warning] 别指望 registry-mirrors 解决 ghcr
> `registry-mirrors` 只对 Docker Hub 生效。凡是从 `ghcr.io` 拉镜像，必须整体替换镜像名前缀；否则加速配置配得再全也是白配。

## 2.2 ghcr 回退链实测与优先级

单个代理源会挂，所以产品化部署要做成「回退链」：按优先级依次尝试，任一成功即停。下表是 2026-08 实测核实过的 ghcr 代理源[深度收集 §2](../02_deep_research.md)：

| 优先级 | 前缀 | 匿名可用 | 说明 |
|--------|------|---------|------|
| 1 | `ghcr.nju.edu.cn` | ✅ | 高校公益，`/v2/` 探测正常，优先教育网，回退链首位 |
| 2 | `docker.m.daocloud.io/ghcr.io` | ✅ | DaoCloud 反代，通用前缀替换，属「追加前缀」型 |
| 3 | `ghcr.1ms.run` | ✅ | 社区 ghcr 代理 |
| 4 | `ghcr.io`（官方直连） | ✅ | 大陆慢 / 易超时，仅作兜底 |
| 5 | `ota.hasscn.top` | 大陆需实测 | HAOS-CN 渠道，境外探测 403（限大陆），放末位 |

为什么这么排？三条原则：一是**优先「可匿名 + 探测通过」的源**，nju 是高校公益且 `/v2/` 探测正常，所以放首位；二是**把「大陆直连慢」的官方源放中间靠后**，官方直连稳定但慢，作为第 4 跳兜底比放在前面更合理；三是**不确定的源放最后或注释掉**，`ota.hasscn.top` 境外探测返回 403（限大陆），大陆可用性未证实，所以放末位并默认注释。

> [!note] 两条待实测项（对应 §7 #1）
> `ghcr.nju.edu.cn` 与 `ota.hasscn.top` 在**中国大陆家庭宽带**的真实可用性仍未逐一实测；本文给出的是 2026-08 探测结论，落地前请按 §8.3 的节奏在目标网络再验证一遍。默认脚本把 `ota.hasscn.top` 注释掉，避免未经验证就进入生产回退链。

下面是一个可直接放进 `install.sh` 的 `pull_with_fallback` 函数骨架：对每个代理源执行 `timeout 300 docker pull`，失败自动切下一跳，成功后回打 tag 到原始名，保证后续 compose 统一用官方镜像名[深度收集 §2](../02_deep_research.md)。

```bash
#!/usr/bin/env bash
# pull_with_fallback：按回退链拉取 ghcr 镜像，任一成功即返回。
# 用法：pull_with_fallback ghcr.io/home-assistant/home-assistant:stable
pull_with_fallback() {
  local source="$1"                    # 原始镜像名（官方前缀）
  local path="${source#ghcr.io/}"      # 去掉前缀，得到 repo:tag

  # 回退链：nju → daocloud → 1ms → 官方直连（hasscn 默认注释，待大陆实测）
  local fallbacks=(
    "ghcr.nju.edu.cn/${path}"
    "docker.m.daocloud.io/ghcr.io/${path}"
    "ghcr.1ms.run/${path}"
    "${source}"
    # "ota.hasscn.top/..."   # 未验证格式，勿默认启用
  )

  for img in "${fallbacks[@]}"; do
    echo "[mirror] 尝试: ${img}"
    if timeout 300 docker pull "$img"; then
      echo "[mirror] 成功: ${img}"
      if [ "$img" != "$source" ]; then
        docker tag "$img" "$source"   # 打回官方名，compose 无需改镜像名
        echo "[mirror] 已打回原始 tag: ${source}"
      fi
      return 0
    fi
    echo "[mirror] 失败，切换下一跳: ${img}"
  done

  echo "[mirror] 全部镜像源失败，请检查网络或更换源" >&2
  return 1
}
```

两个使用注意点：`timeout` 命令来自 GNU coreutils，大多数 Linux 发行版自带；若在精简系统或 BusyBox 环境里缺失，脚本会报 `timeout: command not found`，需要在脚本头部检测或改用「后台拉取 + 轮询」的写法。`300` 秒是为 GHCR 大镜像（HA 镜像几百 MB）留的余量，太小会让慢速网络误判超时，太大又会让故障源拖住整条链。

> [!tip] 为什么拉完要 `docker tag` 回原始名
> 回退链中每个代理源的前缀不同，如果 compose 直接引用代理名，换源时就要改配置；统一「拉取时用代理名、拉完 tag 回官方名」后，`docker-compose.yml` 永远写 `ghcr.io/...`，换镜像源对上层零感知。这也是第 8 章「多客户复制」能成立的前提之一。

## 2.3 Docker Hub 加速配置

`registry-mirrors` 虽然对 ghcr 无效，但对 Docker Hub 是正经有效的，我们仍然要配——因为基础镜像（如 `python`、`debian`、`alpine`）都从 Docker Hub 拉。2026-08 可用的三个 Docker Hub 加速地址如下[深度收集 §2](../02_deep_research.md)：

编辑 `/etc/docker/daemon.json`（若不存在则新建）：

```json
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.m.daocloud.io",
    "https://docker.1panel.live"
  ]
}
```

保存后重启 Docker 并验证：

```bash
sudo systemctl restart docker

# 验证生效（应能看到三行 mirror 地址）
docker info | grep -A 4 "Registry Mirrors"
```

预期输出：

```text
 Registry Mirrors:
  https://docker.1ms.run/
  https://docker.m.daocloud.io/
  https://docker.1panel.live/
```

镜像列表的**顺序就是尝试顺序**：Docker 会按 `registry-mirrors` 数组从上到下尝试，成功即用。把最快的放最前面（示例里 `docker.1ms.run` 第一）能减少等待；某个源挂了 Docker 会自动切下一个，所以多配几个能提高容错。

两个易错点：一是 `daemon.json` 必须是合法 JSON，`"registry-mirrors"` 的值一定是**数组**，少了逗号或用了注释都会导致 Docker 启动失败；二是改完建议用 `sudo systemctl restart docker` 重启而不是 `reload`——部分版本对 reload 不重新读取 registry-mirrors，重启后用 `docker info` 立刻就能看出是否生效。

> [!warning] 记得区分两种加速
> `registry-mirrors`（daemon.json）只管 Docker Hub；ghcr 走 2.2 的「前缀整体替换 + 回退链」。两者是两套机制，缺一不可，别混为一谈。

## 2.4 阿里云 ACR 与产品镜像分发

很多人会想：既然 GitHub 的镜像拉不动，那把镜像全部搬到阿里云 ACR（容器镜像服务）当镜像站用行不行？——**不行**。阿里云 ACR 个人版新实例**不支持匿名拉取**，客户端必须 `docker login` 才能 pull，没法当公开镜像代理用。这也是时效性修正 #3 的核心：报告原方案把 ACR 个人版当作可匿名使用的镜像加速站，实际情况是新实例必须登录[深度收集 §6](../02_deep_research.md)。

所以「把 HA 官方镜像搬到 ACR 再分发给客户」这条路走不通——客户侧没有你的 ACR 凭据；即使有，个人版镜像仓库也做不到「公开匿名拉取」的镜像站体验。ACR 的正确定位只有一种：**产品自有镜像的分发通道**，也就是第 6 章要构建的 Agent 镜像（`ha-agent`）这一类私有产物：

```bash
# 推送方：先登录 ACR 个人版
docker login your-registry.cn-hangzhou.aliyuncs.com

# 给自研 agent 镜像打上 ACR 地址的 tag 并推送
docker tag ha-agent:latest your-registry.cn-hangzhou.aliyuncs.com/my-ns/ha-agent:1.0.0
docker push your-registry.cn-hangzhou.aliyuncs.com/my-ns/ha-agent:1.0.0
```

客户端在 `install.sh` 里拉这个镜像时，也要先 `docker login` 才能拉取——这也决定了产品化时要处理好「客户的 ACR 凭据从哪里来」。Agent 镜像到底走 ACR 私有、Docker Hub 公开还是自建 registry，属于 §7 #7 的待决策事项：ACR 私有适合国内可控分发但需要处理登录凭据，Docker Hub 公开最省事但国内拉取慢且镜像公开，自建 registry 可控性最高但运维成本最大[深度收集 §7](../02_deep_research.md)。就本项目「面向国内非技术用户」的约束，首版倾向 ACR 私有，但要在第 8 章 8.4 节把它定为产品决策项之一。

需要注意，ACR 的登录凭据（阿里云账号的访问密钥）是敏感信息，不要写死在 `install.sh` 里。若首版走 ACR 分发，至少要解决「客户侧凭据注入」：要么安装阶段引导客户在自己的阿里云账号下登录一次，要么为 Agent 镜像单独开一个只读权限的子账号。这属于产品化阶段（第 8 章）要定的决策，这里先知道有这个问题即可。

> [!note] 一句话记住 ACR 的边界
> **ghcr 镜像走代理回退链，Docker Hub 走 registry-mirrors，ACR 只放自研 agent 镜像**。三者各有各的位置，互不替代。

## 2.5 前置环境清单

最后把基础设施层的「验收标准」列出来。清单分两类：两个**不可协商的硬性前置**（架构、Docker 版本）和三个**容器运行时参数**（TZ、network_mode、privileged）。硬性前置不满足就装不起来，或装起来也是已 EOL 的 32 位残废版；运行时参数不设对，HA 会「能启动但体验不对」——时区错乱、发现不到设备，或多开了不必要的特权。第 3 章的 `install.sh` 第一步就是环境检测，这里给出检测逻辑和清单，方便你手动预检[深度收集 §1](../02_deep_research.md)：

```bash
# 架构检测：2025.12 起仅支持 x86_64 / aarch64
arch="$(uname -m)"
case "$arch" in
  x86_64 | aarch64) echo "[env] 架构 OK: ${arch}" ;;
  *) echo "[env] 不支持的架构: ${arch}（32 位已 EOL）" >&2; exit 1 ;;
esac

# Docker Engine 版本检测：需 23.0+
if ! docker info >/dev/null 2>&1; then
  echo "[env] Docker 未运行或未安装" >&2
  exit 1
fi
ver="$(docker version --format '{{.Server.Version}}')"
echo "[env] Docker Engine: ${ver}"
```

| 检查项 | 要求 | 说明 |
|--------|------|------|
| 架构 | `x86_64` / `aarch64` | 2025.12 起仅支持两类；i386/armhf/armv7 已 EOL |
| Docker Engine | 23.0+ | 官方明确 Docker Desktop 不可用，必须是 Engine |
| 时区 | `TZ=Asia/Shanghai` | 必须显式设置，否则 HA 时间 / 日志时区异常 |
| 网络模式 | `network_mode: host` | 官方推荐，mDNS/SSDP 设备发现依赖它 |
| 特权模式 | `privileged` 按需 | 仅接入 USB / Zigbee 设备时需要，默认不开 |

前两项决定「能不能装」，后三项决定「装出来好不好用」。`TZ` 不设会让实体状态和日志时间错乱，排查时非常误导；`network_mode: host` 是官方推荐，因为它直接复用宿主机网络栈，设备发现（mDNS/SSDP）才能扫到局域网里的品牌设备；`privileged` 默认不开，只有需要透传 USB/Zigbee 协调器时才开——常开会放大容器逃逸风险，产品化时应该按设备类型动态决定。

## 本章小结

- `registry-mirrors`（daemon.json）**只对 Docker Hub 生效**，对 `ghcr.io` 无效；ghcr 必须「整体替换镜像名前缀」。
- 前缀替换分「直接替换」与「追加前缀」两种形态，写错形态会拉到不存在的地址。
- ghcr 回退链优先级：`ghcr.nju.edu.cn` → `docker.m.daocloud.io/ghcr.io` → `ghcr.1ms.run` → 官方直连 → `ota.hasscn.top`（末位、待大陆实测）；每个 pull 加 `timeout 300`，失败自动切下一跳。
- `pull_with_fallback` 拉完用 `docker tag` 打回官方名，compose 永远写 `ghcr.io/...`，换源对上层零感知。
- Docker Hub 加速在 `daemon.json` 配 `registry-mirrors`（docker.1ms.run / docker.m.daocloud.io / docker.1panel.live），列表顺序即尝试顺序，与 ghcr 回退链是两套机制。
- 阿里云 ACR 个人版**不能匿名拉取**，只用于自研 agent 镜像分发，不作为 ghcr 替代；其凭据注入是第 8 章待决策项。
- 前置验收标准：`x86_64/aarch64` + Docker Engine 23.0+ + `TZ=Asia/Shanghai` + `network_mode: host`；`privileged` 仅 USB/Zigbee 需要。

---

镜像链这一层打通后，下一章就把这些准备工作串成产品动作：`install.sh` 一键脚本 + `docker-compose.yml` 编排。你会看到环境检测、写 daemon.json、`pull_with_fallback` 和就绪探测是如何被组装成「一条命令部署 HA + Agent」的。
