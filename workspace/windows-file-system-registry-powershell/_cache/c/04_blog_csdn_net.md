---
url: "https://blog.csdn.net/chao_666666/article/details/156590250"
title: "解决 PowerShell 中文乱码问题-CSDN博客"
scraped_at: 2026-09-10T15:42:04+00:00
---

# 解决 PowerShell 中文乱码问题
原创 已于 2026-01-06 22:35:55 修改 · 1.6k 阅读 · ·
本内容遵循CC 4.0 BY-SA版权协议
版权声明：本文为博主原创文章，遵循[ CC 4.0 BY-SA ](http://creativecommons.org/licenses/by-sa/4.0/)版权协议，转载请附上原文出处链接和本声明。 
[ GEO检测 ](https://mp.csdn.net/geo?title=%E8%A7%A3%E5%86%B3+PowerShell+%E4%B8%AD%E6%96%87%E4%B9%B1%E7%A0%81%E9%97%AE%E9%A2%98&url=https%3A%2F%2Fblog.csdn.net%2Fchao_666666%2Farticle%2Fdetails%2F156590250&utm_source=blog_geo)
·
收录于
当前文章被以下社区和专栏收录：
于 2026-01-05 09:19:27 首次发布
##  解决 PowerShell 中文乱码问题
###  问题现象
在使用 PowerShell 时,经常遇到中文显示乱码的问题:

```
UTF-8 缂栫爜宸查厤缃畬鎴愶紒

```

这不仅影响阅读体验,还会导致中文文件名、日志输出等问题。
###  根本原因
PowerShell 中文乱码的根本原因是**编码不一致** :
  1. **控制台代码页** : 默认使用 GBK (代码页 936),而脚本文件使用 UTF-8
  2. **配置文件编码** : PowerShell Profile 的编码与控制台编码不匹配
  3. **加载时机问题** : 配置文件在编码设置之前就已经加载了


###  完整解决方案
####  方案一:修改 PowerShell Profile (适用于普通 PowerShell)
#####  1. 创建或编辑 PowerShell Profile
首先检查 Profile 是否存在:

```
Test-Path $PROFILE

```

如果不存在,创建它:

```
New-Item -Path $PROFILE -ItemType File -Force

```

#####  2. 编辑 Profile 文件
使用记事本打开:

```
notepad $PROFILE

```

**⚠️ 重要** : 文件必须以 **UTF-8 BOM** 格式保存!
添加以下内容:

```
# PowerShell UTF-8 Encoding Configuration
# =============================================

# Set console encoding to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Set code page to UTF-8
chcp 65001 | Out-Null

# Set default parameter encoding
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

```

#####  3. 保存为 UTF-8 BOM 格式
在记事本中保存时:
  1. 点击 “另存为”
  2. 在编码下拉框中选择 “UTF-8”
  3. 保存文件


####  方案二:修改 Windows Terminal 配置 (推荐)
如果你使用 **Windows Terminal** ,这是最优雅的解决方案。
#####  1. 找到配置文件
配置文件位置:

```
%LocalAppData%\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json

```

或直接在 Windows Terminal 中按 `Ctrl + ,` 打开设置。
#####  2. 修改 PowerShell 配置
找到 `"profiles"` -> `"list"` 中的 PowerShell 配置,修改 `"commandline"`:

```
{
    "commandline": "%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -NoExit -Command \"chcp 65001 | Out-Null; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; [Console]::InputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [System.Text.Encoding]::UTF8\"",
    "guid": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}",
    "hidden": false,
    "name": "Windows PowerShell"
}

```

#####  3. 修改 Anaconda PowerShell 配置 (如果使用)

```
{
    "commandline": "%WINDIR%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -NoExit -Command \"chcp 65001 | Out-Null; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; [Console]::InputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [System.Text.Encoding]::UTF8; & 'C:\\path\\to\\anaconda3\\shell\\condabin\\conda-hook.ps1' ; conda activate 'C:\\path\\to\\anaconda3' \"",
    "name": "Anaconda PowerShell Prompt (anaconda3)",
    "icon": "C:\\path\\to\\anaconda3\\Menu\\anaconda_powershell_prompt.ico",
    "startingDirectory": "C:\\Users\\YourUsername"
}

```

#####  4. 设置中文字体 (推荐)
在 `"profiles"` -> `"defaults"` 中添加:

```
"profiles": {
    "defaults": {
        "font": {
            "face": "Microsoft YaHei UI"
        }
    },
    "list": [
        // ...
    ]
}

```

完整配置示例:

```
{
    "$help": "https://aka.ms/terminal-documentation",
    "$schema": "https://aka.ms/terminal-profiles-schema",
    "profiles": {
        "defaults": {
            "font": {
                "face": "Microsoft YaHei UI"
            }
        },
        "list": [
            {
                "commandline": "%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -NoExit -Command \"chcp 65001 | Out-Null; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; [Console]::InputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [System.Text.Encoding]::UTF8\"",
                "guid": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}",
                "hidden": false,
                "name": "Windows PowerShell"
            }
        ]
    }
}

```

####  方案三:通过注册表设置 (全局生效)
以管理员身份运行 PowerShell:

```
# 设置当前用户的控制台代码页
New-Item -Path 'HKCU:\Console' -Force | Out-Null
Set-ItemProperty -Path 'HKCU:\Console' -Name 'CodePage' -Value 65001 -Type DWord

```

###  验证修复
重新打开 PowerShell,运行测试命令:

```
Write-Host "测试中文显示: 你好世界! 🎉"

```

应该看到正确的输出:

```
测试中文显示: 你好世界! 🎉

```

###  常见问题
####  Q1: 为什么修改 Profile 后还是乱码?
**A** : Profile 文件本身的编码必须是 UTF-8 BOM 格式。如果使用普通文本编辑器,可能保存为 ANSI 或其他编码。
**解决方法** :
  1. 使用 PowerShell 命令创建 UTF-8 BOM 文件:


```
$content = @'
# Your content here
'@
$utf8WithBom = New-Object System.Text.UTF8Encoding $True
[System.IO.File]::WriteAllText($PROFILE, $content, $utf8WithBom)

```

  1. 或使用支持 UTF-8 BOM 的编辑器 (如 VS Code) 保存。


####  Q2: Windows Terminal 配置修改后不生效?
**A** : 确保 JSON 格式正确,没有语法错误。
**解决方法** :
  1. 使用 JSON 验证工具检查格式
  2. 完全关闭 Windows Terminal 后重新打开


####  Q3: 每次打开都要手动运行 `chcp 65001`?
**A** : 这说明配置没有正确加载。
**解决方法** :
  1. 检查 Profile 文件路径: `echo $PROFILE`
  2. 确认 Profile 存在: `Test-Path $PROFILE`
  3. 如果使用 Windows Terminal,使用方案二


###  技术原理
####  代码页 (Code Page)
  * **936** : GBK 编码 (简体中文默认)
  * **65001** : UTF-8 编码 (国际标准)


PowerShell 5.x 及以下版本默认使用系统代码页,通常中文 Windows 是 GBK。
####  BOM (Byte Order Mark)
UTF-8 BOM 是文件开头的三个字节 `EF BB BF`,用于标识文件编码。
PowerShell 需要 BOM 来正确识别 Profile 文件的编码,否则会使用系统默认编码 (GBK) 读取,导致中文乱码。
####  编码优先级

```
Windows Terminal commandline > PowerShell Profile > 注册表设置 > 系统默认

```

这就是为什么在 Windows Terminal 中设置最有效。
###  最佳实践
  1. **使用 Windows Terminal** : 更好的渲染、配置灵活
  2. **统一使用 UTF-8** : 脚本文件、配置文件全部使用 UTF-8 BOM
  3. **设置中文字体** : Microsoft YaHei UI 或 Cascadia Code
  4. **版本控制** : PowerShell Core (6+) 默认使用 UTF-8,问题较少


###  相关资源
  * [Windows Terminal 文档](https://aka.ms/terminal-documentation)


###  总结
PowerShell 中文乱码是编码不一致导致的。通过以下三步可以彻底解决:
  1. ✅ 设置控制台代码页为 UTF-8 (65001)
  2. ✅ 配置 PowerShell 使用 UTF-8 编码
  3. ✅ 确保配置文件使用 UTF-8 BOM 格式保存


**推荐方案** : 使用 Windows Terminal + 修改 `settings.json`,一次配置,永久生效。
**发布日期** : 2025-01-05 **适用版本** : Windows PowerShell 5.x, PowerShell Core 6+, Windows Terminal **测试环境** : Windows 10/11
标签
确定要放弃本次机会？ 
福利倒计时
立减 ¥
普通VIP年卡可用
[立即使用](https://mall.csdn.net/vip)
[ chao_666666  ](https://blog.csdn.net/chao_666666)
  * 觉得还不错? 
  * 

[ 新学期领福利！购实物周边送年卡会员！ ](https://mall.csdn.net/vip?utm_source=260904_vip_T1)
[ T恤、键盘、双肩包等周边任选！还能解锁资源下载、VIP文章等多重会员权益！ ](https://mall.csdn.net/vip?utm_source=260904_vip_T1)
参与评论 您还未登录，请先 登录 后发表或查看评论
[ _Powershell_ 7.x中UTF-8环境 _中文_ _乱码_ _解决_ 办法 ](https://blog.csdn.net/shadow_zed/article/details/126396983)
08-18
[ _Powershell_ 7 _中文_ _乱码_ _问题_ _解决_ ](https://blog.csdn.net/shadow_zed/article/details/126396983)
[ _解决_ Windows终端 _PowerShell_ 展示 _乱码_ 的 _问题_ ](https://iteacher.blog.csdn.net/article/details/139149008)
[h a 6 6 6 c k 为 你解决复杂难题！](https://blog.csdn.net/HQ354974212)
05-23
[ 标题： _解决_ Windows终端 _PowerShell_ 展示 _乱码_ 的 _问题_ 在使用Windows终端中的 _PowerShell_ 时，有时会遇到 _乱码_ 显示的 _问题_ ，这可能会给用户带来困扰。这种 _问题_ 通常与字符编码设置有关，因为不同的字符编码会导致终端无法正确显示特定语言或特殊字符。在本文中，我们将介绍如何 _解决_ Windows终端 _PowerShell_ 中 _乱码_ 显示的 _问题_ ，并详细说明各种字符编码的数字表示，以及相关命令的用法。 ](https://iteacher.blog.csdn.net/article/details/139149008)
[ 如何 _解决_ vscode _powershell_ _乱码_ ](https://blog.csdn.net/u012386311/article/details/144566005)
12-18
[ 在 Visual Studio Code 中使用 _PowerShell_ 时出现 _乱码_ ，通常是由于终端编码设置或字体不匹配导致的。 _PowerShell_ 默认的输出编码可能与终端编码不一致。通过以上方法，通常可以 _解决_ VSCode 中 _PowerShell_ 的 _乱码_ _问题_ 。确保你使用的是最新版本的 _PowerShell_ ，因为旧版本可能存在编码 _问题_ 。确保 VSCode 的终端编码与 _PowerShell_ 的编码一致。如果 _乱码_ 是因为字体不支持特定字符（如 _中文_ ），可以尝试更换终端的字体。方法一：设置为 UTF-8 编码。 ](https://blog.csdn.net/u012386311/article/details/144566005)
[ windows 控制台 cmd/_PowerShell_ _中文_ 显示 _乱码_ ， _解决_ 方法 热门推荐 ](https://devpress.csdn.net/v1/article/detail/103072938)
[Where there is a will there is a way ](https://blog.csdn.net/runAndRun)
11-14
[ cmd 控制台默认编码，一般是简体 _中文_ 默认的GBK，如果出现 _中文_ _乱码_ ，一般改为UTF-8可 _解决_ 。 打开 cmd 控制台窗口 win（窗口键，在Ctrl与Alt之间）+R，输入 cmd，回车，这样操作会打开 cmd 控制台窗口。 检查当前的编码 C:\Users\AndyChen>chcp Active code page: 936 显示当家的编码格式为 936。 常用的编码及对应的码值(... ](https://devpress.csdn.net/v1/article/detail/103072938)
[ 【VScode】终端（ _powershell_ ） _中文_ _乱码_ _问题_ _解决_ ](https://blog.csdn.net/qq_62023159/article/details/142880709)
10-12
[ 如果你的VScode的 _powershell_ 出现编码格式不同导致的 _中文_ _乱码_ 情况，希望本文可以帮你了解 _问题_ 起因以及 _解决_ 方法。 ](https://blog.csdn.net/qq_62023159/article/details/142880709)
[ _解决_ _PowerShell_ 下Git _中文_ _乱码_ _问题_ ](https://blog.csdn.net/zweizhao/article/details/146489585)
03-24
[ 通过以上步骤，可以有效 _解决_ _PowerShell_ 下Git _中文_ _乱码_ _问题_ 。合理的配置不仅提升了开发体验，还确保了代码管理和协作的顺利进行。希望本文的详细讲解能够帮助到你，让你在使用Git时更加得心应手。在实际开发过程中，遇到 _问题_ 时，多查阅官方文档和社区资源，往往能找到更全面的 _解决_ 方案。Git作为一个强大的工具，其配置和使用技巧还有很多值得探索的地方。希望你在掌握这些基本配置后，能够进一步深入 _学习_ 和应用Git，提升自己的开发效率。 ](https://blog.csdn.net/zweizhao/article/details/146489585)
[ 【Windows】 _解决_ Windows 11 _Powershell_ _中文_ _乱码_ 的 _问题_ ](https://devpress.csdn.net/v1/article/detail/149172557)
07-07
[ 本文介绍在Windows11的 _PowerShell_ 中设置UTF-8编码的三种方法： 1)临时会话设置； 2)脚本内设置； 3)永久修改配置文件。关键步骤包括修改$OutputEncoding和Console编码，建议使用不带BOM的UTF-8格式（$false参数）。还提供了验证方法和处理文件读写的UTF-8参数示例。修改配置文件时如遇 _问题_ ，可先创建$PROFILE文件。 ](https://devpress.csdn.net/v1/article/detail/149172557)
[ _PowerShell_ | git log _中文_ _乱码_ _问题_ _解决_ ](https://chenzhenyang.blog.csdn.net/article/details/118074818)
06-20
[ _PowerShell_ | git log _中文_ _乱码_ _问题_ _解决_ ](https://chenzhenyang.blog.csdn.net/article/details/118074818)
[ 关于 _powershell_ 脚本中输出 _中文_ 到屏幕显示 _乱码_ _问题_ 的 _解决_ 方法 ](https://devpress.csdn.net/v1/article/detail/142791912)
10-09
[ _powershell_ 脚本标准输出显示 _中文_ ，结果显示为 _乱码_ 的 _解决_ 方法 ](https://devpress.csdn.net/v1/article/detail/142791912)
[ _解决_ _POWERSHELL_ 下cat打开 _中文_ _乱码_ _问题_ ](https://blog.csdn.net/fordream2007/article/details/108471262)
09-08
[ _解决_ _POWERSHELL_ 下cat打开 _中文_ _乱码_ _问题_ cat .\output.txt -Encoding UTF8 或者 get-content .\output.txt -Encoding UTF8  ](https://blog.csdn.net/fordream2007/article/details/108471262)
[ _powershell_ 打开 _中文_ _乱码_ _问题_ 的 _解决_ 办法 ](https://blog.csdn.net/plasma007/article/details/128259243)
12-09
[ _powershell_ 打开 _中文_ _乱码_ _问题_ 的 _解决_ 办法 ](https://blog.csdn.net/plasma007/article/details/128259243)
[ _解决_ MySQL中 _PowerShell_ _中文_ _乱码_ _问题_ ](https://blog.csdn.net/weixin_52879672/article/details/112157495)
01-03
[ 最近在web _学习_ 中，接触到MySQL数据库，在使用 _powershell_ 操作mysql过程中，发现当给mysql数据库中的表格插入 _中文_ 时，始终显示 _乱码_ ，无法显示正常的简体 _中文_ ，在搜索引擎中找了很多文章，都没有彻底 _解决_ ，今天终于找到一个可以彻底 _解决_ 的办法。 第一步 win+R,输入: control,选择区域 区域 -> 管理 -> 更改系统区域设置 勾选 -> Beta版:使用unicode UTF-8 提供全球语言支持；修改完成后需要重新启动计算机 第二步 重启后，win+R，输入 ](https://blog.csdn.net/weixin_52879672/article/details/112157495)
[ VS CODE 调试RUST代码使用 _PowerShell_ 终端出现 _中文_ _乱码_ _问题_ 终极 _解决_ 方式 ](https://blog.csdn.net/niceguy163/article/details/136074538)
02-07
[ 打开设置里的 `settings.json` 文件（使用快捷键 `Ctrl + ,` 然后点击右上角的 `{}` 图标）。这将使得每个新的终端实例自动执行指令 `chcp 65001` 来切换到 UTF-8 编码。1. **更改执行策略以允许脚本运行（如有需要）：**5. **重启 _PowerShell_ 以应用更改：**2. **编辑 _PowerShell_ 配置文件：**3. **添加 UTF-8 编码支持到配置文件：**4. **确认 VS Code 设置：**6. **测试变更是否有效：** ](https://blog.csdn.net/niceguy163/article/details/136074538)
[ （记录） _解决_ Windows 11 _Powershell_ _中文_ _乱码_ 的 _问题_ ](https://blog.csdn.net/m0_60030015/article/details/156232432)
12-24
[ 摘要：本文介绍如何在 _PowerShell_ 中设置UTF-8编码支持 _中文_ 输入输出。包括临时会话修改命令、脚本顶部添加编码设置、永久修改默认编码的方法（通过编辑$PROFILE文件）。同时提供了 _解决_ "禁止运行脚本"错误的方案：使用管理员权限修改执行策略为RemoteSigned。所有设置均采用不带BOM的UTF-8编码格式。 ](https://blog.csdn.net/m0_60030015/article/details/156232432)
[ _解决_ win10 _powershell_ 无法正常输入输出 _中文_ ，显示为 _乱码_ 的 _问题_ ](https://blog.csdn.net/cyxinda/article/details/103047708)
11-13
[ 转：https://blog.csdn.net/icer2015/article/details/80749334 win10 英文版， _powershell_ 上不论输入输出 _中文_ 一直为 _乱码_ ，看了网上许多文章没有一个能真正 _解决_ _问题_ 的。 最后自己瞎折腾出了 _解决_ 办法： 1.开始，打开“运行”，输入“regedit”打开注册表 2.HKEY_CURRENT_USER\Console\%SystemRo... ](https://blog.csdn.net/cyxinda/article/details/103047708)
[ _PowerShell_ 7 _解决_ Windows 下 Codex 客户端 _中文_ _乱码_ _问题_ 最新发布 ](https://devpress.csdn.net/v1/article/detail/161802706)
06-08
[ 【代码】 _PowerShell_ 7 _解决_ Windows 下 Codex 客户端 _中文_ _乱码_ _问题_ 。 ](https://devpress.csdn.net/v1/article/detail/161802706)
[ _解决_ Codex 执行 _PowerShell_ 时 _中文_ _乱码_ _问题_ ：不只是修改profile ](https://blog.csdn.net/2301_77207514/article/details/155498449)
12-02
[ Codex 根本不会执行你的 profile。你改 profile = 白改。这就解释了为什么你在 profile 里设置 UTF-8，却对 Codex 完全无效。 ](https://blog.csdn.net/2301_77207514/article/details/155498449)
[ windows中的cmd及 _powershell_ _中文_ _乱码_ 等 _问题_ 的 _解决_ ](https://miracle.blog.csdn.net/article/details/119046067)
07-23
[ 然后重启即可 _解决_ 。  ](https://miracle.blog.csdn.net/article/details/119046067)
被折叠的 条评论 [为什么被折叠?](https://blogdev.blog.csdn.net/article/details/122245662) [ 到【灌水乐园】发言](https://bbs.csdn.net/forums/FreeZone)
查看更多评论
点击重新获取
钱包余额 0
抵扣说明：
1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。 2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。
