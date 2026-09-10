---
url: "https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/icacls"
title: "icacls | Microsoft Learn"
scraped_at: 2026-09-10T15:41:08+00:00
---

退出编辑器模式
询问 Learn 询问 Learn
读取模式 [ 使用英语阅读 ](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/icacls) Add to Plans 复制 Markdown
注意
访问此页面需要授权。 可以尝试[登录](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/icacls)或更改目录。 
访问此页面需要授权。 可以尝试更改目录。 
# icacls
  * 适用于: ✅ [Windows Server 2025](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2022](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2019](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows Server 2016](https://learn.microsoft.com/windows-server/get-started/windows-server-release-info), ✅ [Windows 11](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Windows 10](https://learn.microsoft.com/windows/release-health/supported-versions-windows-client), ✅ [Azure Local 2311.2 and later](https://learn.microsoft.com/azure/azure-local/release-information-23h2)


显示或修改指定文件中的任意访问控制列表（DACL），并将存储的 DACL 应用于指定目录中的文件。
Note
此命令将替换已弃用的 [cacls 命令](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/cacls)。
## Syntax

```
icacls name [/save aclfile] [/setowner user] [/findsid Sid] [/verify] [/reset] [/T] [/C] [/L] [/Q]
icacls name [/grant[:r] Sid:perm[...]] [/deny Sid:perm [...]] [/remove[:g|:d]] Sid[...]]] [/setintegritylevel Level:policy[...]] [/T] [/C] [/L] [/Q]
icacls directory [/substitute SidOld SidNew [...]] [/restore aclfile] [/C] [/L] [/Q]

```

### Parameters  
| Parameter  | Description  |  
| --- | --- |  
| `<name>`  | 指定要为其显示或修改 DACL 的文件。  |  
| `<directory>`  | 指定要显示或修改 DACL 的目录。  |  
| /t  | 对当前目录及其子目录中的所有指定文件执行该作。  |  
| /c  | 即使发生文件错误，也会继续该作。 仍然显示错误消息。  |  
| /l  | 对符号链接执行作，而不是对目标执行作。  |  
| /q  | 取消成功消息。  |  
| /救 `<ACLfile>`  | 将所有匹配文件的 DACL 存储到访问控制列表 （ACL） 文件中，以供稍后使用 `/restore`。  |  
| /setowner `<user>`  | 将所有匹配文件的所有者更改为指定用户。  |  
| /findsid `<sid>`  | 查找包含显式提及指定安全标识符 （SID） 的 DACL 的所有匹配文件。  |  
| /verify  | 查找具有非规范或长度与访问控制项（ACE）计数不一致的所有文件。  |  
| /reset  | 将 ACL 替换为所有匹配文件的默认继承 ACL。  |  
| /grant[：r] `<sid>`：`<perm>`  | 授予指定的用户访问权限。 权限替换以前授予的显式权限。 不添加 **：r** 意味着权限被添加到任何先前授予的显式权限中。  |  
| /deny `<sid>`：`<perm>`  | 显式拒绝指定的用户访问权限。 为有状态权限添加显式拒绝 ACE，并删除任何显式授予中的相同权限。  |  
| /remove： g |d `<sid>`  | 从 DACL 中删除指定 SID 的所有匹配项。 此命令还可以使用：
* **g** - 删除对指定 SID 授予的所有权限
* **d** - 删除对指定 SID 的所有拒绝权限
 |  
| /setintegritylevel `<perm><level>`  | 将完整性 ACE 显式添加到所有匹配的文件。 可以将级别指定为：
* **l** - 低
* **m** - 中
* **h** - 高
完整性 ACE 的继承选项可能位于级别之前，并且仅应用于目录。  |  
| /替代 `<sidold>``<sidnew>`  | 将现有 SID （ _sidold_ ） 替换为新 SID （ _sidnew_ ） 。 需要使用 `<directory>` 参数。  |  
| /恢复 `<ACLfile>` /c | /l | /q  | 将存储的 DACL 从 `<ACLfile>` 应用于指定目录中的文件。 需要使用 `<directory>` 参数。  |  
| /inheritancelevel： e |d |r  | 设置继承级别，可以是：
* **e** - 启用继承
* **d** - 禁用继承并复制 ACE
* **r** - 禁用继承并仅删除继承的 ACE
 |  
## Remarks
  * SID 可以采用数字或友好名称形式。 如果使用数字形式，将通配符 ***** 附加到 SID 的开头。
  * 此命令将 ACE 条目的规范顺序保留为：
    * Explicit denials
    * Explicit grants
    * Inherited denials
    * Inherited grants
  * 此选项 `<perm>` 是一个权限掩码，可为基本权限、高级权限或继承权限指定：
    * 一系列简单权限（基本权限），无需使用括号：
      * **N** - 无法访问
      * **F** - 完全访问
      * **M** - 修改访问权限
      * **RX** - 读取和执行访问
      * **R** - 只读访问
      * **W** - 只写访问
      * **D** - 删除访问权限
    * 必须使用括号的特定权限（高级权限）的逗号分隔列表：
      * **DE** - 删除
      * **RC** - 读取控制（读取权限）
      * **WDAC** - 写入 DAC （更改权限）
      * **WO** - 写入所有者（获取所有权）
      * **S** - 同步
      * **AS** - 门禁系统安全
      * **MA** - 允许的最大值
      * **GR** - 通用读取
      * **GW** - 通用写入
      * **GE** - 通用执行
      * **GA** - 通用所有
      * **RD** - 读取数据/列表目录
      * **WD** - 写入数据/添加文件
      * **AD** - 追加数据/添加子目录
      * **REA** - 读取扩展属性
      * **WEA** - 写入扩展属性
      * **X** - 执行/遍历
      * **DC** - 删除子项
      * **RA** - 读取属性
      * **WA** - 写入属性
    * 必须使用括号的继承权限序列：
      * **（I）** - 继承。 ACE 继承自父容器。
      * **（OI）** - 对象继承。 此容器中的对象继承此 ACE。 仅适用于目录。
      * **（CI）** - 容器继承。 此父容器中的容器继承此 ACE。 仅适用于目录。
      * **（IO）** - 仅继承。 ACE 继承自父容器，但不适用于对象本身。 仅适用于目录。
      * **（NP）** - 不传播继承。 ACE 由容器和对象从父容器继承，但不会传播到嵌套容器。 仅适用于目录。


## Examples
若要将 C：\Windows 目录中的所有文件的 DACL 及其子目录保存到 ACLFile 文件，请键入：

```
icacls c:\windows\* /save aclfile /t

```

若要为 C：\Windows 目录及其子目录中存在的 ACLFile 中的每个文件还原 DACL，请键入：

```
icacls c:\windows\ /restore aclfile

```

若要向用户授予对名为 Test1 的文件的 Delete 和 Write DAC 权限，请键入：

```
icacls test1 /grant User1:(d,wdac)

```

若要向 SID S-1-1-0 定义的用户授予对名为 TestFile 的文件的删除和写入 DAC 权限，请键入：

```
icacls TestFile /grant *S-1-1-0:(d,wdac)

```

要将 _高_ 完整性级别应用于目录并确保其文件和子目录都继承此级别，请键入：

```
icacls "myDirectory" /setintegritylevel (CI)(OI)H

```

## Related links


## 反馈
此页面是否有帮助？ 
需要有关本主题的帮助？ 
想要尝试使用 Ask Learn 阐明或指导你完成本主题？ 
询问 Learn 询问 Learn
建议修复？ 
  * Last updated on  2025-08-16 


