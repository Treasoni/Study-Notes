---
url: "https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/robocopy"
title: "Robocopy | Microsoft Learn"
scraped_at: 2026-09-10T15:41:26+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/robocopy) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/robocopy)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# robocopy
  * 适用于: ✅ [Windows Server 2025](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2022](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2019](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2016](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows 11](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Windows 10](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Azure Local 2311.2 and later](https://learn.microsoft.com/azure/azure-local/release-information-23h2)


将文件数据从一个位置复制到另一个位置。
## Syntax

```
robocopy <source> <destination> [<file>[ ...]] [<options>]

```

例如，若要将名为 _yearly-report.mov_ 的文件从 _c：\reports_ 复制到文件共享 _\\\marketing\videos_ ，同时启用多线程以获得更高的性能（使用 **/mt** 参数），并在传输中断时重新启动传输的能力（使用 **/z** 参数），请键入：

```
robocopy c:\reports "\\marketing\videos" yearly-report.mov /mt /z

```

Important
如果从设备的 _根目录_ 复制任何数据，则目标目录在复制过程中采用“隐藏”和“系统”属性。
### Parameters  
| Parameter  | Description  |  
| --- | --- |  
| `<source>`  | 指定源目录的路径。  |  
| `<destination>`  | 指定目标目录的路径。  |  
| `<file>`  | 指定要复制的一个或多个文件。 支持通配符（***** 或 **？** ）。 如果未指定此参数，`*.*` 将用作默认值。  |  
| `<options>`  | 指定要与 **robocopy** 命令一起使用的选项，包括 **复制** 、 **文件** 、 **重试** 、 **日志记录** 和 **作业** 选项。  |  
#### Copy options  
| Option  | Description  |  
| --- | --- |  
| /s  | Copies subdirectories. 此选项自动排除空目录。  |  
| /e  | Copies subdirectories. 此选项自动包括空目录。  |  
| /lev:`<n>`  | 仅复制源目录树的前 _n_ 个级别。  |  
| /z  | 以可重启模式复制文件。 在可重启模式下，如果文件复制中断，robocopy 可以从中断位置继续，无需重新复制整个文件。  |  
| /b  | 以备份模式复制文件。 在备份模式下，robocopy 会替代文件和文件夹权限设置 (ACL)，后者在未被替代的情况下可能会阻止访问。  |  
| /zb  | 以可重启模式复制文件。 如果文件访问被拒绝，则切换到备份模式。  |  
| /j  | 使用无缓冲 I/O 进行复制（建议用于大文件）。  |  
| /efsraw  | 在 EFS RAW 模式下复制所有已加密的文件。  |  
| /copy:`<copyflags>`  | 指定要复制的文件属性。 此选项的有效值为：
  * **D** - 数据
  * **A** - 属性
  * **T** - 时间戳
  * **X** - 跳过替代数据流
  * **S - NTFS** 访问控制列表 （ACL）
  * **O** - 所有者信息
  * **U** - 审计信息

**/COPY** 选项的默认值为 **DATA** （数据、属性和时间戳）。 如果使用 **/B** 或 **/ZB** ，则忽略 **X** 标志。  |  
| /dcopy:`<copyflags>`  | 指定要在目录中复制的内容。 此选项的有效值为：
  * **D** - 数据
  * **A** - 属性
  * **T** - 时间戳
  * **E** - 扩展属性
  * **X** - 跳过替代数据流

此选项的默认值为 **DA** （数据和属性）。  |  
| /sec  | 复制具有安全性的文件（相当于 **/copy：DATS** ）。  |  
| /copyall  | 复制所有文件信息（相当于 **/copy：DATSOU）。**  |  
| /nocopy  | 不复制任何文件信息（与 **/purge** 一起使用）。  |  
| /secfix  | 修复所有文件的文件安全性，甚至包括已跳过的文件。  |  
| /timfix  | 修复所有文件的文件时间，甚至包括已跳过的文件。  |  
| /purge  | 删除源中不再存在的目标文件和目录。 将此选项与 **/e** 选项和目标目录一起使用，可以不覆盖目标目录安全设置。  |  
| /mir  | 镜像目录树（相当于 **/e** 加 **/purge** ）。 将此选项与 **/e** 选项和目标目录一起使用，将覆盖目标目录安全设置。  |  
| /mov  | 移动文件，并在复制文件后从源中将其删除。  |  
| /move  | 移动文件和目录，并在复制这些文件和目录后从源中将其删除。  |  
| /a+:[RASHCNET]  | 将指定的属性添加到复制的文件。 此选项的有效值为：
  * **R** - 只读
  * **A** - 存档
  * **S** - 系统
  * **H** - 隐藏
  * **C** - 压缩
  * **N** - 未索引内容
  * **E** - 加密
  * **T** - 临时

 |  
| /a-:[RASHCNETO]  | 从复制的文件中删除指定的属性。 此选项的有效值为：
  * **R** - 只读
  * **A** - 存档
  * **S** - 系统
  * **H** - 隐藏
  * **C** - 压缩
  * **N** - 未索引内容
  * **E** - 加密
  * **T** - 临时
  * **O** - 离线

 |  
| /create  | 仅创建目录树和零长度文件。  |  
| /fat  | 仅使用 8.3 字符长度 FAT 文件名创建目标文件。  |  
| /256  | 关闭对超过 256 个字符的路径的支持。  |  
| /mon:`<n>`  | 监视源，并在检测到 _n 个_ 以上更改时再次运行。  |  
| /mot:`<m>`  | 监视源，如果检测到更改，则在 _m_ 分钟内再次运行。  |  
| /rh:hhmm-hhmm  | 指定可以启动新副本的运行时间。  |  
| /pf  | 检查每个文件（不是每个阶段）的运行时间。  |  
| /ipg:`<n>`  | 指定数据包间的间隙，以便在慢速线路上释放带宽。  |  
| /sj  | 将交接点（软链接）复制到目标路径而不是链接目标。  |  
| /sl  | 不是接在符号链接的后面，而是创建链接的副本。  |  
| /mt:`<n>`  | 创建具有 _n_ 个线程的多线程副本。 _n_ 必须是 1 到 128 之间的整数。 _n_ 的默认值为 8。 为了获得更好的性能，请使用 **/log** 选项重定向输出。 **/mt** 参数不能与 **/ipg** 和 **/efsraw** 参数一起使用。  |  
| /nodcopy  | 不复制目录信息（默认的 **/dcopy：DA** 已完成）。  |  
| /nooffload  | 在不使用 Windows 复制/卸载机制的情况下复制文件。  |  
| /compress  | 在文件传输期间请求网络压缩（如果适用）。  |  
| /sparse:`<y|n>`  | 启用或禁用在复制过程期间保留文件的稀疏状态。 如果未选择任何选项，则默认为 **yes** （启用）。  |  
| /noclone  | 不会尝试将区块克隆作为一种优化。  |  
Important
使用 **/secfix** 复制选项时，使用以下附加复制选项之一指定要复制的安全信息类型：
  * **/copyall**
  * **/copy:o**
  * **/copy:s**
  * **/copy:u**
  * **/sec**


Note
**/mt** 参数是在 Windows Server 2008 R2 中引入的，其功能适用于当前版本的 Windows Server。
#### 复制文件限制选项  
| Option  | Description  |  
| --- | --- |  
| /iomaxsize:`<n>`[kmg]  | 每个读/写周期请求的最大 I/O 大小，以 _n_**k** ilobytes、 **m** egabytes 或 **g** igabytes 为单位。  |  
| /iorate:`<n>`[kmg]  | 请求的 I/O 速率（以 _n_**k ilobytes****m** egabytes 或 **g** igabytes /秒为单位）。  |  
| /threshold:`<n>`[kmg]  | 限制的文件大小阈值，以 _n_**k** ilobytes、 **m** egabytes 或 **g** igabytes 为单位（请参阅 [备注](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/robocopy#remarks)）。  |  
这些限制选项可用于指定 Robocopy 允许使用的最大 I/O 带宽（以“字节/秒”为单位）。 如果未以字节/秒为单位指定，则在指定 **k** 、 **m** 或 **g** 时可以使用整数。 即使指定了较小的值，也会限制的最小 I/O 带宽为 **524288** 字节。
#### 文件选择选项  
| Option  | Description  |  
| --- | --- |  
| /a  | 仅复制设置了 **“存档”** 属性的文件。  |  
| /m  | 仅复制设置了 **“存档”** 属性的文件，并重置“ **存档”** 属性。  |  
| /ia:`[RASHCNETO]`  | 仅包括设置了任何指定属性的文件。 此选项的有效值为：
  * **R** - 只读
  * **A** - 存档
  * **S** - 系统
  * **H** - 隐藏
  * **C** - 压缩
  * **N** - 未索引内容
  * **E** - 加密
  * **T** - 临时
  * **O** - 离线

 |  
| /xa:`[RASHCNETO]`  | 排除设置了任何指定属性的文件。 此选项的有效值为：
  * **R** - 只读
  * **A** - 存档
  * **S** - 系统
  * **H** - 隐藏
  * **C** - 压缩
  * **N** - 未索引内容
  * **E** - 加密
  * **T** - 临时
  * **O** - 离线

 |  
| /xf `<filename>[ ...]`  | 排除与指定的名称或路径匹配的文件。 支持通配符（***** 和**？）。**  |  
| /xd `<directory>[ ...]`  | 排除与指定的名称和路径匹配的目录。  |  
| /xc  | 排除时间戳相同但文件大小不同的现有文件。  |  
| /xn  | 从复制中排除比目标更新的源目录文件。  |  
| /xo  | 从复制中排除比目标更旧的源目录文件。  |  
| /xx  | 排除目标（而不是源）中存在的额外文件和目录。 排除额外文件不会从目标中删除文件。  |  
| /xl  | 排除源（而不是目标）中存在的“孤立”文件和目录。 排除孤立的文件可防止将任何新文件添加到目标。  |  
| /im  | 包括已修改的文件（更改时间不同）。  |  
| /is  | 包括相同的文件。 相同文件的名称、大小、时间和所有属性都相同。  |  
| /it  | 包括“已调整”的文件。 已调整文件的名称、大小和时间相同，但属性不同。  |  
| /max:`<n>`  | 指定最大文件大小（以排除大于 _n_ 字节的文件）。  |  
| /min:`<n>`  | 指定最小文件大小（以排除小于 _n_ 字节的文件）。  |  
| /maxage:`<n>`  | 指定要排除超过 _n_ 天的文件的最大文件期限，或 _基于上次_ 修改文件的时间的日期。  |  
| /minage:`<n>`  | 指定最小文件期限，以排除更新于 _n_ 天的文件或 _基于上次_ 修改文件的时间的日期。  |  
| /maxlad:`<n>`  | 指定上次访问的最大日期（不包括自 _n 以来_ 未使用的文件）。  |  
| /minlad:`<n>`  | 指定上次访问的最短日期（不包括 _自 n_ 以来使用的文件）如果 _n_ 小于 1900，则 _n_ 指定天数。 否则， _n_ 指定格式为 YYYYMMDD 的日期。  |  
| /xj  | 排除交接点（通常默认会包含）。  |  
| /fft  | 采用 FAT 文件时间（精度为两秒）。  |  
| /dst  | 补偿一小时 DST 时差。  |  
| /xjd  | 排除目录的交接点。  |  
| /xjf  | 排除文件的交接点。  |  
#### Retry options  
| Option  | Description  |  
| --- | --- |  
| /r:`<n>`  | 指定复制失败时的重试次数。 _n_ 的默认值为 1,000,000（重试 100 万次）。  |  
| /w:`<n>`  | 指定等待重试的间隔时间，以秒为单位。 _n_ 的默认值为 30（等待时间 30 秒）。  |  
| /reg  | 将 **/r** 和 **/w** 选项中指定的值保存为注册表中的默认设置。  |  
| /tbd  | 指定系统等待定义共享名称（重试错误 67）。  |  
| /lfsm  | 在低可用空间模式下运行，启用复制、暂停和恢复（请参阅 [备注](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/robocopy#remarks)）。  |  
| /lfsm:`<n>`[kmg]  | 以 _n_**k** ilobytes、 **m** egabytes 或 **g** igabytes 为单位指定底层大小。  |  
#### Logging options  
| Option  | Description  |  
| --- | --- |  
| /l  | 指定仅列出文件（而不复制、删除或设置时间戳）。  |  
| /x  | 报告所有额外的文件，而不仅仅是已选择的文件。  |  
| /v  | 生成详细输出，并显示所有已跳过的文件。  |  
| /ts  | 在输出中包括源文件时间戳。  |  
| /fp  | 在输出中包括文件的完整路径名称。  |  
| /bytes  | 以字节为单位输出大小。  |  
| /ns  | 指定不记录文件大小。  |  
| /nc  | 指定不记录文件类。  |  
| /nfl  | 指定不记录文件名。  |  
| /ndl  | 指定不记录目录名称。  |  
| /np  | 指定不显示复制作的进度（到目前为止复制的文件数或目录数）。  |  
| /eta  | 显示复制的文件的估计到达时间 (ETA)。  |  
| /log:`<logfile>`  | 将状态输出写入到日志文件（覆盖现有的日志文件）。  |  
| /log+:`<logfile>`  | 将状态输出写入日志文件（将输出追加到现有日志文件）。  |  
| /unilog:`<logfile>`  | 将状态输出作为 Unicode 文本写入日志文件（覆盖现有日志文件）。  |  
| /unilog+:`<logfile>`  | 将状态输出作为 Unicode 文本写入日志文件（将输出追加到现有日志文件）。  |  
| /tee  | 将状态输出写入控制台窗口和日志文件。  |  
| /njh  | 指定没有作业标头。  |  
| /njs  | 指定没有作业摘要。  |  
| /unicode  | 将状态输出显示为 Unicode 文本。  |  
#### Job options  
| Option  | Description  |  
| --- | --- |  
| /job:`<jobname>`  | 指定要从命名的作业文件派生参数。 若要运行 `/job:jobname`，必须首先运行 `/save:jobname` 参数来创建作业文件。  |  
| /save:`<jobname>`  | 指定要将参数保存到命名的作业文件。 此参数必须在运行 `/job:jobname` 之前运行。 必须在此参数之前指定所有复制、重试和日志记录选项。  |  
| /quit  | 处理命令行后退出（以查看参数）。  |  
| /nosd  | 指示未指定任何源目录。  |  
| /nodd  | 指示未指定目标目录。  |  
| /if  | 包括指定的文件。  |  
#### Remarks
  * 以前，在卷的根目录上使用 **/PURGE** 或 **/MIR** 会导致 robocopy 对系统卷信息目录中的文件应用请求的作。 这不再如此，就像指定了任一类型一样，robocopy 会跳过复制会话的顶级源目录和目标目录中具有该名称的任何文件或目录。
  * 仅当源和目标文件系统支持更改时间戳（例如 NTFS）并且源和目标文件具有不同的更改时间但其他方面都相同时，修改的文件分类才适用。 默认不会复制这些文件。 指定 **/IM** 以包含它们。
  * **/DCOPY：E** 标志请求应尝试对目录进行扩展属性复制。 Robocopy 继续执行复制作，即使无法复制目录的 EA。 此标志不包含在 **/COPYALL** 中。
  * 如果指定了 **/IoMaxSize** 或 **/IoRate** ，则 robocopy 将启用复制文件限制以减少系统负载。 可以对两者进行调整来优化值和复制参数，但允许系统和 robocopy 根据需要将它们调整为允许的值。
  * 如果使用 **/Threshold** ，则指定用于进行限制的最小文件大小。 低于该大小的文件不受限制。 所有三个参数的值均可后跟一个可选后缀字符，例如 [KMG]（千字节、兆字节、千兆字节）。
  * 使用 **/LFSM** 请求 robocopy 在“低可用空间模式”下运行。 在此模式下，每当文件副本会导致目标卷的可用空间低于“floor”值时，robocopy 都会暂停。 可以使用 **/LFSM： _n_**[KMG] 标志显式指定此值。
  * 如果指定 **了 /LFSM** 但没有显式下限值，则下限将设置为目标卷大小的 10%。 低可用空间模式与 **/MT** 和 **/EFSRAW** 不兼容。


### 退出（返回）代码  
| Value  | Description  |  
| --- | --- |  
| 0  | 未复制任何文件。 未遇到任何失败。 没有不匹配的文件。 目标目录中已存在这些文件；因此跳过了复制操作。  |  
| 1  | 已成功复制所有文件。  |  
| 2  | 目标目录中的其他一些文件在源目录中不存在。 未复制任何文件。  |  
| 3  | 复制了一些文件。 存在其他文件。 未遇到任何失败。  |  
| 5  | 复制了一些文件。 某些文件不匹配。 未遇到任何失败。  |  
| 6  | 存在其他文件和不匹配的文件。 未复制任何文件，也没有遇到任何故障，这意味着文件已存在于目标目录中。  |  
| 7  | 已复制文件，存在文件不匹配情况，并且存在其他文件。  |  
| 8  | 有多个文件未复制。  |  
Note
任何等于或大于 **8** 的值都表示在复制作期间至少发生一次故障。
## Examples
强烈建议在运行 `robocopy` 命令时创建一个日志文件，该日志文件可在进程完成验证其完整性后查看。 在以下示例中，每一个都使用 `/LOG:` 参数。 若要将任何日志信息追加到同一日志文件，请改用 `/LOG+:` 参数。
若要将所有文件和子目录（包括空目录）从驱动器“D”上的“记录”文件夹复制到“备份”文件夹，请键入：

```
robocopy C:\Users\Admin\Records D:\Backup /E /ZB /LOG:C:\Logs\Backup.log

```

若要将“记录”文件夹的内容镜像到驱动器“D”上的“备份”文件夹，请删除源中不存在的任何文件，并在每次重试之间等待 5 秒，键入：

```
robocopy C:\Users\Admin\Records D:\Backup /MIR /R:2 /W:5 /LOG:C:\Logs\Backup.log

```

要将所有不为空的文件和子目录从驱动器“D”上的“备份”文件夹复制到驱动器“D”上的“备份”文件夹，请保留具有 16 个多线程复制作的文件数据、属性和时间戳，请键入：

```
robocopy C:\Users\Admin\Records D:\Backup /S /E /COPY:DAT /MT:16 /LOG:C:\Logs\Backup.log

```

若要将文件和子目录（不包括空目录）从“记录”文件夹移动到驱动器“D”上的“备份”文件夹，并排除超过 7 天的文件，请键入：

```
robocopy C:\Users\Admin\Records D:\Backup /S /MAXAGE:7 /MOV /LOG:C:\Logs\Backup.log

```

若要将所有文件和子目录（包括空目录）从驱动器“D”上的“记录”文件夹复制到驱动器“D”上的“备份”文件夹，显示每个文件的估计时间，并删除源中不存在的任何文件和目录，请键入：

```
robocopy C:\Users\Admin\Records D:\Backup /ETA /PURGE /LOG:C:\Logs\Backup.log

```

若要将“C”驱动器上名为“Records”的文件夹中的所有文件和子目录复制到“D”驱动器上的名为“Backup”的文件夹，同时在复制作期间将 I/O 速率限制为每秒 1 兆字节，请键入：

```
robocopy C:\Records D:\Backup /iorate:1m

```

若要在目标文件夹中已存在文件时跳过将文件从源文件夹复制到目标文件夹，无论这些文件是较新、较旧还是已修改，请键入：

```
robocopy C:\Source C:\Destination /XC /XN /XO

```

## Related links


## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-08-16 


