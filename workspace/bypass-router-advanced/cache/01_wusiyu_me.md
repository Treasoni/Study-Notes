---
url: "https://wusiyu.me/openwrt-bypass-gateway-tcp-not-work/"
title: "备忘：OpenWrt在旁路由下Ping通但TCP不通的解决办法 - WuSiYu Blog"
scraped_at: 2026-09-23T06:05:28+00:00
---

[跳至内容](https://wusiyu.me/openwrt-bypass-gateway-tcp-not-work/#wp--skip-link--target)
# 备忘：OpenWrt在旁路由下Ping通但TCP不通的解决办法
2023年8月6日
作者：
在
4–6 分钟
906字
1732次浏览
这里的背景是OpenWRT作为旁路由（aka. 旁路网关，单臂路由，透明网关等），没有一个太准确的叫法，具体的指**另一台“主路由”连接公网并作NAT，OpenWrt不启用NAT，**用户设备** 的上行流量先经过OpenWrt旁路由转发到“主路由”，下行时流量直接通过由主路由发送到用户设备，不经过OpenWrt旁路由**。主要优点在于下行带宽不会受OpenWrt性能的影响，且OpenWrt设备故障或维护时，可手动（或配置自动）切换到主路由。（OpenWRT旁路由可以是单臂路由，也可以有另一根独立的线路连接到主路由，避免带宽限制，如我之前的文章）
但由于上行和下行的通路不同，仅有部分流量会经过OpenWrt，会导致TCP的conntrack出现问题。
具体表现是：已经正确设置了路由，且能用户设备能ping通外网，但对外进行TCP不通，若在用户设备上抓包分析会看到：
  * （从用户设备，客户端）发送SYN
  * 收到（来自公网设备，服务器）SYN + ACK
  * 发送ACK
  * 发送通信内容（payload）
  * （未收到回应ACK）
  * 重复收到SYN + ACK（多次）
  * （重传）发送通信内容（payload）
  * （还是没有回应ACK）


不难看出，这是由于客户端发送的ACK在中途被丢弃了，使得虽然客户端认为TCP连接已经建立，但在服务端看来没有，因此客户端发送的payload不会被确认，而服务器则会重传SYN + ACK，继续等待客户端的ACK。
这种现象和OpenWrt的conntrack有关，由于服务器回应的SYN + ACK没有经过OpenWrt，使得OpenWrt没有正确追踪TCP连接。在一些特定情况下，OpenWrt认为客户端后续的数据包是“无效数据包”，并丢弃，包括客户端发送的ACK。
在OpenWrt中解决的方法也很简单，首先在“防火墙”页面中**关闭“丢弃无效数据包”** ：
其次，若OpenWrt通过独立线路（在防火墙的WAN Zone）连接主路由，则在一些特定情况下（比如因为一些组网需求，对一些内网网段开启了masquerade），还要**打开WAN Zone – 编辑 – 连接追踪设置 – 允许“无效”流量** ，如下图：
_具体conntrack的工作方式和该问题的出现条件，有待进一步验证_
## 评论
### 一条对“备忘：OpenWrt在旁路由下Ping通但TCP不通的解决办法”的回复
  1. 谢谢分享，这个应该就是非对称路由导致的。 


### 发表回复 
## 更多文章
  * ### [X1 Presenter鼠标的macOS版虚拟激光笔软件](https://wusiyu.me/thinkpad-x1-presenter-mouse-for-macos/)
  * ### [Arduino UNO Q 开发板初体验](https://wusiyu.me/arduino-uno-q-board-first-look/)
  * ### [解决Open WebUI接入Qwen3.5/3.6模型后无法自动生成对话标题的问题](https://wusiyu.me/fix-open-webui-with-qwen3-5-3-6-can-not-generate-chat-title/)
  * ### [世界加钱可及？若干 AWS / GreenCloud / Lightlayer / RFCHOST / SiliCloud / Vultr 的日本/新加坡/香港/美国VPS全天ping测试](https://wusiyu.me/aws-greencloud-lightlayer-rfchost-silicloud-vultr-vps-compare/)


