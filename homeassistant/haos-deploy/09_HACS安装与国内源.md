---
title: "第九章：HACS 安装与国内源——第三方集成商店与 GitHub 源加速"
tags:
  - 智能家居/HomeAssistant
  - HAOS/部署教程
  - 学习笔记
created: 2026-08-07
updated: 2026-08-07
status: 已完成
source_project: haos-deploy-tutorial
chapter: 9
---

# 第九章：HACS 安装与国内源——第三方集成商店与 GitHub 源加速

> [!summary] 本章讲什么
> 前八章解决了 HAOS 的安装、镜像与 OTA 国内源，但还差最后一环：**第三方集成（custom_components）的安装渠道**。官方 Add-on 商店装的是加载项，第三方集成（米家、Localtuya、天气卡片、floorplan 等）要靠 **HACS**（Home Assistant Community Store）。本章讲清 HACS 是什么、官方安装为什么在国内卡住、以及四条国内可用的安装路线：HACS 极速版一键装（最常用）、手动装官方版 + gh-proxy 加速、加载项安装器、以及第 5 章 HAOS-CN 的内置方案。
>
> 与第 4 章的关系：第 4 章解决的是「镜像源」（ghcr.io / docker.io），本章解决的是「**GitHub 源**」（HACS 本体与它下载的插件都挂在 GitHub 上）。两条线是 [[01_绪论|第一章]] 那张表里「加载项卡镜像、集成卡 GitHub」的对应解法。

> [!warning] 时效性说明
> 极速版一键脚本地址（`get.hacs.vip`）、GitHub API 代理节点、Gitee 仓库地址均为采集时间（2026-08）可用的社区源。公益代理有请求次数限制、随时可能失效，以实际执行结果为准；失效时换节点或改用 9.4 的手动官方版方案。

## 9.1 HACS 是什么：HA 的「社区商店」

HACS 是 **Home Assistant Community Store** 的缩写，一个社区维护的第三方组件商店。它**本身也是一个集成（custom_component）**，装进 `config/custom_components/hacs/` 后，给你提供一个侧边栏入口，用来安装、更新、管理三类东西：

| 类别 | 例子 | 作用位置 |
|------|------|---------|
| 第三方集成 | 米家 `xiaomi_home`、`localtuya`、`midea_ac_lan` | 设备接入（跑在 HA 主进程） |
| 前端卡片 | `floorplan`、`mini-graphic-card` 等 | Lovelace 面板 UI |
| 主题 | 各种配色主题 | 全局外观 |

和官方商店的关键区别（衔接 [[01_绪论|第一章]] 的表格）：

| 维度 | 官方 Add-on 商店 | HACS |
|------|-----------------|------|
| 装的东西 | 加载项（容器程序） | 第三方集成 / 卡片 / 主题 |
| 运行位置 | 与 HA 并列的容器 | 加载进 HA 主进程内部 |
| 下载源 | ghcr.io（镜像） | GitHub（Release + 源码） |
| 国内瓶颈 | 镜像源 → 第 4 章已解决 | **GitHub 源 → 本章要解决的** |
| 典型例子 | Node-RED、ESPHome、Terminal & SSH | 米家、Localtuya、Floorplan |

> [!note] 加载项 ≠ 集成 ≠ HACS 装的东西
> 「设置 → 加载项」装的是**程序**（容器）；「设置 → 设备与服务」加的是**集成**（驱动）。HACS 装的是后者以及前端资源，不是加载项。装完 HACS 后，你在它里面搜「米家」装的是集成，而不是去加载项商店搜。

## 9.2 官方安装方式与国内卡点

