---
title: GHCR 推送镜像权限配置
tags: [docker, GitHub, GHCR, GitHub-Actions, CI/CD, 权限]
created: 2026-08-08
updated: 2026-08-08
status: published
source_project: ghcr-push-permission
---

# GHCR 推送镜像权限配置

> [!info] 相关目录
> 本笔记属于 [[Docker MOC]]。这份笔记是一份「GHCR 推送镜像权限配置」的完整指南。它从权限模型讲起，先解释为什么 GitHub Actions 的默认 `GITHUB_TOKEN` 往往推不了包；再讲清为什么给 GHCR 用只能选 Classic PAT；随后给出一套可照做的落地配置（生成 Classic PAT → 存入 Repository Secret → workflow 兜底登录）；最后用一张排错对照表和一份自查清单，帮你把第一次推包稳稳跑通。全文以官方文档为依据，配合真实 Issue 实证与业界项目实践（rust-lang / flux2），覆盖从「为什么推不动」到「首推成功」的完整链路。

---

## 目录

1. [[#第一章：GHCR 权限模型与 GITHUB_TOKEN 的限制]]
2. [[#第二章：PAT 选型——为什么 GHCR 只能用 Classic PAT]]
3. [[#第三章：落地配置——Classic PAT + Secret + Workflow 兜底登录]]
4. [[#第四章：实战排错——首推成功与常见坑]]

---

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

> [!tip] 大白话
> 把 `GITHUB_TOKEN` 想成 GitHub 给每次 CI 跑批发的**临时工牌**：不用你申请，跑起来自动发，跑完自动作废。工牌上能干什么（读代码、推镜像）由两件事决定——公司（仓库/组织）的默认规矩，加上你在 workflow 里写的 `permissions:` 授权清单。

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

> [!tip] 大白话
> 2023 年起 GitHub 把"新房子默认上锁"了：以前新建仓库默认给你一把啥都能开的钥匙，现在默认只给"看"的权限（能看代码、能看包），想"写"（推包）必须在 workflow 里明确申请 `packages: write`。老房子不受影响，所以同样的配置在新老仓库表现不一样。

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

> [!tip] 大白话
> `permissions:` 就是这次运行的**授权清单**。GitHub 的规矩是"只认清单、不认默认"：清单里列了哪几项就有哪几项权限，**没列的一律没有**（降到 none）。所以只写 `packages: write` 而漏了 `contents: read`，连最前面的"拉代码"都会失败。

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

---

# 第二章：PAT 选型——为什么 GHCR 只能用 Classic PAT

## 本章要解决什么问题

原指南的第一步是「生成 Fine-grained PAT，勾选 Packages: Read and Write」。但当你真的打开 fine-grained PAT 的权限列表，会发现**根本找不到「Packages」这一项**。这不是你操作失误，而是 GitHub 压根没有给 fine-grained PAT 提供 Packages 权限模型。这一章先把 Classic 与 Fine-grained 两种 PAT 的差异讲透，再用四层证据链回答「为什么 GHCR 只能用 Classic PAT」，最后给出组织禁用 classic PAT 时的替代路径。

第一章我们认识了 `GITHUB_TOKEN` 的上限、知道了某些场景需要 PAT 兜底；本章解决的是紧接其后的选型问题：兜底时该用哪种 PAT。

---

## 1. 两种 PAT：Classic 与 Fine-grained 的分界

> [!tip] 大白话
> 把 PAT 想成**门禁卡**。Classic PAT 是"万能卡"：一勾 `write:packages` 就能进出该账号/组织下所有包的门。Fine-grained PAT 是"按房间授权"的卡，本来更安全——但 GitHub 根本没给"包"这个房间配刷卡口，权限列表里翻遍也找不到 Packages 这一项。所以推 GHCR 镜像，只能拿 Classic 万能卡。

### 1.1 Classic PAT（传统令牌）

- **前缀**：`ghp_`
- **权限粒度**：粗粒度 scope，`write:packages` 一勾就覆盖该账号/组织下的**所有包**
- **过期**：可以不设过期（组织可强制上限）
- **组织支持**：目标组织启用 SSO 时，需「Configure SSO」逐组织授权
- **对 GitHub Packages**：提供 `read:packages` / `write:packages` / `delete:packages` 三个 scope

### 1.2 Fine-grained PAT（细粒度令牌）

- **前缀**：`github_pat_`
- **权限粒度**：细粒度，按「Resource owner（资源所属者）+ 仓库访问范围 + 权限类别」逐项圈定
- **过期**：最长 366 天（企业策略可更短），**必须设置过期时间**
- **组织支持**：创建时把 Resource owner 选为组织，走组织审批流
- **对 GitHub Packages**：**没有 packages 权限项**

### 1.3 对比表

| 维度 | Classic PAT | Fine-grained PAT |
|------|-------------|------------------|
| 前缀 | `ghp_` | `github_pat_` |
| 权限粒度 | 粗粒度 scope（`write:packages` 覆盖账号/组织所有包） | 细粒度，但**无 packages 权限项** |
| 过期 | 可不过期（组织可强制上限） | 最长 366 天（企业策略可更短） |
| 对 GHCR/Packages | ✅ `read:packages` / `write:packages` / `delete:packages` | ❌ 不支持 |
| 组织支持 | 需「Configure SSO」逐组织授权 | Resource owner 选组织 + 组织审批流 |
| 本场景结论 | **GHCR 场景唯一可用 PAT** | 不可用 |

> [!note] 一句话记住
> Fine-grained PAT 的「细」体现在按仓库/资源圈定范围，但它的权限类别里**没有 packages**。再细的粒度也落不到「包」这个资源上。

---

## 2. 关键更正：原指南的 Fine-grained 路径不成立

原指南阶段一的原文是「生成 Fine-grained PAT，勾选 Packages: Read and Write」。这个步骤无法执行：

1. fine-grained PAT 的权限类型列表里**不存在 Packages 这一项**，没有 `packages: read` / `packages: write` 可选
2. 因此也不存在「Packages: Read and Write」这个勾选项
3. 即使强行生成 fine-grained PAT 并用于推送 GHCR，也会在登录/推送时报 scope 不匹配错误

这不是版本差异，也不是 UI 位置变了，而是平台层面的设计决定：GitHub 对 Packages 的认证只开放给 classic PAT。

> [!warning] 误区澄清
> 在 fine-grained PAT 设置页找不到 Packages 权限项，**不是操作问题**。你不需要再翻找更多二级菜单——GitHub 没有提供这一项。原指南这一步应整体替换为：生成 Classic PAT 并勾选 `write:packages`。

---

## 3. 不可用依据链：四层证据

这一节把「fine-grained 不可用于 Packages」的证据从规范到实证串成一条链，每层只回答一个问题。

### 3.1 第一层：官方文档原文（规范层）

GitHub 官方文档「About permissions for GitHub Packages」中明确写道 [About permissions for GitHub Packages — GitHub Docs](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages)：

> GitHub Packages only supports authentication using a personal access token (classic).

一个 `only` 直接封死了 fine-grained 的入口。这是整条链的规范源头，也是最权威的一层。

### 3.2 第二层：docker/login-action Issue #331（行为层）

[docker/login-action Issue #331](https://github.com/docker/login-action/issues/331) 记录了真实用户的踩坑过程：把 fine-grained PAT 的**所有**权限类别都设为 Read-write，推 GHCR 仍然报错：

```text
denied: permission_denied: The token provided does not match expected scopes
```

同一份 workflow 换成 classic PAT 后**立即成功**。这说明问题不在权限勾得多不多，而在 token 类型本身。

### 3.3 第三层：github/docs Issue #33900（解释层）

[github/docs Issue #33900](https://github.com/github/docs/issues/33900) 进一步解释了为什么 UI 里找不到选项：

> Fine-grained access tokens do not have `packages:read` permissions, even when empty.

「even when empty」点破关键：fine-grained PAT 的权限模型里**根本没有 packages 这条 scope**，连空值都不存在——所以界面上永远看不到它。

### 3.4 第四层：github/roadmap Issue #558（现状层）

[github/roadmap Issue #558](https://github.com/github/roadmap/issues/558) 是 GitHub 官方 roadmap 上「让 fine-grained PAT 支持 Packages」的提议。截至本笔记写作（2026-08），该路线图**仍未落地**。也就是说，这不是「暂时没实现、马上会有」，而是一个悬置多年的已知缺口。

### 3.5 依据链小结

```text
官方文档「only supports (classic)」        ← 规范层：权限模型只开放给 classic PAT
        ↓
docker/login-action#331「全开也失败」      ← 行为层：实际推送报 scope 不匹配
        ↓
github/docs#33900「even when empty」       ← 解释层：UI 为什么找不到选项
        ↓
github/roadmap#558「2026 仍未落地」        ← 现状层：短期不会改变
```

四层证据从不同角度指向同一个结论。

> [!note] 结论
> 给 GHCR 用，**只能选 Classic PAT + `write:packages`**（拉取 `read:packages`，私有仓库加 `repo`，删除加 `delete:packages`）。

---

## 4. 适用范围：所有 GitHub Packages 注册表

这条限制**不是 GHCR 独有**，而是 GitHub Packages 平台级的行为。以下注册表全部只认 classic PAT [About permissions for GitHub Packages — GitHub Docs](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages)：

| 注册表 | 说明 |
|--------|------|
| Container registry（GHCR） | `ghcr.io`，本笔记场景 |
| npm | `npm.pkg.github.com` |
| NuGet | `nuget.pkg.github.com` |
| Maven | `maven.pkg.github.com` |
| RubyGems | `rubygems.pkg.github.com` |

所以在任何 Packages 注册表遇到 `The token provided does not match expected scopes`，都应先怀疑是不是用了 fine-grained token。

> [!warning] 易错点
> 排查 scope 报错时，先看 token 前缀：`github_pat_`（fine-grained）直接换成 `ghp_`（classic）重试，往往比反复勾选权限更有效。

---

## 5. 组织禁用 classic PAT 时的替代路径

classic PAT 是 GHCR 的「正解」，但有些组织出于安全考虑会**全局禁用 classic PAT**。这时没有完全等价的替代，只有两条部分路径。

### 5.1 路径一：GITHUB_TOKEN + 仓库 Actions 授权（优先）

不引入 PAT，而是让 `GITHUB_TOKEN` 能用：

1. 打开包设置页 `.../packages/container/<包名>/settings`
2. 找到「Manage Actions access」
3. 点击 Add Repository，把需要的仓库加进去，授予 Write/Admin

配合第一章的 `permissions: contents: read + packages: write`，`GITHUB_TOKEN` 就能直推**已存在的包**。限制：只适用于「包已存在 + 关联到本仓库」的场景，首次建包的 bootstrap 仍可能被 read-only 卡住（详见第四章）。

### 5.2 路径二：GitHub App（支持有限）

GitHub App 的 token 对 Packages 的**支持也有限**，并不能完全替代 classic PAT。仅在组织已有现成 App 基建时作为补充，不作为默认推荐。

### 5.3 决策路径

| 组织策略 | 推荐做法 |
|----------|----------|
| 允许 classic PAT | Classic PAT + `write:packages`（第三章落地） |
| 禁用 classic PAT，且包已存在 | `GITHUB_TOKEN` + 包设置「Manage Actions access」授权仓库 |
| 禁用 classic PAT，且需首次建包 | 优先打通「Manage Actions access」+ 仓库 Actions 权限；GitHub App 为受限备选 |

> [!note] 一句话结论
> 能用 classic PAT 就用 classic PAT；不能用时退回 `GITHUB_TOKEN` + 包级 Actions 授权，GitHub App 只是有限补充。

---

## 本章小结

- Classic PAT（`ghp_`）以粗粒度 scope 提供 `read/write/delete:packages`；Fine-grained PAT（`github_pat_`）的权限类别中**没有 packages 项**，对 GitHub Packages 一律不可用。
- 原指南「Fine-grained PAT 勾选 Packages: Read and Write」不成立——该权限项不存在，强行使用会报 `The token provided does not match expected scopes`。
- 依据链四层：官方文档原句 "only supports ... (classic)" → docker/login-action#331 实证 → github/docs#33900 说明连 `packages:read` 空值都不存在 → github/roadmap#558 显示 2026 年仍未落地。
- 该限制适用于**所有** GitHub Packages 注册表（GHCR / npm / NuGet / Maven / RubyGems），不只 GHCR。
- 组织禁用 classic PAT 时：优先 `GITHUB_TOKEN` + 包设置「Manage Actions access」授权仓库；GitHub App 对 packages 支持有限，仅作补充。

下一章进入落地：生成 Classic PAT、配置 Repository Secret、用 `docker/login-action` 写兜底登录，把本章的选型结论变成一份可复制的 workflow。

---

# 第三章：落地配置——Classic PAT + Secret + Workflow 兜底登录

## 本章要解决什么问题

前两章回答了两个「为什么」：为什么 CI 的默认 `GITHUB_TOKEN` 会推不动包，为什么给 GHCR 用只能选 Classic PAT。但这套认知还停在理论层。这一章把它们落成一条可照做的链路：**生成 Classic PAT → 存进 Repository Secret → 在 workflow 里配置登录（必要时兜底）→ 完整跑通一次推送到 GHCR**。每一步都给出精确的 UI 路径和配置值，照着做就能复现，不做任何跳步。

> [!note] 本章定位
> 这是全笔记最核心的操作章，篇幅也最长。建议边读边在自己的仓库上实操，一次走完预计 1-1.5 小时。前两章是「为什么」，本章是「怎么配」，下一章再讲「配完报错了怎么查」。

---

## 1. 生成 Classic PAT

### 1.1 进入正确的入口

UI 路径：

```text
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

> [!tip] 大白话
> Secret 就是仓库的**保险箱**：把 PAT 这类敏感值锁进去，workflow 要用时用 `secrets.GHCR_TOKEN` 取。GitHub 负责加密存储，还会在日志里把值打码成 `***`，别人翻工作流日志也看不到明文。

### 2.1 UI 路径

UI 路径：

```text
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

> [!tip] 大白话
> 这是"双保险"：有自己配的门禁卡（`GHCR_TOKEN`）就刷自己的，没配就用前台发的临时卡（`GITHUB_TOKEN`）。两种都没有就空着，登录必然失败——但正常情况至少有一种。

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

---

# 第四章：实战排错——首推成功与常见坑

## 本章要解决什么问题

前三章把权限模型、PAT 选型和落地配置都讲完了，但真正第一次 `push` 时，绝大多数人还是会停在一个报错前面。这一章把所有高频坑按「现象 → 原因 → 修复」整理成一张对照表，先把最卡人的「首次建包 bootstrap 死结」单独讲透，再给一份从零到首推成功的自查清单。目标只有一个：让你第一次推包就能成功，而不是在报错里反复打转。

---

## 1. 最高频根因：首次建包的 bootstrap 死结

### 1.1 死结是怎么形成的

第一次往 GHCR 推包并不是「全有或全无」的原子操作：

1. **layer 先上传成功**：镜像的某些层会被先传上去。
2. **GHCR 先创建包条目**：此时它已经建立了一个「包」的元数据，默认 **private**、而且**尚未与任何仓库关联**。
3. **manifest 再被拒**：新仓库默认 read-only，`GITHUB_TOKEN` 没有 `create_package` 权限，最终 manifest 提交被拒。
4. **结果留下一个孤立私有包**：包条目存在，但既未关联仓库、也不完整。

这就是「死结」的关键：**第二次再推时，报错从 `create_package` 变成了 `write_package`**。包条目已经存在了，现在的问题不再是「能不能新建」，而是「对这个已存在的孤立包没有写权限」。于是进入两难：

- 新建被拒（`create_package`）
- 写入也被拒（`write_package`）

> [!tip] 大白话
> 想象第一次装修：工头先砌了墙（layer 上传成功、GHCR 建了包），结果物业以"你还没办装修许可"为由不让继续（manifest 被拒）。墙已经砌了——想重新装修？"不能新建"；想接着装？"这是违章建筑，没权限"。进退两难，只能**拆墙重来**（删孤立包），或**补办手续**（在包设置里给仓库授权）。

同一个仓库删除重建后也会复现同样的场景——旧包权限作废、留下孤立包，社区讨论 #166194 记录的正是「仓库重建 + 孤立包 write_package」这一组合 [Community Discussion #166194](https://github.com/orgs/community/discussions/166194)。

### 1.2 为什么它最容易卡人

因为**报错信息不指向根因**。你会本能地认为是 workflow 权限没配好，反复去改 `permissions:`、去换 PAT，但问题其实在 GHCR 侧已经躺着一个「半成品」包。判断方法很简单：去仓库的 Packages 页面看一眼，是否已经有一个（灰色的、未关联仓库的）包条目。

### 1.3 修复步骤（按顺序）

1. 打开仓库的 **Packages** 页面，找到那个孤立的私有包。
2. 二选一：
   - **方案 A（最干净）**：把孤立包删掉，直接重跑 workflow，让 GHCR 重新建包。
   - **方案 B（保留包）**：进入包设置页 `https://github.com/users/<owner>/packages/container/<包名>/settings`，在 **Manage Actions access** 里 **Add Repository**，选当前仓库并授予 **Write** 或 **Admin**。
3. 重跑 workflow。

方案 B 的授权路径参考 [Andrew Hoog: Grant GHCR permissions to Actions](https://www.andrewhoog.com/posts/how-to-grant-github-container-registry-permissions-to-github-actions/) 的完整操作步骤。

> [!warning] 报错
> `write_package` 往往不是一个独立的配置错误，而是「上一步残留的孤立包」造成的连锁反应。先看 Packages 页有没有残留条目，再去改权限，否则会白改一轮。

### 1.4 预防：Dockerfile 里加一行 OCI label

只要推包时带上关联 label，GHCR 会自动把包关联到对应仓库，从源头避免「孤立包」：

```dockerfile
LABEL org.opencontainers.image.source=https://github.com/<owner>/<repo>
```

关联之后，该仓库的 Actions workflow 自动获得对这个包的访问权，`create_package` 也能正常走通（详见 4.1）。

> [!tip] 修复
> 如果已经产生了孤立包，这行 label 只能「防止以后」，不能「救回过去」——已存在的孤立包仍需手动删除或按 1.3 方案 B 授权。

---

## 2. 报错对照表：现象 → 原因 → 修复

> [!tip] 使用方式
> 先按报错关键词在表里定位，看「原因」理解本质，再按「修复」操作。这张表覆盖 GHCR 推送的绝大多数常见失败。

| 报错特征（现象） | 原因 | 修复 |
|---|---|---|
| `denied: permission_denied: write_package` | 对**已存在**的包没有写权限 | workflow 加 `packages: write`；包设置「Manage Actions access」给仓库加 Write/Admin |
| `denied: permission_denied: create_package` | 无法新建包（新仓库默认 read-only） | 用 Classic PAT 兜底；或仓库 Actions 权限改为 Read and write |
| `denied: ... The token provided does not match expected scopes` | **fine-grained token 的典型失败**——它对 Packages 没有权限项 | 换 Classic PAT + `write:packages` |
| `installation not allowed to Create organization package` | 组织命名空间下创建包被拒 | 组织开启「Members can publish packages」；检查角色权限 |
| 推送成功但匿名拉取 401 | 包默认 private，还没公开 | 包设置 → Danger Zone → Change visibility → Public（**公开后不可回退私有**） |
| 仓库删除重建后推送失败 | 旧包权限作废 / 留下孤立包 | 删孤立包重跑；或包设置重新授权仓库 |
| fork PR 异常 | fork 不传 secret、token 只读 | 拉取场景显式 login + `packages: read`；推送场景跳过 |

### 2.1 先分清一对「兄弟报错」：create_package vs write_package

| | `create_package` | `write_package` |
|---|---|---|
| 含义 | 包**还不存在**，没有「创建」权 | 包**已存在**，没有「写入」权 |
| 典型时机 | 首次推送、新仓库默认 read-only | 包条目已残留 / 未授权仓库 |
| 判断方法 | Packages 页无该包 | Packages 页已有一个（半成品/孤立）包 |
| 修复 | Classic PAT 兜底，或仓库 Actions 权限放开 | 删孤立包，或 Manage Actions access 授 Write/Admin |

两者经常先后出现在同一次「未成功首推」里——先 `create_package` 被拒留下残留，再推就变 `write_package`。这就是第 1 节 bootstrap 死结的完整表现。

### 2.2 `token does not match expected scopes`：fine-grained 的典型失败

这是最容易误判的报错。第一反应通常是「scope 不够」，于是去把 fine-grained PAT 的权限全部勾成 read-write——但问题根本不在这里：

- GitHub Packages **只支持 classic PAT** 认证 [About permissions for GitHub Packages — GitHub Docs](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages)。
- fine-grained PAT 里**不存在 packages 权限项**，即使空权限也没有 `packages: read` [github/docs Issue #33900](https://github.com/github/docs/issues/33900)。
- 实测：把 fine-grained PAT 所有权限设为 read-write 后推 GHCR 依旧报此错，换 classic PAT 同一 workflow 即成功 [docker/login-action Issue #331](https://github.com/docker/login-action/issues/331)。

> [!warning] 报错
> 认前缀就能快速定位：`github_pat_` 开头 = fine-grained，直接换 classic（`ghp_` 开头）+ `write:packages`，不要浪费时间在 fine-grained 的权限页上找 packages 项。

### 2.3 `installation not allowed to Create organization package`：组织命名空间

- **现象**：往组织（org）命名空间推包被拒。
- **原因**：组织策略或账号角色权限不足——默认情况下，成员的 token 未必被允许在组织命名空间下创建包。
- **修复**：组织设置里开启 **Members can publish packages**，并确认所用账号的角色（Member / Owner）具备相应权限。

### 2.4 推送成功但匿名拉取 401：是可见性问题

- **现象**：`docker push` 成功，但换一台机器匿名 `docker pull` 报 401。
- **原因**：GHCR 新建的包**默认 private**，`push` 成功不代表可公开访问。
- **修复**：包设置页 → **Danger Zone** → **Change visibility** → 改为 **Public**。

> [!warning] 报错
> 一旦设为 public **不可回退成 private**。公开前想清楚——这不是个能随手试的操作。

### 2.5 仓库删除重建后推送失败

- **现象**：删除仓库又重建后，同一份 workflow 推包失败（常伴 `write_package`）。
- **原因**：旧包的权限随原仓库作废，重建后留下孤立包，权限没有自动迁移 [Community Discussion #166194](https://github.com/orgs/community/discussions/166194)。
- **修复**：删掉孤立包重跑，或在包设置里重新授权新仓库（同 1.3 方案 B）。

---

## 3. 边界场景：fork PR 该怎么处理

fork PR 触发的 workflow 有两条 GitHub 硬性安全规则，直接决定了「能不能推包」：

1. **secret 不传递**：fork 的 PR 不会收到仓库的 secrets，唯一例外是内置的 `GITHUB_TOKEN`。
2. **token 永远只读**：fork PR 下 `GITHUB_TOKEN` 始终只读，即使 `permissions:` 里写 `packages: write` 也无效 [Automatic token authentication — GitHub Docs](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication)。

所以对 fork PR 的处理策略是：

- **推送场景**：直接跳过。fork PR 的职责是把改动贡献回原仓库，不该也不被允许推 GHCR，别在 push job 上折腾。
- **拉取场景**：如果 fork 的 workflow 需要读取 GHCR 包，**显式 login** 到 GHCR 并声明 `packages: read`，而不是依赖隐式权限。

> [!tip] 修复
> 判断一个 job 会不会被 fork PR 触发，看触发事件即可。凡是 `pull_request` 且可能来自 fork 的 job，默认按「无 secret + 只读」设计。

---

## 4. 最佳实践与业界趋势

### 4.1 用 OCI label 做自动关联（预防性最佳实践）

推包时带上关联 label，让 GHCR 自动把镜像关联到仓库，既解决孤立包问题，也省去手动去包设置里关联：

```dockerfile
# Dockerfile 顶部或构建参数中
LABEL org.opencontainers.image.source=https://github.com/<owner>/<repo>
```

如果用了 `docker/metadata-action`，它通常会注入这一系列 OCI label（`org.opencontainers.image.source` 等），推包时透传 `labels` 即可，不需要手写。

> [!note] 核心概念
> 包一旦与仓库关联，该仓库的 workflow 就自动获得访问权。这行 label 是「让包属于仓库」的最省事方式。

### 4.2 用「Manage Actions access」替代静态 PAT

包**已存在且关联仓库**的前提下，可以在包设置页通过 **Manage Actions access → Add Repository → Write/Admin**，把当前仓库的 Actions 授权到该包。授权之后：

- `GITHUB_TOKEN` 可以直接推送，**无需 PAT** [Working with the Container registry — GitHub Docs](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)。
- 兜底表达式 `${{ secrets.GHCR_TOKEN || secrets.GITHUB_TOKEN }}` 会自动落到 `GITHUB_TOKEN`，静态 PAT 只是没人配时的备胎。

适用前提要记牢：**包必须已经建好**。首次建包仍然会被 read-only 拦截，这正是需要 PAT 兜底的唯一核心场景。

### 4.3 业界趋势：rust-lang / flux2 弃用静态 PAT

主流项目已经在往「默认 `GITHUB_TOKEN`、去掉静态 PAT」迁移，例如 flux2 的一处提交就是把静态 PAT 换成 `secrets.GITHUB_TOKEN` [flux2 commit](https://git.oh.prosoc-portal.com/Mirrors/flux2/commit/7e8e0ab7728314c71f31d26589c1bb62776918db)。原因很直接：

| | 静态 PAT | `GITHUB_TOKEN` |
|---|---|---|
| 注入方式 | 手工生成 + 存 secret | Actions 自动注入 |
| 过期 | 会过期，需轮换 | 每次运行临时、自动过期 |
| 密钥管理 | 要管（泄露面大） | 无需管理 |
| 适用 | 首次建包等兜底 | 常规推送（配合授权） |

> [!tip] 修复
> 定位静态 PAT：只作「GITHUB_TOKEN 力不能及」场景（首次建包、跨账号、本地推送）的兜底。常规 CI 推送优先走 `GITHUB_TOKEN` + Manage Actions access。

### 4.4 用 `gh secret set` 配置 Secret（CLI 兜底）

不想在 UI 上一步步点，可以在仓库根目录用 CLI 直接写入 Repository Secret，配合 workflow 里的兜底表达式使用：

```bash
# 在仓库根目录运行，默认写入当前仓库的 Actions secret
gh secret set GHCR_TOKEN

# 命令会交互式提示粘贴 PAT 值（ghp_...）
# 写入后 Secret 名自动大写；workflow 引用大小写不敏感
```

注意 Secret 命名必须与 workflow 引用完全一致（如 `GHCR_TOKEN`），并遵守命名约束：非 `GITHUB_` 前缀、非数字开头。

---

## 5. 从零到首推成功：自查清单

按顺序走一遍，每一项打勾后再推包。此清单可直接复制到 Obsidian 中勾选。

### 配置前

- [ ] 1. 确认仓库情况：2023-02-02 之后创建的新仓库默认 read-only；老仓库请在 Settings → Actions → General 确认 Workflow permissions 不是 read-only
- [ ] 2. Dockerfile 已加 `LABEL org.opencontainers.image.source=https://github.com/<owner>/<repo>`
- [ ] 3. workflow 的 `permissions:` 块写全：`contents: read` + `packages: write`
- [ ] 4. （若走 PAT 兜底）已生成 **Classic** PAT 并勾选 `write:packages`
- [ ] 5. 已用 `gh secret set GHCR_TOKEN` 或 UI 写入 Repository Secret，命名与 workflow 引用一致
- [ ] 6. 兜底表达式已写：`password: ${{ secrets.GHCR_TOKEN || secrets.GITHUB_TOKEN }}`

### 首推

- [ ] 7. 检查仓库 Packages 页无残留孤立包；有则先删除或先授权（见第 1 节）
- [ ] 8. 推送成功，无 `create_package` / `write_package` 报错
- [ ] 9. 组织命名空间：已确认组织开启「Members can publish packages」

### 发布后（如需公开访问）

- [ ] 10. 可见性确认：private 满足需求则跳过；public 需在 Danger Zone 手动修改，且**不可回退**
- [ ] 11. fork PR 相关 job 已处理：推送场景跳过，拉取场景显式 login + `packages: read`

---

## 本章小结

- 最高频根因是 **bootstrap 死结**：首次推送部分成功留下「孤立私有包」，后续报错从 `create_package` 变成 `write_package`。修复是删孤立包重跑，或包设置里 Manage Actions access 授权仓库；预防只需一行 OCI label。
- 报错对照表覆盖 7 类常见失败，核心是分清 `create_package`（建包）与 `write_package`（写已有包）、识别 fine-grained 的 scopes 报错、组织 `installation not allowed`、以及匿名拉取 401 的本质是可见性问题。
- fork PR 下 secret 不传、`GITHUB_TOKEN` 只读：推送场景跳过，拉取场景显式 login + `packages: read`。
- 业界趋势是「默认 `GITHUB_TOKEN` + Manage Actions access 授权」，静态 Classic PAT 只作首次建包等兜底场景；rust-lang、flux2 均已弃用静态 PAT。
- 把最后这份自查清单当成「从零到首推」的标准走查表：每次报错先回对照表定位，再对照清单逐项核对。

到这里，从「为什么默认凭据推不了包」到「首推成功 + 排错」的完整链路就闭环了。如果你还没做第三章的实操，建议带着本章的清单回到第三章逐项落地；如果只卡在某个报错上，直接从本章第 2 节对照表开始。

---

## 结语

这份笔记带你走完了 GHCR 推送权限配置的完整链路：先建立权限模型认知（第一章），再确定 PAT 选型（第二章），然后按可复制的 workflow 落地（第三章），最后用报错对照表和自查清单解决首推路上的高频坑（第四章）。如果只记得一条结论，那就是：常规 CI 推送优先用 `GITHUB_TOKEN` + 包级「Manage Actions access」授权，Classic PAT 仅作首次建包等兜底场景——并始终在 Dockerfile 里带上一行 `org.opencontainers.image.source` 的 OCI label。
