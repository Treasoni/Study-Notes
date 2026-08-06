---
title: "第二章 镜像与交付：HAOS 镜像 / 国内分发"
type: chapter
chapter: 2
tags:
  - Home-Assistant
  - HAOS
  - Docker
  - 国内镜像
  - 部署
created: 2026-08-05
updated: 2026-08-06
status: 已完成
source_project: ai-smart-home-system
---

# 第二章 镜像与交付：HAOS 镜像 / 国内分发

> 笔记类型：实战构建指南（practice）｜学习深度：精通
> 素材来源：深度收集 §2（HAOS 镜像与国内分发、ghcr 回退链）、§6（时效性修正 #3）、§7（#1、#7）
> 前置关联：[[01_系统架构与部署选型|第一章 系统架构与部署选型]]

> [!summary] 本章回答三个问题
> 1. HAOS 以什么形态交付？部署动作是「建 UEFI 虚拟机挂镜像开机」还是 install.sh？
> 2. 国内怎么把 HAOS 镜像和更新拿下来？（HAOS-CN 国内分发）
> 3. 走 Container 次级渠道时，ghcr 回退链 / Docker Hub 加速 / ACR 怎么配？

部署选型落定之后，第一道真实卡点就是「镜像与更新从哪里来」。这一章按主路径与次级渠道两条线拆：主路径是 HAOS，2.1 讲交付形态、2.2 讲国内分发（HAOS-CN）；次级渠道是 Container，2.3–2.6 保留 ghcr 回退链、Docker Hub 加速与 ACR 边界；最后 2.7 给一份分层的环境清单。配好这一层，第 3 章的部署动作才能真正「开机即用」。

## 2.1 主路径：HAOS 交付形态与部署动作

HAOS 是一套整机系统镜像，不是装在一台已有系统之上的软件。它的交付方式有三种，对应三句部署动作：

| 交付形态 | 说明 | 部署动作 |
|----------|------|---------|
| 预建 VM 镜像 | 官方发布 `haos_ova-{version}`，解压后得到 qcow2 / vdi / vmdk / vhdx 四种格式（ova 为跨平台打包格式），按宿主机选择对应格式 | 新建 UEFI 虚拟机，挂载镜像，开机 |
| 预刷迷你主机 | HAOS 已预刷好的 x86_64 / aarch64 迷你主机 | 接电开机即用 |
| 定制盒子 | 面向「完全不想碰命令行」用户的专用 HAOS 硬件 | 插盒开机 |

三种形态的共性：**没有传统 install.sh**。HAOS 的部署动作 = 开机，而不是「在一台已有系统上跑安装脚本」。这是它与 Container 最本质的差异——Container 需要你先有 Docker 主机、再装软件；HAOS 把「镜像」和「系统」打包在一起，开机即进入 HAOS 初始化界面。

如果你手上是 Proxmox，社区提供了现成的一键脚本，省掉手动「建 VM + 挂镜像」的重复劳动：

```bash
bash -c "$(wget -qO - https://github.com/community-scripts/ProxmoxVE/raw/main/vm/haos-vm.sh)"
```

脚本会拉取 HAOS 镜像、创建 UEFI 虚拟机并配置启动项，跑完开机即可进入 HAOS。注意它本质仍是「建 UEFI 虚拟机挂镜像开机」，只是把手工步骤自动化了，并不涉及任何 install.sh 逻辑（深度收集 §2）。

> [!note] HAOS 没有「install.sh」
> HAOS 交付动作 = 建 UEFI 虚拟机挂镜像开机（或插盒开机），不是传统安装脚本。第 3 章的 install.sh 属于 Container 次级渠道，主路径不涉及。

## 2.2 主路径：HAOS-CN 国内分发与更新

官方 `haos_ova` 镜像托管在 GitHub，下载慢；HAOS 系统更新默认也走境外 OTA。国内适配由 HAOS-CN 解决：它提供国内镜像与加速（ota.hasscn.top），社区把 HAOS 镜像和更新重定向到国内节点。

| 环节 | 境外默认路径 | HAOS-CN 国内适配 |
|------|-------------|-----------------|
| 获取 haos_ova 镜像 | GitHub release 下载 | 国内镜像节点下载 |
| 系统更新 | 境外 OTA | 国内节点（ota.hasscn.top） |

用法很简单：下载镜像时改从国内节点取 `haos_ova-{version}`（镜像内容与官方一致，只是网络路径不同）；更新时把 HAOS 的更新/OTA 地址指向 `ota.hasscn.top`，更新请求就全程走国内。这样「镜像从哪来、更新从哪来」两个问题都在主路径内闭环。

> [!warning] 大陆可用性先实测
> HAOS-CN 是境内适配渠道，境外探测返回 403（限大陆）。落地前请按第 8 章的时效性验证节奏，在目标网络分别实测「下载镜像」和「OTA 更新」两条链路，再把它写进交付流程（深度收集 §7 #1）。

同一个 HAOS-CN 生态在后面 Container 次级渠道里也会出现：2.4 的 ghcr 回退链末位 `ota.hasscn.top` 就是它。主路径里它是获取与更新的主通道，次级渠道里它只作为 ghcr 的兜底。

