# Windows 文件系统、注册表与 PowerShell - 深度素材（阶段 2）

> 运行标识：`windows-file-system-registry-powershell`
> 生成时间：2026-09-10
> 上游：`01_explore_result.md`（P1 探测结果）+ 用户 P1 决策（完整路线 / 三方向均衡 / 允许 C 级经验素材 / 接受降维改写）
> 本文件是 P3 大纲生成与 P4 逐章写作的**唯一素材入口**

---

## 0. 使用方式

- 主体由三个方向的部分素材拼装而成，每个方向内部结构一致：**来源表 → 论断/来源映射 → 矛盾与冲突 → 可操作指引 → 需要降维改写的内容 → 未解决问题与缺口 → 下游交接摘要**。
- **论断条目都带来源 ID**，格式为 `→ [S12]` 这类引用。写作时引用素材请沿用这些 ID，方便回溯。
- 带 `C 级 · 经验型` 标记的条目**只能用于描述"现象"**，不能作为原理依据；其原理对应项已在正文中配对。
- 标注"本文整理"的条目（如 cmd/Bash 对照表）无单一官方出处，其依据来源已在条目内注明。
- 标注"降维改写"的来源（如 KNOWN_FOLDERID）是开发者向官方页，零基础表述需按第 5 节的改写方向重写。

---

## 1. 收集概况与统计

| 指标 | 值 |
|------|-----|
| 来源条目总数 | 67 条 |
| 去重后唯一 URL | 65 个 |
| A 级（官方一手资料） | 63 条 |
| 本文整理（无单一官方出处） | 1 条 |
| C 级（社区经验型） | 3 条 |
| 抓取尝试 / 成功 / 失败 | 64 / 60 / 4 |
| 精读缓存 | `_cache/`（44 个页面 Markdown，供复现） |

**方向分布**

| 方向 | 来源条目 | 唯一 URL | 层级 | 论断条数 | 部分文件 |
|------|---------|---------|------|---------|---------|
| A — Windows 文件系统 | 21 | 21 | 全 A 级 | 40 | `_p2_part_A.md` |
| B — Windows 注册表 | 27 | 27 | 全 A 级 | 40 | `_p2_part_B.md` |
| C — Windows PowerShell | 19 | 18 | A 级 15 · 本文整理 1 · C 级 3 | 38 | `_p2_part_C.md` |

三方向素材密度对齐（40 / 40 / 38 条论断），符合 P1 确认的"三者均衡"约束。

---

## 2. 环境与来源质量提示

采集过程中发现的、影响素材可信度的事实，写作时应知晓：

1. **Learn 页面的"访问此页面需要授权"横幅**：多个 Microsoft Learn 页面抓取后带此横幅，但正文完整。判断为站点模板噪声，**不影响结论**。
2. **培训模块页无法直接抓取**：P1 的 B-1、B-2 两条培训模块（"检查 Windows 注册表""使用注册表编辑器"）无论是 zh-cn 还是 en-us，抓取后只返回课程目录页（74–182 字），无法取得正文。已替换为等价官方页并在来源表中记录替换关系。
3. **部分 P1 链接在 P2 阶段失效**：`checkpoint-computerrestore` 多个 view 参数下 404；`sysinfo/accessing-an-alternate-registry-view` 的 P1 路径 404（正确路径在 `winprog64` 下）。已用 en-us 等价页替换。**P1 的 15 条链接当时实测均为 200，说明 Learn 页面路径会随时间变动**——后续如需复现，优先用来源表中的实际 URL 而非 P1 清单。
4. **C 级来源的取得率偏低**：知乎 403 反爬、CSDN 反爬 2 次、cnblogs 返回空页。最终仅 3 条社区来源成功抓取，均已标注。
5. **管理员权限标注的完整性不一致**：注册表方向指出 `reg.exe` 各子命令是否需要管理员权限**官方全未明示**；文件系统方向的 `compact` / `cipher` / `mountvol` / `robocopy` 同样未说明。素材中此类项已逐条标"官方未说明"，**不得自行推断后在笔记中断言**。

---

## 3. 跨方向关键冲突与判断（写作时须遵守）

三个方向各自记录了自己的矛盾（见各部分第 3 节）。以下是**影响写作口径**的跨方向要点：

| # | 冲突 | 写作口径 |
|---|------|---------|
| 1 | **系统还原是否可作为注册表回滚主路径**：官方页正文称系统还原"仅在 Windows 7/Vista/XP 受支持"，但其"适用于"与 cmdlet 在 Win10/11 仍存在；另一份适用于 Win11 的官方页通篇不提系统还原 | **不把系统还原写成回滚主路径**。主路径是"导出 .reg → 需要时导入还原"；系统还原只作为整机级兜底提及 |
| 2 | **"备份整个注册表"含义不统一**：一处指向"备份系统状态"（整机快照），另一处指向 regedit 导出/导入（按键） | 两者分开写清：**按键级备份**用导出，**整机级**才提系统状态备份 |
| 3 | **HKCU 磁盘文件位置**：两份官方资料分别给 `System32\Config` 与 `%SystemRoot%\Profiles\Username`（Win2000/XP 时代布局），**都没提现代的 `C:\Users\<用户>\NTUSER.DAT`** | **不写死路径**（无来源支持现代路径）。只写"`NTUSER.DAT` / `NTUSER.DAT.LOG` 属于用户配置文件 hive"，磁盘位置以"用户配置文件目录"表述——此口径以素材方向 B 第 3 节为准，修正了本表早期版本误要求写现代路径的错误 |
| 4 | **`FOLDERID_ProgramFilesX86` 默认路径自相矛盾**（同页条目栏 vs 备注表） | 只写"64 位系统上为 `Program Files (x86)`"，不引入矛盾细节 |
| 5 | **`mklink /j` 的定义**（P1 已发现）：官方参数表为"目录联接"，社区误称"目录硬链接" | 以官方参数表为准；社区说法写进易错点 |
| 6 | **`mklink /F` 是否存在**（P1 已发现）：社区称支持，官方参数表仅有 `/d` `/h` `/j` `/?` | 官方为准；作为"网上常见错误信息"写进易错点 |
| 7 | **执行策略是否等于安全边界**：社区普遍当作安全方案，官方明说**它不是安全边界** | 按官方口径写：执行策略是**防误运行的便利机制**，不是安全防护 |
| 8 | **编码"单一默认值"不存在**：5.1 的官方页在同页内自相矛盾 | 写成"三条独立编码通道"（脚本源码编码 / `-Encoding` 参数 / 控制台与对外程序编码），不写"改一个设置就好" |
| 9 | **`AllSigned` 建议**：社区建议用 AllSigned，官方默认是 RemoteSigned | 按官方默认写，AllSigned 作为可选更严档位提及 |

---

## 4. 对下游（P3 大纲）的直接影响

1. **章节骨架已具备**：三个方向各有 7 节结构的完整素材，且各有"下游交接摘要"，可直接支撑"三主题各自成章 + 串联章"的结构。
2. **串联章素材来源**：方向 B 的第 2.10 节（三种执行方式：regedit / reg.exe / PowerShell）与方向 C 的第 2.10 节（文件系统与注册表常用 Cmdlet）是串联章的核心骨料。
3. **降维改写工作量集中点**：文件系统方向的第 5 节（命名空间 / Win32 术语）、注册表方向的第 5 节（13 项 hive/ACL/掩码术语）、PowerShell 方向的第 5 节（.NET 对象 / 参数绑定）——这些是零基础读者最容易卡住的地方，大纲应为其预留足够篇幅，或在大纲阶段就标注"需配类比说明"。
4. **必须配 Callout 的位置**：注册表方向第 4.4 节的"编辑前官方风险 checklist"已标注可直接做成 Callout。

---

## 方向 A — Windows 文件系统（精读素材）


### 1. 来源表

| ID | 标题 | URL | 层级 | 页面日期 | 抓取日期 | 支撑的子主题 |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | 本地文件系统（Win32 apps，zh-cn） | https://learn.microsoft.com/zh-cn/windows/win32/fileio/file-systems | A | 2025-07-10 | 2026-09-10 | 核心概念：卷/目录/文件 |
| A2 | 命名文件、路径和命名空间（zh-cn） | https://learn.microsoft.com/zh-cn/windows/win32/fileio/naming-a-file | A | 2024-08-28 | 2026-09-10 | 命名规则、保留字符、命名空间 |
| A3 | 最大路径长度限制（zh-cn） | https://learn.microsoft.com/zh-cn/windows/win32/fileio/maximum-file-path-limitation | A | 2024-11-21 | 2026-09-10 | MAX_PATH、长路径启用 |
| A4 | icacls（zh-cn） | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/icacls | A | 2025-08-16 | 2026-09-10 | 权限（DACL）读写 |
| A5 | mklink（zh-cn） | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/mklink | A | 2025-07-13 | 2026-09-10 | 链接：符号链接/硬链接/交接点 |
| A6 | KNOWNFOLDERID（zh-cn）· **降维改写** | https://learn.microsoft.com/zh-cn/windows/win32/shell/knownfolderid | A | 2023-06-13 | 2026-09-10 | 系统目录结构与环境变量对应 |
| A7 | 识别的环境变量（USMT，zh-cn）· **降维改写** | https://learn.microsoft.com/zh-cn/windows/deployment/usmt/usmt-recognized-environment-variables | A | 2025-01-29 | 2026-09-10 | Users/Public/ProgramData/AppData 路径 |
| A8 | 文件流（本地文件系统，zh-cn） | https://learn.microsoft.com/zh-cn/windows/win32/fileio/file-streams | A | 2025-07-10 | 2026-09-10 | NTFS 备用数据流（ADS） |
| A9 | attrib（zh-cn） | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/attrib | A | 2025-08-16 | 2026-09-10 | 文件属性 |
| A10 | robocopy（zh-cn） | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/robocopy | A | 2025-08-16 | 2026-09-10 | 复制/备份命令与坑 |
| A11 | mountvol（zh-cn） | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/mountvol | A | 2025-08-16 | 2026-09-10 | 卷装入点 |
| A12 | dir（zh-cn） | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/dir | A | 2025-08-16 | 2026-09-10 | 目录列举与隐藏文件 |
| A13 | compact（zh-cn） | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/compact | A | 2025-08-16 | 2026-09-10 | NTFS 压缩 |
| A14 | NTFS 概述（zh-cn） | https://learn.microsoft.com/zh-cn/windows-server/storage/file-server/ntfs-overview | A | 2025-08-16 | 2026-09-10 | NTFS 能力、卷/群集上限 |
| A15 | diskpart（zh-cn） | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/diskpart | A | 2025-08-16 | 2026-09-10 | 分区/卷/盘符管理 |
| A16 | cipher（zh-cn） | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/cipher | A | 2025-08-16 | 2026-09-10 | EFS 加密命令 |
| A17 | Sparse File Operations（en-us，替换 zh-cn 缺页） | https://learn.microsoft.com/en-us/windows/win32/fileio/sparse-file-operations | A | 2022-01-26 | 2026-09-10 | 稀疏文件原理 |
| A18 | fsutil（zh-cn） | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil | A | 2025-03-05 | 2026-09-10 | 稀疏文件/重分析点子命令总入口 |
| A19 | 硬链接和交接点（zh-cn） | https://learn.microsoft.com/zh-cn/windows/win32/fileio/hard-links-and-junctions | A | 2025-07-08 | 2026-09-10 | 硬链接 vs 交接点语义 |
| A20 | fsutil sparse（zh-cn） | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/fsutil-sparse | A | 2025-08-16 | 2026-09-10 | 稀疏文件命令 |
| A21 | 文件加密 / EFS（zh-cn） | https://learn.microsoft.com/zh-cn/windows/win32/fileio/file-encryption | A | 2025-07-10 | 2026-09-10 | EFS 与压缩互斥 |

层级分布：A 级 21 条，B 级 0 条，C 级 0 条。全部为 Microsoft Learn 官方文档（一手资料）。A6、A7 为按任务要求做的"降维改写"来源（原页面是给部署工程师/开发者的，无零基础中文页）。A17 为 zh-cn 缺页后改用 en-us 等价页，已在标题中标注替换。

---

### 2. 论断 / 来源映射

#### 子主题一：文件系统的基本结构（卷 / 目录 / 文件）

1. Windows 支持的所有文件系统共用三个存储组件：**卷**是"目录和文件的集合"，**目录**是"目录和文件的分层集合"，**文件**是"相关数据的逻辑分组"；组织层级最高一级是卷，文件系统"驻留在卷上"。且**目录在文件系统层面就是一种"具有特殊属性的文件"**，因此"必须像常规文件一样遵循所有命名规则"——文件名的规则同样约束目录名。锚点：A1「本地文件系统」→"Windows 支持的所有文件系统具有以下存储组件"；A2「文件和目录名称」→ [A1][A2]
2. NTFS 是新版 Windows 的默认文件系统，提供"安全描述符、加密、磁盘配额和支持丰富的元数据"。锚点：A14「NTFS 概述」首段 → [A14]

#### 子主题二：命名规则、路径与命名空间

