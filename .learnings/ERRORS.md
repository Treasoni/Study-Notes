# ERRORS.md

## [ERR-20260816-003] 文本处理：perl 中文正则静默失败（no-op 无报错）

### 错误：perl 脚本按中文章节号拆分文档，执行后报告无变化，实为字符类未匹配

**错误**：第一次 perl 拆分脚本用 `-CSD` 但未 `use utf8`，`[一二三四五六七]` 字符类按字节匹配，匹配数为 0，脚本无任何报错地空跑。

**触发场景**：用 perl 处理含中文的 Markdown 文本拆分。

**根因**：perl 源码字面量默认按字节处理；中文字符类匹配不到 UTF-8 字节流；脚本逻辑在「匹配为 0」时输出无变化并成功退出。

**修复**：
- 脚本头部加 `use utf8;` 与 `use open ":std", ":encoding(UTF-8)"`。
- 文件句柄显式 `:encoding(UTF-8)`。
- 成功：8 段、74 defs、0 重复。

**预防措施**：
- perl 处理非 ASCII：必须 `use utf8` + 标准 IO/句柄 `:encoding(UTF-8)`；对含中文的脚本先跑小样本断言匹配数>0。

---

## [ERR-20260831-004] note-updater：编造 OpenClash 可从 Passwall SourceForge 源安装的错误方法

### 错误：笔记写 `opkg install luci-app-openclash`（指向 passwall 源），实际该源不含 OpenClash，用户按教程必然装不上

**错误**：iStoreOS 爬梯笔记的 §4.2 方案 A 把 OpenClash 写成可从 `openwrt-passwall-build` SourceForge feed 安装，且版本号写成 `v0.47.096-beta`。

**触发场景**：更新 OpenWrt/iStoreOS 代理插件安装教程，凭印象补依赖与来源。

**根因**：未核实 feed 实际内容；把 passwall 源与 OpenClash 混为一谈。

**修复**：
- 删除错误步骤，替换为已核实的社区一键脚本（`slobys/openclash-auto-installer`，默认分支 `main`）。
- 用 GitHub API 核实 SourceForge feed 只含 passwall_luci / passwall_packages / passwall2。

**预防措施**：
- 写第三方插件安装步骤前，必须列出目标源的真实包清单（opkg 源查 feed 目录，GitHub 用 API 列 release assets）；`opkg list | grep <插件>` 为空即不可用。

---

## [ERR-20260831-005] note-updater：`.run` 包示例 URL 三处错误（路径/架构/SDK）且未区分 24.10

### 错误：示例 `AUK9527/Are-u-ok/raw/main/apps/PassWall2/PassWall2_x86_64_all_sdk_24.10.run` 路径、架构、SDK 全错

**错误**：方案 C 引用 AUK9527 主仓库 `apps/` 路径，实际该目录只有 aarch64(a53) 22.03 包；24.10 包在 bcseputetto/Are-u-ok 的 `iStoreOS_24.10` Release，且文件名含 `_sdk_24.10`（OpenClash 为 `+x86_64_core` 内置内核格式）。

**触发场景**：写「通过 iStore 手动安装 .run」方案时按网上教程惯例猜 URL。

**根因**：未核实仓库 README（AUK9527 README 明确标注 22.03 / x86_64 在 `x86/` 分支、24.10 已移交 bcseputetto）。

**修复**：
- 改为 `github.com/bcseputetto/Are-u-ok/releases/download/iStoreOS_24.10/PassWall2_26.8.27_x86_64_all_sdk_24.10.run` 等真实文件名。
- 更正「方案 C 是 x86_64 首选」的前提，标注该库覆盖的架构与 SDK。

**预防措施**：
- 示例下载 URL 必须来自实际存在的文件：先 `curl api.github.com/.../contents` 列目录，再写进笔记；注明「以 Release 页实际为准」。

---

## [ERR-20260831-006] note-updater：用户要求「删掉」时仍在打补丁

### 错误：用户指出 iStore 商店无法安装 Passwall/OpenClash 后，我加 warning 补丁保留误导步骤，用户回复「不行就删掉啊」

**错误**：对无效的「通过 iStore 搜索安装」步骤，第一次只加警告标注，未删除。

**触发场景**：用户纠正内容错误且语气明确（「不行就删掉啊」）。

**根因**：倾向最小改动，未把用户「这是错的」当成「删除该内容」的指令。

**修复**：
- 直接删除「通过 iStore 安装」整节，重排编号。
- 经验：用户对误导内容说「删掉」时，删除比标注更符合预期。

**预防措施**：
- 用户明确否定某段内容时，优先直接删除该段（保留关键提示），不要用 warning 打补丁。

---
