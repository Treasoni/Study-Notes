---
title: "第三章 一键交付：预建镜像 / 盒子 / Add-on"
type: chapter
chapter: 3
tags:
  - Home-Assistant
  - Docker
  - Docker-Compose
  - 一键部署
created: 2026-08-05
updated: 2026-08-06
status: 已完成
source_project: ai-smart-home-system
---

# 第三章 一键交付：预建镜像 / 盒子 / Add-on

> 笔记类型：实战构建指南（practice）｜学习深度：精通
> 素材来源：深度收集 §2、§7（#4）
> 前置关联：第 2 章（国内镜像链与 Docker 基础设施准备）

> [!summary] 本章回答三个问题
> 1. 为什么 HAOS 的「一键交付」本质是预建镜像 / 盒子，而不是脚本？
> 2. 交付一台 HAOS 主机（VM / 盒子）的硬性要求是什么，UEFI 为什么躲不掉？
> 3. Agent 的「一键装」如何打包成自定义 Add-on，让用户在 HA 里点一下就能装？

第 2 章解决了国内网络下镜像拉不动的卡点，但那套思路默认的前提是「客户自己有一台 Linux + Docker 主机」。对非技术用户来说，「先装系统、再装 Docker、再跑脚本」本身就是不可逾越的门槛。这一章换一个交付视角：HAOS 官方早就把「一键」做进了产品形态——用户拿到的是一个预建镜像或预刷好的盒子，动作只有「导入（或插电）→ 开机 → 首次引导」；Agent 的「一键装」则打包成自定义 Add-on，在 HA 的界面里点一下就能装。install.sh + docker-compose 不是被否定，而是降级为 Container 次级渠道，只对已经持有 Docker 主机的用户保留。

## 3.1 先转变认知：HAOS 的「一键交付」= 预建镜像 / 盒子

「一键」的本质是交付形态，不是脚本。脚本再顺，也要求用户先有一台能跑 Docker 的主机；而 HAOS 把整台系统直接做成镜像 / 盒子交付，装机、装驱动、装 Docker、配 Supervisor 全部发生在出厂前或镜像里，用户端不出现命令行。

### 3.1.1 三种交付形态对比

| 交付形态 | 用户拿到什么 | 用户动作 | 适合谁 |
|----------|-------------|----------|--------|
| 预建镜像 / 盒子（HAOS） | ova / qcow2 / vdi / vmdk / vhdx，或预刷好的 SBC / x86 盒子 | 导入（或插电）→ 开机 → 首次引导 | 绝大多数非技术用户 |
| 自定义 Add-on（Agent） | HA Add-on Store 里一个可添加的仓库 | 加仓库 → 点安装 → 填 .env | 已经跑在 HA 上的用户 |
| Container（install.sh + compose） | 一个 install.sh + 一份 docker-compose.yml | 装 Docker → 跑脚本 → 填 Key | 已经持有 Docker 主机的用户 |

### 3.1.2 硬件门槛：2GB / 2 vCPU / 32GB 起步

HAOS 对硬件的底线低但明确：最低 2GB 内存 / 2 vCPU / 32GB 存储，推荐 4GB 内存。存储建议 SSD，32GB 是装上基本系统后的安全余量。镜像交付的另一层收益是升级自动化：Supervisor 负责自动更新与快照，升级是平台能力，不需要用户维护脚本或重装系统。

### 3.1.3 UEFI 是躲不掉的门槛

HAOS 只支持 UEFI 引导，这是建 VM 时最容易翻车的一条。VirtualBox 需要在虚拟机设置里勾选「Use EFI」；KVM / Proxmox 使用非 secureboot 的 OVMF 固件（不要开 Secure Boot）。镜像格式按平台选：VirtualBox 用 vdi / ova，VMware 用 vmdk，Hyper-V 用 vhdx，KVM / Proxmox 用 qcow2。格式选错或固件不对，开机只会看到黑屏或引导失败，而不是一个可用的 HAOS。