官方标准安装（见 [hacs.xyz](https://hacs.xyz)）分两步：

```bash
# 1) 在 Terminal & SSH 加载项（或宿主 shell）里执行官方安装脚本
wget -O - https://get.hacs.xyz | bash -
```

然后 设置 → 设备与服务 → 添加集成 → HACS → 用 **GitHub 账号授权**。

两个卡点都在 GitHub：

> [!warning] 卡点一：安装脚本与安装包在 GitHub
> `get.hacs.xyz` 的脚本会去 `raw.githubusercontent.com` 拉脚本、从 `github.com/hacs/integration` 的 Release 下载 `hacs.zip`，解压到 `config/custom_components/hacs/`。大陆直连这些域名慢或超时，社区统计下载失败率可达 30–40%。

> [!warning] 卡点二：首次授权走 GitHub OAuth
> 添加集成时要用 GitHub 账号授权，这一步访问 `github.com` 的认证接口。**任何国内加速都绕不开这一步**——只能直连或临时用代理，转圈属正常现象，稍后再试。

所以「国内可用」的核心策略是：**用加速方式把 hacs.zip 拿到手，授权那步单独解决**。

## 9.3 方案一：HACS 极速版一键安装（国内最常用，推荐）

HACS 极速版是官方 HACS 的国内修改版（项目：`Sheldondxx/integration-homeassist`、`hacs-china`），通过内置 GitHub 代理节点 + 本地缓存 + 自适应重试把下载提速，**覆盖官方集成但共用同一套配置**，装完不用重新配置。

一键安装（HAOS / Supervised 在宿主 shell 或 Terminal & SSH 加载项里执行；Core / Docker 先进 HA 配置目录）：

```bash
wget -O - https://get.hacs.vip | bash -
# 或
curl -fsSL get.hacs.vip | bash
```

装完**重启 HA**，然后 设置 → 设备与服务 → 添加集成 → HACS 完成初始化。

> [!note] 用哪个终端？
> - HAOS：宿主 shell（第 4 章 4.6 的 `login` 控制台 / 22222）或 Terminal & SSH 加载项；
> - Core / Docker：SSH 进宿主机后 `cd` 到 HA 配置目录（`custom_components` 的上级）再执行。

加速效果（项目方宣传数据，建议实测验证）：

| 指标 | 官方 HACS | HACS 极速版 |
|------|----------|-------------|
| 插件列表加载 | 30–60 秒 | 3–5 秒 |
| 10MB 插件下载 | 5–10 分钟 | 15–30 秒 |
| 批量更新 5 个插件 | 20–30 分钟 | 2–3 分钟 |
| 安装成功率 | 60–70% | 99%+ |

**列表/详情加载不出来时**（GitHub API 也被墙）：自 v1.27.1.3 起支持自定义 GitHub API 镜像地址。进 HACS 集成「选项」，填入任一免费节点（每日有请求限额，建议轮换）：

```text
https://ghapi.hacs.vip
https://ghapi-cf.hacs.vip/api
https://hacs-china.chrome7.com/api
https://hacs-china.casen.tk/api
```

**更新极速版本体**：v1.33.0.3+ 可在开发者工具调用服务：

```yaml
service: hacs.upgrade
```

## 9.4 方案二：手动装官方原版 + gh-proxy 加速（零信任成本）

不想用第三方修改版时，用第 4 章验证过的 `gh-proxy.org` 加速前缀手动下载**官方原版** hacs.zip：

```bash
# 1) 在任意有网机器上下官方 hacs.zip（gh-proxy 加速 GitHub Release）
wget https://gh-proxy.org/https://github.com/hacs/integration/releases/latest/download/hacs.zip

# 2) 解压到 config/custom_components/hacs/
unzip hacs.zip -d custom_components/hacs/

# 3) 重启 HA → 设置 → 设备与服务 → 添加集成 → HACS → GitHub 账号授权
```

> [!tip] zip 的目录结构
> HACS 官方 Release 的 zip 解压出来就是 `custom_components/hacs/` 的内容（`__init__.py`、`manifest.json`、`config_flow.py` 等），不要多套一层目录。装完以 `config/custom_components/hacs/manifest.json` 存在为准。

优点：组件是**官方原版**，无第三方信任成本；缺点：首次 GitHub 授权仍要直连（卡点二绕不开）。适合「想要原版、授权那步有办法解决」的用户。

## 9.5 方案三：加载项安装器（HAOS / Supervised 图形化）

不想敲命令，可以走加载项商店图形化安装，思路与第 4 章 4.5 的 Gitee 仓库一致：

1. 设置 → 加载项商店 → 右上角三个点 → 仓库 → 添加：
   ```text
   https://gitee.com/hacs-china/addons
   ```
2. 商店里出现「HACS 极速版安装器」，安装并启动；
3. 看安装器日志，完成后重启 HA；
4. 设备与服务 → 添加集成 → HACS。

> [!note] 与 4.5 的 Gitee 仓库互补
> 4.5 加的 `desmond_GT/hassio-addons` 是「Add-on 搬运优化版」，解决**加载项**装不进；本章加的 `hacs-china/addons` 是「HACS 安装器」，解决**第三方集成**的安装。两者不冲突、可并存。

## 9.6 装完必做的配置与验证

装完 HACS 不是终点，按这个顺序过一遍：

> [!example] 验收清单（按顺序）
> 1. 重启 HA，侧边栏出现 **HACS** 入口；
> 2. 设置 → 设备与服务 → 添加集成 → 搜 **HACS** → 进入 GitHub 授权；
> 3. 授权完成后进入 HACS 首页，能看到「集成 / 前端 / 主题 / 自动化」分类；
> 4. 搜一个插件（如 `xiaomi_home`）试装，确认能列得出、下得动；
> 5. 列表空白 → 按 9.3 配置 GitHub API 代理节点，或更换节点；
> 6. 下载卡死 → 重试一次（公益代理偶发失败是常态）。

> [!warning] 首次 GitHub 授权转圈
> 这是唯一无法加速的环节。一直转圈就换网络环境（临时代理 / 手机热点）重试；授权**成功后**回到国内网络，日常使用走的是代理，不受影响。

## 9.7 风险与信任模型

和 [[05_HAOS-CN极速版|第 5 章]] 讲 HAOS-CN 是同一个道理——极速版是第三方修改版，接受它就要接受它的信任成本：

> [!warning] HACS 极速版风险清单
> 1. **第三方修改版**：在官方集成上改动网络层，公开仓库可见，但建议自行审一遍关键 diff；
> 2. **覆盖官方集成**：与官方 HACS 共用配置，但想切回官方版需用官方脚本重装（`get.hacs.xyz`）；
> 3. **公益代理不可控**：免费节点有请求限额与失效风险，涉及敏感数据的下载注意传输链路；
> 4. **免验证版有安全风险**：跳过 GitHub OAuth 的版本可能装到被篡改的插件，**个人家用不建议**，只选从可信渠道（官方 GitHub / hacs-china）获取；
> 5. **授权直连绕不开**：GitHub 授权那一步仍需直连，不是「完全无需科学上网」。

> [!tip] 与官方版的取舍
> - 要省心、网络差：**HACS 极速版（9.3）**；
> - 要原版组件、有办法过授权：**手动官方 + gh-proxy（9.4）**；
> - 装完 HACS 只是开始，插件后续下载慢，同一套代理体系内解决。

## 与第 5 章的关系：HAOS-CN 已内置

如果你走的是 [[05_HAOS-CN极速版|第 5 章]] 的 HAOS-CN 极速版路线，**这一步可以跳过**：HAOS-CN 在构建时已内置 HACS 极速版，装上就有、不需要 GitHub 账号。商用场景的冬瓜 HAOS 也预装 HACS。本章 9.3–9.5 只服务于**官方原版路线**的用户。

## 本章 Checklist

- [ ] 我能说清 HACS 与官方 Add-on 商店的区别：加载项 vs 第三方集成/卡片/主题
- [ ] 我知道官方安装的两个 GitHub 卡点：下载包在 GitHub、首次授权走 GitHub OAuth
- [ ] 官方原版路线：已用 `curl -fsSL get.hacs.vip | bash` 装好 HACS 极速版并重启 HA
- [ ] 追求原版时：知道用 gh-proxy 前缀手动下载官方 `hacs.zip` 解压到 `custom_components/hacs/`
- [ ] 列表加载不出来时：知道在 HACS 集成「选项」配 GitHub API 代理节点并轮换
- [ ] 我知道首次 GitHub 授权无法加速，转圈时换网络重试
- [ ] 已权衡信任模型：极速版 = 第三方修改版；免验证版有安全风险，不选用
- [ ] HAOS-CN / 冬瓜 HAOS 用户：确认内置 HACS，无需重复安装

## 更新记录

- **2026-08-07**：新增第九章。衔接第 1 章「加载项卡镜像、集成卡 GitHub」框架，补上第三方集成商店 HACS 的安装与国内源四路线（极速版 / 手动官方 + gh-proxy / 加载项安装器 / HAOS-CN 内置）。

---

> ⬅️ 上一章：[[08_故障排查手册与长期运维|第八章 故障排查手册与长期运维]] ｜ 📖 [[部署 HAOS 详细教程|返回索引]]
