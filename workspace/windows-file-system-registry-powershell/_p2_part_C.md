# P2 深度素材 · 方向 C — Windows PowerShell

## 1. 来源表

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

## 2. 论断 / 来源映射

版本标注含义：`5.1` = Windows PowerShell（`powershell.exe`）；`7` = PowerShell 7（`pwsh.exe`）。

### 2.1 核心设计理念：对象而非文本

- PowerShell 与其他 shell 的根本区别是**接受并返回 .NET 对象而不是文本**，因此管道连接更省事 → [C-2]（5.1 / 7）
- 管道是由管道操作符 `|`（ASCII 124）连接的一系列命令，每个运算符把上一条命令的结果发给下一条，按从左到右处理 → [C-1]（5.1 / 7）
- 因为管道传的是进程对象，`Get-Process notepad | Stop-Process` 中 `Stop-Process` 无需 `-Name` / `-ID`；另注意 PowerShell 的"成功流 / 错误流"类似 stdout / stderr，但 **stdin 并未接入 PowerShell 管道** → [C-1]（5.1 / 7）

### 2.2 管道参数绑定与"一次性处理"（易错核心）

- 接收端 cmdlet 必须有"接受管道输入"的参数；用 `Get-Help <cmdlet> -Full` 或 `-Parameter *` 才能查到是哪个参数、按什么方式接收 → [C-1]（5.1 / 7）
- 接收方式有两种：**ByValue**（值可转换到目标 .NET 类型）与 **ByPropertyName**（输入对象有同名属性）；绑定成功需同时满足"参数接受管道输入 + 类型匹配或可转换 + 该参数未在命令中显式使用"，且**无法强制 PowerShell 绑定到特定参数**，绑不上命令就失败 → [C-1]（5.1 / 7）
- 关键区别：管道**一次发送一个对象**，用 `-InputObject` 参数则把集合当**单个数组对象**发送；官方原话是"这种细微差异具有重大后果"，例如 `Get-Process | Get-Member` 显示 `System.Diagnostics.Process`，而 `Get-Member -InputObject (Get-Process)` 显示 `System.Object[]` → [C-1]（5.1 / 7）
- 管道执行时会自动枚举实现 `IEnumerable` 的类型，但有例外：**哈希表需调用 `GetEnumerator()`**，且 **`System.String` 虽实现 `IEnumerable` 却不会被枚举** → [C-1]（5.1 / 7）

### 2.3 发现 PowerShell：命名约定与探索命令

- PowerShell 命令称为 cmdlet（读作"命令莱特"），名字由 **Verb-Noun** 组成（如 `Get-Process`），谓词应取自 `Get-Verb` 返回的标准动词表 → [C-2]（5.1 / 7）
- 四个"自举"命令足以发现几乎所有内容：`Get-Verb`（合法动词）、`Get-Command`（装了哪些命令，支持 `-Name` / `-Verb` / `-Noun` / `-ParameterType` 过滤）、`Get-Member`（对象有哪些属性和方法）、`Get-Help`（命令怎么用） → [C-2]（5.1 / 7）

### 2.4 帮助系统（Get-Help / Update-Help / Get-Command / Get-Member 分工）

- 三者定位不同：`Get-Command` 回答"有哪些命令"、`Get-Member` 回答"这个对象有什么"、`Get-Help` 回答"这个命令怎么用、参数是什么" → [C-2] + [C-6]（5.1 / 7）
- `Get-Help` 从本机帮助文件取内容，**没有帮助文件时只显示基本信息**；从 PowerShell 3.0 起 Windows 自带模块**不含**帮助文件，需用 `Update-Help` 下载或改用 `-Online` → [C-6]（5.1 / 7）
- `-Detailed` / `-Full` / `-Examples` / `-Parameter` **仅在计算机安装了帮助文件时有效，且对 `about_` 概念文章无效**；`-Online` 在浏览器中打开帮助，**不能在远程会话中使用** → [C-6]（5.1 / 7）
- 概念文章名（如 `about_Objects`）**必须以英语输入**，即使是非英语版 PowerShell；`Get-Help about_*` 列出全部概念文章 → [C-6]（5.1 / 7）
- `Update-Help` 无 `-Force` 时**每 24 小时只运行一次**，每个模块下载上限 **1 GB** 未压缩内容；官方说明每天一次的限制正是为了让用户能安全地把它写进配置文件 → [C-7]（5.1 / 7）
- `Update-Help` 权限按版本不同：**PowerShell 6.0 及更低版本需要管理员权限；6.1 及更高版本 `-Scope` 默认 `CurrentUser`**，但更新 `$PSHOME\Modules` 中的模块仍需"以管理员身份运行" → [C-7]（5.1 与 7 差异）
- **en-US 帮助文件始终发布**；系统区域为 en-GB 等不受支持的语言时会报 `The specified culture is not supported`，需显式 `Update-Help -UICulture en-US` → [C-7]（5.1 / 7）