3. 9 个保留字符不能用于文件名：`< > : " / \ | ? *`，外加整数值 0（NUL 字符）；反斜杠是"将名称分隔成组件的保留字符"。锚点：A2「命名约定」→"以下保留字符" → [A2]
4. 一批**保留设备名**不能用作文件名：`CON、PRN、AUX、NUL、COM1–COM9、LPT1–LPT9`，"另请避免这些名称紧跟扩展名"（`NUL.txt` 等效于 `NUL`）；但字符码 **1–31 "在备用数据流中允许使用"**——流名称的规则与文件名称不同。锚点：A2「命名约定」→ [A2]
5. 文件或目录名**不要以空格或句点结尾**（"Windows Shell 和用户界面不支持"）；大小写不敏感，"将名称 OSCAR、Oscar 和 oscar 视为相同"，驱动器号同理（`D:\` 与 `d:\` 同一个卷）。锚点：A2「命名约定」→ [A2]
6. 路径前缀决定解释方式："如果文件名不以下列项之一开头，则其与当前目录相对应"（UNC、`C:\`、`\` 三者例外）；**`C:tmp.txt` 指"驱动器 C 上当前目录中"的文件，与 `C:\tmp.txt` 不同**；`.`/`..` 分别表示当前目录与父目录。锚点：A2「完全限定与相对路径」→ [A2]
7. 三种前缀的用途：`\\?\` "告知 Windows API 禁用所有字符串分析，并将其后面的字符串直接发送到文件系统"；`\\.\` 进入 Win32 设备命名空间，是"直接访问物理磁盘和卷的方式，而无需通过文件系统"；NT 命名空间是"最低级别命名空间"，其中 Win32 的 `C:` 只是"指向 HarddiskVolume1 的符号链接"。锚点：A2「Win32 文件命名空间 / Win32 设备命名空间 / NT 命名空间」→ [A2]
8. 长文件名之外 Windows 还会生成 8.3 短名（形如 `T97B4~1.TXT`），但"**不要假设磁盘上已存在 8.3 别名**"（可被禁用）；在 NTFS/exFAT/UDFS/FAT32 上长名以 Unicode 存储，所以"原始长文件名始终被保留"。锚点：A2「短与长名称」→ [A2]

#### 子主题三：最大路径长度限制

9. 传统上限是 **MAX_PATH = 260 个字符**，构成是"驱动器号、冒号、反斜杠、用反斜杠分隔的名称组件和终止 null 字符"；Unicode 版 API 支持**扩展长度路径，最大约 32,767 个字符**，条件是 `\\?\` 前缀（UNC 路径用 `\\?\UNC\`），且该 32767 是近似值。锚点：A3「最大路径长度限制」→ [A3]
10. `\\?\` 前缀下行为特殊：**不能用正斜杠作分隔符，不能用 `.` 表示当前目录，也不能用 `..` 表示父目录**；"相对路径总字符数始终不能超过 MAX_PATH"；用 API 创建目录时"目录名不能超过 MAX_PATH 减 12"（要留 8.3 名空间）。锚点：A3「最大路径长度限制」→ [A3]
11. Windows 10 1607 起许多 Win32 文件/目录函数移除 MAX_PATH 限制，但**应用必须显式选择支持**，需同时满足两个条件：注册表 `HKLM\SYSTEM\CurrentControlSet\Control\FileSystem` 下 `LongPathsEnabled`(REG_DWORD)=`1`，且应用清单含 `longPathAware`。此值"按进程缓存"，"可能需要重新启动"。锚点：A3「在 Windows 10 版本 1607 及更高版本中启用长路径」→ [A3]
12. Shell 与文件系统要求不同："**可以使用 Shell 用户界面无法正确解释的 Windows API 来创建路径**"——资源管理器打不开的路径可能存在。锚点：A3「最大路径长度限制」→ [A3]

#### 子主题四：系统目录结构（C:\Windows、Program Files、Users、ProgramData、AppData）

> 本子主题来源 A6/A7 是开发者/部署视角的官方参考页，路径事实为 A 级，但表述需降维（见第 5 节）。

13. 用户配置文件目录 `%USERPROFILE%` = `%SystemDrive%\Users\%USERNAME%`（`FOLDERID_Profile`）；其下的 **`AppData` 分三个子目录**：`Roaming`（`%APPDATA%` = `%USERPROFILE%\AppData\Roaming`）是"用作应用程序特定数据的通用存储库"；`Local`（`%LOCALAPPDATA%`）是"充当本地非漫游应用程序的数据存储库"；`LocalLow` = `%USERPROFILE%\AppData\LocalLow`，**没有 CSIDL 等效项**。三者文件夹类型均为 PERUSER（每个用户各一份）。锚点：A6 三条 KNOWNFOLDERID + A7「CSIDL_APPDATA / CSIDL_LOCAL_APPDATA」→ [A6][A7]
14. **全机器共用的两个目录**：`ProgramData`（`%ALLUSERSPROFILE%` = `C:\ProgramData`）是"包含所有用户的应用程序数据的文件系统目录"，XP 时代旧路径为 `%ALLUSERSPROFILE%\Application Data`；`Public`（`%PUBLIC%` = `C:\Users\Public`）是"Windows Vista 新增功能"，"无 CSIDL 等效项"，其下按类型分为 `Public\Documents`、`Desktop`、`Music`、`Pictures`、`Videos`、`Favorites`。二者文件夹类型为 FIXED。锚点：A6「FOLDERID_ProgramData / FOLDERID_Public」+ A7「CSIDL_COMMON_APPDATA」→ [A6][A7]
15. `C:\Windows`（`%windir%`，`FOLDERID_Windows`）与 `System32`（`%windir%\system32`）的路径映射；**64 位系统上 `FOLDERID_SystemX86` 解析为 `%windir%\syswow64`**。锚点：A6「FOLDERID_Windows / FOLDERID_System」+ A7「WINDIR / CSIDL_SYSTEM」→ [A6][A7]
16. `Program Files`（`FOLDERID_ProgramFiles`）= `%ProgramFiles%` = `%SystemDrive%\Program Files`。**`Program Files (x86)` 只存在于 64 位系统**：32 位系统上 `FOLDERID_ProgramFiles` 与 `FOLDERID_ProgramFilesX86` **都**指向 `Program Files`；64 位系统上后者才指向 `Program Files (x86)`；64 位 OS 上运行 32 位应用时 `FOLDERID_ProgramFiles` 也被解析为 `Program Files (x86)`，而 `FOLDERID_ProgramFilesX64`"在任一情况下使用都会导致错误"。锚点：A6「FOLDERID_ProgramFiles / FOLDERID_ProgramFilesX86 / FOLDERID_ProgramFilesX64」及备注表 → [A6]
17. 用户级环境变量速查（Vista 及以后）：`%ALLUSERSPROFILE%`→`C:\ProgramData`、`%APPDATA%`→`…\AppData\Roaming`、`%LOCALAPPDATA%`→`…\AppData\Local`、`%PUBLIC%`→`C:\Users\Public`、`%SystemDrive%`→`C:`、`%windir%`→`C:\Windows`；但路径可能因"文件夹重定向"而变化，"可能与特定计算机上的路径不匹配"。锚点：A6 末段"环境字符串 / 示例路径"表及前导句 → [A6]

#### 子主题五：NTFS 高级特性（ADS、压缩、EFS、稀疏文件、可靠性）

18. **备用数据流（ADS）**：NTFS 中"流包含写入文件的数据，并提供有关文件的详细信息，而不是属性"（例如搜索关键字、创建者身份）；**每个流有自己的分配大小、实际大小、VDL，并"维护自己的压缩、加密和稀疏状态"**；流**没有自己的文件时间**（"更新文件中的任何流时，文件的文件时间将更新"）；只要任一流曾是稀疏的，文件上就会设置 `FILE_ATTRIBUTE_SPARSE_FILE`。锚点：A8「文件流（本地文件系统）」→ [A8]
19. 流的命令行全名格式是"`文件名:流名称:流类型`"（如 `myfile.dat:stream1:$DATA`）；默认数据流未命名，`文件名::$DATA` 等价于 `文件名`；流名称只能用文件名合法的字符（含空格），"**用户无法创建新的流类型**"，流类型"始终以美元符号（$）符号开头"；单字符文件名须写成全限定路径或加 `.\`，因为"Windows 将单个字符文件名视为驱动器号"。锚点：A8「流的命名约定」→ [A8]
20. **目录本身也是一种流**：`DirName`、`DirName::$INDEX_ALLOCATION`、`DirName:$I30:$INDEX_ALLOCATION` 三者等价；EFS 使用 `:$EFS:$LOGGED_UTILITY_STREAM`，TxF 使用 `:$TXF_DATA:$LOGGED_UTILITY_STREAM`。锚点：A8「流类型」表 → [A8]
21. **NTFS 压缩**：`compact` 是"NTFS 文件系统压缩功能的命令行版本"；目录的压缩状态表示"将文件添加到目录时是否自动压缩"，而"**设置目录的压缩状态不一定更改目录中已存在文件的压缩状态**"；`/EXE` 支持 `XPRESS4K`（最快且默认）、`XPRESS8K`、`XPRESS16K`、`LZX`（最紧凑）；**不能压缩 FAT 或 FAT32 分区**。锚点：A13「备注」与参数表 → [A13]
22. **EFS 与 NTFS 压缩互斥（官方明确单向）**：EFS"使用公钥系统为 NTFS 文件系统卷上的单个文件提供加密保护"，而"**无法加密以下项：压缩文件**、系统文件、系统目录、根目录、交易"；但"**可以加密稀疏文件**"——这是它与压缩文件的关键差别。锚点：A21「使用 EFS」→ [A21]
23. **`cipher` 的经典坑（官方原文）**："如果未加密父目录，则修改文件时，加密文件可能会解密。因此，**加密文件时，还应加密父目录**。"；输出用 `E` 标记已加密、`U` 标记未加密；`cipher /w:<directory>` 用于"从整个卷上可用未使用的磁盘空间中删除数据"。锚点：A16「备注」与「示例」→ [A16]
24. **稀疏文件**：程序"将这些未分配的区域视为包含值为零的字节，但没有使用磁盘空间来表示这些零"；应用必须**显式声明**文件为稀疏（`FSCTL_SET_SPARSE`），并"由应用程序负责"用 `FSCTL_SET_ZERO_DATA` 维持稀疏性；"**只有压缩文件或稀疏文件才能具有操作系统已知的清零范围**"，此时 NTFS"可能会取消分配文件中的磁盘空间……将字节范围设置为零，而不会扩展文件大小"；高度碎片化的大稀疏文件可能"超过 NTFS 对磁盘扩展区的限制"。锚点：A17 + A20「备注」+ A18「fsutil sparse」行 → [A17][A18][A20]
25. **可靠性**：NTFS 通过"基于事务的日志文件和检查点信息"提高可靠性，故障后"通过重播事务日志来恢复更改"；**自我修复 NTFS** 可"联机更正 NTFS 文件系统的损坏，而无需运行 `chkdsk.exe`"；卷与文件上限由**群集大小**决定（4 KB 默认→16 TB，64 KB→256 TB，2048 KB 最大→8 PB），装载群集过大的卷报 `STATUS_UNRECOGNIZED_VOLUME`；但"使用依赖于卷影复制服务（VSS）快照……的'以前版本'功能或备份应用程序时，最大支持的卷大小为 64 TB"。锚点：A14「提高可靠性 / 支持大型卷」+ A18「fsutil repair」行 → [A14][A18]

#### 子主题六：链接（硬链接 / 符号链接 / 交接点）

26. "NTFS 文件系统支持三种类型的文件链接：硬链接、交接点和符号链接。"**硬链接**是"文件的文件系统表示形式，其中多个路径引用同一卷中的单个文件"，它**不能引用目录，也不能引用不同卷上的文件**。锚点：A19「硬链接」→ [A19]
27. **交接点**"引用的存储对象是单独的目录"，"还可以链接位于同一计算机上的不同本地卷上的目录"，通过**重分析点**实现；硬链接有个反直觉细节："目录条目大小和文件_属性信息仅在进行更改的链接处明显_更新"——在一个链接上清除只读标志，其他链接仍显示只读。锚点：A19「交接点」与「硬链接」→ [A19]
28. `mklink` 四种形态：默认创建**文件符号链接**，`/d` 目录符号链接，`/h` 硬链接，`/j` 目录交接点；删除用普通命令（`rd` 删目录符号链接、`del` 删硬链接）。`fsutil hardlink` 进一步说明每个文件"可视为至少有一个硬链接"，"**只有在删除了指向某一文件的所有链接之后，才会从文件系统中删除该文件**"。锚点：A5 参数表与 Examples + A18「fsutil hardlink」行 → [A5][A18]

#### 子主题七：文件属性与列举命令（attrib / dir）

29. `attrib` 可设置的属性：`r` 只读、`a` 存档、`s` 系统、`h` 隐藏、`o` 脱机、`i` 非内容索引、`x` 清理、`p` 固定、`u` 未固定、`b` SMR Blob；**操作顺序坑（官方原文）**：文件若设了系统属性或隐藏属性，"必须清除该属性，然后才能更改文件的任何其他属性"；`/s` 递归子目录、`/d` 作用于目录、`/l` 作用于符号链接本身而非目标。锚点：A9 参数表 → [A9]
30. `dir` **默认不显示隐藏文件和系统文件**，加 `/a` 但不指定属性时才"显示所有文件的名称，包括隐藏文件和系统文件"；`dir /r` 可以"显示文件的备用数据流"（零基础读者最容易上手的 ADS 观察入口）；`dir /x` 显示 8.3 短名。**星号通配符的坑**：星号"始终使用短文件名映射"，所以 `dir t97\*` 会同时返回 `t97.txt` 和 `t.txt2`（后者短名为 `T97B4~1.TXT`），`del t97\*` 会删掉两个文件。锚点：A12 参数表与「Remarks」→ [A12]

#### 子主题八：卷、分区、盘符与装入点

31. **卷装入点**允许"链接卷，而无需驱动器号"，且必须建立在"现有 NTFS 目录"上；卷名用 `\\?\volume\{GUID}\` 语法（**需要花括号**）；用多个装入路径的好处是"可以使用单个驱动器号（如 `C:`）访问所有本地卷"，"无需记住哪个卷对应于哪个驱动器号"；`mountvol /p` 会"卸载基本卷，使基本卷脱机，使其不可装载"，且"**如果其他进程正在使用该卷，则 mountvol 会在卸载卷之前关闭所有打开的句柄**"；`/n`/`/e` 控制新基本卷的自动装载，`/s` 用于装载 EFI 系统分区。锚点：A11 首段、参数表与「备注」→ [A11]
32. **diskpart 必须提权**："您必须在本地**管理员**组或具有类似权限的组中才能运行 diskpart。"其核心心智模型是**焦点（focus）**："必须先列出一个对象，然后选择一个对象以使其处于焦点状态。对象具有焦点后，键入的任何 diskpart 命令都将对该对象执行操作"，且焦点会**自动转移**（"创建新分区时，焦点会自动切换到新分区"）。典型四步：`list disk` → `select disk 1` → `create partition primary` → `format fs=ntfs label=Backup quick`。锚点：A15 首段、「Determine focus」与「Examples」→ [A15]
33. NTFS 还提供其他扩容手段：可在"本地 NTFS 卷上的任何空文件夹中装载卷"，并可用磁盘配额"跟踪和控制各个用户的 NTFS 卷上的磁盘空间使用情况"；8.3 短名在 Server 2008 R2 及更高版本格式化卷时"默认禁用"，但"为了实现应用程序兼容性，系统卷上仍启用短名称"。锚点：A14「灵活分配容量 / 最大文件名称和路径」→ [A14]

#### 子主题九：权限（icacls）

34. `icacls` 的作用是"显示或修改指定文件中的任意访问控制列表（DACL）"，并取代已弃用的 `cacls`；**ACE 的规范顺序固定**：显式拒绝 → 显式授予 → 继承的拒绝 → 继承的授予；简单权限不用括号：`N` 无法访问、`F` 完全访问、`M` 修改、`RX` 读取和执行、`R` 只读、`W` 只写、`D` 删除。锚点：A4 首段、Note 与「Remarks」→ [A4]
35. 高级权限与继承标志**必须写在括号里**：`(DE)` 删除、`(WDAC)` 更改权限、`(WO)` 获取所有权、`(RD)` 读取数据/列出目录、`(X)` 执行/遍历；继承标志 `(I)` 继承、`(OI)` 对象继承（仅目录）、`(CI)` 容器继承（仅目录）、`(IO)` 仅继承（"继承自父容器，但不适用于对象本身"）、`(NP)` 不传播继承；`/grant:r` 是"权限替换以前授予的显式权限"，不带 `:r` 则是"添加到任何先前授予的显式权限中"。锚点：A4「Remarks」与参数表 → [A4]
36. 修坏权限的兜底与新式用法：`/reset` 会把 ACL"替换为所有匹配文件的默认继承 ACL"；禁用继承用 `/inheritancelevel:e|d|r`；SID 用数字形式时"将通配符 `*` 附加到 SID 的开头"（`/grant *S-1-1-0:(d,wdac)`）；批量备份/还原用 `icacls c:\windows\* /save aclfile /t` 与 `icacls c:\windows\ /restore aclfile`。锚点：A4 参数表与「Examples」→ [A4]

#### 子主题十：复制与备份（robocopy）

37. `robocopy <source> <destination> [<file>] [<options>]`，不指定文件时默认 `*.*`；`/s` 复制子目录但"自动排除空目录"，`/e`"自动包括空目录"；**`/mir` 相当于 `/e` 加 `/purge`**，即镜像目录树并**删除目标端源中已不存在的文件和目录**（破坏性最强）。锚点：A10「Syntax」与「Copy options」→ [A10]
38. **重试默认值极其激进**：`/r` 默认 **1,000,000** 次、`/w` 默认 **30** 秒，网络路径失效时会长时间假死，官方示例普遍写 `/R:2 /W:5`。锚点：A10「Retry options」与「Examples」→ [A10]
39. **退出代码语义反直觉**：`0` 表示"未复制任何文件"（无失败），`1` 表示"已成功复制所有文件"，"任何等于或大于 **8** 的值都表示在复制作期间至少发生一次故障"；`/copy` 默认值是 `DAT`（数据、属性、时间戳），`/sec` 相当于 `/copy:DATS`，`/copyall` 相当于 `/copy:DATSOU`；官方"强烈建议"每次运行都加 `/log:`。锚点：A10「退出（返回）代码」「Copy options」「Examples」→ [A10]
40. robocopy **默认会包含交接点**，需主动用 `/xj`（全部）、`/xjd`（目录）、`/xjf`（文件）排除；**从设备的根目录复制任何数据时，目标目录在复制过程中会采用"隐藏"和"系统"属性**（官方 Important）；`/sparse:<y|n>` 控制是否保留稀疏状态，不选时默认为 **yes**；`/mt:<n>` 多线程复制 `n` 必须为 1–128（默认 8），且"不能与 `/ipg` 和 `/efsraw` 参数一起使用"。锚点：A10「Syntax」Important 与参数表 → [A10]

---

### 3. 矛盾与冲突

1. **`FOLDERID_ProgramFilesX86` 的默认路径在同一页内前后不一致（A6 页面自身冲突）**：
   - 独立条目栏写：`Default Path | %ProgramFiles% (%SystemDrive%\Program Files)`（与 `FOLDERID_ProgramFiles` 完全相同）；
   - 但页面「备注」的位数对照表写：64 位操作系统 → `%SystemDrive%\Program Files (x86)`。
   - 两者不能同时为真。合理解释是独立条目栏给的是"未做重定向时"的原始值、备注表给的是"按 OS/应用位数解析后"的值，但**页面没有明说**。成章时应采用备注表的结论，并把这一分歧如实标注为待确认。
2. **32 位系统上两个 Program Files 常量指向同一路径**（A6）：32 位 OS 下 `FOLDERID_ProgramFiles` 与 `FOLDERID_ProgramFilesX86` 都是 `%SystemDrive%\Program Files`，而 `FOLDERID_ProgramFilesX64`"32 位操作系统不支持"。这意味着"Program Files (x86) 一定存在"是错误直觉，需要在正文里消歧。
3. **`AppData\LocalLow` 的来源深度不足**：A6 只给路径与"无 CSIDL 等效项"，A7 干脆没有 LocalLow 条目。两个来源都无法回答"它到底给谁用"（通常说法是低完整性级别进程，但本轮**没有官方来源支撑**）。不应把该说法写进第 2 节。
4. **来源覆盖粒度不均**：`fsutil` 主页面（A18）多个子命令行的描述列在抓取结果中为空，只能依赖 A20 等子页面补齐，存在信息缺口。

---

### 4. 可操作指引

> 执行环境标注：**cmd** = Windows 命令提示符（`cmd.exe`）；**PS** = PowerShell。管理员要求仅在该来源明确写出时才标注，其余标注为"来源未说明"。

- 查看并启用长路径支持（需**提升的特权**，PS；也可用 `.reg` 文件或组策略 `计算机配置 > 管理模板 > 系统 > 文件系统 > 启用 Win32 长路径`）：
  `New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force`；注意还需应用清单含 `<ws2:longPathAware>true</ws2:longPathAware>`，即"改注册表"对未适配的程序无效。→ [A3]
- 设置只读属性 / 批量清除只读（**cmd**）：`attrib +r report.txt`、`attrib -r b:\public\*.* /s`；显示单个文件属性用 `attrib news86`（递归作用于目录需额外加 `/d`）。→ [A9]
- 列出目录内容与隐藏项（**cmd**）：默认 `dir` 不显示隐藏/系统文件，需要时用 `dir /a`；查看备用数据流用 `dir /r`；查看 8.3 短名用 `dir /x`。→ [A12]
- 创建符号链接 / 硬链接 / 交接点（**cmd**，来源未说明是否需要管理员）：
  `mklink /d \MyFolder \Users\User1\Documents`（目录符号链接）
  `mklink /h \MyFile.file \User1\Documents\example.file`（硬链接）
  `mklink /j <link> <target>`（目录交接点）→ [A5]
- 压缩整个卷（**cmd**，需在卷根目录执行）：`compact /c /i /s:\`；只压缩指定扩展名而不改目录属性：`compact /c /s:\tmp *.bmp`；查询/设置系统级紧凑状态：`compact /CompactOs:query`、`compact /CompactOs:always`。→ [A13]
- 查看加密状态与加密目录（**cmd**）：`cipher`（E=已加密，U=未加密）、`cipher /e private`；加密时**务必同时加密父目录**；擦除卷上已删除文件的残留空间用 `cipher /w:<directory>`；备份与恢复 EFS 证书密钥用 `cipher /x[:efsfile] [<FileName>]`、`cipher /k`、`cipher /r:<filename> [/smartcard]`。→ [A16]
- 标记文件为稀疏并回收空间（**cmd**，`fsutil` **必须以管理员或管理员组成员身份登录**）：`fsutil sparse setflag c:\temp\sample.txt`；查询用 `queryflag`，扫描非零数据范围用 `queryrange`，用零填充指定区间用 `setrange <beginningoffset> <length>`。→ [A18][A20]
- 创建卷装入点（免盘符挂载，**cmd**，来源未说明管理员要求）：`mountvol \sysmount \\?\volume\{2eca078d-5cbc-43d3-aff8-7e8511f60d0e}\`；列出/删除用 `/l`、`/d`。→ [A11]
- 分区与格式化（**cmd**，**必须属于本地管理员组**）：进入 `diskpart` 后依次 `list disk` → `select disk 1` → `create partition primary` → `format fs=ntfs label=Backup quick`。→ [A15]
- 查看/修改权限（**cmd**）：`icacls test1 /grant User1:(d,wdac)`；用数字 SID 时写成 `/grant *S-1-1-0:(d,wdac)`；权限修坏后用 `icacls <path> /reset` 恢复为默认继承 ACL；批量备份/还原用 `icacls c:\windows\* /save aclfile /t` → `icacls c:\windows\ /restore aclfile`。→ [A4]
- 安全的目录复制/镜像（**cmd**，官方"强烈建议"加日志）：
  `robocopy C:\Users\Admin\Records D:\Backup /E /ZB /LOG:C:\Logs\Backup.log`
  `robocopy C:\Users\Admin\Records D:\Backup /MIR /R:2 /W:5 /LOG:C:\Logs\Backup.log`（**破坏性，先确认再执行**）
  `robocopy C:\Users\Admin\Records D:\Backup /S /E /COPY:DAT /MT:16 /LOG:C:\Logs\Backup.log` → [A10]
- robocopy 演练与限速：`/L` 仅列出不实际复制；`/iorate:1m` 限速 1 MB/s；`/ETA` 显示预计到达时间。→ [A10]

---

### 5. 需要降维改写的内容

以下内容带有开发者/系统管理员口吻，写进零基础笔记前需要改写：

1. **"本地文件系统"里的 API 表述**（A1/A2）："文件系统由一个或多个驱动程序和动态链接库组成"→ 改写成"Windows 靠一组后台程序 + 系统文件来读写硬盘，你不需要知道它们在哪"。`CreateFile`、`DefineDosDevice`、`I/O 系统`等一律删除，只保留结论。
2. **命名空间**（A2）：`\\?\`、`\\.\`、NT 命名空间、`GLOBALROOT`、对象管理器——零基础读者不需要这层。建议只保留"路径开头的两个字符决定了 Windows 用哪套规则理解它"这一个直觉，用"`\\?\` 是给程序用的'别自作聪明'开关"来类比；`PhysicalDrive`、`HarddiskVolume1` 等对象名移入附录或删除。
3. **路径长度限制的注册表细节**（A3）：`REG_DWORD`、`HKLM\SYSTEM\CurrentControlSet\Control\FileSystem`、"按进程缓存"、`longPathAware` 清单——降维为"改一个开关 + 重启"的操作步骤；"应用必须自己声明支持"这一条必须保留（否则读者会误以为改完就万事大吉），但用"老程序不一定认这个开关"来解释。
4. **句柄类术语**（A8/A11）："每个流维护机会锁""共享模式""`FILE_SHARE_DELETE`"、"关闭所有打开的句柄"——改写成"别人正在用这个卷时，强卸载会先断开他们的连接"。
5. **DACL / SID / ACE / 权限掩码**（A4）：零基础笔记建议只教"查看权限"和"重置权限"两条命令，把权限掩码与继承标志表降级为"查表用"的附录；`S-1-5-21-...` 形式的 SID 至少要说明"这是账户的内部编号，不是用户名"；`/setintegritylevel`、完整性级别（低/中/高）整体删除。
6. **CSIDL / KNOWNFOLDERID / GUID**（A6/A7）：`FOLDERID_*` 常量名、`{F1B32785-...}` GUID、"CSIDL 等效项"列——全部改写成"文件夹的中文名 + `%环境变量%` + 真实路径"三列表格，GUID 与 CSIDL 列直接删除（只保留给进阶附注）。**`PERUSER` vs `FIXED` 建议改写为"每个用户各有一份" vs "全机器共用一份"**，这是零基础读者真正需要的区别。
7. **文件流术语**（A8）：`FILE_ATTRIBUTE_SPARSE_FILE`、VDL、"属性类型代码"、`$INDEX_ALLOCATION`/`$I30`——只保留"NTFS 文件可以挂'隐藏的附加文件'，`dir /r` 能看到"，流类型表整体移入附录。
8. **卷/群集/扇区单位**（A14）：`群集大小`、`PB`、`STATUS_UNRECOGNIZED_VOLUME`、FRS/`UseLargeFRS`、`AllocationUnitSize`——零基础部分只需要"NTFS 卷能有多大取决于一个叫群集大小的设置"，把 8 PB / 64 TB(VSS) 的数字放进"冷知识"框或直接删。
9. **`FSCTL_*` 控制码与应用侧义务**（A17）：整页都是 Win32 开发者视角，零基础笔记只应保留 `fsutil sparse setflag` 这一条命令和"稀疏文件 = 用零填充但没真的占空间"这一句结论。
10. **重分析点 / 交接点 / 卷装入点的实现细节**（A11/A18/A19）："重分析点""筛选器驱动"这类表述需替换成"Windows 里一种'指针文件'"的类比，并明确"删链接 ≠ 删原文件"。
11. **robocopy 退出码表**（A10）：`0/1/2/3/5/6/7/8` 的完整表格对零基础读者无意义，改写成"0 和 1 都是正常，≥8 才是出错"一句话，并把 `/mir` 标红为危险参数。
12. **`compact /EXE` 算法名与 `cipher` 证书类参数**（A13/A16）：`XPRESS4K/8K/16K/LZX`、`/r:<filename> [/smartcard]`、`.pfx`/`.cer` 文件——零基础阶段只保留 `/CompactOs:query` 和"加密后要备份密钥"，其余移入进阶附录。

---

### 6. 未解决问题与缺口

1. **符号链接（`mklink /d`）是否需要管理员权限，本轮无来源支撑。** A5 页面完全没有提及权限要求。零基础读者最容易卡在这里（"拒绝访问"），必须补一条官方来源或明确标注为社区经验（C 级）。
2. **`AppData\LocalLow` 的官方用途说明缺失。** A6 只给路径、A7 无条目。常见的"低完整性级别进程（如 IE 保护模式）使用"说法本轮**无官方来源**，不能写进第 2 节。需补 Microsoft Learn 的完整性级别（Integrity Level）页面。
3. **`C:\Windows` 下各子目录（System32、SysWOW64、WinSxS、Temp、Installer）的作用，本轮只覆盖了 `System32`/`SysWOW64`/`Fonts`/`Resources` 的路径映射**，没有覆盖"为什么不能手删"的官方依据。需补 `WinSxS` 或 Windows 文件夹相关官方页。
4. **NTFS 压缩与 EFS 互斥的"另一方向"未验证。** A21 明确"无法加密压缩文件"，但没有明确"加密后能否再压缩"。第 2 节只写了单向结论，成章时不应写成双向"互斥"。
5. **`attrib` 页面关于"设了系统/隐藏属性后必须先清除才能改其他属性"的表述与实际行为是否一致，本轮无法核实**（只有一个来源）。零基础读者按此操作可能得不到预期结果，需实测或补第二个官方来源。
6. **`compact`、`cipher`、`mountvol`、`robocopy` 是否需要管理员权限，页面均未说明。** 第 4 节已按"来源未说明"处理，不臆测。
7. **A1（本地文件系统）页面内容极薄（约 1000 字）**，只有三个概念定义 + 一个主题索引表。此外**多个页面抓取后带有"访问此页面需要授权"的横幅**，疑为爬虫以未登录状态访问 Learn 所致；正文参数表完整，判断不影响结论，但建议上游知悉。
8. **`fsutil` 主页面部分子命令的描述列在抓取结果中为空**（A18 表中若干行），导致 `fsutil fsinfo`、`fsutil volume` 等信息不完整；如需使用需单独抓取子页面。
9. **未覆盖**：文件/目录时间戳三项（创建、访问、修改）的官方说明（A12 只提到 `/t:c|a|w` 三个字段名），以及 **ReFS 与 NTFS 的区别**（A14 仅链接了 ReFS 概述页，未精读）。

---

### 7. 下游交接摘要

- **骨架**：卷/目录/文件三层模型（A1）→ 命名与路径规则 + `\\?\`/`\\.\` 前缀与 MAX_PATH 260 限制（A2/A3）→ 系统目录地图（Windows / Program Files(x86) / Users / Public / ProgramData / AppData 三兄弟）（A6/A7）。
- **进阶层**：NTFS 四大特性——ADS（`dir /r` 观察）、压缩（`compact`）、加密 EFS（`cipher`，与压缩单向互斥、须加密父目录）、稀疏文件（`fsutil sparse`）；链接三兄弟（硬链接 / 符号链接 / 交接点，`mklink`）。
- **命令层**：`dir` + `attrib` 看属性 → `icacls` 看/改/重置权限 → `robocopy` 复制备份（重点讲 `/r` 默认百万次重试与退出码 ≥8 才是失败）→ `mountvol` / `diskpart` 管理卷与装入点。
- **坑清单（可直接成小节）**：`NUL.txt` 等保留设备名、`C:tmp.txt` ≠ `C:\tmp.txt`、`dir t97\*` 因短名映射误匹配、`attrib` 系统/隐藏属性的操作顺序、robocopy 默认重试与交接点默认被跟随、`cipher` 未加密父目录导致自动解密。
- **待补后再写**：`mklink` 提权要求、`LocalLow` 官方用途、`System32/WinSxS` 的"不要手删"依据——这三点在补来源前不要写成结论。

---

## 方向 B — Windows 注册表（精读素材）


### 1. 来源表

| ID | 标题 | URL | 层级 | 页面日期 | 抓取日期 | 支撑的子主题 |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | 注册表的结构 | https://learn.microsoft.com/zh-cn/windows/win32/sysinfo/structure-of-the-registry | A | 2025-03-12 | 2026-09-10 | 核心概念与术语 |
| S2 | 注册表 Hives | https://learn.microsoft.com/zh-cn/windows/win32/sysinfo/registry-hives | A | 2025-03-12 | 2026-09-10 | Hive 与磁盘文件 |
| S3 | 注册表文件 | https://learn.microsoft.com/zh-cn/windows/win32/sysinfo/registry-files | A | 2025-03-12 | 2026-09-10 | Hive 加载/卸载原理 |
| S4 | Predefined Keys | https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys | A | 2021-01-07 | 2026-09-10 | 预定义根键 |
| S5 | 注册表值类型 | https://learn.microsoft.com/zh-cn/windows/win32/sysinfo/registry-value-types | A | 2025-03-12 | 2026-09-10 | 值类型 REG_* |
| S6 | 面向高级用户的 Windows 注册表信息（KB256986） | https://learn.microsoft.com/zh-cn/troubleshoot/windows-server/performance/windows-registry-advanced-users | A | 2026-02-12 | 2026-09-10 | 大小限制 / 备份 / 还原 / HKCR 合并视图 |
| S7 | 注册表项安全和访问权限 | https://learn.microsoft.com/zh-cn/windows/win32/sysinfo/registry-key-security-and-access-rights | A | 2025-03-12 | 2026-09-10 | 权限、ACL、KEY_* 掩码 |
| S8 | reg commands（总览 + Caution） | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/reg | A | 2025-08-16 | 2026-09-10 | reg.exe 总览与官方警告 |
| S9 | reg query | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/reg-query | A | 2025-08-16 | 2026-09-10 | 查询命令 |
| S10 | reg add | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/reg-add | A | 2025-08-16 | 2026-09-10 | 新增命令 |
| S11 | reg delete | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/reg-delete | A | 2025-08-16 | 2026-09-10 | 删除命令 |
| S12 | reg copy | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/reg-copy | A | 2025-08-16 | 2026-09-10 | 复制命令 |
| S13 | reg export | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/reg-export | A | 2025-08-16 | 2026-09-10 | 备份（导出 .reg） |
| S14 | reg import | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/reg-import | A | 2025-08-16 | 2026-09-10 | 还原（导入 .reg） |
| S15 | reg save | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/reg-save | A | 2025-08-16 | 2026-09-10 | 备份（保存 .hiv） |
| S16 | reg restore | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/reg-restore | A | 2025-08-16 | 2026-09-10 | 还原（写回 .hiv） |
| S17 | reg load | https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/reg-load | A | 2025-08-16 | 2026-09-10 | 临时挂载 hive 排查 |
| S18 | 如何在 Windows 中备份和还原注册表 | https://support.microsoft.com/zh-cn/windows/如何备份和还原注册表-855140ad-e318-2a13-2829-d428a2ab0692 | A | 未标注 | 2026-09-10 | regedit 界面级备份/还原步骤 |
| S19 | 运行和 RunOnce 注册表键 | https://learn.microsoft.com/zh-cn/windows/win32/setupapi/run-and-runonce-registry-keys | A | 2026-02-21 | 2026-09-10 | 开机自启相关实用路径 |
| S20 | Accessing an Alternate Registry View | https://learn.microsoft.com/en-us/windows/win32/winprog64/accessing-an-alternate-registry-view | A | 2021-02-08 | 2026-09-10 | 32/64 位视图与 WOW6432Node |
| S21 | about_Registry_Provider | https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_registry_provider | A | 2025-02-05 | 2026-09-10 | PowerShell 访问注册表 |
| S22 | Get-ItemProperty | https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-itemproperty | A | 未标注 | 2026-09-10 | PowerShell 读取值 |
| S23 | Verbs and File Associations | https://learn.microsoft.com/en-us/windows/win32/shell/fa-verbs | A | 2021-01-07 | 2026-09-10 | 文件关联与右键菜单 |
| S24 | Programmatic Identifiers（ProgID） | https://learn.microsoft.com/en-us/windows/win32/shell/fa-progids | A | 未标注 | 2026-09-10 | 文件关联 ProgID |
| S25 | Creating Shortcut Menu Handlers | https://learn.microsoft.com/en-us/windows/win32/shell/context-menu-handlers | A | 未标注 | 2026-09-10 | 自定义 shell verb 与权限 |
| S26 | Enable-ComputerRestore | https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/enable-computerrestore | A | 未标注 | 2026-09-10 | 系统还原点回滚 |
| S27 | User Environment Variables | https://learn.microsoft.com/en-us/windows/win32/shell/user-environment-variables | A | 2021-01-07 | 2026-09-10 | 环境变量概念（注册表路径缺失，见第 6 节） |

来源层级分布：A 级 27 条，B 级 0 条，C 级 0 条。本轮未使用任何非官方来源。

**替换说明**：P1 指定的 B-1、B-2（training 模块 `explore-windows-architecture/4-examine-windows-registry` 与 `5-use-windows-registry-editor`）在 zh-cn 与 en-us 两个版本下均只能抓取到 Training 课程目录页（74–182 字，标题为"浏览所有课程、学习路径和模块"），判定为不可用；已用同主题官方 Win32 页 S1/S2/S4 替代其"注册表概述"职能，用 S18 替代其"注册表编辑器操作"职能。P1 指定的 `checkpoint-computerrestore` 在多个 view 参数下均返回 404，改用 S26（Enable-ComputerRestore）承担系统还原职能。

### 2. 论断 / 来源映射

（共 38 条。命令语法、示例与操作步骤集中在第 4 节，本节只保留"论断"。）

#### 2.1 注册表是什么：结构与术语

- 注册表是一个分层数据库，数据以树格式组织；树中每个节点称为**键**，每个键可同时包含**子项**和称为**值**的数据条目；键可以有任意数量的值；键名不区分大小写、不能包含反斜杠 `\`，但值名称和数据**可以**包含反斜杠；键名不做本地化，值可以被本地化 → [S1]（小节"注册表的结构"）
- 注册表树最深可达 512 层；通过单次注册表 API 调用一次最多创建 32 层 → [S1]
- 应用程序必须先打开一个键才能向注册表添加数据；系统定义了一批**始终打开**的预定义键作为入口，添加数据的应用应始终在预定义键框架内工作，以便管理工具能找到并使用新数据；预定义项（根键）名称最大长度为 255 个字符 → [S4][S6]

#### 2.2 预定义根键（零基础最常打交道的 5 个）

- `HKEY_LOCAL_MACHINE`（HKLM）保存计算机**物理状态**的数据：总线类型、系统内存、已安装软硬件，以及 Plug and Play 信息（`Enum` 分支记录了系统上出现过的全部硬件）；`HKEY_CURRENT_USER`（HKCU）保存**当前用户**偏好：环境变量设置、程序组、颜色、打印机、网络连接和应用偏好 → [S4]
- HKCU 映射到 `HKEY_USERS` 中当前用户的分支；该映射是**按进程**建立的，基于第一个引用它的线程的安全上下文；若该安全上下文在 HKU 下没有已加载的 hive，则映射到 `HKEY_USERS\.Default` → [S4]
- `HKEY_CLASSES_ROOT`（HKCR）**不是真实存储位置**，而是 `HKLM\Software\Classes`（本机所有用户的默认设置）与 `HKCU\Software\Classes`（仅交互式用户的覆盖设置）的合并视图；写 HKCR 会被系统重定向到二者之一，因此"要更改交互式用户的设置，必须在 `HKEY_CURRENT_USER\Software\Classes` 下而不是在 HKEY_CLASSES_ROOT 下进行更改；要更改默认设置，必须在 `HKEY_LOCAL_MACHINE\Software\Classes` 下进行更改" → [S6]
- `HKEY_CURRENT_CONFIG` 只是 `HKLM\System\CurrentControlSet\Hardware Profiles\Current` 的**别名**，描述当前硬件配置与标准配置之间的差异；`HKEY_PERFORMANCE_DATA` 的数据**并不真的存在注册表里**，而是注册表函数触发系统从数据源实时收集 → [S4]

#### 2.3 Hive（配置单元）与磁盘文件

- **配置单元（hive）**是注册表中键、子项和值的逻辑组，带有"一组在操作系统启动时或用户登录时加载到内存中的支持文件" → [S2]
- 每次新用户登录都会为该用户创建一个新的配置单元（**用户配置文件配置单元**），位于 `HKEY_USERS` 键下，内容包括该用户的应用程序设置、桌面、环境、网络连接和打印机 → [S2]
- Hives 的**大部分**支持文件位于 `%SystemRoot%\System32\Config` 目录中（每次用户登录时更新）；标准 hive 与支持文件的对应关系如下 → [S2]：

  | 注册表配置单元 | 支持文件 |
  | --- | --- |
  | HKEY_CURRENT_CONFIG | System、System.alt、System.log、System.sav |
  | HKEY_CURRENT_USER | Ntuser.dat、Ntuser.dat.log |
  | HKEY_LOCAL_MACHINE\SAM | Sam、Sam.log、Sam.sav |
  | HKEY_LOCAL_MACHINE\Security | Security、Security.log、Security.sav |
  | HKEY_LOCAL_MACHINE\Software | Software、Software.log、Software.sav |
  | HKEY_LOCAL_MACHINE\System | System、System.alt、System.log、System.sav |
  | HKEY_USERS\.DEFAULT | Default、Default.log、Default.sav |

- 文件扩展名的含义：无扩展名 = 配置单元数据的**完整副本**；`.alt` = 仅 `HKLM\System` 才有的备份副本（"只有系统密钥具有 .alt 文件"）；`.log` = 键和值项更改的**事务日志**；`.sav` = 配置单元的备份副本 → [S2]
- 注册表文件只有标准格式与最新格式两种；Windows 2000 只支持标准格式，从 Windows XP 起支持最新格式；但在支持最新格式的 Windows 上，`HKEY_CURRENT_USER`、`HKLM\SAM`、`HKLM\Security`、`HKEY_USERS\.DEFAULT` **仍使用标准格式**，其余 hive 使用最新格式 → [S2]
- 应用程序可以把注册表的一部分保存在文件里再加载回来（适用于数据量大、条目过多或数据是临时的场景）；`RegLoadKey` 把文件数据加载到 `HKEY_USERS` 或 `HKEY_LOCAL_MACHINE` 下的指定子项，之后可用 `RegUnLoadKey` 还原到以前的状态 → [S3]

#### 2.4 值类型：REG_* 到底是什么

- 注册表值可以存储多种格式的数据，这些类型定义在 `winnt.h` 头文件中：`REG_SZ`（以 null 结尾的字符串）、`REG_BINARY`（任何形式的二进制数据）、`REG_DWORD`（32 位数字）、`REG_QWORD`（64 位数字）、`REG_NONE`（没有定义的值类型）等；其中 `REG_DWORD_LITTLE_ENDIAN` 在 Windows 头文件中**就定义为 `REG_DWORD`**（Windows 设计为运行在小端架构上），`REG_DWORD_BIG_ENDIAN` 供某些 UNIX 大端系统使用 → [S5]
- `REG_EXPAND_SZ` 是"包含对环境变量的**未扩展引用**"的字符串，例如 `%PATH%`；要展开须调用 `ExpandEnvironmentStrings` → [S5]
- `REG_MULTI_SZ` 是以长度为 0 的字符串结尾的字符串序列（示例 `String1\0String2\0String3\0LastString\0\0`），需要**两个**终止 null 字符，且**不能包含零长度字符串**（空序列定义为 `\0`） → [S5]
- 字符串的终止符是读写注册表最常见的陷阱：写入时必须把终止 null 计入长度（应使用 `strlen(string) + 1`，而非 `strlen`）；读取时字符串**可能未正确终止**，必须自行确保终止，否则可能覆盖缓冲区 → [S5]
- 在注册表编辑器里，DWORD 值可以按二进制、十六进制或十进制格式显示；`REG_QWORD` 在注册表编辑器中以**二进制值形式**显示（Windows 2000 引入） → [S6]

#### 2.5 尺寸限制：为什么会遇到"值写不进去"

- 值名称最大长度 16,383 个字符（Windows Server 2003 / XP / Vista）；**超过 2,048 字节的长值必须存储为文件**，只在注册表中存文件名——"这有助于注册表高效执行"；此外**一个项的所有值的总大小有 64K 限制** → [S6]

#### 2.6 32 位 / 64 位注册表视图（WOW6432Node）

- 默认情况下，WOW64 上的 32 位应用程序访问 32 位注册表视图，64 位应用程序访问 64 位注册表视图；`KEY_WOW64_64KEY`（0x0100）让任一应用访问 64 位键，`KEY_WOW64_32KEY`（0x0200）让任一应用访问 32 位键；这两个标志**对共享注册表键无效**，且**同时指定会失败**并返回 `ERROR_INVALID_PARAMETER` → [S20]
- `Wow6432Node` 与 `WowAA32Node` 键是**保留的**，"为了兼容性，应用程序不应直接使用这些键"；官方最佳实践是：应用一旦用某个标志访问了备用视图，之后对**子键**的所有创建/删除/打开操作都必须显式使用**同一个标志**，而要准确枚举两个视图中的所有键必须**分两遍**枚举（一遍用其中一个标志打开的句柄，另一遍用另一个标志） → [S20]
- 读者实际会遇到的只是两个开关：`reg query` / `reg add` / `reg import` 等命令提供 `/reg:32` 与 `/reg:64` 指定注册表视图；而 64 位 Windows 自带的 64 位注册表编辑器会在 `HKEY_LOCAL_MACHINE\Software\WOW6432Node` 节点下显示 32 位项 → [S9][S10][S14][S6]

#### 2.7 权限与所有者

- Windows 安全模型允许控制对注册表项的访问；调用 `RegCreateKeyEx` 或 `RegSetKeySecurity` 时可为键指定**安全描述符**，若指定 `NULL` 则键获得默认安全描述符，而**键的默认安全描述符中的 ACL 继承自其直接父键** → [S7]
- 注册表项的有效访问权限包括 `DELETE`、`READ_CONTROL`、`WRITE_DAC`、`WRITE_OWNER` 这些标准访问权限，但**不支持 `SYNCHRONIZE`**；键特定权限中 `KEY_QUERY_VALUE` 查询值必需、`KEY_SET_VALUE` 创建/删除/设置值必需、`KEY_CREATE_SUB_KEY` 创建子项必需、`KEY_ENUMERATE_SUB_KEYS` 枚举子项必需、`KEY_NOTIFY` 请求更改通知必需，`KEY_CREATE_LINK`（0x0020）**保留供系统使用** → [S7]
- 打开键时系统会按安全描述符检查请求的访问权限，权限不足则打开失败；**如果管理员需要访问某个键，官方给出的解决方案是启用 `SE_TAKE_OWNERSHIP_NAME` 特权，并以 `WRITE_OWNER` 访问权限打开该键** → [S7]
- 核对权限的两个入口：注册表编辑器中定位到键 → "编辑"菜单 → "权限"；PowerShell 中 `Get-Acl` 读取、`Set-Acl` 写入（官方示例用 `RegistryAccessRule` 为指定用户加 `FullControl`） → [S7][S21]

#### 2.8 备份与回滚（强制内容）

- 官方在 `reg` 命令页用 Caution 级警告确立基调：「除非没有替代项，否则不要直接编辑注册表。注册表编辑器绕过标准安全措施，允许降低性能、损坏系统甚至要求重新安装 Windows 的设置。……如果必须直接编辑注册表，请先备份它。」 → [S8]
- 官方推荐的修改顺序是「使用 Windows 用户界面更改系统设置，而不是手动编辑注册表」，并补充"编辑注册表有时可能是解决产品问题的最佳方法"，若 Microsoft 知识库提供了针对该问题的分步说明文章，则「建议完全按照这些说明操作」；同页警告错误修改"可能需要重新安装操作系统才能解决。Microsoft 不能保证可以解决这些问题" → [S6]
- 官方把"备份"写进了命令本身：`reg save` 的备注是「在编辑任何注册表项之前，必须使用 **reg save** 命令保存父子项。如果编辑失败，则可以使用 **reg restore** 作还原原始子项」，`reg restore` 的定义即"将保存的子项和条目写回注册表" → [S15][S16]
- 三条 .reg / .hiv 路径的边界不同：`reg export` 导出时必须用 **.reg** 扩展名且**仅适用于本地计算机**；`reg import` 的文件**必须由 reg export 提前创建**，同样仅本地；`reg restore` 的文件必须由 `reg save` 创建、**必须是 .hiv 扩展名**，且会**覆盖**目标键的现有内容 → [S13][S14][S16]
- regedit 界面路径是官方给出步骤最完整的备份方式：「开始」→ 搜索 `regedit.exe` → 回车（**若有管理员密码或确认提示，需提供**）→ 定位并单击要备份的项或子项 → 「文件」>「导出」→ 选位置、填文件名 → 「保存」；还原为「文件」>「导入」→ 选备份文件 → 「打开」 → [S18]
- 备份**整个**注册表要用备份工具备份**系统状态**（"系统状态包括注册表、COM+ 类注册数据库和启动文件"），还原整机走"从备份还原系统状态"；备份系统状态还会在 `%SystemRoot%\Repair` 文件夹中创建注册表文件的更新副本 → [S6]
- 系统还原是另一条回滚路径：`Enable-ComputerRestore -Drive "C:\"` 在指定文件系统驱动器上启用系统还原功能，之后可用 `Restore-Computer` 之类的工具还原到以前的状态；官方明确要求在 Windows Vista 及更高版本上**必须用"以管理员身份运行"打开 Windows PowerShell** 才能运行该 cmdlet，且**要在任何驱动器上启用都必须先在系统驱动器上同时启用**，不能用于外部驱动器或远程网络驱动器；可用 `Rstrui.exe` 查看每个驱动器的还原状态 → [S26]
- `reg load` / `reg unload` 覆盖"临时挂载做排查"这一场景：`reg load` 把保存的子项和条目写入注册表中的**其他**子项，"此命令适用于用于故障排除或编辑注册表项的临时文件"，而 `reg unload` 的定义就是"删除使用 reg load 作加载的注册表部分" → [S17][S8]

