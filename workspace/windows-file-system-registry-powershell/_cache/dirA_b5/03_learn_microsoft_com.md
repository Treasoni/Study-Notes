---
url: "https://learn.microsoft.com/zh-cn/windows/win32/fileio/hard-links-and-junctions"
title: "硬链接和接合 - Win32 apps | Microsoft Learn"
scraped_at: 2026-09-10T15:42:00+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows/win32/fileio/hard-links-and-junctions) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows/win32/fileio/hard-links-and-junctions)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# 硬链接和交接点
NTFS 文件系统支持三种类型的文件链接：硬链接、交接点和符号链接。 本文概述了硬链接和接合。 有关符号链接的信息，请参阅 [“创建符号链接](https://learn.microsoft.com/zh-cn/windows/win32/fileio/creating-symbolic-links)”。
## 硬链接
_硬链接_ 是文件的文件系统表示形式，其中多个路径引用同一卷中的单个文件。 若要创建硬链接，请使用 [CreateHardLinkA](https://learn.microsoft.com/zh-cn/windows/win32/api/WinBase/nf-winbase-createhardlinka) 函数。
对硬链接文件所做的任何更改都对通过引用该文件的链接访问该文件的应用程序立即可见。 文件上的属性反映在该文件的每个硬链接中，对该文件的属性的更改将传播到所有硬链接。 但是，目录条目大小和文件 _属性信息仅在进行更改的链接处明显_ 更新。 例如，如果清除特定硬链接上的只读属性标志，以便可以删除该硬链接，并且文件有多个硬链接，则其他硬链接显示只读属性仍设置，但事实并非如此。 若要将文件更改回只读状态，必须从文件剩余的硬链接之一设置该文件上的只读标志。
例如，在本地`C:``D:`驱动器和`Z:`网络驱动器映射到`\\fred\share`的系统中，允许将以下引用作为硬链接：
  * `C:\dira\ethel.txt` 链接到 `C:\dirb\dirc\lucy.txt`
  * `D:\dir1\tinker.txt` 链接到 `D:\dir2\dirx\bell.txt`
  * `C:\diry\bob.bak` 链接到 `C:\dir2\mina.txt`


这是因为所有链接都是同一卷上的文件。 硬链接不能引用目录，只能引用文件，也不能引用不同卷上的文件。
不允许使用以下引用：
  * `C:\dira` 链接到 `C:\dirb`
  * `C:\dira\ethel.txt` 链接到 `D:\dirb\lucy.txt`
  * `C:\dira\ethel.txt` 链接到 `Z:\dirb\lucy.txt`


若要删除硬链接，请使用 [DeleteFileA](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-deletefilea) 函数。 无论链接的创建顺序如何，都可以按任意顺序删除硬链接。
## 交接点
_交接点_ （也称为 _软链接）不同于硬链接_ ，因为它引用的存储对象是单独的目录。 交接点还可以链接位于同一计算机上的不同本地卷上的目录。 否则，交汇点的工作方式与硬链接相同。 交接点通过 [重新分析点](https://learn.microsoft.com/zh-cn/windows/win32/fileio/reparse-points)实现。
假设硬链接部分中的条件相同，则允许将以下引用作为交接点：
  * `C:\dira` 链接到 `C:\dirb\dirc`
  * `C:\dirx` 链接到 `D:\diry`


不允许使用以下引用，因为它们引用映射的网络卷，或者直接引用文件：
  * `C:\dira\one.txt` 链接到 `C:\dirb\two.txt`
  * `C:\dir1` 链接到 `Z:\dir2`


## 相关内容


## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-07-08 


