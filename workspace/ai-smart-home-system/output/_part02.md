## 第二章 国内镜像链与 Docker 基础设施准备

> 笔记类型：实战构建指南（practice）｜学习深度：精通
> 素材来源：`02_deep_research.md` §2（国内镜像链）、§6（时效性修正 #3）、§7（#1、#7）
> 前置关联：[[01_系统架构与部署选型|第一章 系统架构与部署选型]]

> [!summary] 本章回答三个问题
> 1. 为什么 `daemon.json` 的 `registry-mirrors` 对 `ghcr.io` 无效？
> 2. ghcr 镜像怎么用「前缀整体替换 + 回退链」稳定拉下来？
> 3. Docker Hub 加速、阿里云 ACR、前置环境清单怎么配？

第一章选定了「Container 为主」的部署路线，第一脚就会踩到一个真实卡点：在国内家庭宽带下，`docker pull ghcr.io/home-assistant/home-assistant:stable` 经常超时甚至拉不动。这一章把「镜像拉不动」这个卡点拆掉——先讲清楚为什么惯用的 daemon.json 加速对 ghcr 无效，再给出一条实测过的 ghcr 回退链和可直接复用的 `pull_with_fallback` 脚本，最后补上 Docker Hub 加速、ACR 定位和前置环境清单。配好这一层，第 3 章的 `install.sh` 才能真的「一条命令」跑通。

### 2.1 关键认知：registry-mirrors 只对 Docker Hub 生效，对 ghcr.io 无效

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

### 2.2 ghcr 回退链实测与优先级

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

### 2.3 Docker Hub 加速配置

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

### 2.4 阿里云 ACR 与产品镜像分发

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

### 2.5 前置环境清单

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

### 本章小结

- `registry-mirrors`（daemon.json）**只对 Docker Hub 生效**，对 `ghcr.io` 无效；ghcr 必须「整体替换镜像名前缀」。
- 前缀替换分「直接替换」与「追加前缀」两种形态，写错形态会拉到不存在的地址。
- ghcr 回退链优先级：`ghcr.nju.edu.cn` → `docker.m.daocloud.io/ghcr.io` → `ghcr.1ms.run` → 官方直连 → `ota.hasscn.top`（末位、待大陆实测）；每个 pull 加 `timeout 300`，失败自动切下一跳。
- `pull_with_fallback` 拉完用 `docker tag` 打回官方名，compose 永远写 `ghcr.io/...`，换源对上层零感知。
- Docker Hub 加速在 `daemon.json` 配 `registry-mirrors`（docker.1ms.run / docker.m.daocloud.io / docker.1panel.live），列表顺序即尝试顺序，与 ghcr 回退链是两套机制。
- 阿里云 ACR 个人版**不能匿名拉取**，只用于自研 agent 镜像分发，不作为 ghcr 替代；其凭据注入是第 8 章待决策项。
- 前置验收标准：`x86_64/aarch64` + Docker Engine 23.0+ + `TZ=Asia/Shanghai` + `network_mode: host`；`privileged` 仅 USB/Zigbee 需要。

---

镜像链这一层打通后，下一章就把这些准备工作串成产品动作：`install.sh` 一键脚本 + `docker-compose.yml` 编排。你会看到环境检测、写 daemon.json、`pull_with_fallback` 和就绪探测是如何被组装成「一条命令部署 HA + Agent」的。

## 第三章 一键部署：install.sh 与 docker-compose 编排

> 笔记类型：实战构建指南（practice）｜学习深度：精通
> 素材来源：`02_deep_research.md` §2、§7（#4）
> 前置关联：第 2 章（国内镜像链与 Docker 基础设施准备）

> [!summary] 本章回答三个问题
> 1. 「一条命令」的背后，install.sh 到底按什么顺序做了哪些事？
> 2. HA 与 Agent 两个容器，如何在同一个 docker-compose.yml 里正确协作？
> 3. HA 官方镜像没有 curl，healthcheck 怎么写？.env 里的 API Key 怎么保护？

第 2 章解决了第一个真实卡点：国内网络下镜像拉不动。但「能拉镜像」和「客户能一键装好整套系统」之间还隔着一整段距离——装 Docker、写加速配置、拉两个镜像、填 API Key、等 HA 首次启动、给用户一个能访问的地址。本章把这些事固化成一个可重复执行的 `install.sh`，配一份同时编排 HA 与 Agent 的 `docker-compose.yml`，让「一条命令部署」从口号变成真的能跑的脚本。读完你不仅能读懂、复现，还能按自己的客户场景改造它。

