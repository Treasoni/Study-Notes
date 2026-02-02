---
tags:
  - qBittorent
---

前提：我的qBittorent配置在pve中的linux中的docker里，我还在pve中搭建了istores旁路由。
# 1. 给 qBittorrent 配代理（核心步骤）

## 1.1打开 qBittorrent WebUI

进入：

`设置 → 连接`
![](assets/qBittorent配置代理/file-20260202223705113.png)

## 1.2 代理服务器设置这样填👇
**混合代理（重点）**

`192.168.110.119:7893`
这是：

- Clash 的 **代理入口**
- 同时支持：
    - HTTP
    - SOCKS5

![](assets/qBittorent配置代理/截屏2026-02-02%2022.35.34.png)

| 项目  | 值                                    |
| --- | ------------------------------------ |
| 类型  | **SOCKS5**                           |
| 主机  | **iStoreOS 的 IP**（如 192.168.110.119） |
| 端口  | **7893**                             |
| 用户名 | 留空                                   |
| 密码  | 留空                                   |
> [!warning]

> ⚠️ 这是重点警告
	qb → iStoreOS 上的 Clash（局域网）
	而 Clash 默认对局域网代理是：无认证的
