# P2 深度素材 · 方向 A — Windows 文件系统

## 1. 来源表

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

## 2. 论断 / 来源映射

### 子主题一：文件系统的基本结构（卷 / 目录 / 文件）

1. Windows 支持的所有文件系统共用三个存储组件：**卷**是"目录和文件的集合"，**目录**是"目录和文件的分层集合"，**文件**是"相关数据的逻辑分组"；组织层级最高一级是卷，文件系统"驻留在卷上"。且**目录在文件系统层面就是一种"具有特殊属性的文件"**，因此"必须像常规文件一样遵循所有命名规则"——文件名的规则同样约束目录名。锚点：A1「本地文件系统」→"Windows 支持的所有文件系统具有以下存储组件"；A2「文件和目录名称」→ [A1][A2]
2. NTFS 是新版 Windows 的默认文件系统，提供"安全描述符、加密、磁盘配额和支持丰富的元数据"。锚点：A14「NTFS 概述」首段 → [A14]

### 子主题二：命名规则、路径与命名空间

3. 9 个保留字符不能用于文件名：`< > : " / \ | ? *`，外加整数值 0（NUL 字符）；反斜杠是"将名称分隔成组件的保留字符"。锚点：A2「命名约定」→"以下保留字符" → [A2]
4. 一批**保留设备名**不能用作文件名：`CON、PRN、AUX、NUL、COM1–COM9、LPT1–LPT9`，"另请避免这些名称紧跟扩展名"（`NUL.txt` 等效于 `NUL`）；但字符码 **1–31 "在备用数据流中允许使用"**——流名称的规则与文件名称不同。锚点：A2「命名约定」→ [A2]
5. 文件或目录名**不要以空格或句点结尾**（"Windows Shell 和用户界面不支持"）；大小写不敏感，"将名称 OSCAR、Oscar 和 oscar 视为相同"，驱动器号同理（`D:\` 与 `d:\` 同一个卷）。锚点：A2「命名约定」→ [A2]
6. 路径前缀决定解释方式："如果文件名不以下列项之一开头，则其与当前目录相对应"（UNC、`C:\`、`\` 三者例外）；**`C:tmp.txt` 指"驱动器 C 上当前目录中"的文件，与 `C:\tmp.txt` 不同**；`.`/`..` 分别表示当前目录与父目录。锚点：A2「完全限定与相对路径」→ [A2]
7. 三种前缀的用途：`\\?\` "告知 Windows API 禁用所有字符串分析，并将其后面的字符串直接发送到文件系统"；`\\.\` 进入 Win32 设备命名空间，是"直接访问物理磁盘和卷的方式，而无需通过文件系统"；NT 命名空间是"最低级别命名空间"，其中 Win32 的 `C:` 只是"指向 HarddiskVolume1 的符号链接"。锚点：A2「Win32 文件命名空间 / Win32 设备命名空间 / NT 命名空间」→ [A2]
8. 长文件名之外 Windows 还会生成 8.3 短名（形如 `T97B4~1.TXT`），但"**不要假设磁盘上已存在 8.3 别名**"（可被禁用）；在 NTFS/exFAT/UDFS/FAT32 上长名以 Unicode 存储，所以"原始长文件名始终被保留"。锚点：A2「短与长名称」→ [A2]

### 子主题三：最大路径长度限制

9. 传统上限是 **MAX_PATH = 260 个字符**，构成是"驱动器号、冒号、反斜杠、用反斜杠分隔的名称组件和终止 null 字符"；Unicode 版 API 支持**扩展长度路径，最大约 32,767 个字符**，条件是 `\\?\` 前缀（UNC 路径用 `\\?\UNC\`），且该 32767 是近似值。锚点：A3「最大路径长度限制」→ [A3]
10. `\\?\` 前缀下行为特殊：**不能用正斜杠作分隔符，不能用 `.` 表示当前目录，也不能用 `..` 表示父目录**；"相对路径总字符数始终不能超过 MAX_PATH"；用 API 创建目录时"目录名不能超过 MAX_PATH 减 12"（要留 8.3 名空间）。锚点：A3「最大路径长度限制」→ [A3]
11. Windows 10 1607 起许多 Win32 文件/目录函数移除 MAX_PATH 限制，但**应用必须显式选择支持**，需同时满足两个条件：注册表 `HKLM\SYSTEM\CurrentControlSet\Control\FileSystem` 下 `LongPathsEnabled`(REG_DWORD)=`1`，且应用清单含 `longPathAware`。此值"按进程缓存"，"可能需要重新启动"。锚点：A3「在 Windows 10 版本 1607 及更高版本中启用长路径」→ [A3]
12. Shell 与文件系统要求不同："**可以使用 Shell 用户界面无法正确解释的 Windows API 来创建路径**"——资源管理器打不开的路径可能存在。锚点：A3「最大路径长度限制」→ [A3]

### 子主题四：系统目录结构（C:\Windows、Program Files、Users、ProgramData、AppData）

> 本子主题来源 A6/A7 是开发者/部署视角的官方参考页，路径事实为 A 级，但表述需降维（见第 5 节）。

13. 用户配置文件目录 `%USERPROFILE%` = `%SystemDrive%\Users\%USERNAME%`（`FOLDERID_Profile`）；其下的 **`AppData` 分三个子目录**：`Roaming`（`%APPDATA%` = `%USERPROFILE%\AppData\Roaming`）是"用作应用程序特定数据的通用存储库"；`Local`（`%LOCALAPPDATA%`）是"充当本地非漫游应用程序的数据存储库"；`LocalLow` = `%USERPROFILE%\AppData\LocalLow`，**没有 CSIDL 等效项**。三者文件夹类型均为 PERUSER（每个用户各一份）。锚点：A6 三条 KNOWNFOLDERID + A7「CSIDL_APPDATA / CSIDL_LOCAL_APPDATA」→ [A6][A7]
14. **全机器共用的两个目录**：`ProgramData`（`%ALLUSERSPROFILE%` = `C:\ProgramData`）是"包含所有用户的应用程序数据的文件系统目录"，XP 时代旧路径为 `%ALLUSERSPROFILE%\Application Data`；`Public`（`%PUBLIC%` = `C:\Users\Public`）是"Windows Vista 新增功能"，"无 CSIDL 等效项"，其下按类型分为 `Public\Documents`、`Desktop`、`Music`、`Pictures`、`Videos`、`Favorites`。二者文件夹类型为 FIXED。锚点：A6「FOLDERID_ProgramData / FOLDERID_Public」+ A7「CSIDL_COMMON_APPDATA」→ [A6][A7]
15. `C:\Windows`（`%windir%`，`FOLDERID_Windows`）与 `System32`（`%windir%\system32`）的路径映射；**64 位系统上 `FOLDERID_SystemX86` 解析为 `%windir%\syswow64`**。锚点：A6「FOLDERID_Windows / FOLDERID_System」+ A7「WINDIR / CSIDL_SYSTEM」→ [A6][A7]
16. `Program Files`（`FOLDERID_ProgramFiles`）= `%ProgramFiles%` = `%SystemDrive%\Program Files`。**`Program Files (x86)` 只存在于 64 位系统**：32 位系统上 `FOLDERID_ProgramFiles` 与 `FOLDERID_ProgramFilesX86` **都**指向 `Program Files`；64 位系统上后者才指向 `Program Files (x86)`；64 位 OS 上运行 32 位应用时 `FOLDERID_ProgramFiles` 也被解析为 `Program Files (x86)`，而 `FOLDERID_ProgramFilesX64`"在任一情况下使用都会导致错误"。锚点：A6「FOLDERID_ProgramFiles / FOLDERID_ProgramFilesX86 / FOLDERID_ProgramFilesX64」及备注表 → [A6]
17. 用户级环境变量速查（Vista 及以后）：`%ALLUSERSPROFILE%`→`C:\ProgramData`、`%APPDATA%`→`…\AppData\Roaming`、`%LOCALAPPDATA%`→`…\AppData\Local`、`%PUBLIC%`→`C:\Users\Public`、`%SystemDrive%`→`C:`、`%windir%`→`C:\Windows`；但路径可能因"文件夹重定向"而变化，"可能与特定计算机上的路径不匹配"。锚点：A6 末段"环境字符串 / 示例路径"表及前导句 → [A6]

### 子主题五：NTFS 高级特性（ADS、压缩、EFS、稀疏文件、可靠性）

18. **备用数据流（ADS）**：NTFS 中"流包含写入文件的数据，并提供有关文件的详细信息，而不是属性"（例如搜索关键字、创建者身份）；**每个流有自己的分配大小、实际大小、VDL，并"维护自己的压缩、加密和稀疏状态"**；流**没有自己的文件时间**（"更新文件中的任何流时，文件的文件时间将更新"）；只要任一流曾是稀疏的，文件上就会设置 `FILE_ATTRIBUTE_SPARSE_FILE`。锚点：A8「文件流（本地文件系统）」→ [A8]
19. 流的命令行全名格式是"`文件名:流名称:流类型`"（如 `myfile.dat:stream1:$DATA`）；默认数据流未命名，`文件名::$DATA` 等价于 `文件名`；流名称只能用文件名合法的字符（含空格），"**用户无法创建新的流类型**"，流类型"始终以美元符号（$）符号开头"；单字符文件名须写成全限定路径或加 `.\`，因为"Windows 将单个字符文件名视为驱动器号"。锚点：A8「流的命名约定」→ [A8]
20. **目录本身也是一种流**：`DirName`、`DirName::$INDEX_ALLOCATION`、`DirName:$I30:$INDEX_ALLOCATION` 三者等价；EFS 使用 `:$EFS:$LOGGED_UTILITY_STREAM`，TxF 使用 `:$TXF_DATA:$LOGGED_UTILITY_STREAM`。锚点：A8「流类型」表 → [A8]
21. **NTFS 压缩**：`compact` 是"NTFS 文件系统压缩功能的命令行版本"；目录的压缩状态表示"将文件添加到目录时是否自动压缩"，而"**设置目录的压缩状态不一定更改目录中已存在文件的压缩状态**"；`/EXE` 支持 `XPRESS4K`（最快且默认）、`XPRESS8K`、`XPRESS16K`、`LZX`（最紧凑）；**不能压缩 FAT 或 FAT32 分区**。锚点：A13「备注」与参数表 → [A13]
22. **EFS 与 NTFS 压缩互斥（官方明确单向）**：EFS"使用公钥系统为 NTFS 文件系统卷上的单个文件提供加密保护"，而"**无法加密以下项：压缩文件**、系统文件、系统目录、根目录、交易"；但"**可以加密稀疏文件**"——这是它与压缩文件的关键差别。锚点：A21「使用 EFS」→ [A21]
23. **`cipher` 的经典坑（官方原文）**："如果未加密父目录，则修改文件时，加密文件可能会解密。因此，**加密文件时，还应加密父目录**。"；输出用 `E` 标记已加密、`U` 标记未加密；`cipher /w:<directory>` 用于"从整个卷上可用未使用的磁盘空间中删除数据"。锚点：A16「备注」与「示例」→ [A16]
24. **稀疏文件**：程序"将这些未分配的区域视为包含值为零的字节，但没有使用磁盘空间来表示这些零"；应用必须**显式声明**文件为稀疏（`FSCTL_SET_SPARSE`），并"由应用程序负责"用 `FSCTL_SET_ZERO_DATA` 维持稀疏性；"**只有压缩文件或稀疏文件才能具有操作系统已知的清零范围**"，此时 NTFS"可能会取消分配文件中的磁盘空间……将字节范围设置为零，而不会扩展文件大小"；高度碎片化的大稀疏文件可能"超过 NTFS 对磁盘扩展区的限制"。锚点：A17 + A20「备注」+ A18「fsutil sparse」行 → [A17][A18][A20]
25. **可靠性**：NTFS 通过"基于事务的日志文件和检查点信息"提高可靠性，故障后"通过重播事务日志来恢复更改"；**自我修复 NTFS** 可"联机更正 NTFS 文件系统的损坏，而无需运行 `chkdsk.exe`"；卷与文件上限由**群集大小**决定（4 KB 默认→16 TB，64 KB→256 TB，2048 KB 最大→8 PB），装载群集过大的卷报 `STATUS_UNRECOGNIZED_VOLUME`；但"使用依赖于卷影复制服务（VSS）快照……的'以前版本'功能或备份应用程序时，最大支持的卷大小为 64 TB"。锚点：A14「提高可靠性 / 支持大型卷」+ A18「fsutil repair」行 → [A14][A18]

### 子主题六：链接（硬链接 / 符号链接 / 交接点）

26. "NTFS 文件系统支持三种类型的文件链接：硬链接、交接点和符号链接。"**硬链接**是"文件的文件系统表示形式，其中多个路径引用同一卷中的单个文件"，它**不能引用目录，也不能引用不同卷上的文件**。锚点：A19「硬链接」→ [A19]
27. **交接点**"引用的存储对象是单独的目录"，"还可以链接位于同一计算机上的不同本地卷上的目录"，通过**重分析点**实现；硬链接有个反直觉细节："目录条目大小和文件_属性信息仅在进行更改的链接处明显_更新"——在一个链接上清除只读标志，其他链接仍显示只读。锚点：A19「交接点」与「硬链接」→ [A19]
28. `mklink` 四种形态：默认创建**文件符号链接**，`/d` 目录符号链接，`/h` 硬链接，`/j` 目录交接点；删除用普通命令（`rd` 删目录符号链接、`del` 删硬链接）。`fsutil hardlink` 进一步说明每个文件"可视为至少有一个硬链接"，"**只有在删除了指向某一文件的所有链接之后，才会从文件系统中删除该文件**"。锚点：A5 参数表与 Examples + A18「fsutil hardlink」行 → [A5][A18]

### 子主题七：文件属性与列举命令（attrib / dir）

29. `attrib` 可设置的属性：`r` 只读、`a` 存档、`s` 系统、`h` 隐藏、`o` 脱机、`i` 非内容索引、`x` 清理、`p` 固定、`u` 未固定、`b` SMR Blob；**操作顺序坑（官方原文）**：文件若设了系统属性或隐藏属性，"必须清除该属性，然后才能更改文件的任何其他属性"；`/s` 递归子目录、`/d` 作用于目录、`/l` 作用于符号链接本身而非目标。锚点：A9 参数表 → [A9]
30. `dir` **默认不显示隐藏文件和系统文件**，加 `/a` 但不指定属性时才"显示所有文件的名称，包括隐藏文件和系统文件"；`dir /r` 可以"显示文件的备用数据流"（零基础读者最容易上手的 ADS 观察入口）；`dir /x` 显示 8.3 短名。**星号通配符的坑**：星号"始终使用短文件名映射"，所以 `dir t97\*` 会同时返回 `t97.txt` 和 `t.txt2`（后者短名为 `T97B4~1.TXT`），`del t97\*` 会删掉两个文件。锚点：A12 参数表与「Remarks」→ [A12]

### 子主题八：卷、分区、盘符与装入点

31. **卷装入点**允许"链接卷，而无需驱动器号"，且必须建立在"现有 NTFS 目录"上；卷名用 `\\?\volume\{GUID}\` 语法（**需要花括号**）；用多个装入路径的好处是"可以使用单个驱动器号（如 `C:`）访问所有本地卷"，"无需记住哪个卷对应于哪个驱动器号"；`mountvol /p` 会"卸载基本卷，使基本卷脱机，使其不可装载"，且"**如果其他进程正在使用该卷，则 mountvol 会在卸载卷之前关闭所有打开的句柄**"；`/n`/`/e` 控制新基本卷的自动装载，`/s` 用于装载 EFI 系统分区。锚点：A11 首段、参数表与「备注」→ [A11]
32. **diskpart 必须提权**："您必须在本地**管理员**组或具有类似权限的组中才能运行 diskpart。"其核心心智模型是**焦点（focus）**："必须先列出一个对象，然后选择一个对象以使其处于焦点状态。对象具有焦点后，键入的任何 diskpart 命令都将对该对象执行操作"，且焦点会**自动转移**（"创建新分区时，焦点会自动切换到新分区"）。典型四步：`list disk` → `select disk 1` → `create partition primary` → `format fs=ntfs label=Backup quick`。锚点：A15 首段、「Determine focus」与「Examples」→ [A15]
33. NTFS 还提供其他扩容手段：可在"本地 NTFS 卷上的任何空文件夹中装载卷"，并可用磁盘配额"跟踪和控制各个用户的 NTFS 卷上的磁盘空间使用情况"；8.3 短名在 Server 2008 R2 及更高版本格式化卷时"默认禁用"，但"为了实现应用程序兼容性，系统卷上仍启用短名称"。锚点：A14「灵活分配容量 / 最大文件名称和路径」→ [A14]

### 子主题九：权限（icacls）

34. `icacls` 的作用是"显示或修改指定文件中的任意访问控制列表（DACL）"，并取代已弃用的 `cacls`；**ACE 的规范顺序固定**：显式拒绝 → 显式授予 → 继承的拒绝 → 继承的授予；简单权限不用括号：`N` 无法访问、`F` 完全访问、`M` 修改、`RX` 读取和执行、`R` 只读、`W` 只写、`D` 删除。锚点：A4 首段、Note 与「Remarks」→ [A4]
35. 高级权限与继承标志**必须写在括号里**：`(DE)` 删除、`(WDAC)` 更改权限、`(WO)` 获取所有权、`(RD)` 读取数据/列出目录、`(X)` 执行/遍历；继承标志 `(I)` 继承、`(OI)` 对象继承（仅目录）、`(CI)` 容器继承（仅目录）、`(IO)` 仅继承（"继承自父容器，但不适用于对象本身"）、`(NP)` 不传播继承；`/grant:r` 是"权限替换以前授予的显式权限"，不带 `:r` 则是"添加到任何先前授予的显式权限中"。锚点：A4「Remarks」与参数表 → [A4]
36. 修坏权限的兜底与新式用法：`/reset` 会把 ACL"替换为所有匹配文件的默认继承 ACL"；禁用继承用 `/inheritancelevel:e|d|r`；SID 用数字形式时"将通配符 `*` 附加到 SID 的开头"（`/grant *S-1-1-0:(d,wdac)`）；批量备份/还原用 `icacls c:\windows\* /save aclfile /t` 与 `icacls c:\windows\ /restore aclfile`。锚点：A4 参数表与「Examples」→ [A4]

### 子主题十：复制与备份（robocopy）

37. `robocopy <source> <destination> [<file>] [<options>]`，不指定文件时默认 `*.*`；`/s` 复制子目录但"自动排除空目录"，`/e`"自动包括空目录"；**`/mir` 相当于 `/e` 加 `/purge`**，即镜像目录树并**删除目标端源中已不存在的文件和目录**（破坏性最强）。锚点：A10「Syntax」与「Copy options」→ [A10]
38. **重试默认值极其激进**：`/r` 默认 **1,000,000** 次、`/w` 默认 **30** 秒，网络路径失效时会长时间假死，官方示例普遍写 `/R:2 /W:5`。锚点：A10「Retry options」与「Examples」→ [A10]
39. **退出代码语义反直觉**：`0` 表示"未复制任何文件"（无失败），`1` 表示"已成功复制所有文件"，"任何等于或大于 **8** 的值都表示在复制作期间至少发生一次故障"；`/copy` 默认值是 `DAT`（数据、属性、时间戳），`/sec` 相当于 `/copy:DATS`，`/copyall` 相当于 `/copy:DATSOU`；官方"强烈建议"每次运行都加 `/log:`。锚点：A10「退出（返回）代码」「Copy options」「Examples」→ [A10]
40. robocopy **默认会包含交接点**，需主动用 `/xj`（全部）、`/xjd`（目录）、`/xjf`（文件）排除；**从设备的根目录复制任何数据时，目标目录在复制过程中会采用"隐藏"和"系统"属性**（官方 Important）；`/sparse:<y|n>` 控制是否保留稀疏状态，不选时默认为 **yes**；`/mt:<n>` 多线程复制 `n` 必须为 1–128（默认 8），且"不能与 `/ipg` 和 `/efsraw` 参数一起使用"。锚点：A10「Syntax」Important 与参数表 → [A10]

---

## 3. 矛盾与冲突

1. **`FOLDERID_ProgramFilesX86` 的默认路径在同一页内前后不一致（A6 页面自身冲突）**：
   - 独立条目栏写：`Default Path | %ProgramFiles% (%SystemDrive%\Program Files)`（与 `FOLDERID_ProgramFiles` 完全相同）；
   - 但页面「备注」的位数对照表写：64 位操作系统 → `%SystemDrive%\Program Files (x86)`。
   - 两者不能同时为真。合理解释是独立条目栏给的是"未做重定向时"的原始值、备注表给的是"按 OS/应用位数解析后"的值，但**页面没有明说**。成章时应采用备注表的结论，并把这一分歧如实标注为待确认。
2. **32 位系统上两个 Program Files 常量指向同一路径**（A6）：32 位 OS 下 `FOLDERID_ProgramFiles` 与 `FOLDERID_ProgramFilesX86` 都是 `%SystemDrive%\Program Files`，而 `FOLDERID_ProgramFilesX64`"32 位操作系统不支持"。这意味着"Program Files (x86) 一定存在"是错误直觉，需要在正文里消歧。
3. **`AppData\LocalLow` 的来源深度不足**：A6 只给路径与"无 CSIDL 等效项"，A7 干脆没有 LocalLow 条目。两个来源都无法回答"它到底给谁用"（通常说法是低完整性级别进程，但本轮**没有官方来源支撑**）。不应把该说法写进第 2 节。
4. **来源覆盖粒度不均**：`fsutil` 主页面（A18）多个子命令行的描述列在抓取结果中为空，只能依赖 A20 等子页面补齐，存在信息缺口。

---

## 4. 可操作指引

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

## 5. 需要降维改写的内容

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

## 6. 未解决问题与缺口

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

## 7. 下游交接摘要

- **骨架**：卷/目录/文件三层模型（A1）→ 命名与路径规则 + `\\?\`/`\\.\` 前缀与 MAX_PATH 260 限制（A2/A3）→ 系统目录地图（Windows / Program Files(x86) / Users / Public / ProgramData / AppData 三兄弟）（A6/A7）。
- **进阶层**：NTFS 四大特性——ADS（`dir /r` 观察）、压缩（`compact`）、加密 EFS（`cipher`，与压缩单向互斥、须加密父目录）、稀疏文件（`fsutil sparse`）；链接三兄弟（硬链接 / 符号链接 / 交接点，`mklink`）。
- **命令层**：`dir` + `attrib` 看属性 → `icacls` 看/改/重置权限 → `robocopy` 复制备份（重点讲 `/r` 默认百万次重试与退出码 ≥8 才是失败）→ `mountvol` / `diskpart` 管理卷与装入点。
- **坑清单（可直接成小节）**：`NUL.txt` 等保留设备名、`C:tmp.txt` ≠ `C:\tmp.txt`、`dir t97\*` 因短名映射误匹配、`attrib` 系统/隐藏属性的操作顺序、robocopy 默认重试与交接点默认被跟随、`cipher` 未加密父目录导致自动解密。
- **待补后再写**：`mklink` 提权要求、`LocalLow` 官方用途、`System32/WinSxS` 的"不要手删"依据——这三点在补来源前不要写成结论。
