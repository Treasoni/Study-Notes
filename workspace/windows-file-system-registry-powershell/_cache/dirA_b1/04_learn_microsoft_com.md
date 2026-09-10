---
url: "https://learn.microsoft.com/zh-cn/windows/win32/fileio/naming-a-file"
title: "文件命名、路径和命名空间 - Win32 apps | Microsoft Learn"
scraped_at: 2026-09-10T15:41:08+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows/win32/fileio/naming-a-file) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows/win32/fileio/naming-a-file)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# 命名文件、路径和命名空间
Windows 支持的文件系统使用文件和目录的概念来访问存储在磁盘或设备上的数据。 使用适用于文件和设备 I/O 的 Windows API 的 Windows 开发人员应了解文件和目录的名称的规则、约定和限制。
可以使用文件 I/O API 从磁盘、设备和网络共享访问数据。 文件和目录以及命名空间是路径概念的一部分，路径是获取数据的位置的字符串表示形式，无论数据来自磁盘、设备还是用于特定操作的网络连接。
某些文件系统（如 NTFS）支持链接文件和目录，它们也遵循文件命名约定和规则，就像常规文件或目录一样。 有关其他信息，请参阅[硬链接和交汇点](https://learn.microsoft.com/zh-cn/windows/win32/fileio/hard-links-and-junctions)和[重新分析点和文件操作](https://learn.microsoft.com/zh-cn/windows/win32/fileio/reparse-points-and-file-operations)。
若要了解如何配置 Windows 以支持长文件路径，请参阅[最大路径长度限制](https://learn.microsoft.com/zh-cn/windows/win32/fileio/maximum-file-path-limitation)。
## 文件和目录名称
所有文件系统都遵循单个文件的相同常规命名约定：基文件名和可选扩展名，用句点分隔。 但是，每个文件系统（例如 NTFS、CDFS、exFAT、UDFS、FAT 和 FAT32）对目录或文件路径中各个组件的形成都可以有特定和不同的规则。 请注意， _目录_ 只是具有特殊属性的文件，该属性将其指定为目录，但不管怎样，必须像常规文件一样遵循所有命名规则。 由于术语 _目录_ 在文件系统中仅指特殊类型的文件，因此某些参考资料将使用常规术语 _文件_ 来囊括目录和数据文件等等概念。 因此，除非另行指定，否则文件的任何命名或使用规则或示例也适用于目录。 术语 _路径_ 是指一个或多个目录、反斜杠，可能还有一个卷名称。 有关详细信息，请参阅[路径](https://learn.microsoft.com/zh-cn/windows/win32/fileio/naming-a-file#fully-qualified-vs-relative-paths)部分。
字符计数限制也可能不同，并可能因使用的文件系统和路径名称前缀格式而异。 由于需要支持向后兼容机制，情况进一步复杂化。 例如，较旧的 MS-DOS FAT 文件系统支持基文件名最多 8 个字符，扩展名最多支持 3 个字符，总共支持 12 个字符（包括点分隔符）。 这通常称为 _8.3 文件名_ 。 Windows FAT 和 NTFS 文件系统不限于 8.3 文件名，因为它们有 _长文件名支持_ 功能，但也支持 8.3 版本的长文件名。
### 命名约定
以下基本规则使应用程序能够创建和处理文件和目录的有效名称，而不考虑文件系统：
  * 使用句点将基文件名与目录或文件名称中的扩展名分隔开。
  * 使用反斜杠 (\\) 分隔 _路径_ 的 _组件_ 。 反斜杠将文件名与其路径分开，并将一个目录名与路径中的另一个目录名分开。 不能在实际文件或目录的名称中使用反斜杠，因为它是将名称分隔成组件的保留字符。
  * 根据需要使用反斜杠作为[卷名称](https://learn.microsoft.com/zh-cn/windows/win32/fileio/naming-a-volume)的一部分，例如“C:\”在“C:\path\file”中或“\\\server\share”在“\\\server\share\path\file”中是通用命名约定 (UNC) 名称。 有关 UNC 名称的详细信息，请参阅[最大路径长度限制](https://learn.microsoft.com/zh-cn/windows/win32/fileio/naming-a-file#maximum-path-length-limitation)部分。
  * 不要假定区分大小写。 例如，将名称 OSCAR、Oscar 和 oscar 视为相同，即使某些文件系统（如符合 POSIX 的文件系统）可能将其视为不同。 请注意，NTFS 支持用于区分大小写的 POSIX 语义，但这不是默认行为。 有关详细信息，请参阅 [CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea)。
  * （驱动器号）的卷指定符同样不区分大小写。 例如，“D:\”和“d:\”指的是同一个卷。
  * 使用当前代码页中的任何字符作为名称，包括 Unicode 字符和扩展字符集 (128-255) 中的字符，但以下各项除外：
    * 以下保留字符：
      * <（小于）
      * >（大于）
      * :（冒号）
      * "（双引号）
      * /（正斜杠）
      * \（反斜杠）
      * |（竖线或管道符）
      * ? （问号）
      * *（星号）
    * 整数值零，有时称为 ASCII _NUL_ 字符。
    * 字符的整数表示范围介于 1 到 31 之间，但在备用数据流中允许使用这些字符。 有关文件流的详细信息，请参阅[文件流](https://learn.microsoft.com/zh-cn/windows/win32/fileio/file-streams)。
    * 目标文件系统不允许的任何其他字符。
  * 使用点号作为路径中的目录 _组件_ 来表示当前目录，例如".\temp.txt"。 有关详细信息，请参阅[路径](https://learn.microsoft.com/zh-cn/windows/win32/fileio/naming-a-file#fully-qualified-vs-relative-paths)。
  * 使用两个连续的句点 (..) 作为路径中的目录 _组件_ ，以表示当前目录的父目录，例如“..\temp.txt”。 有关详细信息，请参阅[路径](https://learn.microsoft.com/zh-cn/windows/win32/fileio/naming-a-file#fully-qualified-vs-relative-paths)。
  * 不要将以下保留名称用于文件的名称：
CON、PRN、AUX、NUL、COM1、COM2、COM3、COM4、COM5、COM6、COM7、COM8、COM9、COM¹、COM²、COM³、LPT1、LPT2、LPT3、LPT4、LPT5、LPT6、LPT7、LPT8、LPT9、LPT¹、LPT²、LPT³。 另请避免这些名称紧跟扩展名；例如，NUL.txt 和 NUL.tar.gz 都等效于 NUL。 有关详细信息，请参阅[命名空间](https://learn.microsoft.com/zh-cn/windows/win32/fileio/naming-a-file#win32-file-namespaces)。
注意
Windows 可将 8 位 [ISO/IEC 8859-1](https://en.wikipedia.org/wiki/ISO/IEC_8859-1) 上标数字 ¹、² 和 ³ 识别为数字，并将其视为 COM# 和 LPT# 设备名称的有效部分，使其保留在每个目录中。 例如，`echo test > COM¹` 无法创建文件。
  * 不要用空格或句点结束文件或目录名称。 尽管基础文件系统可能支持此类名称，但 Windows Shell 和用户界面不支持。 不过，指定句点作为名称的第一个字符是可接受的。 例如，“.temp”。


### 短与长名称
长文件名被视为超出短 MS-DOS（也称为 _8.3_ ）样式命名约定的任何文件名。 创建长文件名时，Windows 还可以创建名称的短 8.3 格式，称为 _8.3 别名_ 或短名称，也将其存储在磁盘上。 此 8.3 别名可以出于性能原因在系统范围内或针对指定卷禁用，具体取决于特定的文件系统。
**Windows Server 2008、Windows Vista、Windows Server 2003 和 Windows XP：** 在 Windows 7 和 Windows Server 2008 R2 之前，无法禁用指定卷的 8.3 别名。
在许多文件系统上，文件名将在名称的每个组件中包含一个波形符 (~)，该组件太长，无法符合 8.3 命名规则。
注意
并非所有文件系统都遵循波形符替换约定，并且系统可以配置为禁用 8.3 别名生成，即使系统通常支持它。 因此，不要假设磁盘上已存在 8.3 别名。
若要从系统请求 8.3 文件名、长文件名或文件的完整路径，请考虑以下选项：
  * 若要获取 8.3 格式的长文件名，请使用 [GetShortPathName](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-getshortpathnamew) 函数。
  * 若要获取短名称的长文件名版本，请使用 [GetLongPathName](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-getlongpathnamea) 函数。
  * 若要获取文件的完整路径，请使用 [GetFullPathName](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-getfullpathnamea) 函数。


在较新的文件系统（如 NTFS、exFAT、UDFS 和 FAT32）上，Windows 将长文件名以 Unicode 格式存储在磁盘上，这意味着原始长文件名始终被保留。 即使长文件名包含扩展字符，也同样适用，无论在磁盘读取或写入操作期间哪个代码页处于活动状态。
可以在 NTFS 文件系统分区和 Windows FAT 文件系统分区之间复制使用长文件名的文件，而不会丢失任何文件名信息。 对于较旧的 MS-DOS FAT 和某些类型的 CDFS (CD-ROM) 文件系统，可能不是这样，具体取决于实际文件名。 在这种情况下，如果可能，将替换短文件名。
## 路径
指定文件的 _路径_ 由一个或多个 _组件_ 组成，由特殊字符（反斜杠）分隔，每个组件通常为目录名或文件名，下面讨论了一些值得注意的例外情况。 路径的开头或 _前缀_ 的外观通常对系统如何解释该路径至关重要。 此前缀确定路径使用的 _命名空间_ ，以及路径中的哪个位置额外使用了哪些特殊字符，包括最后一个字符。
如果路径的组件是文件名，则它必须是最后一个组件。
路径的每个组件也将受特定文件系统的指定最大长度约束。 一般情况下，这些规则分为两类： _短_ 和 _长_ 。 请注意，目录名由文件系统存储为特殊类型的文件，但文件的命名规则也适用于目录名。 总之，路径只是字符串表示形式，用于描述特定文件或目录名之下所有目录之间的层次结构。
### 完全限定与相对路径
对于操作文件的 Windows API 函数，文件名通常可以与当前目录相对应，而某些 API 需要完全限定的路径。 如果文件名不以下列项之一开头，则其与当前目录相对应：
  * 任何格式的 UNC 名称，始终以两个反斜杠字符开头 ("\\\")。 有关详细信息，请参阅下一部分。
  * 带反斜杠的磁盘指示符，例如“C:\”或“d:\”。
  * 单个反斜杠，例如“\directory”或“\file.txt”。 这也称为 _绝对路径_ 。


如果文件名仅以磁盘指示符开头，而不是冒号后的反斜杠，则将其解释为驱动器上具有指定字母的当前目录的相对路径。 请注意，当前目录可能是根目录，也可能不是根目录，具体取决于该目录在该磁盘上最近执行“更改目录”操作期间所设置的内容。 该格式的示例如下：
  * “C:tmp.txt”是指驱动器 C 上当前目录中名为“tmp.txt”的文件。
  * “C:tempdir\tmp.txt”是指驱动器 C 上当前目录的子目录中的文件。


如果路径包含“双点”，则也称其为相对路径：也就是说，两个句点一起位于路径的一个组件中。 此特殊说明符用于表示当前目录上方的目录，也称为“父目录”。 该格式的示例如下：
  * “..\tmp.txt”指定名为 tmp.txt 的文件，该文件位于当前目录的父目录中。
  * “..\\..\tmp.txt”指定高于当前目录两个目录的文件。
  * “..\tempdir\tmp.txt”指定位于目录 tempdir 中的文件 tmp.txt，该文件是当前目录的对等目录。


相对路径可以合并这两种示例类型，例如“C:..\tmp.txt”。 这很有用，因为尽管系统会跟踪当前驱动器以及该驱动器的当前目录，但它也会跟踪不同驱动器号（如果系统有多个）中的当前目录，无论将哪个驱动器指示符设置为当前驱动器。
### 最大路径长度限制
在 Windows 10 版本 1607 之前的 Windows 版本中，路径的最大长度为 **MAX_PATH** ，定义为 260 个字符。 在更高版本的 Windows 中，需要更改注册表项或使用组策略工具来删除限制。 有关完整详细信息，请参阅[最大路径长度限制](https://learn.microsoft.com/zh-cn/windows/win32/fileio/maximum-file-path-limitation)。
## 命名空间
Windows API 中使用的命名空间约定主要有两类，通常称为 _NT 命名空间_ 和 _Win32 命名空间_ 。 NT 命名空间设计为其他子系统和命名空间（包括 Win32 子系统和按扩展名分配的 Win32 命名空间）可存在的最低级别命名空间。 POSIX 是 Windows 中基于 NT 命名空间构建的子系统的另一个示例。 早期版本的 Windows 还为某些特殊设备（例如通信（串行和并行）端口）以及默认显示控制台（现在所谓 NT 设备命名空间的一部分）定义了多个预定义或保留的名称，并且为了向后兼容，当前版本的 Windows 仍予支持。
### Win32 文件命名空间
本部分和下一部分汇总了 Win32 命名空间前缀和约定，并介绍了使用方式。 请注意，这些示例旨在与 Windows API 函数一起使用，并不一定都适用于 Windows Shell 应用程序，例如 Windows 资源管理器。 因此，可能的路径范围比通常从 Windows Shell 应用程序提供的路径更广，利用这一点的 Windows 应用程序可以使用这些命名空间约定进行开发。
对于文件 I/O，路径字符串的“\\\?\”前缀会告知 Windows API 禁用所有字符串分析，并将其后面的字符串直接发送到文件系统。 例如，如果文件系统支持大型路径和文件名，则可以越过 Windows API 在其他情况下强制执行的 **MAX_PATH** 限制。
由于它关闭了路径字符串的自动扩展，因此“\\\?\”前缀还允许在路径名称中使用“..”和“.”，如果尝试对文件执行操作并将保留相对路径说明符作为完全限定路径的一部分，这些符号非常有用。
许多（但并非所有）文件 I/O API 都支持“\\\?\”；应查看每个 API 的参考主题才能确定。
请注意，应使用 Unicode API 来确保“\\\?\”前缀允许超过 **MAX_PATH** 。
### Win32 设备命名空间
“\\\\.\”前缀将访问 Win32 设备命名空间，而不是 Win32 文件命名空间。 这是直接访问物理磁盘和卷的方式，而无需通过文件系统（如果 API 支持这种类型的访问）。 可以照此方式访问磁盘以外的许多设备（例如，使用 [CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 和 [DefineDosDevice](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-definedosdevicew) 函数）。
例如，如果要打开系统的串行通信端口 1，可以在调用 [CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 函数时使用“COM1”。 这样做是因为 COM1-COM9 是 NT 命名空间中保留名称的一部分，尽管使用“\\\\.\”前缀也适用于这些设备名称。 相比之下，如果安装了 100 端口串行扩展板，并且想要打开 COM56，则无法使用“COM56”打开它，因为 COM56 没有预定义的 NT 命名空间。 需要使用“\\\\.\COM56”打开它，因为“\\\\.\”直接转到设备命名空间，而无需尝试查找预定义的别名。
使用 Win32 设备命名空间的另一个示例是将 [CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 函数与“\\\\.\PhysicalDrive _X_ ”（其中 _X_ 是有效整数值）或“\\\\.\CdRom _X_ ”一起使用。 这样，可以绕过文件系统直接访问这些设备。 这之所以有效，是因为这些设备名称是由系统在枚举这些设备时创建的，并且某些驱动程序还会在系统中创建其他别名。 例如，实现名称“C:\”的设备驱动程序有自己的命名空间，恰好也是该文件系统。
通过 [CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 函数的 API 通常使用“\\\\.\”前缀，因为 **CreateFile** 是用于打开文件和设备的函数，具体取决于所使用的参数。
如果使用 Windows API 函数，则应使用“\\\\.\”前缀来访问设备，而不访问文件。
大多数 API 不支持“\\\\.\”；只有那些专为与设备命名空间协作而设计的 API 才能识别它。 始终检查每个 API 的参考主题来确定。
### NT 命名空间
也有一些 API 允许使用 NT 命名空间约定，但 Windows 对象管理器使这一点在大多数情况下变得不必要。 为了进行说明，可以使用 Windows Sysinternals [WinObj](https://learn.microsoft.com/zh-cn/sysinternals/downloads/winobj) 工具在系统对象浏览器中浏览 Windows 命名空间。 运行此工具时，看到的是从根开始的 NT 命名空间，或“\”。 名为“Global??”的子文件夹是 Win32 命名空间所在的位置。 命名设备对象驻留在“Device”子目录中的 NT 命名空间中。 在这里，还可以找到 Serial0 和 Serial1，这些设备对象表示系统存在的前两个 COM 端口。 表示卷的设备对象类似于“HarddiskVolume1”，尽管数字后缀可能会有所不同。 子目录“Harddisk0”下的名称“DR0”是磁盘等设备对象的一个示例。
为了使这些设备对象可供 Windows 应用程序访问，设备驱动程序会在 Win32 命名空间“Global??”中创建符号链接 (symlink)，指向各自的设备对象。 例如，“Global??”子目录下的 COM0 和 COM1 只是指向 Serial0 和 Serial1 的符号链接，“C:”是指向 HarddiskVolume1 的符号链接，“Physicaldrive0”是指向 DR0 的符号链接，以此类推。 如果没有符号链接，指定的设备“Xxx”将无法供任何使用 Win32 命名空间约定的 Windows 应用程序使用，如前所述。 但是，可以使用任何 API 向该设备打开句柄，只要该 API 支持格式“\Device\Xxx”的 NT 命名空间绝对路径。
通过终端服务和虚拟机添加多用户支持后，虚拟化 Win32 命名空间中的系统范围根设备变得更有必要。 方法是为 Win32 命名空间添加名为“GLOBALROOT”的符号链接，可以在前面讨论的 WinObj 浏览器工具的“Global??”子目录中看到该符号链接，并且可以通过路径“\\\?\GLOBALROOT”进行访问。 此前缀可确保其后面的路径指向系统对象管理器的真实根路径，而不是会话相关路径。
## 另请参阅


## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2024-08-28 


