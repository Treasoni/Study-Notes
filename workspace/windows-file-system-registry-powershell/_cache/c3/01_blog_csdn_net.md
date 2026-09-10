---
url: "https://blog.csdn.net/m0_60030015/article/details/156232432"
title: "（记录）解决Windows 11 Powershell 中文乱码的问题_windows powershell 乱码-CSDN博客"
scraped_at: 2026-09-10T15:42:42+00:00
---

# （记录）解决Windows 11 Powershell 中文乱码的问题
原创 已于 2026-01-05 15:21:07 修改 · 1.3k 阅读 · ·
本内容遵循CC 4.0 BY-SA版权协议
版权声明：本文为博主原创文章，遵循[ CC 4.0 BY-SA ](http://creativecommons.org/licenses/by-sa/4.0/)版权协议，转载请附上原文出处链接和本声明。 
[ GEO检测 ](https://mp.csdn.net/geo?title=%EF%BC%88%E8%AE%B0%E5%BD%95%EF%BC%89%E8%A7%A3%E5%86%B3Windows+11+Powershell+%E4%B8%AD%E6%96%87%E4%B9%B1%E7%A0%81%E7%9A%84%E9%97%AE%E9%A2%98&url=https%3A%2F%2Fblog.csdn.net%2Fm0_60030015%2Farticle%2Fdetails%2F156232432&utm_source=blog_geo)
·
收录于
当前文章被收录于：
[ 问题记录 ](https://blog.csdn.net/m0_60030015/category_13109039.html "问题记录")
当前文章被以下社区和专栏收录：
于 2025-12-24 14:32:51 首次发布
**目录**
[1.临时修改当前会话编码为UTF-8](https://blog.csdn.net/m0_60030015/article/details/156232432#1.%E4%B8%B4%E6%97%B6%E4%BF%AE%E6%94%B9%E5%BD%93%E5%89%8D%E4%BC%9A%E8%AF%9D%E7%BC%96%E7%A0%81%E4%B8%BAUTF-8)
[2.输入输出都支持中文字符，如下设置](https://blog.csdn.net/m0_60030015/article/details/156232432#2.%E8%BE%93%E5%85%A5%E8%BE%93%E5%87%BA%E9%83%BD%E6%94%AF%E6%8C%81%E4%B8%AD%E6%96%87%E5%AD%97%E7%AC%A6%EF%BC%8C%E5%A6%82%E4%B8%8B%E8%AE%BE%E7%BD%AE)
[3.脚本中设置编码，在脚本顶部添加：](https://blog.csdn.net/m0_60030015/article/details/156232432#3.%E8%84%9A%E6%9C%AC%E4%B8%AD%E8%AE%BE%E7%BD%AE%E7%BC%96%E7%A0%81%EF%BC%8C%E5%9C%A8%E8%84%9A%E6%9C%AC%E9%A1%B6%E9%83%A8%E6%B7%BB%E5%8A%A0%EF%BC%9A)
[4.永久修改Powershell默认编码](https://blog.csdn.net/m0_60030015/article/details/156232432#4.%E6%B0%B8%E4%B9%85%E4%BF%AE%E6%94%B9Powershell%E9%BB%98%E8%AE%A4%E7%BC%96%E7%A0%81)
[5.如果出现“无法加载文件***\WindowsPowerShell\profile.ps1，因为在此系统上禁止运行脚本”问题，修改计算机上现用策略即可解决](https://blog.csdn.net/m0_60030015/article/details/156232432#5.%E5%A6%82%E6%9E%9C%E5%87%BA%E7%8E%B0%E2%80%9C%E6%97%A0%E6%B3%95%E5%8A%A0%E8%BD%BD%E6%96%87%E4%BB%B6***%5CWindowsPowerShell%5Cprofile.ps1%EF%BC%8C%E5%9B%A0%E4%B8%BA%E5%9C%A8%E6%AD%A4%E7%B3%BB%E7%BB%9F%E4%B8%8A%E7%A6%81%E6%AD%A2%E8%BF%90%E8%A1%8C%E8%84%9A%E6%9C%AC%E2%80%9D%E9%97%AE%E9%A2%98%EF%BC%8C%E4%BF%AE%E6%94%B9%E8%AE%A1%E7%AE%97%E6%9C%BA%E4%B8%8A%E7%8E%B0%E7%94%A8%E7%AD%96%E7%95%A5%E5%8D%B3%E5%8F%AF%E8%A7%A3%E5%86%B3)
#### 1.临时修改当前会话编码为UTF-8
在Powershell中运行下面命令

```
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
```

其中false表示不带BOM的UTF-8
#### 2.输入输出都支持中文字符，如下设置

```
$InputEncoding = [Console]::InputEncoding = [Text.UTF8Encoding]::new($false)
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
```

#### 3.脚本中设置编码，在脚本顶部添加：

```
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
```

#### 4.永久修改Powershell默认编码
在Powershell中运行下面命令

```
notepad $PROFILE
```

如果提示未创建，运行下面命令创建

```
New-Item -Path $PROFILE -ItemType File -Force
```

在$PROFILE中添加以下内容

```
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
```

保存关闭，重启Powershell即可生效
#### 5.如果出现“无法加载文件***\WindowsPowerShell\profile.ps1，因为在此系统上禁止运行脚本”问题，修改计算机上现用策略即可解决
以管理员身份打开Powershell，运行下面命令，查看现有策略

```
get-executionpolicy
```

策略列表如下：
以管理员身份打开Powershell，运行下面命令，更改执行策略

```
set-executionpolicy Remotesigned
```

标签
关注博主即可阅读全文
确定要放弃本次机会？ 
福利倒计时
立减 ¥
普通VIP年卡可用
[立即使用](https://mall.csdn.net/vip)
[ 眼底流转天上月  ](https://blog.csdn.net/m0_60030015)
  * 觉得还不错? 
  * 

[ 新学期领福利！购实物周边送年卡会员！ ](https://mall.csdn.net/vip?utm_source=260904_vip_T1)
[ T恤、键盘、双肩包等周边任选！还能解锁资源下载、VIP文章等多重会员权益！ ](https://mall.csdn.net/vip?utm_source=260904_vip_T1)
参与评论 您还未登录，请先 登录 后发表或查看评论
[ _Powershell_ 7.x中UTF-8环境 _中文_ _乱码_ _解决_ 办法 ](https://blog.csdn.net/shadow_zed/article/details/126396983)
08-18
[ _Powershell_ 7 _中文_ _乱码_ _问题_ _解决_ ](https://blog.csdn.net/shadow_zed/article/details/126396983)
[ _解决_ _Windows_ 终端 _PowerShell_ 展示 _乱码_ 的 _问题_ ](https://iteacher.blog.csdn.net/article/details/139149008)
[h a 6 6 6 c k 为 你解决复杂难题！](https://blog.csdn.net/HQ354974212)
05-23
[ 标题： _解决_ _Windows_ 终端 _PowerShell_ 展示 _乱码_ 的 _问题_ 在使用 _Windows_ 终端中的 _PowerShell_ 时，有时会遇到 _乱码_ 显示的 _问题_ ，这可能会给用户带来困扰。这种 _问题_ 通常与字符编码设置有关，因为不同的字符编码会导致终端无法正确显示特定语言或特殊字符。在本文中，我们将介绍如何 _解决_ _Windows_ 终端 _PowerShell_ 中 _乱码_ 显示的 _问题_ ，并详细说明各种字符编码的数字表示，以及相关命令的用法。 ](https://iteacher.blog.csdn.net/article/details/139149008)
[ 如何 _解决_ vscode _powershell_ _乱码_ ](https://blog.csdn.net/u012386311/article/details/144566005)
12-18
[ 在 Visual Studio Code 中使用 _PowerShell_ 时出现 _乱码_ ，通常是由于终端编码设置或字体不匹配导致的。 _PowerShell_ 默认的输出编码可能与终端编码不一致。通过以上方法，通常可以 _解决_ VSCode 中 _PowerShell_ 的 _乱码_ _问题_ 。确保你使用的是最新版本的 _PowerShell_ ，因为旧版本可能存在编码 _问题_ 。确保 VSCode 的终端编码与 _PowerShell_ 的编码一致。如果 _乱码_ 是因为字体不支持特定字符（如 _中文_ ），可以尝试更换终端的字体。方法一：设置为 UTF-8 编码。 ](https://blog.csdn.net/u012386311/article/details/144566005)
[ _windows_ 控制台 cmd/_PowerShell_ _中文_ 显示 _乱码_ ， _解决_ 方法 热门推荐 ](https://devpress.csdn.net/v1/article/detail/103072938)
[Where there is a will there is a way ](https://blog.csdn.net/runAndRun)
11-14
[ cmd 控制台默认编码，一般是简体 _中文_ 默认的GBK，如果出现 _中文_ _乱码_ ，一般改为UTF-8可 _解决_ 。 打开 cmd 控制台窗口 win（窗口键，在Ctrl与Alt之间）+R，输入 cmd，回车，这样操作会打开 cmd 控制台窗口。 检查当前的编码 C:\Users\AndyChen>chcp Active code page: 936 显示当家的编码格式为 936。 常用的编码及对应的码值 _(_... ](https://devpress.csdn.net/v1/article/detail/103072938)
[ _powershell_ _中文_ _乱码_ _windows_ cmd ](https://devpress.csdn.net/v1/article/detail/130467272)
05-02
[ 方法1. 进入控制面板 -> 时钟和区域 -> 区域 -> 管理 -> 更改系统区域设置 -> 勾选Beta版:使用 UnicodeUTF-8提供全球语言支持 _(_ U _)_ 该操作为将命令窗口字符集永久调整为utf-8，重启依然生效，但是当我尝试cat查看文件时依然出现了 _乱码_ 。 _问题_ 的起因是windoes默认字符编码是GBK,而目前通用字符集使用的是UTF-8。为使用最新的 _windows_ 特性，将默认字符集切换到UTF-8。该操作为将当前命令窗口字符切换到utf-8，打开新的失效。关于字符集的 _问题_ 欢迎移架到。 ](https://devpress.csdn.net/v1/article/detail/130467272)
[ 暂时 _解决_ HiBit Uninstaller 导致 VSCode 右键菜单 _中文_ _乱码_ 的 _问题_ ](https://devpress.csdn.net/v1/article/detail/159670341)
03-31
[ 摘要： _Windows_ _11_ 系统中使用HiBit Uninstaller扫描注册表后，VSCode右键菜单出现 _中文_ _乱码_ 。经排查发现该 _问题_ 仅出现在 _Windows_ _11_ 系统，是由于HiBit Uninstaller在扫描时会在HKLM\SOFTWARE\Classes下创建与HKCU中同名的空注册表项，导致系统优先读取空项而显示异常。 _解决_ 方案包括手动删除HKLM下的空注册表项，或使用提供的 _PowerShell_ 脚本自动修复。脚本会自动检测并删除相关空项，同时生成操作日志。该 _问题_ 在 _Windows_ 10系统中不会复现， ](https://devpress.csdn.net/v1/article/detail/159670341)
[ 彻底 _解决_ _Windows_ 命令行 _中文_ _乱码_ ：永久设置CMD/_PowerShell_ 为UTF-8编码 最新发布 ](https://blog.csdn.net/weixin_30493401/article/details/101406712)
08-15
[ 字符编码是计算机存储和显示文字的基础规则，它定义了字符与二进制数据的映射关系。在跨平台开发和数据处理中，UTF-8因其通用性成为事实标准，而 _Windows_ 系统传统上默认使用GBK编码，这导致了控制台环境中的 _中文_ _乱码_ _问题_ 。 _解决_ 这一编码冲突对于确保脚本正确执行、日志可读和数据传输准确至关重要。通过调整 _Windows_ 的活动代码页和系统区域设置，可以将命令行环境永久对齐至UTF-8编码，从而一劳永逸地消除 _乱码_ 困扰。本文聚焦于**CMD**和**_PowerShell_ **的编码配置，提供了从原理到永久设置的完整实操指南 ](https://blog.csdn.net/weixin_30493401/article/details/101406712)
[ _Windows_ _11_ Git 安装配置避坑指南：从签名验证到 _中文_ _乱码_ 全解 ](https://devpress.csdn.net/v1/article/detail/96721133)
07-15
[ Git 是分布式版本控制系统的标准实现，其核心原理基于快照存储、有向无环图（DAG）提交历史与三棵树（Working Directory/Index/Repository）模型。在 _Windows_ _11_ 平台上，由于系统级安全机制（如 SmartScreen、驱动签名强制）、NTFS 文件系统特性（换行符、时间戳精度、ACL 权限）及终端环境（Git Bash/mintty vs _Windows_ Terminal）的深度耦合，原生 Git 工具链极易出现配置失效、 _中文_ _乱码_ 、SSH 认证失败、VS Code  ](https://devpress.csdn.net/v1/article/detail/96721133)
[ VS2026 _中文_ _乱码_ _问题_ _解决_ 方案与编码优化 ](https://blog.csdn.net/weixin_34122810/article/details/94750494)
08-04
[ 文本编码是软件开发中的基础概念，涉及字符集转换、文件存储和显示渲染等多个技术环节。Unicode作为现代编码标准，其UTF-8实现因其兼容性和高效性被广泛采用。在IDE环境中，编码配置直接影响源代码的可读性和跨平台兼容性，特别是处理多语言项目时。Visual Studio 2026引入的严格编码验证机制，虽然提升了安全性，但也带来了 _中文_ _乱码_ 等典型 _问题_ 。通过系统区域设置调整、IDE编码配置优化和项目级文件转换，开发者可以有效 _解决_ 编码冲突 _问题_ 。这些方法在STM32开发、Qt应用等场景中尤为重要，能确保 _中文_ 注释、 ](https://blog.csdn.net/weixin_34122810/article/details/94750494)
[ _Windows_ 下OpenClaw _中文_ 版快速部署指南 ](https://devpress.csdn.net/v1/article/detail/98940565)
07-24
[ 自动化工具在现代开发流程中扮演着关键角色，通过脚本化操作提升工程效率。OpenClaw作为轻量级开源工具集，其核心原理是基于模块化设计实现工作流编排。技术价值体现在降低开发门槛，特别适合个人开发者快速构建自动化流程。在 _Windows_ 环境下部署时，需注意系统环境配置和 _中文_ 语言包集成等关键环节。本文以OpenClaw _中文_ 版为例，详细解析从环境准备到服务调优的全流程，涵盖 _PowerShell_ 脚本调试、环境变量配置等实用技巧，帮助开发者快速搭建稳定的自动化工作环境。 ](https://devpress.csdn.net/v1/article/detail/98940565)
[ _Windows_ 安装Cursor全链路排障指南： _解决_ 打不开、 _中文_ _乱码_ 、AI不响应 ](https://blog.csdn.net/weixin_34167819/article/details/93730645)
07-07
[ Cursor作为基于VS Code内核的AI编程工具，其在 _Windows_ 平台的运行依赖Electron框架、系统安全策略与本地化环境协同。理解Smart App Control拦截机制、 _Windows_ Defender实时防护对模型加载的I/O阻塞、以及区域设置与时间同步对国际化模块的影响，是保障稳定运行的基础。技术价值在于打通从系统级配置（如SAC关闭、Defender排除路径）到应用层调优（locale四层覆盖、.cursorignore配额管理）的完整链路。典型应用场景包括前端工程师启用自动函数补全、 ](https://blog.csdn.net/weixin_34167819/article/details/93730645)
[ Dev-C++ 5._11_ 教学配置指南： _解决_ _中文_ _乱码_ 与环境崩溃 ](https://blog.csdn.net/weixin_34130389/article/details/92519794)
07-14
[ Dev-C++ 是面向编程初学者的轻量级C/C++集成开发环境，其核心价值在于零配置、强确定性与教学友好性。它基于MinGW编译器（特别是TDM-GCC定制版），通过内置调试器、 _中文_ 界面和精简依赖，规避了VS Code、CLion等现代IDE在教学场景中常见的环境变量配置失败、CMake语法报错、UAC权限冲突等 _问题_ 。技术原理上，其稳定性源于Delphi 7底层架构、硬编码编译路径与GBK编码深度适配，而非泛化的跨平台抽象。对高校教师、职教助教及自学学生而言，它支撑起‘写→编译→运行→调试’的原子化学习闭环 ](https://blog.csdn.net/weixin_34130389/article/details/92519794)
[ _Windows_ _中文_ 版下 MSVC 对 UTF-8 支持（避免 _乱码_ ） ](https://blog.csdn.net/qq_36349997/article/details/136204190)
02-21
[ 上面也提到了， _中文_ 版的终端编码是 GB2312，在保证源码是 UTF-8 的情况下，又要保证终端正常显示 _中文_ ，考虑到两类方法：一种是将终端编码改 UTF-8，参考 https://blog.iyatt.com/?出现 _乱码_ 通常就是 _记录_ 的规则和阅读的规则不一样导致的，举一个例子，我在纸上写了四个字“女子弓虽”，如果别人读的时候是把我的每两个字当作一个字，那么读取出来就是“好强”， _乱码_ 产生大致就是相似的原因。基于 VS 管理的项目的话，在项目名上右键打开属性，C/C++ -> 命令行 -> 其他选项 中加上。 ](https://blog.csdn.net/qq_36349997/article/details/136204190)
[ Git 2.45 + TortoiseGit 2.16 _Windows_ _11_ 环境配置：3步 _解决_ SSH 密钥与 _中文_ 路径兼容 ](https://blog.csdn.net/weixin_34109408/article/details/92364938)
07-11
[ 本文详细介绍了在 _Windows_ _11_ 环境下配置Git 2.45和TortoiseGit 2.16的完整流程，重点 _解决_ SSH密钥配置与 _中文_ 路径兼容 _问题_ 。通过三步核心操作：环境准备、SSH密钥全流程配置和 _中文_ 路径 _解决_ 方案，帮助开发者高效搭建开发环境并避免常见错误。 ](https://blog.csdn.net/weixin_34109408/article/details/92364938)
[ _Windows_ 下Hermes Agent保姆级安装指南： _PowerShell_ +uv+Python 3._11_ 全链路部署 ](https://blog.csdn.net/weixin_30443075/article/details/99136255)
07-09
[ Hermes Agent是一种面向任务的智能体（Agent）系统，其核心能力依赖于可编程工作流、多工具协同与本地模型集成。要稳定运行这类AI Agent，底层需满足异步并发控制、跨进程环境隔离与安全脚本执行三大技术前提。 _PowerShell_ 提供了 _Windows_ 原生的策略管理与环境变量动态继承能力，uv则 _解决_ 了Python版本碎片化与虚拟环境不可靠等长期痛点，而Python 3._11_ 引入的TaskGroup和ExceptionGroup特性，正是支撑Hermes多任务容错调度的关键语言基础。该组合在企业办公、 ](https://blog.csdn.net/weixin_30443075/article/details/99136255)
[ _Windows_ Vibe Coding： _PowerShell_ +ripgrep+Python 快速开发实践 ](https://devpress.csdn.net/v1/article/detail/102009379)
07-06
[ Vibe Coding 是一种强调心流、反馈即时、工具极简的现代编码范式，核心在于缩短‘想法→执行→结果’的响应链路。其技术原理依托于操作系统原生能力的深度协同： _PowerShell_ 提供基于对象的管道化系统操控能力，ripgrep 实现毫秒级结构化文本搜索，Python 充当轻量级数据转换与胶水逻辑引擎。这种组合在 _Windows_ 平台具备独特优势——无需 WSL、不依赖开发者模式，即可打通办公场景（Excel/Log/邮件）、运维任务与日常自动化。对广大 _Windows_ 开发者、运维人员及技术型办公用户 ](https://devpress.csdn.net/v1/article/detail/102009379)
[ OFD文档 _乱码_ _问题_ 排查与 _Windows_ Server字体 _解决_ 方案 ](https://blog.csdn.net/weixin_30596735/article/details/97991954)
08-11
[ OFD作为国产版式文档标准，其核心优势在于跨平台一致性，但字体兼容性 _问题_ 常导致 _乱码_ 现象。本文深入解析 _Windows_ Server环境下的字体机制差异，揭示系统默认字体缺失与回退机制失效的技术原理。通过对比桌面版与服务器版 _Windows_ 的字体配置差异，提出标准化字体部署方案，包括 _PowerShell_ 自动化安装、字体缓存重建等工程实践。针对OFD处理库ofdrw的应用场景，详细说明强制字体嵌入与子集化优化技巧，并给出容器化部署的Dockerfile最佳实践。这些 _解决_ 方案不仅适用于电子发票系统，也可推广到电子合同 ](https://blog.csdn.net/weixin_30596735/article/details/97991954)
[ PaiCLI _Windows_ 终端兼容性完整 _解决_ 方案 ](https://devpress.csdn.net/v1/article/detail/162497918)
07-01
[ _Windows_ 控制台默认使用 GBK 代码页（cp936），而 PaiCLI 内部（JLine + Java + LLM API）全链路使用 UTF-8。当用户输入的 _中文_ 从控制台经 JLine 读取、传入模型、再从模型响应回显到控制台时，经历了 GBK → UTF-8 → GBK 的多轮编码转换，导致部分字符丢失变成问号。本文档 _记录_ 在 _Windows_ 环境下运行 PaiCLI 时遇到的两大终端 _问题_ （ _中文_ _乱码_ 与 ANSI 回退）的根因分析、踩坑 _记录_ 和最终 _解决_ 方案。只对当前终端窗口有效，关闭窗口后失效。 ](https://devpress.csdn.net/v1/article/detail/162497918)
[ Unity _中文_ _乱码_ 终极 _解决_ 方案：统一编码与系统设置 ](https://blog.csdn.net/cuankuangzhong6373/article/details/100505086)
[cuankuangzhong6373的博客](https://blog.csdn.net/cuankuangzhong6373)
08-01
[ 字符编码是计算机存储和处理文本信息的基础机制，它定义了字符与二进制数据之间的映射关系。在软件开发中，编码不匹配会导致文本显示异常，特别是包含非ASCII字符（如 _中文_ ）时。其技术原理在于文件保存编码与读取解码方式不一致，造成二进制数据被错误解析。统一编码标准对于保障代码可读性、团队协作效率和跨平台兼容性具有重要价值。在Unity开发环境中，C#脚本文件常因编码 _问题_ 出现 _中文_ _乱码_ ，这主要发生在代码预览、外部编辑器打开等场景。通过将文件编码统一为UTF-8 with BOM，并配置系统区域设置，可以有效 _解决_ _乱码_ _问题_ ](https://blog.csdn.net/cuankuangzhong6373/article/details/100505086)
[ Claude Code _Windows_ 安装全解析：Git、Node.js与 _PowerShell_ 深度适配指南 ](https://devpress.csdn.net/v1/article/detail/92984929)
07-15
[ Claude Code 是面向终端开发者的原生 AI 编程助手，其核心能力依赖于对 Git、Node.js 和 _PowerShell_ 等底层工具链的深度集成。它并非简单封装 API，而是通过终端环境感知、文件系统实时读取与 Shell 命令注入实现上下文感知式协作。技术价值在于消除浏览器依赖、保持开发流连续性，并支持跨技术栈（如 TypeScript、Java、Docker）的即时分析与执行。典型应用场景包括遗留项目性能诊断、CI 失败根因定位、多仓库快速代码重构等。本文聚焦 _Windows_ 平台——尤其是 ](https://devpress.csdn.net/v1/article/detail/92984929)
被折叠的 条评论 [为什么被折叠?](https://blogdev.blog.csdn.net/article/details/122245662) [ 到【灌水乐园】发言](https://bbs.csdn.net/forums/FreeZone)
查看更多评论
点击重新获取
钱包余额 0
抵扣说明：
1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。 2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。
