# GHCR 推送镜像权限配置 - 探测结果（P1）

> 收集时间: 2026-08-08
> 收集方式: 3 个 subagent 并行探测（GHCR 权限模型 / Fine-grained PAT / Secret + docker/login-action）
> 信源偏好: 官方文档优先 + 技术博客 + 官方社区讨论

---

## 方向 A：GHCR 权限模型与 GITHUB_TOKEN 限制

| # | 标题 | 相关性 | 来源 |
|---|------|--------|------|
| 1 | [About permissions for GitHub Packages](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages) | 5/5 | 官方文档 |
| 2 | [permission_denied write_package 讨论 #166194](https://github.com/orgs/community/discussions/166194) | 5/5 | 官方社区 |
| 3 | [buildx write_package 讨论 #32184](https://github.com/orgs/community/discussions/32184) | 4/5 | 官方社区 |
| 4 | [GITHUB_TOKEN write package 报错（Stack Overflow）](https://stackoverflow.com/questions/70646920/) | 5/5 | 社区问答 |
| 5 | [Changes to default GITHUB_TOKEN permissions（Arinco）](https://arinco.com.au/blog/changes-to-the-default-github_token-permissions/) | 4/5 | 技术博客 |

**关键发现：**
- `GITHUB_TOKEN` 默认对 packages 是**只读**（`packages: read`）；发布镜像需在 workflow 的 `permissions` 块显式声明 `packages: write`。
- **2023 年起** GitHub 把新仓库/组织默认 Workflow permissions 改为只读，旧仓库可能仍默认读写 → 同一份 YAML 在不同仓库行为不同。
- 一旦声明 `permissions` 块，**未列出的作用域自动降为 `none`**。
- GHCR 新包**默认私有**；包必须与仓库正确关联，否则 `write_package` 被拒。
- 仓库删除重建后 GHCR 视为全新仓库，旧包权限不继承 → 持续 `write_package` 失败；需删除孤立包或配置 `Manage Actions access`。
- fork PR 的 token **强制只读**，无法推送。
- 核心结论：内置 `GITHUB_TOKEN` 在显式 `packages: write` 下**可以**推送，但当目标账号/组织未开通默认 Packages 权限、需要跨账号或更高权限 token 时，就需要用户 PAT。

---

## 方向 B：Fine-grained PAT 生成与权限配置

| # | 标题 | 相关性 | 来源 |
|---|------|--------|------|
| 1 | [About permissions for GitHub Packages](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages) | 5/5 | 官方文档 |
| 2 | [Fine-grained PATs GA（GitHub Changelog 2025-03-18）](https://github.blog/changelog/2025-03-18-fine-grained-pats-are-now-generally-available/) | 4/5 | 官方 Changelog |
| 3 | [Introducing fine-grained PATs（GitHub Blog）](https://github.blog/security/application-security/introducing-fine-grained-personal-access-tokens-for-github/) | 4/5 | 官方博客 |
| 4 | [GHCR with fine-grained PAT: limitations（Stack Overflow TIL）](https://agents.stackoverflow.com/tils/02bbc3e5-82b4-4912-96ea-1bab8153d0d4) | 4/5 | 社区问答 |
| 5 | [GHCR: Complete Guide（Gecko Security）](https://www.gecko.security/blog/ghcr-github-container-registry-guide) | 4/5 | 技术博客 |

**关键发现（含重要时间线）：**
- **Fine-grained PAT 于 2025-03-18 GA**，GA 时官方明确「Packages 与 Checks API」仍是未支持缺口；此后**分注册表逐步补上**。
- **截至 2026 年，GHCR 推镜像可用 Fine-grained PAT**：把仓库级「Packages」权限设为 `Read and write` 即可。旧资料说「不支持」是因为 2025 年初的时间线。
- 经典 PAT（`ghp_` 前缀）对应粗粒度 scope：推包需 `write:packages`、拉取 `read:packages`、私有仓库关联镜像还需 `repo`。
- Fine-grained PAT（`github_pat_` 前缀）关键配置：`Resource owner`=包所属账号/组织、`Repository access`=目标仓库、`Packages` 权限=Read and write、`Expiration`≤366 天且强制过期。
- 组织级包必须把**组织**设为 Resource owner 并开启组织允许策略；token 可能处于 pending 直到组织审批。

---

## 方向 C：Repository Secret + docker/login-action 兜底

| # | 标题 | 相关性 | 来源 |
|---|------|--------|------|
| 1 | [Using secrets in GitHub Actions（官方文档）](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) | 5/5 | 官方文档 |
| 2 | [Working with the Container registry（官方文档）](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) | 5/5 | 官方文档 |
| 3 | [docker/login-action（GitHub Marketplace）](https://github.com/docker/login-action) | 5/5 | 官方文档 |
| 4 | [GHCR_TOKEN secret 兜底 commit 示例](https://github.com/julesdg6/openclaw-mission-control-unraid/commit/9e1f174047e1e2144f921b3d7b9d53a2a51870cd) | 5/5 | 社区实操 |
| 5 | [Push Docker Images to GHCR（OneUptime, 2026-02）](https://oneuptime.com/blog/post/2026-02-08-how-to-push-docker-images-to-github-container-registry/view) | 4/5 | 技术博客 |

**关键发现：**
- Repository Secret 入口：仓库 `Settings → Secrets and variables → Actions → New repository secret`，引用方式 `${{ secrets.名称 }}`。
- Secret 上限 48KB、每仓库最多 100 个；**fork 触发的 PR 不传 Secret**（`GITHUB_TOKEN` 除外）。
- `docker/login-action@v3` 核心 inputs：`registry`（默认 docker.io）、`username`、`password`、`logout`（默认 true）。GHCR 官方示例用 `registry: ghcr.io` + `${{ github.actor }}` + GITHUB_TOKEN。
- **兜底表达式** `password: ${{ secrets.GHCR_TOKEN || secrets.GITHUB_TOKEN }}`：优先用户配置的 `GHCR_TOKEN`，为空时回退到默认 `GITHUB_TOKEN`。
- 兜底必要性的根因：2023 年起默认 Actions 权限只读，`GITHUB_TOKEN` 无法创建新包 → 需要高权限 token 兜底；回退在包已存在或权限改为读写时可用。
- 常见坑：Secret 命名必须与 workflow 引用完全一致；`403` / `permission_denied: write_package` 多为缺 `packages: write` 或孤儿包未关联仓库。

---

## 方向菜单（待用户选择）

**A. 全方向覆盖（推荐）** — 权限模型 + PAT 配置 + Secret/Workflow 落地三块都深度收集，构成完整「概念 + 实战」笔记（对应三个自然章节）。

**B. 侧重原理（A + B）** — 权限模型 + Fine-grained PAT 配置为重点，实战（Secret/Workflow）简略。

**C. 侧重实战（B + C）** — PAT + Secret/Workflow 落地为重点，权限模型简略。

---

## 综合分析

1. 三方向互为因果，构成一条完整链路：**为什么需要额外 token（权限模型）→ 生成什么 token（PAT）→ 怎么注入与兜底（Secret + Workflow）**。
2. 资料时效性需注意：Fine-grained PAT 对 GHCR 的支持是 **2025 年中后逐步落地**的，大量旧教程仍说「fine-grained 不支持 packages」，应优先采用 2026 年及官方当前文档。
3. 用户场景「未开通默认 Packages 权限 / 需要跨账号或高权限 token 推镜像」正是 GITHUB_TOKEN 兜底方案的典型触发条件，与探测结果完全吻合。
