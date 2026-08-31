---
url: "https://blog.csdn.net/u013262414/article/details/155347617"
title: "飞牛fnos折腾记（三）在飞牛fnos上安装iStoreOS作为软路由（旁路由搭建方式）_飞牛 软路由-CSDN博客"
scraped_at: 2026-08-31T16:21:30+00:00
---

  * [ AtomGit ](https://link.csdn.net?target=https%3A%2F%2Fgitcode.com%3Futm_source%3Dcsdn_toolbar)
  * [ InsCode ](https://agent.inscode.net/?utm_source=more_dropdown "InsCode")


登录
登录后您可以：
  * 复制代码和一键运行
  * 与博主大V深度互动
  * 解锁海量精选资源
  * 获取前沿技术资讯

立即登录
[开通会员 送T恤+百万token ](https://mall.csdn.net/vip?utm_source=dl_hover)
[ 会员·新人礼包 ](https://mall.csdn.net/vip?utm_source=260805_vip_toolbarhyzx_hy)
# 飞牛fnos折腾记（三）在飞牛fnos上安装iStoreOS作为软路由（旁路由搭建方式）
原创 已于 2025-11-28 12:42:57 修改 · 5.3k 阅读 · ·
本内容遵循CC 4.0 BY-SA版权协议
版权声明：本文为博主原创文章，遵循[ CC 4.0 BY-SA ](http://creativecommons.org/licenses/by-sa/4.0/)版权协议，转载请附上原文出处链接和本声明。 
[ GEO检测 ](https://mp.csdn.net/geo?title=%E9%A3%9E%E7%89%9Bfnos%E6%8A%98%E8%85%BE%E8%AE%B0%EF%BC%88%E4%B8%89%EF%BC%89%E5%9C%A8%E9%A3%9E%E7%89%9Bfnos%E4%B8%8A%E5%AE%89%E8%A3%85iStoreOS%E4%BD%9C%E4%B8%BA%E8%BD%AF%E8%B7%AF%E7%94%B1%EF%BC%88%E6%97%81%E8%B7%AF%E7%94%B1%E6%90%AD%E5%BB%BA%E6%96%B9%E5%BC%8F%EF%BC%89&url=https%3A%2F%2Fblog.csdn.net%2Fu013262414%2Farticle%2Fdetails%2F155347617&utm_source=blog_geo)
·
收录于
飞牛fnos
当前文章被收录于：
[ 飞牛fnos ](https://blog.csdn.net/u013262414/category_13093936.html "飞牛fnos")
当前文章被以下社区和专栏收录：
于 2025-11-28 12:40:44 首次发布
##  前言
之前群晖中一直有个iStoreOS的软路由，并且在上面部署了DNS服务器作为加速，以及一系列科学上网的小玩意儿，今天这篇文章只阐述如何安装iStoreOS，各类科学插件就不再多做赘述。
##  准备工作
首先我们要准备几个小东西放在我们的飞牛上：
###  第一步
[fnos_temp.iso](https://fw0.koolcenter.com/iStoreOS/Virtual/fnOS_temp.iso) 镜像（点击即可跳转下载页面），这是一个预制的iStoreOS包，用来帮助启动正式iStoreOS使用。
###  第二步
[iStoreOS镜像下载地址](https://fw.koolcenter.com/iStoreOS/x86_64_efi/) 下载efi镜像
下载最新版即可 `检查一下两个镜像文件是不是都在飞牛os中`
然后复制下来镜像路径 `很重要！后面要用到` `很重要！后面要用到` `很重要！后面要用到` 比如我的路径就是：/vol1/1001/downloads/istoreos-24.10.4-2025112116-x86-64-squashfs-combined-efi.img.gz 那么我存放镜像的文件夹就是：/vol1/1001/downloads/ 
###  第三步
在fnos系统设置中打开ssh，并确定自己的账户有ssh权限 如果账户后面带有SSH，就说明本账户是有SSH操作权限的，如果没有，那就点击 **更多** 启用SSH `注意：只有管理员账户才能启用SSH`
###  第四步
安装虚拟机套件 
###  第五步 开启OVS
在网络面板中开启OVS
##  开干
###  第一步：新建虚拟机
操作系统选择Linux，6.x-2.6 kernel 
`注意：主板固件一定要选择UEFI，系统镜像选择temp镜像`
之后就一直下一步就可以了。
###  第二步：解压包
使用ssh工具（putty、Xshell、WindTerm、甚至是windows自带的命令行都可以）连接服务器 `这里我们以windows自带命令行为例` 开始菜单搜索cmd并打开 打开后输入以下代码：

```
ssh 你的fnos用户名@fnos地址


Lobster AI


```

敲回车进入之后会让确认，输入yes后如下图 登录后，先使用sudo -i命令提权，然后进入存放镜像的目录（）

```
# 提权，会让输入密码
sudo -i

# 进入存放镜像的目录
cd /vol1/1001/downloads/ 

# 解压镜像
gzip -d istoreos-24.10.4-2025112116-x86-64-squashfs-combined-efi.img.gz

# 查看解压结果
ls -l

# 有istoreos-24.10.4-2025112116-x86-64-squashfs-combined-efi.img文件代表解压成功


Lobster AIbash


```

  * 1
  * 2
  * 3
  * 4
  * 5
  * 6
  * 7
  * 8
  * 9
  * 10
  * 11
  * 12
  * 13


###  第三步 挂载新的镜像到虚拟机
还是在ssh命令行中进行操作

```
# 查看虚拟机列表
virsh list --all
# 执行后可以看到如下结果，shutoff关闭的虚拟机就是iStoreOS虚拟机，我们记下来它的Name
# Id   Name       State
#---------------------------
# 20   ypiufp9b   running
# -    169h7uow   shut off

# 挂载新的镜像
virsh attach-disk 169h7uow /vol1/1001/downloads/istoreos-24.10.4-2025112116-x86-64-squashfs-combined-efi.img vdb --driver qemu --subdriver raw --persistent   #导入img到虚拟机
# Disk attached successfully


Lobster AIbash


```

  * 1
  * 2
  * 3
  * 4
  * 5
  * 6
  * 7
  * 8
  * 9
  * 10
  * 11


###  第四步 重新配置虚拟机
取消镜像挂载如下图 磁盘界面会新增一个硬盘，如果没有自己就手动添加一个，之后虚拟机开机即可。
##  配置IStoreOS（旁路由）
因为家里也不需要流量清洗等，所以软路由就选了个旁路由模式（主要是提供DNS服务和科学上网服务）
###  通过VNC方式连接IStoreOS虚拟机
当看到IStoreOS is ready就代表启动成功
###  quickstart
这时候按任意键进入IStoreOS的命令行执行以下命令

```
# 快速开始
quickstart
# 看到Show Interrfaces直接敲回车


Lobster AIbash


```

###  重设管理员密码
我的IStoreOS的初始IP地址为192.168.31.97，在浏览器中输入，并进入
直接点击登录，我们并没有设置管理员密码，登录进去之后设置以下管理员密码
###  网络配置（旁路由）
点击保存配置，软路由就配置完成了，后续安装服务就可以了。
标签
确定要放弃本次机会？ 
福利倒计时
立减 ¥
普通VIP年卡可用
[立即使用](https://mall.csdn.net/vip)
  * 觉得还不错? 
  * 

[ _飞_ _牛_ _fnos_ _折腾_ _记_ （四）玩docker-使用docker compose部署gitlab ](https://blog.csdn.net/u013262414/article/details/155447572)
12-01
[ 摘要： 本文 _记_ 录了将GitLab从群晖迁移到 _fnOS_ 过程中遇到的权限问题和解决方案。主要挑战包括 _fnOS_ 用户文件夹权限限制导致GitLab初始化失败，以及共享内存不足引发500/502错误。通过SSH以root身份在存储空间创建专用目录，并调整docker-compose.yml配置（如设置shm_size为5G）成功部署。建议避开 _fnOS_ 的用户文件夹权限限制，将数据存放在存储空间或根目录下，并针对具体 _服务器_ 环境调整GitLab配置。 ](https://blog.csdn.net/u013262414/article/details/155447572)
参与评论 您还未登录，请先 登录 后发表或查看评论
[ _飞_ _牛_ Nas 秒变 “网络管家”！ _飞_ _牛_ Nas虚拟机 _安装_ _软路由_ 保姆级教程 ](https://xiaoqiangclub.blog.csdn.net/article/details/148711517)
06-17
[ 🎯想给 _飞_ _牛_ Nas增添 _软路由_ 功能？本文详细介绍通过虚拟机 _安装_ _istoreos_ 的全过程，从准备工作到网络设置，助你轻松实现 _飞_ _牛_ Nas功能升级！ ](https://xiaoqiangclub.blog.csdn.net/article/details/148711517)
[ 常用iOS第 _三_ 方库以及XCode插件介绍.pdf ](https://download.csdn.net/download/weixin_38542354/22912180)
09-15
[ 常用iOS第 _三_ 方库以及XCode插件介绍.pdf ](https://download.csdn.net/download/weixin_38542354/22912180)
[ Nas上部署 _iStoreOS_ ，让你的 NAS 瞬间变身 _软路由_ ！（群晖/_飞_ _牛_ Nas如何快速部署 _iStoreOS_ ） ](https://xiaoqiangclub.blog.csdn.net/article/details/144397682)
12-12
[ Nas上部署 _iStoreOS_ ，让你的 NAS 瞬间变身 _软路由_ ！（群晖/_飞_ _牛_ Nas如何快速部署 _iStoreOS_ ） ](https://xiaoqiangclub.blog.csdn.net/article/details/144397682)
[ ios 最全的第 _三_ 方库.pdf ](https://download.csdn.net/download/bigicy/10290241)
03-16
[ 总结了最全的ios开发过程中必备的第 _三_ 方库文件，包括富文本、图像音频处理、数据库、聊天、摄像拍照、网络请求、通信、动画等，统计了常用的Xcode第 _三_ 方插件，附带很多完整项目和技术博客。 ](https://download.csdn.net/download/bigicy/10290241)
[ _fnOS_ _飞_ _牛_ NAS本地部署DeepSeek-R1大模型结合内网穿透远程在线访问 ](https://devpress.csdn.net/v1/article/detail/145895684)
03-20
[ 今天和大家分享一下如何在本地的 _fnOS_ _飞_ _牛_ 云NAS中部署DeepSeek-R1大模型，并结合cpolar内网穿透工具轻松实现远程访问与使用本地大模型，无需公网IP也不用准备云 _服务器_ 那么麻烦。 ](https://devpress.csdn.net/v1/article/detail/145895684)
[ _飞_ _牛_ NAS新增虚拟机功能，如果使用虚拟机网卡直通 _安装_ ikuai _软路由_ （如何解决OVS网桥绑定失败以及打开ovs后无法访问 _飞_ _牛_ nas等问题） ](https://xiaoqiangclub.blog.csdn.net/article/details/145366169)
01-26
[ _飞_ _牛_ NAS新增虚拟机功能，如果使用虚拟机网卡直通 _安装_ ikuai _软路由_ ](https://xiaoqiangclub.blog.csdn.net/article/details/145366169)
[ iStore OS 插件的手动 _安装_ 与特殊卸载 ](https://blog.csdn.net/KeyBordkiller/article/details/143781862)
11-14
[ 提供项目原地址，手动 _安装_ 方法，插件存在冲突时可通过终端形式卸载插件。 ](https://blog.csdn.net/KeyBordkiller/article/details/143781862)
[ 一些常用的iOS第 _三_ 方库和插件 ](https://blog.csdn.net/yaoliangjun306/article/details/50672769)
02-16
[ https://github.com/ViewDeck/ViewDeck // 侧滑菜单 https://github.com/Draveness/ATProperty // 快捷键提示 https://github.com/alcatraz/Alcatraz // 插件管理 ](https://blog.csdn.net/yaoliangjun306/article/details/50672769)
[ 超全！整理常用的iOS第 _三_ 方资源 ](https://blog.csdn.net/sevenquan/article/details/50554156)
01-21
[ 一：第 _三_ 方插件 1:基于响应式编程思想的oc 地址：https://github.com/ReactiveCocoa/ReactiveCocoa 2：hud提示框 地址：https://github.com/jdg/MBProgressHUD 3：XML/HTML解析 地址：https://github.com/topfunky/hpple 4：有文字 ](https://blog.csdn.net/sevenquan/article/details/50554156)
[ IOS开发常用的 _三_ 方库以及Xcode常用插件 ](https://blog.csdn.net/litong19930321/article/details/46888667)
07-15
[ 第 _三_ 方库CocoaPodCocoaPod并不是iOS上的第 _三_ 方库 而是大名鼎鼎的第 _三_ 方库的管理工具在CocoaPod没有出现之前 第 _三_ 方库的管理是非常痛苦的 尤其是一些大型的库 _(_ 比如nimbus _)_ 每次对库进行更新 都可能会非常的痛苦CocoaPod的出现解决了这些问题 以Framework的 _方式_ 引入第 _三_ 方库 极大的节约了集成的时间 而且通吃Objective-C和Swift _(_ Swift上的Cath ](https://blog.csdn.net/litong19930321/article/details/46888667)
[ _飞_ _牛_ _fnOS_ _安装_ KDE桌面 热门推荐 ](https://devpress.csdn.net/v1/article/detail/139319511)
09-09
[ 这段时间新出的nas系统 _飞_ _牛_ os真不错，基于debian的可 _折腾_ 性又高了不少，今天就来给这个系统装个KDE桌面，插上显示器也能当个电脑自己进自己的管理界面，播放下视频，上上网啥的。 ](https://devpress.csdn.net/v1/article/detail/139319511)
[ _istoreos_ -24.10.0-2025041811-installer-x86-64.iso ](https://download.csdn.net/download/2503_91868679/90720212)
04-29
[ 最新 _iStoreOS_ 资源 ](https://download.csdn.net/download/2503_91868679/90720212)
[ _istoreos_ -24.10.2-2025082211-easepi-r1-squashfs.img.gz ](https://download.csdn.net/download/xyz030556/91999719)
09-23
[ _istoreos_ 镜像版本：24.10.2-2025082211-easepi-r1 _iStoreOS_ 是基于 OpenWrt 深度优化的开源智能路由系统，它简化了操作，增强了稳定性，内置软件中心，支持 Docker，可让设备变身家庭 “全能超主机”，适合新手和专业用户使用。 ](https://download.csdn.net/download/xyz030556/91999719)
[ _飞_ _牛_ _fnos_ _安装_ _iStoreOS_[项目代码] 最新发布 ](https://download.csdn.net/download/cat789/92645123)
02-09
[ 本文详细介绍了在 _飞_ _牛_ _fnos_ 系统上 _安装_ _iStoreOS_ 作为 _软路由_ （ _旁路由_ ）的完整步骤。首先需要准备 _fnos_ _temp.iso和 _iStoreOS_ 镜像文件，并确保它们存放在指定路径。接着在 _fnos_ 系统设置中启用SSH权限，并 _安装_ 虚拟机套件。通过SSH工具连接 _服务器_ 后，解压镜像文件并挂载到虚拟机。重新配置虚拟机后，启动 _iStoreOS_ 并通过VNC连接进行初始设置，包括重设管理员密码和网络配置（ _旁路由_ 模式）。整个过程涵盖了从准备工作到最终配置的详细操作指南，适合需要在 _飞_ _牛_ _fnos_ 上 _搭建_ _软路由_ 的用户参考。 ](https://download.csdn.net/download/cat789/92645123)
[ _飞_ _牛_ _fnos_ _折腾_ _记_ （一） _安装_ ](https://blog.csdn.net/u013262414/article/details/155265087)
11-26
[ 本文 _记_ 录了在华为RH2288H V3 _服务器_ 上直接 _安装_ _飞_ _牛_ OS _(__fnos_ _)_ 的过程。作者作为群晖十年用户，分析了群晖系统的优缺点，转而尝试 _fnos_ 。 _安装_ 过程中遇到"no screens found"错误，提供了两种解决方案：使用低版本Rufus _(_ 3.2 _)_ 重制U盘镜像或改用应急 _安装_ 模式。最终成功 _安装_ 并进入系统初始化界面。文章详细 _记_ 录了异常情况的处理过程，为类似硬件环境下的 _fnos_ _安装_ 提供了参考方案。 ](https://blog.csdn.net/u013262414/article/details/155265087)
[ _飞_ _牛_ _fnOS_ _安装_ 8852be网卡驱动并成功连接 ](https://blog.csdn.net/mountain_D_kyle/article/details/145360312)
01-25
[ 免责声明：该流程理论上不会影响保存的数据，但因为涉及更新软件 _(_ apt-get upgrade _)_ 可能影响系统稳定性？自己的数据请自己负责。由于debian内核不识别8852be的网卡，所以需要自行 _安装_ 网卡驱动。debian内核版本：6.6.38-trim。然后就可以按照 _飞_ _牛_ 官网教程连接wifi使用了。PS 里面可能存在多余步骤，欢迎大佬指正。PS 不回复问题，因为我是小白。最后 _折腾_ 过程以及代码如下， _fnos_ 版本：0.8.36。本人使用的是迷你主机。 ](https://blog.csdn.net/mountain_D_kyle/article/details/145360312)
[ _飞_ _牛_ _fnos_ _折腾_ _记_ （二）分配存储空间-关于ZFS、Btrfs的选择、Raid的选择以及缓存和配置等问题 ](https://devpress.csdn.net/v1/article/detail/155307140)
11-27
[ 同样容量下btrfs的raid5/6重建更慢大容量情况下btrfs添加硬盘时间很长（我20T的数据加一块14T的硬盘加了半个月，因为数据需要重新分布）btrfs在重建过程中炸！过！硬！盘！（当然应该和btrfs关系不大，当时是电源供电的问题，但是心理阴影是真实存在的）但是btrfs也并不是那么的不堪，对于轻量级和大多数场景下都够用了，尤其是btrfs可以动态转换raid（比如raid5转raid6），这一点很爽，尤其群晖的小伙伴可以使用一下SHR系列的raid，好用，爱用。 ](https://devpress.csdn.net/v1/article/detail/155307140)
[ 【10Gbps/5盘位】专为 _fnOS_ 而设计， _飞_ _牛_ FD5 硬盘柜体验报告 ](https://blog.csdn.net/qq_63499861/article/details/145129179)
01-14
[ _飞_ _牛_ 为什么推出 FD5 硬盘柜？🔺 _飞_ _牛_ 私有云 _fnOS_ 推出来之后实在是太火爆了，并且它的兼容性也是出奇的好，所以很多小伙伴直接使用自己手头闲置的小主机， _笔记_ 本电脑，甚至是一些矿渣 _服务器_ 啥的就给 _折腾_ 上了。但是这些设备都有一个通病，那就是存储容量都及其有限，就比如说我 _折腾_ 的这台N305的小主机，这么好的配置，奈何硬盘容量仅有512GB，几个原盘电影就给塞满了，这谁受的了？所以 _飞_ _牛_ 也是真的“深查民情”，首先为大家安排了这个一个硬盘柜为大家解决硬盘焦虑的问题。FD5 硬盘柜有啥优势没？🔺必须的呀！ ](https://blog.csdn.net/qq_63499861/article/details/145129179)
  * 400-660-0108
  * 工作时间 8:30-22:00 


  * [北京互联网违法和不良信息举报中心](http://www.bjjubao.org/)
  * ©1999-2026北京创新乐知网络技术有限公司


登录后您可以享受以下权益：
  * 免费复制代码
  * 和博主大V互动
  * 下载海量资源
  * 发动态/写文章/加入社区

×立即登录
被折叠的 条评论 [为什么被折叠?](https://blogdev.blog.csdn.net/article/details/122245662) [ 到【灌水乐园】发言](https://bbs.csdn.net/forums/FreeZone)
查看更多评论
点击重新获取
钱包余额 0
抵扣说明：
1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。 2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。
选择你想要举报的内容（必选）
  * 内容涉黄
  * 政治相关
  * 内容抄袭
  * 涉嫌广告
  * 内容侵权
  * 侮辱谩骂
  * 样式问题
  * 其他


原文链接（必填）
请选择具体原因（必选）
  * 包含不实信息
  * 涉及个人隐私


请选择具体原因（必选）
  * 侮辱谩骂
  * 诽谤


请选择具体原因（必选）
  * 搬家样式
  * 博文样式


补充说明（选填）
取消
确定
下载APP 程序员都在用的中文IT技术交流社区 公众号 专业的中文 IT 技术社区，与千万技术人共成长 视频号 关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！
