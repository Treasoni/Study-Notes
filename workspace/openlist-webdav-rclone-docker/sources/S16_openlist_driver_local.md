---
url: "https://doc.oplist.org/guide/drivers/local"
title: "Local storage - OpenList Docs"
scraped_at: 2026-09-11T17:05:31+00:00
---

Menu
Return to top
# Local storage 
Support mounting the directory of the local machine.
支持挂载本机的目录。
## Root folder path [​](https://doc.oplist.org/guide/drivers/local#root-folder-path)
## 根文件夹ID [​](https://doc.oplist.org/guide/drivers/local#%E6%A0%B9%E6%96%87%E4%BB%B6%E5%A4%B9id)
The path of folder you wanted to mount. For example:
  * Linux: `/root`
  * Windows: `C:`


您要挂载的文件夹的路径。 例如：
  * Linux: `/root`
  * Windows: `C:`


## Local storage video thumbnail [​](https://doc.oplist.org/guide/drivers/local#local-storage-video-thumbnail)
## 本地存储视频封面 [​](https://doc.oplist.org/guide/drivers/local#%E6%9C%AC%E5%9C%B0%E5%AD%98%E5%82%A8%E8%A7%86%E9%A2%91%E5%B0%81%E9%9D%A2)
You need to use the `ffmpeg` tool to add.
需要使用 `ffmpeg` 工具来添加.
## Local storage PDF thumbnail on macOS [​](https://doc.oplist.org/guide/drivers/local#local-storage-pdf-thumbnail-on-macos)
## macOS 本地存储 PDF 缩略图 [​](https://doc.oplist.org/guide/drivers/local#macos-%E6%9C%AC%E5%9C%B0%E5%AD%98%E5%82%A8-pdf-%E7%BC%A9%E7%95%A5%E5%9B%BE)
On macOS, the Local storage driver can generate thumbnails from the first page of PDF files using the system Quick Look tool.
To enable this feature:
  1. Enable `Thumbnail`.
  2. Enable `PDF thumbnail`.
  3. It is recommended to configure `Thumb cache folder` to avoid rendering the same PDF repeatedly.


This feature is disabled by default and is only available when OpenList runs on macOS. Rendering is performed on cache misses and may consume additional CPU and memory.
在 macOS 上，本机存储驱动可以调用系统 Quick Look 工具，为 PDF 文件生成首页缩略图。
启用方法：
  1. 开启 `缩略图（Thumbnail）`。
  2. 开启 `PDF 缩略图（PDF thumbnail）`。
  3. 建议配置 `缩略图缓存目录（Thumb cache folder）`，避免重复渲染同一 PDF 文件。


该功能默认关闭，并且仅在 OpenList 运行于 macOS 时可用。缓存未命中时会执行渲染，可能额外消耗 CPU 和内存。
## Recycle bin path [​](https://doc.oplist.org/guide/drivers/local#recycle-bin-path)
## 回收站路径 [​](https://doc.oplist.org/guide/drivers/local#%E5%9B%9E%E6%94%B6%E7%AB%99%E8%B7%AF%E5%BE%84)
path to recycle bin, delete permanently if empty or keep 'delete permanently'
If you fill in this path, you will move the file into the folder when deleting the local storage file, so that you have a chance to regret it.
The method of filling in the above -mentioned mounting path is different from different system filling methods.
If you don’t know if you fill in it correctly, you can test it yourself first and then use the production environment to use it yourself.
  * Linux: `/root`
  * Windows: `C:`


回收站的路径，如果为空则永久删除或保持“永久删除”
如果填写此路径在删除本地存储文件时会将文件移动到此文件夹內，让你有一次后悔的机会。
填写方式参考上述挂载路径的方式不同系统填写方式不同。
如果不知道是否填写正确，可以先自己在测试环境进行测试一下再进行生产环境使用
  * Linux: `/root`
  * Windows: `C:`


## The default download method used [​](https://doc.oplist.org/guide/drivers/local#the-default-download-method-used)
## 默认使用的下载方式 [​](https://doc.oplist.org/guide/drivers/local#%E9%BB%98%E8%AE%A4%E4%BD%BF%E7%94%A8%E7%9A%84%E4%B8%8B%E8%BD%BD%E6%96%B9%E5%BC%8F)
## Contributors
[Edit this page on GitHub](https://github.com/OpenListTeam/OpenList-Docs/edit/main/pages/guide/drivers/local.md)
Last updated: 
