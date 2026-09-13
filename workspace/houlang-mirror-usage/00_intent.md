# 厚浪镜像（HLmirror）镜像加速器使用方法 - 意图文件

## 基本信息

- **主题**: 厚浪镜像（HLmirror）镜像加速器使用方法
- **项目标识**: `houlang-mirror-usage`
- **运行标识**: `houlang-mirror-usage`
- **工作流**: `learning-note-flow`（阶段 3-4 走大纲模式）
- **创建时间**: 2026-09-13
- **当前阶段**: 阶段 0（意图澄清，等待用户确认）
- **输出目标**: obsidian
- **Vault 路径**: `D:\Study-Notes`
- **笔记目录**: `docker/`
- **MOC 路径**: `docker/Docker MOC.md`

## 用户原始请求

> https://mirror.houlang.cloud/dashboard，如何使用这镜像加速器

## 学习目标

### 笔记类型

**实战（practice）+ 速查（cheat_sheet）混合**——「上手怎么配 + 事后怎么查」。

- 主线：从注册到成功 `docker pull` 的完整可复现步骤。
- 速查层：9 个上游后缀 → 拉取地址对照表，供以后直接查表替换。

### 学习深度

上手（能独立完成配置、能排错、能解释为什么这样做）。

### 用户基础

有了解。用户 vault 内已有大量 Docker 与镜像加速相关笔记（见下方交叉引用），不需要从「什么是 Docker」讲起，但需要讲清**本服务与传统 registry-mirrors 的机制差异**。

## 研究计划

### 探索方向

1. **机制**：前缀式地址重写（`mirror.houlang.cloud/{后缀}/...`）vs 传统 `registry-mirrors` 直连镜像的区别，以及各自的适用边界。
2. **实操**：注册 → 建令牌 → 目标机器 `docker login` → 替换地址 → `docker pull` 的完整链路，含无需登录的场景判定。
3. **排错与边界**：鉴权失败、令牌失效、私有镜像（GHCR）、`docker login` 与 `daemon.json` 的相互关系、限速与配额。

### 重点收集

- **核心概念**：上游（upstream）、后缀代号（dh/ghcr/…）、访问令牌、前缀重写、回源与缓存、digest 校验。
- **实战命令**：`docker login -u <邮箱> -p <hlm_令牌> mirror.houlang.cloud`；`docker pull mirror.houlang.cloud/dh/library/nginx:latest`；`mirror.houlang.cloud/ghcr/immich-app/immich-server:v2.6.1`。
- **常见坑**：把令牌当密码用；误以为能填进 `daemon.json` 的 `registry-mirrors`；私有仓库鉴权；`latest` 与 digest 校验；限速导致的"变慢"误判。
- **工具链**：Docker / Docker Desktop、containerd / Kubernetes（k8s 后缀）、GHCR、compose 中 `image:` 字段的写法。
- **对照**：与 `docker/镜像加速器vs代理-概念对比.md` 的结论是否仍然成立、是否需要互相补充。

### 信源偏好

- 官方文档：是（`home.houlang.cloud` 知识库、控制台内的图文教程与镜像源列表）
- 技术博客：是（仅在官方口径缺失时补充，且必须标注为二手）
- 社区讨论：是（QQ 群 230832864 仅作为线索，不作为引用来源）
- 学术论文：否

### planner 已直接核实的事实（2026-09-13，供 research-collector 起步，**仍需回源复核**）

| 来源 ID | 位置 | 内容 |
| --- | --- | --- |
| S1 | `https://home.houlang.cloud/archives/ru-he-shi-yong-xin-ban-hlmirror` | 官方教程《如何使用新版 HLmirror》，发布 2026-03-31，已取到全文 |
| S2 | `https://mirror.houlang.cloud/` 首页 meta | 服务定位：国内缓存 + 自动回源，加速 Docker Hub / GHCR 等公开镜像源，注册即用、限时免费 |
| S3 | `https://mirror.houlang.cloud/assets/index-*.js`（前端 bundle） | `docker login -u <email> -p <token> <host>` 命令模板；令牌前缀 `hlm_`；配额字段 `monthly_quota_bytes`、`download_rate_limit_bps`；缓存按 digest 校验并可回退旧缓存 |
| S4 | `https://mirror.houlang.cloud/dashboard` 界面文案 | 控制台分区：账号信息 / 用量 / 镜像源列表 / 访问令牌；用户 API `GET /api/user/{profile,usage,channels,tokens}` |

**待复核的疑点（不要直接写进笔记）**：

1. 官方教程列出 **9** 个后缀（dh、gcr、ghcr、nvcr、k8s、mcr、elastic、**gitlab**、quay），而前端 bundle 内置常量只有 **8** 个（无 gitlab）。以控制台 `/api/user/channels` 实际返回为准，并说明"以后缀以控制台为准"。
2. 教程未明确**是否所有场景都必须登录**（匿名能否拉取公开镜像）；需实测或回源确认。
3. 教程未给出**配额与限速的具体数值**（免费额度、单用户限速），需查控制台或说明"以账号实际为准"。
4. 上游不可用时"回退旧缓存"的时长窗口，官方是否有公开数值。
5. `docker logout` / 令牌吊销（suspend）后的表现。

### 交叉引用（vault 内既有笔记，供双链与去重）

- `docker/DockerDesktop镜像加速器配置.md`
- `docker/镜像加速器vs代理-概念对比.md`
- `docker/docker进行代理.md`
- `docker/docker镜像拉取DNS解析超时排错.md`
- `docker/Docker MOC.md`
- `linux/GitHub 国内网络连接超时解决方案/`
- `homeassistant/docker-ha/06_国内稳定运行_版本锁定与镜像加速策略.md`

> 注意：以上链目标须在阶段 6 写双链前逐条 `os.path.exists` 核实，章级锚点避开含反引号/箭头/竖线的标题。

## 写作要求（沿用项目既有偏好）

1. 每个核心概念补 `[!tip] 大白话` 通俗解释 + 打比方（如"前缀重写 = 换前台代收"、"令牌 = 临时工牌"）。
2. 解释抽象机制按「它是什么 / 解决什么问题 → 具体产物长什么样 → 带具体值的可代入例子（命令与输出）→ 对比表 → 大白话类比」落地。
3. 代码块带语言标识并标注执行位置（本地 / 服务器）；命令示例用真实存在的镜像名。
4. 表格不要嵌套在列表项内（Obsidian 渲染问题）。
5. 正文中「官方口径/原文」类表述必须逐条回源比对，不转述。
6. 如最终产物 >30KB 或多于 3 章，发布前建议拆分，由用户决定单文件还是分册。

## 备注

- 本轮为**新主题学习笔记**，不是旧笔记导入、不是单篇/批量更新；既有 `workspace/workflow-runs/update-mirror-config.workflow.md`（2026-08-08 已完成）是 Docker 镜像源过时信息修复，与本轮无冲突，但阶段 2 应参考其已核实结论避免重复研究。
- 阶段 1 探测请优先直连官方站点与 GitHub 相关 issue；`mirror.houlang.cloud` 与 `home.houlang.cloud` 在 WebFetch 侧被拦截，需用 `curl` 获取。
