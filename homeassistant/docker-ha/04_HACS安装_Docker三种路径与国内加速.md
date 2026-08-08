---
title: "第四章：HACS 安装 —— Docker 三种路径与国内加速"
tags:
  - Home-Assistant
  - Docker
  - HACS
  - 智能家居
  - 运维
  - 实战教程
created: 2026-08-08
updated: 2026-08-08
status: 已完成
source_project: docker-ha-tutorial
chapter: 四
---

# 第四章：HACS 安装 —— Docker 三种路径与国内加速

[[03_工程化部署_docker-compose完整配置与三大关键决策.md|← 第三章 · 工程化部署]] ｜ [[05_HACS首次配置与常用仓库实战.md|第五章 · HACS 配置 →]]

[[Docker 部署 Home Assistant 完全指南|← 返回索引]]

第三章我们用 docker-compose 把 HA 本体稳稳跑起来了。但这时的 HA 还是个「空房子」——没有米家、没有好看的前端卡片、没有丰富的自定义集成。这一章我们装 HACS，把社区生态请进来，并重点解决国内网络下「怎么把 HACS 下载下来」这个现实问题。

### 4.1 HACS 是什么，为什么 Docker 版要手动装

> [!tip] 大白话
> HACS 可以想成「手机应用商店」。HA 官方自带的功能像系统预装 App，而米家、影音卡片、各种主题都是第三方 App——HACS 就是那个让你能发现、下载、更新这些第三方 App 的应用商店。[HACS 官方文档](https://hacs.xyz)

HACS（Home Assistant Community Store）是 HA 社区最重要的生态入口，装三类东西：集成（integrations，如小米 Miot）、前端卡片（lovelace cards，如 Mushroom）、主题（themes）。Docker 版没有 Supervisor，也就没有「应用商店」的安装器，所以 HACS 需要我们自己动手放进去。

> [!tip] 大白话
> 为什么 Docker 版要手动放文件？想成「从安装包装 App」：HAOS 有应用商店自动下载安装，Docker 版没有商店，你得自己把 App 的安装包（hacs.zip）解压到指定目录，再重启让 HA 加载它。

### 4.2 官方脚本 get.hacs.xyz 在做什么

官方安装脚本的核心是一条命令 `wget -O - https://get.hacs.xyz | bash -`，它一共干 6 件事：

1. 探测含 `.HA_VERSION` 的配置目录（Docker 版就是 `/config`）
2. 检查 `wget` 和 `unzip`，缺一个就报错退出
3. 下载 `github.com/hacs/integration/releases/latest/download/hacs.zip`
4. 解压到 `custom_components/hacs/`（先删旧目录再解压）
5. 比对最低版本要求 `MINIMUM_HA_VERSION`
6. 提示重启 HA

理解这 6 步，就理解三种安装路径为什么可行：脚本的本质 = **找目录 → 下载 zip → 解压到 `custom_components/hacs/`**。只要最终效果一致，用什么方式装都行。

### 4.3 Docker 三种安装路径

Docker 版装 HACS 有 3 条路，区别只在「在哪一步下载、在哪一步解压」。

#### 路径一：进容器跑官方脚本

最省事，但要容器内有 wget/unzip 且能直连 GitHub：

```bash
# 1. 进容器拿到 shell
docker exec -it homeassistant bash
# 2. 切到配置目录（必须含 .HA_VERSION 才会被脚本识别）
cd /config
# 3. 跑官方脚本（自动探测目录、下载、解压）
wget -O - https://get.hacs.xyz | bash -
# 4. 退出容器并重启 HA
exit
docker restart homeassistant
```

#### 路径二：宿主机解压到挂载目录

脚本依赖容器内工具，但你可以直接在宿主机手动完成同样的事：

```bash
# 1. 进入宿主机上挂载到容器 /config 的目录
cd /path/to/your/config
# 2. 建目录、下载、解压
mkdir -p custom_components/hacs
wget https://github.com/hacs/integration/releases/latest/download/hacs.zip
unzip hacs.zip -d custom_components/hacs && rm hacs.zip
# 3. 重启让 HA 加载
docker restart homeassistant
```

#### 路径三：docker cp + 容器内解压

下载在宿主机做（方便套代理，见 4.4），解压交给容器内工具：

```bash
# 1. 宿主机下载（这里就能拼 gh-proxy 加速前缀）
wget -O /tmp/hacs.zip https://github.com/hacs/integration/releases/latest/download/hacs.zip
# 2. 拷进容器配置目录
docker cp /tmp/hacs.zip homeassistant:/config/custom_components/hacs/
# 3. 进容器解压并清理压缩包
docker exec -it homeassistant sh
cd /config/custom_components/hacs && unzip hacs.zip && rm hacs.zip
exit
# 4. 重启
docker restart homeassistant
```

> [!warning] 关键约束
> 文件必须**直接落在 `custom_components/hacs/` 根目录**，里面直接是 `__init__.py`、`const.py` 这些文件，不能多一层嵌套（比如 `custom_components/hacs/hacs/`）。多套一层 HA 就找不到。放好后一定要 `docker restart homeassistant`，HACS 才会被加载。

三条路径怎么选，看这张表：

| 路径 | 下载在哪做 | 解压在哪做 | 适用场景 |
|------|-----------|-----------|---------|
| 路径一 docker exec | 容器内 | 容器内 | 容器能直连 GitHub 且自带 unzip |
| 路径二 宿主机解压 | 宿主机 | 宿主机 | 挂载目录在宿主机、想少进容器 |
| 路径三 docker cp | 宿主机 | 容器内 | 宿主机下载要配代理，解压交给容器 |

### 4.4 国内加速：下载可以加速，授权必须直连

> [!tip] 大白话
> 国内加速 = 给 GitHub 下载装「加速器」。HACS 从 GitHub 下压缩包、拉仓库列表经常很慢或失败，加速器帮你绕过这段慢路。但它只管「下载」这一步——首次 GitHub 授权（Device flow）要打开浏览器访问 github.com，必须直连，加速器帮不上。

三个加速手段：

1. **gh-proxy 前缀代理**：在原始 GitHub 地址前拼代理前缀。`ghproxy.com` 已于 2025 年起失效；截至 2026-08 实测可用的是 `gh-proxy.com`、`ghproxy.net`（`mirror.ghproxy.com`、`ghfast.top` 也已失效）。写法是把原 URL 整个拼在代理域名后面，例如 `wget https://gh-proxy.com/https://github.com/hacs/integration/releases/latest/download/hacs.zip`，配合路径二/三使用。
2. **hacs-china 极速版**：一键安装脚本 `wget -O - https://get.hacs.vip | bash -` 已于 2026-08-08 失效（443 拒连），勿再使用。极速版项目本身仍活跃：可从 Gitee 镜像 [hacs-china](https://gitee.com/hacs-china) 手动下载安装包放入 `custom_components/hacs/`，或干脆用官方 HACS + 第 1 条的 gh-proxy 前缀代理。注意它是第三方 fork，且同样只加速下载。
3. **GitHub API 代理**：HACS 3.x 的「选项」UI 里填自定义 API 地址（不是 configuration.yaml），如 `ghapi-cf.hacs.vip/api`、`hacs-china.chrome7.com/api`，解决集成列表/版本检查加载失败。注意 `ghapi.hacs.vip/api` 已随 `get.hacs.vip` 一并失效，勿填。

> [!example] 实测命令（2026-08-08）
> 国内网络走「路径二（宿主机解压）」+ `gh-proxy.com` 前缀，一条龙完成下载 → 解压 → 重启：

```bash
cd /path/to/your/config          # 换成你挂载到容器 /config 的目录
mkdir -p custom_components/hacs
wget -O /tmp/hacs.zip "https://gh-proxy.com/https://github.com/hacs/integration/releases/latest/download/hacs.zip"
unzip -o /tmp/hacs.zip -d custom_components/hacs && rm /tmp/hacs.zip
docker restart homeassistant
```

> [!warning] 两个高频坑
> 代理域名（gh-proxy.com、ghproxy.net、ghapi-cf.hacs.vip 等）可用性易变，实操前先实测再配置。另外小容器常缺 `unzip`（Synology 会报 `'unzip' is not installed`），此时走路径二用宿主机 unzip 更稳；解压后如权限不对，`chown -R 1000:1000 custom_components/hacs` 修正属主。

### 本章小结

- HACS = HA 的社区应用商店，装集成 / 前端卡片 / 主题三类扩展
- 官方脚本 = 找 `/config` → 下载 hacs.zip → 解压到 `custom_components/hacs/`
- 三种路径殊途同归：进容器跑脚本 / 宿主机解压 / docker cp，选顺手的一条即可
- 文件必须直接落在 `custom_components/hacs/` 根目录，放完 `docker restart`
- 国内加速只解决「下载」，GitHub 首次授权必须直连

HACS 文件放好了，但还没真正「开通」——第五章我们完成首次配置和 GitHub 授权，再装一批常用的卡片与集成。

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-08-08 | 4.4 更新：`get.hacs.vip` 一键脚本与 `ghapi.hacs.vip/api` 已失效（443 拒连），标注勿用；代理前缀实测可用名单改为 `gh-proxy.com` / `ghproxy.net`，移除已失效的 `mirror.ghproxy.com`、`ghfast.top`；补充 Gitee 手动安装兜底 |
| 2026-08-08 | 4.4 增加「实测命令」：路径二 + `gh-proxy.com` 前缀的一条龙安装命令（下载 → 解压 → 重启） |
