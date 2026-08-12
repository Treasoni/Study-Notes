# 搭建 AI API 中转站（new-api） - 探测式收集结果

收集时间: 2026-08-11
项目: new-api-relay-station
工作流: learning-note-flow（阶段 1：探测式收集）

## 探测角度与结论

### 角度 1：项目认知与概览
- new-api 是基于 One API 二次开发的 **AGPL-3.0 开源 AI 模型网关**（Go + Vue，GitHub 44.9k stars）。
- 核心能力：聚合 OpenAI、Claude、Gemini、DeepSeek、Midjourney、Suno 等多源模型；**跨协议转换**（OpenAI⇄Claude、OpenAI→Gemini）；以 OpenAI/Claude 兼容接口对外统一分发。
- 内置：渠道路由、令牌限制、额度/按次计费、负载均衡、数据看板。
- 完全兼容 One API 原版数据库（one-api.db 可直用）。
- 官方文档：https://docs.newapi.pro/ 与 https://github.com/QuantumNous/new-api （仓库 README）
- 关键结论：市面很多「AI 中转站」后台就是跑 new-api 代码，是自建中转站的主流方案。

### 角度 2：从零部署与上手
- **最低要求**：Linux + Docker + Docker Compose（amd64/arm64）。
- **官方镜像**：`calciumion/new-api:latest`，默认端口 3000。
- **快速启动**（单容器，SQLite）：
  ```bash
  docker run -d -p 3000:3000 -v ./data:/data calciumion/new-api:latest
  ```
  默认 SQLite，务必挂载 `/data` 持久化；远程库需 MySQL ≥5.7.8 或 PostgreSQL ≥9.6。
- **Docker Compose 部署**：克隆仓库 → 编辑 `docker-compose.yml`（自带 MySQL + Redis + 主服务）→ `docker compose up -d`。
- **首次启动**：进入初始化向导，**创建管理员账号密码**并选择使用模式（自用 / 对外服务 / 演示站点）。官方无内置默认账号；社区流传的 `root/123456`、`admin/admin123` 因版本而异，登录后立即改密。
- 端口冲突可映射为 `"3480:3000"`；健康检查接口 `/api/status`。

### 角度 3：日常使用与常见坑
- **渠道管理**：Type / Key / BaseURL / Models / Group / Priority / Weight / ModelMapping / AutoBan / StatusCodeMapping。单渠道支持多 Key 池轮换；选路 = Priority 优先 → Weight 随机。
- **模型映射注意**：ModelMapping 是「入站→上游」单向改写，不会自动让模型「存在」；需把模型名同时加进渠道 Models 列表，并核对用户组/渠道分组是否匹配。
- **令牌管理**：令牌为 OpenAI 兼容格式 `sk-{base_key}`；管理员可加 `-{channel_id}` 强制路由；支持无限配额、过期时间、模型白名单（ModelLimits）、IP/CIDR 白名单。
- **额度计算**：额度 = 组倍率 × 模型倍率 ×（提示词 token + 补全 token × 补全倍率）。令牌配额与账户余额分离——令牌配额不足即使账户有余额也报「额度不足」。
- **常见坑**：
  1. 「无可用渠道/模型不存在」多半是模型列表与映射没同步，或分组不匹配。
  2. 重试机制只对 HTTP 429 生效；`exhausted`/额度不足等非 429 错误直接透传，建议配置「自动禁用关键词」兜底。
  3. 接入 NextChat 等客户端用 Claude 系模型需在模型名加 `@openai` 后缀、地址不带 `/v1`，否则协议头不匹配鉴权失败。
  4. 渠道测试报 JSON 解析错误（invalid character '<'）多为被 CDN/反代拦截返回 HTML。

## 高质量信源清单

| # | 标题 | URL | 评分 | 类型 |
|---|------|-----|------|------|
| 1 | new-api 官方仓库 README | https://github.com/QuantumNous/new-api | 5/5 | 官方文档 |
| 2 | new-api 官方文档站 | https://docs.newapi.pro/ | 5/5 | 官方文档 |
| 3 | 官方 Wiki：特性介绍 | https://github.com/QuantumNous/new-api-docs/blob/main/docs/wiki/features-introduction.md | 5/5 | 官方文档 |
| 4 | 官方部署文档：Docker Compose | https://github.com/QuantumNous/new-api-docs/blob/main/docs/en/installation/docker-compose-installation.md | 5/5 | 官方文档 |
| 5 | 官方 FAQ | https://docs.newapi.pro/zh/docs/support/faq | 5/5 | 官方文档 |
| 6 | DeepWiki：渠道管理 | https://deepwiki.com/QuantumNous/new-api/3-channel-management | 5/5 | 技术文档 |
| 7 | DeepWiki：令牌管理 | https://deepwiki.com/QuantumNous/new-api/6.2-api-tokens | 4/5 | 技术文档 |
| 8 | 腾讯云：基于 Docker 搭建 NewAPI 图文教程 | https://cloud.tencent.com.cn/developer/article/2632560 | 4/5 | 技术博客 |
| 9 | cnbugs：New API 搭建教程 | https://www.cnbugs.com/post-6936.html | 4/5 | 技术博客 |
| 10 | linux.do：new-api 接入 NextChat 排障 | https://linux.do/t/topic/176116 | 5/5 | 社区讨论 |
| 11 | GitHub Issue #2659：exhausted 不重试 | https://github.com/QuantumNous/new-api/issues/2659 | 4/5 | GitHub Issues |
| 12 | V2EX：NewAPI 开源自荐 | https://global.v2ex.co/t/1197864 | 4/5 | 社区讨论 |

## 候选学习方向

- **A. 从零搭建 + 上手使用（一条龙实战）**：环境准备 → Docker 部署 → 初始化向导 → 渠道配置 → 令牌管理 → 接入第三方客户端。最贴合「我想搭建中转站，教我搭建使用」。
- **B. 架构与原理理解**：new-api 内部机制（渠道路由、协议转换、计费模型、多租户）。偏概念，适合想深入底层。
- **C. 常见坑与运维排障**：FAQ、常见报错、数据备份与升级、安全加固（HTTPS、改密）。适合已搭好、想稳定运维。
- **D. 自由组合**：以 A 为主干，融入 C 的避坑要点；B 只作概念铺垫。
