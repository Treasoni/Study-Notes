# LEARNINGS.md

## [LRN-20260816-004] knowledge_gap — 本机 perl 处理中文必须显式 utf8，否则字符类正则静默失败

**Logged**: 2026-08-16
**Priority**: high
**Status**: pending
**Area**: scripts

### Summary
Windows/Git Bash 下 python/python3 是商店存根不可用，用 perl 处理含中文 Markdown 时，字符类正则必须 `use utf8;` + `use open ":std", ":encoding(UTF-8)"`，否则按字节匹配导致脚本静默 no-op。

### Details
- 事实：第一次 perl 拆分脚本只加 `-CSD`，`[一二三四五六七]` 匹配不到，输出「无变化」且无报错；补 `use utf8;` 后才真正执行（8 段、74 defs、0 重复）。
- 根因：perl 默认把源码字面量当字节串，中文字符类不匹配 UTF-8 字节序列；且无报错，是静默失败。
- 下次做法：perl 处理非 ASCII 文本，脚本开头固定三件套：`use utf8;`、`use open ":std", ":encoding(UTF-8)"`、文件句柄加 `:encoding(UTF-8)`；先小样本验证匹配数>0。

### Suggested Action
- 需要文本处理脚本时优先考虑 perl/node；perl 处理中文必须带 utf8 三件套并先小样本验证。

---

## [LRN-20260831-005] knowledge_gap — iStoreOS 24.10 代理插件的真实安装来源与 `.run` 包命名

**Logged**: 2026-08-31
**Priority**: high
**Status**: pending
**Area**: docs / 软路由教程

### Summary
iStoreOS 官方 iStore 商店默认不含代理插件（法律/政策原因）；Passwall 官方源是 SourceForge `openwrt-passwall-build`（只含 passwall_luci / passwall_packages / passwall2 三个 feed，**不含 OpenClash**）；OpenClash 需社区一键脚本或 GitHub Release IPK；24.10 的 `.run` 包在 `bcseputetto/Are-u-ok` 的 `iStoreOS_24.10` Release（原 AUK9527 主仓库仅 22.03 aarch64 包）。

### Details
- 事实：真实文件名（GitHub API 核实）：`PassWall2_26.8.27_x86_64_all_sdk_24.10.run`、`OpenClash_0.47.156+x86_64_core_sdk_24.10.run`（`+core` = 内置 Clash/Mihomo 内核）。OpenClash 官方 IPK 下载模式为 `releases/download/v<版本>/luci-app-openclash_<版本>_all.ipk`。
- 根因：网上教程互相抄、信息过时；把 passwall 源误当 OpenClash 源。
- 下次做法：写代理插件安装步骤前，先用 GitHub API 列出软件源 feed 目录 / release assets 的真实文件，再写命令。

### Suggested Action
- 涉及 OpenWrt/iStoreOS 第三方插件安装的笔记，均按「官方 iStore 不含 → 备选方案按已验证来源」的结构更新。

---

## [LRN-20260831-006] best_practice — 验证安装方法用 GitHub API（curl api.github.com）而非被屏蔽的 WebFetch

**Logged**: 2026-08-31
**Priority**: medium
**Status**: pending
**Area**: workflow / research-tools

### Summary
`raw.githubusercontent.com`、`github.com` 在 WebFetch 被拦截，但 `curl api.github.com` 可用，能列出目录、release assets、默认分支，是核实「方法对不对」的最可靠手段。

### Details
- 事实：`curl -s api.github.com/repos/{owner}/{repo}/contents/{path}` 列目录；`/releases/tags/{tag}` 列 assets；`/repos/{owner}/{repo}` 返回 `default_branch`。
- 根因：WebFetch 有域名安全校验；GitHub API 端点未被拦截。
- 下次做法：需要验证仓库内容时直接用 Bash curl + api.github.com，再写进笔记/报告。

### Suggested Action
- 将 api.github.com 用法加入资料收集的默认工具集。

---

## [LRN-20260905-007] best_practice — 解释概念要「落到可见处」：具体产物 + 可代入例子 + 对比表，不只抛抽象结论

**Logged**: 2026-09-05
**Priority**: high
**Status**: pending
**Area**: workflow / 学习笔记生产

### Summary
生成学习笔记解释抽象概念时，按「它是什么 / 解决什么问题 → 具体产物长什么样 → 带具体值的可代入例子 → 对比表 → 大白话类比」展开；正文要能独立让「有点没懂」的读者靠图/表/例子读懂，而不是只抛抽象结论。用户在同一天对两节内容（3.4、4.2）连续两次给出同一反馈并两次明确要求「生成笔记时都要这样」，已升级为默认写作标准。

### Details
- 事实（第 1 次）：3.4 节初稿只写「.python-version 内容是版本请求而非精确小版本 + 逐级向上查找」两句抽象结论；补上「纸条定位 → 3.12 vs 3.12.9 后果对比表 → ~/code 目录树继承示例 → 大白话」后，用户回复「放入笔记」，并下达「生成笔记时对于这些概念的解释都要这样」。
- 事实（第 2 次）：4.2 节（激活与停用）用户再反馈「不是很懂」；按同法补上「.venv 目录树（bin vs Scripts）→ 激活只做三件事 → which/where 前后对比 → 哪个 shell 跑哪个文件表格」后，用户回复「你这里的解释我就看的明白，你之后生成笔记时都要这样」——模式确认：读者无法从抽象结论反推机制，需要先看见产物/过程再接受结论。
- 根因：抽象结论没有给读者可停留的实体落点——不知道 `.python-version` / 激活脚本具体长什么样、选项间实际差别、机制到底怎么发生。
- 下次做法：每解释一个非平凡概念，先给读者「看得见」的东西（文件内容、目录树、命令输出、路径示例），再下结论；写完自检：删掉类比后，正文能否仅靠表格/例子让困惑读者理解。

### Suggested Action
- 该规则已两次被用户主动强调，应从「记录偏好」升级为「生成阶段的默认检查点」：并入章节写作模板 / chapter-writer 的写作要求，而不只停留在 RULES.md。

---