#### 2.9 常用实用路径

- 开机自启共有**四个** `Run` / `RunOnce` 键（HKLM 与 HKCU 各两个，均在 `Software\Microsoft\Windows\CurrentVersion\` 下）；`Run` 键使程序在**每次**用户登录时运行，`RunOnce` 键使程序运行**一次，然后删除该键**；键的数据值是**不超过 260 个字符**的命令行，形式为 `说明-字符串 = 命令行`，且"如果在任何特定密钥下注册了多个程序，则这些程序运行的顺序**不确定**" → [S19]
- `HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce` **仅在重新启动后管理员组的成员登录时才执行**；`RunOnce` 默认在命令行运行**之前**删除值，值名前加感叹号 `!` 可把删除**延迟到命令运行之后**（"如果没有感叹号前缀，当 RunOnce 操作失败时，下次启动计算机时不会要求关联程序运行"）；"默认情况下，当计算机以安全模式启动时，将忽略这些键"，值名前加星号 `*` 可**强制程序在安全模式下仍然运行** → [S19]
- 文件关联侧的三个可追溯结论：右键菜单每条命令由一个 **verb（谓词）**标识，verb 对应的命令字符串形如 `"My Program.exe" "%1"`，**任何可能包含空格的元素都必须加引号**；ProgID 的标准键名格式为 `[厂商或应用].[组件].[版本]`（如 `Word.Document.6`），位于 `HKEY_CLASSES_ROOT` 下；因为 HKCR 是 HKCU 与 HKLM 的组合，**可以把自定义 verb 注册在 `HKEY_CURRENT_USER\Software\Classes` 下，其主要好处是"不需要提升权限"** → [S23][S24][S25]

#### 2.10 三种执行方式：regedit / reg.exe / PowerShell

- 官方列举的可修改注册表手段包括注册表编辑器（Regedit.exe 或 Regedt32.exe）、组策略、系统策略、注册表（.reg）文件、Windows Script Host 脚本、WMI（含 Wmic.exe）以及控制台注册表工具 Reg.exe；其中 `reg` 的 keyname 必须包含有效根键，本地有效根键为 `HKLM`、`HKCU`、`HKCR`、`HKU`、`HKCC`，而指定远程计算机时**只有 `HKLM` 和 `HKU` 有效** → [S6][S9]
- PowerShell 侧注册表提供程序的驱动器为 `HKLM:`（映射 HKEY_LOCAL_MACHINE 配置单元）与 `HKCU:`（映射 HKEY_CURRENT_USER 配置单元），也可用提供程序全名语法 `Registry::HKEY_LOCAL_MACHINE\Software`；四个 cmdlet 分工明确：`Get-ChildItem` 看**子项**（不显示父键属性）、`Get-Item` 看**键本身及其属性**、`Get-ItemProperty` 看**值**、`Get-ItemPropertyValue`（PowerShell 5.0 起）只返回指定属性的值 → [S21][S22]
- 修改与删除的官方行为差异：`Set-ItemProperty` 的动态参数 `-Type` 决定数据类型，**默认为 `String`（REG_SZ）**，可选 `ExpandString`、`Binary`、`DWord`、`MultiString`、`QWord`、`Unknown`（表示不受支持的类型如 `REG_RESOURCE_LIST`）；`Remove-Item` 在项**包含子项时默认弹出确认**，加 `-Recurse` 才免提示；`Remove-ItemProperty` 只删值，`Clear-Item` 清空键的**所有值**而保留键本身 → [S21]

### 3. 矛盾与冲突

1. **HKCU 支持文件的磁盘位置，两份官方文档不一致。**
   - S2（Win32「注册表 Hives」，2025-03-12）：「Hives 的大部分支持文件都位于 `%SystemRoot%\System32\Config` 目录中」，并在对应表中列出 `HKEY_CURRENT_USER` 的支持文件为 `Ntuser.dat`、`Ntuser.dat.log`，**未指明目录**。
   - S6（KB256986，2026-02-12）：「除 HKEY_CURRENT_USER 以外的所有配置单元的支持文件都位于 …… `%SystemRoot%\System32\Config` 文件夹中。HKEY_CURRENT_USER 的支持文件位于 `%SystemRoot%\Profiles\Username` 文件夹中。」
   - 前者说"大部分在 Config"（暗示存在例外但未列举），后者把边界划得更死并给出 `%SystemRoot%\Profiles\Username`。`%SystemRoot%\Profiles\Username` 是 Windows 2000/XP 时代的布局描述；两页均未提及现代 Windows 的 `C:\Users\<用户名>\NTUSER.DAT`。**未静默合并**：写作时应只说"NTUSER.DAT/NTUSER.DAT.LOG 属于用户配置文件 hive"，磁盘位置以"用户配置文件目录"表述，不写死路径。

2. **系统还原的可用范围表述与当前适用版本不一致。**
   - S26（Enable-ComputerRestore，标注适用于 Windows 7/Vista/XP，视图为 `?view=powershell-5.1`）正文写：「系统还原点和 ComputerRestore cmdlet **仅在 Windows 7、Windows Vista 和 Windows XP 等客户端操作系统上受支持**」，但同一页的"适用于"以及官方 cmdlet 集在 Windows 10/11 的 PowerShell 5.1 中仍然存在。文档的版本声明明显滞后。
   - 同时 S18（备份还原注册表，适用于 **Windows 11 / Windows 10 / Windows 8.1**）**完全没有提到系统还原**，只给 regedit 导出/导入两条路径；S6 指向的整机回滚路径是"从备份还原系统状态"，同样不是系统还原。
   - 结论：**不应把系统还原点写成注册表回滚的第一推荐手段**。写作时应把"导出 .reg / 导入 .reg"作为主路径（S18 明确覆盖 Win11），系统还原作为附注并注明官方版本声明存疑。

3. **"备份整个注册表"的手段在两份官方文档中指向不同工具。**
   - S6 指向"备份工具备份系统状态"（含注册表、COM+ 类注册数据库、启动文件），并在还原章节同样使用"从备份还原系统状态"。
   - S18 面向 Win11/Win10 用户，只教 regedit 的「文件 > 导出 / 导入」。
   - 两者不冲突但覆盖面不同：S18 的 regedit 导出是**按项**导出，S6 的系统状态是**整机**快照。零基础读者容易把"导出 HKLM\Software 下的一个键"误解为"备份了整个注册表"，写作时必须显式区分。

4. **"不要直接编辑注册表"的强度，两页语气不同。**
   - S8（reg 命令）用 Caution 级警告，说注册表编辑器"绕过标准安全措施"，"允许降低性能、损坏系统甚至要求重新安装 Windows 的设置"。
   - S6（KB256986）用 Warning 级警告，补充"Microsoft 不能保证可以解决这些问题。您应自行承担修改注册表的风险"，但同时承认"编辑注册表有时可能是解决产品问题的最佳方法"。

5. `reg copy` 页面内文末残留 "**reg 比较** 作的返回值为" 字样（`reg compare` 的文案未清理），与命令本体（`reg copy`）不对应。属官方页面笔误，不影响结论，但引用返回值语义时以页面正文的 0=Success / 1=Failure 为准。

### 4. 可操作指引

**管理员权限一栏只写官方页明确写出的内容**；官方未明示的一律标注为"官方未说明"（详见第 6 节第 8 条）。

#### 4.1 主路径：导出备份 → 导入还原（覆盖 Windows 11/10/8.1）

- **方式一 · regedit 界面**（官方来源 S18）
  1. 「开始」→ 搜索 `regedit.exe` → 回车。**若有管理员密码或确认提示，需提供**（官方原文即含此提示） → [S18]
  2. 在注册表编辑器中找到并单击要备份的项或子项
  3. 「文件」>「导出」
  4. 在"导出注册表文件"对话框中选择保存位置，并输入备份文件名
  5. 「保存」
  - 还原：打开 `regedit.exe`（同上，有管理员确认提示）→「文件」>「导入」→ 选择备份文件 →「打开」 → [S18]
  - **权限：官方明确写出会有管理员密码/确认提示**，即导出与导入都按提权处理。

- **方式二 · 命令行 reg.exe**（官方来源 S13/S14）
  ```bat
  :: 备份：把某个键（含所有子项和值）导出为 .reg
  reg export "HKLM\SOFTWARE\MyApp" AppBkUp.reg /y

  :: 还原：把 .reg 导入回注册表
  reg import AppBkUp.reg
  ```
  - `<filename>` 必须带 `.reg` 扩展名；`/y` 覆盖同名文件不提示；导出**仅适用于本地计算机**；键名含空格必须加引号 → [S13]
  - `reg import` 的文件必须由 `reg export` 提前创建 → [S14]
  - 返回值 0 = 成功 / 1 = 失败，可用于脚本判断 → [S13][S14]
  - **权限：S13/S14 页面未明示。** 见第 6 节第 8 条。

#### 4.2 进阶路径：整键快照 → 写回（.hiv）

```bat
:: 编辑前先做整键快照（官方指定的"编辑前必做"动作）
reg save "HKLM\Software\MyApp" AppBkUp.hiv /y