### 3.1 install.sh 逐段拆解（8 个步骤）

「一键」不是魔法，是把 8 件确定的事按确定顺序做掉，并且每一步都可重跑。拆开来看是这样的：

| 步骤 | 动作 | 关键点 |
|------|------|--------|
| ① | 环境检测 | 拒绝 32 位架构；检查 Docker 是否已装 |
| ② | 装 Docker | `get.docker.com --mirror Aliyun`，失败回退 DaoCloud |
| ③ | 写 daemon.json | 只加速 Docker Hub；ghcr 走 ④ 的前缀替换 |
| ④ | ghcr 回退链拉镜像 | `pull_with_fallback`，每跳 `timeout 300` |
| ⑤ | 交互写 .env | TZ / DEEPSEEK_API_KEY / HA_IMAGE / AGENT_IMAGE，chmod 600 |
| ⑥ | 写 compose 并启动 | `docker compose up -d`，幂等收敛 |
| ⑦ | 等待就绪 | 探测 `:8123`，接受 200/302，超时 ≥600s |
| ⑧ | 打印访问地址 | 输出 HA 与 Agent 的入口 |

完整脚本骨架如下（`02_deep_research.md` §2 的 install.sh 骨架逐行落地，含注释）：

```bash
#!/usr/bin/env bash
# ============================================================
# 一键部署脚本 v1.0 —— HA + Agent 一条命令拉起
# 设计原则：可重复执行（幂等）、失败可重试、敏感信息保护
# 步骤：①环境检测 → ②装Docker → ③写daemon.json → ④回退链拉镜像
#       → ⑤交互写.env → ⑥写compose + up -d → ⑦等待就绪 → ⑧打印地址
# ============================================================
set -euo pipefail

# ---------- ① 环境检测 ----------
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64 | aarch64) ;;
  *)
    echo "[错误] 仅支持 x86_64 / aarch64（2025.12 起 32 位已 EOL）。当前: $ARCH"
    exit 1
    ;;
esac

# 重跑场景：若已有 .env，加载自定义值（首次运行文件不存在，跳过）
if [ -f .env ]; then
  set -a; . ./.env; set +a
fi

# ---------- ② 装 Docker ----------
# Docker Engine 23.0+ 是硬性前置（官方明确 Docker Desktop 不可用）
if ! command -v docker >/dev/null 2>&1; then
  echo "[步骤2] 未检测到 Docker，开始安装..."
  curl -fsSL https://get.docker.com --mirror Aliyun | sh \
    || curl -fsSL https://get.daocloud.io/docker | sh
else
  echo "[步骤2] Docker 已安装，跳过。"
fi

# ---------- ③ 写 daemon.json（只加速 Docker Hub） ----------
echo "[步骤3] 写入 Docker Hub 加速配置..."
mkdir -p /etc/docker
cat > /etc/docker/daemon.json <<'EOF'
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.m.daocloud.io",
    "https://docker.1panel.live"
  ]
}
EOF
# systemd 主机重启 docker 使配置生效；非 systemd 环境忽略
systemctl restart docker 2>/dev/null || true

# ---------- ④ ghcr 回退链（整体替换镜像名前缀，而非 registry-mirrors） ----------
pull_with_fallback() {
  local original="$1"      # 形如 ghcr.io/home-assistant/home-assistant:stable
  local name="${original#ghcr.io/}"
  local mirrors=(
    "ghcr.nju.edu.cn"              # 高校公益，优先教育网
    "docker.m.daocloud.io/ghcr.io" # DaoCloud 反代
    "ghcr.1ms.run"                 # 社区 ghcr 代理
    ""                             # 空 = 官方直连兜底
    "ota.hasscn.top"               # HAOS-CN，限大陆，放末位
  )
  for prefix in "${mirrors[@]}"; do
    local candidate
    if [ -n "$prefix" ]; then
      candidate="${prefix}/${name}"   # 关键：整体替换镜像名前缀
    else
      candidate="$original"
    fi
    echo "  尝试拉取: $candidate"
    # timeout 300：单源最多等 5 分钟，失败自动切下一跳
    if timeout 300 docker pull "$candidate"; then
      # 统一 tag 回原始名，后续 compose 无需关心实际来源
      docker tag "$candidate" "$original"
      return 0
    fi
  done
  echo "[错误] 所有镜像源均失败，请检查网络后重试。"
  return 1
}

echo "[步骤4] 拉取 HA 镜像..."
pull_with_fallback "${HA_IMAGE:-ghcr.io/home-assistant/home-assistant:stable}"

# ---------- ⑤ 交互写 .env（仅在不存在时执行，保证幂等） ----------
if [ ! -f .env ]; then
  echo "[步骤5] 生成 .env ..."
  read -rp "  时区（默认 Asia/Shanghai）: " TZ_INPUT
  TZ="${TZ_INPUT:-Asia/Shanghai}"
  read -rsp "  DeepSeek API Key（输入不回显）: " DEEPSEEK_KEY
  echo
  cat > .env <<EOF
TZ=$TZ
DEEPSEEK_API_KEY=$DEEPSEEK_KEY
HA_IMAGE=${HA_IMAGE:-ghcr.io/home-assistant/home-assistant:stable}
AGENT_IMAGE=${AGENT_IMAGE:-registry.example.com/ha-agent:latest}
EOF
fi
# .env 含密钥，只允许属主读写
chmod 600 .env
# 防呆：.env 存在但 Key 为空则中止
if grep -q '^DEEPSEEK_API_KEY=$' .env; then
  echo "[错误] .env 中 DEEPSEEK_API_KEY 为空，请补全后重跑。"
  exit 1
fi

# ---------- ⑥ 写 compose + up -d（幂等，重复执行收敛到同一状态） ----------
echo "[步骤6] 生成 docker-compose.yml 并启动..."
cat > docker-compose.yml <<'EOF'
services:
  homeassistant:
    image: ${HA_IMAGE}
    container_name: homeassistant
    restart: unless-stopped
    network_mode: host
    privileged: false            # 仅在需要 USB / Zigbee 时设为 true
    environment:
      TZ: ${TZ}
    volumes:
      - ./config:/config
      - /run/dbus:/run/dbus:ro
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request,sys; r=urllib.request.urlopen('http://127.0.0.1:8123/', timeout=5); sys.exit(0 if r.status == 200 else 1)"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 300s

  agent:
    image: ${AGENT_IMAGE}
    container_name: ha-agent
    restart: unless-stopped
    network_mode: host
    environment:
      TZ: ${TZ}
      HA_BASE_URL: http://127.0.0.1:8123
      DEEPSEEK_API_KEY: ${DEEPSEEK_API_KEY}
    depends_on:
      homeassistant:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request,sys; r=urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5); sys.exit(0 if r.status == 200 else 1)"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s
EOF

docker compose up -d

# ---------- ⑦ 等待就绪（接受 200/302，首次启动可能 5-10 分钟） ----------
echo "[步骤7] 等待 Home Assistant 就绪（首次启动较慢）..."
READY=0
for _ in $(seq 1 120); do
  # 接受 200（已 onboarded）与 302（尚未 onboarding，前端已起来）
  CODE="$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8123/ || true)"
  if [ "$CODE" = "200" ] || [ "$CODE" = "302" ]; then
    READY=1
    echo "  就绪（HTTP $CODE）"
    break
  fi
  sleep 5
done
if [ "$READY" != "1" ]; then
  echo "[警告] 120 次探测仍未就绪，请手动访问 http://127.0.0.1:8123/ 检查。"
fi

# ---------- ⑧ 打印访问地址 ----------
IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
echo "=============================================="
echo " Home Assistant: http://${IP:-127.0.0.1}:8123"
echo " Agent 文档:     http://127.0.0.1:8000/docs"
echo " 配置目录:       $(pwd)/config"
echo "=============================================="
```