### 2.5 执行策略（"禁止运行脚本"的官方来源）

- 执行策略**不是安全边界**，而是"深层防御"：用户无法运行脚本时，直接在命令行粘贴脚本内容即可绕过 → [C-3]（5.1 / 7）
- `Restricted` 允许单个命令但**阻止所有脚本文件**，包括 `.ps1xml`、`.psm1` 和 PowerShell 配置文件（`.ps1`）；从 Internet 下载的脚本会被标记"来自 Internet"，`RemoteSigned` 下不运行未签名者，可用 `Unblock-File` 解除，但 `curl.exe` / `Invoke-RestMethod` / `Invoke-WebRequest` 下载的文件**不会**带此标记 → [C-3]（5.1 / 7）
- 默认策略 `Default` = 客户端与服务器均为 **RemoteSigned**；若所有作用域都是 `Undefined`，则客户端有效策略是 **Restricted**、服务器是 **RemoteSigned** → [C-3]（5.1 / 7）
- 作用域优先级：`Process`（最高，存 `$Env:PSExecutionPolicyPreference`，**不写注册表**）> `CurrentUser`（存用户 `powershell.config.json`）> `LocalMachine`（存 `$PSHOME/powershell.config.json`）；**组策略设置覆盖所有作用域** → [C-3]（5.1 / 7）
- `Get-ExecutionPolicy -List` 按优先级列出各作用域实际值；`Set-ExecutionPolicy -Scope CurrentUser` **不需要管理员**，改 `LocalMachine` 需要管理员 → [C-3]（5.1 / 7）

### 2.6 Provider 与 PSDrive（"一切皆盘符"的统一模型）

- Provider 把专用数据存储以**驱动器形式**暴露，路径与使用方式同硬盘；内置 8 个：Alias / Certificate / Environment / FileSystem / Function / Registry / Variable / WSMan。其中**Certificate、Registry、WSMan 仅在 Windows 平台可用** → [C-5]（5.1 / 7）
- 同一批 cmdlet 可作用于任何 Provider 的数据：`New-Item` 在 `C:` 建文件、在注册表建键、在 `Alias:` 建别名，用法相同；分层数据用 `drive:\location\child-location` 导航，含空格须用双引号，`.` 与 `..` 分别表示当前与上层 → [C-5] + [C-15]（5.1 / 7）
- FileSystem 是唯一有默认 Home 的 Provider（值等于 `$HOME`），`~` 表示 Home；没有 Home 的 Provider 用 `~` 会报错 → [C-5]（5.1 / 7）
- 动态参数只在配合特定 Provider 时才出现，例如 `Cert:` 给 `Get-Item` / `Get-ChildItem` 增加 `CodeSigningCert`；用 `Get-Help <provider-name>` 查该 Provider 的动态参数 → [C-5]（5.1 / 7）
- `Get-PSDrive` 能看到 `New-PSDrive` 创建的会话级驱动器，而 `net use`、`[System.IO.DriveInfo]::GetDrives()`、`Get-CimInstance` **都看不到** → [C-13]（5.1 / 7）

### 2.7 Windows PowerShell 5.1 与 PowerShell 7 的并行关系

- 两个版本**并行安装并行运行**，各有独立的安装路径、可执行文件名、`PSModulePath`、配置文件、事件日志；5.1 是 `powershell.exe`（`$Env:windir\System32\WindowsPowerShell\v1.0`），6/7 是 `pwsh.exe`（`$Env:ProgramFiles\PowerShell\7`） → [C-4]（5.1 / 7 并存）
- PowerShell 7 的 `$Env:PSModulePath` **额外包含 Windows PowerShell 路径**（`$HOME\Documents\WindowsPowerShell\Modules` 等）以支持模块自动加载；5.1 的默认模块路径是 `$HOME\Documents\WindowsPowerShell\Modules` 与 `$Env:ProgramFiles\WindowsPowerShell\Modules` → [C-4] + [C-14]（两版本差异）
- 配置文件位置改名：5.1 为 `$HOME\Documents\WindowsPowerShell`，7 为 `$HOME\Documents\PowerShell`；用 `$PROFILE | Select-Object *Host* | Format-List` 查看实际路径 → [C-4]（两版本差异）
- PowerShell 7.4 基于 **.NET 8.0**，5.1 基于 **.NET Framework 4.x**，版本差异可能影响脚本行为（尤其是直接调用 .NET 方法时）；ISE 仅支持 5.1、无更新计划，官方推荐 VS Code PowerShell 扩展 → [C-4]（两版本差异）