:: 编辑失败时写回原始子项（会覆盖该键现有内容）
reg restore "HKLM\Software\MyApp" AppBkUp.hiv

:: 仅做临时加载排查，用完必须卸载
reg load   HKLM\TempHive TempHive.hiv
reg unload HKLM\TempHive
```
- 官方备注（可直接引用为"编辑前先备份"的依据）：「在编辑任何注册表项之前，必须使用 **reg save** 命令保存父子项。如果编辑失败，则可以使用 **reg restore** 作还原原始子项。」 → [S15][S16]
- `reg restore` 的文件必须由 `reg save` 创建且**必须是 .hiv 扩展名**，会**覆盖**目标键的现有内容；仅适用于本地计算机 → [S16]
- `reg unload` 的定义就是"删除使用 reg load 操作加载的注册表部分"，因此 load 之后必须 unload → [S8][S17]
- **权限：S15/S16/S17 页面未明示。** 见第 6 节第 8 条。

#### 4.3 整机回滚路径

- **系统状态备份**：用备份工具备份系统状态（含注册表、COM+ 类注册数据库、启动文件）；还原时从备份还原系统状态；备份系统状态还会在 `%SystemRoot%\Repair` 生成注册表文件的更新副本 → [S6]
- **系统还原点**（附注路径，需说明版本存疑）
  ```powershell
  # 在 C: 上启用系统还原功能
  Enable-ComputerRestore -Drive "C:\"
  ```
  - **权限：官方明确要求**「使用'以管理员身份运行'选项打开 Windows PowerShell」 → [S26]
  - 官方提示：要在任何驱动器上启用，必须**先在系统驱动器上同时启用**；不能用它给外部驱动器或远程网络驱动器启用；可用 `Rstrui.exe` 查看每个驱动器的还原状态 → [S26]

#### 4.4 编辑前的官方风险 checklist（可直接做成 Callout）

- 「除非没有替代项，否则不要直接编辑注册表。注册表编辑器绕过标准安全措施，允许降低性能、损坏系统甚至要求重新安装 Windows 的设置。可以使用控制面板中的程序或 Microsoft 管理控制台（MMC）安全地更改大多数注册表设置。**如果必须直接编辑注册表，请先备份它。**」 → [S8]
- 「如果使用注册表编辑器或使用其他方法错误地修改了注册表，则可能会发生严重问题。这些问题可能需要重新安装操作系统才能解决。Microsoft 不能保证可以解决这些问题。」 → [S6]
- 「建议使用 Windows 用户界面更改系统设置，而不是手动编辑注册表。」若 KB 已给出针对该问题的分步说明，「建议完全按照这些说明操作」 → [S6]
- 遇到权限不足的键：启用 `SE_TAKE_OWNERSHIP_NAME` 特权并以 `WRITE_OWNER` 打开（官方给出的"管理员需要访问密钥"的唯一解决方案） → [S7]
- 查看/核对某个键的现有权限：注册表编辑器 → 定位到键 → 「编辑」>「权限」 → [S7]

#### 4.5 查询与验证（改完先看，别急着改）

```bat
:: 查某个值（限定类型、区分大小写、完全匹配）
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion" /v ProgramFilesDir
reg query "HKLM\SOFTWARE\Microsoft" /s /f asp.net /k
reg query "HKLM\SOFTWARE" /ve
```
- `reg query <keyname> [{/v <valuename> | /ve}] [/s] [/se <separator>] [/f <data>] [{/k | /d}] [/c] [/e] [/t <Type>] [/z]`（完整语法来源 S9）
- `/s` 递归查询所有子项和值；`/f` 指定搜索数据或模式；`/k` **必须与 /f 同时使用**、仅搜键名；`/d` 仅搜数据；`/c` 区分大小写；`/e` 仅返回完全匹配；`/t` 限定 `REG_SZ`/`REG_MULTI_SZ`/`REG_EXPAND_SZ`/`REG_DWORD`/`REG_BINARY`/`REG_NONE`；`/z` 附带类型的等效数字 → [S9]

```powershell
# 只读地看一眼值（不会改动任何东西）
Get-ItemProperty -Path HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion -Name "ProgramFilesDir"
Get-ItemPropertyValue -Path HKLM:\SOFTWARE\Microsoft\Wbem -Name BUILD
Get-ChildItem -Path HKLM:\HARDWARE -Exclude D*
```
- 第一条来源 S22（官方示例 3，页面说明它依赖映射到 HKLM 的 `HKLM:` 驱动器，也可改用 `Registry::HKEY_LOCAL_MACHINE\...` 路径）；后两条来源 S21 → [S22][S21]

#### 4.6 修改与删除命令（附风险提示）

```bat
:: 新增值（/ve 表示添加 null 值；/f 免确认）
reg add "HKLM\Software\MyCo" /v Data /t REG_BINARY /d fe340ead /f
reg add "HKLM\Software\MyCo" /v MRU /t REG_MULTI_SZ /d fax\0mail\0
reg add "HKLM\Software\MyCo" /v Path /t REG_EXPAND_SZ /d ^%systemroot^%

