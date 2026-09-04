---
url: "https://learn.microsoft.com/zh-cn/windows/wsl/compare-versions"
title: "比较 WSL 版本 | Microsoft Learn"
scraped_at: 2026-09-04T15:57:07+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows/wsl/compare-versions) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows/wsl/compare-versions)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# 比较 WSL 版本
详细了解不同的 WSL 版本，包括为什么 WSL 2 现在是默认版本，以及可能需要将已安装的 Linux 分发版切换到早期 WSL 1 体系结构的特定方案或异常。
## 比较 WSL 1 和 WSL 2
本指南将比较 WSL 1 和 WSL 2，包括 [选择使用 WSL 1 而非 WSL 2 的例外情况](https://learn.microsoft.com/zh-cn/windows/wsl/compare-versions#exceptions-for-using-wsl-1-rather-than-wsl-2)。 WSL 1 和 WSL 2 之间的主要区别是使用托管 VM 内的实际 Linux 内核、支持完整的系统调用兼容性，以及跨 Linux 和 Windows作系统的性能。 WSL 2 是安装 Linux 分发版时的当前默认版本，使用最新的虚拟化技术在轻型实用工具虚拟机（VM）内运行 Linux 内核。 WSL2 以托管 VM 中的独立容器的形式运行 Linux 分发版。 如果分发版当前正在运行 WSL 1，并且想要更新到 WSL 2，请参阅 [从 WSL 1 更新到 WSL 2](https://learn.microsoft.com/zh-cn/windows/wsl/install#upgrade-version-from-wsl-1-to-wsl-2)。
### 比较功能  
| 功能 / 特点  | WSL 1  | WSL 2  |  
| --- | --- | --- |  
| Windows 与 Linux 之间的集成  | ✅  | ✅  |  
| 快速启动时间  | ✅  | ✅  |  
| 与传统虚拟机相比，资源占用很小  | ✅  | ✅  |  
| 使用 VMware 和 VirtualBox 的当前版本运行  | ✅  | ❌  |  
| 托管 VM  | ❌  | ✅  |  
| 完整 Linux 内核  | ❌  | ✅  |  
| 完整的系统调用兼容性  | ❌  | ✅  |  
| 跨 OS 文件系统的性能  | ✅  | ❌  |  
| systemd 支持  | ❌  | ✅  |  
| IPv6 支持  | ✅  | ✅  |  
如上面的比较表所示，WSL 2 体系结构在多种方面优于 WSL 1，但在不同操作系统的文件系统的性能方面除外，这可以通过将项目文件存储在与运行项目工具相同的操作系统上来解决。
WSL 2 仅在 Windows 11 或 Windows 10 版本 1903 版本 18362 或更高版本中可用。 通过选择 **Windows 徽标键 + R** 来检查 Windows 版本，键入 **winver** ，选择“ **确定** ”。 （或在 Windows 命令提示符中输入 `ver` 命令）。 可能需要 [更新到最新的 Windows 版本](ms-settings:windowsupdate)。 对于低于 14393 的版本，WSL 根本不支持。
有关最新的 WSL 2 更新的详细信息，请参阅 [Windows 命令行博客](https://devblogs.microsoft.com/commandline/)，包括 [Systemd 支持现已在 WSL 和 WSL](https://devblogs.microsoft.com/commandline/systemd-support-is-now-available-in-wsl/)[2023 年 9 月更新](https://devblogs.microsoft.com/commandline/windows-subsystem-for-linux-september-2023-update/) 中提供，了解有关 IPv6 支持的详细信息。
注释
WSL 2 将与 [VMware 15.5.5+](https://blogs.vmware.com/workstation/2020/05/vmware-workstation-now-supports-hyper-v-mode.html) 配合使用，尽管 [VirtualBox 6+](https://www.virtualbox.org/wiki/Changelog-6.0) 指出存在 WSL 支持，但仍存在重大挑战，因此不支持它。 在我们的[常见问题解答中](https://learn.microsoft.com/zh-cn/windows/wsl/faq#will-i-be-able-to-run-wsl-2-and-other-3rd-party-virtualization-tools-such-as-vmware--or-virtualbox-)了解详细信息。
## WSL 2 中的新增功能
WSL 2 是对基础体系结构的重大改革，它使用虚拟化技术和 Linux 内核来启用新功能。 此更新的主要目标是提高文件系统性能并添加完整的系统调用兼容性。
  * [将 Linux 分发版本从 WSL 1 设置为 WSL 2](https://learn.microsoft.com/zh-cn/windows/wsl/basic-commands#set-wsl-version-to-1-or-2)
  * [有关 WSL 2 的常见问题](https://learn.microsoft.com/zh-cn/windows/wsl/faq)


### WSL 2 体系结构
传统的 VM 体验启动速度可能很慢，是隔离的，会消耗大量资源，并且需要时间来管理它。 WSL 2 没有这些属性。
WSL 2 提供 WSL 1 的优势，包括 Windows 和 Linux 之间的无缝集成、快速启动时间、少量的资源占用，并且不需要 VM 配置或管理。 虽然 WSL 2 确实使用 VM，但它在后台进行管理和运行，使你拥有与 WSL 1 相同的用户体验。
### 完整 Linux 内核
WSL 2 中的 Linux 内核由 Microsoft 基于最新稳定分支构建，该分支的源代码可从 [kernel.org](https://kernel.org) 获取。此内核已专门针对 WSL 2 进行优化，以便在 Windows 上提供卓越的 Linux 体验，特别是在尺寸和性能方面进行了优化。 内核将由 Windows 更新提供服务，这意味着你将获得最新的安全修补程序和内核改进，而无需自行管理它。
[WSL 2 Linux 内核是开放源代码](https://github.com/microsoft/WSL2-Linux-Kernel)。 若要了解更多内容，请查看由构建该内核的团队编写的博客文章《[Windows 发布 Linux 内核](https://devblogs.microsoft.com/commandline/shipping-a-linux-kernel-with-windows/)》。
在 [适用于 Linux 的 Windows 子系统内核的发行说明](https://learn.microsoft.com/zh-cn/windows/wsl/kernel-release-notes)中了解详细信息。
### 提高了文件 IO 性能
WSL 2 的文件密集型操作（例如`git clone`、`npm install`、`apt update`、`apt upgrade`等）都明显更快。
实际速度提高取决于正在运行的应用以及它与文件系统的交互方式。 WSL 2 的初始版本在解压缩压缩的 tarball 时运行速度比 WSL 1 快最多达到 20 倍，在使用 `git clone`、`npm install` 和 `cmake` 处理各种项目时速度提高约为 2-5 倍。
### 完整的系统调用兼容性
Linux 二进制文件使用系统调用来执行访问文件、请求内存、创建进程等功能。 而 WSL 1 使用了由 WSL 团队生成的转换层，但 WSL 2 包含其自己的 Linux 内核，具有完整的系统调用兼容性。 优点包括：
  * 可以在 WSL 内部运行的一组全新的应用，例如 等。
  * Linux 内核的任何更新都立即可供使用（无需等待 WSL 团队实现更新并添加更改）。


## 使用 WSL 1 而不是 WSL 2 的异常
建议使用 WSL 2，因为它提供更快的性能和 100% 系统调用兼容性。 但是，在某些情况下，你可能更喜欢使用 WSL 1。 如果以下情况，请考虑使用 WSL 1：
  * 项目文件必须存储在 Windows 文件系统中。 WSL 1 可更快地访问从 Windows 装载的文件。 
    * 如果你将使用 WSL Linux 分发版访问 Windows 文件系统上的项目文件，并且这些文件不能存储在 Linux 文件系统上，则通过使用 WSL 1，你将在 OS 文件系统中实现更快的性能。
  * 需要在同一文件中使用 Windows 和 Linux 工具进行交叉编译的项目。 
    * 在 WSL 1 中，跨 Windows 和 Linux作系统的文件性能比 WSL 2 更快，因此，如果使用 Windows 应用程序访问 Linux 文件，则目前 WSL 1 的性能将更快。
  * 项目需要访问串行端口或 USB 设备。 _然而_ USB 设备支持现已通过 `USBIPD-WIN` 项目用于 WSL 2。 有关设置步骤，请参阅 [连接 USB 设备](https://learn.microsoft.com/zh-cn/windows/wsl/connect-usb) 。
  * WSL 2 不包括对访问串行端口的支持。 在 [常见问题解答](https://learn.microsoft.com/zh-cn/windows/wsl/faq#can-i-access-the-gpu-in-wsl-2--are-there-plans-to-increase-hardware-support-) 或 [WSL GitHub 存储库中详细了解串行支持问题](https://github.com/microsoft/WSL/issues/4322)。
  * 内存要求严格 
    * WSL 2 的内存使用量在使用它时会增大和收缩。 当进程释放内存时，会自动返回到 Windows。 但是，截至现在，WSL 2 在关闭 WSL 实例之前，尚未将内存中的缓存页释放回 Windows。 如果长时间运行 WSL 会话或访问大量文件，此缓存可能会占用 Windows 上的内存。 我们正在跟踪改进 [WSL GitHub 存储库问题 4166](https://github.com/microsoft/WSL/issues/4166) 上的此体验的工作。
  * 对于使用 VirtualBox 的用户，请务必使用最新版本的 VirtualBox 和 WSL 2。 请参阅 [相关的常见问题解答](https://learn.microsoft.com/zh-cn/windows/wsl/faq#will-i-be-able-to-run-wsl-2-and-other-3rd-party-virtualization-tools-such-as-vmware--or-virtualbox-)。
  * 如果您依赖 Linux 发行版在与主机相同的网络中获取 IP 地址，那么可能需要设置一个解决方案才能运行 WSL 2。 WSL 2 作为 Hyper-V 虚拟机运行。 这是 WSL 1 中使用的桥接网络适配器的更改，这意味着 WSL 2 对其虚拟网络使用网络地址转换（NAT）服务，而不是将其桥接到主机网络接口卡（NIC），从而导致在重启时更改的唯一 IP 地址。 若要详细了解将 WSL 2 服务的 TCP 端口转发到主机 OS 的问题和解决方法，请参阅 [WSL GitHub 存储库问题 4150、NIC 桥模式（TCP 解决方法）。](https://github.com/microsoft/WSL/issues/4150)


注释
请考虑尝试使用 VS Code [远程 WSL 扩展](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) 将项目文件存储在 Linux 文件系统上，使用 Linux 命令行工具，还可以在 Windows 上使用 VS Code 在 Internet 浏览器中创作、编辑、调试或运行项目，而无需与在 Linux 和 Windows 文件系统中工作相关的任何性能降低。 [了解详细信息](https://learn.microsoft.com/zh-cn/windows/wsl/tutorials/wsl-vscode)。
## Microsoft 商店中的 WSL
WSL 已将更新功能从 Windows OS 映像中移出，并包含在微软应用商店提供的包中。 这意味着，一旦更新和服务可用，您将可以立即获得更新和服务，而无需等待您的Windows操作系统更新。
WSL 最初作为需要启用的可选组件包含在 Windows作系统中，以便安装 Linux 分发版。 应用商店中的 WSL 具有相同的用户体验，并且是相同的产品，但接收更新和服务作为应用商店包，而不是作为整个 OS 更新。 从 Windows 版本 19044 或更高版本开始，运行 `wsl.exe --install` 此命令将从 Microsoft 应用商店安装 WSL 服务更新。 （[请参阅宣布此更新的博客文章](https://devblogs.microsoft.com/commandline/the-windows-subsystem-for-linux-in-the-microsoft-store-is-now-generally-available-on-windows-10-and-11)）。 如果已在使用 WSL，则可以更新以确保通过运行 `wsl.exe --update`，从应用商店接收最新的 WSL 功能和服务。
注释
如果组织中无法访问Microsoft应用商店，则仍可以通过追加 `--web-download` 到 `--update` 命令来利用此 WSL 版本，例如 `wsl --update --web-download`。 每次有新版本推出时，您需要手动使用此方法更新 WSL。
在 GitHub 上与我们协作 
可以在 GitHub 上找到此内容的源，还可以在其中创建和查看问题和拉取请求。 有关详细信息，请参阅[参与者指南](https://learn.microsoft.com/contribute/content/how-to-write-quick-edits)。 
Windows Subsystem for Linux 
[ 提出文档问题 ](https://learn.microsoft.com/zh-cn/windows/wsl/compare-versions) [ 提供产品反馈 ](https://github.com/microsoft/WSL/issues)
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-06-10 


