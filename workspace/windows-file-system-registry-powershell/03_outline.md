# 学习笔记大纲：《Windows 文件系统、注册表与 PowerShell》

> 笔记类型：概念笔记 + 实战笔记（兼重）——每章都含「讲清原理结构」与「可复制命令清单」两部分
> 读者定位：零基础中文读者；术语首次出现必须先解释再使用
> 预计总篇幅：25000–31500 字
> 章节数：6（引言 1 + 三主题章 3 + 串联章 1 + 总结章 1）
> 深度均衡：文件系统 / 注册表 / PowerShell 三章篇幅与深度相当（对应素材论断 40 / 40 / 38 条）
> 素材入口：`02_deep_research.md`（唯一素材入口；引用 ID 沿用其中的 `[A*]` / `[S*]` / `[C-*]`）

---

## 全局写作约定（chapter-writer 必须遵守）

### 一、命令标注格式（每条命令都必须满足）

1. **执行环境**必须标明：`cmd`（命令提示符）/ `PowerShell` / `regedit`（注册表编辑器界面）/ `diskpart`（交互式子环境）。
2. **适用版本**必须标明：`5.1`（`powershell.exe`）/ `7`（`pwsh.exe`）/ `5.1 & 7`。非 PowerShell 命令标"全版本适用"。
3. **管理员权限**：
   - 来源明说则照写（例：`diskpart` 必须属于本地管理员组 [A15]；`fsutil` 必须以管理员或管理员组成员身份登录 [A18]；`Set-ExecutionPolicy -Scope CurrentUser` 不需要管理员 [C-3]；启用系统还原的 cmdlet 需"以管理员身份运行" [S26]；regedit 导出/导入会有管理员确认提示 [S18]）。
   - **来源未说明的一律写"官方未说明"，不得推断**。需特别保守处理的清单见本节第四条。
4. 建议统一命令块格式：命令块前一行写「环境 / 版本 / 权限」三元组，块内用 `#` 注释写用途。

### 二、"官方未说明"清单（写作时必须保守处理，不得补全为结论）

| 位置 | 项 | 要求的写法 |
|---|---|---|
| 第 1 章 1.6 | `mklink /d`（符号链接）提权要求 | 只能写"创建符号链接可能需要提升权限，**官方文档未明确说明**"（P2 已拍定） |
| 第 1 章 1.5 / 1.3 / 1.9 | `compact`、`cipher`、`mountvol`、`robocopy` 管理员要求 | 写"官方未说明"；`fsutil` 例外，有明确来源 [A18] |
| 第 2 章 2.7 / 2.8 | `reg export / import / save / restore / load / unload` 管理员要求 | 写"官方未说明"；只有 regedit [S18]、PowerShell 提权 [S26]、`HKCU\Software\Classes` 免提权 [S25] 三处有官方依据 |
| 第 1 章 1.4 | `AppData\LocalLow` 的用途 | 只写路径与"无 CSIDL 等效项"；**不写**"低完整性级别进程使用"（无来源） |
| 第 1 章 1.4 | `System32` / `WinSxS` "不可手动删除" | 只描述其存在，**不写**"不可删"的断言（无官方依据） |
| 第 1 章 1.8 | `attrib` 的"设 s/h 后须先清除才能改其他属性" | 单一来源 [A9]，写作时标注"仅一条官方来源、未实测" |
| 第 1 章 1.5 | EFS 与 NTFS 压缩的互斥方向 | **只写单向**"无法加密已压缩文件" [A21]；**不得写成双向"互斥"** |
| 第 2 章 2.9 | `HKCR\*\shell` 通配 verb、"给所有文件加右键菜单" | 无 A 级来源，**不写**；只讲 ProgID 级 verb [S23][S25] |
| 第 2 章 2.3 | `USRCLASS.DAT`、`RegBack` 目录 | 零命中，**不写** |
| 第 2 章 2.9 | `HKLM\SYSTEM\...\Session Manager\Environment`、`HKCU\Environment` | 零命中，**不写**；需要时只用已命中的路径 |
| 第 3 章 3.7 | 中文用户名导致 `PSModulePath` 异常 | **不写进正文**（无任何可用来源，P2 已拍定） |
| 第 3 章 3.7 | 中文目录下调外部程序报 `Error 3` | 只作 C 级"现象"提及 [C-19]，**不解释成原理**（无 A 级支撑） |
| 全篇 | 注册表"优化 / 清理 / 加速"第三方工具 | **绝对不得出现** |

### 三、注册表章强制口径

1. 必须含"**先备份再修改**"的完整操作步骤。
2. 回滚**主路径 = 导出 `.reg` → 需要时导入还原**（官方步骤覆盖 Win11 [S18]）。
3. 进阶路径 = `reg save` → `reg restore`（`.hiv`，官方明写"编辑任何注册表项之前必须 reg save" [S15][S16]）。
4. **系统还原只作整机级兜底/附注**，并注明官方版本声明存疑（[S26] 正文说仅 Win7/Vista/XP 受支持，但 [S18] 覆盖 Win11 且完全不提系统还原）。**不得写成回滚主路径。**
5. 明确区分"**按键级备份**（regedit 导出）"与"**整机级备份**（备份系统状态）"，不得混为一谈。
6. 素材第 4.4 节的"编辑前官方风险 checklist"必须原样落地为 Callout（见第 2 章 2.7）。

### 四、来源使用纪律

1. **C 级来源（C-17 / C-18 / C-19）只用于"现象描述"**，其原理必须回指 A 级来源（C-17 现象 → [C-3] 原理；C-18 现象 → [C-8] 原理；C-19 无 A 级原理，降级为"某些第三方程序的已知限制"）。
2. 素材中"本文整理"条目（[C-16] cmd/Bash 对照表）无单一官方出处，引用时标注"本文整理，逐格依据见 C-2 / C-4 / C-5 / C-8 / C-3"。
3. 素材标注"**降维改写**"的来源（A6、A7）是开发者/部署视角官方页：路径事实为 A 级可直接用，表述必须按第 5 节方向重写。
4. 引用 [S6]（KB256986）时注明"内容源自经典 KB，个别路径描述偏旧"。

### 五、降维改写通用手法

术语首次出现采用「**中文人话 → 官方术语 → 它到底指什么**」三步；正文优先用中文人话，官方术语放括号或脚注。三章各自的降维清单见各章"需降维改写"栏。

### 六、Callout 约定（Obsidian）

`[!note]` 核心概念 / `[!tip]` 实践建议 / `[!warning]` 易错点 / `[!example]` 示例 / `[!summary]` 小结。每章结尾一个 `[!summary]`。

---

## 第零章：导读——文件系统、注册表、PowerShell 是什么关系

- **篇幅**：短（1000–1500 字）
- **覆盖要点**：
  - 一句话各自定位：文件系统管"数据放在哪"，注册表管"系统和程序怎么配置自己"，PowerShell 管"怎么用命令批量操作前两者"
  - 三者的交叉点：注册表长在文件系统上（hive 是磁盘文件）、PowerShell 用同一套命令操作两者（Provider）
  - 本笔记的阅读约定：命令块三元组标注（环境 / 版本 / 权限）、"官方未说明"的处理方式
  - 安全练习纪律：命令先在小范围试、改注册表前先导出 `.reg`
- **素材引用**：[A1]（卷/目录/文件概览）、[S2]（hive 是磁盘文件）、[C-5]（Provider 统一模型）、[S8]（官方 Caution：改注册表前先备份）、素材第 6 节第 1–3 条
- **代码示例**：无
- **对应素材位置**：各方向第 7 节"下游交接摘要"；素材第 6 节"结构建议"
- **核心易错点（Callout 预留）**：
  - `[!warning]` 三者不是三个并列的软件，而是"存储层 / 配置层 / 操作层"的关系；读者最常混淆的是"注册表也是存在硬盘上的文件"这一点
- **需降维改写**：无（本章为导读）

---

## 第一章：Windows 文件系统——数据到底放在哪

- **篇幅**：长（6500–8000 字）
- **覆盖要点**：卷/目录/文件三层模型 → 命名与路径规则 → 盘符与装入点 → 系统目录地图 → NTFS 四大特色 → 链接三兄弟 → 属性与权限 → 复制备份
- **素材引用**：[A1]–[A21]（全方向 21 条来源）；论断 1–40
- **代码示例**：有（约 20 个代码块 / 约 45 条命令）
- **对应素材位置**：方向 A 第 2 节子主题一～十；第 3 节矛盾 1–4；第 4 节可操作指引；第 5 节降维改写 1–12；第 6 节缺口 1–9
- **本章定位**：概念部分占约 55%（1.1–1.6），命令清单占约 45%（1.3、1.5–1.9）

**小节结构**

- **1.1 三个基本名词：卷、目录、文件**（概念，短）
  - 1.1.1 官方定义：卷是"目录和文件的集合"，目录是"目录和文件的分层集合"，文件是"相关数据的逻辑分组" [A1]
  - 1.1.2 反直觉点：目录在文件系统层面本身就是一种"具有特殊属性的文件"，所以目录名受文件名规则约束 [A1][A2]
  - 1.1.3 NTFS 是什么、为什么是新版 Windows 的默认（安全描述符 / 加密 / 磁盘配额 / 丰富元数据）[A14]
  - 降维：删掉"文件系统由驱动程序和动态链接库组成""CreateFile""I/O 系统"等表述，改写为"Windows 靠一组后台程序 + 系统文件读写硬盘，你不需要知道它们在哪"（方向 A 第 5 节第 1 条）

