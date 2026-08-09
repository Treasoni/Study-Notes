---
title: "第 8 章：HACS 分发"
tags:
  - HomeAssistant
  - 集成开发
  - 学习笔记
created: 2026-08-08
updated: 2026-08-08
status: 完成
source_project: home-assistant-integration
---

> [[07_测试与调试|⬅️ 上一章]] | [[HA集成开发指南|📑 目录]] | [[09_常见坑与最佳实践|下一章 ➡️]]

# 第 8 章：HACS 分发

第 7 章我们让集成通过了测试与调试，质量达标。但这只是「自己能用」；想让其他用户也能一键安装，还差最后一步——通过 HACS（Home Assistant Community Store）把集成分发出去。

> [!tip] 大白话
> HACS 就是「集成界的应用商店」。你在 GitHub 上把集成「上架」（通过 hassfest + hacs/action 校验），其他用户就能在 HACS 里搜索到它、点一下安装，就像手机上装 App 一样。本章就是走完「上架」这条路。

## 8.1 仓库根目录的 hacs.json

HACS 靠仓库根目录的 `hacs.json` 识别这个仓库装的是什么、代码放在哪。最简版本只需要一个必填字段：

```json
{
  "name": "My Awesome Integration"
}
```

`name` 是必填的显示名。其余都是可选：

| 字段 | 作用 |
|------|------|
| `content_in_root` | 代码是否直接放仓库根目录，而不是 `custom_components/` 子目录 |
| `zip_release` | 是否从 Release 的 zip 包安装（需配套 `filename` 指定包内路径） |
| `homeassistant` | 要求的最低 HA 版本 |
| `hacs` | 要求的最低 HACS 版本 |
| `persistent_directory` | 需要持久化保留的目录（更新下载时不被清掉） |

> [!note] 目录规则
> 默认 HACS 要求集成代码放在 `custom_components/<domain>/` 下，只有 `content_in_root: true` 才能直接放根目录。我们第 3 章一直遵守该结构，默认配置就够用。

## 8.2 manifest.json 至少要有 6 个必填字段

HACS 校验时，`manifest.json` 至少要包含这 6 个字段：

| 字段 | 说明 |
|------|------|
| `domain` | 唯一工号，与目录名一致（第 3 章定下，不可改） |
| `documentation` | 集成文档链接 |
| `issue_tracker` | 问题反馈入口链接 |
| `codeowners` | GitHub 维护者，格式 `@用户名` |
| `name` | 显示名 |
| `version` | 版本号 |

> [!warning] version 必须有
> 内置集成可以省略 `version`，但自定义集成在 HACS 里 `version` 是硬性必填——它既是合规校验项，也是第 8.5 节版本比对的依据。

## 8.3 双 Action 校验：上架前的质检

上架前先让两个 GitHub Action 自动检查，避免用户装到坏包。

### hassfest：HA 官方合规校验

`.github/workflows/hassfest.yaml`：

```yaml
name: Validate with hassfest

on:
  push:
  pull_request:
  schedule:
    - cron: "0 0 * * *"

jobs:
  validate:
    runs-on: "ubuntu-latest"
    steps:
      - uses: "actions/checkout@v4"
      - uses: "home-assistant/actions/hassfest@master"
```

它跟踪 HA 的 beta 通道，能在兼容性出问题前提前提醒你。

### hacs/action：HACS 自己的校验

`.github/workflows/hacs.yaml`：

```yaml
name: HACS Action

on:
  push:
  pull_request:
  schedule:
    - cron: "0 0 * * *"

jobs:
  hacs:
    runs-on: "ubuntu-latest"
    steps:
      - uses: "actions/checkout@v4"
      - uses: "hacs/action@main"
        with:
          category: "integration"
```

`category` 必填，我们是集成所以填 `integration`。两个 Action 都配好后，每次 push/PR 都会自动跑一遍，等于上架前的免费质检。

> [!tip] 大白话
> hassfest 是「平台方审核」，hacs/action 是「应用商店审核」。两个都过了，用户端才敢给你一键安装。

## 8.4 打版本：Release tag 才是版本号

HACS 以 **GitHub Release 的 tag** 作为版本来源，而不是 commit。

> [!warning] 只 push tag 不建 Release 无效
> 只打 tag 却不在 GitHub 上「Create release」是没有用的，HACS 拉不到版本。发布流程必须是：打 tag → 建 Release。
> 如果仓库还没有任何 tag，HACS 会退回用 commit 的前 7 位哈希当版本号（能看到版本，但不规范）。

> [!tip] 大白话
> Release tag 是货架上的「版本编号」。只打 tag 不建 Release，等于货架上没摆货，HACS 这个售货员拿不到东西，用户自然也无从更新。

建议的发布流程：

1. 修改 `manifest.json` 的 `version`（如 `0.1.0`）
2. `git tag v0.1.0` 并 `git push --tags`
3. 在 GitHub 仓库页为这个 tag 创建 Release

> [!note] 每仓库一个集成
> HACS 规定一个仓库只能放一个集成；有 Release 时用户端会展示最近 5 个版本。

## 8.5 HACS 怎么发现更新

用户安装后，HACS 的更新机制是这样的：

- HACS 通过 **GitHub API** 拉取你的 release 数据，约每天检查一次
- 用户已装版本存在 `manifest.json` 的 `version` 字段（HACS 记录在 `.storage/hacs.repositories`）
- 拿「当前已装版本」与「最新 release tag」比对，有新的就提示更新
- 用户下载新版本后，**必须重启 HA 才生效**

> [!warning] 未认证会被限流
> HACS 的 GitHub API 请求若未认证会被限流，导致版本陈旧。这也是「HACS 不更新」最常见的原因之一，第 9 章还会遇到。

## 最后一步：加入 brands

还有一个前置小条件：你的集成需要先加入 `home-assistant/brands` 仓库，HACS 才会收录展示。这一步通过向该仓库提交 PR 完成，具体按它的说明来即可。

## 本章小结

- `hacs.json` 是 HACS 的「上架登记表」：`name` 必填，`content_in_root`/`zip_release`/`homeassistant`/`hacs`/`persistent_directory` 按需可选。
- `manifest.json` 至少要有 6 个字段：`domain`/`documentation`/`issue_tracker`/`codeowners`/`name`/`version`。
- hassfest（`home-assistant/actions/hassfest@master`）+ hacs/action（`category: integration`）双 Action 是分发前自动质检。
- 版本取 Release tag：只 push tag 不建 Release 无效；无 tag 时退回 commit 前 7 位。
- HACS 通过 GitHub API 拉 release、约每天比对版本，未认证会限流；更新后需重启 HA 才生效。

至此，从环境搭建到测试调试再到 HACS 分发的完整链路就走通了。但上架只是开始——第 9 章我们把这些过程中最容易踩的坑集中起来，逐条给你「症状 → 原因 → 修法」。

---

---

> [[07_测试与调试|⬅️ 上一章]] | [[HA集成开发指南|📑 目录]] | [[09_常见坑与最佳实践|下一章 ➡️]]

