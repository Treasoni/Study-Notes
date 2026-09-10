---
url: "https://www.cnblogs.com/geekbruce/articles/18905587"
title: "Windows中打开powershell后，出现报错无法加载文件 xxxx，因为在此系统上禁止运行脚本。解决方案详解！ - AlphaGeek - 博客园"
scraped_at: 2026-09-10T15:42:04+00:00
---

#  [Running water never grows stale. So you just have to keep on flowing.](https://www.cnblogs.com/geekbruce)
## 世上无难事，只要肯攀登。


#  [ Windows中打开powershell后，出现报错无法加载文件 xxxx，因为在此系统上禁止运行脚本。解决方案详解！ ](https://www.cnblogs.com/geekbruce/articles/18905587 "发布于 2025-05-31 20:55")
每当打开Powershell后，默认报错如下：
> Windows PowerShell 版权所有 (C) Microsoft Corporation。保留所有权利。
> 尝试新的跨平台 PowerShell https://aka.ms/pscore6
> . : 无法加载文件 C:\Users\Admin\Documents\WindowsPowerShell\profile.ps1，因为在此系统上禁止运行脚本。
> 有关详细信息，请参 阅 https:/go.microsoft.com/fwlink/?LinkID=135170 中的 about_Execution_Policies。
> 所在位置 行:1 字符: 3 + . 'C:\Users\Admin\Documents\WindowsPowerShell\profile.ps1'
> + ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ +
> CategoryInfo : SecurityError: (:) []，PSSecurityException + FullyQualifiedErrorId : UnauthorizedAccess
**Solution:**
报错提示表明我的 Windows PowerShell 脚本执行策略（Execution Policy）被设置为禁止运行脚本（默认情况下可能是 Restricted），因此无法加载 profile.ps1 文件。
要解决这个问题，可以调整 PowerShell 的执行策略。以下是具体步骤：
### 步骤 1：检查当前执行策略
  1. 打开 PowerShell（以管理员身份运行，右键“Windows PowerShell”选择“以管理员身份运行”）。
  2. 输入以下命令查看当前策略：



```
**Get-ExecutionPolicy**
```

如果返回 Restricted，说明脚本运行被禁止。
### 步骤 2：更改执行策略
你可以将执行策略设置为允许运行脚本。推荐选择以下选项之一：
  * **仅运行已签名的脚本（建议）** ： 
    * 设置为 AllSigned，这要求所有脚本（包括 profile.ps1）必须有数字签名。
    * 命令：



```
**Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy AllSigned -Force**
```

  * 优点：提高安全性，只有经过签名的脚本可以运行。
  * 注意：如果你自己编写了 profile.ps1，需要对其进行签名（可使用自签名证书）。


**允许运行所有脚本（不推荐用于生产环境）** ：
  * 设置为 Unrestricted，允许运行所有脚本（包括未签名的）。
  * 命令：



```
**Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted -Force**
```

  *     * 缺点：降低安全性，可能存在运行恶意脚本的风险，仅在开发或测试环境中使用。
  * **仅运行本地脚本（推荐折中方案）** ： 
    * 设置为 RemoteSigned，允许运行本地未签名的脚本，但需要远程脚本有签名。
    * 命令：



```
**Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force**
```

  *     * 优点：兼顾安全性和便利性，适合大多数用户。
  * **说明** ： 
    * -Scope CurrentUser 只影响当前用户，不影响其他用户。
    * -Force 跳过确认提示。


### 步骤 3：验证更改
再次运行以下命令确认策略已更改：

```
**Get-ExecutionPolicy**
```

如果显示为 RemoteSigned、AllSigned 或 Unrestricted，说明设置成功。
### 步骤 4：测试 profile.ps1
  * 重新打开 PowerShell，检查是否还能看到报错。
  * 如果仍有问题，尝试手动加载 profile.ps1：



```
**. 'C:\Users\Admin\Documents\WindowsPowerShell\profile.ps1'**
```

  * 如果报错消失，说明问题已解决。


### 步骤 5：（可选）检查 profile.ps1 文件
  * 如果问题仍然存在，可能是 profile.ps1 文件内容有误。打开该文件（使用记事本或 VS Code）：



```
**notepad C:\Users\Admin\Documents\WindowsPowerShell\profile.ps1**
```

检查是否有语法错误或不兼容的命令。如果不确定内容，可以暂时删除或注释掉（加 #）部分代码，重新测试。
### 注意事项
  * **安全性** ：避免将执行策略设置为 Unrestricted 除非你完全信任你的环境。
  * **管理员权限** ：如果需要为所有用户更改策略，使用 -Scope LocalMachine 代替 -Scope CurrentUser，但需以管理员身份运行。
  * **重置策略** ：如果想恢复默认设置，可以重新设置为 Restricted：



```
**Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Restricted -Force**
```

### 总结
通过将 PowerShell 的执行策略从 Restricted 更改为 RemoteSigned（或其他适合的策略），可以取消该报错。
推荐使用 **RemoteSigned** 作为折中方案，确保安全性并允许本地脚本运行。
其他类似问题，参考资料
[1] <https://blog.csdn.net/qq_45689957/article/details/138576370>
posted @ 2025-05-31 20:55 [AlphaGeek](https://www.cnblogs.com/geekbruce) 阅读(14262) 评论(0) [收藏](javascript:void\(0\)) [举报](https://report.cnblogs.com?targetLink=https%3A%2F%2Fwww.cnblogs.com%2Fgeekbruce%2Farticles%2F18905587&targetId=18905587&targetType=0)
[博客园](https://www.cnblogs.com/) © 2004-2026 [浙公网安备 33010602011771号](http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=33010602011771) [浙ICP备2021040463号-3](https://beian.miit.gov.cn)
