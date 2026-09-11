---
url: "https://doc.oplist.org/guide/advanced/webdav"
title: "WebDAV - OpenList Docs"
scraped_at: 2026-09-11T17:03:39+00:00
---

Menu
Return to top
# WebDAV 
WebDAV (Web Distributed Authoring and Versioning) is a set of extensions to the Hypertext Transfer Protocol (HTTP) that enables users to collaboratively create, edit, and manage files directly on a web server.
OpenList can be served as a WebDAV server, allowing users to access and modify files through a web interface.
WebDAV（Web 分布式创作和版本控制）是一种扩展超文本传输协议（HTTP）的协议，它允许用户使用 Web 服务器上的文件。
OpenList 可以作为 WebDAV 服务器，允许用户通过 Web 界面访问和修改网盘内的文件。
## Permission Configuration Instructions [​](https://doc.oplist.org/guide/advanced/webdav#permission-configuration-instructions)
## 权限配置说明 [​](https://doc.oplist.org/guide/advanced/webdav#%E6%9D%83%E9%99%90%E9%85%8D%E7%BD%AE%E8%AF%B4%E6%98%8E)
To enable a specific user to use WebDAV, the following permissions must be enabled in the `User => Permissions` settings:
  1. **WebDAV Read**
     * This permission must be enabled to **view and read** files and directories in WebDAV.
     * If the user **only needs to view or play files** , enabling this permission is sufficient.
  2. **WebDAV Management**
     * This permission must be enabled to perform **write operations** (such as create, modify, delete, etc.).
     * **Enabling only`WebDAV Management` is not enough!** You must also enable `WebDAV Management` **as well as** the specific file system permissions required for the planned operations (such as `rename`, `delete`, `copy`, `create directories or upload`, etc.).


要使特定用户能够使用 WebDAV，需在 `用户 => 权限` 设置中为其开启以下权限：
  1. **WebDAV 读取**
     * 必须开启此权限才能**查看和读取** WebDAV 中的文件和目录。
     * 如果用户**仅需查看或播放文件** ，开启此权限即可。
  2. **WebDAV 管理**
     * 必须开启此权限才能进行**写入操作** （创建、修改、删除等）。
     * **仅开启`WebDAV 管理` 还不够！** 需要同时开启 `WebDAV 管理` **以及** 其计划执行操作所需的具体文件系统权限（如 `重命名`、`删除`、`复制`、`创建目录或上传` 等）。