## 2.3 次级渠道（Container）：关键认知，registry-mirrors 只对 Docker Hub 生效

> [!note] 本节起为次级渠道
> 以下 2.3–2.6 全部面向 Container 次级渠道。HAOS 主路径不需要 Docker，也不需要镜像回退链；只有「容器化交付 / 已有 Docker 主机」场景才需要读这一段。

很多人拉镜像卡顿的第一反应是去 `/etc/docker/daemon.json` 配 `registry-mirrors`。这个操作对 Docker Hub（`docker.io`）有效，但对 `ghcr.io`（GitHub Container Registry）**完全无效**。

原因在 `registry-mirrors` 的工作机制：它只改写默认 registry（Docker Hub）的拉取请求，Docker 不会对 `ghcr.io`、`quay.io` 这类第三方 registry 做镜像改写。所以正确做法只有一个：**把镜像名里的 registry 前缀整体替换成可用的代理地址**。替换有两种形态（深度收集 §2）：

| 形态 | 规则 | 例子 |
|------|------|------|
| 直接替换 | 把 `ghcr.io/` 整段换成新主机名 | `ghcr.io/...` → `ghcr.nju.edu.cn/...` |
| 追加前缀 | 在新主机名后保留 `/ghcr.io/` 路径段 | `ghcr.io/...` → `docker.m.daocloud.io/ghcr.io/...` |

写错形态是最常见的坑：把「直接替换」用在 DaoCloud 上、或把「追加前缀」用在 nju 上，都会拉到一个不存在的地址。动手前先确认目标源属于哪种形态。

## 2.4 次级渠道（Container）：ghcr 回退链实测与优先级

单个代理源会挂，所以要做成「回退链」：按优先级依次尝试，任一成功即停。下表是 2026-08 实测核实过的 ghcr 代理源（深度收集 §2）：

| 优先级 | 前缀 | 匿名可用 | 说明 |
|--------|------|---------|------|
| 1 | `ghcr.nju.edu.cn` | ✅ | 高校公益，`/v2/` 探测正常，回退链首位 |
| 2 | `docker.m.daocloud.io/ghcr.io` | ✅ | DaoCloud 反代，通用前缀替换，属「追加前缀」型 |
| 3 | `ghcr.1ms.run` | ✅ | 社区 ghcr 代理 |
| 4 | `ghcr.io`（官方直连） | ✅ | 大陆慢 / 易超时，仅作兜底 |
| 5 | `ota.hasscn.top` | 大陆需实测 | HAOS-CN 渠道，境外探测 403（限大陆），放末位 |

排序三原则：优先「可匿名 + 探测通过」的源（nju 放首位）；把「大陆直连慢」的官方源放中间靠后兜底；不确定的源放最后或注释掉（`ota.hasscn.top` 默认注释）。

> [!note] 两条待实测项（深度收集 §7 #1）
> `ghcr.nju.edu.cn` 与 `ota.hasscn.top` 在中国大陆家庭宽带的真实可用性仍未逐一实测；本文给出的是 2026-08 探测结论。落地前在目标网络再验证一遍，默认脚本把 `ota.hasscn.top` 注释掉。

下面是可直接放进 install.sh 的 `pull_with_fallback` 函数骨架：对每个代理源执行 `timeout 300 docker pull`，失败自动切下一跳，成功后打回 tag 到原始名，保证 compose 统一用官方镜像名（深度收集 §2）：

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

两个使用注意点：`timeout` 来自 GNU coreutils，精简系统或 BusyBox 环境缺失时会报 `timeout: command not found`，需在脚本头部检测或改用「后台拉取 + 轮询」；`300` 秒是为 HA 这种几百 MB 大镜像留的余量，太小误判超时，太大让故障源拖住整条链。

> [!tip] 为什么拉完要 `docker tag` 回原始名
> 回退链里每个代理源前缀不同，compose 直接引用代理名就要随源改配置；统一「拉取时用代理名、拉完 tag 回官方名」后，`docker-compose.yml` 永远写 `ghcr.io/...`，换镜像源对上层零感知。

## 2.5 次级渠道（Container）：Docker Hub 加速配置

`registry-mirrors` 对 ghcr 无效，但对 Docker Hub 正经有效，仍然要配——基础镜像（`python`、`debian`、`alpine`）都从 Docker Hub 拉。编辑 `/etc/docker/daemon.json`（不存在则新建）（深度收集 §2）：

```json
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.m.daocloud.io",
    "https://docker.1panel.live"
  ]
}
```

保存后重启并验证：

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

列表顺序就是尝试顺序，把最快的放最前面能减少等待；某源挂了 Docker 自动切下一个。两个易错点：`daemon.json` 必须是合法 JSON，`"registry-mirrors"` 的值一定是数组；改完用 `sudo systemctl restart docker` 而非 `reload`，部分版本 reload 不重新读取 registry-mirrors。

> [!warning] 区分两种加速
> `registry-mirrors`（daemon.json）只管 Docker Hub；ghcr 走 2.4 的「前缀整体替换 + 回退链」。两套机制，缺一不可，别混为一谈。