## 3.2 主路径 A：预建镜像 / 盒子（导入 → 开机 → 首次引导）

交付 HAOS 有两条子路径，取决于客户手里有没有虚拟化平台；无论哪条，客户侧的三个动作都一样：导入（或插电）→ 开机 → 首次引导。

### 3.2.1 有虚拟化平台：导入官方镜像

从 Home Assistant 官网 Installation 页下载对应平台的镜像（VirtualBox 的 ova / vdi，KVM / Proxmox 的 qcow2 等），导入后按 3.1.3 配置 UEFI，开机即进入 HAOS 首次引导。对客户来说，这步等价于「装一个虚拟机」，全程没有命令行。OVA 包尤其适合新手：它把虚拟机配置、磁盘、固件设置打在一起，导入后通常只需确认 UEFI 已启用。

### 3.2.2 Proxmox：一条社区命令建好 VM

如果交付目标平台是 Proxmox，社区提供了一键建 VM 脚本，本质是把「下载 qcow2 + 建 VM + 配 OVMF 固件」固化成一条命令：

```bash
bash -c "$(wget -qO - https://github.com/community-scripts/ProxmoxVE/raw/main/vm/haos-vm.sh)"
```

脚本执行完，Proxmox 里就多了一台已配好 UEFI 与磁盘的 HAOS 虚拟机，用户只需开机走首次引导。注意这条命令建立的是「VM 环境」的一键，HAOS 本身的一键仍然在预建镜像里。

### 3.2.3 没有虚拟化平台：预刷主机 / 盒子

对完全没有服务器概念的客户，交付一台预刷好 HAOS 的 SBC 或 x86 盒子是最省事的形式：插电 → 开机 → 首次引导。HAOS 支持 x86-64 与多种 SBC，把官方镜像刷进 SD 卡或 eMMC，插上交给客户即可。这一步的「一键」发生在交付前、在供应商一侧，客户侧只剩开机。

### 3.2.4 首次引导 = onboarding 向导

无论哪种形态，开机后都是同一个画面：浏览器打开 onboarding 向导，创建账号、设时区、给房子起名。这和 3.4 里 install.sh 探测到 302 是同一件事——HA 服务起来了，但离「非技术用户 5 分钟承诺」还差一个向导。让这个向导自动化（无头 onboarding），是第 4 章的主题。

## 3.3 主路径 B：Agent 的一键装 = 自定义 Add-on

HAOS 交付完成后，Agent 怎么「一键装」？答案不是分发脚本，而是把它打包成一个自定义 Add-on，放进 HA 的 Add-on Store。

### 3.3.1 Add-on 的三件套

一个 Add-on 就是一个目录，至少包含三个文件：

| 文件 | 作用 |
|------|------|
| `config.json` | Add-on 元信息：名称、版本、支持的架构、启动方式、选项（options）与 schema，决定 Add-on Store 如何展示、安装时让用户填什么 |
| `Dockerfile` | 把 Agent 代码构建成镜像，声明运行环境与启动命令 |
| `run.sh` | 容器启动入口，读取配置、拉起 Agent 进程 |

整个目录托管在一个 Git 仓库里。用户拿到仓库地址后，在 HA 的「设置 → 加载项 → 加载项商店 → 右上角 ⋮ → 仓库」添加这个仓库，Add-on Store 里就会出现你的 Agent。

### 3.3.2 一键安装 → 填 .env（HA token / DeepSeek key）

用户点「安装」后，HA 读取 `config.json` 里的 `options` 与 `schema`，在 Add-on 的「配置」页生成一个表单，让用户填两个值：HA 的长效访问令牌（token）和 DeepSeek API Key。安装本身是点一下的事，剩下的都是表单，全程无命令行。`config.json` 大致长这样：

