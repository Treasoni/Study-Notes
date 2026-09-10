# Windows 文件系统、注册表与 PowerShell - 阶段 1 探测结果

## 探测概况

- **探测时间**：2026-09-10
- **探测方式**：3 个并行 subagent，分别覆盖方向 A（文件系统）、B（注册表）、C（PowerShell）
- **候选记录**：15 条（A 5 条 / B 5 条 / C 5 条），按 canonical URL 去重后**无重复**
- **链接核验**：15/15 返回 HTTP 200（`curl -L`，2026-09-10 实测）；无失效或需登录链接
- **来源层级**：A 级（官方文档 / 一手资料）15 条；B 级 0 条；C 级 0 条
- **来源集中度**：全部来自 Microsoft Learn（含 zh-cn 本地化）。这是有意的取舍——本项目面向零基础读者且以准确为先，探测阶段只保留权威一手源；社区经验类资料留到 P2 按需定向检索（见"覆盖缺口"）

> 说明：探测阶段未纳入 B/C 级来源，意味着**实操踩坑类经验**（中文乱码、中文路径、权限报错的具体表现）目前是空白，需要 P2 补一轮定向检索。

---

## 方向菜单

用户已在 P0 确认 A/B/C 三个方向 + 串联章。本菜单的作用是在**方向内部选择侧重点与深度**，以及决定 P2 的投入规模。

### 方向 A — Windows 文件系统基础

| 子主题 | 探测覆盖情况 |
|--------|-------------|
| 卷 / 分区 / 盘符的关系 | ✅ A-1 |
| 路径规则（绝对、相对、盘符相对、UNC、保留名） | ✅ A-2（官方总集，最完整） |
| 长路径限制（MAX_PATH 260）与启用方法 | ✅ A-3 |
| NTFS 权限 ACL 与继承（查看/修改/重置） | ✅ A-4 |
| 硬链接 / 符号链接 / 目录联接 | ✅ A-5 |
| 系统目录结构（Windows / Program Files / Users / AppData…） | ⚠️ 缺零基础中文一手页 |
| 文件属性（只读/隐藏/系统）与 `attrib` | ⚠️ 未覆盖 |
| 备用数据流 ADS / EFS 加密 / NTFS 压缩 | ⚠️ 仅找到开发者向规范，缺入门页 |
| 卷标、挂载点、`dir` / `robocopy` 基础命令 | ⚠️ 未覆盖 |

### 方向 B — Windows 注册表

| 子主题 | 探测覆盖情况 |
|--------|-------------|
| 注册表是什么、为何存在 | ✅ B-1 |
| 五个根键的作用 | ✅ B-1 |
| Hive 文件磁盘位置 | ⚠️ 仅 B-1 内概述，无独立专题页 |
| 值的类型（REG_SZ / DWORD / QWORD / BINARY / MULTI_SZ…） | ✅ B-5（开发者口吻，需降维改写） |
| regedit 界面操作与 .reg 导入导出 | ✅ B-2 |
| `reg` 命令行全量参考（add/query/export/import…） | ✅ B-3 |
| 自启动 Run / RunOnce 键 | ✅ B-4 |
| 键的安全权限与所有者 | ⚠️ 仅 Win32 API 视角，零基础可读性不足 |
| 误改后的回滚 / 系统还原 | ⚠️ 缺"操作步骤级"一手页 |
| 文件关联 / 环境变量 / 系统信息等常见路径 | ⚠️ 散落各处，无独立一手页 |

### 方向 C — Windows PowerShell

| 子主题 | 探测覆盖情况 |
|--------|-------------|
| PowerShell 是什么（shell + 语言 + 配置框架） | ✅ C-2 |
| 对象模型与管道传对象 | ✅ C-1 |
| Cmdlet 动词-名词命名规范 | ✅ C-2 |
| 帮助系统 Get-Help / Get-Command / Get-Member | ⚠️ 部分落在 C-2，无独立专题 |
| Provider 与 PSDrive（含 HKLM:、Env:、Cert:） | ✅ C-5（2022 年页，概念仍有效） |
| 执行策略 ExecutionPolicy（取值、作用域、报错成因） | ✅ C-3 |
| 5.1 与 7 的差异与并存 | ✅ C-4 |
| 与 cmd / Bash 的逐项对照 | ⚠️ 无专页，需自行拼装 |
| 中文乱码、中文路径等实操踩坑 | ⚠️ 无一手源，需 C 级定向检索 |

