# 第一章：GHCR 权限模型与 GITHUB_TOKEN 的限制

## 本章要解决什么问题

当你在 GitHub Actions 里用 `secrets.GITHUB_TOKEN` 推镜像到 GHCR，第一次大概率会遇到 `denied: permission_denied: create_package`。明明仓库就在同一个账号下，为什么推不上去？这一章先建立权限模型的整体认知，回答「为什么 CI 的默认凭据不一定能推镜像」。只有理解了 `GITHUB_TOKEN` 的定位、2023 年的默认权限变更和 `permissions:` 块的规则，后面几章的选型与配置才讲得通。

---

## 1. GITHUB_TOKEN 是什么

### 1.1 一个自动签发、自动过期的临时令牌

`GITHUB_TOKEN`（在 workflow 中以 `secrets.GITHUB_TOKEN` 引用）是 GitHub Actions 在每次 job 运行时**自动签发**的一次性令牌 [Automatic token authentication — GitHub Docs](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication)：

- **per-run 临时令牌**：每次运行创建，运行结束即失效
- **自动过期、无需管理**：不需要你手动生成、轮换或删除
- **无需在 Secret 页面配置**：它是内置变量，不像其他 secret 要手工创建

它本质上是一个「随运行环境走」的短期凭据。它的权限范围取决于两件事：仓库/组织/企业层的默认设置，以及 workflow 内的 `permissions:` 块。

> [!note] 核心概念
> `GITHUB_TOKEN` 不是用户的身份，而是「这一次 workflow 运行」的身份。它代表当前仓库在 Actions 环境下能做什么，权限上限由「默认策略 + `permissions:` 块」共同决定。

### 1.2 为什么默认凭据不「万能」

`GITHUB_TOKEN` 的权限不是固定的全读写，而是跟随策略。这正是本章后面要展开的层层收紧：**默认值**、**`permissions:` 块**、**fork 只读**，每一层都可能让推包失败。

---

## 2. 2023 默认权限变更：新对象的 GITHUB_TOKEN 默认只读