```json
{
  "name": "HA Agent",
  "version": "1.0.0",
  "slug": "ha_agent",
  "description": "跨品牌 AI 智能家居 Agent",
  "arch": ["aarch64", "amd64"],
  "startup": "application",
  "boot": "auto",
  "options": {
    "deepseek_api_key": "",
    "ha_token": ""
  },
  "schema": {
    "deepseek_api_key": "str",
    "ha_token": "str"
  }
}
```

Add-on 的选项最终以环境变量的形式注入 run.sh 所在容器，等价于 install.sh 第 ⑤ 步生成的 `.env`，只是填写界面从命令行换成了表单。HA 长效令牌需要在「个人资料 → 安全 → 长期访问令牌」里生成，这个值和 DeepSeek Key 一样属于敏感信息，只存在 Add-on 配置里。

### 3.3.3 为什么对非技术用户成立

Add-on 路径的三次点击（加仓库 → 安装 → 填表单）全部发生在 HA 的图形界面里。HAOS 已预装运行环境，Add-on 镜像由 HA 拉取并纳入 Supervisor 管理——升级、开机自启、日志查看都由平台接管，用户不需要维护脚本或重启容器。这是「一键交付」对非技术用户最完整的一步，也是产品化交付时 Agent 侧应优先走的路。

## 3.4 次级渠道：Container（install.sh + docker-compose）

> [!warning] 本渠道已降级为次级
> 预建镜像 / 盒子与 Add-on 是主交付路径。install.sh + docker-compose 仅适用于**已经持有 Docker 主机的用户**——他们不想要整台 HAOS 虚拟机，只想在现有 Docker 环境里把 HA 与 Agent 跑起来。本章保留这部分内容，因为理解容器里 HA 与 Agent 的协作关系、以及无 HAOS 环境下的快速试用，仍然用得上。

### 3.4.1 install.sh 逐段拆解（8 个步骤）

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

完整脚本骨架如下（深度收集 §2 的 install.sh 骨架逐行落地，含注释）：

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

**① 环境检测：先把不可能的环境挡在门外**

脚本第一件事不是动手，而是先看这台机器值不值得装。`set -euo pipefail` 让任何一条命令失败就立即退出，避免「装了一半才发现前面有问题」。架构检查用 `uname -m` 拒绝 `i386 / armhf / armv7`——2025.12 起 HA 官方只支持 x86_64 / aarch64，在这类老设备上硬装只会得到一堆看不懂的错误。

**② 装 Docker：一个命令，两个镜像源**

`curl -fsSL https://get.docker.com --mirror Aliyun | sh` 是 Docker 官方安装脚本，`--mirror Aliyun` 让它走阿里云镜像；如果这一条失败（阿里云不可达），用 `||` 回退到 `https://get.daocloud.io/docker`。注意这里是「安装脚本本身」的国内加速，和第 ③ 步的「镜像下载加速」是两件事。

**③ 写 daemon.json：只解决 Docker Hub**

`registry-mirrors` 只对 Docker Hub 生效，对 `ghcr.io` 完全无效（这是第 2 章的核心认知，脚本里用注释再强调一次）。它解决的是后续所有「从 Docker Hub 拉公共镜像」的加速；ghcr 的 HA 镜像不归它管，交给第 ④ 步。

**④ pull_with_fallback：整体替换镜像名前缀**

这是脚本里含金量最高的一段。核心写法是 `candidate="${prefix}/${name}"`，即把 `ghcr.io/home-assistant/home-assistant:stable` 的 `ghcr.io/` 前缀整段换掉，得到 `ghcr.nju.edu.cn/home-assistant/home-assistant:stable`，而不是去配 daemon.json。每个候选源用 `timeout 300 docker pull` 包裹：源挂起 5 分钟自动判失败、切下一跳，不会卡死整条脚本。拉成功后 `docker tag` 回原始名，这样第 ⑥ 步的 compose 永远只写规范名，不关心镜像实际从哪来。回退链顺序与实测优先级一致：`ghcr.nju.edu.cn` → `docker.m.daocloud.io/ghcr.io` → `ghcr.1ms.run` → 官方直连兜底 → `ota.hasscn.top`（限大陆，放末位）。