- **1.2 命名规则与路径规则（全章第一坑区）**（概念 + 实验，中）
  - 1.2.1 9 个保留字符 `< > : " / \ | ? *` 与 NUL 字符；反斜杠是"分隔名称的保留字符" [A2]
  - 1.2.2 保留设备名 `CON / PRN / AUX / NUL / COM1–COM9 / LPT1–LPT9`；`NUL.txt` 等效于 `NUL` [A2]
  - 1.2.3 不要以空格或句点结尾；大小写不敏感（`OSCAR` = `oscar`，`D:\` = `d:\`）[A2]
  - 1.2.4 8.3 短名 `T97B4~1.TXT`；**不要假设短名一定存在**（可被禁用）[A2]
  - 1.2.5 绝对路径 / 相对路径 / UNC；**`C:tmp.txt` 指"C 盘当前目录"，与 `C:\tmp.txt` 完全不同**；`.` 与 `..` [A2]
  - 1.2.6 路径开头的两个字符决定 Windows 用哪套规则：`\\?\` 是"给程序用的'别自作聪明'开关"，`\\.\` 是直接访问设备的入口 [A2]
  - 1.2.7 MAX_PATH = 260 的构成；扩展长度路径约 32767 字符（近似值）；`\\?\` 下不能用正斜杠、不能用 `.` / `..` [A3]
  - 1.2.8 长路径开关：注册表 `LongPathsEnabled`(REG_DWORD)=1 **且**应用清单含 `longPathAware`，二者缺一不可；该值按进程缓存、可能需要重启 [A3]
  - 降维：命名空间（`\\?\` / `\\.\` / NT 命名空间 / GLOBALROOT / 对象管理器）只保留"路径开头两个字符决定规则"这一个直觉，`PhysicalDrive`、`HarddiskVolume1` 等对象名删除或移入附录（方向 A 第 5 节第 2 条）
  - 降维：`REG_DWORD`、"按进程缓存"降为"改一个开关 + 可能需要重启"；但"应用必须自己声明支持"**必须保留**，用"老程序不一定认这个开关"解释（方向 A 第 5 节第 3 条）

- **1.3 盘符、卷、装入点与分区**（概念 + 命令，中）
  - 1.3.1 盘符与卷的区别；卷名语法 `\\?\volume\{GUID}\`（**需要花括号**）[A11]
  - 1.3.2 卷装入点：把卷挂到"现有 NTFS 目录"，可以不用盘符；好处是"用一个 `C:` 就能访问所有本地卷" [A11]
  - 1.3.3 `mountvol` 的 `/l` `/d` `/p` `/n` `/e` `/s`；`/p` 卸载会使卷脱机且**先关闭所有打开的句柄** [A11]
  - 1.3.4 `diskpart` 的**焦点模型**：先 `list` 再 `select`，之后所有命令作用于焦点对象，且焦点会**自动转移**；典型四步 `list disk` → `select disk 1` → `create partition primary` → `format fs=ntfs label=Backup quick` [A15]
  - 1.3.5 冷知识框：NTFS 卷上限由**群集大小**决定（4KB→16TB，64KB→256TB）；用 VSS"以前版本"时最大 64TB [A14]
  - 命令清单：`mountvol \\?\volume{...}\`、`mountvol /p`、`diskpart` 四步
  - 降维：句柄 / 共享模式 / `FILE_SHARE_DELETE` → "别人正在用这个卷时，强卸载会先断开他们的连接"（方向 A 第 5 节第 4 条）；群集大小 / PB / `STATUS_UNRECOGNIZED_VOLUME` → 一句话 + 冷知识框（第 8 条）

- **1.4 系统目录地图：C:\Windows、Program Files、Users、ProgramData、AppData**（概念，中）
  - 1.4.1 `%USERPROFILE%` 与 `AppData` 三兄弟：`Roaming`（`%APPDATA%`，漫游）、`Local`（`%LOCALAPPDATA%`，非漫游）、`LocalLow` [A6][A7]
  - 1.4.2 全机器共用的两个目录：`ProgramData`（`%ALLUSERSPROFILE%`）与 `Users\Public`（`%PUBLIC%`，Vista 新增）[A6][A7]
  - 1.4.3 `C:\Windows`（`%windir%`）、`System32`、64 位系统上的 `SysWOW64` [A6][A7]
  - 1.4.4 `Program Files` 与 `Program Files (x86)`：**`Program Files (x86)` 只存在于 64 位系统**；32 位系统上两个常量指向同一路径 [A6]
  - 1.4.5 用户级环境变量速查表（中文名 + `%环境变量%` + 真实路径三列）；提醒路径可能因"文件夹重定向"而不同 [A6]
  - 降维：删除 `FOLDERID_*` 常量名、GUID、CSIDL 列，改写为三列表格；`PERUSER` vs `FIXED` 改写为"每个用户各有一份" vs "全机器共用一份"（方向 A 第 5 节第 6 条）
  - **核心易错点（Callout 预留）**：
    - `[!warning]` "`Program Files (x86)` 一定存在"是错误直觉（32 位系统上不存在）；`FOLDERID_ProgramFilesX86` 默认路径官方同页两处自相矛盾，正文只写"64 位系统上为 `Program Files (x86)`"，不引入矛盾细节【跨方向冲突 #4；方向 A 矛盾 1、2】
    - `[!warning]` `AppData\LocalLow` 的用途**官方未说明**，不要编（方向 A 矛盾 3、缺口 2）
    - `[!warning]` `System32` / `WinSxS` 只描述其存在，**不写"不可手动删除"**（缺口 3）

- **1.5 NTFS 的四个特色功能：备用数据流、压缩、加密、稀疏文件**（概念 + 命令，长）
  - 1.5.1 备用数据流（ADS）：流"包含写入文件的数据"，每个流有自己的分配大小、实际大小和压缩/加密/稀疏状态；流**没有自己的文件时间** [A8]
  - 1.5.2 ADS 观察入口：`dir /r`；流名格式 `文件名:流名称:流类型`，`文件名::$DATA` 等价于 `文件名`；**用户无法创建新的流类型** [A8][A12]
  - 1.5.3 NTFS 压缩：`compact` 是命令行版；**"设置目录的压缩状态不一定更改已存在文件的压缩状态"**；不能压缩 FAT/FAT32 [A13]
  - 1.5.4 EFS 加密：`cipher`，输出 `E` = 已加密、`U` = 未加密；**"如果未加密父目录，则修改文件时加密文件可能会解密"→ 加密文件时必须同时加密父目录** [A16]
  - 1.5.5 EFS 单向结论：**无法加密已压缩文件**，但**可以加密稀疏文件**（只说这一个方向）[A21]
  - 1.5.6 稀疏文件：程序把未分配区域视为零但不用磁盘表示；应用必须**显式声明**为稀疏；`fsutil sparse setflag / queryflag / queryrange / setrange`；`fsutil` 必须以管理员身份运行 [A17][A18][A20]
  - 命令清单：`dir /r`、`compact /c /s:\`、`compact /CompactOs:query`、`cipher`、`cipher /e`、`cipher /w:`、`cipher /x`、`fsutil sparse setflag`
  - 降维：`FILE_ATTRIBUTE_SPARSE_FILE` / VDL / 流类型表 / `$INDEX_ALLOCATION` 全部移入附录，正文只留"NTFS 文件可以挂'隐藏的附加文件'，`dir /r` 能看到"（方向 A 第 5 节第 7 条）；`FSCTL_*` 只留 `fsutil sparse setflag` 一条命令 + 一句结论（第 9 条）；`XPRESS4K/8K/16K/LZX`、`.pfx/.cer` 移入进阶附录（第 12 条）
  - **核心易错点（Callout 预留）**：
    - `[!warning]` EFS 与压缩**只验证了单向**，不得写成双向"互斥"（方向 A 缺口 4）
    - `[!warning]` `compact` / `cipher` 管理员要求 **官方未说明**；`fsutil` 明确需要管理员 [A18]（缺口 6）
    - `[!warning]` `fsutil` 主页部分子命令描述抓取为空，涉及 `fsutil fsinfo` / `fsutil volume` 时不展开（方向 A 矛盾 4、缺口 8）

- **1.6 链接三兄弟：硬链接、符号链接、交接点**（概念 + 命令，中）
  - 1.6.1 **硬链接**：多个路径引用同一卷中的同一文件；**不能引用目录、不能跨卷** [A19]
  - 1.6.2 **交接点**：引用的是"单独的目录"，可链接同一台机器上的不同本地卷；靠重分析点实现 [A19]
  - 1.6.3 反直觉细节：目录条目大小和文件属性信息**只在进行更改的那个链接处更新**（一处清只读，另一处仍显示只读）[A19]
  - 1.6.4 `mklink` 四种形态：默认文件符号链接、`/d` 目录符号链接、`/h` 硬链接、`/j` 目录交接点；删除用普通命令（`rd` / `del`）[A5]
  - 1.6.5 硬链接的删除语义：**只有删除指向某一文件的所有链接后，该文件才会从文件系统删除** [A18]
  - 降维："重分析点""筛选器驱动"→"Windows 里一种'指针文件'"的类比，并明确"**删链接 ≠ 删原文件**"（方向 A 第 5 节第 10 条）
  - **核心易错点（Callout 预留）**：
    - `[!warning]` `/j` 的官方定义是"**目录联接**"，社区误称"目录硬链接"——以官方参数表为准【跨方向冲突 #5】
    - `[!warning]` `mklink /F` **不存在**（官方参数表只有 `/d` `/h` `/j` `/?`），网上常见信息有误【跨方向冲突 #6】
    - `[!warning]` `mklink /d` 的提权要求**官方未说明**：只能写"可能需要提升权限，官方文档未明确说明"（缺口 1；P2 已拍定）

- **1.7 查看与修改元数据：文件属性（attrib）与权限（icacls）**（命令 + 概念，中）
  - 1.7.1 `attrib` 属性字母：`r` 只读、`a` 存档、`s` 系统、`h` 隐藏、`o` 脱机、`i` 非内容索引等；`/s` 递归、`/d` 作用于目录、`/l` 作用于链接本身 [A9]
  - 1.7.2 `icacls` 是什么：显示或修改 DACL，取代已弃用的 `cacls`；**ACE 规范顺序固定**（显式拒绝 → 显式授予 → 继承的拒绝 → 继承的授予）[A4]
  - 1.7.3 简单权限字母 `N / F / M / RX / R / W / D`；高级权限和继承标志**必须写在括号里**（`(DE)` `(OI)` `(CI)` `(IO)` `(NP)`）；`/grant:r` 是替换而非追加 [A4]
  - 1.7.4 修坏权限的兜底 `/reset`（替换为默认继承 ACL）；`/inheritancelevel:e|d|r` 控制继承；数字 SID 前要加 `*`；ACL 批量备份/还原 `/save` → `/restore` [A4]
  - 降维：DACL / SID / ACE / 权限掩码只教"查看权限"和"重置权限"两条命令，掩码与继承标志表降级为"查表用"附录；SID 要说明"这是账户的内部编号，不是用户名"；`/setintegritylevel` 与完整性级别整体删除（方向 A 第 5 节第 5 条）
  - **核心易错点（Callout 预留）**：
    - `[!warning]` `attrib` 的"设了系统/隐藏属性后必须先清除，才能更改文件的其他属性"**仅有一条官方来源、未实测**，按此操作可能得不到预期结果（缺口 5）

- **1.8 列目录与看隐藏内容：dir 的三个开关与星号坑**（命令，短）
  - 1.8.1 `dir` 默认不显示隐藏/系统文件；`/a`（不带属性）才显示全部；`/r` 显示备用数据流；`/x` 显示 8.3 短名 [A12]
  - 1.8.2 **星号通配符始终使用短文件名映射**：`dir t97\*` 会同时返回 `t97.txt` 与 `t.txt2`，`del t97\*` 会删掉两个文件 [A12]
  - **核心易错点（Callout 预留）**：
    - `[!warning]` 星号通配符 + 短名映射的**误删风险**，搭配 `del` 时尤其危险 [A12]

- **1.9 复制与备份：robocopy 的默认值有多危险**（命令，中）
  - 1.9.1 基本语法与 `/s`（排除空目录）vs `/e`（包含空目录）[A10]
  - 1.9.2 **`/mir` = `/e` + `/purge`**，会删除目标端源中已不存在的文件和目录（破坏性最强），必须标红 [A10]
  - 1.9.3 **默认重试极其激进**：`/r` 默认 1,000,000 次、`/w` 默认 30 秒 → 网络路径失效时会长时间假死；官方示例普遍写 `/R:2 /W:5` [A10]
  - 1.9.4 退出码语义反直觉：`0` = 未复制任何文件（无失败），`1` = 全部成功复制，**≥8 才是至少发生一次故障** [A10]
  - 1.9.5 `/copy` 默认 `DAT`；`/sec` = `/copy:DATS`；`/copyall` = `/copy:DATSOU`；官方"强烈建议"每次加 `/log:` [A10]
  - 1.9.6 两个隐藏行为：robocopy **默认会跟随交接点**，需 `/xj` `/xjd` `/xjf` 排除；从设备根目录复制时目标目录会获得"隐藏 + 系统"属性 [A10]
  - 降维：完整退出码表改写为"**0 和 1 都算正常，≥8 才是出错**"一句话，`/mir` 标红（方向 A 第 5 节第 11 条）
  - 命令清单：`robocopy <src> <dst> /E /ZB /LOG:`、`/MIR /R:2 /W:5`、`/S /E /COPY:DAT /MT:16`、`/L` 演练、`/iorate:1m`、`/ETA`
  - **核心易错点（Callout 预留）**：
    - `[!warning]` `/mir` 会**删除目标端文件**，执行前必须先 `/L` 演练
    - `[!warning]` 默认 `/r:1000000 /w:30` 会让失效网络路径长时间假死
    - `[!warning]` robocopy 管理员要求 **官方未说明**（缺口 6）

- **本章核心易错点汇总（Callout 预留，逐条落到具体小节）**：见 1.2（`C:tmp.txt` ≠ `C:\tmp.txt`、`NUL.txt`、8.3 短名）、1.4（Program Files (x86) 存在性、LocalLow 用途、WinSxS 不可删）、1.5（EFS 单向、compact/cipher 权限未说明）、1.6（`/j` 定义、`/F` 不存在、`mklink /d` 提权未说明）、1.7（attrib 操作顺序单源未实测）、1.8（星号 + 短名误删）、1.9（`/mir` 破坏性、默认重试、退出码）
- **需降维改写（来自方向 A 第 5 节，12 条全部有归属）**：1.1（API 表述）、1.2（命名空间、路径长度注册表细节）、1.3（句柄类术语、卷/群集单位）、1.4（CSIDL/KNOWNFOLDERID/GUID、PERUSER/FIXED）、1.5（文件流术语、`FSCTL_*`、算法名与证书参数）、1.6（重分析点）、1.9（退出码表）
- **素材未覆盖、需在文中标注为空白的点**：文件/目录时间戳三项（创建/访问/修改）的官方说明、ReFS 与 NTFS 的区别（方向 A 缺口 9）

---

## 第二章：Windows 注册表——系统和程序的配置中心

- **篇幅**：长（6500–8000 字）
- **覆盖要点**：树/键/子项/值 → 五个根键 → Hive 与磁盘文件 → 值类型与尺寸限制 → 32/64 位视图 → 权限与所有者 → **备份与回滚（强制主线）** → 查询修改删除命令 → 实用路径速查
- **素材引用**：[S1]–[S27]（全方向 27 条来源）；论断 2.1–2.10
- **代码示例**：有（约 14 个代码块 / 约 32 条命令）
- **对应素材位置**：方向 B 第 2 节 2.1–2.10；第 3 节矛盾 1–5；第 4 节 4.1–4.7（4.4 为 Callout 来源）；第 5 节降维改写表（13 项）；第 6 节缺口 1–12
- **本章定位**：概念部分占约 50%（2.1–2.6），命令与安全流程占约 50%（2.7–2.9）

**小节结构**

- **2.1 注册表是什么：树、键、子项、值**（概念，短）
  - 2.1.1 分层数据库，数据以树组织；节点叫**键**，键下可同时有**子项**和**值** [S1]
  - 2.1.2 命名规则：键名**不能含反斜杠**、不做本地化；值名称和数据**可以**含反斜杠、可以被本地化 [S1]
  - 2.1.3 树的深度：最深可达 512 层；单次 API 调用一次最多创建 32 层 [S1]
  - 2.1.4 预定义根键的意义：应用"应始终在预定义键框架内工作"，这样管理工具才找得到数据 [S4][S6]
  - 降维：预定义项 / 句柄 / `RegOpenKeyEx` 下沉到"给开发者的补充"区块；正文只说"注册表有 5 个顶层文件夹"（方向 B 第 5 节）

- **2.2 五个根键各管什么**（概念，中）
  - 2.2.1 `HKLM`：保存计算机**物理状态**数据（总线类型、系统内存、已安装软硬件、即插即用信息）[S4]
  - 2.2.2 `HKCU`：保存**当前用户**偏好（环境变量、程序组、颜色、打印机、网络连接、应用偏好）；它映射到 `HKEY_USERS` 中当前用户的分支，映射是**按进程**建立的；没有已加载 hive 时映射到 `HKEY_USERS\.Default` [S4]
  - 2.2.3 `HKCR`：**不是真实存储位置**，是 `HKLM\Software\Classes` 与 `HKCU\Software\Classes` 的**合并视图**；写 HKCR 会被重定向 [S6]
  - 2.2.4 `HKCC` 只是 `HKLM\System\CurrentControlSet\Hardware Profiles\Current` 的**别名**；`HKEY_PERFORMANCE_DATA` 的数据**并不真的存在注册表里** [S4]
  - **核心易错点（Callout 预留）**：
    - `[!warning]` 想改"交互式用户的设置"必须写在 `HKCU\Software\Classes`；想改"默认设置"必须写在 `HKLM\Software\Classes`；**不要直接写 HKCR** [S6]

- **2.3 Hive：注册表在磁盘上的真实文件**（概念，中）
  - 2.3.1 **hive（配置单元）**是键/子项/值的逻辑组，带一组"在系统启动或用户登录时加载到内存的支持文件" [S2]
  - 2.3.2 每次新用户登录都会创建一个**用户配置文件配置单元**，挂在 `HKEY_USERS` 下 [S2]
  - 2.3.3 支持文件对照表：`HKLM\SAM`→`Sam`、`HKLM\Security`→`Security`、`HKLM\Software`→`Software`、`HKLM\System`→`System`、`HKU\.DEFAULT`→`Default`；**大部分**位于 `%SystemRoot%\System32\Config` [S2]
  - 2.3.4 用户级 hive 的磁盘承载文件是 `NTUSER.DAT`（及 `.LOG`）[S2][S6]
  - 2.3.5 扩展名含义：无扩展名 = 完整副本；`.alt` = 仅 `HKLM\System` 才有的备份副本；`.log` = 事务日志；`.sav` = 备份副本 → **这些是系统自己用的副本和日志，不要动它们** [S2]
  - 2.3.6 格式演进：Win2000 只支持标准格式，XP 起支持最新格式；但 `HKCU`、`HKLM\SAM`、`HKLM\Security`、`HKU\.DEFAULT` **仍使用标准格式** [S2]
  - 2.3.7 临时挂载场景：`RegLoadKey` / `RegUnLoadKey` 把注册表的一部分当文件加载再卸下 [S3]
  - 降维：hive / "配置单元"是生造词 → 首次出现写"注册表的'数据库文件'（官方术语叫 hive，中文译作'配置单元'）"，并立刻落到"它是磁盘上真实存在的文件"；后文统一用"注册表文件"或直接给文件名；".log / .alt / .sav"重点是"不要删"而不是"它们是什么"（方向 B 第 5 节）
  - **核心易错点（Callout 预留）**：
    - `[!warning]` **HKCU 支持文件的磁盘位置，两份官方文档不一致**（`%SystemRoot%\System32\Config` vs `%SystemRoot%\Profiles\Username`），**都没有提现代路径**；写作时只说"`NTUSER.DAT` 属于用户配置文件 hive"，磁盘位置用"用户配置文件目录"表述，**不写死路径**，并注明"部分官方资料仍沿用旧布局描述"【跨方向冲突 #3；方向 B 矛盾 1】
    - `[!warning]` `USRCLASS.DAT`、`RegBack` 目录**零来源命中**，不写（方向 B 缺口 3、4）

- **2.4 值类型：一套类型的三副面孔**（概念 + 查表，中）
  - 2.4.1 常用类型：`REG_SZ`（字符串）、`REG_BINARY`（二进制）、`REG_DWORD`（32 位数字）、`REG_QWORD`（64 位数字）、`REG_NONE` [S5]
  - 2.4.2 `REG_EXPAND_SZ`：包含对环境变量的**未扩展引用**（如 `%PATH%`），需要时用 `ExpandEnvironmentStrings` 展开 [S5]
  - 2.4.3 `REG_MULTI_SZ`：以**两个**长度为 0 的字符串结尾的序列，**不能包含零长度字符串** [S5]
  - 2.4.4 **三列对照表**：`REG_SZ` ↔ regedit 显示"字符串值" ↔ PowerShell `-Type String`，再补一列"什么时候用" [S5][S6][S21]
  - 2.4.5 字符串终止符是读写注册表最常见的陷阱（写入要把终止 null 计入长度；读取时字符串可能未正确终止）[S5]
  - 2.4.6 regedit 里 DWORD 可按二进制/十六进制/十进制显示；`REG_QWORD` 在编辑器中以**二进制值**形式显示 [S6]
  - 2.4.7 尺寸限制一张小表：值名称 ≤16,383 字符；**值数据 >2,048 字节必须改存文件**；**一个键的所有值合计 ≤64K**；`Run` 键命令行 ≤260 字符 [S6][S19]
  - 降维：读者在 regedit 里看到的是"字符串值 / DWORD 值"，不是 `REG_SZ`；`REG_DWORD_LITTLE_ENDIAN` 只需一句"Windows 上它就等于 `REG_DWORD`，不用管"；`\0` 写成"字符串末尾的隐藏结束符"；小端/大端压成一句可选脚注（方向 B 第 5 节）

- **2.5 64 位系统上的两套注册表：WOW6432Node**（概念，短）
  - 2.5.1 默认行为：32 位应用访问 32 位视图，64 位应用访问 64 位视图；`KEY_WOW64_64KEY`（0x0100）/ `KEY_WOW64_32KEY`（0x0200）可切换，但**对共享注册表键无效**，**同时指定会失败**（`ERROR_INVALID_PARAMETER`）[S20]
  - 2.5.2 **`Wow6432Node` 与 `WowAA32Node` 是保留键，"应用程序不应直接使用这些键"** [S20]
  - 2.5.3 读者实际只会遇到两个开关：`reg query` / `reg add` / `reg import` 的 `/reg:32` 与 `/reg:64`；64 位 regedit 会在 `HKLM\Software\WOW6432Node` 下显示 32 位项 [S9][S10][S14][S6]
  - 降维：改写为"**64 位系统上其实有两套注册表：64 位程序看一套，32 位程序看另一套，32 位那套挂在 `WOW6432Node` 下面**"；掩码数字放进折叠块或删去（方向 B 第 5 节）
  - **核心易错点（Callout 预留）**：
    - `[!warning]` 找不到某个键时，先怀疑"是不是看错了视图"；**不要直接去改 `WOW6432Node`**（保留键）[S20]

- **2.6 权限与所有者**（概念，短）
  - 2.6.1 键可以带一张权限清单；未指定时**默认权限清单继承自它的直接父键** [S7]
  - 2.6.2 查值需要 `KEY_QUERY_VALUE`、写值需要 `KEY_SET_VALUE`、建子项需要 `KEY_CREATE_SUB_KEY`、枚举子项需要 `KEY_ENUMERATE_SUB_KEYS`；注册表键**不支持 `SYNCHRONIZE`**；`KEY_CREATE_LINK` 保留给系统 [S7]
  - 2.6.3 权限不足时官方给出的唯一解法：启用 `SE_TAKE_OWNERSHIP_NAME` 特权并以 `WRITE_OWNER` 打开该键 [S7]
  - 2.6.4 两个核对入口：regedit「编辑」>「权限」；PowerShell `Get-Acl` / `Set-Acl` [S7][S21]
  - 降维：ACL / SACL / 安全描述符压缩成一条脚注，正文用"权限清单""审计清单"；`SE_TAKE_OWNERSHIP_NAME` / `WRITE_OWNER` 改写为"**取得所有权**"与"以**所有者身份写入**的权限"，正文给动作："在权限对话框里把所有者改成自己，再赋完全控制"（方向 B 第 5 节）

- **2.7 备份与回滚（本章强制主线，必须先讲再讲修改）**（概念 + 命令，长）
  - 2.7.1 官方的两条警告原文（Caution 级 [S8] + Warning 级 [S6]）："除非没有替代项，否则不要直接编辑注册表""错误修改可能需要重新安装操作系统才能解决，Microsoft 不能保证可以解决"；同时官方也承认"编辑注册表有时可能是解决产品问题的最佳方法" [S8][S6]
  - 2.7.2 官方推荐的修改顺序：优先用 Windows 用户界面或组策略改系统设置；若 KB 有分步说明，"建议完全按照这些说明操作" [S6]
  - 2.7.3 **主路径（覆盖 Win11）：导出 `.reg` → 导入还原**
    - regedit 界面步骤（官方最完整）：开始 → 搜索 `regedit.exe` → 回车（**若有管理员密码或确认提示，需提供**）→ 定位并单击要备份的项 →「文件」>「导出」→ 选位置填文件名 →「保存」；还原为「文件」>「导入」[S18]
    - 命令行：`reg export "HKLM\SOFTWARE\MyApp" AppBkUp.reg /y` → `reg import AppBkUp.reg`；`.reg` 扩展名必须有；**仅适用于本地计算机**；返回 0 = 成功 / 1 = 失败 [S13][S14]
  - 2.7.4 **进阶路径：整键快照 → 写回（.hiv）**
    - `reg save "HKLM\Software\MyApp" AppBkUp.hiv /y` → `reg restore "HKLM\Software\MyApp" AppBkUp.hiv`
    - 官方备注可直接引用为"编辑前先备份"的依据："在编辑任何注册表项之前，必须使用 **reg save** 命令保存父子项。如果编辑失败，则可以使用 **reg restore** 还原原始子项" [S15][S16]
    - `reg restore` 会**覆盖**目标键现有内容，文件必须由 `reg save` 创建且必须是 `.hiv` 扩展名 [S16]
    - 临时排查：`reg load HKLM\TempHive TempHive.hiv` → 用完必须 `reg unload HKLM\TempHive` [S17][S8]
  - 2.7.5 **整机级兜底**：备份工具备份"系统状态"（含注册表、COM+ 类注册数据库、启动文件）；还原走"从备份还原系统状态"；还会在 `%SystemRoot%\Repair` 生成注册表文件的更新副本 [S6]
  - 2.7.6 **系统还原（只作附注，不作主路径）**：`Enable-ComputerRestore -Drive "C:\"`；官方明确要求"以管理员身份运行"；要在任何驱动器上启用必须**先在系统驱动器上启用**；不能用于外部驱动器或远程网络驱动器；`Rstrui.exe` 可查看还原状态 [S26]
  - 2.7.7 **Callout：编辑前的官方风险 checklist**（素材第 4.4 节直接落地，必须出现）
    - `[!warning]` 除非没有替代项，否则不要直接编辑注册表；能改设置就用控制面板 / 组策略 / MMC
    - `[!warning]` 错误修改可能需要重新安装操作系统才能解决，Microsoft 不能保证可以解决
    - `[!tip]` 修改前必须备份；主路径是导出 `.reg`，进阶是 `reg save` 出 `.hiv`
    - `[!tip]` 遇到权限不足的键：取得所有权（启用 `SE_TAKE_OWNERSHIP_NAME` 特权，以 `WRITE_OWNER` 打开）[S7]
    - `[!tip]` 改之前先核对现有权限：regedit → 定位到键 →「编辑」>「权限」[S7]
  - **核心易错点（Callout 预留）**：
    - `[!warning]` **系统还原不得写成回滚主路径**：官方一页说它仅在 Win7/Vista/XP 受支持，另一页（覆盖 Win11）完全不提它【跨方向冲突 #1；方向 B 矛盾 2】
    - `[!warning]` **"备份整个注册表"含义不统一**：按键级备份 = 导出 `.reg`；整机级 = 备份系统状态。不要把"导出 HKLM\Software 下一个键"当成"备份了整个注册表"【跨方向冲突 #2；方向 B 矛盾 3】
    - `[!warning]` `reg export / import / save / restore / load` 的管理员要求 **官方全未明示**；只有 regedit [S18]、PowerShell 提权 [S26]、`HKCU\Software\Classes` 免提权 [S25] 三处有依据（方向 B 缺口 8）
    - `[!tip]` "不要直接编辑注册表"的**语气强度**两页不同：`reg` 命令页是 Caution 级，KB256986 是 Warning 级并承认有时必须改——两处原文都要保留，不要合成一个更强或更弱的版本（方向 B 矛盾 4）