### 2.8 编码与中文乱码（A 级原理）

- Windows 支持 Unicode 与传统字符集，**PowerShell 默认使用 Unicode**，但多个 cmdlet 有 `-Encoding` 参数可指定其他字符集 → [C-8]（5.1 / 7）
- 在 Windows PowerShell 中**除 `UTF7` 外任何 Unicode 编码总是创建 BOM**；PowerShell（v6 及以上）**默认为所有文本输出 `utf8NoBOM`** → [C-8]（5.1 与 7 的关键差异）
- Windows PowerShell 中"默认编码"其实**不一致**：`Out-File` 与 `>` / `>>` 创建 **UTF-16LE**；`Export-Csv` 创建 **ASCII**；`New-Item -Type File -Value` 创建**不带 BOM 的 UTF-8**；`Add-Content` / `Set-Content` 在目标文件为空或不存在时用 `Default`（系统 ANSI 旧代码页） → [C-8]（仅 5.1）
- 自动变量 `$OutputEncoding` **只影响 PowerShell 与外部程序通信的编码，不影响重定向运算符和 cmdlet 写文件的编码**；从 PowerShell 5.1 起 `>` 和 `>>` 内部调用 `Out-File`，所以 `$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'` 能同时管住写文件和重定向 → [C-8]（5.1 起 / 7）
- BOM 取舍双向：官方一处建议"为避免 UTF-8 文件中使用 BOM"（Unix 工具不支持），另一处指出**含非 ASCII 字符的脚本在 5.1 下需要 BOM，否则会被误读为过时的 ANSI 代码页** → [C-8]（5.1 与 7 建议相反）

### 2.9 PowerShell 与 cmd / Bash 的对照

- 与 cmd / Bash 的根本差别不在命令名，而在**管道里流动的是对象还是文本**，以及**命令名遵循 Verb-Noun 而非简写**；逐项对照见第 4 节表 → [C-16]（5.1 / 7）

### 2.10 文件系统与注册表常用 Cmdlet（衔接方向 A / B）