---

## 候选资料清单

### 方向 A — Windows 文件系统

| ID | 资料 | 层级 | 日期 | 分 |
|----|------|------|------|---|
| A-1 | [本机文件系统 Local File Systems](https://learn.microsoft.com/zh-cn/windows/win32/fileio/file-systems) — 讲清卷/目录/文件三个存储组件，是理解"分区-卷-盘符"关系的地基 | A | Learn 持续更新 | 5 |
| A-2 | [命名文件、路径和命名空间](https://learn.microsoft.com/zh-cn/windows/win32/fileio/naming-a-file) — 路径规则总集：绝对/相对、盘符相对 `C:tmp.txt`、UNC、`\\?\` 扩展长度路径、保留名 CON/NUL | A | Learn 持续更新 | 5 |
| A-3 | [最大文件路径限制](https://learn.microsoft.com/zh-cn/windows/win32/fileio/maximum-file-path-limitation) — MAX_PATH 260 的由来与 32767 上限，LongPathsEnabled 与应用清单需同时满足 | A | Learn 持续更新 | 5 |
| A-4 | [icacls 命令](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/icacls) — 查看/授予/拒绝/重置 DACL，继承标记 (I)(OI)(CI)(IO)，权限掩码 F/M/RX，/T /reset 用法 | A | Learn 持续更新 | 5 |
| A-5 | [mklink 命令](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/mklink) — /h 硬链接、/d 目录符号链接、/j 目录联接的官方参数表与示例 | A | 2017-10-16（持续维护） | 4 |

### 方向 B — Windows 注册表

| ID | 资料 | 层级 | 日期 | 分 |
|----|------|------|------|---|
| B-1 | [检查 Windows 注册表（培训模块）](https://learn.microsoft.com/zh-cn/training/modules/explore-windows-architecture/4-examine-windows-registry) — 注册表为何存在、五个根键、Hive 磁盘位置（System32\config、NTUSER.DAT）、WOW6432Node | A | 未标注 | 5 |
| B-2 | [使用 Windows 注册表编辑器（培训模块）](https://learn.microsoft.com/zh-cn/training/modules/explore-windows-architecture/5-use-windows-registry-editor) — regedit 操作、.reg 格式、`regedit /s` 静默导入、导出/导入备份还原、修改前先备份 | A | 未标注 | 5 |
| B-3 | [reg 命令](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/reg) — add/query/export/import/save/restore 全量参考，/t 类型、/reg:32\|64 视图，含官方警告与先备份要求 | A | 未标注 | 5 |
| B-4 | [Run and RunOnce Registry Keys](https://learn.microsoft.com/zh-cn/windows/win32/setupapi/run-and-runonce-registry-keys) — 四个自启动键、值格式与 260 字符上限、`!`/`*` 前缀语义、安全模式被忽略 | A | 未标注 | 4 |
| B-5 | [注册表项值类型](https://learn.microsoft.com/zh-cn/windows/win32/sysinfo/registry-value-types) — REG_SZ / EXPAND_SZ / BINARY / DWORD / QWORD / MULTI_SZ 定义，易错点（null 终止符、双 null、大小端） | A | 未标注 | 4 |

### 方向 C — Windows PowerShell

| ID | 资料 | 层级 | 日期 | 分 |
|----|------|------|------|---|
| C-1 | [about_Pipelines](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_pipelines) — 管道传 .NET 对象而非文本流，ByValue / ByPropertyName 参数绑定，Get-Member 探查对象 | A | 2025-12-28 | 5 |
| C-2 | [发现 PowerShell](https://learn.microsoft.com/zh-cn/powershell/scripting/discover-powershell) — 入门首篇：shell + 脚本语言 + 配置管理框架三合一，动词-名词命名拆解，Get-Verb/Get-Command/Get-Member/Get-Help | A | 2025-09-02 | 5 |
| C-3 | [about_Execution_Policies](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_execution_policies) — 全部取值、五个 Scope 优先级、"禁止运行脚本"报错成因与修复写法 | A | 2026-08-31 | 5 |
| C-4 | [从 Windows PowerShell 5.1 迁移到 PowerShell 7](https://learn.microsoft.com/zh-cn/powershell/scripting/whats-new/migrating-from-windows-powershell-51-to-powershell-7) — 两者为独立产品且可并存（powershell.exe / pwsh.exe）、PSModulePath 合并、.NET 差异、默认 UTF-8 | A | 2024-04-02 | 5 |
| C-5 | [about_Providers](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers) — Provider 把注册表/环境变量/证书以文件系统式路径暴露，内置驱动器对照表，Get-PSProvider / New-PSDrive | A | 2022-08-29 | 4 |

---

## 来源冲突（P2 需并列保留，不得静默合并）

1. **`mklink /j` 的定义**：官方参数表定义为"目录联接（Junction）"；Microsoft Q&A 上一则回答把它描述为"指向目录的硬链接"。后者与官方"Windows 不存在目录硬链接"的定义不符。
2. **`mklink /F` 是否存在**：部分中文社区文章称 mklink 支持 `/F` 强制参数；官方参数表仅有 `/d` `/h` `/j` `/?`。

> 处理原则：以官方参数表为准，冲突说法作为"网上常见错误信息"写入易错点章节。

---

## 覆盖缺口（P2 需要补充检索）

| # | 缺口 | 建议补法 |
|---|------|---------|
| 1 | 系统目录结构（C:\Windows、Program Files (x86)、Users、ProgramData、AppData\Roaming/Local/LocalLow 的作用与区别） | 定向检索 Microsoft Learn 的 KNOWN_FOLDERID / 环境变量页，或用官方支持文档降维改写 |
| 2 | NTFS 高级特性（备用数据流 ADS、EFS 加密、NTFS 压缩及其互斥关系） | 补 `win32/fileio/file-streams` 官方页并做降维；EFS 找官方支持页 |
| 3 | 文件属性与基础命令（只读/隐藏/系统属性、`attrib`、`dir`、`robocopy`） | 补 Windows Server 命令行参考中的 `attrib` / `dir` / `robocopy` 页 |
| 4 | 注册表安全权限与所有者 | 补官方 `registry-key-security-and-access-rights`，需降维 |
| 5 | 注册表误改回滚的操作级步骤（系统还原 / 注册表导入还原） | 找官方支持文档中"操作步骤"型页面 |
| 6 | 注册表常见实用路径（文件关联、环境变量、系统信息） | 从 B-1 与官方高级用户支持文章提取 |
| 7 | PowerShell 帮助系统专题（Update-Help 限制、-Online 用法） | 补 `about_Update-Help` / `about_Get-Help` 官方页 |
| 8 | PowerShell 与 cmd / Bash 的逐项对照表 | 无官方专页，需在 P2 自行归纳成表（可标为"本文整理"） |
| 9 | 实操踩坑经验（中文乱码、中文路径、权限报错） | 定向检索 C 级社区来源，标注为"经验型"；官方侧补 `about_Character_Encoding` |

---

## P2 深度收集范围估算

- **现有可直接复用的核心源**：15 条（A 5 / B 5 / C 5），全部为 A 级且链接有效
- **需新增检索**：9 个缺口点，预计新增 8–12 条来源（其中 A 级约 8 条、C 级经验型约 2–4 条）
- **P2 预计处理规模**：
  - 精简路线（每方向 3–5 篇）：P2 处理约 12–15 篇
  - 完整路线（含全部缺口补齐）：P2 处理约 20–25 篇
- **下游影响**：按 P0 确认的"三主题各自成章 + 串联章"，大纲阶段预计 5–7 章；P2 处理规模直接决定每章素材密度

---

## 待用户决策（P1 检查点）

1. **P2 投入规模**：走精简路线（12–15 篇，够写出扎实入门笔记）还是完整路线（20–25 篇，连冷门子主题一并覆盖）？
2. **方向内取舍**：三个方向里有想重点深挖的吗？（例如 PowerShell 多花篇幅、注册表只讲安全操作）
3. **社区经验素材**：是否要补中文乱码、权限报错这类实操踩坑内容？（需要引入 C 级社区来源，会降低整体来源纯净度）
4. **系统目录结构**（AppData 等）对零基础读者价值高但缺一手中文页，是否接受"由官方参考页降维改写"的写法？
