---
url: "https://alistgo.com/guide/webdav.html"
title: "WebDav | AList Docs"
scraped_at: 2026-09-11T17:05:11+00:00
---

[Skip to main content](https://alistgo.com/guide/webdav.html#main-content)
# WebDav
September 7, 2022WebdavGuideAbout 2 min
Tips
≥ v3.42.0 The above versions need to open the two permissions of `Webdav Read` and `Webdav Manage` in User => Permissions
  * If you only read and do not modify, you only need to open `Webdav Read`
  * If you want to add, delete or modify files, you need to open `Webdav manage` permissions and also need `Make dir or upload`, `Delete`, `Rename`, `Move`, `Copy` and other permissions. You can selectively open them according to your needs.


Besides, since v3.42.0, writing to WebDAV not only requires the `Webdav Manage` permission but also basic permissions such as `rename`, `delete`, and `copy`.
### [**WebDAV config**](https://alistgo.com/guide/webdav.html#webdav-config)  
| Name  | Value  |  
| --- | --- |  
| Url  | http[s]://domain:port/dav/  |  
| Host  | domain  |  
| Path  | dav  |  
| Scheme  | http/https  |  
| Port  | Same as web port  |  
| Username  | Same as web username  |  
| Password  | Same as web password  |  
Can't fill in? [Click to view Fill in Example](https://alistgo.com/guide/webdav.html#webdav-fill-in-example)
### [**WebDav Support**](https://alistgo.com/guide/webdav.html#webdav-support)  
| Storage strategy  | list  | download  | mkdir  | rename  | move  | copy  | upload  |  
| --- | --- | --- | --- | --- | --- | --- | --- |  
| LocalStorage  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |  
| AliyunDirve  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |  
| Onedrive  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |  
| 189Cloud  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |  
| GoogleDrive  | ✅  | ✅  | ✅  | ✅  | ✅  | ❌  | ✅  |  
| 123pan  | ✅  | ✅  | ✅  | ✅  | ✅  | ❌  | ✅  |  
| FTP  | ✅  | ✅  | ✅  | ✅  | ✅  | ❌  | ✅  |  
| SFTP  | ✅  | ✅  | ✅  | ✅  | ✅  | ❌  | ✅  |  
| PikPak  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |  
| S3  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |  
| USS  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |  
| WebDAV  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |  
| Teambition  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |  
| Mediatrack  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |  
| 139yun  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |  
| YandexDisk  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |  
| BaiduNetdisk  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |  
| Quark  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |  
| KodBox  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |  
## [**Software that can be used to mount WebDav**](https://alistgo.com/guide/webdav.html#software-that-can-be-used-to-mount-webdav)
  1. **Windows**
     * [Potplayer](https://potplayer.daum.net/), [kmplayer](https://www.kmplayer.com/home), RaiDrive, [kodi](https://kodi.tv/download), [OneCommander](https://www.onecommander.com/), [Mountain Duck](https://mountainduck.io/), [netdrive](https://www.netdrive.net/)❌, [rclone](https://rclone.org/), [AIMP](https://www.aimp.ru/)
  2. **Android**
     * [Nplayer](https://www.aliyundrive.com/s/cf3p39UXkxa), [kmplayer](https://www.kmplayer.com/home), ES File Manager, [kodi](https://kodi.tv/download), [nova nova magic change](https://www.aliyundrive.com/s/cf3p39UXkxa/folder/63e8dcc229204583fff34f8cbd53dfcd6a86f526), [reex](https://www.aliyundrive.com/s/cf3p39UXkxa/folder/63e8e0027b7473f82cc64bbb9be0a34794c32c07), cx File Manager, Solid Explorer, [X-plore File Manager](https://www.lonelycatgames.com/apps/xplore), [MiXplorer](https://mixplorer.com/)
  3. **IOS**
     * [VidHub](https://okaapps.com/product/1659622164), Nplayer, [kmplayer](https://www.kmplayer.com/home), infuse, zFuse, Fileball File Manager
  4. **电视TV**
     * [VidHub](https://okaapps.com/product/1659622164), [Nplayer](https://www.aliyundrive.com/s/cf3p39UXkxa), [kodi](https://kodi.tv/download), [nova nova magic change](https://www.aliyundrive.com/s/cf3p39UXkxa/folder/63e8dcc229204583fff34f8cbd53dfcd6a86f526)
     * If you only look at Ali, you can use Ali's official cooperation 
       * Huanshi store-Alibaba cloud disk TV version, online disk player-Alibaba cloud disk TV version
  5. **Mac**
     * [VidHub](https://okaapps.com/product/1659622164), IINA, [Mountain Duck](https://mountainduck.io/), infuse, [netdrive](https://www.netdrive.net/), [rclone](https://rclone.org/)
  6. **Linux**
     * davfs2, [rclone](https://rclone.org/)
  7. **Notes**


If there is a suitable addition, please add~
### [**WebDav fill-in example**](https://alistgo.com/guide/webdav.html#webdav-fill-in-example)
Give a few examples of filling in **`WebDav`**, the account password is the account password of your AList user
This is basically the way of writing, and the way of writing may be different for different software. If there is no separate path option, it is normal to add the `/dav` option after the site
The different buttons at the top below can be clicked to view
NplayerreexESInfuseFileballPotplayernas
Nplayer
Infuse
Fileball
Potplayer
Please check the reminder content carefully1.The new version v3.25.0 has updated the new password method, and the acquisition method has also been changed. For details, please refer to the documentation page of your own installation method2.v3.25.1 Aliyun_open can choose to mount the backup disk or resource library by itself, for details [Click to view for details](https://alistgo.com/guide/drivers/aliyundrive_open.html#drive-type)3.The new version of AList version greater than v3.22.1 adds single sign-on to automatically register as an AList account, click to view the [detailed description](https://alistgo.com/guide/advanced/sso.html#sso-automatically-registers-as-an-alist-account)4.[139Cloud](https://alistgo.com/guide/drivers/139.html)and[189Cloud](https://alistgo.com/guide/drivers/189.html)For details of changes, please view the document by yourself, respectively5.v3.20.1version Breaking Changes [View detailed description](https://github.com/alist-org/alist/discussions/4702), go to [Configure documentation page](https://alistgo.com/config/configuration.html#scheme)6. AList v3.30.0 will no longer support Win7/Server2008 because Go does not support it. [Click to view detailed instructions](https://github.com/golang/go/issues/64622) .7.After adding the cloud disk, please configure [anti-theft/meta information] and other measures in time to prevent the account from being [frozen/disabled] due to malicious [access/sharing] by [crawlers/others].
您的首选语言是 zh-CN，是否切换到该语言？
Your primary language is zh-CN, do you want to switch to it?
记住我的选择 / Remember my choice
切换到 zh-CN / Switch to zh-CN取消 / Cancel