:: 删除（危险，务必先 reg export 备份）
reg delete "HKLM\Software\MyCo\MyApp\Timeout" /f
reg delete "HKLM\Software\MyCo" /v MTU /f

:: 复制（/s 连同所有子项和条目）
reg copy "HKLM\Software\MyCo\MyApp" "HKLM\Software\MyCo\SaveMyApp" /s
```
- `reg add` **无法通过此操作添加子树**；`REG_EXPAND_SZ` 类型的数据里百分号 `%` 必须用插入符号 `^` 转义（`^%systemroot^%`）；`/t` 可选 `REG_SZ`、`REG_MULTI_SZ`、`REG_DWORD`、`REG_DWORD_BIG_ENDIAN`、`REG_DWORD_LITTLE_ENDIAN`、`REG_BINARY`、`REG_LINK`、`REG_FULL_RESOURCE_DESCRIPTOR`、`REG_EXPAND_SZ` → [S10]
- `reg delete` 的 `/va` **删除指定键中的所有条目但不删除其中的子项**；`/v` 删特定条目；`/ve` 仅删没有值的条目；`/f` 免确认 → [S11]
- `reg copy` "复制子项时，此命令不要求确认"；`/s` 复制该项下所有子项和条目 → [S12]
- PowerShell 等价写法与差异：`Set-ItemProperty`（`-Type` 默认 `String`）、`New-ItemProperty`、`Copy-Item` / `Copy-ItemProperty`、`Move-Item` / `Move-ItemProperty`、`Rename-Item` / `Rename-ItemProperty`、`Remove-Item`（含子项时默认确认，`-Recurse` 免提示）、`Remove-ItemProperty`、`Clear-Item` / `Clear-ItemProperty` → [S21]
- **官方提醒用管理接口替代直接改注册表**：官方示例把服务启动类型从 Automatic 改成 Manual，既可用 `Set-ItemProperty -Path $path -Name Start -Value 3`，也可用 `Set-Service -Name Spooler -StartupType Automatic` 改回 → [S21]

#### 4.7 常被问到的实用路径速查

| 用途 | 路径 | 来源 |
| --- | --- | --- |
| 开机自启（所有用户，每次登录） | `HKLM\Software\Microsoft\Windows\CurrentVersion\Run` | [S19] |
| 开机自启（所有用户，仅一次；**仅管理员组登录时执行**） | `HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce` | [S19] |
| 开机自启（当前用户，每次登录） | `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` | [S19] |
| 开机自启（当前用户，仅一次） | `HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce` | [S19] |
| 文件右键菜单命令（verb） | `HKEY_CLASSES_ROOT\<ProgID>\shell\<verb>\command`，`(Default)` = 命令行 | [S23] |
| 某应用处理任意文件类型的默认过程 | `HKEY_CLASSES_ROOT\Applications\<MyProgram.exe>\shell\...` | [S23] |
| 类级右键菜单（真实示例） | `HKEY_CLASSES_ROOT\DesktopBackground\Shell` | [S25] |
| 无需提权注册自定义 verb | `HKEY_CURRENT_USER\Software\Classes` | [S25] |
| 32 位程序在 64 位系统上的视图 | `HKEY_LOCAL_MACHINE\Software\WOW6432Node`（**保留键，不应直接使用**） | [S6][S20] |
| 硬件/即插即用历史 | `HKLM\HARDWARE`（含 `DESCRIPTION`、`DEVICEMAP`、`RESOURCEMAP`、`ACPI`、`UEFI`） | [S21]（`Get-ChildItem -Path HKLM:\HARDWARE` 输出）、[S1] |
| 用户配置文件 hive 的键位置 | `HKEY_USERS` 下，每个登录用户一个 | [S2] |
| 硬件配置文件信息 | `HKLM\System\CurrentControlSet\Hardware Profiles\Current`（= HKEY_CURRENT_CONFIG） | [S4] |
| 系统信息（官方示例出现的版本类路径） | `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion` | [S22] |

### 5. 需要降维改写的内容

| 原始术语 | 出现在 | 零基础读者的问题 | 改写方向 |
| --- | --- | --- | --- |
| **hive / 配置单元** | S2、S3、S21 | "配置单元"是生造词，读者无法与磁盘文件建立联系 | 首次出现写「注册表的"数据库文件"（官方术语叫 hive，中文译作"配置单元"）」，并立刻给"它是磁盘上真实存在的文件"这一落点；后文统一用"注册表文件"或直接给文件名 |
| **ACL / 安全描述符 / SACL** | S7 | 纯 Windows 安全模型的开发者术语 | 只保留读者需要的动作层：**"每个注册表键都带一张权限清单，默认从父键继承"**；ACL/SACL/安全描述符三个词压缩成一条脚注，正文用"权限清单""审计清单" |
| **WOW6432Node / 注册表视图 / KEY_WOW64_*** | S20、S6、S9 | "WOW64""备用视图""0x0100 掩码"对零基础完全无意义 | 改写为：**"64 位系统上其实有两套注册表：64 位程序看一套，32 位程序看另一套，32 位那套被挂在 WOW6432Node 下面"**；掩码数字只作为开发者的补充信息放进折叠块或删去；强调读者真正会遇到的只有 `/reg:32`、`/reg:64` 两个开关和"不要直接改 WOW6432Node"这条告诫 |
| **`REG_*` 类型名与掩码** | S5、S6、S21 | 读者在 regedit 里看到的是「字符串值 / DWORD 值 / 二进制值 / 多字符串值」，不是 `REG_SZ` | 用**三列对照**：`REG_SZ` ↔ regedit 显示"字符串值" ↔ PowerShell 的 `-Type String`；再补一列"什么时候用"。`REG_DWORD_LITTLE_ENDIAN` 只需一句"Windows 上它就等于 REG_DWORD，不用管" |
| **`\0` / null 结尾 / 终止符** | S5、S27 | 非计算机专业读者不知 `\0` 是什么 | 写成"字符串末尾的隐藏结束符"；`REG_MULTI_SZ` 的"两个终止 null"改写为"结尾要有两个隐藏结束符，所以列表里不能有空行" |
| **小端 / 大端（little-endian）** | S5 | 与日常使用完全无关 | 压成一句可选脚注：Windows 是小端，因此 `REG_DWORD` 就是小端格式，读者不需要理解字节序 |
| **ProgID / verb / ShellExecuteEx** | S23、S24、S25 | 三个词都需要解释 | verb → "右键菜单里的**一条命令项**"；ProgID → "文件类型的**登记名**，格式是 `厂商.组件.版本`"；ShellExecuteEx 完全不进正文 |
| **间接字符串 `@%SystemRoot%\shell32.dll,-154`** | S24 | 看着像乱码 | 只作为"别手动改这类值"的警告出现，不解释语法 |
| **事务日志 `.log` / `.alt` / `.sav`** | S2 | 读者会误以为可以手动删/改 | 改写为"这些是**系统自己用的副本和日志，不要动它们**"，重点是"不要删"而不是"它们是什么" |
| **预定义项 / 句柄 / `RegOpenKeyEx`** | S1、S4、S7 | API 视角 | 全部下沉到"给开发者的补充"区块；正文只说"注册表有 5 个顶层文件夹（HKLM、HKCU、HKCR、HKU、HKCC）" |
| **256 字符 / 16383 字符 / 2048 字节 / 64K 限制** | S6、S19 | 四个数字容易被误记混 | 做成一张小表并各配一句"什么时候会遇到"：Run 键命令行 ≤260 字符（写自启）；值名称 ≤16383 字符；值数据 >2048 字节要改存文件；**一个键里所有值加起来 ≤64K**（装不下时就要拆键或改存文件） |
| **"父子项"** | S15、S16 | 官方原文的"保存父子项"表述生硬 | 改写为"保存这个键**以及它下面的所有子键和值**" |
| **`SE_TAKE_OWNERSHIP_NAME` / `WRITE_OWNER`** | S7 | 特权名与访问权名都是英文常量 | 改写为"**取得所有权**"与"以**所有者身份写入**的权限"，常量名放脚注；正文给读者动作："在权限对话框里把所有者改成自己，再赋完全控制" |

### 6. 未解决问题与缺口

以下内容在本轮来源中**无法追溯**，不得写入第 2 节，需后续补抓或降级处理：

1. **训练模块 B-1 / B-2 不可用**。`learn.microsoft.com/zh-cn/training/modules/explore-windows-architecture/4-examine-windows-registry` 与 `.../5-use-windows-registry-editor` 在 zh-cn 与 en-us 下均只返回课程目录页（74–182 字）。已用 S1/S2/S4/S18 覆盖其职能，但**"使用注册表编辑器"的界面级操作（新建项/重命名/查找/收藏夹）在官方来源中缺失**，目前只有 S18 的导出/导入，以及 S6 的一句能力清单："可以使用注册表编辑器执行以下操作：查找子树、项、子项或值；添加子项或值；更改值；删除子项或值；重命名子项或值"。
2. **`Checkpoint-ComputerRestore` 页面 404**。`microsoft.powershell.management/checkpoint-computerrestore` 在 `?view=powershell-5.1`、`powershell-7.6`、`windowsserver2022-ps` 下均返回 404。**"创建还原点"的官方 cmdlet 出处缺失**，第 4.3 节只能给 `Enable-ComputerRestore`（启用）而给不出官方"创建还原点"命令。需重新定位（可能已迁出 `Microsoft.PowerShell.Management` 或需要不同 URL）。
3. **`USRCLASS.DAT` 在全部 27 条来源中零命中**。P1 明确要求覆盖 `NTUSER.DAT / USRCLASS.DAT`，但官方 Win32 / KB 页只提到 `Ntuser.dat`、`Ntuser.dat.log`，**没有任何一条来源提到 USRCLASS.DAT**。需补抓（候选方向：`HKCU\Software\Classes` 的磁盘承载文件相关页，或 User Profile 相关页）。
4. **`RegBack` 目录零命中**。全部来源未出现 `RegBack`。P1 要求的"RegBack"磁盘位置目前无官方出处。
5. **环境变量的注册表路径零命中**。P1 指定的 `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment` 与 `HKCU\Environment` 在 S27（User Environment Variables）中**完全未出现**——S27 只讲环境块（environment block）、`CreateEnvironmentBlock` 和"控制面板 → 系统 → 环境"的界面路径，另有"用 `set` 命令设置的环境变量只对设置它的那个命令窗口及其子进程有效"。**该路径目前无官方来源支撑**，需补抓。
6. **`HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion` 路径未直接命中**。来源中出现的最接近路径是 S22 的 `HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion`（注意是 `...\Windows\CurrentVersion`，**不是** `...\Windows NT\CurrentVersion`）与 S21 的 `HKLM:\SOFTWARE\Microsoft\Wbem`。P1 点名的那个"系统信息"路径需单独验证。
7. **`HKCR\*\shell` 与 `AllFilesystemObjects` 通配 verb 未命中**。P1 明确点名 `HKCR\*\shell`，但 S23 与 S25 只给出 `HKEY_CLASSES_ROOT\<ProgID>\shell`、`HKEY_CLASSES_ROOT\Applications\...\shell`、`HKEY_CLASSES_ROOT\DesktopBackground\Shell`、`HKEY_CLASSES_ROOT\drive` 这几种形态，**没有任何一条来源提到 `*` 或 `AllFilesystemObjects` 这个通配写法**。若正文要写"给所有文件加右键菜单"，目前**没有 A 级出处**，需补抓，或改为只讲 ProgID 级 verb。
8. **管理员权限要求覆盖不全**。逐条核对后：只有 S18（regedit 导出/导入会弹管理员确认）与 S26（PowerShell 需"以管理员身份运行"）明确写了权限要求；S25 从反面确认了 `HKCU\Software\Classes` 路径"不需要提升权限"。**`reg export/import/save/restore/load` 是否需要管理员权限，官方页均未明示**；S7 只从 API 角度讲了 `SE_TAKE_OWNERSHIP_NAME` + `WRITE_OWNER` 的提权路径。P1 要求"标注是否需要管理员权限"，这一项目前**只能对 regedit、PowerShell 和 HKCU\Software\Classes 三条路径给出官方依据**，reg.exe 侧需另找出处或明确写"官方未说明"。
9. **`reg` 子命令的远程使用限制未逐条核对**。S9–S17 反复出现"如果指定了远程计算机，则有效的根密钥为 HKLM 和 HKU"，但 S8 总览只说"使用 reg 配置远程计算机的注册表会限制您可以在某些作中使用的参数。检查每个作的语法和参数，以验证它们是否可以在远程计算机上使用"——**具体哪些子命令不支持远程，未逐条核实完毕**。
10. **S1、S2、S3、S5、S7 页面均出现"访问此页面需要授权"的提示文本**。抓取内容完整（章节、表格、示例齐全），判断为爬虫未携带登录态时的页面模板提示，不影响内容可信度；但若后续需要引用页面内的交互式组件或图表，需人工复核。
11. **S6 的版本适用范围偏旧**。KB256986 的"适用于"标注为 "Supported versions of Windows Server"，但正文中的支持文件表、`%SystemRoot%\Profiles\Username`、`WOW6432Node` 描述带有明显的 Windows XP/2003/Vista 时代痕迹（页面 2026-02-12 更新，但技术描述未刷新）。引用时需注明"内容源自经典 KB，个别路径描述偏旧"。
12. **`Get-ItemProperty` 页面日期未取到**。S22 的抓取结果中未包含 "Last updated" 字段，与 S1/S2 等页的显式日期不同，无法标注确切更新时间。

### 7. 下游交接摘要

- 注册表 = 一棵树：节点叫键，键下可挂子项和值；顶层只有 5 个常用根键（HKLM 机器级、HKCU 用户级、HKCR 是合并视图不是真实位置、HKU 所有用户、HKCC 硬件配置别名）。
- 值有类型之分：最常用 REG_SZ（字符串）、REG_DWORD（32 位数字）、REG_BINARY（二进制）、REG_MULTI_SZ（多行列表）、REG_EXPAND_SZ（含 %变量% 的字符串）；regedit 显示名、reg.exe 的 `/t`、PowerShell 的 `-Type` 是同一套类型的三副面孔。
- 注册表在磁盘上是真实文件（hive）：机器级在 `%SystemRoot%\System32\Config`，用户级对应用户配置文件里的 NTUSER.DAT，`.log`/`.sav`/`.alt` 是系统自用副本，**不要删**。
- 三种执行方式各有定位：regedit 适合"看得见再改"，`reg.exe` 适合可复制的命令与批处理，PowerShell 用 `HKLM:` / `HKCU:` 驱动器适合脚本化；官方统一建议优先用图形界面或组策略，改注册表是最后手段。
- 动手前必须备份、出事必须能回滚：主路径是 regedit「文件 > 导出 / 导入」（官方步骤覆盖 Win11），进阶是 `reg save` → `reg restore`（.hiv，官方明写"编辑前必须 reg save"），整机兜底是备份系统状态；系统还原点可作附注但官方版本声明存疑。
- 两个最容易踩的坑要显式警告：一是 64 位系统上有两套注册表视图（WOW6432Node 是保留键，不应直接改），二是 RunOnce 的删值时机、`!` / `*` 前缀语义与"仅管理员组成员登录才执行"的行为差异。

---

## 方向 C — Windows PowerShell（精读素材）


### 1. 来源表

| ID | 标题 | URL | 层级 | 页面日期 | 抓取日期 | 支撑的子主题 |
| --- | --- | --- | --- | --- | --- | --- |
| C-1 | about_Pipelines（关于管道） | https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_pipelines | A | 2025-12-28 | 2026-09-10 | 管道传对象、参数绑定、一次性处理、原生命令管道 |
| C-2 | 发现 PowerShell | https://learn.microsoft.com/zh-cn/powershell/scripting/discover-powershell | A | 2026-04-10 | 2026-09-10 | 对象而非文本、Verb-Noun 命名、四大探索 cmdlet |
| C-3 | about_Execution_Policies（执行策略） | https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_execution_policies | A | 2026-08-31 | 2026-09-10 | 执行策略、作用域、组策略、Unblock-File |
| C-4 | 从 Windows PowerShell 5.1 迁移到 PowerShell 7 | https://learn.microsoft.com/zh-cn/powershell/scripting/whats-new/migrating-from-windows-powershell-51-to-powershell-7 | A | 2026-04-10 | 2026-09-10 | 5.1/7 并行、路径差异、PSModulePath、配置文件、ISE |
| C-5 | about_Providers（提供程序） | https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers | A | 2025-02-05 | 2026-09-10 | Provider 与 PSDrive、统一路径模型、动态参数 |
| C-6 | Get-Help (Microsoft.PowerShell.Core) | https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/get-help | A | 未标注 | 2026-09-10 | 帮助系统入口、-Online/-Full/-Parameter、about_ 文章 |
| C-7 | Update-Help (Microsoft.PowerShell.Core) | https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/update-help | A | 未标注 | 2026-09-10 | 帮助文件下载、每天一次限制、Scope、en-US |
| C-8 | about_Character_Encoding（字符编码） | https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_character_encoding | A | 2025-01-30 | 2026-09-10 | 5.1/7 编码差异、BOM、重定向编码、中文乱码原理 |
| C-9 | Get-ChildItem (Microsoft.PowerShell.Management) | https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-childitem | A | 未标注 | 2026-09-10 | 文件系统/注册表浏览、-Force/-Recurse/-LiteralPath |
| C-10 | Set-Location (Microsoft.PowerShell.Management) | https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/set-location | A | 未标注 | 2026-09-10 | 切换位置、跨 Provider 导航、位置历史 |
| C-11 | Get-ItemProperty (Microsoft.PowerShell.Management) | https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-itemproperty | A | 未标注 | 2026-09-10 | 读注册表值、读文件属性、Registry:: 备用路径 |
| C-12 | Set-ItemProperty (Microsoft.PowerShell.Management) | https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/set-itemproperty | A | 未标注 | 2026-09-10 | 写注册表值、-Type 动态参数、值与项的区别 |
| C-13 | Get-PSDrive (Microsoft.PowerShell.Management) | https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-psdrive | A | 未标注 | 2026-09-10 | 列出驱动器、PSDrive 与 Windows 映射的区别 |
| C-14 | about_PSModulePath | https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_psmodulepath | A | 2026-08-25 | 2026-09-10 | 模块搜索路径、5.1/7 路径差异、Documents 重定向 |
| C-15 | New-Item (Microsoft.PowerShell.Management) | https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/new-item | A | 未标注 | 2026-09-10 | 新建文件/目录/注册表项/profile 文件 |
| C-16 | PowerShell 与 cmd / Bash 逐项对照表 | 无独立 URL | 本文整理（来源见 C-2 / C-4） | 不适用 | 2026-09-10 | 新手心智模型对照 |
| C-17 | Windows 中打开 powershell 后，出现报错"无法加载文件 xxxx，因为在此系统上禁止运行脚本" | https://www.cnblogs.com/geekbruce/articles/18905587 | C 级 · 经验型 | 2025-05-31 | 2026-09-10 | "禁止运行脚本"报错的真实表现 |
| C-18 | 解决 PowerShell 中文乱码问题 | https://blog.csdn.net/chao_666666/article/details/156590250 | C 级 · 经验型 | 2026-01-05 发布 / 2026-01-06 修改 | 2026-09-10 | 中文乱码的真实表现与常见改法 |
| C-19 | Encoding Failure in Windows PowerShell with Chinese Directory Paths（GitNexus issue #1811） | https://github.com/abhigyanpatwari/GitNexus/issues/1811 | C 级 · 经验型 | 2026-05-25 | 2026-09-10 | 中文路径下 native 层 Error 3 的真实表现 |

抓取说明：本轮共发起 21 次抓取，成功 17 次、失败 4 次。失败的为知乎（HTTP 403 反爬）、CSDN 部分文章（`minimal_text` 反爬）与 cnblogs 一篇（返回用户中心空页），未写入来源表；替代来源见第 6 节缺口说明。

---

### 2. 论断 / 来源映射

版本标注含义：`5.1` = Windows PowerShell（`powershell.exe`）；`7` = PowerShell 7（`pwsh.exe`）。

#### 2.1 核心设计理念：对象而非文本

- PowerShell 与其他 shell 的根本区别是**接受并返回 .NET 对象而不是文本**，因此管道连接更省事 → [C-2]（5.1 / 7）
- 管道是由管道操作符 `|`（ASCII 124）连接的一系列命令，每个运算符把上一条命令的结果发给下一条，按从左到右处理 → [C-1]（5.1 / 7）
- 因为管道传的是进程对象，`Get-Process notepad | Stop-Process` 中 `Stop-Process` 无需 `-Name` / `-ID`；另注意 PowerShell 的"成功流 / 错误流"类似 stdout / stderr，但 **stdin 并未接入 PowerShell 管道** → [C-1]（5.1 / 7）

#### 2.2 管道参数绑定与"一次性处理"（易错核心）

- 接收端 cmdlet 必须有"接受管道输入"的参数；用 `Get-Help <cmdlet> -Full` 或 `-Parameter *` 才能查到是哪个参数、按什么方式接收 → [C-1]（5.1 / 7）
- 接收方式有两种：**ByValue**（值可转换到目标 .NET 类型）与 **ByPropertyName**（输入对象有同名属性）；绑定成功需同时满足"参数接受管道输入 + 类型匹配或可转换 + 该参数未在命令中显式使用"，且**无法强制 PowerShell 绑定到特定参数**，绑不上命令就失败 → [C-1]（5.1 / 7）
- 关键区别：管道**一次发送一个对象**，用 `-InputObject` 参数则把集合当**单个数组对象**发送；官方原话是"这种细微差异具有重大后果"，例如 `Get-Process | Get-Member` 显示 `System.Diagnostics.Process`，而 `Get-Member -InputObject (Get-Process)` 显示 `System.Object[]` → [C-1]（5.1 / 7）
- 管道执行时会自动枚举实现 `IEnumerable` 的类型，但有例外：**哈希表需调用 `GetEnumerator()`**，且 **`System.String` 虽实现 `IEnumerable` 却不会被枚举** → [C-1]（5.1 / 7）

#### 2.3 发现 PowerShell：命名约定与探索命令

- PowerShell 命令称为 cmdlet（读作"命令莱特"），名字由 **Verb-Noun** 组成（如 `Get-Process`），谓词应取自 `Get-Verb` 返回的标准动词表 → [C-2]（5.1 / 7）
- 四个"自举"命令足以发现几乎所有内容：`Get-Verb`（合法动词）、`Get-Command`（装了哪些命令，支持 `-Name` / `-Verb` / `-Noun` / `-ParameterType` 过滤）、`Get-Member`（对象有哪些属性和方法）、`Get-Help`（命令怎么用） → [C-2]（5.1 / 7）

#### 2.4 帮助系统（Get-Help / Update-Help / Get-Command / Get-Member 分工）

- 三者定位不同：`Get-Command` 回答"有哪些命令"、`Get-Member` 回答"这个对象有什么"、`Get-Help` 回答"这个命令怎么用、参数是什么" → [C-2] + [C-6]（5.1 / 7）
- `Get-Help` 从本机帮助文件取内容，**没有帮助文件时只显示基本信息**；从 PowerShell 3.0 起 Windows 自带模块**不含**帮助文件，需用 `Update-Help` 下载或改用 `-Online` → [C-6]（5.1 / 7）
- `-Detailed` / `-Full` / `-Examples` / `-Parameter` **仅在计算机安装了帮助文件时有效，且对 `about_` 概念文章无效**；`-Online` 在浏览器中打开帮助，**不能在远程会话中使用** → [C-6]（5.1 / 7）
- 概念文章名（如 `about_Objects`）**必须以英语输入**，即使是非英语版 PowerShell；`Get-Help about_*` 列出全部概念文章 → [C-6]（5.1 / 7）
- `Update-Help` 无 `-Force` 时**每 24 小时只运行一次**，每个模块下载上限 **1 GB** 未压缩内容；官方说明每天一次的限制正是为了让用户能安全地把它写进配置文件 → [C-7]（5.1 / 7）
- `Update-Help` 权限按版本不同：**PowerShell 6.0 及更低版本需要管理员权限；6.1 及更高版本 `-Scope` 默认 `CurrentUser`**，但更新 `$PSHOME\Modules` 中的模块仍需"以管理员身份运行" → [C-7]（5.1 与 7 差异）
- **en-US 帮助文件始终发布**；系统区域为 en-GB 等不受支持的语言时会报 `The specified culture is not supported`，需显式 `Update-Help -UICulture en-US` → [C-7]（5.1 / 7）

#### 2.5 执行策略（"禁止运行脚本"的官方来源）

- 执行策略**不是安全边界**，而是"深层防御"：用户无法运行脚本时，直接在命令行粘贴脚本内容即可绕过 → [C-3]（5.1 / 7）
- `Restricted` 允许单个命令但**阻止所有脚本文件**，包括 `.ps1xml`、`.psm1` 和 PowerShell 配置文件（`.ps1`）；从 Internet 下载的脚本会被标记"来自 Internet"，`RemoteSigned` 下不运行未签名者，可用 `Unblock-File` 解除，但 `curl.exe` / `Invoke-RestMethod` / `Invoke-WebRequest` 下载的文件**不会**带此标记 → [C-3]（5.1 / 7）
- 默认策略 `Default` = 客户端与服务器均为 **RemoteSigned**；若所有作用域都是 `Undefined`，则客户端有效策略是 **Restricted**、服务器是 **RemoteSigned** → [C-3]（5.1 / 7）
- 作用域优先级：`Process`（最高，存 `$Env:PSExecutionPolicyPreference`，**不写注册表**）> `CurrentUser`（存用户 `powershell.config.json`）> `LocalMachine`（存 `$PSHOME/powershell.config.json`）；**组策略设置覆盖所有作用域** → [C-3]（5.1 / 7）
- `Get-ExecutionPolicy -List` 按优先级列出各作用域实际值；`Set-ExecutionPolicy -Scope CurrentUser` **不需要管理员**，改 `LocalMachine` 需要管理员 → [C-3]（5.1 / 7）

#### 2.6 Provider 与 PSDrive（"一切皆盘符"的统一模型）

- Provider 把专用数据存储以**驱动器形式**暴露，路径与使用方式同硬盘；内置 8 个：Alias / Certificate / Environment / FileSystem / Function / Registry / Variable / WSMan。其中**Certificate、Registry、WSMan 仅在 Windows 平台可用** → [C-5]（5.1 / 7）
- 同一批 cmdlet 可作用于任何 Provider 的数据：`New-Item` 在 `C:` 建文件、在注册表建键、在 `Alias:` 建别名，用法相同；分层数据用 `drive:\location\child-location` 导航，含空格须用双引号，`.` 与 `..` 分别表示当前与上层 → [C-5] + [C-15]（5.1 / 7）
- FileSystem 是唯一有默认 Home 的 Provider（值等于 `$HOME`），`~` 表示 Home；没有 Home 的 Provider 用 `~` 会报错 → [C-5]（5.1 / 7）
- 动态参数只在配合特定 Provider 时才出现，例如 `Cert:` 给 `Get-Item` / `Get-ChildItem` 增加 `CodeSigningCert`；用 `Get-Help <provider-name>` 查该 Provider 的动态参数 → [C-5]（5.1 / 7）
- `Get-PSDrive` 能看到 `New-PSDrive` 创建的会话级驱动器，而 `net use`、`[System.IO.DriveInfo]::GetDrives()`、`Get-CimInstance` **都看不到** → [C-13]（5.1 / 7）

#### 2.7 Windows PowerShell 5.1 与 PowerShell 7 的并行关系

- 两个版本**并行安装并行运行**，各有独立的安装路径、可执行文件名、`PSModulePath`、配置文件、事件日志；5.1 是 `powershell.exe`（`$Env:windir\System32\WindowsPowerShell\v1.0`），6/7 是 `pwsh.exe`（`$Env:ProgramFiles\PowerShell\7`） → [C-4]（5.1 / 7 并存）
- PowerShell 7 的 `$Env:PSModulePath` **额外包含 Windows PowerShell 路径**（`$HOME\Documents\WindowsPowerShell\Modules` 等）以支持模块自动加载；5.1 的默认模块路径是 `$HOME\Documents\WindowsPowerShell\Modules` 与 `$Env:ProgramFiles\WindowsPowerShell\Modules` → [C-4] + [C-14]（两版本差异）
- 配置文件位置改名：5.1 为 `$HOME\Documents\WindowsPowerShell`，7 为 `$HOME\Documents\PowerShell`；用 `$PROFILE | Select-Object *Host* | Format-List` 查看实际路径 → [C-4]（两版本差异）
- PowerShell 7.4 基于 **.NET 8.0**，5.1 基于 **.NET Framework 4.x**，版本差异可能影响脚本行为（尤其是直接调用 .NET 方法时）；ISE 仅支持 5.1、无更新计划，官方推荐 VS Code PowerShell 扩展 → [C-4]（两版本差异）

#### 2.8 编码与中文乱码（A 级原理）

- Windows 支持 Unicode 与传统字符集，**PowerShell 默认使用 Unicode**，但多个 cmdlet 有 `-Encoding` 参数可指定其他字符集 → [C-8]（5.1 / 7）
- 在 Windows PowerShell 中**除 `UTF7` 外任何 Unicode 编码总是创建 BOM**；PowerShell（v6 及以上）**默认为所有文本输出 `utf8NoBOM`** → [C-8]（5.1 与 7 的关键差异）
- Windows PowerShell 中"默认编码"其实**不一致**：`Out-File` 与 `>` / `>>` 创建 **UTF-16LE**；`Export-Csv` 创建 **ASCII**；`New-Item -Type File -Value` 创建**不带 BOM 的 UTF-8**；`Add-Content` / `Set-Content` 在目标文件为空或不存在时用 `Default`（系统 ANSI 旧代码页） → [C-8]（仅 5.1）
- 自动变量 `$OutputEncoding` **只影响 PowerShell 与外部程序通信的编码，不影响重定向运算符和 cmdlet 写文件的编码**；从 PowerShell 5.1 起 `>` 和 `>>` 内部调用 `Out-File`，所以 `$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'` 能同时管住写文件和重定向 → [C-8]（5.1 起 / 7）
- BOM 取舍双向：官方一处建议"为避免 UTF-8 文件中使用 BOM"（Unix 工具不支持），另一处指出**含非 ASCII 字符的脚本在 5.1 下需要 BOM，否则会被误读为过时的 ANSI 代码页** → [C-8]（5.1 与 7 建议相反）