- `Get-ChildItem` 是通用列项命令（别名 `dir`、`gci`），**默认不显示隐藏项**，需 `-Force`；`-Force` **不会替代安全限制**。官方明确**不建议把 `-Path` 与 `-Recurse` 一起用**，应改用 `-LiteralPath` 指定目标目录 + `-Filter` / `-Include` 指定匹配模式 → [C-9]（5.1 / 7）
- 注册表"值"是键的**属性**而不是项/子项：用 `Get-Item` 或 `Get-ChildItem` 看不到值，必须用 `Get-ItemProperty` / `Set-ItemProperty`；也可用 `Registry::HKEY_LOCAL_MACHINE\...` 形式绕开 `HKLM:` 驱动器 → [C-11] + [C-12]（5.1 / 7）
- `Set-Location` 可切换到任何 Provider 路径（`HKLM:\`、`Cert:\`、`Env:\`）；驱动器名不带反斜杠（如 `C:`）时表示"恢复到该盘当前目录" → [C-10]（5.1 / 7）
- PowerShell 6.2 起 `Set-Location -Path -` / `+` 可在**最近 20 个位置**的历史中前后导航，`cd -` 是最短写法；官方同时备注 PowerShell 的"当前目录"是**每个 runspace 独立**的，与 `[System.Environment]::CurrentDirectory` 不同 → [C-10]（前者仅 7 / 6.2 起）

### 2.11 社区经验型现象（仅现象，原理必须回溯 A 级）

- 现象：打开 PowerShell 即报 `无法加载文件 C:\Users\<用户>\Documents\WindowsPowerShell\profile.ps1，因为在此系统上禁止运行脚本`，并伴随 `CategoryInfo: SecurityError ... PSSecurityException` —— 原理对应 `Restricted` 阻止 `.ps1` 配置文件、以及 `Undefined` 时客户端有效策略为 `Restricted` → [C-17]（现象）+ [C-3]（原理）**C 级 · 经验型**
- 现象：正常中文被显示成 `UTF-8 缂栫爜宸查厤缃畬鎴愶紒` 一类字符，社区归因为"控制台代码页 936（GBK）与脚本文件 UTF-8 不一致" —— 原理对应 5.1 的 `Out-File` UTF-16LE 默认与 `-Encoding` 参数 → [C-18]（现象）+ [C-8]（原理）**C 级 · 经验型**
- 现象：中文目录会让第三方 native 组件报 `Error 3: The system cannot find the path specified.`，而路径在资源管理器中可见 —— 官方 A 级来源本轮未覆盖 native API 层，**原理未落到 A 级** → [C-19] **C 级 · 经验型**（详见第 6 节）

---

## 3. 矛盾与冲突

1. **"Windows PowerShell 默认编码"不存在单一答案。** C-8 同一页先说"通常，Windows PowerShell 默认使用 Unicode UTF-16LE 编码"，紧接着又说"Windows PowerShell 中 cmdlet 使用的默认编码不一致"，同页列举的 `Out-File`（UTF-16LE）、`Export-Csv`（ASCII）、`Add-Content` 空文件（ANSI Default）互相矛盾。写作时必须把结论限定为"**按 cmdlet 分别判断**"，不能写成"5.1 默认是 XX 编码"。

2. **BOM 的建议方向相反，取决于文件类型。** C-8 一处说"为获得最佳整体兼容性，**避免**在 UTF-8 文件中使用 BOM"（针对跨平台工具链），另一处说"如果需要在脚本中使用非 Ascii 字符，**请使用 BOM** 将它们另存为 UTF-8"（针对 5.1 读 `.ps1`）。C-18（C 级）只主张后者。两者不是真冲突，但必须按"脚本源码 vs 数据文件"分开表述，否则会让零基础读者得出互相打架的结论。

3. **C 级文章把执行策略当成"安全方案"，A 级明说它不是安全边界。** C-17 推荐 `AllSigned` 并称"提高安全性"，C-18 相关段落未提任何限制；而 C-3 明确"执行策略不是安全边界，它是深层防御……可以在命令行中键入脚本内容，从而轻松绕过策略"。改写时必须保留 C-3 的限定语。

4. **"迁移简单、快速且安全"是官方立场，但存在未覆盖的落差。** C-4 开头称迁移"简单、快速且安全"，同页又说明 ISE 不再更新、部分模块需要 `Import-Module -UseWindowsPowerShell` 兼容层、.NET 版本差异可能改变脚本行为。对零基础读者，"简单"应降级为"5.1 与 7 可以共存，所以可以慢慢迁"。

5. **C 级文章普遍漏掉 `Update-Help` 的硬限制。** 中文社区常见建议是"把 `Update-Help` 写进 `$PROFILE` 自动更新"，但都没提"每 24 小时只运行一次"和"每模块 1 GB"上限（C-7 明确列出，且说明每天一次限制正是为了让用户能安全地把它放进配置文件）。不是冲突，而是 C 级来源不完整。

6. **编码问题的归因层次不同。** C-18 把中文乱码全部归因于"代码页 936 vs UTF-8 不一致"，C-8 则指出还涉及 `$OutputEncoding`（对外部程序）与 cmdlet `-Encoding`（对文件）两条**互不相干**的通道。C-18 的方案在"写文件正常但调用外部程序仍乱码"时会失效。

7. **社区与官方对"该用哪个策略"的默认推荐不一致。** C-17 把 `AllSigned` 列为"建议"、`RemoteSigned` 列为"折中方案"；C-3 明确说 Windows 的默认策略（`Default`）就是 **RemoteSigned**。以 A 级为准，正文应把 RemoteSigned 写成默认与推荐项。

---

## 4. 可操作指引

以下命令均已标注适用版本。`5.1` = `powershell.exe`，`7` = `pwsh.exe`。

### 4.1 认识环境（先跑这几条）

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

### 4.2 帮助系统（推荐的标准流程）

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

### 4.3 执行策略（"禁止运行脚本"的标准解法）

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

### 4.4 编码与中文（5.1 必做，7 可选）

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

### 4.5 文件系统与注册表常用操作（衔接方向 A / B）

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

### 4.6 对照表：PowerShell vs cmd vs Bash（本文整理，来源见 C-2 / C-4）

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

## 5. 需要降维改写的内容

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

## 6. 未解决问题与缺口

1. **中文用户名导致模块/配置文件路径异常，未落到任何可追溯来源。** 本轮尝试的三个中文社区来源全部抓取失败：知乎执行策略文（HTTP 403 反爬）、CSDN 中文用户名 conda 文（`minimal_text` 反爬）、cnblogs 编码文（返回"用户中心"空页）。因此"中文用户名导致 `PSModulePath` 乱码"只能列为待验证现象，**不要写进正文**。可用的 A 级相邻事实只有 [C-14]：Documents 文件夹位置会被文件夹重定向和 OneDrive 改变，官方给的验证命令是 `[Environment]::GetFolderPath('MyDocuments')`；以及 [C-4] 给出的两版本 `$Env:PSModulePath` 默认值清单。

2. **中文路径下 native 组件报 `Error 3: The system cannot find the path specified.` 缺 A 级原理。** 目前唯一来源 [C-19] 是第三方项目（GitNexus）的 issue，属 C 级且非 PowerShell 官方内容。若正文要写这条，必须先补 PowerShell 官方关于本机命令参数传递/编码的页面（如 `about_Parsing`、`PSNativeCommandArgumentPassing`），或降级为"某些第三方程序的已知限制"。

3. **无官方 PowerShell vs cmd / Bash 对照专页。** 已按任务要求以 [C-16] 自行归纳，逐格依据均能回溯到 A 级来源；但"变量语法""路径分隔符"两行来自 [C-2] 的间接推论而非官方成文对照，溯源强度弱于其他行。

4. **多张 cmdlet 参考页未标注更新时间。** [C-6] [C-7] [C-9] [C-10] [C-11] [C-12] [C-13] [C-15] 抓取结果中没有 `Last updated on` 字段，来源表的"页面日期"只能记"未标注"。若上游需要时效性声明，需改抓 `?view=powershell-7.6` 或英文页确认。

5. **PowerShell 7 的当前稳定版本号未确认。** [C-4] 只说明"PowerShell 7.4 基于 .NET 8.0"，未给出撰写时点的最新版本；来源表中的版本标注因此统一写作 `7` 而非具体小版本。

6. **执行策略在 Windows Server Core / Nano Server 上的 `AuthorizationManager check failed` 未纳入第 2 节。** [C-3] 有此专节（该场景依赖 `explorer.exe` 提供的区域检查 API，Server Core 上不存在），但对零基础读者属极边缘场景，已刻意剔除；若正文需要"企业服务器"章节可从 C-3 补回。

7. **`about_Execution_Policies` 中"UNC 路径不允许在 RemoteSigned 下运行"这条只在特定系统成立**（官方原文："在无法将通用命名约定（UNC）路径与 Internet 路径区分开来的系统上"），条件依赖平台，不建议对零基础读者写成通用结论。

8. **"7 与 5.1 并存"对新手实际意味着装哪个、用哪个，本轮来源未给官方倾向。** [C-4] 只说两者可以并行、迁移简单，未明确建议新手默认用哪个。正文若要给"就用 7"的结论，需要额外来源支撑（如 PowerShell 支持生命周期页）。

---

## 7. 下游交接摘要

- 主线骨架：**对象而不是文本 → 管道一次传一个对象 → 参数绑定决定谁能接住 → Provider 把一切变成盘符 → 统一用 Get-ChildItem / Get-ItemProperty / Set-Location 操作**；这条链能把 PowerShell 与 cmd/Bash 的区别一次讲透（C-1、C-2、C-5、C-16）。
- 新手三件套必须先教：`Get-Command` 找命令、`Get-Help` 看用法、`Get-Member` 看对象——并说清三者回答的是不同问题（C-2、C-6）。
- 两个版本必须全程并行标注：`powershell.exe`（5.1）与 `pwsh.exe`（7）可共存，但**默认编码、配置文件路径、PSModulePath、Update-Help 权限**四项行为不同，是本方向最易出错的地方（C-4、C-7、C-8）。
- 最大的两个实操坑都有 A 级原理可依：**"禁止运行脚本"= 执行策略**（`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`，且强调它不是安全边界）；**中文乱码 = 5.1 各 cmdlet 默认编码不一致**（改法是用 `-Encoding` 与 `$PSDefaultParameterValues`，不是只改 `chcp`）（C-3、C-8）。
- 有 3 条 C 级现象可作"你是不是也遇到这个"的开场素材，但只能写现象、原理必须回到 A 级；中文用户名路径与中文路径 native 报错两条**证据不足，本轮不建议写入正文**（C-17、C-18、C-19）。
