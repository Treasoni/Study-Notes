---
url: "https://doc.istoreos.com/zh/guide/istoreos/install_x86.html"
title: "x86 物理机 | 易有云产品中心"
scraped_at: 2026-08-31T16:19:10+00:00
---

###  [#](https://doc.istoreos.com/zh/guide/istoreos/install_x86.html#x86-%E7%89%A9%E7%90%86%E6%9C%BA) x86 物理机
  * x86物理机，范围很广，可以是各种"电脑"，或者J4125/N5105等小主机。
  * 这里介绍x86实机安装iStoreOS固件。


##  [#](https://doc.istoreos.com/zh/guide/istoreos/install_x86.html#_1-%E8%A7%86%E9%A2%91%E6%95%99%E7%A8%8B) 1.视频教程
  * 2025最新！X86物理机安装iStoreOS全攻略：Windows、Mac双平台教学


##  [#](https://doc.istoreos.com/zh/guide/istoreos/install_x86.html#_2-%E5%87%86%E5%A4%87%E5%B7%A5%E4%BD%9C) 2.准备工作
  * 一个 U盘
  * 一个显示器
  * 一个键盘
  * 一台 windows 电脑


##  [#](https://doc.istoreos.com/zh/guide/istoreos/install_x86.html#_3-%E4%B8%8B%E8%BD%BD%E5%9B%BA%E4%BB%B6) 3.下载固件
  * [固件下载 (opens new window)](https://site.istoreos.com/firmware/download?devicename=x86_64&firmware=iStoreOS)


越前面版本越新，请注意看中间的日期，比如 xxx20221123xx-xxx.img.gz。下载完成之后不需要解压。
##  [#](https://doc.istoreos.com/zh/guide/istoreos/install_x86.html#_4-%E5%81%9A%E5%90%AF%E5%8A%A8%E7%9B%98) 4.做启动盘
  * 电脑上用 rufus 做 USB 启动盘


[Rufus下载 (opens new window)](https://rufus.ie/zh/)
  * 电脑插入U盘，打开rufus工具，选择下载好的固件，把固件写入到U盘


  * 把 U盘/键盘/显示器 接入X86机器


选择从U盘启动，一般按 F11 (x86机器太多，范围太广，可能不一定所有的机器都是F11快捷启动，具体自行查看)，选择接入的U盘，就可以启动。
如果找不到U盘，那么可能你的U盘不兼容，需要换一个U盘。
  * 把固件从U盘安装到系统


登录U盘系统，登录成功之后，输入：
`quickstart` (或者 qu + tab 自动补全)
选择 Install X86，一直按确定，就行了。具体如下图所示：
  * 用 `Show Interfaces` 查看网线插入到了哪个网口，以及查看当前LAN口的IP


##  [#](https://doc.istoreos.com/zh/guide/istoreos/install_x86.html#_5-%E5%90%AF%E5%8A%A8%E7%B3%BB%E7%BB%9F) 5.启动系统
系统写入完成后，拔掉外接设备(U盘/键盘等)，通电启动。
###  [#](https://doc.istoreos.com/zh/guide/istoreos/install_x86.html#%E8%BF%9B%E5%85%A5%E5%90%8E%E5%8F%B0%E7%AE%A1%E7%90%86) 进入后台管理
  * 默认后台地址 http://192.168.100.1/ （多网口机型） 或者 http://iStoreOS.lan/
  * 默认密码：password
  * 如果设备只有一个网口，则此网口就是 LAN 并且是 DHCP 客户端模式；如果大于一个网口，默认第一个网口是 WAN 口，其它都是 LAN。
  * 如果要修改 LAN 口 IP，首页有个内网设置，或者命令行用 quickstart 命令修改
  * 必读一轮我们的 [FAQ](https://doc.istoreos.com/zh/guide/istoreos/question.html)，后续出现问题知道如何解决！


酷友社论坛
加入社区，交流分享
探索更多乐趣！
<https://www.koolcenter.com/>


直播连线
每周二、四 19:30，宝哥与你相约直播间！


在线微信客服
在线时间：工作日00:00～13:30


QQ互助交流群 
仅玩家互助交流，无客服及技术人员常驻 
微信群（仅对付费用户开放）
最新优惠活动、功能试用第一时间会在微信群发布，有技术人员在群内解答问题 


商务合作邮箱