#### 2.9 PowerShell 与 cmd / Bash 的对照

- 与 cmd / Bash 的根本差别不在命令名，而在**管道里流动的是对象还是文本**，以及**命令名遵循 Verb-Noun 而非简写**；逐项对照见第 4 节表 → [C-16]（5.1 / 7）

#### 2.10 文件系统与注册表常用 Cmdlet（衔接方向 A / B）

- `Get-ChildItem` 是通用列项命令（别名 `dir`、`gci`），**默认不显示隐藏项**，需 `-Force`；`-Force` **不会替代安全限制**。官方明确**不建议把 `-Path` 与 `-Recurse` 一起用**，应改用 `-LiteralPath` 指定目标目录 + `-Filter` / `-Include` 指定匹配模式 → [C-9]（5.1 / 7）
- 注册表"值"是键的**属性**而不是项/子项：用 `Get-Item` 或 `Get-ChildItem` 看不到值，必须用 `Get-ItemProperty` / `Set-ItemProperty`；也可用 `Registry::HKEY_LOCAL_MACHINE\...` 形式绕开 `HKLM:` 驱动器 → [C-11] + [C-12]（5.1 / 7）
- `Set-Location` 可切换到任何 Provider 路径（`HKLM:\`、`Cert:\`、`Env:\`）；驱动器名不带反斜杠（如 `C:`）时表示"恢复到该盘当前目录" → [C-10]（5.1 / 7）
- PowerShell 6.2 起 `Set-Location -Path -` / `+` 可在**最近 20 个位置**的历史中前后导航，`cd -` 是最短写法；官方同时备注 PowerShell 的"当前目录"是**每个 runspace 独立**的，与 `[System.Environment]::CurrentDirectory` 不同 → [C-10]（前者仅 7 / 6.2 起）

#### 2.11 社区经验型现象（仅现象，原理必须回溯 A 级）

- 现象：打开 PowerShell 即报 `无法加载文件 C:\Users\<用户>\Documents\WindowsPowerShell\profile.ps1，因为在此系统上禁止运行脚本`，并伴随 `CategoryInfo: SecurityError ... PSSecurityException` —— 原理对应 `Restricted` 阻止 `.ps1` 配置文件、以及 `Undefined` 时客户端有效策略为 `Restricted` → [C-17]（现象）+ [C-3]（原理）**C 级 · 经验型**
- 现象：正常中文被显示成 `UTF-8 缂栫爜宸查厤缃畬鎴愶紒` 一类字符，社区归因为"控制台代码页 936（GBK）与脚本文件 UTF-8 不一致" —— 原理对应 5.1 的 `Out-File` UTF-16LE 默认与 `-Encoding` 参数 → [C-18]（现象）+ [C-8]（原理）**C 级 · 经验型**
- 现象：中文目录会让第三方 native 组件报 `Error 3: The system cannot find the path specified.`，而路径在资源管理器中可见 —— 官方 A 级来源本轮未覆盖 native API 层，**原理未落到 A 级** → [C-19] **C 级 · 经验型**（详见第 6 节）

---

### 3. 矛盾与冲突

1. **"Windows PowerShell 默认编码"不存在单一答案。** C-8 同一页先说"通常，Windows PowerShell 默认使用 Unicode UTF-16LE 编码"，紧接着又说"Windows PowerShell 中 cmdlet 使用的默认编码不一致"，同页列举的 `Out-File`（UTF-16LE）、`Export-Csv`（ASCII）、`Add-Content` 空文件（ANSI Default）互相矛盾。写作时必须把结论限定为"**按 cmdlet 分别判断**"，不能写成"5.1 默认是 XX 编码"。

2. **BOM 的建议方向相反，取决于文件类型。** C-8 一处说"为获得最佳整体兼容性，**避免**在 UTF-8 文件中使用 BOM"（针对跨平台工具链），另一处说"如果需要在脚本中使用非 Ascii 字符，**请使用 BOM** 将它们另存为 UTF-8"（针对 5.1 读 `.ps1`）。C-18（C 级）只主张后者。两者不是真冲突，但必须按"脚本源码 vs 数据文件"分开表述，否则会让零基础读者得出互相打架的结论。

3. **C 级文章把执行策略当成"安全方案"，A 级明说它不是安全边界。** C-17 推荐 `AllSigned` 并称"提高安全性"，C-18 相关段落未提任何限制；而 C-3 明确"执行策略不是安全边界，它是深层防御……可以在命令行中键入脚本内容，从而轻松绕过策略"。改写时必须保留 C-3 的限定语。

4. **"迁移简单、快速且安全"是官方立场，但存在未覆盖的落差。** C-4 开头称迁移"简单、快速且安全"，同页又说明 ISE 不再更新、部分模块需要 `Import-Module -UseWindowsPowerShell` 兼容层、.NET 版本差异可能改变脚本行为。对零基础读者，"简单"应降级为"5.1 与 7 可以共存，所以可以慢慢迁"。

5. **C 级文章普遍漏掉 `Update-Help` 的硬限制。** 中文社区常见建议是"把 `Update-Help` 写进 `$PROFILE` 自动更新"，但都没提"每 24 小时只运行一次"和"每模块 1 GB"上限（C-7 明确列出，且说明每天一次限制正是为了让用户能安全地把它放进配置文件）。不是冲突，而是 C 级来源不完整。

6. **编码问题的归因层次不同。** C-18 把中文乱码全部归因于"代码页 936 vs UTF-8 不一致"，C-8 则指出还涉及 `$OutputEncoding`（对外部程序）与 cmdlet `-Encoding`（对文件）两条**互不相干**的通道。C-18 的方案在"写文件正常但调用外部程序仍乱码"时会失效。

7. **社区与官方对"该用哪个策略"的默认推荐不一致。** C-17 把 `AllSigned` 列为"建议"、`RemoteSigned` 列为"折中方案"；C-3 明确说 Windows 的默认策略（`Default`）就是 **RemoteSigned**。以 A 级为准，正文应把 RemoteSigned 写成默认与推荐项。

---

### 4. 可操作指引

以下命令均已标注适用版本。`5.1` = `powershell.exe`，`7` = `pwsh.exe`。

#### 4.1 认识环境（先跑这几条）

```powershell
# 查看当前会话运行的版本 —— 5.1 / 7
$PSVersionTable