- **2.8 查询、修改、删除：reg.exe 与 PowerShell 对照**（命令，长）
  - 2.8.1 `reg query` 完整语法与参数：`/s` 递归、`/f` 搜索数据或模式、`/k`（**必须与 `/f` 同时使用**）仅搜键名、`/d` 仅搜数据、`/c` 区分大小写、`/e` 完全匹配、`/t` 限定类型、`/z` 附类型数字 [S9]
  - 2.8.2 `reg add`：**无法通过此操作添加子树**；`REG_EXPAND_SZ` 里的百分号必须用 `^` 转义（`^%systemroot^%`）；`/t` 可选类型清单 [S10]
  - 2.8.3 `reg delete`：`/va` 删该键所有值**但不删子项**、`/v` 删特定值、`/ve` 只删没有值的条目、`/f` 免确认 [S11]
  - 2.8.4 `reg copy`：指定 `/s` 才连同所有子项和条目；复制子项时**不要求确认** [S12]
  - 2.8.5 PowerShell 等价写法与差异：`Set-ItemProperty`（**`-Type` 默认 `String`（REG_SZ）**）、`New-ItemProperty`、`Copy-ItemProperty`、`Move-ItemProperty`、`Rename-ItemProperty`、`Remove-Item`（含子项时**默认弹确认**，加 `-Recurse` 免提示）、`Remove-ItemProperty`、`Clear-Item`（清空键的所有值但保留键本身）[S21]
  - 2.8.6 官方提醒：能用管理接口就别直接改注册表（示例：服务启动类型既可用 `Set-ItemProperty` 也可用 `Set-Service` 改回）[S21]
  - 2.8.7 `reg` 的根键规则：本地有效根键为 `HKLM` / `HKCU` / `HKCR` / `HKU` / `HKCC`；指定远程计算机时**只有 `HKLM` 和 `HKU` 有效** [S9][S8]
  - **核心易错点（Callout 预留）**：
    - `[!warning]` `reg add` **不能创建子树**；`reg delete /va` **不会删子项** [S10][S11]
    - `[!warning]` `Set-ItemProperty` 的 `-Type` 默认为 `String`，写数字型值必须显式指定 `DWord` / `QWord`，否则类型写错 [S21][S22]
    - `[!tip]` `reg copy` 页面文末残留"reg 比较作的返回值"字样，属官方笔误，引用返回值语义以页面正文的 0 = Success / 1 = Failure 为准（方向 B 矛盾 5）