**⑤ 交互写 .env：一次输入，之后不打扰**

只在 `.env` 不存在时才进入交互，避免重跑时覆盖已填好的 Key。`read -rsp` 让 API Key 输入不回显，防止有人站在身后看到密钥。写完立刻 `chmod 600 .env`，并且用 `grep` 防呆——Key 为空就中止，不留一个「看起来装好了其实不能用」的半成品。为什么四个变量就够：`TZ` 定时区、`DEEPSEEK_API_KEY` 给 Agent 用、`HA_IMAGE` / `AGENT_IMAGE` 定两个镜像。

**⑥ 写 compose + up -d：一条命令拉起两个容器**

compose 文件用 heredoc 在脚本里现场生成，好处是仓库只需分发一个 `install.sh`，客户不会拿到「脚本和文件不同步」的版本。`docker compose up -d`（v2 插件，带空格）本身是幂等的——重复执行会收敛到目标状态，不会重复创建容器。两个容器如何协作见 3.4.2。

**⑦ 等待就绪：接受 200，也接受 302**

首次启动 HA 要创建配置目录、初始化 `.storage`，冷启动 5-10 分钟很正常。探测 `/` 时 302 表示「前端已经起来但还没完成 onboarding 向导」，200 表示「已经 onboarding 完」，两者都算就绪；只有连接拒绝才继续等。循环 120 次 × 5 秒 = 上限 600 秒，对应素材里「超时 ≥600s」的要求。

**⑧ 打印访问地址：把结果交给用户**

用 `hostname -I` 取主机的局域网 IP，输出 HA 和 Agent 两个入口。对非技术用户，这一步是他们唯一需要看的信息；`/config` 目录路径也打出来，方便后续排错。

### 3.4.2 docker-compose.yml 关键配置

install.sh 只是编排者，真正决定两个容器怎么跑的是 compose 文件。先看全貌（即 3.4.1 脚本第 ⑥ 步写入的同一份）：

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

### 3.4.3 healthcheck 的无 curl 方案

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

### 3.4.4 .env 交互与敏感信息保护

`.env` 是 Container 渠道全系统唯一的密钥存放处，模板如下（install.sh 第 ⑤ 步自动生成）：

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

这套设计的直接收益是：整个部署过程，非技术用户只需要在第一次运行时输入一个 API Key，之后所有重跑、升级都不再需要碰密钥。Add-on 渠道的 `.env` 等价物就是 3.3.2 的选项表单，同样的密钥保护诉求由 HA 的凭据存储承担。

## 3.5 常见坑与排错

主路径（HAOS 预建镜像 / 盒子 / Add-on）：

- **建 VM 忘开 UEFI**：HAOS 只支持 UEFI。VirtualBox 没勾 Use EFI、Proxmox 用了 SeaBIOS 或开了 Secure Boot，开机就是黑屏或引导失败。先检查固件，再怀疑镜像。
- **镜像格式不匹配**：vdi / vmdk / vhdx / qcow2 按平台选，ova 是打包好的更省事。格式选错或位数不匹配，导入时会直接报错。
- **磁盘给得太小**：低于 32GB 会让 Supervisor 在后续更新时空间告急。给足 32GB、推荐 SSD，避免「能开机但装不了几个 Add-on」。
- **Add-on 仓库添加失败 / 装完不出现**：确认仓库地址是 Git 仓库根目录（包含 `config.json` 所在目录），且 `config.json` 里 `slug` 唯一、`arch` 包含目标机架构（aarch64 / amd64）。
- **HA token 没用「长期访问令牌」**：普通登录态短令牌不能持久供 Add-on 调用，需在「个人资料 → 安全 → 长期访问令牌」生成并填入。

次级渠道（Container）：

