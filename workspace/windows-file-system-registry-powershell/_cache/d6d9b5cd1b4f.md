---
url: "https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/reg-restore"
title: "reg restore | Microsoft Learn"
scraped_at: 2026-09-10T15:41:16+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/reg-restore) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/reg-restore)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# reg restore
  * 适用于: ✅ [Windows Server 2025](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2022](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2019](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2016](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows 11](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Windows 10](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Azure Local 2311.2 and later](https://learn.microsoft.com/azure/azure-local/release-information-23h2)


将保存的子项和条目写回注册表。
## Syntax

```
reg restore <keyname> <filename>

```

### Parameters  
| Parameter  | Description  |  
| --- | --- |  
| `<keyname>`  | 指定要还原的子项的完整路径。 还原作仅适用于本地计算机。 _密钥名_ 必须包含有效的根密钥。 本地计算机的有效根密钥为：**HKLM** 、**HKCU、****HKCR、****HKU** 和 **HKCC** 。 如果注册表项名称包含空格，请将密钥名称括在引号中。  |  
| `<filename>`  | 指定要写入注册表的内容的文件的名称和路径。 此文件必须使用 **reg save** 命令提前创建，并且必须具有 .hiv 扩展名。  |  
| /?  | 在命令提示符下显示帮助。  |  
#### Remarks
  * 在编辑任何注册表项之前，必须使用 **reg save** 命令保存父子项。 如果编辑失败，则可以使用 **reg restore** 作还原原始子项。
  * **reg 还原** 作的返回值为：  
| Value  | Description  |  
| --- | --- |  
| 0  | Success  |  
| 1  | Failure  |  


### Examples
要将名为 NTRKBkUp.hiv 的文件还原到密钥 HKLM\Software\Microsoft\ResKit，并覆盖密钥的现有内容，请键入：

```
reg restore HKLM\Software\Microsoft\ResKit NTRKBkUp.hiv

```

## Related links
  *   * [reg save 命令](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/reg-save)


## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-08-16 


