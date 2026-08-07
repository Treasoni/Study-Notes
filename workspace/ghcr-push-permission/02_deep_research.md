# GHCR 推送镜像权限配置 - 深度素材（P2）

> 收集时间: 2026-08-08
> 收集方式: 3 个 subagent 定向深读 + 权威源核实（WebFetch docs.github.com + 多源 WebSearch 交叉验证）
> 时效性: 2026-08 现状；GitHub 政策以官方文档为准

---

## ⚠️ 最重要结论：Fine-grained PAT 不支持 GitHub Packages

**官方文档原文**：`GitHub Packages only supports authentication using a personal access token (classic).`

**核实链**：
- docs.github.com「About permissions for GitHub Packages」明确只支持 **classic PAT**（已直接抓取原文确认）。
- [docker/login-action Issue #331](https://github.com/docker/login-action/issues/331)：用户把 fine-grained PAT 所有权限设为 Read-write，推 GHCR 仍报 `denied: permission_denied: The token provided does not match expected scopes`；换 classic PAT 同一 workflow 即成功。
- [github/docs Issue #33900](https://github.com/github/docs/issues/33900)："Fine-grained access tokens do not have `packages:read` permissions, even when empty."
- [github/roadmap Issue #558](https://github.com/github/roadmap/issues/558)：fine-grained 支持 Packages 的路线图 2026 年仍未落地。
- 适用范围：适用于**所有** GitHub Packages 注册表（Container Registry / npm / NuGet / Maven / RubyGems 等）。

**对用户指南的影响**：
- ❌ 指南「阶段一：生成 Fine-grained PAT，勾选 Packages: Read and Write」——**该权限项在 fine-grained PAT 中不存在**。
- ✅ 正确做法：**Classic PAT + `write:packages`**（推送）/ `read:packages`（拉取）/ 私有仓库加 `repo` / 删除加 `delete:packages`。
- ✅ 指南「阶段二：Repository Secret + 阶段三：Workflow 兜底」逻辑正确，可保留。

---

## 1. GHCR 权限模型与 GITHUB_TOKEN 限制

### 1.1 GITHUB_TOKEN 是什么
- Actions 运行时自动签发、per-run 临时令牌（`secrets.GITHUB_TOKEN`），自动过期，无需管理。
- 作用域取决于仓库/组织/企业默认设置 + workflow 内 `permissions:` 块。

### 1.2 默认行为（2023 变更）
- 2023-02-02 起，新创建对象的 GITHUB_TOKEN 默认权限从 read/write 改为 **read-only**（只影响新仓库/组织，不回溯 2023-02 前创建的旧仓库）。
- 默认只读：`contents: read` + `packages: read` → 无法推送/创建包。

### 1.3 `permissions:` 块规则（关键）
```yaml
permissions:
  contents: read
  packages: write
```
- 一旦写 `permissions:`，**未列出的 scope 一律降为 `none`**（不继承默认值）。
- 常见坑：只写 `permissions: { packages: write }` 会让 `contents` 变 `none`，导致 `actions/checkout` 失败 → 必须显式带 `contents: read`。
- job 级 `permissions:` 覆盖顶层。
- fork PR 触发的 workflow：GITHUB_TOKEN **始终只读**，写 `packages: write` 也无效。

### 1.4 包可见性与包-仓库关联
- GHCR 新包**默认 private**；与仓库关联（link）后继承该仓库可见性。
- **一旦手动设为 public，不可再改回 private**。
- 关联方式：OCI label `org.opencontainers.image.source=https://github.com/<owner>/<repo>` 自动关联；关联后该仓库的 workflow 自动获得访问权。
- GITHUB_TOKEN 只能访问**当前 workflow 所在仓库**关联的包；跨账号/其他仓库的私有包需额外配置或 PAT。

### 1.5 何时仍需用户 PAT（本笔记触发场景）
1. 新仓库默认 read-only，首次 `create_package` 被拒
2. 跨账号/跨仓库访问私有包
3. 组织命名空间推包被拒（`installation not allowed to Create organization package`）
4. 需要包级 admin/删除等更高权限
5. 本地/非 Actions 环境推送

---

## 2. PAT 选型：Classic vs Fine-grained

| 维度 | Classic PAT | Fine-grained PAT |
|------|-------------|------------------|
| 前缀 | `ghp_` | `github_pat_` |
| 权限粒度 | 粗粒度 scope（`write:packages` 覆盖该账号/组织所有包） | 细粒度，但**无 packages 权限项** |
| 过期 | 可不过期（组织可强制上限） | 最长 366 天（企业策略可更短） |
| 对 GHCR/Packages | ✅ `read:packages` / `write:packages` / `delete:packages` | ❌ **不支持** |
| 组织支持 | 需「Configure SSO」逐组织授权 | Resource owner 选组织 + 组织审批流 |
| 本场景结论 | **GHCR 场景唯一可用 PAT** | 不可用 |

> 结论：**给 GHCR 用，只能选 Classic PAT + `write:packages`。** 若组织策略禁用了 classic PAT，则只能靠 `GITHUB_TOKEN`（配合仓库 Actions 访问授权）或 GitHub App（App token 对 packages 支持也有限）。

---

## 3. 生成 Classic PAT（面向 GHCR 推送，正确路径）

> UI 路径：头像 → **Settings** → 左下 **Developer settings** → **Personal access tokens** → **Tokens (classic)** → **Generate new token (classic)**

| 配置项 | 推荐值 |
|--------|--------|
| Note | 语义化命名，如 `ghcr-push-<project>` |
| Expiration | 短期（30/60/90 天），纳入轮换 |
| Scopes | 推送：`write:packages`（UI 自动附带 `read:packages`）；私有仓库加 `repo`；删除镜像加 `delete:packages`（可选） |
| SSO | 目标组织启用 SSO 时，点 **Configure SSO → Authorize** |

**注意**：勾选 `write:packages` 时 UI 会**自动同时勾选 `repo`**（权限偏大）；纯 CI 场景优先用 `GITHUB_TOKEN` 而非 PAT。

---

## 4. Repository Secret 配置（阶段二，指南正确）

> UI 路径：仓库 **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

- **Name**: 如 `GHCR_TOKEN`（必须与 workflow 引用一致；存储时自动大写，引用大小写不敏感）
- **Secret**: 粘贴 Classic PAT（`ghp_...`）
- **约束**: 单值 ≤ 48KB；仓库级每仓库 ≤ 100 个；命名仅 `[a-zA-Z0-9_]`，不能以 `GITHUB_` 开头、不能以数字开头
- **fork 的 PR 不传 secret**（唯一例外：`GITHUB_TOKEN`）
- **CLI**: `gh secret set GHCR_TOKEN`

---

## 5. docker/login-action 兜底（阶段三，指南正确）

### 5.1 兜底表达式语义
```yaml
password: ${{ secrets.GHCR_TOKEN || secrets.GITHUB_TOKEN }}
```
- `||` 返回第一个 truthy 操作数（JS 短路语义）
- 未定义的 secret 求值为空字符串（falsy）→ 自动落到下一个候选
- 语义：**配了 GHCR_TOKEN（Classic PAT）优先用；没配则回退临时 GITHUB_TOKEN**

### 5.2 何时其实不需要兜底
- 包**已存在**且关联仓库、并在包设置「Manage Actions access」授予该仓库 write/admin 时，`GITHUB_TOKEN` 可正常推送，无需 PAT。
- 业界趋势：rust-lang、flux2 等已弃用静态 PAT，改用 `secrets.GITHUB_TOKEN`（自动注入、不过期、无需管理密钥）。

### 5.3 完整可复制 YAML
```yaml
name: Publish to GHCR

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      # 方案 A：只用 GITHUB_TOKEN（推荐）
      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      # 方案 B：兜底认证（首次建包被 read-only 拦截时的兼容写法）
      # - name: Log in to GHCR (fallback)
      #   uses: docker/login-action@v3
      #   with:
      #     registry: ${{ env.REGISTRY }}
      #     username: ${{ github.actor }}
      #     password: ${{ secrets.GHCR_TOKEN || secrets.GITHUB_TOKEN }}

      - name: Extract metadata (tags, labels)
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=tag
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## 6. 常见坑与排查

| 报错特征 | 含义 | 修复 |
|---|---|---|
| `denied: permission_denied: write_package` | 对已存在包无写权限 | workflow 加 `packages: write`；包设置「Manage Actions access」给仓库加 Write/Admin |
| `denied: permission_denied: create_package` | 无法新建包（默认 read-only） | 用 Classic PAT 兜底；或仓库 Actions 权限改 Read and write |
| `denied: ... The token provided does not match expected scopes` | **fine-grained token 的典型失败** | 换 Classic PAT + `write:packages` |
| `installation not allowed to Create organization package` | 组织命名空间创建被拒 | 组织开「Members can publish packages」；检查角色权限 |
| 推送成功但匿名拉取 401 | 包默认私有 | 包设置 → Danger Zone → Change visibility → Public（**公开后不可回退私有**） |
| 仓库删除重建后推送失败 | 旧包权限作废/孤立包 | 删孤立包；或包设置重新授权仓库 |
| fork PR 异常 | fork 不传 secret、token 只读 | 拉取场景显式 login + `packages: read`；推送场景跳过 |

**孤立包 bootstrap 死结（最高频根因）**：
- 成因：首次 push 部分成功（layer 上传、创建私有且未关联的包条目），manifest 被拒 → 留下孤立私有包；仓库重建也会复现。
- 修复：Packages 页删掉孤立包重跑；或包设置页 `.../packages/container/<包名>/settings` → **Manage Actions access** → Add Repository → Write/Admin。
- 预防：Dockerfile 加 `LABEL org.opencontainers.image.source=...` 让 GHCR 自动关联仓库。

---

## 7. 关键信源

- [About permissions for GitHub Packages — GitHub Docs](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages) — 「Packages 只支持 classic PAT」权威出处；scope 表
- [Automatic token authentication — GitHub Docs](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication) — `permissions:` 块"未列出= none"、fork 只读
- [Working with the Container registry — GitHub Docs](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) — GHCR 登录/推送、镜像命名
- [Publishing Docker images — GitHub Docs](https://docs.github.com/en/actions/publishing-packages/publishing-docker-images) — 官方 GHCR 发布 workflow 骨架
- [Configuring a package's access control and visibility — GitHub Docs](https://docs.github.com/en/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility) — 默认私有、public 不可回退、Manage Actions access
- [Using secrets in GitHub Actions — GitHub Docs](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) — Secret UI 路径、48KB、fork 不传
- [docker/login-action Issue #331](https://github.com/docker/login-action/issues/331) — fine-grained 推 GHCR 失败实证
- [github/docs Issue #33900](https://github.com/github/docs/issues/33900) — fine-grained 无 packages:read
- [github/roadmap Issue #558](https://github.com/github/roadmap/issues/558) — fine-grained 支持 Packages 路线图（未落地）
- [2023-02-02 default GITHUB_TOKEN read-only changelog](https://github.blog/changelog/2023-02-02-github-actions-updating-the-default-github_token-permissions-to-read-only/) — 2023 默认权限变更
- [Community Discussion #166194](https://github.com/orgs/community/discussions/166194) — 仓库重建 + 孤立包 write_package
- [Andrew Hoog: Grant GHCR permissions to Actions](https://www.andrewhoog.com/posts/how-to-grant-github-container-registry-permissions-to-github-actions/) — Manage Actions access 授权步骤
- [Gecko Security: GHCR Complete Guide (2026-04)](https://www.gecko.security/blog/ghcr-github-container-registry-guide) — 2026 现状综合
- [StackOverflow: GITHUB_TOKEN write package](https://stackoverflow.com/questions/70646920/) — `packages: write` 通常够用
- [flux2 commit: 弃用静态 PAT 改 GITHUB_TOKEN](https://git.oh.prosoc-portal.com/Mirrors/flux2/commit/7e8e0ab7728314c71f31d26589c1bb62776918db) — 业界迁移实例
