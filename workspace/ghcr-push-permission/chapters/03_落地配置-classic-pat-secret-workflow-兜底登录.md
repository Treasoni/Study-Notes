# 第三章：落地配置——Classic PAT + Secret + Workflow 兜底登录

## 本章要解决什么问题

前两章回答了两个「为什么」：为什么 CI 的默认 `GITHUB_TOKEN` 会推不动包，为什么给 GHCR 用只能选 Classic PAT。但这套认知还停在理论层。这一章把它们落成一条可照做的链路：**生成 Classic PAT → 存进 Repository Secret → 在 workflow 里配置登录（必要时兜底）→ 完整跑通一次推送到 GHCR**。每一步都给出精确的 UI 路径和配置值，照着做就能复现，不做任何跳步。

> [!note] 本章定位
> 这是全笔记最核心的操作章，篇幅也最长。建议边读边在自己的仓库上实操，一次走完预计 1-1.5 小时。前两章是「为什么」，本章是「怎么配」，下一章再讲「配完报错了怎么查」。

---

## 1. 生成 Classic PAT

### 1.1 进入正确的入口

UI 路径：

```
头像 → Settings → 左下角 Developer settings → Personal access tokens
     → Tokens (classic) → Generate new token (classic)
```

`Personal access tokens` 下面其实有两个入口：**Fine-grained tokens** 和 **Tokens (classic)**。上一章已经论证过：fine-grained PAT 不存在 packages 权限项，对 GHCR 完全不可用。所以这里**必须点 Tokens (classic)**，不要进错门。

> [!warning] 易错点
> 生成页面有两个入口。如果误进了 Fine-grained tokens，你会在权限列表里怎么都找不到 Packages 项——不是你没找对，是它根本不存在。GHCR 只认 classic PAT。

### 1.2 按推荐值填写

进入「Generate new token (classic)」页面后，从上到下依次是 Note、Expiration、Scopes，以及组织启用 SSO 时才出现的授权区块。推荐配置如下 [About permissions for GitHub Packages — GitHub Docs](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages)：

| 配置项 | 推荐值 | 说明 |
|--------|--------|------|
| Note | `ghcr-push-<project>` | 语义化命名，例如 `ghcr-push-my-app`，方便日后识别与回收 |
| Expiration | 30 / 60 / 90 天 | 短期 + 纳入轮换，不要把过期时间设为 No expiration |
| Scopes | 见 1.3 | 推送 `write:packages`；私有仓库加 `repo`；删除镜像加 `delete:packages`（可选） |
| SSO | 见 1.4 | 目标组织启用 SSO 时，点 **Configure SSO → Authorize** |

- **Note**：给这个 token 起一个一眼能看出用途的名字。你很可能在半年内生成好多个 PAT，`ghcr-push-<project>` 这种命名能让你在「个人设置 → Tokens」列表里快速定位，也方便到期前找到并轮换。
- **Expiration**：GitHub 支持最长不过期，但**不建议**。CI 用的静态凭据一旦泄露，影响面很大；把过期时间压到 30/60/90 天，等于强制自己定期轮换。如果组织策略允许的最短过期时间更短，以组织策略为准。

### 1.3 Scopes 怎么勾

Scopes 是这页的核心，直接决定这个 PAT 能做什么。对照下表勾选 [About permissions for GitHub Packages — GitHub Docs](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages)：

| Scope | 作用 | 何时需要 |
|-------|------|----------|
| `write:packages` | 向 GHCR 上传/推送包；勾选时 UI 自动附带 `read:packages` | 推镜像**必选** |
| `repo` | 访问仓库代码与 metadata（含私有仓库） | 仓库是 private 时建议勾；公开仓库可不勾 |
| `delete:packages` | 删除 GHCR 上的镜像 | 需要删除/清理功能时可选 |

> [!tip] 最小权限
> 如果仓库是公开的，只保留 `write:packages`（以及自动附带的 `read:packages`）就足够，把 UI 自动勾上的 `repo` 取消，收窄这个 token 的权限面。