- **2.9 实用路径速查与开机自启**（命令 + 概念，中）
  - 2.9.1 开机自启共**四个** `Run` / `RunOnce` 键（HKLM 与 HKCU 各两个，均在 `Software\Microsoft\Windows\CurrentVersion\` 下）；`Run` 每次登录运行、`RunOnce` 运行一次后**删除该键** [S19]
  - 2.9.2 `RunOnce` 的三个行为细节：`HKLM\...\RunOnce` **仅在管理员组成员登录时执行**；默认在命令行运行**之前**删值，值名前加 `!` 可**延迟到命令运行之后**；默认在安全模式下忽略，值名前加 `*` 可**强制在安全模式运行** [S19]
  - 2.9.3 文件关联三要素：**verb（谓词）**= 右键菜单里的一条命令项，命令字符串形如 `"My Program.exe" "%1"`（含空格的元素必须加引号）；**ProgID** = 文件类型的登记名，格式 `厂商.组件.版本`（如 `Word.Document.6`）；键位置 `HKEY_CLASSES_ROOT\<ProgID>\shell\<verb>\command` [S23][S24]
  - 2.9.4 一个免提权技巧：因为 HKCR 是 HKCU 与 HKLM 的组合，**可以把自定义 verb 注册在 `HKEY_CURRENT_USER\Software\Classes` 下，"主要好处是不需要提升权限"** [S25]
  - 2.9.5 速查表（只收已命中项）：四个自启键、`HKCR\DesktopBackground\Shell`、`HKCR\Applications\<MyProgram.exe>\shell\...`、`HKLM\Software\WOW6432Node`、`HKLM\HARDWARE`、`HKU`（用户 hive 键位置）、`HKLM\System\CurrentControlSet\Hardware Profiles\Current`、`HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion` [S19][S23][S25][S6][S21][S2][S4][S22]
  - **核心易错点（Callout 预留）**：
    - `[!warning]` `RunOnce` 的删值时机与 `!` / `*` 前缀语义容易记反；`HKLM\...\RunOnce` 仅管理员组登录时执行 [S19]
    - `[!warning]` `HKCR\*\shell` 通配 verb、"给所有文件加右键菜单"**无 A 级来源**，不写（方向 B 缺口 7）
    - `[!tip]` 看到形如 `@%SystemRoot%\shell32.dll,-154` 的间接字符串，只当"别手动改这类值"的警告，不解释语法（方向 B 第 5 节）

- **本章核心易错点汇总（Callout 预留，逐条落到具体小节）**：见 2.2（HKCR 是合并视图）、2.3（HKCU 磁盘位置两说、USRCLASS.DAT/RegBack 零命中）、2.5（WOW6432Node 保留键）、2.7（系统还原非主路径、整机级 vs 按键级、reg.exe 权限未说明、警告语气差异）、2.8（reg add / delete 边界、`-Type` 默认 String、页面笔误）、2.9（RunOnce 语义、`HKCR\*\shell` 无来源）
- **需降维改写（来自方向 B 第 5 节，13 项全部有归属）**：hive（2.3）、ACL/SACL/安全描述符（2.6）、WOW6432Node 与掩码（2.5）、`REG_*` 类型名（2.4）、`\0` 终止符（2.4）、小端（2.4）、ProgID/verb（2.9）、间接字符串（2.9）、`.log/.alt/.sav`（2.3）、预定义项/句柄（2.1）、四个尺寸数字（2.4）、"父子项"表述（2.7）、`SE_TAKE_OWNERSHIP_NAME`（2.6）
- **素材未覆盖、需在文中标注为空白的点**：注册表编辑器的界面级操作（新建项/重命名/查找/收藏夹）官方来源缺失（方向 B 缺口 1）；创建还原点的官方 cmdlet 出处缺失（缺口 2）；环境变量注册表路径零命中（缺口 5）；`HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion` 未直接命中（缺口 6）

---

## 第三章：Windows PowerShell——用命令操作前两者

- **篇幅**：长（6500–8000 字）
- **覆盖要点**：对象而非文本 → 管道与参数绑定 → 命令命名与四个自举命令 → 帮助系统 → Provider 与 PSDrive → 执行策略 → 编码与中文乱码 → 5.1 与 7 的并行关系 → 与 cmd/Bash 对照
- **素材引用**：[C-1]–[C-19]；其中 A 级 15 条、本文整理 1 条（[C-16]）、C 级 3 条（[C-17][C-18][C-19]）；论断 2.1–2.11
- **代码示例**：有（约 14 个代码块 / 约 40 条命令）
- **对应素材位置**：方向 C 第 2 节 2.1–2.11；第 3 节矛盾 1–7；第 4 节 4.1–4.4、4.6；第 5 节降维改写表（13 项）；第 6 节缺口 1–8
- **本章定位**：概念部分占约 55%（3.1–3.5、3.8），命令与排错占约 45%（3.4、3.6、3.7）
- **注意**：方向 C 第 2.10 节（文件系统与注册表常用 Cmdlet）**主体放入第 4 章**，本章只做"有这些命令"的预告

**小节结构**

- **3.1 对象而不是文本：PowerShell 与 cmd 的根本差别**（概念，短）
  - 3.1.1 官方结论：PowerShell **接受并返回 .NET 对象而不是文本**，所以管道连接更省事 [C-2]
  - 3.1.2 用对比场景讲清好处：文本管道只能传字符串，想取"第 3 列"要切字符串；对象管道里每个进程自带 `Name`、`Id`、`Handles` 等**带名字的格子**，可以直接点出来 [C-2]
  - 降维：不得直接写".NET 对象"就完事，必须先用上面这个对比场景铺垫（方向 C 第 5 节第 1 行）

- **3.2 管道怎么工作：一次一个对象**（概念 + 例子，中）
  - 3.2.1 管道由 `|` 连接，每个运算符把上一条命令的结果发给下一条，按从左到右处理 [C-1]
  - 3.2.2 因为传的是对象，`Get-Process notepad | Stop-Process` 中 `Stop-Process` 无需 `-Name` / `-ID` [C-1]
  - 3.2.3 成功流 / 错误流类似 stdout / stderr，但**stdin 并未接入 PowerShell 管道** [C-1]
  - 3.2.4 接收端必须"接受管道输入"；用 `Get-Help <cmdlet> -Full` 或 `-Parameter *` 才能查到是哪个参数、怎么接收 [C-1]
  - 3.2.5 两种接收方式：**ByValue**（按值：类型匹配或可转换）与 **ByPropertyName**（按属性名：输入对象有同名属性）；绑定成功需三条同时满足；**无法强制绑定到特定参数** [C-1]
  - 3.2.6 **关键区别**：管道**一次发送一个对象**；用 `-InputObject` 则把集合当**单个数组对象**发送——官方称"这种细微差异具有重大后果"（`Get-Process | Get-Member` 显示 `System.Diagnostics.Process`，而 `Get-Member -InputObject (Get-Process)` 显示 `System.Object[]`）[C-1]
  - 3.2.7 自动枚举的例外：哈希表需 `GetEnumerator()`；**`System.String` 虽实现 `IEnumerable` 却不会被枚举** [C-1]
  - 降维：ByValue / ByPropertyName 改成"下一个命令按什么规则接住上一个命令丢过来的东西：看值的类型（**按值**）还是看属性的名字（**按属性名**）"；"实现 `IEnumerable`"改成"数组会被拆成一个个元素逐个往后传；**字符串和哈希表不会被拆开**"，各配一个可跑的例子（方向 C 第 5 节）
  - **核心易错点（Callout 预留）**：
    - `[!warning]` 报"输入对象无法绑定到任何参数"时的排查三步：`Get-Help <cmd> -Parameter <目标参数>`（是否接受管道输入、按值还是按属性名）→ `... | Get-Member`（对象有没有同名属性）→ `Trace-Command -Name ParameterBinding` [C-1]

- **3.3 命令长什么样：Verb-Noun 与四个自举命令**（概念，短）
  - 3.3.1 cmdlet 命名是 **Verb-Noun**（如 `Get-Process`），谓词取自 `Get-Verb` 返回的标准动词表 [C-2]
  - 3.3.2 四个自举命令回答四个不同问题：`Get-Verb`（合法动词）、`Get-Command`（装了哪些命令，支持 `-Name` / `-Verb` / `-Noun` / `-ParameterType` 过滤）、`Get-Member`（对象有什么属性方法）、`Get-Help`（命令怎么用）[C-2][C-6]
  - 3.3.3 官方推荐的"找命令"顺序：`Get-Command` → `Get-Help` → `Get-Member` [C-2][C-6]

- **3.4 让 PowerShell 自己教你怎么用：Get-Help 与 Update-Help**（命令，中）
  - 3.4.1 `Get-Help` 从本机帮助文件取内容，**没有帮助文件时只显示基本信息**；**从 PowerShell 3.0 起 Windows 自带模块不含帮助文件**，需 `Update-Help` 下载或用 `-Online` [C-6]
  - 3.4.2 `-Detailed` / `-Full` / `-Examples` / `-Parameter` **只在装了帮助文件时有效，且对 `about_` 概念文章无效**；`-Online` 打开浏览器版，**不能在远程会话中使用** [C-6]
  - 3.4.3 概念文章名（如 `about_Execution_Policies`）**必须以英语输入**，即使是非英语版 PowerShell；`Get-Help about_*` 列出全部 [C-6]
  - 3.4.4 `Update-Help` 的硬限制：无 `-Force` 时**每 24 小时只运行一次**；每模块下载上限 **1 GB** 未压缩内容；官方说明"每天一次"的限制正是为了让用户能安全地把它写进配置文件 [C-7]
  - 3.4.5 `Update-Help` 权限按版本不同：**6.0 及更低需管理员；6.1+ 的 `-Scope` 默认 `CurrentUser`**，但更新 `$PSHOME\Modules` 中的模块仍需"以管理员身份运行" [C-7]
  - 3.4.6 `en-US` 帮助文件始终发布；系统区域为 en-GB 等不受支持语言时报 `The specified culture is not supported`，需显式 `Update-Help -UICulture en-US` [C-7]
  - 降维：把"需要 Administrators 组成员身份"改成"只有装在系统目录里的那部分帮助需要管理员；你自己装的模块，普通账户就能更新"（方向 C 第 5 节最后一行）
  - **核心易错点（Callout 预留）**：
    - `[!warning]` 中文社区常建议"把 `Update-Help` 写进 `$PROFILE` 自动更新"，但都不提**每 24 小时只运行一次**与**每模块 1 GB** 上限（方向 C 矛盾 5）

- **3.5 Provider 与 PSDrive：把一切变成"盘"**（概念 + 命令，中）
  - 3.5.1 Provider 把专用数据存储以**驱动器形式**暴露，用法同硬盘；内置 8 个：Alias / Certificate / Environment / FileSystem / Function / Registry / Variable / WSMan；其中 **Certificate、Registry、WSMan 仅在 Windows 平台可用** [C-5]
  - 3.5.2 同一批 cmdlet 可作用于任何 Provider：`New-Item` 在 `C:` 建文件、在注册表建键、在 `Alias:` 建别名，用法相同；分层数据用 `drive:\location\child-location` 导航，含空格须加双引号；`.` 与 `..` 分别表示当前与上层 [C-5][C-15]
  - 3.5.3 FileSystem 是唯一有默认 Home 的 Provider（值等于 `$HOME`），`~` 表示 Home；没有 Home 的 Provider 用 `~` 会报错 [C-5]
  - 3.5.4 **动态参数**只在配合特定 Provider 时才出现（如 `Cert:` 给 `Get-ChildItem` 增加 `-CodeSigningCert`）；用 `Get-Help <provider-name>` 查该 Provider 的动态参数 [C-5]
  - 3.5.5 `Get-PSDrive` 能看到 `New-PSDrive` 创建的会话级驱动器，而 `net use`、`[System.IO.DriveInfo]::GetDrives()`、`Get-CimInstance` **都看不到** [C-13]
  - 降维："Provider 是 .NET 程序"只讲效果——"PowerShell 把注册表、证书、环境变量都做成了'盘'，用同一套 `dir` / `cd` 就能逛"；"动态参数"改成"有些参数只有在特定盘符下才出现，比如在 `Cert:` 盘里 `Get-ChildItem` 才会多出 `-CodeSigningCert`"（方向 C 第 5 节）

- **3.6 执行策略：它防的是手滑，不是防坏人**（概念 + 命令，中）
  - 3.6.1 **执行策略不是安全边界**，而是"深层防御"：用户无法运行脚本时，直接在命令行粘贴脚本内容即可绕过 [C-3]
  - 3.6.2 `Restricted` 允许单个命令但**阻止所有脚本文件**（`.ps1` / `.ps1xml` / `.psm1` / 配置文件）[C-3]
  - 3.6.3 从 Internet 下载的脚本会被标记"来自 Internet"，`RemoteSigned` 下不运行未签名者，可用 `Unblock-File` 解除；但 `curl.exe` / `Invoke-RestMethod` / `Invoke-WebRequest` 下载的文件**不会**带此标记 [C-3]
  - 3.6.4 默认策略 `Default` = 客户端与服务器均为 **RemoteSigned**；若所有作用域都是 `Undefined`，则客户端有效策略是 **Restricted**、服务器是 **RemoteSigned** [C-3]
  - 3.6.5 作用域优先级：`Process`（最高，存在 `$Env:PSExecutionPolicyPreference`，**不写注册表**）> `CurrentUser`（存用户 `powershell.config.json`）> `LocalMachine`；**组策略设置覆盖所有作用域** [C-3]
  - 3.6.6 `Get-ExecutionPolicy -List` 按优先级列出各作用域实际值；`Set-ExecutionPolicy -Scope CurrentUser` **不需要管理员**，改 `LocalMachine` 需要管理员 [C-3]
  - 命令清单：`Get-ExecutionPolicy -List`、`Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`、`-Scope Process`、`pwsh.exe -ExecutionPolicy RemoteSigned`、`Unblock-File`、`Set-ExecutionPolicy Undefined -Scope CurrentUser`
  - 降维：作用域三级不要一次抛出——**先只讲 `CurrentUser`**（"只影响我自己、不用管理员"），`LocalMachine` / 组策略放到"公司电脑改了不生效怎么办"的排错小节；"深层防御"改成"它防的是手滑，不是防坏人：改它主要是避免自己误运行来路不明的脚本，所以别为了省事关掉它"（方向 C 第 5 节）
  - **核心易错点（Callout 预留）**：
    - `[!warning]` **执行策略不是安全边界**：社区普遍把它当安全方案，官方明说不是——按官方口径写为"**防误运行的便利机制**"【跨方向冲突 #7；方向 C 矛盾 3】
    - `[!warning]` **默认与推荐都是 `RemoteSigned`**，不是 `AllSigned`；`AllSigned` 只作为"可选更严档位"提及【跨方向冲突 #9；方向 C 矛盾 7】
    - `[!example]` C 级现象开场：打开 PowerShell 即报"无法加载文件 …\profile.ps1，因为在此系统上禁止运行脚本"（`PSSecurityException`）——**原理回指 [C-3]**（`Restricted` 阻止 `.ps1` 配置文件；`Undefined` 时客户端有效策略为 `Restricted`）[C-17]（现象）+ [C-3]（原理）
    - `[!note]` UNC 路径在 `RemoteSigned` 下的限制**只在特定系统成立**，不写成通用结论（方向 C 缺口 7）；Server Core 的 `AuthorizationManager check failed` 刻意剔除（缺口 6）

- **3.7 编码与中文乱码：三条独立通道**（概念 + 命令，长）
  - 3.7.1 前提事实：Windows 支持 Unicode 与传统字符集，PowerShell 默认使用 Unicode，多个 cmdlet 有 `-Encoding` 参数 [C-8]
  - 3.7.2 **通道一 · 脚本源码编码**：在 Windows PowerShell 中除 `UTF7` 外任何 Unicode 编码**总是创建 BOM**；PowerShell（v6+）**默认为所有文本输出 `utf8NoBOM`** [C-8]
  - 3.7.3 **通道二 · `-Encoding` 参数与 cmdlet 默认值**：5.1 的"默认编码"**不一致**——`Out-File` 与 `>` / `>>` 创建 **UTF-16LE**；`Export-Csv` 创建 **ASCII**；`New-Item -Type File -Value` 创建**不带 BOM 的 UTF-8**；`Add-Content` / `Set-Content` 在目标文件为空或不存在时用 `Default`（系统 ANSI 旧代码页）[C-8]
  - 3.7.4 **通道三 · 控制台与对外部程序编码**：`$OutputEncoding` **只影响 PowerShell 与外部程序通信，不影响重定向运算符和 cmdlet 写文件的编码**；从 5.1 起 `>` / `>>` 内部调用 `Out-File`，所以 `$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'` 能同时管住写文件和重定向 [C-8]
  - 3.7.5 BOM 取舍双向，按文件类型分开：**5.1 的 `$PROFILE` 用 UTF-8 BOM**（含非 ASCII 字符的脚本在 5.1 下需要 BOM，否则被误读为过时 ANSI 代码页）；**纯数据文件用 UTF-8 无 BOM**（跨平台工具链建议避免 BOM）[C-8]
  - 3.7.6 诊断与落盘命令清单：`chcp`、`[Console]::OutputEncoding`、`[Console]::InputEncoding`、`$OutputEncoding`、`Out-File -Encoding utf8`、`$PSDefaultParameterValues`、`Test-Path $PROFILE` → `New-Item -Path $PROFILE -ItemType File -Force` → `notepad $PROFILE` [C-8]
  - 降维：**BOM** 用现象讲——"文件开头多 3 个看不见的字节，用来告诉程序'我是 UTF-8'"；`$PSDefaultParameterValues` / `$OutputEncoding` 分成两句话——"`$OutputEncoding` 管'和外部程序说话'，`-Encoding` / `$PSDefaultParameterValues` 管'存到文件'，两者互不覆盖"（方向 C 第 5 节）
  - **核心易错点（Callout 预留）**：
    - `[!warning]` **编码不写"改一个设置就好"**，必须写成**三条独立通道**（脚本源码编码 / `-Encoding` 参数 / 控制台与对外程序编码）【跨方向冲突 #8；方向 C 矛盾 1】
    - `[!warning]` "5.1 默认是 XX 编码"这句话**不存在**，必须按 cmdlet 分别判断 [C-8]
    - `[!warning]` BOM 的两条官方建议方向相反，按"**脚本源码 vs 数据文件**"分开表述，否则读者会得出互相打架的结论（方向 C 矛盾 2）
    - `[!example]` C 级现象：中文显示成 `UTF-8 缂栫爜宸查厤缃畬鎴愶紒` 一类字符（社区归因"代码页 936 与 UTF-8 不一致"）——**原理回指 [C-8]**；社区方案在"写文件正常但调用外部程序仍乱码"时会失效（方向 C 矛盾 6）[C-18]（现象）+ [C-8]（原理）
    - `[!warning]` 中文目录下第三方 native 组件报 `Error 3: The system cannot find the path specified.` **只有 C 级第三方 issue、无 A 级原理**，只能写成"某些第三方程序的已知限制"，**不解释成 PowerShell 的原理** [C-19]（现象，方向 C 缺口 2）
    - `[!warning]` **中文用户名导致 `PSModulePath` 异常不写进正文**（无任何可用来源，P2 已拍定；可用的相邻 A 级事实只有"Documents 位置会被重定向和 OneDrive 改变" [C-14]）