下面按步骤看每一段为什么这么写。

#### 3.1.1 ① 环境检测：先把不可能的环境挡在门外

脚本第一件事不是动手，而是先看这台机器值不值得装。`set -euo pipefail` 让任何一条命令失败就立即退出，避免「装了一半才发现前面有问题」。架构检查用 `uname -m` 拒绝 `i386 / armhf / armv7`——2025.12 起 HA 官方只支持 x86_64 / aarch64，在这类老设备上硬装只会得到一堆看不懂的错误。

#### 3.1.2 ② 装 Docker：一个命令，两个镜像源

`curl -fsSL https://get.docker.com --mirror Aliyun | sh` 是 Docker 官方安装脚本，`--mirror Aliyun` 让它走阿里云镜像；如果这一条失败（阿里云不可达），用 `||` 回退到 `https://get.daocloud.io/docker`。注意这里是「安装脚本本身」的国内加速，和第 ③ 步的「镜像下载加速」是两件事。

#### 3.1.3 ③ 写 daemon.json：只解决 Docker Hub

`registry-mirrors` 只对 Docker Hub 生效，对 `ghcr.io` 完全无效（这是第 2 章的核心认知，脚本里用注释再强调一次）。它解决的是后续所有「从 Docker Hub 拉公共镜像」的加速；ghcr 的 HA 镜像不归它管，交给第 ④ 步。

