---
url: "https://doc.istoreos.com/zh/guide/istoreos/question/about_network.html"
title: "Merlin 跟 iStoreOS 的旁路由设置 | 易有云产品中心"
scraped_at: 2026-08-31T16:19:10+00:00
---

##  [#](https://doc.istoreos.com/zh/guide/istoreos/question/about_network.html#merlin-%E8%B7%9F-istoreos-%E7%9A%84%E6%97%81%E8%B7%AF%E7%94%B1%E8%AE%BE%E7%BD%AE) Merlin 跟 iStoreOS 的旁路由设置
视频教程：[iStoreOS 旁路由 (opens new window)](https://www.bilibili.com/video/BV1pY411N7fX)。
##  [#](https://doc.istoreos.com/zh/guide/istoreos/question/about_network.html#%E6%97%81%E8%B7%AF%E7%94%B1-dhcp-%E8%AE%BE%E7%BD%AE) 旁路由 DHCP 设置
如果主路由打开 DHCP，则需要把 DHCP 的网关改成旁路由的网关。要不就关闭主路由 DHCP，打开旁路由 DHCP。一个局域网不能同时存在两个DHCP。
##  [#](https://doc.istoreos.com/zh/guide/istoreos/question/about_network.html#istoreos-%E4%BD%9C%E4%B8%BA%E4%B8%BB%E8%B7%AF%E7%94%B1-%E5%A6%82%E6%9E%9C%E8%A6%81%E8%AE%A9%E6%97%A0%E7%BA%BF%E8%B7%AF%E7%94%B1%E5%99%A8%E5%BA%95%E4%B8%8B%E7%9A%84%E8%AE%BE%E5%A4%87%E8%B7%9F-istoreos-%E4%B8%80%E4%B8%AA%E5%B1%80%E5%9F%9F%E7%BD%91) iStoreOS 作为主路由，如果要让无线路由器底下的设备跟 iStoreOS 一个局域网
需要把无线路由器设置为 AP 模式
##  [#](https://doc.istoreos.com/zh/guide/istoreos/question/about_network.html#%E5%A6%82%E6%9E%9C%E6%98%AF-mesh-%E8%B7%AF%E7%94%B1%E5%99%A8-%E6%AF%94%E5%A6%82-aimesh-%E6%88%96%E8%80%85-orbi-%E5%8F%AF%E4%BB%A5%E6%8A%8A-aimesh-%E5%B7%A5%E4%BD%9C%E5%9C%A8-ap-%E6%A8%A1%E5%BC%8F-aimesh-%E4%BE%9D%E7%84%B6%E6%9C%89%E6%95%88) 如果是 Mesh 路由器，比如 AIMesh，或者 Orbi，可以把 AIMesh 工作在 AP 模式，AiMesh 依然有效
##  [#](https://doc.istoreos.com/zh/guide/istoreos/question/about_network.html#orbi-%E8%B7%9F-istoreos-%E7%9A%84%E7%BB%84%E7%BD%91%E6%95%99%E7%A8%8B) Orbi 跟 iStoreOS 的组网教程
##  [#](https://doc.istoreos.com/zh/guide/istoreos/question/about_network.html#%E5%8F%AA%E6%9C%89%E4%B8%80%E4%B8%AA-lan-%E5%8F%A3%E7%9A%84%E6%97%B6%E5%80%99-%E5%8F%AA%E8%83%BD%E8%B5%B0%E6%97%81%E8%B7%AF%E7%94%B1%E9%85%8D%E7%BD%AE%E5%90%91%E5%AF%BC-%E8%AE%BE%E7%BD%AE%E4%B8%BA%E5%9B%BA%E5%AE%9A-ip) 只有一个 LAN 口的时候，只能走旁路由配置向导，设置为固定 IP
比如用的是树莓派等设备，如果只有 LAN 口，则需要用电脑先接到旁路由，再通过向导只能配置为旁路由形态。
如果不懂的话，就按下面的图片进行配置：（配置完成之后，电脑就没网络了，必须把树莓派接到路由器下面再用新的 IP 链接）
##  [#](https://doc.istoreos.com/zh/guide/istoreos/question/about_network.html#%E6%97%81%E8%B7%AF%E7%94%B1%E8%AE%BE%E7%BD%AE%E5%AE%8C%E6%88%90%E4%B9%8B%E5%90%8E-%E4%B8%8B%E9%9D%A2%E7%9A%84%E8%AE%BE%E5%A4%87%E6%97%A0%E6%B3%95%E4%B8%8A%E7%BD%91) 旁路由设置完成之后，下面的设备无法上网
首先推荐走旁路由设置向导，出问题的概率就很低了。如果出现这样的问题，可能性一：
"网络" -> "接口" -> "LAN" 使用默认网关确保打勾。
可能行二，你使用的小米等的主路由导致的问题，尝试解决：
"网络" -> "防火墙" -> "区域里面的LAN" 把 "IP 动态伪装" 打勾
##  [#](https://doc.istoreos.com/zh/guide/istoreos/question/about_network.html#%E8%BD%AF%E4%BB%B6%E6%9B%B4%E6%96%B0%E4%B9%8B%E5%90%8E-%E7%95%8C%E9%9D%A2%E9%94%99%E4%B9%B1) 软件更新之后，界面错乱
浏览器缓存问题。可以尝试 ctrl + F5 强制刷新，如果还不行，可以 F12 进到弹出来的菜单：
"网络" -> "停用缓存" 打勾，之后再刷新网页。好了之后，再按 F12 关闭窗口。
如果是很老的浏览器，考虑切换到 chrome 浏览器试试
##  [#](https://doc.istoreos.com/zh/guide/istoreos/question/about_network.html#%E9%98%BF%E9%87%8C%E4%BA%91%E7%9B%98%E6%88%96%E8%80%85-jellyfin-%E7%AD%89%E6%8F%92%E4%BB%B6%E5%AF%BC%E8%87%B4%E5%86%85%E6%B5%8B-100-%E6%88%96%E8%80%85-cpu-%E5%B1%85%E9%AB%98%E4%B8%8D%E4%B8%8B) 阿里云盘或者 Jellyfin 等插件导致内测 100% 或者 CPU 居高不下
首页进到终端，用 top 等相关的命令自行排查
##  [#](https://doc.istoreos.com/zh/guide/istoreos/question/about_network.html#jellyfin-emby-plex-%E6%A0%B8%E5%BF%83%E6%98%BE%E5%8D%A1%E9%A9%B1%E5%8A%A8%E6%94%AF%E6%8C%81) Jellyfin/Emby/Plex 核心显卡驱动支持
如果部分较新的 CPU，比如 N5105 的核显支持，可以尝试下载[iStoreOS_22.03 测试版固件 (opens new window)](https://github.com/istoreos/istoreos/issues/716)。Linux 内核是 5.10 版本。
##  [#](https://doc.istoreos.com/zh/guide/istoreos/question/about_network.html#win10%E6%97%A0%E6%B3%95%E8%AE%BF%E9%97%AE%E9%83%A8%E5%88%86samba%E6%9C%8D%E5%8A%A1%E5%99%A8%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88) Win10无法访问部分Samba服务器的解决方案
  * 依次打开“控制面板 -> 程序 -> 程序和功能”， 点击“启用或关闭Windows功能 -> SMB1.0/CIFS文件共享支持”；


  * 按下【win】+【R】键，然后输入“gpedit.msc”回车进入组策略界面；


然后“计算机配置 -> 管理模板 -> 网络 -> Lanman工作站 -> 启用不安全的来宾策略”；
  * 注册表编辑器 ->



```
\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters

```

找到“AllowInsecureGuestAuth”这个值，然后数值数据改为1。
若无，则新建DWORD(32位)值，名称为“AllowInsecureGuestAuth”，然后数值数据改为1。
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


