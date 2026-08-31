---
url: "https://doc.istoreos.com/zh/guide/istoreos/practice/BypassRouter.html"
title: "如何更好地使用旁路由 | 易有云产品中心"
scraped_at: 2026-08-31T16:19:10+00:00
---

##  [#](https://doc.istoreos.com/zh/guide/istoreos/practice/BypassRouter.html#%E5%A6%82%E4%BD%95%E6%9B%B4%E5%A5%BD%E5%9C%B0%E4%BD%BF%E7%94%A8%E6%97%81%E8%B7%AF%E7%94%B1) 如何更好地使用旁路由
  * 旁路由（也称为辅助路由或旁路网关）是网络中的一种特殊配置，通常用于在不改变主网络结构的情况下，提供额外的网络功能或优化流量。
  * 通常是在主路由器上接入一台额外的路由设备（如运行iStoreOS或OpenWrt系统的设备），通过LAN口连接主路由，分担特定网络任务，而不直接连接互联网，从而扩展主路由功能而不影响其稳定性。
  * 旁路由通过网关设置实现数据流控制，无需修改网络拓扑或IP地址；支持手动指定IP或DHCP分配等。

  
| 主旁方案  | 主路由  | 旁路由  | 优点  |  
| --- | --- | --- | --- |  
| [手动静态IP (opens new window)](https://mp.weixin.qq.com/s/10qixmNu0P88H3L1UN7c6g)  | 任何路由器  | iStoreOS设备  | 最简单、最易上手、适合新手  |  
| [旁路由DHCP (opens new window)](https://mp.weixin.qq.com/s/vCwXLALzEce4atWRY8ooRQ)  | 任何路由器  | iStoreOS设备  | 适应性最广、管理方便  |  
| [华硕浮动网关 (opens new window)](https://mp.weixin.qq.com/s/RV0_PWIPhrw4E4LJBoG0Wg)  | 华硕ASUSGO固件  | iStoreOS设备  | 华硕路由最佳旁路、自动切换  |  
| iStoreOS浮动网关  | iStoreOS设备  | iStoreOS设备  | iStoreOS最佳旁路、自动切换  |  
##  [#](https://doc.istoreos.com/zh/guide/istoreos/practice/BypassRouter.html#%E6%89%8B%E5%8A%A8%E9%9D%99%E6%80%81ip%E6%96%B9%E6%A1%88) 手动静态IP方案
  * 主路由：任何路由器，默认开启DHCP，不需要其他任何设置；
  * 旁路由：搭载iStoreOS的设备，关闭DHCP；
  * 连接：旁路由LAN口连接主路由LAN口；
  * 局域网内设备：手动为设备分配静态IP，网关/DNS设为旁路由IP。
  * 刷入ASUSGO梅林改版固件102.4及以上版本固件的设备（BE88U、BE86U、AX88U-Pro、AX86U-Pro等），和ROG魔盒最新官改固件；通过加强版“手动指定功能”，直接为局域网内的设备指定网关/DNS为旁路由IP。
  * ####  [#](https://doc.istoreos.com/zh/guide/istoreos/practice/BypassRouter.html#%E5%85%B7%E4%BD%93%E6%96%87%E5%AD%97%E6%95%99%E7%A8%8B-%E6%9C%80%E7%AE%80%E5%8D%95%E7%9A%84%E6%97%81%E8%B7%AF%E7%94%B1%E9%85%8D%E7%BD%AE-%E6%89%8B%E5%8A%A8%E9%9D%99%E6%80%81ip) 具体文字教程——>>[最简单的旁路由配置——手动静态IP (opens new window)](https://mp.weixin.qq.com/s/10qixmNu0P88H3L1UN7c6g)


##  [#](https://doc.istoreos.com/zh/guide/istoreos/practice/BypassRouter.html#%E6%97%81%E8%B7%AF%E7%94%B1dhcp%E6%96%B9%E6%A1%88) 旁路由DHCP方案
  * 主路由：任何路由器，默认关闭DHCP，网关设为旁路由IP；
  * 旁路由：搭载iStoreOS的设备，开启DHCP，全面接管局域网；
  * 连接：旁路由LAN口连接主路由LAN口；
  * 局域网内设备：通过iStoreOS旁路由上的“局域网设备管理”为设备自由分配网关为主/旁路由。
  * ####  [#](https://doc.istoreos.com/zh/guide/istoreos/practice/BypassRouter.html#%E5%85%B7%E4%BD%93%E6%96%87%E5%AD%97%E6%95%99%E7%A8%8B-%E6%97%81%E8%B7%AF%E7%94%B1%E5%BC%80%E5%90%AFdhcp%E6%9C%80%E4%BD%B3%E6%96%B9%E6%A1%88%E8%A7%A3%E6%9E%90) 具体文字教程——>>[旁路由开启DHCP最佳方案解析！ (opens new window)](https://mp.weixin.qq.com/s/vCwXLALzEce4atWRY8ooRQ)


##  [#](https://doc.istoreos.com/zh/guide/istoreos/practice/BypassRouter.html#%E5%8D%8E%E7%A1%95-%E6%B5%AE%E5%8A%A8%E7%BD%91%E5%85%B3%E6%96%B9%E6%A1%88) (华硕)浮动网关方案
  * 主路由：刷入ASUSGO改版固件的华硕路由器，默认开启DHCP，安装「浮动网关」软件；
  * 旁路由：搭载iStoreOS的设备，关闭DHCP，安装「浮动网关」软件；
  * 连接：旁路由LAN口连接主路由LAN口；
  * 局域网内设备：手动为设备分配静态IP，网关/DNS设为浮动网关IP。
  * 刷入ASUSGO梅林改版固件102.4及以上版本固件的设备（BE88U、BE86U、AX88U-Pro、AX86U-Pro等），和ROG魔盒最新官改固件；通过加强版“手动指定功能”，直接为局域网内的设备指定网关/DNS为浮动网关IP。
  * ####  [#](https://doc.istoreos.com/zh/guide/istoreos/practice/BypassRouter.html#%E5%85%B7%E4%BD%93%E6%96%87%E5%AD%97%E6%95%99%E7%A8%8B-%E5%8D%8E%E7%A1%95%E8%B7%AF%E7%94%B1%E5%99%A8%E6%9C%80%E7%A8%B3%E5%A6%A5%E3%80%81%E6%9C%80%E6%99%BA%E8%83%BD%E7%9A%84%E6%97%81%E8%B7%AF%E7%94%B1%E6%96%B9%E6%A1%88-%E6%B5%AE%E5%8A%A8%E7%BD%91%E5%85%B3) 具体文字教程——>>[华硕路由器最稳妥、最智能的旁路由方案——浮动网关！ (opens new window)](https://mp.weixin.qq.com/s/RV0_PWIPhrw4E4LJBoG0Wg)


##  [#](https://doc.istoreos.com/zh/guide/istoreos/practice/BypassRouter.html#istoreos-%E6%B5%AE%E5%8A%A8%E7%BD%91%E5%85%B3%E6%96%B9%E6%A1%88) (iStoreOS)浮动网关方案
  * 主路由：搭载iStoreOS的设备，默认开启DHCP，安装「浮动网关」软件；
  * 旁路由：搭载iStoreOS的设备，关闭DHCP，安装「浮动网关」软件；
  * 连接：旁路由LAN口连接主路由LAN口；
  * 局域网内设备：通过iStoreOS主路由上的“局域网设备管理”为设备自由分配网关为主/旁路由/浮动网关IP。


##  [#](https://doc.istoreos.com/zh/guide/istoreos/practice/BypassRouter.html#istoreos%E5%88%86%E8%BA%AB-%E6%B5%AE%E5%8A%A8%E7%BD%91%E5%85%B3%E6%96%B9%E6%A1%88) (iStoreOS分身)浮动网关方案
  * 主路由：搭载iStoreOS的设备，默认开启DHCP，安装「浮动网关」软件；
  * 旁路由：在主路由上安装「iStore分身」并启用，关闭DHCP，安装「浮动网关」软件；
  * 连接：iStoreOS分身是在主路由上的「虚拟系统」，不需要实际连线；
  * 局域网内设备：通过iStoreOS主路由上的“局域网设备管理”为设备自由分配网关为主/旁路由/浮动网关IP。


← [ 软件中心  (opens new window)](https://doc.linkease.com/zh/guide/istore/)
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