#### 3.1.4 ④ pull_with_fallback：整体替换镜像名前缀

这是脚本里含金量最高的一段。核心写法是 `candidate="${prefix}/${name}"`，即把 `ghcr.io/home-assistant/home-assistant:stable` 的 `ghcr.io/` 前缀整段换掉，得到 `ghcr.nju.edu.cn/home-assistant/home-assistant:stable`，而不是去配 daemon.json。每个候选源用 `timeout 300 docker pull` 包裹：源挂起 5 分钟自动判失败、切下一跳，不会卡死整条脚本。拉成功后 `docker tag` 回原始名，这样第 ⑥ 步的 compose 永远只写规范名，不关心镜像实际从哪来。回退链顺序与实测优先级一致：`ghcr.nju.edu.cn` → `docker.m.daocloud.io/ghcr.io` → `ghcr.1ms.run` → 官方直连兜底 → `ota.hasscn.top`（限大陆，放末位）。

#### 3.1.5 ⑤ 交互写 .env：一次输入，之后不打扰

只在 `.env` 不存在时才进入交互，避免重跑时覆盖已填好的 Key。`read -rsp` 让 API Key 输入不回显，防止有人站在身后看到密钥。写完立刻 `chmod 600 .env`，并且用 `grep` 防呆——Key 为空就中止，不留一个「看起来装好了其实不能用」的半成品。为什么四个变量就够：`TZ` 定时区、`DEEPSEEK_API_KEY` 给 Agent 用、`HA_IMAGE` / `AGENT_IMAGE` 定两个镜像。

#### 3.1.6 ⑥ 写 compose + up -d：一条命令拉起两个容器

compose 文件用 heredoc 在脚本里现场生成，好处是仓库只需分发一个 `install.sh`，客户不会拿到「脚本和文件不同步」的版本。`docker compose up -d`（v2 插件，带空格）本身是幂等的——重复执行会收敛到目标状态，不会重复创建容器。两个容器如何协作见 3.2。

#### 3.1.7 ⑦ 等待就绪：接受 200，也接受 302

首次启动 HA 要创建配置目录、初始化 `.storage`，冷启动 5-10 分钟很正常。探测 `/` 时 302 表示「前端已经起来但还没完成 onboarding 向导」，200 表示「已经 onboarding 完」，两者都算就绪；只有连接拒绝才继续等。循环 120 次 × 5 秒 = 上限 600 秒，对应素材里「超时 ≥600s」的要求。

#### 3.1.8 ⑧ 打印访问地址：把结果交给用户

用 `hostname -I` 取主机的局域网 IP，输出 HA 和 Agent 两个入口。对非技术用户，这一步是他们唯一需要看的信息；`/config` 目录路径也打出来，方便后续排错。

### 3.2 docker-compose.yml 关键配置

install.sh 只是编排者，真正决定两个容器怎么跑的是 compose 文件。先看全貌（即 3.1 脚本第 ⑥ 步写入的同一份）：

