# 第二章：PAT 选型——为什么 GHCR 只能用 Classic PAT

## 本章要解决什么问题

原指南的第一步是「生成 Fine-grained PAT，勾选 Packages: Read and Write」。但当你真的打开 fine-grained PAT 的权限列表，会发现**根本找不到「Packages」这一项**。这不是你操作失误，而是 GitHub 压根没有给 fine-grained PAT 提供 Packages 权限模型。这一章先把 Classic 与 Fine-grained 两种 PAT 的差异讲透，再用四层证据链回答「为什么 GHCR 只能用 Classic PAT」，最后给出组织禁用 classic PAT 时的替代路径。

第一章我们认识了 `GITHUB_TOKEN` 的上限、知道了某些场景需要 PAT 兜底；本章解决的是紧接其后的选型问题：兜底时该用哪种 PAT。

---

## 1. 两种 PAT：Classic 与 Fine-grained 的分界

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

```
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

```
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