### 1.4 SSO Configure

如果目标仓库在**启用了 SSO 的组织**下，token 生成后回到 token 列表页，这一行会出现一个 **Configure** 按钮。点它 → 在弹出的页面点 **Authorize** 授权目标组织。没有这一步，这个 PAT 在组织命名空间下推包会被拒（对应第四章的 `installation not allowed` 类报错）。

### 1.5 注意：勾 `write:packages` 会连带 `repo`

> [!warning] 权限偏大警告
> 勾选 `write:packages` 时，GitHub 的 UI 会**自动同时勾选 `repo`**。这等于给了这个 token 读写你所有可见仓库代码的权限，明显偏大。公开仓库场景下建议手动取消 `repo`；私有仓库推包则需要保留（见 1.3）。

生成完成后，页面会展示一次 `ghp_...` 开头的完整 token，**关闭后不再显示**，立刻复制保存。这个 token 就是下一步要存进 Repository Secret 的值。

> [!tip] 纯 CI 场景的提醒
> 如果你只是在 GitHub Actions 里推镜像，本章第 4 节方案 A（纯 `GITHUB_TOKEN`）是更推荐的默认做法。Classic PAT 主要在「首次建包被默认 read-only 拦截」等场景做兜底，这样你甚至不需要长期维护一个 PAT。

---

## 2. Repository Secret 配置

PAT 不能直接写死在 workflow 里，要存进仓库的 Secret。这样 workflow 用 `secrets.XXX` 引用，GitHub 负责加密存储，日志里也不会泄露明文。

### 2.1 UI 路径

UI 路径：

```
仓库 Settings → Secrets and variables → Actions → New repository secret
```

- **Name**：`GHCR_TOKEN`
- **Secret**：粘贴第 1 节复制的 `ghp_...`

> [!note] 为什么叫 GHCR_TOKEN
> 名字可以任意取，但必须与后面 workflow 里引用的 `secrets.GHCR_TOKEN` **完全一致**。取一个一眼能看出用途的名字（`GHCR_TOKEN` 就是这个项目的惯例）。命名约束见 2.2。

### 2.2 命名约束

Secret 名字不是随便写的，GitHub 有硬性约束 [Using secrets in GitHub Actions — GitHub Docs](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)：

| 约束 | 规则 |
|------|------|
| 字符集 | 仅 `[a-zA-Z0-9_]`（字母、数字、下划线） |
| 禁止前缀 | 不能以 `GITHUB_` 开头（该前缀保留给内置变量） |
| 禁止首位数字 | 不能以数字开头 |
| 大小写 | 存储时自动转大写；引用时大小写不敏感 |

命名示例：

```text
GHCR_TOKEN      ✅ 合法（推荐）
ghcr_token      ✅ 合法（存储后自动变 GHCR_TOKEN）
GITHUB_TOKEN    ❌ 保留前缀，不能用作自定义 secret 名
1GHCR_TOKEN     ❌ 数字开头
GHCR-TOKEN      ❌ 连字符不在允许字符集内
```

### 2.3 大小限制与 fork 不传

| 限制 | 数值 |
|------|------|
| 单个 secret 上限 | ≤ 48KB（一个 `ghp_...` 远小于此，正常无需担心） |
| 仓库级 secret 数量 | 每仓库 ≤ 100 个 |

另一条关键规则：**fork 的 PR 不传 secret**。从 fork 仓库发起的 PR 触发的 workflow 里，`secrets.GHCR_TOKEN` 是空值——唯一例外是内置的 `GITHUB_TOKEN`。这意味着 fork PR 场景既没有 PAT 兜底、`GITHUB_TOKEN` 又只读，推包天然失败，详见第四章的 fork 边界场景。

> [!warning] fork PR 里兜底也救不了
> 兜底表达式 `secrets.GHCR_TOKEN || secrets.GITHUB_TOKEN` 在 fork PR 里会落到 `GITHUB_TOKEN`，但 fork 的 token 永远是只读的，所以推包仍会失败。这是 GitHub 的安全隔离设计，不是配置错误。