```yaml
services:
  homeassistant:
    image: ${HA_IMAGE}
    container_name: homeassistant
    restart: unless-stopped
    network_mode: host
    privileged: false
    environment:
      TZ: ${TZ}
    volumes:
      - ./config:/config
      - /run/dbus:/run/dbus:ro
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request,sys; r=urllib.request.urlopen('http://127.0.0.1:8123/', timeout=5); sys.exit(0 if r.status == 200 else 1)"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 300s

  agent:
    image: ${AGENT_IMAGE}
    container_name: ha-agent
    restart: unless-stopped
    network_mode: host
    environment:
      TZ: ${TZ}
      HA_BASE_URL: http://127.0.0.1:8123
      DEEPSEEK_API_KEY: ${DEEPSEEK_API_KEY}
    depends_on:
      homeassistant:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request,sys; r=urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5); sys.exit(0 if r.status == 200 else 1)"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s
```

关键字段逐个说：

| 字段 | 值 | 为什么 |
|------|-----|--------|
| `image: ${HA_IMAGE}` | 从 .env 取 | 镜像来源由 install.sh 的镜像链决定，compose 只写规范名 |
| `network_mode: host` | host | 官方推荐；mDNS / SSDP 设备发现依赖宿主机网络 |
| `privileged: false` | 默认关 | 仅在需要 USB / Zigbee 设备时才开，纯云 MVP 保持关 |
| `environment: TZ: ${TZ}` | 显式时区 | HA 不会自动读宿主时区，`TZ=Asia/Shanghai` 必须显式 |
| `./config:/config` | 配置卷 | HA 的 `configuration.yaml`、`.storage`、custom_components 都落在这里 |
| `/run/dbus:/run/dbus:ro` | 只读挂载 | 供部分集成（如 Bluetooth、某些 mDNS）使用宿主 dbus |
| `depends_on: condition: service_healthy` | 依赖健康 | Agent 必须等 HA 完全就绪再启动，否则首次调用直接连不上 |

Agent sidecar 的 `HA_BASE_URL=http://127.0.0.1:8123` 之所以能用 127.0.0.1，正是因为 `network_mode: host`——两个容器共享宿主机网络栈，Agent 通过 localhost 就能访问 HA 的 REST API。这也是 host 网络除了设备发现之外的第二个好处。

### 3.3 healthcheck 的无 curl 方案

这是最容易踩的一颗雷：**HA 官方容器镜像里没有 curl**（镜像基于精简 Debian，只带 Python 运行环境）。如果你按习惯写 `test: ["CMD", "curl", "-f", "http://127.0.0.1:8123"]`，healthcheck 会直接报 `executable file not found`，容器永远不健康，于是 `depends_on: condition: service_healthy` 会把 Agent 永远堵在启动阶段——表面上两个容器都在，实际上 Agent 一直在等。

解法是用镜像里一定存在的 `python3` + `urllib` 探测：

```text
test: ["CMD", "python3", "-c",
  "import urllib.request,sys; r=urllib.request.urlopen('http://127.0.0.1:8123/', timeout=5); sys.exit(0 if r.status == 200 else 1)"]
```

两点要理解：

- `urllib.request.urlopen` 默认会跟随 302 重定向。HA 未 onboarding 时访问 `/` 返回 302，urlopen 会追到 onboarding 页面拿到 200，所以「在线但未向导」和「已就绪」在这里都表现为 `status == 200`，判断成立。这也让 `r.status in (200, 302)` 的写法被简化成只看 200。
- `start_period: 300s` 告诉 compose 前 300 秒内的失败不计入失败重试——冷启动期的异常回滚请求会抛异常、返回非零退出码，这恰恰是「还没好」的正确信号，但 `start_period` 让这段时间的失败不直接判死容器。

Agent 的 healthcheck 同理，但探测的是自己的 `:8000/health`，且 `start_period: 60s`（Python 进程启动比 HA 快得多）。

### 3.4 .env 交互与敏感信息保护

`.env` 是全系统唯一的密钥存放处，模板如下（install.sh 第 ⑤ 步自动生成）：

```bash
# 时区：默认 Asia/Shanghai，中国大陆用户通常不需要改
TZ=Asia/Shanghai

# DeepSeek API Key：必填，来自 platform.deepseek.com
DEEPSEEK_API_KEY=

# HA 官方镜像：install.sh 已用回退链拉好并 tag 回规范名
HA_IMAGE=ghcr.io/home-assistant/home-assistant:stable

# Agent 镜像：产品自有镜像，若在 ACR 个人版需先 docker login
AGENT_IMAGE=registry.example.com/ha-agent:latest
```

保护措施一共四道：

