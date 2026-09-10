# P2 深度素材 · 方向 B — Windows 注册表

## 1. 来源表

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

## 2. 论断 / 来源映射

（共 38 条。命令语法、示例与操作步骤集中在第 4 节，本节只保留"论断"。）

### 2.1 注册表是什么：结构与术语

- 注册表是一个分层数据库，数据以树格式组织；树中每个节点称为**键**，每个键可同时包含**子项**和称为**值**的数据条目；键可以有任意数量的值；键名不区分大小写、不能包含反斜杠 `\`，但值名称和数据**可以**包含反斜杠；键名不做本地化，值可以被本地化 → [S1]（小节"注册表的结构"）
- 注册表树最深可达 512 层；通过单次注册表 API 调用一次最多创建 32 层 → [S1]
- 应用程序必须先打开一个键才能向注册表添加数据；系统定义了一批**始终打开**的预定义键作为入口，添加数据的应用应始终在预定义键框架内工作，以便管理工具能找到并使用新数据；预定义项（根键）名称最大长度为 255 个字符 → [S4][S6]

### 2.2 预定义根键（零基础最常打交道的 5 个）

- `HKEY_LOCAL_MACHINE`（HKLM）保存计算机**物理状态**的数据：总线类型、系统内存、已安装软硬件，以及 Plug and Play 信息（`Enum` 分支记录了系统上出现过的全部硬件）；`HKEY_CURRENT_USER`（HKCU）保存**当前用户**偏好：环境变量设置、程序组、颜色、打印机、网络连接和应用偏好 → [S4]
- HKCU 映射到 `HKEY_USERS` 中当前用户的分支；该映射是**按进程**建立的，基于第一个引用它的线程的安全上下文；若该安全上下文在 HKU 下没有已加载的 hive，则映射到 `HKEY_USERS\.Default` → [S4]
- `HKEY_CLASSES_ROOT`（HKCR）**不是真实存储位置**，而是 `HKLM\Software\Classes`（本机所有用户的默认设置）与 `HKCU\Software\Classes`（仅交互式用户的覆盖设置）的合并视图；写 HKCR 会被系统重定向到二者之一，因此"要更改交互式用户的设置，必须在 `HKEY_CURRENT_USER\Software\Classes` 下而不是在 HKEY_CLASSES_ROOT 下进行更改；要更改默认设置，必须在 `HKEY_LOCAL_MACHINE\Software\Classes` 下进行更改" → [S6]
- `HKEY_CURRENT_CONFIG` 只是 `HKLM\System\CurrentControlSet\Hardware Profiles\Current` 的**别名**，描述当前硬件配置与标准配置之间的差异；`HKEY_PERFORMANCE_DATA` 的数据**并不真的存在注册表里**，而是注册表函数触发系统从数据源实时收集 → [S4]

### 2.3 Hive（配置单元）与磁盘文件

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

### 2.4 值类型：REG_* 到底是什么

- 注册表值可以存储多种格式的数据，这些类型定义在 `winnt.h` 头文件中：`REG_SZ`（以 null 结尾的字符串）、`REG_BINARY`（任何形式的二进制数据）、`REG_DWORD`（32 位数字）、`REG_QWORD`（64 位数字）、`REG_NONE`（没有定义的值类型）等；其中 `REG_DWORD_LITTLE_ENDIAN` 在 Windows 头文件中**就定义为 `REG_DWORD`**（Windows 设计为运行在小端架构上），`REG_DWORD_BIG_ENDIAN` 供某些 UNIX 大端系统使用 → [S5]
- `REG_EXPAND_SZ` 是"包含对环境变量的**未扩展引用**"的字符串，例如 `%PATH%`；要展开须调用 `ExpandEnvironmentStrings` → [S5]
- `REG_MULTI_SZ` 是以长度为 0 的字符串结尾的字符串序列（示例 `String1\0String2\0String3\0LastString\0\0`），需要**两个**终止 null 字符，且**不能包含零长度字符串**（空序列定义为 `\0`） → [S5]
- 字符串的终止符是读写注册表最常见的陷阱：写入时必须把终止 null 计入长度（应使用 `strlen(string) + 1`，而非 `strlen`）；读取时字符串**可能未正确终止**，必须自行确保终止，否则可能覆盖缓冲区 → [S5]
- 在注册表编辑器里，DWORD 值可以按二进制、十六进制或十进制格式显示；`REG_QWORD` 在注册表编辑器中以**二进制值形式**显示（Windows 2000 引入） → [S6]

### 2.5 尺寸限制：为什么会遇到"值写不进去"

- 值名称最大长度 16,383 个字符（Windows Server 2003 / XP / Vista）；**超过 2,048 字节的长值必须存储为文件**，只在注册表中存文件名——"这有助于注册表高效执行"；此外**一个项的所有值的总大小有 64K 限制** → [S6]

### 2.6 32 位 / 64 位注册表视图（WOW6432Node）

- 默认情况下，WOW64 上的 32 位应用程序访问 32 位注册表视图，64 位应用程序访问 64 位注册表视图；`KEY_WOW64_64KEY`（0x0100）让任一应用访问 64 位键，`KEY_WOW64_32KEY`（0x0200）让任一应用访问 32 位键；这两个标志**对共享注册表键无效**，且**同时指定会失败**并返回 `ERROR_INVALID_PARAMETER` → [S20]
- `Wow6432Node` 与 `WowAA32Node` 键是**保留的**，"为了兼容性，应用程序不应直接使用这些键"；官方最佳实践是：应用一旦用某个标志访问了备用视图，之后对**子键**的所有创建/删除/打开操作都必须显式使用**同一个标志**，而要准确枚举两个视图中的所有键必须**分两遍**枚举（一遍用其中一个标志打开的句柄，另一遍用另一个标志） → [S20]
- 读者实际会遇到的只是两个开关：`reg query` / `reg add` / `reg import` 等命令提供 `/reg:32` 与 `/reg:64` 指定注册表视图；而 64 位 Windows 自带的 64 位注册表编辑器会在 `HKEY_LOCAL_MACHINE\Software\WOW6432Node` 节点下显示 32 位项 → [S9][S10][S14][S6]

### 2.7 权限与所有者

- Windows 安全模型允许控制对注册表项的访问；调用 `RegCreateKeyEx` 或 `RegSetKeySecurity` 时可为键指定**安全描述符**，若指定 `NULL` 则键获得默认安全描述符，而**键的默认安全描述符中的 ACL 继承自其直接父键** → [S7]
- 注册表项的有效访问权限包括 `DELETE`、`READ_CONTROL`、`WRITE_DAC`、`WRITE_OWNER` 这些标准访问权限，但**不支持 `SYNCHRONIZE`**；键特定权限中 `KEY_QUERY_VALUE` 查询值必需、`KEY_SET_VALUE` 创建/删除/设置值必需、`KEY_CREATE_SUB_KEY` 创建子项必需、`KEY_ENUMERATE_SUB_KEYS` 枚举子项必需、`KEY_NOTIFY` 请求更改通知必需，`KEY_CREATE_LINK`（0x0020）**保留供系统使用** → [S7]
- 打开键时系统会按安全描述符检查请求的访问权限，权限不足则打开失败；**如果管理员需要访问某个键，官方给出的解决方案是启用 `SE_TAKE_OWNERSHIP_NAME` 特权，并以 `WRITE_OWNER` 访问权限打开该键** → [S7]
- 核对权限的两个入口：注册表编辑器中定位到键 → "编辑"菜单 → "权限"；PowerShell 中 `Get-Acl` 读取、`Set-Acl` 写入（官方示例用 `RegistryAccessRule` 为指定用户加 `FullControl`） → [S7][S21]

### 2.8 备份与回滚（强制内容）

- 官方在 `reg` 命令页用 Caution 级警告确立基调：「除非没有替代项，否则不要直接编辑注册表。注册表编辑器绕过标准安全措施，允许降低性能、损坏系统甚至要求重新安装 Windows 的设置。……如果必须直接编辑注册表，请先备份它。」 → [S8]
- 官方推荐的修改顺序是「使用 Windows 用户界面更改系统设置，而不是手动编辑注册表」，并补充"编辑注册表有时可能是解决产品问题的最佳方法"，若 Microsoft 知识库提供了针对该问题的分步说明文章，则「建议完全按照这些说明操作」；同页警告错误修改"可能需要重新安装操作系统才能解决。Microsoft 不能保证可以解决这些问题" → [S6]
- 官方把"备份"写进了命令本身：`reg save` 的备注是「在编辑任何注册表项之前，必须使用 **reg save** 命令保存父子项。如果编辑失败，则可以使用 **reg restore** 作还原原始子项」，`reg restore` 的定义即"将保存的子项和条目写回注册表" → [S15][S16]
- 三条 .reg / .hiv 路径的边界不同：`reg export` 导出时必须用 **.reg** 扩展名且**仅适用于本地计算机**；`reg import` 的文件**必须由 reg export 提前创建**，同样仅本地；`reg restore` 的文件必须由 `reg save` 创建、**必须是 .hiv 扩展名**，且会**覆盖**目标键的现有内容 → [S13][S14][S16]
- regedit 界面路径是官方给出步骤最完整的备份方式：「开始」→ 搜索 `regedit.exe` → 回车（**若有管理员密码或确认提示，需提供**）→ 定位并单击要备份的项或子项 → 「文件」>「导出」→ 选位置、填文件名 → 「保存」；还原为「文件」>「导入」→ 选备份文件 → 「打开」 → [S18]
- 备份**整个**注册表要用备份工具备份**系统状态**（"系统状态包括注册表、COM+ 类注册数据库和启动文件"），还原整机走"从备份还原系统状态"；备份系统状态还会在 `%SystemRoot%\Repair` 文件夹中创建注册表文件的更新副本 → [S6]
- 系统还原是另一条回滚路径：`Enable-ComputerRestore -Drive "C:\"` 在指定文件系统驱动器上启用系统还原功能，之后可用 `Restore-Computer` 之类的工具还原到以前的状态；官方明确要求在 Windows Vista 及更高版本上**必须用"以管理员身份运行"打开 Windows PowerShell** 才能运行该 cmdlet，且**要在任何驱动器上启用都必须先在系统驱动器上同时启用**，不能用于外部驱动器或远程网络驱动器；可用 `Rstrui.exe` 查看每个驱动器的还原状态 → [S26]
- `reg load` / `reg unload` 覆盖"临时挂载做排查"这一场景：`reg load` 把保存的子项和条目写入注册表中的**其他**子项，"此命令适用于用于故障排除或编辑注册表项的临时文件"，而 `reg unload` 的定义就是"删除使用 reg load 作加载的注册表部分" → [S17][S8]