### 2.4 CLI 方式

不想用浏览器点，可以用 `gh` 命令行（需已登录、在仓库目录内运行）：

```bash
gh secret set GHCR_TOKEN
```

运行后会提示输入 secret 值，粘贴 `ghp_...` 回车确认，等价于 UI 操作。这样也方便把 secret 的创建脚本化、纳入自动化。

---

## 3. docker/login-action 兜底登录

### 3.1 兜底表达式语义

登录这一步是整个 workflow 的「灵活开关」。核心是下面这个表达式：

```yaml
password: ${{ secrets.GHCR_TOKEN || secrets.GITHUB_TOKEN }}
```

拆开看它的语义：

- `||` 是 GitHub Actions 表达式里的「或」运算符，**返回第一个 truthy 操作数**（JS 短路语义）
- **未定义的 secret 在表达式里求值为空字符串**，空字符串是 falsy，会自动落到下一个候选
- 合起来就是：**配了 `GHCR_TOKEN`（Classic PAT）就用它；没配就回退到临时 `GITHUB_TOKEN`**

不同场景下实际用哪个凭据，看这张表：

| 场景 | `GHCR_TOKEN` | `GITHUB_TOKEN` | 实际用于登录的 |
|------|--------------|----------------|----------------|
| 配了 PAT | 有值 | 有值 | PAT（优先） |
| 没配 PAT | 空（未定义） | 有值 | GITHUB_TOKEN |
| fork PR | 空（不传） | 有但只读 | GITHUB_TOKEN（只读，推包仍会失败） |

### 3.2 何时其实不需要兜底

兜底不是必须的。以下情况 `GITHUB_TOKEN` 能直接推，连 PAT 都不用配：

- 包**已存在**，且与当前仓库**关联**
- 包设置页的 **Manage Actions access** 已把当前仓库加入并授予 **Write / Admin** 权限