1. **`chmod 600`**——写完后立刻收紧权限，只有属主能读写。系统里其他用户（以及任何以低权限跑的进程）读不到 API Key。
2. **不入库**——`.env` 必须进 `.gitignore`。项目仓库里只放 `.env.example`（占位值），真实 Key 只存在于客户机器上。同理，运行期 `./config/` 里会积累设备 token、网关 key、集成凭据，也应一起 ignore，绝不上传。
3. **幂等防覆盖**——install.sh 只在 `.env` 不存在时写入，重跑不会用空值覆盖已填的 Key；且启动前校验 Key 非空。
4. **compose 自动加载**——`docker compose` 会默认读取项目目录的 `.env` 做变量插值，所以 compose 里直接写 `${DEEPSEEK_API_KEY}`，Key 只进容器环境变量、不进镜像、不进日志。

这套设计的直接收益是：整个部署过程，非技术用户只需要在第一次运行时输入一个 API Key，之后所有重跑、升级都不再需要碰密钥。

### 3.5 常见坑与排错

- **以为配了 daemon.json 就能拉 ghcr**：`registry-mirrors` 只对 Docker Hub 生效。HA 镜像拉不动，必须走 3.1.4 的「整体替换镜像名前缀」，这是第 2 章认知在脚本里的落地。
- **没给 pull 加 timeout**：官方 ghcr 直连在大陆会长时间挂起。没有 `timeout 300`，脚本就停在「正在拉取」；加上了，才会 5 分钟自动切下一跳。
- **首次启动很慢被误判为失败**：HA 冷启动 5-10 分钟。healthcheck 要配 `start_period`，install.sh 的就绪探测上限要 ≥600s，否则用户会以为装坏了。
- **compose 版本不兼容**：用 v2 插件 `docker compose`（带空格），不要用 v1 的 `docker-compose`。`depends_on: condition: service_healthy` 在 v1 上不被支持；且现代 compose 不需要顶层的 `version:` 键。Docker Engine 23.0+ 默认自带 v2，这正是第 1 章「Docker Engine 23.0+」前置的又一重原因。
- **healthcheck 写了 curl**：HA 镜像没有 curl，healthcheck 会一直失败并连带卡住 Agent。改用 `python3 urllib`，见 3.3。
- **Agent 镜像拉不下来**：回退链只覆盖公共的 HA ghcr 镜像。产品自有 agent 镜像若放在阿里云 ACR 个人版，新实例不支持匿名拉取，必须先 `docker login`，再 `docker compose up -d`。
- **`privileged` 随手开**：`privileged: true` 等于把宿主机绝大部分权限交给容器。纯云 MVP 保持 `false`，只有接了 USB 协调器 / Zigbee 设备时才开。

> [!note] 「就绪」≠「能用了」
> install.sh 第 ⑦ 步探测到的 302，恰恰说明 HA 还停在浏览器 onboarding 向导——服务起来了，但离「非技术用户 5 分钟承诺」还差一步：让首次启动不需要浏览器。这是第 4 章的主题。

### 本章小结

- install.sh = 8 步确定动作（环境检测 → 装 Docker → daemon.json → 回退链拉镜像 → 写 .env → compose up → 等就绪 → 打印地址），每一步幂等可重跑。
- ghcr 拉不动的解法是 `pull_with_fallback` 整体替换镜像名前缀 + 每跳 `timeout 300`，不是配 registry-mirrors。
- compose 用 `network_mode: host` + `depends_on: condition: service_healthy` 让 HA 与 Agent 在同一网络栈协作，Agent 通过 `http://127.0.0.1:8123` 访问 HA。
- HA 官方镜像无 curl，healthcheck 用 `python3 urllib` 探测 8123 / 8000，配合 `start_period` 容忍冷启动。
- `.env` 用 `chmod 600` + gitignore + 幂等写入 + compose 自动加载四道保护，全系统唯一的密钥存放点。
- 就绪探测接受 200/302，但「服务起来」≠「完成 onboarding」，后者交给下一章。

---

下一章解决「服务起来了但还差临门一脚」的问题：install.sh 探测到的那条 302 重定向，说明 HA 正在等着用户用浏览器完成首次向导。要让「一条命令部署」对非技术用户真正成立，就得把这个向导也自动化——无头 onboarding 就是第 4 章的主题。