2023-02-02 起，GitHub 调整了新创建对象的 `GITHUB_TOKEN` 默认权限 [2023-02-02 默认权限变更 changelog](https://github.blog/changelog/2023-02-02-github-actions-updating-the-default-github_token-permissions-to-read-only/)：

| 时间点 | 新仓库 `GITHUB_TOKEN` 默认权限 |
|--------|-------------------------------|
| 2023-02-02 之前 | read / write |
| 2023-02-02 之后 | **read-only**（默认 `contents: read` + `packages: read`） |

关键点有两个：

1. **只影响新对象**：变更不回溯，2023-02-02 之前创建的仓库/组织不受影响
2. **`packages: read` 意味着不能写包**：`GITHUB_TOKEN` 只能读包，不能创建（`create_package`）或推送（`write_package`）

> [!warning] 易错点
> 如果你的仓库是 2023 年前创建、且从未改过默认权限，可能一直「看似正常」地推送成功。但新仓库（或新组织下的仓库）默认就是只读——同一份 workflow 换到新仓库立刻 `create_package` 被拒。问题不在你的 YAML，而在默认策略。

---

## 3. `permissions:` 块——未列出的 scope 一律是 none

### 3.1 基本写法

在 workflow 的 job 顶层显式声明权限：

```yaml
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
```

`packages: write` 是推送到 GHCR 的关键：它允许这个 job 的 `GITHUB_TOKEN` 对包做写操作（创建 + 推送）。

### 3.2 铁律：未列出即 none

一旦你写了 `permissions:` 块，**未列出的 scope 一律降为 `none`**，不再继承默认值。这是最常见的坑之一：

```yaml
# ❌ 常见错误：只声明 packages: write
permissions:
  packages: write

# 此时 contents 为 none → actions/checkout 拉代码失败
```

checkout 失败的表现：workflow 在第一步就报错，类似 `Error: fatal: could not read Username for 'https://github.com': terminal prompts disabled`——因为 `GITHUB_TOKEN` 没有 `contents: read` 权限去读仓库代码 [Automatic token authentication — GitHub Docs](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication)。

```yaml
# ✅ 正确写法：显式带上 contents: read
permissions:
  contents: read
  packages: write
```

> [!warning] 易错点
> 只写 `permissions: { packages: write }` 会让 `contents` 变 `none`，导致 `actions/checkout` 拉不到代码。凡是声明了 `permissions:`，就把依赖的 scope 全部列全——最少是 `contents: read` + `packages: write`。

### 3.3 job 级覆盖顶层

顶层 `permissions:` 与 job 级 `permissions:` 并存时，**job 级覆盖顶层**。如果顶层已经声明 `packages: write`，某个不推包的 job 可以单独收紧为只读，实现最小权限。

### 3.4 fork PR 的 `GITHUB_TOKEN` 永远只读

从 fork 仓库发起的 PR 触发的 workflow，其 `GITHUB_TOKEN` **始终只读**——即使你在 `permissions:` 里写了 `packages: write` 也无效。这是 GitHub 的安全隔离设计。所以 fork PR 场景下无法靠 `GITHUB_TOKEN` 推包，详见第四章的边界场景。

---

## 4. 包可见性与包-仓库关联

### 4.1 默认 private，public 不可回退

GHCR 新建的包**默认私有**，只有关联了仓库的包才会继承仓库的可见性。一旦手动把包设为 public，**不可再改回 private** [Configuring a package's access control and visibility — GitHub Docs](https://docs.github.com/en/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility)。

> [!warning] 易错点
> 「推送成功但匿名拉取 401」通常就是这个原因：包还是私有的。去包设置页 Danger Zone 改为 Public，但请想清楚——公开后无法回退。

### 4.2 OCI label 自动关联

包与仓库的关联可以手动设置，也可以**自动关联**：在 Dockerfile 里写 OCI label，让 GHCR 自动把包关联到对应仓库 [Working with the Container registry — GitHub Docs](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)：

```dockerfile
LABEL org.opencontainers.image.source=https://github.com/<owner>/<repo>
```

关联之后，该仓库的 Actions workflow 自动获得对这个包的访问权。这也是第四章「孤立包 bootstrap 死结」的预防手段——推镜像时带上这个 label，包就不会游离在仓库之外。

### 4.3 `GITHUB_TOKEN` 只能访问「本仓库关联」的包

`GITHUB_TOKEN` 的作用域是**当前 workflow 所在的仓库**。它能访问的只有：

- 与当前仓库关联的包
- 当前仓库命名空间下的包

跨账号、跨仓库的私有包，`GITHUB_TOKEN` 访问不了，需要额外的授权或 PAT。

---

## 5. 何时仍需用户 PAT（本笔记的触发场景）

理解上面这些规则后，「什么时候必须用 PAT」就清晰了。以下任一场景，`GITHUB_TOKEN` 都可能不够：

| 场景 | 原因 |
|------|------|
| 首次建包被拒 | 新仓库默认 read-only，`create_package` 被拒 |
| 跨账号/跨仓库访问私有包 | `GITHUB_TOKEN` 只能访问当前仓库关联的包 |
| 组织命名空间推包被拒 | 组织策略拒绝，如 `installation not allowed to Create organization package` |
| 需要包级 admin/删除等更高权限 | `GITHUB_TOKEN` 上限受默认策略约束 |
| 本地/非 Actions 环境推送 | 本地 `docker push` 没有 `GITHUB_TOKEN`，必须用 PAT 登录 |

> [!note] 核心概念
> PAT 解决的是「`GITHUB_TOKEN` 力所不能及」的场景。本笔记的主线是：先搞清楚默认凭据卡在哪（第一章），再选对 PAT 类型（第二章），最后落地配置（第三章）。

---

## 本章小结

- `GITHUB_TOKEN` 是 Actions 每次运行自动签发的临时令牌，自动过期、无需管理，权限受「默认策略 + `permissions:` 块」双重约束。
- 2023-02-02 起新仓库的 `GITHUB_TOKEN` 默认只读（`contents: read` + `packages: read`），推不了包是默认行为，不是配置错误。
- `permissions:` 块遵循「未列出即 none」：只写 `packages: write` 会让 `contents` 变 none、checkout 失败；job 级覆盖顶层；fork PR 的 token 永远只读。
- GHCR 包默认 private，public 不可回退；Dockerfile 里的 OCI label 可让 GHCR 自动关联仓库，关联后该仓库 workflow 自动获得访问权。
- `GITHUB_TOKEN` 只能访问当前仓库关联的包；首次建包、跨账号/组织、包级高权限、本地推送等场景仍需用户 PAT。

下一章将回答一个更细的选型问题：为什么 GHCR 只能用 Classic PAT，而 Fine-grained PAT 里甚至找不到 packages 权限项。