## 2.6 次级渠道（Container）：阿里云 ACR 与产品镜像分发

「把 HA 官方镜像搬到阿里云 ACR 当镜像站」这条路走不通：ACR 个人版新实例**不支持匿名拉取**，客户端必须 `docker login` 才能 pull，没法当公开镜像代理（这是时效性修正 #3 的核心，深度收集 §6）。

ACR 的正确定位只有一种：**产品自有镜像的分发通道**，也就是第 6 章的 Agent 镜像（`ha-agent`）这类私有产物：

```bash
# 推送方：先登录 ACR 个人版
docker login your-registry.cn-hangzhou.aliyuncs.com

# 给自研 agent 镜像打上 ACR 地址的 tag 并推送
docker tag ha-agent:latest your-registry.cn-hangzhou.aliyuncs.com/my-ns/ha-agent:1.0.0
docker push your-registry.cn-hangzhou.aliyuncs.com/my-ns/ha-agent:1.0.0
```

客户端拉取时也要先 `docker login`——这决定了产品化时要处理好「客户的 ACR 凭据从哪里来」。Agent 镜像走 ACR 私有、Docker Hub 公开还是自建 registry，是深度收集 §7 #7 的待决策事项；就本项目「面向国内非技术用户」的约束，首版倾向 ACR 私有，但要在第 8 章把它定为产品决策项之一。ACR 登录凭据是敏感信息，不要写死在 `install.sh` 里。

> [!note] 一句话记住三种渠道的边界
> **ghcr 镜像走代理回退链，Docker Hub 走 registry-mirrors，ACR 只放自研 agent 镜像。** 三者各有位置，互不替代；且三者都只在 Container 次级渠道里出现。

## 2.7 前置环境清单

最后把「镜像与交付」这层的验收标准分两层列出。**主路径（HAOS）** 的四项：

| 检查项 | 要求 | 说明 |
|--------|------|------|
| 架构 | x86_64 / aarch64 | 2025.12 起仅支持两类，32 位已 EOL |
| 交付形态 | 预建 VM 镜像 / 预刷迷你主机 / 定制盒子 | 按客户硬件选择 |
| 虚拟化 | 支持 UEFI 的虚拟机 | 官方镜像按 UEFI 引导 |
| 网络 | 能连通 HAOS-CN 国内节点 | 镜像下载与系统更新走国内 |

**次级渠道（Container）** 的五项（第 3 章 install.sh 第一步会检测前两项）：

| 检查项 | 要求 | 说明 |
|--------|------|------|
| 架构 | x86_64 / aarch64 | 2025.12 起仅支持两类 |
| Docker Engine | 23.0+ | 官方明确 Docker Desktop 不可用 |
| 时区 | `TZ=Asia/Shanghai` | 必须显式设置，否则时间 / 日志错乱 |
| 网络模式 | `network_mode: host` | 官方推荐，mDNS/SSDP 设备发现依赖 |
| 特权模式 | `privileged` 按需 | 仅 USB / Zigbee 设备需要，默认不开 |

HAOS 那四项决定「能不能开机即用」；Container 那五项决定「能不能装起来、装出来好不好用」。产品化时按客户走的路径取对应清单，别混着验收。

## 本章小结

- 主路径是 HAOS：交付形态 = 预建 VM 镜像（`haos_ova-{version}` 解压得到 qcow2 / vdi / vmdk / vhdx）/ 预刷迷你主机 / 定制盒子；部署动作 = 建 UEFI 虚拟机挂镜像开机（或插盒开机），没有传统 install.sh。
- HAOS-CN 提供国内镜像与加速（ota.hasscn.top），把「下载 haos_ova」和「OTA 更新」都重定向到国内节点；境内可用性需在目标网络实测。
- Proxmox 上可用社区一键脚本 `haos-vm.sh` 自动建 HAOS 虚拟机，跑完开机即用，本质仍是「建 UEFI 虚拟机挂镜像开机」。
- 次级渠道（Container）三件事：`registry-mirrors` 只对 Docker Hub 生效；ghcr 用「前缀整体替换 + 回退链」（nju → daocloud → 1ms → 官方直连 → hasscn 末位）；ACR 个人版不能匿名拉取，只放自研 agent 镜像。
- 前置清单分两层：HAOS 主路径看架构 + 交付形态 + UEFI 虚拟机 + 国内节点连通；Container 次级渠道看架构 + Docker Engine 23.0+ + `TZ` + `network_mode: host`，`privileged` 仅 USB/Zigbee 需要。

---

镜像与交付这一层就绪后，下一章进入「部署动作」，把本章准备好的镜像变成真正跑起来的系统：HAOS 主路径是「建 UEFI 虚拟机挂镜像开机」的开机即用，Container 次级渠道是 install.sh + docker-compose 的一条命令编排。两条路在这一章都能对号入座。

---

> [[01_系统架构与部署选型|⬅ 第一章]] · [[基于 Home Assistant 的跨品牌 AI 智能家居一键部署系统|返回索引]] · [[03_一键部署install脚本与docker编排|第三章 ➡]]
