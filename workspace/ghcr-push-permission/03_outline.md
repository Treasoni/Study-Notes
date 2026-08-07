## 学习笔记大纲：《GHCR 推送镜像权限配置》

> 笔记类型：概念 + 实战
> 预计总篇幅：约 18-22 页（章节长度分布：中/中/长/中）
> 章节数：4 章

### 章节概览

| 章节 | 定位 | 篇幅 | 核心内容 | 素材引用 | 代码示例 |
|------|------|------|----------|----------|----------|
| 第一章：GHCR 权限模型与 GITHUB_TOKEN 的限制 | 概念基础 | 中 | 为什么 CI 默认凭据不一定能推镜像 | §1 | 有 |
| 第二章：PAT 选型——为什么只能用 Classic PAT | 概念更正 | 中 | 更正原指南误区，Fine-grained 不可用的依据 | §2、§7 | 无 |
| 第三章：落地配置——PAT + Secret + Workflow 兜底登录 | 操作实战 | 长 | 从生成 PAT 到完整可复制 workflow | §3、§4、§5 | 有 |
| 第四章：实战排错——首推成功与常见坑 | 排错实战 | 中 | 报错对照、孤立包死结、边界场景、最佳实践 | §6、§5.2 | 有 |

---

### 第一章：GHCR 权限模型与 GITHUB_TOKEN 的限制

- **篇幅**：中（约 4-5 页）
- **覆盖要点**：
  - `GITHUB_TOKEN` 是什么：per-run 临时令牌、自动过期、无需管理
  - 2023-02-02 默认权限变更：新对象 `GITHUB_TOKEN` 默认 read-only，`packages` 默认 `read` 导致无法创建/推送包
  - `permissions:` 块规则：未列出 scope 一律降为 `none`（"只写 packages 会害 checkout 失败"）、job 级覆盖、fork PR 始终只读
  - 包可见性与包-仓库关联：默认 private、public 不可回退、OCI label 自动关联、GITHUB_TOKEN 只能访问本仓库关联的包
  - 何时仍需用户 PAT（本笔记触发场景）：首次建包被拒、跨账号/跨仓库、组织命名空间、包级 admin、非 Actions 环境
- **素材引用**：§1.1、§1.2、§1.3、§1.4、§1.5
- **代码示例**：有（`permissions:` 块 YAML 片段、常见错误示例）

### 第二章：PAT 选型——为什么 GHCR 只能用 Classic PAT

- **篇幅**：中（约 3-4 页）
- **覆盖要点**：
  - Classic vs Fine-grained PAT 对比：前缀、权限粒度、过期策略、组织授权方式
  - **关键更正**：原指南「阶段一生成 Fine-grained PAT 勾选 Packages: Read and Write」不成立——fine-grained PAT 中不存在 packages 权限项
  - Fine-grained 不可用的依据链：官方文档原文、docker/login-action Issue #331 实证、github/docs #33900、roadmap #558（2026 未落地）
  - 适用范围：所有 GitHub Packages 注册表（Container / npm / NuGet / Maven / RubyGems）
  - 组织策略禁用 classic PAT 时的替代路径：`GITHUB_TOKEN` + 仓库 Actions 授权、GitHub App（有限支持）
- **素材引用**：§2、§7 信源中的官方文档与 Issues
- **代码示例**：无

### 第三章：落地配置——Classic PAT + Secret + Workflow 兜底登录

- **篇幅**：长（约 5-6 页）
- **覆盖要点**：
  - 生成 Classic PAT：UI 路径、Note 命名、过期设置（短期纳入轮换）、Scopes（`write:packages` / `repo` / `delete:packages`）、SSO Configure
  - 注意点：勾 `write:packages` 会连带 `repo`（权限偏大）；纯 CI 优先 `GITHUB_TOKEN`
  - Repository Secret 配置：UI 路径、命名约束（非 `GITHUB_` 前缀、非数字开头、大小写不敏感）、48KB 限制、fork PR 不传 secret、CLI `gh secret set`
  - `docker/login-action` 兜底：`${{ secrets.GHCR_TOKEN || secrets.GITHUB_TOKEN }}` 短路语义
  - 何时其实不需要兜底：包已存在 + 关联仓库 +「Manage Actions access」授权后 `GITHUB_TOKEN` 可直推
  - 完整可复制 workflow：方案 A（纯 GITHUB_TOKEN，推荐）/ 方案 B（兜底认证），含 metadata-action、build-push-action、gha cache
- **素材引用**：§3、§4、§5.1、§5.2、§5.3
- **代码示例**：有（完整 publish-to-ghcr workflow YAML、兜底表达式、Secret 命名示例）

### 第四章：实战排错——首推成功与常见坑

- **篇幅**：中（约 4-5 页）
- **覆盖要点**：
  - 首次建包 bootstrap 死结（最高频根因）：部分上传留下孤立私有包、manifest 被拒；修复步骤 + 预防（Dockerfile 加 OCI label）
  - 报错对照表：`write_package`、`create_package`、`token does not match expected scopes`（fine-grained 典型失败）、组织 `installation not allowed`、匿名拉取 401、仓库重建后推送失败
  - fork PR 边界场景：不传 secret、token 只读，拉取场景需显式 login + `packages: read`
  - 最佳实践与业界趋势：`LABEL org.opencontainers.image.source` 自动关联、rust-lang / flux2 弃用静态 PAT 改 `GITHUB_TOKEN`
  - 检查清单：一份从零配置到首推成功的自查清单
- **素材引用**：§6、§5.2、§7（Community Discussion、flux2 commit、Andrew Hoog 授权步骤）
- **代码示例**：有（Dockerfile LABEL 片段、`gh secret set` CLI 片段、检查清单 YAML 片段）

---

## 学习路径说明

### 前置要求
- 有 GitHub 账号与仓库基本操作经验（Settings、Secrets 页面导航）
- Docker 基础：理解 image、tag、`docker push` 的概念
- 能读懂基础 GitHub Actions workflow（on / jobs / steps / uses）
- 无需提前有 GHCR 使用经验，本章从权限模型讲起

### 学完能做什么
- 能独立配置一条从零开始向 GHCR 推送镜像的完整链路（PAT → Secret → workflow → 首推成功）
- 能说清「为什么 CI 默认 `GITHUB_TOKEN` 可能推不了包」的底层原因
- 能正确选型 Classic PAT 与 Fine-grained PAT，并解释 fine-grained 为何不可用于 Packages
- 遇到常见报错（`write_package` / `create_package` / scope mismatch / 组织拒绝 / 401）能对照定位并修复
- 掌握业界推荐做法：优先 `GITHUB_TOKEN` + 「Manage Actions access」，静态 PAT 仅作兜底

### 建议学习顺序
1. 第一章 → 第二章：先建立权限模型认知，再理解选型结论（约 1-1.5 小时）
2. 第三章：按步骤实操，用示例仓库完成一次配置（约 1-1.5 小时）
3. 第四章：先读报错对照表，再回到第三章自查（约 30-45 分钟）
4. 总计约 3-4 小时可完整走通；若只为解决当前报错，可先读第四章定位，再回看第三章落地

> 素材缺口提示：本大纲默认读者在 Actions 环境内操作；本地/非 Actions 环境（Docker CLI 直推）只涉及 PAT 登录，未单列章节，如需可后续补充。