- **3.8 PowerShell 5.1 与 7：两个版本可以一起装**（概念，中）
  - 3.8.1 两版本**并行安装并行运行**，各有独立的安装路径、可执行名、`PSModulePath`、配置文件、事件日志；5.1 是 `powershell.exe`（`$Env:windir\System32\WindowsPowerShell\v1.0`），6/7 是 `pwsh.exe`（`$Env:ProgramFiles\PowerShell\7`）[C-4]
  - 3.8.2 `PSModulePath` 差异：PowerShell 7 的 `$Env:PSModulePath` **额外包含 Windows PowerShell 路径**以支持模块自动加载；5.1 默认是 `$HOME\Documents\WindowsPowerShell\Modules` 与 `$Env:ProgramFiles\WindowsPowerShell\Modules` [C-4][C-14]
  - 3.8.3 **配置文件位置改名**：5.1 为 `$HOME\Documents\WindowsPowerShell`，7 为 `$HOME\Documents\PowerShell`；用 `$PROFILE | Select-Object *Host* | Format-List` 查看实际路径 [C-4]
  - 3.8.4 运行时基础不同：7.4 基于 **.NET 8.0**，5.1 基于 **.NET Framework 4.x**；ISE **仅支持 5.1、无更新计划**，官方推荐 VS Code PowerShell 扩展 [C-4]
  - 3.8.5 跑只支持 5.1 的老模块用兼容开关 `Import-Module -UseWindowsPowerShell`（替代讲 .NET 版本号）[C-4]
  - **核心易错点（Callout 预留）**：
    - `[!warning]` **四项最易出错的行为差异必须全程并行标注**：默认编码、配置文件路径、`PSModulePath`、`Update-Help` 权限 [C-4][C-7][C-8]
    - `[!warning]` 官方称迁移"简单、快速且安全"，但同页也说明 ISE 不再更新、部分模块需兼容层、.NET 版本差异可能改变脚本行为——对零基础读者降级为"**5.1 与 7 可以共存，所以可以慢慢迁**"（方向 C 矛盾 4）
    - `[!note]` "新手该默认用 7 吗"**本轮无官方倾向来源**，正文不给"就用 7"的结论（方向 C 缺口 8）

