![](assets/qBittorent的Tracker/file-20260202222958349.png)
# 1.  Tracker 是干嘛的？（一句话版）

> **Tracker 就是“告诉你：谁手里有这个文件”的服务器**

没有 Tracker，qBittorrent **不知道该去连谁**。

# 2. BT 下载到底在干什么？（一步一步）

你点“下载”的时候，qBittorrent其实要完成 **三件事**：

## 2.1 第一步：拿到「元数据」（metadata）

也就是：

>- 文件列表
>- 每个文件多大
>- 分成多少块

👉 你现在 **就卡在这一步**

## 2.2  第二步：找人（Peers）

找人的方式有 **3 种**：

|方式|作用|
|---|---|
|**Tracker**|问服务器「谁在做种」|
|**DHT**|去 BT 网络里“广播问”|
|**PeX / LSD**|从已连接的人那打听|


## 2.3 📥 第三步：开始下数据

只有 **前两步成功**，才会写文件。

# 3. 无法现在是为什么？
![](assets/qBittorent的Tracker/file-20260202222958349.png)

结合你截图里的信息：

- Tracker 页面是空的
- 种子数：`0 (4338)`
- 状态：**下载元数据**
- 下载速度：0 B/s

👉 **这说明：**

- ✅ torrent 加成功了
- ❌ 但 **Tracker 全部连不上**
- ❌ DHT 也没起作用（被墙 / 被阻断）

# 4. 如何解决？

## 4.1 检查并添加 Tracker

手动添加 Tracker 列表：

1. **打开「Trackers」标签页**
2. **复制 Tracker 列表**（从以下来源）
3. **右键 → 手动添加 Tracker**

推荐 Tracker 列表：

| 来源 | 链接 |
|------|------|
| 中文合集 | https://trackerslist.com/ |
| GitHub 项目 | https://github.com/XIU2/TrackersListCollection |
| Nanodesu Int | https://ngosang.github.io/trackerslist/ |

## 4.2 启用 DHT 和 PEX

**设置 → BitTorrent**

- ✅ **启用 DHT**（去中心化追踪）
- ✅ **启用 Local Peer Discovery**（局域网发现）
- ✅ **启用 Peer Exchange**（节点交换）

## 4.3 端口转发

确保下载端口可以访问：

**设置 → 连接**

- **监听端口**：默认 6881
- **UPnP / NAT-PMP**：如果路由器支持可以开启
- **手动端口转发**：在路由器上映射端口

## 4.4 使用代理（参考「qBittorrent配置代理.md」）

如果 Tracker 被墙，需要通过代理连接：

**设置 → 连接 → 代理服务器**

- 类型：SOCKS5
- 填入你的代理地址

# 5. Tracker 状态说明

| 状态 | 含义 | 处理 |
|------|------|------|
| **Working** | 正常工作 | ✅ 无需操作 |
| **Updating** | 正在更新 | ✅ 等待即可 |
| **Not Working** | 连接失败 | ❌ 检查网络/代理 |
| **Not Contacted** | 未连接 | ❌ 手动更新或添加 Tracker |
| **Disabled** | 已禁用 | ⚠️ 手动启用 |

# 6. 常见问题排查

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