## Basic Connection Configuration [​](https://doc.oplist.org/guide/advanced/webdav#basic-connection-configuration)
## 基础连接配置 [​](https://doc.oplist.org/guide/advanced/webdav#%E5%9F%BA%E7%A1%80%E8%BF%9E%E6%8E%A5%E9%85%8D%E7%BD%AE)
Use the following parameters to connect your WebDAV client:  
| Configuration Item  | Value / Description  |  
| --- | --- |  
| **Url**  | `http[s]://your-domain:port/dav/`  |  
| **Host**  | Your domain (e.g., `openlist.example.com`)  |  
| **Path**  | `dav`  |  
| **Protocol**  |  `http` or `https` (strongly recommend using **https** for security)  |  
| **Port**  | The port **must be identical** to the one used for accessing the OpenList web interface  |  
| **Username**  | The **username** you use to log into the OpenList web interface  |  
| **Password**  | The **password** you use to log into the OpenList web interface  |  
使用以下参数连接你的 WebDAV 客户端：  
| 配置项  | 值 / 说明  |  
| --- | --- |  
| **Url**  | `http[s]://你的域名:端口/dav/`  |  
| **Host / 主机**  | 你的域名 (例如: `openlist.example.com`)  |  
| **路径 / Path**  | `dav`  |  
|  `http` 或 `https` (强烈建议使用 **https** 以保障安全)  |  
| 与访问 OpenList 网页端使用的端口**完全一致**  |  
| **用户名**  | 你在 OpenList 网页端登录使用的**用户名**  |  
| 你在 OpenList 网页端登录使用的**密码**  |  
## Storage Support [​](https://doc.oplist.org/guide/advanced/webdav#storage-support)
## 存储支持 [​](https://doc.oplist.org/guide/advanced/webdav#%E5%AD%98%E5%82%A8%E6%94%AF%E6%8C%81)
WIP, please stay tuned
WARNING
Renaming during copy is not currently supported.
WARNING
暂不支持复制时重命名。
## Client Software [​](https://doc.oplist.org/guide/advanced/webdav#client-software)
## 客户端软件 [​](https://doc.oplist.org/guide/advanced/webdav#%E5%AE%A2%E6%88%B7%E7%AB%AF%E8%BD%AF%E4%BB%B6)
The following is a list of software that can be used to mount or access WebDAV services, categorized by platform:
以下是一些可用于挂载或访问 WebDAV 服务的软件，按平台分类：
### 🖥️ Windows [​](https://doc.oplist.org/guide/advanced/webdav#%F0%9F%96%A5%EF%B8%8F-windows)
  * **File Managers / Mounting Tools:**
    * [RaiDrive](https://www.raidrive.com/) (Recommended for mounting)
    * [Mountain Duck](https://mountainduck.io/) (Mount as a disk)
    * [rclone](https://rclone.org/) (Command line/mounting)
    * [OneCommander](https://www.onecommander.com/) (File manager)
  * **Media Players (Direct Playback):**
    * [AIMP](https://www.aimp.ru/) (Audio player)


  * **文件管理器 / 挂载工具:**
    * [RaiDrive](https://www.raidrive.com/) (推荐挂载)
    * [Mountain Duck](https://mountainduck.io/) (挂载为磁盘)
    * [rclone](https://rclone.org/) (命令行/挂载)
    * [OneCommander](https://www.onecommander.com/) (文件管理器)
  * **媒体播放器 (可直接播放):**
    * [AIMP](https://www.aimp.ru/) (音频播放器)


### 📱 Android [​](https://doc.oplist.org/guide/advanced/webdav#%F0%9F%93%B1-android)
  * **File Managers:**
    * [MiXplorer](https://mixplorer.com/) (Manual APK installation required, open source)
    * ES File Explorer
  * **Media Players (Direct Playback):**
    * [VLC for Android](https://www.videolan.org/vlc/download-android.html) (Open source)


  * **文件管理器:**
    * [MiXplorer](https://mixplorer.com/) (需手动安装 APK, 开源)
    * ES 文件管理器
  * **媒体播放器 (可直接播放):**
    * [VLC for Android](https://www.videolan.org/vlc/download-android.html) (开源)


### 🍎 iOS / iPadOS [​](https://doc.oplist.org/guide/advanced/webdav#%F0%9F%8D%8E-ios-ipados)
  * **Media Players / File Managers (Direct Playback / Management):**


  * **媒体播放器 / 文件管理器 (可直接播放/管理):**


### 📺 TV (Android TV / Google TV) [​](https://doc.oplist.org/guide/advanced/webdav#%F0%9F%93%BA-tv-android-tv-google-tv)
  * **Media Players (Direct Playback):**


  * **媒体播放器 (可直接播放):**


### 🍏 macOS [​](https://doc.oplist.org/guide/advanced/webdav#%F0%9F%8D%8F-macos)
  * **File Managers / Mounting Tools:**
    * [Mountain Duck](https://mountainduck.io/) (Mount as a disk)
    * [rclone](https://rclone.org/) (Command line/mounting)
  * **Media Players (Direct Playback):**
    * [IINA](https://iina.io/) (Open source)


  * **文件管理器 / 挂载工具:**
    * [Mountain Duck](https://mountainduck.io/) (挂载为磁盘)
    * [rclone](https://rclone.org/) (命令行/挂载)
  * **媒体播放器 (可直接播放):**
    * [IINA](https://iina.io/) (开源)


### 🐧 Linux [​](https://doc.oplist.org/guide/advanced/webdav#%F0%9F%90%A7-linux)
  * **Mounting Tools / Command Line:**
    * [rclone](https://rclone.org/) (Recommended, feature-rich)
    * `davfs2` (System-level mounting, requires configuration)


  * **挂载工具 / 命令行:**
    * [rclone](https://rclone.org/) (推荐, 功能强大)
    * `davfs2` (系统级挂载, 需配置)


### 📝 Note-taking Software [​](https://doc.oplist.org/guide/advanced/webdav#%F0%9F%93%9D-note-taking-software)
### 📝 笔记软件 [​](https://doc.oplist.org/guide/advanced/webdav#%F0%9F%93%9D-%E7%AC%94%E8%AE%B0%E8%BD%AF%E4%BB%B6)
  * [Joplin](https://joplinapp.org/) (Supports WebDAV sync for notes, open source)


> **Feel free to contribute!** If you find other excellent and compatible WebDAV clients, feel free to recommend them.
  * [Joplin](https://joplinapp.org/) (支持 WebDAV 同步笔记, 开源)


> **欢迎补充！** 如果你发现其他优秀且兼容的 WebDAV 客户端，欢迎推荐。
## Client Configuration Examples [​](https://doc.oplist.org/guide/advanced/webdav#client-configuration-examples)
## 客户端配置示例 [​](https://doc.oplist.org/guide/advanced/webdav#%E5%AE%A2%E6%88%B7%E7%AB%AF%E9%85%8D%E7%BD%AE%E7%A4%BA%E4%BE%8B)
The interfaces of different software vary, but the key is to correctly fill in the information from the "Basic Connection Configuration" above.
不同软件界面各异，核心是正确填写上面“基础连接配置”中的信息。
### nPlayer (iOS/Android) [​](https://doc.oplist.org/guide/advanced/webdav#nplayer-ios-android)
### Reex (Android) [​](https://doc.oplist.org/guide/advanced/webdav#reex-android)
### ES File Explorer (iOS & Android) [​](https://doc.oplist.org/guide/advanced/webdav#es-file-explorer-ios-android)
### ES 文件浏览器 (iOS & Android) [​](https://doc.oplist.org/guide/advanced/webdav#es-%E6%96%87%E4%BB%B6%E6%B5%8F%E8%A7%88%E5%99%A8-ios-android)
### Infuse (iOS/macOS) [​](https://doc.oplist.org/guide/advanced/webdav#infuse-ios-macos)
### Fileball (iOS) [​](https://doc.oplist.org/guide/advanced/webdav#fileball-ios)
### PotPlayer (Windows) [​](https://doc.oplist.org/guide/advanced/webdav#potplayer-windows)
### Synology NAS (Add via File Station) [​](https://doc.oplist.org/guide/advanced/webdav#synology-nas-add-via-file-station)
### 群晖 NAS (通过 File Station 添加) [​](https://doc.oplist.org/guide/advanced/webdav#%E7%BE%A4%E6%99%96-nas-%E9%80%9A%E8%BF%87-file-station-%E6%B7%BB%E5%8A%A0)
## Contributors
[Edit this page on GitHub](https://github.com/OpenListTeam/OpenList-Docs/edit/main/pages/guide/advanced/webdav.md)
Last updated: 
