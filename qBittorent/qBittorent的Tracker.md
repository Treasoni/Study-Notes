---
title: qBittorrent Tracker 配置详解
created: 2026-02-05
updated: 2026-04-05
tags:
  - qBittorrent
  - Tracker
  - BT下载
---

# qBittorrent Tracker 配置详解

## 1. Tracker 是干嘛的？（一句话版）

> **Tracker 就是"告诉你：谁手里有这个文件"的服务器**

没有 Tracker，qBittorrent **不知道该去连谁**。

---

## 2. BT 下载到底在干什么？（一步一步）

你点"下载"的时候，qBittorrent 其实要完成 **三件事**：

### 2.1 第一步：拿到「元数据」（metadata）

也就是：

- 文件列表
- 每个文件多大
- 分成多少块

> [!warning] 当前状态
> 如果卡在"下载元数据"，说明你就卡在这一步

### 2.2 第二步：找人（Peers）

找人的方式有 **3 种**：

| 方式 | 作用 |
|------|------|
| **Tracker** | 问服务器「谁在做种」 |
| **DHT** | 去 BT 网络里"广播问" |
| **PeX / LSD** | 从已连接的人那打听 |

### 2.3 第三步：开始下数据

只有 **前两步成功**，才会写文件。

---

## 3. 无法下载是为什么？

![](assets/qBittorent的Tracker/截屏2026-02-05%2021.08.11.png)

结合截图里的信息：

- Tracker 页面是空的
- 种子数：`0 (4338)`
- 状态：**下载元数据**
- 下载速度：0 B/s

**这说明：**

- torrent 加成功了
- 但 **Tracker 全部连不上**
- DHT 也没起作用（被墙 / 被阻断）

---

## 4. 如何解决？

### 4.1 检查并添加 Tracker

手动添加 Tracker 列表：

1. **打开「Trackers」标签页**
2. **复制 Tracker 列表**（从以下来源）
3. **右键 -> 手动添加 Tracker**

**推荐 Tracker 列表**（XIU2 项目，每日更新）：

| 列表类型 | 地址 | 数量 |
|---------|------|------|
| BEST（推荐） | `https://cf.trackerslist.com/best.txt` | 81 个 |
| ALL（完整） | `https://cf.trackerslist.com/all.txt` | 149 个 |
| HTTP only | `https://cf.trackerslist.com/http.txt` | 72 个 |

**备用 CDN 地址**：
- jsDelivr：`https://cdn.jsdelivr.net/gh/XIU2/TrackersListCollection/best.txt`
- Raw GitHub：`https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/best.txt`

> [!info] 来源
> - [XIU2/TrackersListCollection](https://github.com/XIU2/TrackersListCollection) - GitHub 项目主页（30.9k+ Stars）
> - [trackerslist.com](https://trackerslist.com/#/zh) - 中文介绍页

### 4.2 启用 DHT 和 PEX

**设置 -> BitTorrent**

- **启用 DHT**（去中心化追踪）
- **启用 Local Peer Discovery**（局域网发现）
- **启用 Peer Exchange**（节点交换）

### 4.3 端口转发

确保下载端口可以访问：

**设置 -> 连接**

- **监听端口**：默认 6881
- **UPnP / NAT-PMP**：如果路由器支持可以开启
- **手动端口转发**：在路由器上映射端口

### 4.4 使用代理

如果 Tracker 被墙，需要通过代理连接：

**设置 -> 连接 -> 代理服务器**

- 类型：SOCKS5
- 填入你的代理地址

> [!tip] 详细配置
> 参见 [[qBittorent配置代理]] 获取完整的代理配置指南

---

## 5. Tracker 状态说明

| 状态 | 含义 | 处理 |
|------|------|------|
| **Working** | 正常工作 | 无需操作 |
| **Updating** | 正在更新 | 等待即可 |
| **Not Working** | 连接失败 | 检查网络/代理 |
| **Not Contacted** | 未连接 | 手动更新或添加 Tracker |
| **Disabled** | 已禁用 | 手动启用 |

---

## 6. 常见问题排查

### Q: Tracker 全是 "Not Working"

**可能原因：**
- 网络无法访问 Tracker
- Tracker 服务器已关闭
- 需要代理访问

**解决：** 检查网络，配置代理，或更换 Tracker 列表

### Q: 种子数一直是 0

**可能原因：**
- 种子资源已死（无人做种）
- Tracker 连不上
- DHT 未启用

**解决：**
- 检查 Tracker 连接状态
- 启用 DHT
- 尝试重新下载磁力链接

### Q: 下载速度慢

**检查：**
- Tracker 状态是否正常
- DHT 节点数（状态栏）
- 连接的 Peers 数量

---

## 相关笔记

- [[qBittorrent的使用]] - qBittorrent 使用指南
- [[qBittorent PT站点与分享率]] - PT 站点与分享率管理
- [[qBittorent配置代理]] - 代理配置指南

---

## 参考资料

### 官方资源

- [qBittorrent 官方网站](https://www.qbittorrent.org/) - 下载与文档
- [qBittorrent GitHub](https://github.com/qbittorrent/qBittorrent) - 源代码与 Issues
- [WebUI API 文档 (v5.0)](https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-5.0)) - API 参考

### Tracker 列表

- [XIU2/TrackersListCollection](https://github.com/XIU2/TrackersListCollection) - Tracker 列表（每日更新）
- [trackerslist.com](https://trackerslist.com/#/zh) - 中文介绍页

### 社区教程

- [Best qBittorrent Settings 2026](https://www.rapidseedbox.com/blog/qbittorrent-settings) - RapidSeedbox 优化指南

---
*最后更新：2026-04-05*