- **3.9 一张表看懂 PowerShell / cmd / Bash 的差别**（对照表，短）
  - 3.9.1 十维对照表：管道传的东西、命令名风格、路径分隔符、盘符、变量语法、脚本扩展名、执行前提、默认文本输出编码、配置文件、运行位置 [C-16]
  - 3.9.2 标注方式："本文整理，无官方对照专页；各格依据来自 [C-2]（对象 vs 文本、Verb-Noun）、[C-4]（可执行名、配置文件路径、跨平台、PSModulePath）、[C-5]（Provider 盘符）、[C-8]（默认编码）、[C-3]（执行策略）；其中'变量语法''路径分隔符'两行为间接推论，溯源强度弱于其他行"（方向 C 缺口 3）
  - **核心易错点（Callout 预留）**：
    - `[!warning]` 与 cmd / Bash 的根本差别**不在命令名，而在管道里流动的是对象还是文本** [C-2]

- **本章核心易错点汇总（Callout 预留，逐条落到具体小节）**：见 3.2（管道绑定失败排查、`-InputObject` 差异、字符串不被枚举）、3.4（Update-Help 硬限制）、3.6（执行策略不是安全边界、RemoteSigned 是默认）、3.7（三条编码通道、5.1 默认不统一、BOM 双向、Error 3 无原理、中文用户名不写）、3.8（四项版本差异、"简单迁移"降级）
- **需降维改写（来自方向 C 第 5 节，13 行全部有归属）**：对象而非文本（3.1）、`IEnumerable`（3.2）、ByValue/ByPropertyName（3.2）、无法强制绑定（3.2）、动态参数（3.5）、Provider 是 .NET 程序（3.5）、执行策略不是安全边界（3.6）、作用域优先级（3.6）、runspace 当前目录（3.5 或删）、BOM（3.7）、`$PSDefaultParameterValues` / `$OutputEncoding`（3.7）、.NET 版本号（3.8）、`-Path` 与 `-Recurse`（第 4 章 4.2）、Update-Help 权限（3.4）
- **素材未覆盖、需在文中标注为空白的点**：8 张 cmdlet 页无 `Last updated` 字段（时效不可考，方向 C 缺口 4）；PowerShell 7 当前稳定版本号未确认（缺口 5），全篇版本标注统一写 `7`