### 2.9 常用实用路径

- 开机自启共有**四个** `Run` / `RunOnce` 键（HKLM 与 HKCU 各两个，均在 `Software\Microsoft\Windows\CurrentVersion\` 下）；`Run` 键使程序在**每次**用户登录时运行，`RunOnce` 键使程序运行**一次，然后删除该键**；键的数据值是**不超过 260 个字符**的命令行，形式为 `说明-字符串 = 命令行`，且"如果在任何特定密钥下注册了多个程序，则这些程序运行的顺序**不确定**" → [S19]
- `HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce` **仅在重新启动后管理员组的成员登录时才执行**；`RunOnce` 默认在命令行运行**之前**删除值，值名前加感叹号 `!` 可把删除**延迟到命令运行之后**（"如果没有感叹号前缀，当 RunOnce 操作失败时，下次启动计算机时不会要求关联程序运行"）；"默认情况下，当计算机以安全模式启动时，将忽略这些键"，值名前加星号 `*` 可**强制程序在安全模式下仍然运行** → [S19]
- 文件关联侧的三个可追溯结论：右键菜单每条命令由一个 **verb（谓词）**标识，verb 对应的命令字符串形如 `"My Program.exe" "%1"`，**任何可能包含空格的元素都必须加引号**；ProgID 的标准键名格式为 `[厂商或应用].[组件].[版本]`（如 `Word.Document.6`），位于 `HKEY_CLASSES_ROOT` 下；因为 HKCR 是 HKCU 与 HKLM 的组合，**可以把自定义 verb 注册在 `HKEY_CURRENT_USER\Software\Classes` 下，其主要好处是"不需要提升权限"** → [S23][S24][S25]

### 2.10 三种执行方式：regedit / reg.exe / PowerShell

- 官方列举的可修改注册表手段包括注册表编辑器（Regedit.exe 或 Regedt32.exe）、组策略、系统策略、注册表（.reg）文件、Windows Script Host 脚本、WMI（含 Wmic.exe）以及控制台注册表工具 Reg.exe；其中 `reg` 的 keyname 必须包含有效根键，本地有效根键为 `HKLM`、`HKCU`、`HKCR`、`HKU`、`HKCC`，而指定远程计算机时**只有 `HKLM` 和 `HKU` 有效** → [S6][S9]
- PowerShell 侧注册表提供程序的驱动器为 `HKLM:`（映射 HKEY_LOCAL_MACHINE 配置单元）与 `HKCU:`（映射 HKEY_CURRENT_USER 配置单元），也可用提供程序全名语法 `Registry::HKEY_LOCAL_MACHINE\Software`；四个 cmdlet 分工明确：`Get-ChildItem` 看**子项**（不显示父键属性）、`Get-Item` 看**键本身及其属性**、`Get-ItemProperty` 看**值**、`Get-ItemPropertyValue`（PowerShell 5.0 起）只返回指定属性的值 → [S21][S22]
- 修改与删除的官方行为差异：`Set-ItemProperty` 的动态参数 `-Type` 决定数据类型，**默认为 `String`（REG_SZ）**，可选 `ExpandString`、`Binary`、`DWord`、`MultiString`、`QWord`、`Unknown`（表示不受支持的类型如 `REG_RESOURCE_LIST`）；`Remove-Item` 在项**包含子项时默认弹出确认**，加 `-Recurse` 才免提示；`Remove-ItemProperty` 只删值，`Clear-Item` 清空键的**所有值**而保留键本身 → [S21]

## 3. 矛盾与冲突

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

## 4. 可操作指引

**管理员权限一栏只写官方页明确写出的内容**；官方未明示的一律标注为"官方未说明"（详见第 6 节第 8 条）。

### 4.1 主路径：导出备份 → 导入还原（覆盖 Windows 11/10/8.1）

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

### 4.2 进阶路径：整键快照 → 写回（.hiv）

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

### 4.3 整机回滚路径

- **系统状态备份**：用备份工具备份系统状态（含注册表、COM+ 类注册数据库、启动文件）；还原时从备份还原系统状态；备份系统状态还会在 `%SystemRoot%\Repair` 生成注册表文件的更新副本 → [S6]
- **系统还原点**（附注路径，需说明版本存疑）
  ```powershell
  # 在 C: 上启用系统还原功能
  Enable-ComputerRestore -Drive "C:\"
  ```
  - **权限：官方明确要求**「使用'以管理员身份运行'选项打开 Windows PowerShell」 → [S26]
  - 官方提示：要在任何驱动器上启用，必须**先在系统驱动器上同时启用**；不能用它给外部驱动器或远程网络驱动器启用；可用 `Rstrui.exe` 查看每个驱动器的还原状态 → [S26]

### 4.4 编辑前的官方风险 checklist（可直接做成 Callout）

- 「除非没有替代项，否则不要直接编辑注册表。注册表编辑器绕过标准安全措施，允许降低性能、损坏系统甚至要求重新安装 Windows 的设置。可以使用控制面板中的程序或 Microsoft 管理控制台（MMC）安全地更改大多数注册表设置。**如果必须直接编辑注册表，请先备份它。**」 → [S8]
- 「如果使用注册表编辑器或使用其他方法错误地修改了注册表，则可能会发生严重问题。这些问题可能需要重新安装操作系统才能解决。Microsoft 不能保证可以解决这些问题。」 → [S6]
- 「建议使用 Windows 用户界面更改系统设置，而不是手动编辑注册表。」若 KB 已给出针对该问题的分步说明，「建议完全按照这些说明操作」 → [S6]
- 遇到权限不足的键：启用 `SE_TAKE_OWNERSHIP_NAME` 特权并以 `WRITE_OWNER` 打开（官方给出的"管理员需要访问密钥"的唯一解决方案） → [S7]
- 查看/核对某个键的现有权限：注册表编辑器 → 定位到键 → 「编辑」>「权限」 → [S7]

### 4.5 查询与验证（改完先看，别急着改）

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

### 4.6 修改与删除命令（附风险提示）

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

### 4.7 常被问到的实用路径速查

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

## 5. 需要降维改写的内容

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

## 6. 未解决问题与缺口

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

## 7. 下游交接摘要

- 注册表 = 一棵树：节点叫键，键下可挂子项和值；顶层只有 5 个常用根键（HKLM 机器级、HKCU 用户级、HKCR 是合并视图不是真实位置、HKU 所有用户、HKCC 硬件配置别名）。
- 值有类型之分：最常用 REG_SZ（字符串）、REG_DWORD（32 位数字）、REG_BINARY（二进制）、REG_MULTI_SZ（多行列表）、REG_EXPAND_SZ（含 %变量% 的字符串）；regedit 显示名、reg.exe 的 `/t`、PowerShell 的 `-Type` 是同一套类型的三副面孔。
- 注册表在磁盘上是真实文件（hive）：机器级在 `%SystemRoot%\System32\Config`，用户级对应用户配置文件里的 NTUSER.DAT，`.log`/`.sav`/`.alt` 是系统自用副本，**不要删**。
- 三种执行方式各有定位：regedit 适合"看得见再改"，`reg.exe` 适合可复制的命令与批处理，PowerShell 用 `HKLM:` / `HKCU:` 驱动器适合脚本化；官方统一建议优先用图形界面或组策略，改注册表是最后手段。
- 动手前必须备份、出事必须能回滚：主路径是 regedit「文件 > 导出 / 导入」（官方步骤覆盖 Win11），进阶是 `reg save` → `reg restore`（.hiv，官方明写"编辑前必须 reg save"），整机兜底是备份系统状态；系统还原点可作附注但官方版本声明存疑。
- 两个最容易踩的坑要显式警告：一是 64 位系统上有两套注册表视图（WOW6432Node 是保留键，不应直接改），二是 RunOnce 的删值时机、`!` / `*` 前缀语义与"仅管理员组成员登录才执行"的行为差异。
