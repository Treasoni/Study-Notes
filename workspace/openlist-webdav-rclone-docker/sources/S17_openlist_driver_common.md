---
url: "https://doc.oplist.org/guide/drivers/common"
title: "Common - OpenList Docs"
scraped_at: 2026-09-11T17:05:31+00:00
---

Menu
Return to top
# Common 
## Mount Path [​](https://doc.oplist.org/guide/drivers/common#mount-path)
## 挂载路径 [​](https://doc.oplist.org/guide/drivers/common#%E6%8C%82%E8%BD%BD%E8%B7%AF%E5%BE%84)
The unique identifier for the mount point, the name displayed externally, and the location where it should be mounted. If you want to mount it to the root directory, please enter `/`.
挂载项的唯一标识，对外展示的名称，要挂载到的位置。如果要挂载到根目录，请填写 `/`。
DANGER
You cannot use duplicate mount path names, otherwise, the following error will occur:
json
```
Failed to create storage in database: UNIQUE constraint failed: x_storages.mount_path
```

Solution: Use [aliases](https://doc.oplist.org/guide/drivers/alias) to aggregate multiple mount points.
DANGER
不能使用重复的挂载路径名称，否则会报错：
json
```
Failed create storage in database: UNIQUE constraint failed: x_storages.mount_path
```

解决方法：使用 [别名](https://doc.oplist.org/guide/drivers/alias) 对多个挂载项目进行聚合。
DANGER
The mount path name is a required field and cannot be left empty, or the following error will occur:
json
```
Key: 'Storage.MountPath' Error: Field validation for 'MountPath' failed on the 'required' tag
```

Solution: If you want to mount to the root directory, please enter `/`.
DANGER
挂载路径名称是必填项，不能为空，否则会报错：
json
```
Key: 'Storage.MountPath' Error:Field validation for 'MountPath' failed on the 'required' tag
```

解决方案：如果要挂载到根目录，请填写 `/`。
## Order [​](https://doc.oplist.org/guide/drivers/common#order)
## 序号 [​](https://doc.oplist.org/guide/drivers/common#%E5%BA%8F%E5%8F%B7)
When mounting multiple drives, this is used for sorting. The smaller the number, the further to the front. Negative numbers can also be used.
当挂载多个驱动时，用于排序。越小越靠前。可以填写负数。
## Remark [​](https://doc.oplist.org/guide/drivers/common#remark)
## 备注 [​](https://doc.oplist.org/guide/drivers/common#%E5%A4%87%E6%B3%A8)
You can add notes for easier management.
您可以添加备注，以方便管理。
### Reference [​](https://doc.oplist.org/guide/drivers/common#reference)
### 引用 [​](https://doc.oplist.org/guide/drivers/common#%E5%BC%95%E7%94%A8)
Reference authentication, tokens, etc., from the **"Mounted Storage"** to enable sharing the same token between multiple cloud drives.
Currently, the following cloud drives are supported:
  * 139Yun
  * AliyundriveOpen
  * 189CloudPC
  * 123PanShare（ref 123Pan）
  * Cloudreve V3 / V4


**How to use** : In the storage settings, set the first line of **Remark** to: **ref:/mount_path**
**Important** : `ref:/` should be in lowercase letters and symbols.
从 `已挂载的存储` 中引用认证、令牌等，实现同一个 Token 多个网盘使用。
目前支持如下网盘：
  * 中国移动云盘
  * 阿里云盘Open
  * 天翼云盘客户端
  * 123云盘分享（引用123云盘）
  * Cloudreve V3 / V4


**使用方法** ：在存储设置中将`备注(Remark)`的第一行设置为：**ref:/挂载路径**
**注意事项** ：`ref:/` 为小写英文和符号
## Enable signing [​](https://doc.oplist.org/guide/drivers/common#enable-signing)
## 启用签名 [​](https://doc.oplist.org/guide/drivers/common#%E5%90%AF%E7%94%A8%E7%AD%BE%E5%90%8D)
Sign and encrypt files (no password required), only valid for this driver, if other signatures are not enabled and `signature all` and `meta-information encryption` are not set, others will not be signed.
Usage scenario: I don’t want to enable all signatures, and I don’t want to set metadata encryption. I just want to sign and encrypt a certain driver to prevent it from being scanned.
Scope of influence: `Settings-->Global-->Signature All` > `Metainformation Directory Encryption` > `Single Driver Signature`.
对文件进行签名加密(不会需要密码)，仅对本驱动生效，如果别的没启用签名也没设置`签名全部`和`元信息加密`其他的不会进行签名。
使用场景：不想开启全部签名，也不想设置元信息加密，只想对某驱动进行签名加密防止被扫。
影响范围：`设置-->全局-->签名所有` > `元信息目录加密` > `单驱动签名`
## Disable index [​](https://doc.oplist.org/guide/drivers/common#disable-index)
## 禁用索引 [​](https://doc.oplist.org/guide/drivers/common#%E7%A6%81%E7%94%A8%E7%B4%A2%E5%BC%95)
Allow users to disable storage indexing.
  * For example, if you enable `Ignore Index` in the index options, you no longer need to configure it after enabling `Disable Index`, which is more convenient.


允许用户禁用存储索引。
  * 例如索引选项中的`忽略索引`，启用`禁用索引`后不需要再去配置了，这样也更方便一些


## Cache Expiration [​](https://doc.oplist.org/guide/drivers/common#cache-expiration)
## 缓存过期 [​](https://doc.oplist.org/guide/drivers/common#%E7%BC%93%E5%AD%98%E8%BF%87%E6%9C%9F)
Cache time of directory structure.
目录结构的缓存时间。
## Custom Cache Policies [​](https://doc.oplist.org/guide/drivers/common#custom-cache-policies)
## 自定义缓存策略 [​](https://doc.oplist.org/guide/drivers/common#%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BC%93%E5%AD%98%E7%AD%96%E7%95%A5)
Cache time for directory paths (in minutes).
You can customize the cache time for specific file paths using pattern matching. The configuration supports wildcard patterns:
  * `*` matches a **single** directory level.
  * `**` matches **multiple** directory levels.


Example configuration:
txt
```
/Series/Completed/*:60
/Series/Updating/*/**:10
/Series/Archived/**:30
```

Explanation:
  * `*` matches only a single directory level. Items directly under `/Series/Completed` will be cached for 60 minutes. This does **not** include deeper subdirectories — for example, `/Series/Completed/A/B` will not match this rule.
  * `**` matches multiple directory levels. Therefore, the contents of subdirectories under `/Series/Updating` will be cached for 10 minutes. For example, `/Series/Updating/A/B` and `/Series/Updating/C/D` will match.
  * The pattern `/Series/Updating/*/**` enforces a “single level followed by multi-level” match. As a result, directories directly under `/Series/Updating` will **not** be matched by this rule.
  * All contents under `/Series/Archived` (including any depth of subdirectories) will be cached for 30 minutes.


目录路径缓存时间（单位：分钟）。
可以通过模式匹配来自定义某些文件路径的缓存时间。配置支持通配符：
  * `*` 匹配单层目录。
  * `**` 匹配多层目录。


示例配置：
txt
```
/剧集/已完结/*:60
/剧集/更新中/*/**:10
/剧集/归档/**:30
```

说明：
  * `*` 仅匹配单层目录，因此 `/剧集/已完结` 下**直接** 包含的项将被缓存 60 分钟。由于是单层匹配，不包括更深层的子目录，例如 `/剧集/已完结/A/B` 将不会匹配该规则。
  * `**` 匹配多层目录，因此 `/剧集/更新中` 下级目录的内容会被缓存 10 分钟。例如 `/剧集/更新中/A/B` 和 `/剧集/更新中/C/D` 都会符合该规则。
  * 由于 `/剧集/更新中/*/**` 严格设置了模糊匹配单层目录，所以直属于 `/剧集/更新中` 下都目录将不会命中规则。
  * `/剧集/归档` 下的内容（包括任意层级的子目录）都会被缓存 30 分钟。


## Web proxy [​](https://doc.oplist.org/guide/drivers/common#web-proxy)
## Web 代理 [​](https://doc.oplist.org/guide/drivers/common#web-%E4%BB%A3%E7%90%86)
Whether the web preview,download and the direct link go through the transfer. If you open this, recommended you set [site_url](https://doc.oplist.org/configuration/configuration#site-url) so that OpenList can works fine.
网页预览、下载和直接链接是否通过中转。如果你打开此项，建议你设置[site_url](https://doc.oplist.org/configuration/configuration#site-url)，以帮助OpenList更好的工作。
TIP
  * **Web proxy Strategies:** It is a strategy when using the webpage. The default is a local agent. If you fill in the proxy URL and enable the web agent to use the proxy URL
  * **Webdav policy Strategies:** It is an option to use the webdav function
    * If there are 302 options default to 302, if there is no 302 option default to the local agent, if you want to use the agent URL, please fill in and manually switch to the proxy URL strategy


The two are different configurations.
TIP
  * **Web代理** ：是使用网页时候的策略，默认为本地代理，如果填写了代理URL并且启用了Web代理使用的是代理URL
  * **WebDAV策略** ：是在使用WebDAV功能时候的选项，
    * 如果有302选项默认为302，如果没有302选项默认为本地代理，如果要使用代理URL请填写并且手动切换到代理URL策略


两者是不同的配置。
## Webdav policy [​](https://doc.oplist.org/guide/drivers/common#webdav-policy)
## WebDAV 策略 [​](https://doc.oplist.org/guide/drivers/common#webdav-%E7%AD%96%E7%95%A5)
  * **302 redirect:** redirect to the real link
    * Although it does not consume traffic, it is not recommended to share and use it.
  * **use proxy URL:** redirect to proxy URL
    * It will consume the traffic of the agent URL
  * **native proxy:** return data directly through local transit(best compatibility)
    * The traffic of the construction of OpenList device will consume


  * **302 重定向** ：重定向到真实链接
    * 虽然不会消耗流量，但是不建议共享使用，有封禁账户的风险
  * **使用代理 URL** ：重定向到代理 URL
    * 会消耗搭建代理URL的流量
  * **本机代理** ：直接通过本地中转返回数据（最佳兼容性）
    * 会消耗搭建OpenList设备的流量


### Description of three modes [​](https://doc.oplist.org/guide/drivers/common#description-of-three-modes)
### 三种模式说明 [​](https://doc.oplist.org/guide/drivers/common#%E4%B8%89%E7%A7%8D%E6%A8%A1%E5%BC%8F%E8%AF%B4%E6%98%8E)
## Download proxy URL [​](https://doc.oplist.org/guide/drivers/common#download-proxy-url)
## 下载代理 URL [​](https://doc.oplist.org/guide/drivers/common#%E4%B8%8B%E8%BD%BD%E4%BB%A3%E7%90%86-url)
When the proxy is turned on without filling in this field, the local machine will be used for transfer by default.
开启代理时不填写此字段，默认使用本机进行传输。
### 1. Cloudflare Workers [​](https://doc.oplist.org/guide/drivers/common#_1-cloudflare-workers)
### 1. Cloudflare Workers [​](https://doc.oplist.org/guide/drivers/common#_1-cloudflare-workers-1)
Here’s the translation:
You can use Cloudflare Workers as a proxy. Simply fill in your Cloudflare Workers address here.
The code to set up Workers can be found at <https://github.com/OpenListTeam/OpenList-Proxy/blob/main/openlist-proxy.js>. When using it, you need to replace the following variables:
  * `ADDRESS`: Your OpenList address, which must include the protocol header and should not end with a `/`. For example, `https://pan.example.com`.
  * `TOKEN`: The [Token](https://doc.oplist.org/configuration/other#token) of the admin account, which can be found in the “Other Settings” section of the OpenList admin page.
  * `WORKER_ADDRESS`: Your Worker address, which is usually the same as the **Download Proxy URL**.
⚠️ Cloudflare Workers free CDN support is only compatible with **http80** and **https443** ports (whether domestic or international), as tested by group members.


When filling in the **Download Proxy URL** in the OpenList backend configuration, the link should not end with a `/`.
Detailed text tutorial: <https://anwen-anyi.github.io/index/11-durl.html>
可以使用 Cloudflare Workers 做代理，这里填写您的 Cloudflare Workers 地址即可。
搭建 Workers 代码可以在 <https://github.com/OpenListTeam/OpenList-Proxy/blob/main/openlist-proxy.js> 找到，实际使用时需要配置环境变量：
在 OpenList 后台挂载配置时 填写 **下载代理URL** 时候的 链接结尾 不可以带 `/`
更多内容请参考[OpenList Proxy](https://doc.oplist.org/ecosystem/official_proxy)
来自安稳的详细文字教程：<https://anwen-anyi.github.io/index/11-durl.html>
### 2. Universal Binary [​](https://doc.oplist.org/guide/drivers/common#_2-universal-binary)
### 2. 通用二进制 [​](https://doc.oplist.org/guide/drivers/common#_2-%E9%80%9A%E7%94%A8%E4%BA%8C%E8%BF%9B%E5%88%B6)
You can use another machine as a proxy. Download the program from <https://github.com/OpenListTeam/OpenList-Proxy/releases> and check the usage instructions with `./openlist-proxy -help`.
Detailed text tutorial: <https://anwen-anyi.github.io/index/11-durl.html>
您可以使用另一台机器进行代理，在 <https://github.com/OpenListTeam/OpenList-Proxy/releases> 下载程序并通过 `./openlist-proxy -help` 查看使用方法。
更多内容请参考[OpenList Proxy](https://doc.oplist.org/ecosystem/official_proxy)
来自安稳的详细文字教程：<https://anwen-anyi.github.io/index/11-durl.html>
### 3. Developing on your own [​](https://doc.oplist.org/guide/drivers/common#_3-developing-on-your-own)
### 3. 自行开发 [​](https://doc.oplist.org/guide/drivers/common#_3-%E8%87%AA%E8%A1%8C%E5%BC%80%E5%8F%91)
You can develop your own proxy program. The general steps are as follows:
  * When downloading, it will request `PROXY_URL/path?sign=sign_value`.
  * In the proxy program, validate the `sign`. The calculation method for `sign` is:


js
```
const to_sign = `${path}:${expireTimeStamp}`
const _sign = safeBase64(hmac_sha256(to_sign, TOKEN))
const sign = `${_sign}:${expireTimeStamp}`
```

`TOKEN` is the [Token](https://doc.oplist.org/configuration/other#token) of the administrator account, which can be obtained in the “Other Settings” section of the OpenList management page.
  * After validating the signature, request `HOST/api/fs/link` to obtain the file URL and the request headers to include.
  * Use the information to make the request and handle the response.


你可以开发自己的代理程序，一般步骤是：
  * 下载时会请求 `PROXY_URL/path?sign=sign_value`
  * 在代理程序中验证 `sign`，`sign` 的计算方法为：


js
```
const to_sign = `${path}:${expireTimeStamp}`
const _sign = safeBase64(hmac_sha256(to_sign, TOKEN))
const sign = `${_sign}:${expireTimeStamp}`
```

`TOKEN` 即管理员账户的 [Token](https://doc.oplist.org/configuration/other#token)，可在 OpenList 管理页面中进入“其他设置”得到。
  * 验证签名正确后，请求 `HOST/api/fs/link`，可以得到文件的 URL 和要携带的请求头
  * 使用信息请求和返回


## Sort related [​](https://doc.oplist.org/guide/drivers/common#sort-related)
## 排序相关 [​](https://doc.oplist.org/guide/drivers/common#%E6%8E%92%E5%BA%8F%E7%9B%B8%E5%85%B3)
  * **Sort by** : Sort by what
  * **Sort direction** : Whether the sort direction is ascending or descending


  * **排序方式** ：按什么排序
  * **排序方向** ：排序方向是升序还是降序


INFO
Some drives use their own sorting method, which may be different.
INFO
有些驱动器使用自己的排序方法，可能会有所不同。
## Extract folder [​](https://doc.oplist.org/guide/drivers/common#extract-folder)
## 提取文件夹 [​](https://doc.oplist.org/guide/drivers/common#%E6%8F%90%E5%8F%96%E6%96%87%E4%BB%B6%E5%A4%B9)
  * **Extract to front** : put all folders to the front when sorting
  * **Extract to back** : put all folders to the back when sorting


  * **提取到前面** ：排序时将所有文件夹放在前面
  * **提取到后面** ：排序时将所有文件夹放在后面


## Contributors
[Edit this page on GitHub](https://github.com/OpenListTeam/OpenList-Docs/edit/main/pages/guide/drivers/common.md)
Last updated: 