---

## 第四章：串联——用 PowerShell 同时操作文件系统与注册表

- **篇幅**：中（3000–4000 字）
- **覆盖要点**：Provider 让两件事变成一件事 → 文件系统常用操作清单 → 注册表常用操作清单 → 三种执行方式对照选型 → 一条端到端的安全示例
- **素材引用**：[C-5][C-9][C-10][C-11][C-12][C-13][C-15]（方向 C 第 2.10 节与第 4.5 节）、[S6][S8][S9][S21][S22]（方向 B 第 2.10 节）、方向 A 第 4 节命令清单
- **代码示例**：有（约 10 个代码块 / 约 35 条命令）
- **对应素材位置**：方向 B 第 2.10 节 + 第 4.5 节；方向 C 第 2.10 节 + 第 4.5 节；素材第 4 节第 2 条（"串联章素材来源"）
- **本章定位**：**命令为主（约 80%）**，概念只做"为什么能统一操作"的衔接

**小节结构**

- **4.1 为什么两件事能变成一件事**（概念，短）
  - 4.1.1 回顾 Provider 模型：FileSystem 与 Registry 是同一套命令体系下的两个"盘" [C-5]
  - 4.1.2 关键区别提示：文件系统里的"东西"是项（文件/目录），注册表里的"值"是**属性**——这是后面所有命令差异的根源 [C-11][C-12]
  - 4.1.3 路径统一写法：`C:\...`、`HKLM:\...`、`Registry::HKEY_LOCAL_MACHINE\...` [C-11]

- **4.2 文件系统常用操作清单**（命令，中）
  - 4.2.1 列目录与看隐藏项：`Get-ChildItem -Path C:\Test`、`-Force`（含隐藏/系统项）；**`-Force` 不会替代安全限制** [C-9]
  - 4.2.2 **官方推荐的递归写法**：**不建议把 `-Path` 与 `-Recurse` 一起用**，改用 `Get-ChildItem -LiteralPath <目录> -Recurse -Filter <模式>` [C-9]
  - 4.2.3 切换位置：`Set-Location` 可切到任何 Provider 路径（`HKLM:\`、`Cert:\`、`Env:\`）；驱动器名不带反斜杠（如 `C:`）表示"恢复到该盘当前目录" [C-10]
  - 4.2.4 位置历史：PowerShell 6.2 起 `Set-Location -Path -` / `+` 可在**最近 20 个位置**中前后导航，`cd -` 是最短写法（**仅 7 可用，5.1 不可用**）[C-10]
  - 4.2.5 新建文件/目录：`New-Item -Path "C:\" -Name "Logfiles" -ItemType "Directory"` [C-15]
  - 4.2.6 驱动器与卷查看：`Get-PSDrive`（含 Provider 驱动器）[C-13]
  - 降维：`-Path` 与 `-Recurse` 的内部机制不解释，直接给结论 + 一条安全写法（方向 C 第 5 节）；runspace/当前目录那句压缩成"在 PowerShell 里 `cd` 只影响 PowerShell 自己，不影响你在脚本里调用的程序"
  - **核心易错点（Callout 预留）**：
    - `[!warning]` `-Path` + `-Recurse` 是官方**不建议**的写法 [C-9]
    - `[!note]` `cd -` / `cd +` **仅 PowerShell 6.2+（含 7）可用**，5.1 会报错 [C-10]

