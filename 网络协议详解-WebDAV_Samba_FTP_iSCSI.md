# 网络协议详解：WebDAV、Samba、FTP、iSCSI

## 目录
1. [WebDAV](#webdav)
2. [Samba](#samba)
3. [FTP](#ftp)
4. [iSCSI](#iscsi)
5. [对比总结](#对比总结)
6. [选择建议](#选择建议)

---

## WebDAV

### 什么是WebDAV？

**WebDAV**（Web Distributed Authoring and Versioning）是基于HTTP协议的扩展协议。

> **通俗理解**：你可以把它想象成"增强版的HTTP"。普通HTTP只能"读取"网页，而WebDAV让你能"读写"文件，就像在本地操作文件一样，但操作的是远程服务器上的文件。

**核心特点**：
- 基于HTTP（通常使用80/443端口）
- 支持文件的创建、读取、更新、删除（CRUD操作）
- 支持文件锁定（防止多人同时编辑冲突）
- 支持文件属性查询
- 支持目录管理

### 应用场景

| 场景 | 说明 |
|------|------|
| **网盘服务** | 百度网盘、坚果云等云端存储服务 |
| **代码协作** | Subversion（SVN）版本控制系统使用WebDAV |
| **办公文档协作** | 在线Office工具 |
| **跨平台文件共享** | Windows、Mac、Linux都能访问的文件共享 |

### 如何使用

#### Windows连接WebDAV

1. 打开"此电脑"
2. 点击"映射网络驱动器"或在地址栏输入：
   ```
   https://你的服务器地址/webdav路径
   ```
3. 输入用户名和密码
4. 挂载成功后可像本地磁盘一样操作

#### Mac连接WebDAV

1. 打开"访达"（Finder）
2. 顶部菜单栏选择"前往" → "连接服务器"
3. 输入地址：`https://你的服务器地址/webdav路径`
4. 输入用户名密码连接

#### Linux连接WebDAV

```bash
# 安装 davfs2
sudo apt install davfs2

# 挂载
sudo mount -t davfs https://你的服务器地址/webdav路径 /挂载点
```

---

## Samba

### 什么是Samba？

**Samba**是Linux/Unix系统上实现SMB/CIFS协议的开源软件。

> **通俗理解**：Samba让Linux服务器能"说Windows的语言"。Windows局域网中大家共享文件夹用的是SMB协议，Samba让Linux也能参与这个"Windows文件共享聚会"。

**核心特点**：
- 实现SMB/CIFS协议
- 让Linux服务器与Windows系统无缝集成
- 支持文件和打印机共享
- 支持用户认证和权限控制
- 支持域控制器功能

### 应用场景

| 场景 | 说明 |
|------|------|
| **局域网文件共享** | 公司内部文件服务器 |
| **家庭NAS** | 群晖、威联通等NAS设备 |
| **Windows与Linux互通** | 让Linux文件服务器服务Windows客户端 |
| **打印机共享** | 局域网内共享打印机 |

### 如何使用

#### Windows连接Samba共享

1. 打开"此电脑"
2. 地址栏输入：`\\你的服务器IP\共享文件夹名`
3. 输入用户名密码

#### Mac连接Samba共享

1. 打开"访达"
2. "前往" → "连接服务器"
3. 输入：`smb://你的服务器IP/共享文件夹名`

#### Linux配置Samba服务器

```bash
# 安装Samba
sudo apt install samba

# 配置共享（编辑 /etc/samba/smb.conf）
[共享名]
   path = /共享路径
   browseable = yes
   writable = yes
   valid users = 用户名

# 创建用户
sudo smbpasswd -a 用户名

# 重启服务
sudo systemctl restart smbd
```

#### Linux连接Samba

```bash
# 安装客户端
sudo apt install cifs-utils

# 挂载
sudo mount -t cifs //服务器IP/共享名 /挂载点 -o username=用户名
```

---

## FTP

### 什么是FTP？

**FTP**（File Transfer Protocol）是最古老、最经典的文件传输协议。

> **通俗理解**：FTP就像是"快递员"。它专门负责把文件从一台电脑"快递"到另一台电脑，不管这两台电脑是什么系统，只要都"懂"FTP语言就行。

**核心特点**：
- 使用21端口（控制连接）和20端口（数据连接）
- 支持主动模式和被动模式
- 支持断点续传
- 支持匿名访问和认证访问
- 历史悠久，几乎所有设备都支持

### 应用场景

| 场景 | 说明 |
|------|------|
| **网站文件上传** | 上传网页文件到服务器 |
| **大文件传输** | 传输视频、安装包等大文件 |
| **批量文件操作** | 批量上传下载文件 |
| **自动化任务** | 通过脚本定时同步文件 |

### 如何使用

#### 使用客户端连接

**常用客户端**：FileZilla、WinSCP、lftp

**FileZilla配置**：
1. 主机：`你的服务器IP`
2. 用户名和密码
3. 端口：21
4. 点击"快速连接"

#### 命令行使用

```bash
# 连接
ftp 你的服务器IP

# FTP命令
put 文件名          # 上传文件
get 文件名          # 下载文件
mput *              # 批量上传
mget *              # 批量下载
ls                  # 列出文件
cd 目录名           # 切换目录
lcd 目录名          # 切换本地目录
bye                 # 退出
```

#### Linux配置FTP服务器（vsftpd）

```bash
# 安装
sudo apt install vsftpd

# 配置 /etc/vsftpd.conf
anonymous_enable=NO       # 禁止匿名
local_enable=YES          # 允许本地用户
write_enable=YES          # 允许写入
chroot_local_user=YES     # 用户限制在主目录

# 重启
sudo systemctl restart vsftpd
```

---

## iSCSI

### 什么是iSCSI？

**iSCSI**（Internet Small Computer System Interface）是基于TCP/IP网络的SCSI协议实现。

> **通俗理解**：SCSI是"硬盘接口语言"，传统用于连接本地硬盘。iSCSI把SCSI"打包"进TCP/IP，让远方的硬盘"看起来"就像本地硬盘一样——你的电脑会以为那块硬盘是直接插在主板上的，尽管它可能在几公里外的数据中心。

**核心特点**：
- 基于TCP/IP（通常使用3260端口）
- 块级存储传输（传输整个磁盘块，不是文件）
- 支持多路径、负载均衡
- 支持存储级复制和快照
- 性能接近本地存储

### 应用场景

| 场景 | 说明 |
|------|------|
| **服务器虚拟化** | VMware、Hyper-V、KVM的共享存储 |
| **数据库集群** | 多台服务器共享同一块存储 |
| **企业存储中心** | SAN（存储区域网络） |
| **灾备方案** | 远程存储镜像 |

### 与文件共享协议的本质区别

| 类型 | 协议示例 | 传输单位 | 客户端看到的是 |
|------|----------|----------|----------------|
| **文件级共享** | WebDAV、Samba、FTP | 文件 | 远程文件夹中的文件 |
| **块级共享** | iSCSI | 磁盘块 | 一块全新的本地磁盘 |

> 这个区别很重要：Samba共享让你访问"远程文件夹里的文件"，iSCSI给你"一块好像插在你电脑上的硬盘"。

### 如何使用

#### 配置iSCSI目标端（服务器）

**Linux使用targetcli配置**：

```bash
# 安装
sudo apt install targetcli-fb

# 配置
sudo targetcli

# 进入配置界面后
/> backstores/block create name=共享磁盘 dev=/dev/sdb1
/> iscsi/ create iqn.2024-01.com.example:storage
/> iscsi/iqn.2024-01.com.example:storage/tpg1/luns create /backstores/block/共享磁盘
/> iscsi/iqn.2024-01.com.example:storage/tpg1/acls create iqn.2024-01.com.example:client
/> iscsi/iqn.2024-01.com.example:storage/tpg1/portals create 0.0.0.0 3260
/> exit
```

#### 配置iSCSI发起端（客户端）

```bash
# 安装
sudo apt install open-iscsi

# 发现目标
sudo iscsiadm -m discovery -t st -p 服务器IP:3260

# 连接
sudo iscsiadm -m node -T iqn.2024-01.com.example:storage -p 服务器IP:3260 -l

# 查看连接的磁盘
sudo fdisk -l

# 分区格式化使用（这会显示为新磁盘）
sudo mkfs.ext4 /dev/sdX
sudo mount /dev/sdX /挂载点
```

---

## 对比总结

### 功能对比表

| 特性 | WebDAV | Samba | FTP | iSCSI |
|------|--------|-------|-----|-------|
| **协议基础** | HTTP | SMB | TCP | TCP/IP + SCSI |
| **传输层级** | 文件级 | 文件级 | 文件级 | 块级 |
| **跨平台** | 优秀 | Windows最佳 | 优秀 | 好 |
| **网络穿透** | 好（HTTP） | 局域网为主 | 主动模式需配置 | 灵活 |
| **加密** | HTTPS支持 | VPN配合 | FTPS/SFTP | CHAP/IPSec |
| **适合用途** | 网盘、协作 | 局域网共享 | 文件传输 | 存储虚拟化 |

### 性能对比

| 场景 | 最佳选择 | 次优选择 |
|------|----------|----------|
| **局域网文件共享** | Samba | WebDAV |
| **互联网访问** | WebDAV | FTP（加密） |
| **大文件传输** | FTP | Samba |
| **虚拟化存储** | iSCSI | NFS |
| **多用户协作编辑** | WebDAV | Samba |

### 安全性对比

| 协议 | 默认安全 | 增强方式 |
|------|----------|----------|
| WebDAV | 基本认证 | HTTPS + OAuth2 |
| Samba | 弱（NTLM） | AD域 + VPN |
| FTP | 明文传输 | FTPS/SFTP |
| iSCSI | CHAP认证 | CHAP + IPSec |

---

## 选择建议

### 场景决策树

```
需要什么？
├─ 网盘/云存储服务 → WebDAV
├─ 局域网内共享文件给Windows → Samba
├─ 批量上传下载大文件 → FTP
├─ 服务器虚拟化/集群存储 → iSCSI
├─ 跨平台协作编辑文档 → WebDAV
└─ 家庭NAS给多设备共享 → Samba + WebDAV（双协议）
```

### 具体建议

**个人/家庭用户**：
- 局域网共享：Samba
- 远程访问：WebDAV（通过HTTPS）

**企业办公**：
- Windows环境：Samba + AD域
- 混合环境：WebDAV + Samba

**开发运维**：
- 代码协作：WebDAV（SVN）
- 备份传输：FTP/SFTP

**数据中心/服务器**：
- 虚拟化：iSCSI
- 集群：iSCSI

---

## 补充说明

### 端口速查

| 协议 | 标准端口 | 说明 |
|------|----------|------|
| WebDAV | 80/443 | HTTP/HTTPS |
| Samba | 139/445 | 139(NBT), 445(SMB) |
| FTP | 20/21 | 21(控制), 20(数据) |
| FTPS | 990 | 显式TLS |
| SFTP | 22 | SSH协议 |
| iSCSI | 3260 | TCP |

### 常见问题

**Q: FTP和SFTP有什么区别？**
A: FTP是独立协议，SFTP是SSH的一部分，SFTP更安全。

**Q: Samba能否互联网访问？**
A: 技术上可以，但不推荐（性能和安全都不如WebDAV），建议配合VPN使用。

**Q: iSCSI能否多主机同时写入？**
A: 需要集群文件系统（如GFS2、OCFS2）支持，否则会有数据损坏风险。

**Q: WebDAV和Samba选哪个？**
A: 局域网选Samba（更快），互联网选WebDAV（穿透性好）。

---

*文档版本：v1.0*
*创建日期：2026-02-10*