满足这两条后，仓库的 workflow 用 `GITHUB_TOKEN` 就能正常推送 [Andrew Hoog: Grant GHCR permissions to Actions](https://www.andrewhoog.com/posts/how-to-grant-github-container-registry-permissions-to-github-actions/)。这也是业界趋势：rust-lang、flux2 等项目已弃用静态 PAT，改为 `secrets.GITHUB_TOKEN`（自动注入、不过期、无需管理密钥）[flux2 commit: 弃用静态 PAT 改 GITHUB_TOKEN](https://git.oh.prosoc-portal.com/Mirrors/flux2/commit/7e8e0ab7728314c71f31d26589c1bb62776918db)。

> [!tip] 建议
> 兜底是「首次建包被默认 read-only 拦截」时的过渡方案。包一旦建立并授权给仓库，就应切回纯 `GITHUB_TOKEN`（方案 A），把 PAT 删掉，减少一个需要维护的静态凭据。

---

## 4. 完整可复制的 workflow

下面这份 `publish-to-ghcr.yml` 是完整可复制的骨架，放到仓库 `.github/workflows/` 下即可。默认启用**方案 A（纯 `GITHUB_TOKEN`）**；想切方案 B 时，按文件内注释互换登录那一步。

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

> [!tip] 直接复制即可
> 这份 YAML 可以原样保存为 `publish-to-ghcr.yml`。第一次推送就用方案 B 的兜底写法更稳（详见第四章首次建包死结），包建立并授权后切回方案 A。

### 4.1 方案 B 的登录步骤

方案 B 与方案 A 的**唯一区别是登录那一步**。把方案 A 的登录步骤注释掉，换成下面这段即可：

```yaml
      - name: Log in to GHCR (fallback)
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GHCR_TOKEN || secrets.GITHUB_TOKEN }}
```

前提是你已经按第 1 节生成 PAT、按第 2 节存成 `GHCR_TOKEN`。其余步骤（metadata、build-push、cache）完全不变。

### 4.2 每个 action 在做什么

| 步骤 | Action | 作用 |
|------|--------|------|
| Checkout | `actions/checkout@v4` | 拉取仓库代码到运行环境 |
| Buildx | `docker/setup-buildx-action@v3` | 准备 Docker Buildx（多架构构建、构建缓存的基础） |
| Login | `docker/login-action@v3` | 向 GHCR 登录，之后 push 才被允许 |
| Metadata | `docker/metadata-action@v5` | 根据分支/tag/semver/sha 生成镜像 tags 与 OCI labels |
| Build & Push | `docker/build-push-action@v6` | 构建镜像并推送；`cache-from/to: type=gha` 用 GitHub Actions 缓存加速后续构建 |

几个值得注意的配置点 [Publishing Docker images — GitHub Docs](https://docs.github.com/en/actions/publishing-packages/publishing-docker-images)：

- **`permissions:` 块**：`contents: read` + `packages: write` 缺一不可。第一章讲过「未列出即 none」——只写 `packages: write` 会让 `contents` 变 none，checkout 直接失败。
- **`IMAGE_NAME: ${{ github.repository }}`**：生成 `ghcr.io/<owner>/<repo>` 形式的镜像名，这是 GHCR 的默认命名约定。若想要自定义镜像名，改这个值即可。
- **镜像名要求小写**：GHCR 镜像名必须是小写。如果仓库名含大写字母，需要先把 `IMAGE_NAME` 转成小写，否则登录/推送会被拒 [Working with the Container registry — GitHub Docs](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)。
- **`metadata-action` 的 labels 会自动带上 `org.opencontainers.image.source`**：这正是第一章讲的 OCI label 自动关联——把包关联到仓库，避免产生游离的孤立包（第四章会细讲）。
- **gha 缓存**：`cache-from: type=gha` + `cache-to: type=gha,mode=max` 让构建层缓存落到 Actions 缓存里，重复构建快很多。

### 4.3 首次推送后看什么

workflow 跑完，在 Actions 的 job 日志里找 `Build and push Docker image` 这一步，成功时会出现类似输出：

```text
The push refers to repository [ghcr.io/<owner>/<repo>]
<digest>: digest: sha256:...
<digest>: pushed
```

然后去 GitHub 仓库主页右侧的 **Packages** 区（或直接访问 `github.com/<owner>?tab=packages`），能看到刚推上去的镜像包。如果这一步报 `create_package` / `write_package` 之类的错误，先别慌——那是第四章排错章节的主战场，对照报错表定位即可。

---

## 本章小结

- 生成 Classic PAT：入口在 **Developer settings → Tokens (classic)**，推荐 `ghcr-push-<project>` 命名、30/60/90 天过期；推送勾 `write:packages`，私有仓库加 `repo`，删除镜像加 `delete:packages`，组织启用 SSO 时记得 Configure SSO。
- 勾 `write:packages` 会自动连带勾选 `repo`，权限偏大；公开仓库建议手动取消 `repo`。
- Repository Secret：`Settings → Secrets and variables → Actions`，命名 `GHCR_TOKEN`，遵循「仅 `[a-zA-Z0-9_]`、不以 `GITHUB_` 开头、不以数字开头」约束，单值 ≤ 48KB；fork PR 不传 secret；也可以用 `gh secret set GHCR_TOKEN`。
- 兜底表达式 `${{ secrets.GHCR_TOKEN || secrets.GITHUB_TOKEN }}` 按 JS 短路语义取第一个 truthy 值：配了 PAT 用 PAT，没配回退 `GITHUB_TOKEN`。
- 包已存在 + 关联仓库 + 「Manage Actions access」授权后，`GITHUB_TOKEN` 可直推，不需要兜底；rust-lang、flux2 等业界项目已弃用静态 PAT。
- 完整 workflow = checkout + buildx + login（方案 A 纯 token / 方案 B 兜底）+ metadata + build-push，`permissions` 块必须 `contents: read` + `packages: write`，build-push 记得带 `cache-from/to: type=gha`。

下一章进入排错实战：首次建包 bootstrap 死结、各种报错对照表、fork PR 边界场景，以及一份从零到首推成功的自查清单——帮你把本章搭好的链路稳稳跑通。