# 查看当前会话有哪些驱动器（含 Provider 驱动器） —— 5.1 / 7
Get-PSDrive

# 查看各作用域的执行策略取值 —— 5.1 / 7
Get-ExecutionPolicy -List

# 查看本机 Provider 列表 —— 5.1 / 7
Get-PSProvider
```
→ [C-13] [C-3] [C-5]

#### 4.2 帮助系统（推荐的标准流程）

```powershell
# 首次：下载本机帮助文件（PowerShell 6.1+ 默认只装当前用户，无需管理员） —— 5.1 / 7
Update-Help -Verbose

# 若系统区域不是 en-US 而下载失败（报 The specified culture is not supported） —— 5.1 / 7
Update-Help -UICulture en-US -Force

# 查命令怎么用 —— 5.1 / 7
Get-Help Get-ChildItem
Get-Help Get-ChildItem -Examples
Get-Help Get-ChildItem -Parameter Path
Get-Help Get-ChildItem -Online        # 打开浏览器版本；不能在远程会话中用

# 逐页阅读（help 内部分页调用 Get-Help，man 是 help 的别名） —— 5.1 / 7
help Get-ChildItem
Get-ChildItem -?                      # 等价于 Get-Help，但只对 cmdlet 有效

# 查概念文章（名字必须用英语） —— 5.1 / 7
Get-Help about_*
Get-Help about_Execution_Policies

# 查提供程序专属帮助 —— 5.1 / 7
Get-Help Certificate
Get-Help Registry
```
→ [C-6] [C-7] [C-5]

**官方推荐的"找命令"顺序**：`Get-Command -Verb Get -Noun U*`（有哪些命令）→ `Get-Help`（怎么用）→ `Get-Process | Get-Member`（返回对象有什么属性/方法）→ [C-2] [C-6]（5.1 / 7）

**管道绑定失败时的官方排查手段** —— 5.1 / 7：
```powershell
Trace-Command -Name ParameterBinding -PSHost -Expression {
  Get-Item -Path HKLM:\Software\MyCompany\sales |
    Move-ItemProperty -Path HKLM:\Software\MyCompany\design -Name product
}
Get-Help Move-ItemProperty -Parameter Destination   # 看它是否按属性名接收管道输入
Get-Item -Path HKLM:\Software\MyCompany\sales | Get-Member   # 看对象有没有 Destination 属性
```
→ [C-1]

#### 4.3 执行策略（"禁止运行脚本"的标准解法）

```powershell
# 只看不写 —— 5.1 / 7
Get-ExecutionPolicy
Get-ExecutionPolicy -List

# 官方推荐的最小改动：只影响当前用户，不需要管理员 —— 5.1 / 7
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 只对当前会话生效，不落盘（改的是 $Env:PSExecutionPolicyPreference） —— 5.1 / 7
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 起一个"只这一次"的会话 —— 5.1 用 powershell.exe，7 用 pwsh.exe
pwsh.exe -ExecutionPolicy RemoteSigned

# 解除"来自 Internet"标记（下载的脚本被 RemoteSigned 拦下时） —— 5.1 / 7
Unblock-File -Path .\downloaded.ps1

# 恢复默认（删除当前用户设置，回到系统默认值） —— 5.1 / 7
Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope CurrentUser
```
→ [C-3]

#### 4.4 编码与中文（5.1 必做，7 可选）

```powershell
# —— 先诊断：看当前代码页与三条编码通道 —— 5.1 / 7
chcp
[Console]::OutputEncoding
[Console]::InputEncoding
$OutputEncoding

# —— 写文件时显式指定编码（最不容易错） —— 5.1 / 7
'你好' | Out-File -FilePath .\a.txt -Encoding utf8
'你好' | Set-Content -Path .\a.txt -Encoding utf8

# —— 会话级默认：让所有 cmdlet 的 -Encoding 都走 utf8 —— 5.1（5.1 起）/ 7
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

# —— 会话级：控制台与对外部程序的编码（中文乱码的临场解法） —— 5.1 / 7
# 注意：$OutputEncoding 只影响与外部程序通信，不影响写文件
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding  = [System.Text.Encoding]::UTF8
$OutputEncoding           = [System.Text.Encoding]::UTF8

# —— 落盘到配置文件（永久生效） —— 5.1 / 7
Test-Path $PROFILE
New-Item -Path $PROFILE -ItemType File -Force   # 不存在时先创建
notepad $PROFILE
```
→ [C-8] + [C-18]（C 级 · 经验型，提供的是社区通行写法）

> **写入 `$PROFILE` 时的关键分歧**：C-18 主张存为 **UTF-8 BOM**，C-8 主张脚本文件**避免 BOM**。官方口径是"5.1 下含非 ASCII 字符的脚本需要 BOM，否则会被当成过时 ANSI 代码页读取"——因此 **5.1 的 `$PROFILE` 用 UTF-8 BOM，纯数据文件用 UTF-8 无 BOM**。→ [C-8] [C-18]

#### 4.5 文件系统与注册表常用操作（衔接方向 A / B）

```powershell
# —— 文件系统 —— 5.1 / 7
Get-ChildItem -Path C:\Test                                 # 列目录（别名 dir / gci）
Get-ChildItem -Path C:\Test -Force                          # 含隐藏/系统项
Get-ChildItem -LiteralPath C:\Test -Recurse -Filter *.log   # 官方推荐的递归写法
Set-Location C:\Test                                        # 切换目录（别名 cd / chdir）

