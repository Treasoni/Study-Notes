---
url: "https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/mklink"
title: "mklink | Microsoft Learn"
scraped_at: 2026-09-10T15:41:08+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/mklink) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/mklink)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# mklink
  * 适用于: ✅ [Windows Server 2025](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2022](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2019](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2016](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows 11](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Windows 10](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Azure Local 2311.2 and later](https://learn.microsoft.com/azure/azure-local/release-information-23h2)


创建目录或文件符号或硬链接。
## Syntax

```
mklink [[/d] | [/h] | [/j]] <link> <target>

```

### Parameters  
| Parameter  | Description  |  
| --- | --- |  
| /d  | 创建目录符号链接。 默认情况下，此命令将创建文件符号链接。  |  
| /h  | 创建硬链接而不是符号链接。  |  
| /j  | 创建目录交接点。  |  
| `<link>`  | 指定要创建的符号链接的名称。  |  
| `<target>`  | 指定新符号链接引用的路径（相对或绝对）。  |  
| /?  | 在命令提示符下显示帮助。  |  
### Examples
若要从根目录创建和删除名为 MyFolder 的符号链接到 \Users\User1\Documents 目录，并将名为 Myfile.file 的硬链接创建和删除到位于该目录中的 example.file 文件的硬链接，请键入：

```
mklink /d \MyFolder \Users\User1\Documents
mklink /h \MyFile.file \User1\Documents\example.file
rd \MyFolder
del \MyFile.file

```

## Related links
  *   * [del command](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/del)
  * [rd command](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/rd)
  * Windows PowerShell [中的](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/new-item?view=powershell-6&preserve-view=true)New-Item


## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-07-13 