- **以为配了 daemon.json 就能拉 ghcr**：`registry-mirrors` 只对 Docker Hub 生效。HA 镜像拉不动，必须走 3.4.1 ④ 的「整体替换镜像名前缀」，这是第 2 章认知在脚本里的落地。
- **没给 pull 加 timeout**：官方 ghcr 直连在大陆会长时间挂起。没有 `timeout 300`，脚本就停在「正在拉取」；加上了，才会 5 分钟自动切下一跳。
- **首次启动很慢被误判为失败**：HA 冷启动 5-10 分钟。healthcheck 要配 `start_period`，install.sh 的就绪探测上限要 ≥600s，否则用户会以为装坏了。
- **compose 版本不兼容**：用 v2 插件 `docker compose`（带空格），不要用 v1 的 `docker-compose`。`depends_on: condition: service_healthy` 在 v1 上不被支持；且现代 compose 不需要顶层的 `version:` 键。Docker Engine 23.0+ 默认自带 v2，这正是第 1 章「Docker Engine 23.0+」前置的又一重原因。
- **healthcheck 写了 curl**：HA 镜像没有 curl，healthcheck 会一直失败并连带卡住 Agent。改用 `python3 urllib`，见 3.4.3。
- **Agent 镜像拉不下来**：回退链只覆盖公共的 HA ghcr 镜像。产品自有 agent 镜像若放在阿里云 ACR 个人版，新实例不支持匿名拉取，必须先 `docker login`，再 `docker compose up -d`。
- **`privileged` 随手开**：`privileged: true` 等于把宿主机绝大部分权限交给容器。纯云 MVP 保持 `false`，只有接了 USB 协调器 / Zigbee 设备时才开。

> [!note] 「就绪」≠「能用了」
> 主路径的首次引导、次级渠道探测到的 302，指的都是同一件事：HA 服务起来了，但还停在浏览器 onboarding 向导——离「非技术用户 5 分钟承诺」还差一步。让首次启动不需要浏览器，是第 4 章的主题。

## 本章小结

- HAOS 的「一键交付」本质是预建镜像 / 盒子，不是脚本：用户动作只有「导入（或插电）→ 开机 → 首次引导」，装机、装 Docker、配 Supervisor 全在交付前完成。
- 建 HAOS VM 的硬性门槛是 UEFI：VirtualBox 勾 Use EFI，KVM / Proxmox 用非 secureboot 的 OVMF；镜像格式按平台选 qcow2 / vdi / vmdk / vhdx。Proxmox 可用社区一键脚本 `bash -c "$(wget -qO - https://github.com/community-scripts/ProxmoxVE/raw/main/vm/haos-vm.sh)"`。
- Agent 的「一键装」= 自定义 Add-on：config.json + Dockerfile + run.sh 托管在 Git 仓库，用户在 Add-on Store 加仓库 → 一键安装 → 填 .env（HA 长期访问令牌 / DeepSeek Key）。
- 硬件最低 2GB / 2 vCPU / 32GB、推荐 4GB；Supervisor 自动更新 + 快照，升级是平台能力而非用户负担。
- install.sh + docker-compose 降级为 Container 次级渠道，仅适用于已有 Docker 主机的用户；其核心知识（ghcr 回退链、host 网络、无 curl 的 healthcheck、.env 四道保护）仍然成立。
- 首次引导 = onboarding 向导，自动化留给第 4 章。

---

下一章解决「服务起来了但还差临门一脚」的问题：无论是主路径的首次引导，还是次级渠道探测到的那条 302，都说明 HA 正等着用户用浏览器完成向导。要让「一键交付」对非技术用户真正成立，就得把这个向导也自动化——无头 onboarding 就是第 4 章的主题。

---

> [[02_国内镜像链与Docker基础设施|⬅ 第二章]] · [[基于 Home Assistant 的跨品牌 AI 智能家居一键部署系统|返回索引]] · [[04_无头onboarding自动化|第四章 ➡]]