# —— 位置历史（PowerShell 6.2 起，仅 7 可用；5.1 不可用） —— 7
cd -
cd +

# —— 注册表：读值 —— 5.1 / 7
Get-ItemProperty -Path HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion -Name ProgramFilesDir
Get-ItemProperty -Path HKLM:\SOFTWARE\Microsoft\PowerShell\1\PowerShellEngine

# —— 注册表：写值（值属于"属性"，不是"项"） —— 5.1 / 7
Set-ItemProperty -Path "HKLM:\Software\ContosoCompany" -Name "NoOfEmployees" -Value 823
Get-ItemProperty -Path "HKLM:\Software\ContosoCompany"   # 用 Get-ChildItem 看不到它

# —— 新建项 / 文件 / 目录 —— 5.1 / 7
New-Item -Path "C:\" -Name "Logfiles" -ItemType "Directory"
New-Item -Path $PROFILE -ItemType "File" -Force

# —— 路径备用写法（不依赖 HKLM: 驱动器） —— 5.1 / 7
Get-ItemProperty -Path Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion
```
→ [C-9] [C-10] [C-11] [C-12] [C-15]

#### 4.6 对照表：PowerShell vs cmd vs Bash（本文整理，来源见 C-2 / C-4）

| 维度 | PowerShell 5.1（`powershell.exe`） | PowerShell 7（`pwsh.exe`） | cmd.exe | Bash |
| --- | --- | --- | --- | --- |
| 管道传的东西 | .NET 对象 | .NET 对象 | 文本 | 文本 |
| 命令名风格 | Verb-Noun（`Get-ChildItem`）+ 别名（`dir`/`ls`） | 同 5.1 | 独立小工具（`dir`） | 独立小工具（`ls`） |
| 路径分隔符 | `\`（多数场景 `/` 也可用） | `\`（`/` 可用） | `\` | `/` |
| 盘符 | `C:`，另有 Provider 盘符 `HKLM:`、`Cert:`、`Env:` | 同 5.1 | `C:` | 无（挂载点） |
| 变量语法 | `$name`；环境变量 `$Env:NAME` | 同 5.1 | `%NAME%` | `$name` / `${name}` |
| 脚本扩展名 | `.ps1`（另有模块 `.psm1`、清单 `.psd1`） | `.ps1` | `.bat` / `.cmd` | `.sh`（常无扩展名） |
| 脚本执行前提 | 受执行策略约束（默认 RemoteSigned） | 受执行策略约束 | 不受执行策略约束 | 需 `chmod +x` |
| 默认文本输出编码 | 因 cmdlet 而异（`Out-File` = UTF-16LE） | 统一 `utf8NoBOM` | 系统 ANSI 代码页 | UTF-8 |
| 配置文件 | `$HOME\Documents\WindowsPowerShell\*profile.ps1` | `$HOME\Documents\PowerShell\*profile.ps1` | 无 | `~/.bashrc` 等 |
| 运行位置 | 仅 Windows | Windows / macOS / Linux | 仅 Windows | 类 Unix |

→ [C-16]，各格依据来自 [C-2]（对象 vs 文本、Verb-Noun）、[C-4]（可执行名、配置文件路径、跨平台、PSModulePath）、[C-5]（Provider 盘符）、[C-8]（默认编码）、[C-3]（执行策略）。

---

### 5. 需要降维改写的内容

| 原文表述（含来源） | 问题 | 零基础改写方向 |
| --- | --- | --- |
| "接受并返回 .NET 对象，而不是文本" → [C-2] | 零基础读者不知道 .NET 对象是什么，也不知道对象比文本好在哪 | 用对比场景讲：文本管道只能传字符串，想取"第 3 列"要切字符串；对象管道里每个进程自带 `Name`、`Id`、`Handles` 等带名字的格子，可以直接点出来 |
| "实现 `IEnumerable` 接口或其泛型对等接口的任何类型会被自动枚举" → [C-1] | 接口术语，且**反直觉**（数组会拆开、字符串不会） | 改写成"数组会被拆成一个个元素逐个往后传；字符串和哈希表不会被拆开"，各配一个可跑的例子 |
| "ByValue / ByPropertyName 参数绑定" → [C-1] | 零基础无法理解"绑定"这个动作 | 改成"下一个命令按什么规则接住上一个命令丢过来的东西：看值的类型（按值）还是看属性的名字（按属性名）" |
| "无法建议或强制 PowerShell 绑定到特定参数" → [C-1] | 抽象 | 改成排查步骤：报"输入对象无法绑定到任何参数"时，先 `Get-Help <cmd> -Parameter <目标参数>` 看它是否接受管道输入、按值还是按属性名 |
| "动态参数" → [C-5] | 术语；读者不知道为什么这个参数昨天不存在 | 改成"有些参数只有在特定盘符下才出现，比如在 `Cert:` 盘里 `Get-ChildItem` 才会多出 `-CodeSigningCert`" |
| "Provider 是 .NET 程序" → [C-5] | 实现细节，对使用者无用 | 直接讲效果："PowerShell 把注册表、证书、环境变量都做成了'盘'，用同一套 `dir` / `cd` 就能逛" |
| "执行策略不是安全边界，是深层防御" → [C-3] | 安全术语 | 改成"它防的是手滑，不是防坏人：改它主要是避免自己误运行来路不明的脚本，所以别为了省事关掉它" |
| "作用域优先级 Process > CurrentUser > LocalMachine，组策略覆盖一切" → [C-3] | 三级概念一次抛出 | 先只讲 `CurrentUser` 一条，用"只影响我自己、不用管理员"说清楚；`LocalMachine` / 组策略放到"公司电脑改了不生效怎么办"的排错小节 |
| "每个 runspace 有独立的当前目录，与 `[System.Environment]::CurrentDirectory` 不同" → [C-10] | 完全开发者视角，且零基础读者极少直接调 .NET | 可删，或压成一句提示："在 PowerShell 里 `cd` 只影响 PowerShell 自己，不影响你在脚本里调用的程序" |
| "BOM（字节顺序标记）" → [C-8] | 编码学概念 | 用现象讲：文件开头多 3 个看不见的字节，用来告诉程序"我是 UTF-8"；5.1 不加就会把中文当乱码读 |
| "`$PSDefaultParameterValues` / `$OutputEncoding`" → [C-8] | 变量名对新手无意义，且两者作用域不同极易混 | 分成两句话：`$OutputEncoding` 管"和外部程序说话"，`-Encoding` / `$PSDefaultParameterValues` 管"存到文件"；两者互不覆盖 |
| "PowerShell 7.4 基于 .NET 8.0，5.1 基于 .NET Framework 4.x" → [C-4] | 版本号对新手无意义 | 改成"如果你要跑只支持 5.1 的老模块，PowerShell 7 提供了兼容开关 `Import-Module -UseWindowsPowerShell`" |
| "`-Path` 与 `-Recurse` 一起用时的递归行为" → [C-9] | 官方备注本身就是开发者语气的边界情况说明 | 直接给结论 + 一条安全写法：`Get-ChildItem -LiteralPath <目录> -Recurse -Filter <模式>`，不解释内部机制 |
| "`Update-Help` 需要 Administrators 组成员身份" → [C-7] | 权限术语，且该限制按版本变化 | 改成"只有装在系统目录里的那部分帮助需要管理员；你自己装的模块，普通账户就能更新" |

---

### 6. 未解决问题与缺口

1. **中文用户名导致模块/配置文件路径异常，未落到任何可追溯来源。** 本轮尝试的三个中文社区来源全部抓取失败：知乎执行策略文（HTTP 403 反爬）、CSDN 中文用户名 conda 文（`minimal_text` 反爬）、cnblogs 编码文（返回"用户中心"空页）。因此"中文用户名导致 `PSModulePath` 乱码"只能列为待验证现象，**不要写进正文**。可用的 A 级相邻事实只有 [C-14]：Documents 文件夹位置会被文件夹重定向和 OneDrive 改变，官方给的验证命令是 `[Environment]::GetFolderPath('MyDocuments')`；以及 [C-4] 给出的两版本 `$Env:PSModulePath` 默认值清单。

2. **中文路径下 native 组件报 `Error 3: The system cannot find the path specified.` 缺 A 级原理。** 目前唯一来源 [C-19] 是第三方项目（GitNexus）的 issue，属 C 级且非 PowerShell 官方内容。若正文要写这条，必须先补 PowerShell 官方关于本机命令参数传递/编码的页面（如 `about_Parsing`、`PSNativeCommandArgumentPassing`），或降级为"某些第三方程序的已知限制"。

3. **无官方 PowerShell vs cmd / Bash 对照专页。** 已按任务要求以 [C-16] 自行归纳，逐格依据均能回溯到 A 级来源；但"变量语法""路径分隔符"两行来自 [C-2] 的间接推论而非官方成文对照，溯源强度弱于其他行。

4. **多张 cmdlet 参考页未标注更新时间。** [C-6] [C-7] [C-9] [C-10] [C-11] [C-12] [C-13] [C-15] 抓取结果中没有 `Last updated on` 字段，来源表的"页面日期"只能记"未标注"。若上游需要时效性声明，需改抓 `?view=powershell-7.6` 或英文页确认。

5. **PowerShell 7 的当前稳定版本号未确认。** [C-4] 只说明"PowerShell 7.4 基于 .NET 8.0"，未给出撰写时点的最新版本；来源表中的版本标注因此统一写作 `7` 而非具体小版本。

6. **执行策略在 Windows Server Core / Nano Server 上的 `AuthorizationManager check failed` 未纳入第 2 节。** [C-3] 有此专节（该场景依赖 `explorer.exe` 提供的区域检查 API，Server Core 上不存在），但对零基础读者属极边缘场景，已刻意剔除；若正文需要"企业服务器"章节可从 C-3 补回。

7. **`about_Execution_Policies` 中"UNC 路径不允许在 RemoteSigned 下运行"这条只在特定系统成立**（官方原文："在无法将通用命名约定（UNC）路径与 Internet 路径区分开来的系统上"），条件依赖平台，不建议对零基础读者写成通用结论。

8. **"7 与 5.1 并存"对新手实际意味着装哪个、用哪个，本轮来源未给官方倾向。** [C-4] 只说两者可以并行、迁移简单，未明确建议新手默认用哪个。正文若要给"就用 7"的结论，需要额外来源支撑（如 PowerShell 支持生命周期页）。

---

### 7. 下游交接摘要

- 主线骨架：**对象而不是文本 → 管道一次传一个对象 → 参数绑定决定谁能接住 → Provider 把一切变成盘符 → 统一用 Get-ChildItem / Get-ItemProperty / Set-Location 操作**；这条链能把 PowerShell 与 cmd/Bash 的区别一次讲透（C-1、C-2、C-5、C-16）。
- 新手三件套必须先教：`Get-Command` 找命令、`Get-Help` 看用法、`Get-Member` 看对象——并说清三者回答的是不同问题（C-2、C-6）。
- 两个版本必须全程并行标注：`powershell.exe`（5.1）与 `pwsh.exe`（7）可共存，但**默认编码、配置文件路径、PSModulePath、Update-Help 权限**四项行为不同，是本方向最易出错的地方（C-4、C-7、C-8）。
- 最大的两个实操坑都有 A 级原理可依：**"禁止运行脚本"= 执行策略**（`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`，且强调它不是安全边界）；**中文乱码 = 5.1 各 cmdlet 默认编码不一致**（改法是用 `-Encoding` 与 `$PSDefaultParameterValues`，不是只改 `chcp`）（C-3、C-8）。
- 有 3 条 C 级现象可作"你是不是也遇到这个"的开场素材，但只能写现象、原理必须回到 A 级；中文用户名路径与中文路径 native 报错两条**证据不足，本轮不建议写入正文**（C-17、C-18、C-19）。

---
---

## 5. 跨方向未解决问题汇总（P2 缺口）

三方向各自的第 6 节共记录 30+ 条缺口。以下按**对成章的影响程度**排序，只列会在笔记中留下空白的问题：

### 高影响（会形成可见空白，大纲阶段需决策）

| # | 问题 | 涉及方向 | 建议处理 |
|---|------|---------|---------|
| 1 | **中文用户名 → `PSModulePath` 异常**：三个来源全挂，**无任何可用来源** | C | 方向 C 明确建议**不写进正文**，避免无来源断言 |
| 2 | **中文路径下调用外部程序报 `Error 3`**：仅有第三方 C 级 issue，缺 A 级原理 | C | 只作为"现象"在经验型区块提及，不解释成原理 |
| 3 | **`mklink /d` 是否需要管理员权限**：官方页完全未提，而这是零基础读者最常见的卡点 | A | 大纲阶段决定是"标注官方未说明"还是补一轮定向检索 |
| 4 | **`LocalLow` 的官方用途**：多处只有路径、无用途说明 | A | 不写用途，或标"官方未说明" |
| 5 | **`System32\WinSxS`"不可手动删除"的官方依据**：未找到 | A | 只描述其存在，不写"不可删"的断言 |
| 6 | **环境变量注册表路径、`USRCLASS.DAT`、`RegBack`、`HKCR\*\shell` 通配 verb**：零命中 | B | 实用路径速查表仅收录已命中项；未命中项不写 |
| 7 | **`HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion`**：未直接命中（只有 `...\Windows\CurrentVersion`） | B | 改用已命中的路径，或标注需复核 |

### 中低影响（可标注为"官方未说明"后照常写）

| # | 问题 | 涉及方向 |
|---|------|---------|
| 8 | `reg.exe` 各子命令是否需要管理员权限（官方全未明示） | B |
| 9 | `compact` / `cipher` / `mountvol` / `robocopy` 的管理员要求未说明 | A |
| 10 | `attrib` 关于"设 s/h 后须先清除才能改其他属性"仅单一来源、未实测 | A |
| 11 | EFS 与 NTFS 压缩的互斥只验证了单向（反向未验证） | A |
| 12 | 文件时间戳三项、ReFS 未覆盖 | A |
| 13 | `fsutil` 主页部分子命令描述抓取为空 | A |
| 14 | 无官方 PowerShell 与 cmd/Bash 对照页，"变量语法""路径分隔符"两行属**间接推论** | C |
| 15 | 8 张 cmdlet 页无 `Last updated` 字段（时效不可考） | C |
| 16 | PowerShell 7 当前稳定版本号未确认 | C |
| 17 | "新手该默认用 7 吗"无官方倾向来源 | C |
| 18 | Server Core `AuthorizationManager check failed`、UNC 路径限制——刻意剔除 | C |

### 已在素材中记录但**不应**进入笔记的内容

- 注册表方向的第三方"优化/清理/加速"工具（用户已确认本项目只讲结构与安全操作）。
- 无 A 级原理支撑的社区断言（如中文用户名问题）。

---

## 6. 下游交接摘要

**交接给 `outline-generator`（P3）的输入**：

1. **结构建议**：3 个主题章（各含概念 + 命令 + 易错点）+ 1 个串联章。素材已按子主题切好，可直接映射到章节小节。
2. **素材密度**：40 / 40 / 38 条论断，三方向均衡；每方向约 21 / 27 / 19 条来源可支撑"概念 → 命令 → 踩坑"三段式。
3. **写作约束（必须传递给 chapter-writer）**：
   - 所有命令标注执行环境（cmd / PowerShell / regedit）与适用版本（5.1 / 7）
   - 所有管理员权限要求：来源明确写出的照写，未说明的标"官方未说明"，**不得推断**
   - 注册表章必须含"先备份再修改"的操作步骤，且以导出/导入为主路径
   - C 级来源仅用于现象描述，原理必须回指 A 级
   - 降维改写点集中在三方向第 5 节，写作时需配类比
4. **大纲阶段需向用户确认的问题**：见第 5 节"高影响"表中第 1、3 项——**均已在 P2 检查点拍定**，见下节。

---

## 7. P2 检查点决策（2026-09-10 已确认，写作时直接遵守）

| 决策项 | 结论 |
|--------|------|
| 素材质量 | **认可**，直接进入阶段 3 大纲生成，不补检索 |
| 执行模式 | **大纲模式**（逐章写，逐章确认），不走随性模式 |
| `mklink /d` 提权要求 | **标"官方未说明"**，不自行断言。写法："创建符号链接可能需要提升权限，官方文档未明确说明" |
| 中文用户名 → `PSModulePath` 异常 | **不写进正文**（无任何可用来源，不符合"每条论断可追溯"标准） |
| 进阶路径 / 学习资源 | 本轮未收集；入门笔记默认不写该章节，除非用户另行要求 |

**对 P4 逐章写作的硬约束（承接第 6 节第 3 条）**：
- 所有命令标注执行环境（cmd / PowerShell / regedit）与适用版本（5.1 / 7）
- 管理员权限要求：来源明说则照写，未说明则标"官方未说明"，**不得推断**
- 注册表章必须含"先备份再修改"，且以导出 .reg / 导入还原为主路径；系统还原只作整机级兜底
- C 级来源仅用于现象描述，原理必须回指 A 级
- 不得引入任何"注册表优化 / 清理 / 加速"第三方工具内容
