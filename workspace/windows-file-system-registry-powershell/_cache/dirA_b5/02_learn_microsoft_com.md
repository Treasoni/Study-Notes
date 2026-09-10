---
url: "https://learn.microsoft.com/zh-cn/windows/win32/fileio/creating-and-opening-files"
title: "创建和打开文件 - Win32 apps | Microsoft Learn"
scraped_at: 2026-09-10T15:42:00+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows/win32/fileio/creating-and-opening-files) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows/win32/fileio/creating-and-opening-files)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# 创建和打开文件
[CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 函数可以创建新文件或打开现有文件。 必须指定文件名、创建说明和其他属性。 在应用程序创建新文件时，操作系统会将其添加到指定目录。
## 选择正确的文件 API  
| Scenario  | 推荐的 API  | 备注  |  
| --- | --- | --- |  
| C/C++ 中的简单文件读取/写入  |  `fopen` / `fread` / `fwrite` （CRT） 或 C++ `std::ifstream`/`std::ofstream`  | 可移植，自动处理缓冲。 足以满足大多数应用程序级文件 I/O。  |  
| 文件路径操作和枚举  | C++17 `std::filesystem`  | 可移植的新式 C++ 。 用于目录遍历、路径操作和基本文件元数据。  |  
| 重叠（异步）I/O  |  **CreateFile** 使用 `FILE_FLAG_OVERLAPPED`  | 对于 I/O 完成端口、高性能服务器和非阻塞文件操作是必需的。  |  
| 细粒度共享或锁定  |  **CreateFile** 的 _dwShareMode_  | 只有 CreateFile 可以控制进程之间的并发文件访问。  |  
| 内存映射文件  |  **CreateFile** + [CreateFileMapping](https://learn.microsoft.com/zh-cn/windows/win32/api/winbase/nf-winbase-createfilemappinga)  | 共享内存、大型文件随机访问和进程间通信是必需的。  |  
| 设备、管道、邮件槽或控制台  |  **CreateFile**  | CRT 和标准库 API 不支持这些 Win32 对象类型。  |  
| .NET托管应用程序  |  `System.IO.File` / `System.IO.FileStream`  | 对于 .NET 代码是首选。 内部使用 CreateFile，但提供基于异常的错误处理和 async/await。  |  
Important
**错误处理** ：始终检查 **CreateFile** 的返回值。 失败时，它将返回 `INVALID_HANDLE_VALUE` （而不是 `NULL`）。 调用失败后立即调用 [GetLastError](https://learn.microsoft.com/zh-cn/windows/win32/api/errhandlingapi/nf-errhandlingapi-getlasterror) 以获取特定的错误代码。 常见错误包括`ERROR_FILE_NOT_FOUND`和 `ERROR_ACCESS_DENIED``ERROR_SHARING_VIOLATION`。
注释
**常见陷阱 - dwShareMode** ：将 _dwShareMode_ 设置为 `0` （独占访问）是安全的，但如果另一个进程已打开文件，则可能会导致 `ERROR_SHARING_VIOLATION` 此问题。 对于其他进程可以并发读取的日志文件或文件，请使用 `FILE_SHARE_READ`。 避免使用 `FILE_SHARE_WRITE`，除非你有协调机制——未协调的并发写入可能会损坏文件内容。
## 在应用程序中处理文件
操作系统将唯一标识符（称为 _句柄_ ）分配给使用[CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea)打开或创建的每个文件。 应用程序可以将此句柄与读取、写入和描述文件的函数配合使用。 在关闭对该句柄的所有引用之前，它将一直有效。 当应用程序启动时，如果这些句柄在创建时被设为可继承，它将继承启动它的进程中的所有打开句柄。
应用程序应在尝试使用句柄访问文件之前检查 [CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 返回的句柄的值。 如果发生错误，则句柄值将 **INVALID_HANDLE_VALUE** ，应用程序可以使用 [GetLastError](https://learn.microsoft.com/zh-cn/windows/win32/api/errhandlingapi/nf-errhandlingapi-getlasterror) 函数获取扩展的错误信息。
当应用程序使用 [CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 时，它必须使用 _dwDesiredAccess_ 参数来指定它是否打算从文件读取、写入文件、读取和写入文件，或者两者都不执行。 这就是所谓的请求 _访问模式_ 。 应用程序还必须使用 _dwCreationDisposition_ 参数来指定在文件已经存在的情况下应采取的操作，即所谓的 _创建处置_ 。 例如，应用程序可以调用 [CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 并将 _dwCreationDisposition_ 设置为 **CREATE_ALWAYS** ，以始终创建一个新文件，即使同名文件已经存在（从而覆盖现有文件）。 成功与否取决于前一个文件的属性和安全设置等因素（有关详细信息，请参阅以下部分）。
应用程序还使用[CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea)来指定是要共享文件以读取、写入、两者皆共享还是都不共享。 这就是所谓的 _共享模式_ 。 未共享的已打开文件（ _dwShareMode_ 设置为零）在其句柄关闭之前，无论是打开文件的应用程序还是其他应用程序都无法再次打开。 这也被称为独占访问。
当进程使用 [CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 尝试打开已在共享模式下打开的文件（ _dwShareMode_ 设置为有效的非零值），系统将请求的访问和共享模式与打开文件时指定的文件进行比较。 如果指定的访问或共享模式与前次调用中指定的模式冲突，则 **CreateFile** 将失败。
下表说明了使用各种访问模式和共享模式（[dwDesiredAccess](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea)、 _dwShareMode_ ）对 _CreateFile_ 的两个调用的有效组合。 调用 **CreateFile** 的顺序并不重要。 但是，每个文件句柄上的任何后续文件 I/O 操作仍将受到与该特定文件句柄相关的当前访问和共享模式的限制。  
| 首次调用 CreateFile  | 对 CreateFile 的有效第二次调用  |  
| --- | --- |  
|  **GENERIC_READ** 、**FILE_SHARE_READ**  |  - **GENERIC_READ** 、**FILE_SHARE_READ** - **GENERIC_READ** 、**FILE_SHARE_READ****FILE_SHARE_WRITE**  |  
|  **GENERIC_READ** 、**FILE_SHARE_WRITE**  |  - **GENERIC_WRITE** , **FILE_SHARE_READ** - **GENERIC_WRITE** 、**FILE_SHARE_READ****FILE_SHARE_WRITE**  |  
|  **GENERIC_READ** 、**FILE_SHARE_READ** 、**FILE_SHARE_WRITE**  |  - **GENERIC_READ** 、**FILE_SHARE_READ** - **GENERIC_READ** 、 **FILE_SHARE_READ** 、 **FILE_SHARE_WRITE** - **GENERIC_WRITE** , **FILE_SHARE_READ** - **GENERIC_WRITE** 、 **FILE_SHARE_READ** 、 **FILE_SHARE_WRITE** - **GENERIC_READ****GENERIC_WRITE** 、**FILE_SHARE_READ** - **GENERIC_READ****GENERIC_WRITE** 、**FILE_SHARE_READ** 、**FILE_SHARE_WRITE**  |  
|  **GENERIC_WRITE** 、**FILE_SHARE_READ**  |  - **GENERIC_READ** 、 **FILE_SHARE_WRITE** - **GENERIC_READ** 、 **FILE_SHARE_READ** 、 **FILE_SHARE_WRITE**  |  
|  **GENERIC_WRITE** 、**FILE_SHARE_WRITE**  |  - **GENERIC_WRITE** , **FILE_SHARE_WRITE** - **GENERIC_WRITE** 、 **FILE_SHARE_READ** 、 **FILE_SHARE_WRITE**  |  
|  **GENERIC_WRITE** 、**FILE_SHARE_READ** 、**FILE_SHARE_WRITE**  |  - **GENERIC_READ** 、 **FILE_SHARE_WRITE** - **GENERIC_READ** 、 **FILE_SHARE_READ** 、 **FILE_SHARE_WRITE** - **GENERIC_WRITE** , **FILE_SHARE_WRITE** - **GENERIC_WRITE** 、 **FILE_SHARE_READ** 、 **FILE_SHARE_WRITE** - **GENERIC_READ** 、 **GENERIC_WRITE** 、 **FILE_SHARE_WRITE** - **GENERIC_READ** 、 **GENERIC_WRITE** 、 **FILE_SHARE_READ** 、 **FILE_SHARE_WRITE**  |  
|  **GENERIC_READ** 、**GENERIC_WRITE** 、**FILE_SHARE_READ**  |  - **GENERIC_READ** 、 **FILE_SHARE_READ** 、 **FILE_SHARE_WRITE**  |  
|  **GENERIC_READ** 、**GENERIC_WRITE** 、**FILE_SHARE_WRITE**  |  - **GENERIC_WRITE** 、 **FILE_SHARE_READ** 、 **FILE_SHARE_WRITE**  |  
|  **GENERIC_READ** 、**GENERIC_WRITE** 、**FILE_SHARE_READ** 、**FILE_SHARE_WRITE**  |  - **GENERIC_READ** 、 **FILE_SHARE_READ** 、 **FILE_SHARE_WRITE** - **GENERIC_WRITE** 、 **FILE_SHARE_READ** 、 **FILE_SHARE_WRITE** - **GENERIC_READ** 、 **GENERIC_WRITE** 、 **FILE_SHARE_READ** 、 **FILE_SHARE_WRITE**  |  
除了标准文件属性，还可以通过将指向 [SECURITY_ATTRIBUTES](https://learn.microsoft.com/zh-cn/previous-versions/windows/desktop/legacy/aa379560\(v=vs.85\)) 结构的指针作为 [CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 的第四个参数来指定安全属性。 但是，基础文件系统必须支持安全性才能产生相关效果（例如，NTFS 文件系统支持安全性，但各种 FAT 文件系统不支持安全性）。 有关安全属性的详细信息，请参阅[访问控制](https://learn.microsoft.com/zh-cn/windows/win32/SecAuthZ/access-control)。
创建新文件的应用程序可以提供模板文件的可选句柄， [CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 从中获取文件属性和扩展属性以创建新文件。
## CreateFile 场景
有多种基本方案可用于使用 [CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 函数启动对文件的访问权限。 概括起来包括：
  * 在不存在同名文件的情况下创建新文件。
  * 即使已经存在同名文件，也要创建新文件，从而清除其数据并清空。
  * 仅在现有文件存在且完好无损时才打开它。
  * 仅在现有文件存在的情况下打开该文件，并将其截断为空。
  * 打开文件时始终：如果存在则按原样打开，如果不存在则创建新文件。


这些方案可通过正确使用 _dwCreationDisposition_ 参数来控制。 下面将详细介绍这些情景如何与该参数的值相对应，以及使用这些值时的情况。
当创建或打开新文件且该名称的文件尚不存在时（ _dwCreationDisposition_ 设置为 **CREATE_NEW** 、**CREATE_ALWAYS** 或 **OPEN_ALWAYS** ），[CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 函数执行以下操作：
  * 将 _dwFlagsAndAttributes_ 指定的文件属性和标志与 **FILE_ATTRIBUTE_ARCHIVE** 相结合。
  * 将文件长度设置为零。
  * 如果指定了 _hTemplateFile_ 参数，则将模板文件提供的扩展属性复制到新文件中（这将覆盖前面指定的所有 **FILE_ATTRIBUTE_*** 标志）。
  * 设置 **bInheritHandle** 成员指定的继承标志以及由 **lpSecurityAttributes** 参数 （ _SECURITY_ATTRIBUTES_ 结构） 的 [lpSecurityDescriptor](https://learn.microsoft.com/zh-cn/previous-versions/windows/desktop/legacy/aa379560\(v=vs.85\)) 成员指定的安全描述符（如果提供）。


创建新文件时，即使已存在同名文件（ _dwCreationDisposition_ 设置为 **CREATE_ALWAYS** ）， [CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 函数也会执行以下作：
  * 检查当前文件属性和安全设置是否允许写入访问，如果拒绝则失败。
  * 将 _dwFlagsAndAttributes_ 指定的文件属性和标志与 **FILE_ATTRIBUTE_ARCHIVE** 和现有文件属性相结合。
  * 将文件长度设置为零（也就是说，文件中的任何数据都不再可用，文件为空）。
  * 如果指定了 _hTemplateFile_ 参数，则将模板文件提供的扩展属性复制到新文件中（这将覆盖前面指定的所有 **FILE_ATTRIBUTE_*** 标志）。
  * 设置由 **lpSecurityAttributes** 参数 （ _SECURITY_ATTRIBUTES_ 结构） 的 [bInheritHandle](https://learn.microsoft.com/zh-cn/previous-versions/windows/desktop/legacy/aa379560\(v=vs.85\)) 成员指定的继承标志（如果已提供），但忽略**SECURITY_ATTRIBUTES** 结构的 **lpSecurityDescriptor** 成员。
  * 如果否则成功（即 [CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 返回有效句柄），调用 [GetLastError](https://learn.microsoft.com/zh-cn/windows/win32/api/errhandlingapi/nf-errhandlingapi-getlasterror) 将生成代码 **ERROR_ALREADY_EXISTS** ，即使对于此特定用例，它实际上不是错误（如果打算创建“new”（空）文件代替现有文件）。


打开现有文件（ _dwCreationDisposition_ 设置为 **OPEN_EXISTING** 、 **OPEN_ALWAYS** 或 **TRUNCATE_EXISTING** ）时， [CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 函数将执行以下作：
  * 检查请求访问的当前文件属性和安全设置，如果拒绝则失败。
  * 将 **dwFlagsAndAttributes** 指定的文件标志 (_FILE_FLAG_*_) 与现有文件属性相结合，并忽略 **dwFlagsAndAttributes** 指定的任何文件属性 (_FILE_ATTRIBUTE_*_)。
  * 只有当 _dwCreationDisposition_ 设置为 **TRUNCATE_EXISTING** 时，才会将文件长度设置为零，否则将保持当前文件长度，并按原样打开文件。
  * 忽略 _hTemplateFile_ 参数。
  * 设置由 **lpSecurityAttributes** 参数 （ _SECURITY_ATTRIBUTES_ 结构） 的 [bInheritHandle](https://learn.microsoft.com/zh-cn/previous-versions/windows/desktop/legacy/aa379560\(v=vs.85\)) 成员指定的继承标志（如果已提供），但忽略**SECURITY_ATTRIBUTES** 结构的 **lpSecurityDescriptor** 成员。


## 文件属性和目录
文件属性是与文件或目录相关联的元数据的一部分，每个属性都有自己的用途，以及如何设置和更改的规则。 其中一些属性只适用于文件，一些属性只适用于目录。 例如，**FILE_ATTRIBUTE_DIRECTORY** 属性只适用于目录：文件系统使用该属性来确定磁盘上的对象是否为目录，但不能更改现有文件系统对象的该属性。
一些文件属性可以为某个目录设置，但只对在该目录下创建的文件有意义，它们就像默认属性一样。 例如，可以在目录对象上设置 **FILE_ATTRIBUTE_COMPRESSED** ，但由于目录对象本身不包含实际数据，因此它并不是真正的压缩对象；不过，标有该属性的目录会告诉文件系统压缩添加到该目录中的任何新文件。 可以在目录上设置的任何文件属性，以及添加到该目录的新文件也将设置的任何文件属性，都被称为 _继承属性_ 。
[CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 函数提供一个参数，用于在创建文件时设置某些文件属性。 一般来说，这些属性是应用程序在创建文件时最常用的属性，但 **CreateFile** 并不能使用所有可能的文件属性。 某些文件属性需要在文件已存在后，使用其他函数，例如 [SetFileAttributes](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-setfileattributesa)、[DeviceIoControl](https://learn.microsoft.com/zh-cn/windows/desktop/api/ioapiset/nf-ioapiset-deviceiocontrol) 或 [DecryptFile](https://learn.microsoft.com/zh-cn/windows/win32/api/WinBase/nf-winbase-decryptfilea)。 对于 **FILE_ATTRIBUTE_DIRECTORY** ，创建时需要 [CreateDirectory](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createdirectorya) 函数，因为 **CreateFile** 无法创建目录。 其他需要特殊处理的文件属性包括 **FILE_ATTRIBUTE_REPARSE_POINT** 和 **FILE_ATTRIBUTE_SPARSE_FILE** ，它们需要 **DeviceIoControl** 。 有关详细信息，请参阅 [SetFileAttributes](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-setfileattributesa)。
如前所述，文件属性继承发生在创建文件时，文件属性是从文件所在目录属性中读取的。 下表汇总了这些继承的属性及其与 [CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea) 功能的关系。  
| 目录属性状态  | CreateFile 会让新文件继承替代功能  |  
| --- | --- |  
|  **FILE_ATTRIBUTE_COMPRESSED** 已设置。  | 无控制。 使用 [DeviceIoControl](https://learn.microsoft.com/zh-cn/windows/desktop/api/ioapiset/nf-ioapiset-deviceiocontrol) 清除。  |  
|  **FILE_ATTRIBUTE_COMPRESSED** 未设置。  | 无控制。 使用 [DeviceIoControl](https://learn.microsoft.com/zh-cn/windows/desktop/api/ioapiset/nf-ioapiset-deviceiocontrol) 进行设置。  |  
|  **FILE_ATTRIBUTE_ENCRYPTED** 已设置。  | 无控制。 使用 [DecryptFile](https://learn.microsoft.com/zh-cn/windows/desktop/api/WinBase/nf-winbase-decryptfilea)。  |  
|  **FILE_ATTRIBUTE_ENCRYPTED** 未设置。  | 可以使用 [CreateFile](https://learn.microsoft.com/zh-cn/windows/desktop/api/FileAPI/nf-fileapi-createfilea) 进行设置。  |  
|  **FILE_ATTRIBUTE_NOT_CONTENT_INDEXED** 已设定。  | 无控制。 使用 [SetFileAttributes](https://learn.microsoft.com/zh-cn/windows/desktop/api/FileAPI/nf-fileapi-setfileattributesa) 清除。  |  
|  **FILE_ATTRIBUTE_NOT_CONTENT_INDEXED** 未设置。  | 无控制。 使用 [SetFileAttributes](https://learn.microsoft.com/zh-cn/windows/desktop/api/FileAPI/nf-fileapi-setfileattributesa) 进行设置。  |  
## 相关内容
[CreateFile](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-createfilea)
[DeviceIoControl](https://learn.microsoft.com/zh-cn/windows/win32/api/ioapiset/nf-ioapiset-deviceiocontrol)
[打开文件进行读取或写入](https://learn.microsoft.com/zh-cn/windows/win32/fileio/opening-a-file-for-reading-or-writing)
[SetFileAttributes](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-setfileattributesa)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2026-07-17 


