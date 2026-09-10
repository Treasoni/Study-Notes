---
url: "https://learn.microsoft.com/zh-cn/windows/win32/fileio/file-encryption"
title: "文件加密 - Win32 apps | Microsoft Learn"
scraped_at: 2026-09-10T15:42:00+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows/win32/fileio/file-encryption) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows/win32/fileio/file-encryption)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# 文件加密
加密文件系统（EFS）为文件和目录提供了额外的安全级别。 它使用公钥系统为 NTFS 文件系统卷上的单个文件提供加密保护。
通常，对 Windows 安全模型提供的文件和目录对象的访问控制足以保护对敏感信息的未经授权的访问。 但是，如果包含敏感数据的笔记本电脑丢失或被盗，则可能会泄露该数据的安全保护。 加密文件会增加安全性。
## 使用 EFS
若要确定文件系统是否支持文件和目录的文件加密，请调用 [GetVolumeInformation](https://learn.microsoft.com/zh-cn/windows/win32/api/FileAPI/nf-fileapi-getvolumeinformationa) 函数并检查 **FS_FILE_ENCRYPTION** 位标志。 请注意，无法加密以下项：
  * 压缩文件
  * 系统文件
  * 系统目录
  * 根目录
  * 交易


可以加密稀疏文件。
TxF 不支持加密文件系统 （EFS） 文件上的大多数作。 TxF 支持的唯一操作是读取操作，例如 [ReadEncryptedFileRaw](https://learn.microsoft.com/zh-cn/windows/win32/api/WinBase/nf-winbase-readencryptedfileraw)。
注意
加密源文件后，**CopyFile** 和 **CopyFileEx** 依赖于 EFS 服务（托管在 lsass.exe中）来创建目标文件，并应用用于源文件加密的密钥。 这些作由 EFS 服务执行，同时模拟 **CopyFile** 或 **CopyFileEx** 调用方。
## 在本部分中
以下主题提供有关文件加密的信息：  
| 主题  | 描述  |  
| --- | --- |  
| 标记为加密的文件是使用当前加密驱动程序由 NTFS 文件系统加密的。  |  
| 列出用于创建新密钥、向加密文件添加密钥、查询加密文件的密钥以及从加密文件中删除密钥的函数。  |  
| 原始加密功能启用加密文件的备份。  |  
有关加密的详细信息，请参阅 [将用户添加到加密文件](https://learn.microsoft.com/zh-cn/windows/win32/fileio/adding-users-to-an-encrypted-file)。
有关加密的详细信息，请参阅 [加密](https://learn.microsoft.com/zh-cn/windows/desktop/SecCrypto/cryptography-portal)。
## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-07-10 


