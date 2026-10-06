# 把 SMB/CIFS 共享文件夹挂载到 Linux 服务器 - 意图文件

## 基本信息

- **主题**: 把 SMB/CIFS 共享文件夹挂载到 Linux 服务器
- **项目标识**: smb-cifs-mount-linux
- **运行标识**: smb-cifs-mount-linux
- **工作流**: learning-note-flow
- **创建时间**: 2026-09-18
- **当前阶段**: 阶段 6（Obsidian 美化与发布）
- **输出目标**: project-output（`workspace/smb-cifs-mount-linux/output/`）+ Obsidian vault 发布
- **Vault 路径**: `D:\Study-Notes`
- **笔记目录**: `linux/SMB挂载/`（拆分系列：`SMB挂载-00-总目录.md` + `SMB挂载-01..05-*.md`）
- **MOC 路径**: `linux/linux MOC.md`（另在 `docker/Docker MOC.md` 加第 5 册索引）

## 学习目标

### 笔记类型
实战笔记（附 SMB vs NFS 协议选择对比）

### 学习深度
上手实战：手动挂载 → 凭据文件 → fstab 开机自动挂载 → 掉线/权限/版本协商排错

### 用户基础
有了解（用户已有 Debian / Ubuntu 服务器运维经验，做过 FNOS、iStoreOS、Docker、LVM 等主题）

### 原始提问
> 我如何把 sma 共享文件的协议挂载到我的 Linux 服务器中？

注：`sma` 按 SMB 笔误处理，已与用户确认走 SMB/CIFS 主线。

## 研究计划

### 范围界定
- **挂载端（重点）**: Debian / Ubuntu Linux 服务器，`cifs-utils` 生态
- **共享端（例子）**: 服务端写法保持通用；具体示例覆盖飞牛 FNOS NAS 与 Windows 共享
- **关联既有笔记**: `网络协议详解-WebDAV_Samba_FTP_iSCSI.md`（仅一行 `mount -t cifs`）、`workspace/openlist-webdav-rclone-docker/`（挂载类主题，可复用挂载/排错写作模式）

### 探索方向
1. 共享协议选型：SMB/CIFS vs NFS vs WebDAV，什么场景挂哪种
2. 手动挂载实操：`cifs-utils` 安装、`mount -t cifs`、`-o` 选项全集（`vers`、`uid/gid`、`file_mode/dir_mode`、`iocharset`）
3. 持久化挂载：凭据文件（`credentials=`）权限、`/etc/fstab` 写法、`_netdev`/`nofail`/`x-systemd.automount` 与开机顺序陷阱
4. 排错与运维：`mount error(13/112/2)` 含义、SMB 方言协商、掉线重连、`smbclient` 诊断、只读/写权限不符
5. 无人值守场景：systemd mount unit、Docker 容器内挂载共享卷的差异

### 重点收集
- **核心概念**: SMB/CIFS 与 NFS 的定位差异、UNC 路径、SMB 版本/方言（SMB1/2/3）、挂载点语义
- **实战代码**: `cifs-utils` 安装、带凭据文件的完整 `mount` 命令、`/etc/fstab` 行、`credentials` 文件权限、systemd unit 示例、`smbclient -L` 探测命令
- **常见坑**: fstab 启动顺序导致开机卡死/挂载失败、凭据文件权限过宽被拒、`uid/gid` 与文件权限不符、中文文件名乱码、SMB1 被禁用、NAS 休眠唤醒后失联
- **工具链**: `cifs-utils`、`smbclient`、`mount.cifs`、`systemd` mount units、`findmnt`、`dmesg`/`journalctl`

### 信源偏好
- 官方文档: 是（Samba 官方 wiki、Linux man pages `mount.cifs(8)`、Microsoft SMB 文档、Debian/Ubuntu 文档）
- 技术博客: 是（作为排错案例补充，需标注来源层级）
- 社区讨论: 是（Forum / AskUbuntu / Superuser，仅用于实例佐证）
- 学术论文: 否

## 备注

- 待用户确认后可补充：具体服务器发行版版本、共享端设备型号（若影响 SMB 方言设置）、是否需要覆盖 Docker 容器内挂载场景。
- Obsidian 发布位置（vault_path / note_folder / moc_path）留待阶段 6 前确认。
