---
url: "https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/cipher"
title: "cipher | Microsoft Learn"
scraped_at: 2026-09-10T15:41:37+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/cipher) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/cipher)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# cipher
  * 适用于: ✅ [Windows Server 2025](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2022](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2019](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2016](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows 11](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Windows 10](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Azure Local 2311.2 and later](https://learn.microsoft.com/azure/azure-local/release-information-23h2)


显示或更改 NTFS 卷上的目录和文件的加密。 如果不带参数使用， **cipher** 则显示当前目录及其包含的任何文件的加密状态。
## Syntax

```
cipher [/e | /d | /c] [/s:<directory>] [/b] [/h] [pathname [...]]
cipher /k
cipher /r:<filename> [/smartcard]
cipher /u [/n]
cipher /w:<directory>
cipher /x[:efsfile] [filename]
cipher /y
cipher /adduser [/certhash:<hash> | /certfile:<filename>] [/s:directory] [/b] [/h] [pathname [...]]
cipher /removeuser /certhash:<hash> [/s:<directory>] [/b] [/h] [<pathname> [...]]
cipher /rekey [pathname [...]]

```

### Parameters  
| Parameters  | Description  |  
| --- | --- |  
| /b  | 如果遇到错误，则中止。 默认情况下， **cipher** 即使遇到错误也会继续运行。  |  
| /c  | 显示有关加密文件的信息。  |  
| /d  | 解密指定的文件或目录。  |  
| /e  | 加密指定的文件或目录。 将标记目录，以便之后添加的文件将被加密。  |  
| /h  | 显示具有隐藏属性或系统属性的文件。 默认情况下，这些文件不会加密或解密。  |  
| /k  | 创建用于加密文件系统（EFS）文件的新证书和密钥。 如果指定了 **/k** 参数，则忽略所有其他参数。  |  
| /r：`<filename>` [/智能卡]  | 生成 EFS 恢复代理密钥和证书，然后将其写入 .pfx 文件（包含证书和私钥），以及一个.cer文件（仅包含证书）。 如果指定了 **/smartcard** ，它会将恢复密钥和证书写入智能卡，并且不会生成 .pfx 文件。  |  
| /s:`<directory>`  | 对指定 _目录_ 中的所有子目录执行指定作。  |  
| /u [/n]  | 查找本地驱动器上的所有加密文件。 如果与 **/n** 参数一起使用，则不会进行任何更新。 如果不带 **/n** 使用，则 **/u** 会将用户的文件加密密钥或恢复代理的密钥与当前密钥进行比较，并在它们发生更改时进行更新。 此参数仅适用于 **/n** 。  |  
| /w:`<directory>`  | 从整个卷上可用未使用的磁盘空间中删除数据。 如果使用 **/w** 参数，则忽略所有其他参数。 指定的目录可以位于本地卷中的任何位置。 如果它是装入点或指向另一卷中的目录，则会删除该卷上的数据。  |  
| /x[：efsfile] [`<FileName>`]  | 将 EFS 证书和密钥备份到指定的文件名。 如果与 **：efsfile** 一起使用， **则 /x** 将备份用于加密文件的用户证书。 否则，将备份用户的当前 EFS 证书和密钥。  |  
| /y  | 在本地计算机上显示当前的 EFS 证书缩略图。  |  
| /adduser [/certhash：`<hash>`  | /certfile:`<filename>`]  |  
| /rekey  | 更新指定的加密文件以使用当前配置的 EFS 密钥。  |  
| /removeuser /certhash：`<hash>`  | 从指定文件中删除用户。 为 _/certhash_ 提供的**哈希** 必须是要删除的证书的 SHA1 哈希。  |  
| /?  | 在命令提示符下显示帮助。  |  
### Remarks
  * 如果未加密父目录，则修改文件时，加密文件可能会解密。 因此，加密文件时，还应加密父目录。
  * 管理员可以将.cer文件的内容添加到 EFS 恢复策略，以便为用户创建恢复代理，然后导入 .pfx 文件以恢复单个文件。
  * 可以使用多个目录名称和通配符。
  * 必须在多个参数之间放置空格。


## Examples
若要显示当前目录中每个文件和子目录的加密状态，请键入：

```
cipher

```

加密的文件和目录标有 **E** 。未加密的文件和目录用 **U** 标记。例如，以下输出指示当前目录及其所有内容当前未加密：

```
Listing C:\Users\MainUser\Documents\
New files added to this directory will not be encrypted.
U Private
U hello.doc
U hello.txt

```

若要在上一示例中使用的专用目录上启用加密，请键入：

```
cipher /e private

```

以下输出显示：

```
Encrypting files in C:\Users\MainUser\Documents\
Private             [OK]
1 file(s) [or directorie(s)] within 1 directorie(s) were encrypted.

```

该 **cipher** 命令显示以下输出：

```
Listing C:\Users\MainUser\Documents\
New files added to this directory will not be encrypted.
E Private
U hello.doc
U hello.txt

```

其中 **Private** 目录现在标记为已加密。
### Related links


## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-08-16 