- **4.3 注册表常用操作清单**（命令，中）
  - 4.3.1 **读值**：`Get-ItemProperty -Path HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion -Name ProgramFilesDir`；`Get-ItemPropertyValue`（**PowerShell 5.0 起**）只返回值；`Get-ChildItem -Path HKLM:\HARDWARE -Exclude D*` [C-11][S22][S21]
  - 4.3.2 四个 cmdlet 的分工：`Get-ChildItem` 看**子项**（不显示父键属性）、`Get-Item` 看**键本身及其属性**、`Get-ItemProperty` 看**值**、`Get-ItemPropertyValue` 只取指定属性的值 [S21][S22]
  - 4.3.3 **写值**：`Set-ItemProperty -Path "HKLM:\Software\ContosoCompany" -Name "NoOfEmployees" -Value 823`；`-Type` 默认 `String`（REG_SZ），可选 `ExpandString` / `Binary` / `DWord` / `MultiString` / `QWord` / `Unknown` [C-12][S21]
  - 4.3.4 新建项：`New-Item` 在注册表建键，用法与建目录相同 [C-15]
  - 4.3.5 **删值与删键**：`Remove-ItemProperty` 只删值；`Remove-Item` 在项**包含子项时默认弹确认**，加 `-Recurse` 免提示；`Clear-Item` 清空键的**所有值**但保留键本身 [S21]
  - 4.3.6 路径备用写法：`Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion`（不依赖 `HKLM:` 驱动器）[C-11]
  - 4.3.7 **用 PowerShell 改注册表的安全流程**：先 `reg export` 备份（第 2 章 2.7.3 主路径）→ 读值确认现状 → 改值 → 读值复核 → 需要时 `reg import` 回滚
  - **核心易错点（Callout 预留）**：
    - `[!warning]` 注册表的"值"是键的**属性**而不是项/子项：用 `Get-Item` 或 `Get-ChildItem` **看不到值**，必须用 `Get-ItemProperty` / `Set-ItemProperty` [C-11][C-12]
    - `[!warning]` `Set-ItemProperty` 的 `-Type` **默认为 `String`**，写数字型值必须显式指定 `DWord` / `QWord`，否则类型写错 [S21][C-12]

- **4.4 三种执行方式对照与选型：regedit / reg.exe / PowerShell**（对照 + 概念，短）
  - 4.4.1 官方列举的可修改注册表手段：注册表编辑器（Regedit.exe / Regedt32.exe）、组策略、系统策略、`.reg` 文件、Windows Script Host、WMI（含 Wmic.exe）、控制台工具 Reg.exe [S6]
  - 4.4.2 三者定位：**regedit** 适合"看得见再改"（官方步骤最完整的备份方式）；**reg.exe** 适合可复制的命令与批处理；**PowerShell** 用 `HKLM:` / `HKCU:` 驱动器适合脚本化 [S6][S9][S21]
  - 4.4.3 选型表：是否可视化 / 是否可脚本化 / 备份方式 / 提权要求（第三列按"官方明确写出的"填，其余写"官方未说明"）
  - 4.4.4 官方统一态度：优先用 Windows 用户界面或组策略改系统设置，直接改注册表是最后手段 [S6][S8]

- **4.5 一条端到端示例：改一个值 → 验证 → 回滚**（示例，短）
  - 4.5.1 场景：用 PowerShell 修改一个自定义键的值（不用系统关键键）
  - 4.5.2 完整七步：`reg export` 备份 → `Get-ItemProperty` 读现状 → `Set-ItemProperty` 改值（显式 `-Type`）→ `Get-ItemProperty` 复核 → 说明"改错了怎么办" → `reg import` 回滚 → `Remove-Item` 清理演示键
  - 4.5.3 同一场景的 regedit 与 reg.exe 版本对照（体现三种方式是同一件事的三个入口）
  - **核心易错点（Callout 预留）**：
    - `[!warning]` 示例必须用**自建键**，不得使用系统关键键；这是本章唯一允许出现的注册表修改示例

- **本章核心易错点汇总（Callout 预留）**：见 4.2（`-Path` + `-Recurse`）、4.3（值不是项、`-Type` 默认 String）、4.5（示例只用自建键）
- **需降维改写**：把"值与项的区别"用类比讲清（键像文件夹、值像文件夹上的标签页）；`Registry::` 形式的路径只作为"备用写法"出现，不解释提供程序全名语法
- **本章不写的内容**：`HKCR\*\shell` 通配 verb（无来源）、中文用户名 `PSModulePath`（无来源）、任何注册表优化/清理/加速工具（禁止）

---

## 第五章：总结与速查

- **篇幅**：短（1500–2000 字）
- **覆盖要点**：三张速查表 → 九个跨方向易错点回顾 → "官方未说明"与证据不足清单 → 安全练习建议
- **素材引用**：各方向第 4 节命令清单；素材第 3 节（9 条跨方向冲突）；素材第 5 节高影响表 + 中低影响表
- **代码示例**：无（只做索引，不重复命令块）
- **对应素材位置**：方向 A/B/C 第 4 节与第 7 节；素材第 3、5、6 节

**小节结构**

- **5.1 三张速查表**（索引，中）
  - 5.1.1 文件系统命令表（含环境 / 版本 / 权限三元组）[方向 A 第 4 节]
  - 5.1.2 注册表命令表（regedit / reg.exe / PowerShell 三列对照）[方向 B 第 4 节]
  - 5.1.3 PowerShell 命令表（探索 / 帮助 / 执行策略 / 编码四组）[方向 C 第 4 节]
- **5.2 九个跨方向易错点回顾（一张表）** [素材第 3 节]
  - 5.2.1 系统还原不是回滚主路径（第 2 章 2.7）
  - 5.2.2 按键级备份 vs 整机级备份（第 2 章 2.7）
  - 5.2.3 HKCU 磁盘位置官方两说（第 2 章 2.3）
  - 5.2.4 `Program Files (x86)` 官方自相矛盾（第 1 章 1.4）
  - 5.2.5 `mklink /j` 是"目录联接"不是"目录硬链接"（第 1 章 1.6）
  - 5.2.6 `mklink /F` 不存在（第 1 章 1.6）
  - 5.2.7 执行策略不是安全边界（第 3 章 3.6）
  - 5.2.8 编码没有"单一默认值"，是三条通道（第 3 章 3.7）
  - 5.2.9 默认 `RemoteSigned`，`AllSigned` 只是可选项（第 3 章 3.6）
- **5.3 "官方未说明"与证据不足清单**（提醒，短）
  - 5.3.1 逐条列出本笔记中所有"官方未说明"标记（`mklink /d`、`compact` / `cipher` / `mountvol` / `robocopy`、`reg.exe` 各子命令）
  - 5.3.2 逐条列出"素材未覆盖因此未写"的内容（`LocalLow` 用途、`WinSxS` 不可删、`USRCLASS.DAT`、`RegBack`、环境变量注册表路径、`HKCR\*\shell`、中文用户名 `PSModulePath`、中文路径 `Error 3` 原理）
  - 5.3.3 提醒读者：这些位置不要当成结论使用
- **5.4 接着往下练的建议**（短）
  - 5.4.1 在自建目录与自建注册表键上练，不碰系统关键键
  - 5.4.2 每次改注册表前先导出 `.reg`，练成条件反射
  - 5.4.3 用 `Get-Help` / `Get-Command` / `Get-Member` 自己探索，不依赖记忆

---

## 学习路径说明

### 前置要求

- 会开机、会用文件资源管理器打开文件夹、会复制粘贴路径即可
- 不需要任何编程基础；不需要了解什么是字节、编码、数据库（相关概念都在第 3 章 3.7 现场解释）
- 需要一台 Windows 10 或 Windows 11 电脑；如果只是阅读不想动手，也可以跳过所有命令清单
- 动手前提醒：所有涉及注册表修改的命令都只应作用在**自建的键**上，不要拿系统关键键做实验

### 学完能做什么

- 看懂一个完整路径里的每一段是什么意思，知道 `C:tmp.txt` 与 `C:\tmp.txt` 为什么不是同一个文件，知道 `\\?\` 是干什么的
- 说清楚 `C:\Windows`、`Program Files (x86)`、`AppData\Roaming`、`ProgramData`、`Users\Public` 各放什么，以及哪些是"每个用户一份"、哪些是"全机器共用一份"
- 用 `dir` / `attrib` / `icacls` / `robocopy` 完成"看内容 → 看属性 → 看权限 → 安全复制"一条龙，并知道 robocopy 的 `/mir` 和默认重试为什么危险
- 说清注册表"树 / 键 / 子项 / 值"四个词，认识五个根键，知道 HKCR 不是真实位置
- 独立完成"导出 `.reg` 备份 → 修改 → 复核 → 需要时导入回滚"这套流程，并知道系统还原不是回滚主路径
- 用 PowerShell 的对象管道、`Get-ChildItem` / `Get-ItemProperty` / `Set-ItemProperty` 同时操作文件系统与注册表
- 遇到"无法加载文件，因为在此系统上禁止运行脚本"和中文乱码时，知道问题出在哪一层，而不是盲改设置
- 分清 PowerShell 5.1 与 7 的四处关键行为差异（默认编码、配置文件路径、`PSModulePath`、`Update-Help` 权限）

### 建议学习顺序

| 顺序 | 章节 | 预计字数 | 建议用时 | 说明 |
|---|---|---|---|---|
| 1 | 第零章 导读 | 1000–1500 | 5 分钟 | 建立"三层关系"的整体印象，读完即可 |
| 2 | 第一章 文件系统 | 6500–8000 | 60–90 分钟 | 概念最多的一章；1.2 命名与路径规则建议反复读 |
| 3 | 第二章 注册表 | 6500–8000 | 60–90 分钟 | **2.7 备份与回滚必须完整读完再动手**；2.8 命令部分可先只看 query |
| 4 | 第三章 PowerShell | 6500–8000 | 60–90 分钟 | 3.1–3.2 是全书最难的两个概念，读不懂可先跳到 3.6 / 3.7 看两条最实用的排错 |
| 5 | 第四章 串联 | 3000–4000 | 30–45 分钟 | 建议边读边在自建目录与自建键上跑命令 |
| 6 | 第五章 总结与速查 | 1500–2000 | 20 分钟 | 可以反复回来查表 |

**灵活读法**：如果最急迫的问题是"脚本跑不起来"或"中文乱码"，可以先读 3.6 与 3.7，再回头补 3.1–3.5。如果最急迫的是"想清理开机自启项"，先读 2.7（备份）再读 2.9（自启路径），不要跳读。
