---
url: "https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/mountvol"
title: "mountvol | Microsoft Learn"
scraped_at: 2026-09-10T15:41:26+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/mountvol) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/mountvol)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# mountvol
  * 适用于: ✅ [Windows Server 2025](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2022](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2019](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2016](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows 11](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Windows 10](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Azure Local 2311.2 and later](https://learn.microsoft.com/azure/azure-local/release-information-23h2)


创建、删除或列出卷装入点。 还可以链接卷，而无需驱动器号。
## Syntax

```
mountvol [<drive>:]<path volumename>
mountvol [<drive>:]<path> /d
mountvol [<drive>:]<path> /l
mountvol [<drive>:]<path> /p
mountvol /r
mountvol [/n|/e]
mountvol <drive>: /s

```

### Parameters  
| Parameter  | Description  |  
| --- | --- |  
| `[<drive>:]<path>`  | 指定装入点将驻留的现有 NTFS 目录。  |  
| `<volumename>`  | 指定是装入点目标的卷名称。 卷名称使用以下语法，其中 _GUID_ 是全局唯一标识符： `\\?\volume\{GUID}\`。 需要括号 `{ }`。  |  
| /d  | 从指定的文件夹中删除卷装入点。  |  
| /l  | 列出指定文件夹的已装载卷名称。  |  
| /p  | 从指定的目录中删除卷装入点，卸载基本卷，使基本卷脱机，使其不可装载。 如果其他进程正在使用该卷，则 **mountvol** 会在卸载卷之前关闭所有打开的句柄。  |  
| /r  | 删除不再在系统中的卷的卷装入点目录和注册表设置，防止它们自动装载，并在将以前的卷装入点（s）添加到系统时提供这些目录和注册表设置。  |  
| /n  | 禁用新基本卷的自动装载。 添加到系统时，不会自动装载新卷。  |  
| /e  | 重新启用新基本卷的自动装载。  |  
| /s  | 将 EFI 系统分区装载到指定的驱动器上。  |  
| /?  | 在命令提示符下显示帮助。  |  
## Remarks
  * 如果在使用 **/p** 参数时卸载卷，则卷列表会将卷显示为未挂载，直到创建卷装载点。
  * 如果卷有多个挂载点，请在使用 **/p** 之前使用 **/d** 删除其他挂载点。 可以通过分配卷装入点使基本卷可再次装载。
  * 如果需要在不重新格式化或替换硬盘驱动器的情况下扩展卷空间，可以将装载路径添加到另一卷。 将一个卷与多个装载路径结合使用的好处是，可以使用单个驱动器号（如 `C:`）访问所有本地卷。 无需记住哪个卷对应于哪个驱动器号，尽管你仍然可以装载本地卷并为其分配驱动器号。


## Examples
若要创建装入点，请键入：

```
mountvol \sysmount \\?\volume\{2eca078d-5cbc-43d3-aff8-7e8511f60d0e}\

```

## Related links


## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-08-16 


