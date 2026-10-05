---
url: "https://alist-doc.nn.ci/docs/driver/base/"
title: "基本配置 | Alist Document"
scraped_at: 2026-10-05T12:03:33+00:00
---

[Skip to main content](https://alist-doc.nn.ci/docs/driver/base/)
New version available: [AList V3](https://alist.nn.ci)
On this page
所有账号的通用项
### 虚拟路径[​](https://alist-doc.nn.ci/docs/driver/base/#%E8%99%9A%E6%8B%9F%E8%B7%AF%E5%BE%84 "Direct link to heading")
必填，唯一标识符，即你要挂载到的位置，如果你要挂载到根目录，即为`/`
### index（索引）[​](https://alist-doc.nn.ci/docs/driver/base/#index%E7%B4%A2%E5%BC%95 "Direct link to heading")
当有多个账号时，用于排序，越小越靠前
### proxy（代理相关）[​](https://alist-doc.nn.ci/docs/driver/base/#proxy%E4%BB%A3%E7%90%86%E7%9B%B8%E5%85%B3 "Direct link to heading")
一个有三个相关选项：
  * proxy：网页端和直链走不走中转
  * webdav_proxy：webdav文件下载走不走中转
  * webdav_direct：webdav是否直接由本机中转


如果没有proxy和webdav_proxy选项，则说明只能走中转
> 存储分可以直接请求（有proxy开关）和不可以直接请求的（无proxy开关） 不可以直接请求的会直接走程序所在服务器（如果你没有填down_proxy_url） 可以直接请求的：
>   * proxy关、webdav_proxy关：文件下载请求完全不走服务器
>   * proxy开、webdav_proxy关：网页上的预览、直链下载都走服务器，但webdav下载不走服务器
>   * proxy关、webdav_proxy开：网页上的预览、直链下载不走服务器，但webdav下载走服务器
>   * proxy开、webdav_proxy开：网页预览、直链下载和webdav下载都走服务器。
>   * webdav_direct: 如果打开此开关，则webdav文件直接由本机中转，且不经过302跳转。如果此项关闭且打开webdav_proxy，webdav客户端在get文件时可能会经过多次302跳转。因为部分客户端可能不支持302跳转get文件，所以打开此开关可能会提示部分客户端的兼容性。
> 

### down_proxy_url（下载代理地址）[​](https://alist-doc.nn.ci/docs/driver/base/#down_proxy_url%E4%B8%8B%E8%BD%BD%E4%BB%A3%E7%90%86%E5%9C%B0%E5%9D%80 "Direct link to heading")
不填此字段开启代理时，默认使用本机进行中转。提供两种代理方法：
#### cloudflare workers[​](https://alist-doc.nn.ci/docs/driver/base/#cloudflare-workers "Direct link to heading")
可以使用`cloudflare workers`进行代理，此处填写`cloudflare workers`地址即可。 workers代码可以在<https://github.com/alist-org/alist-proxy/blob/main/alist-proxy.js> 找到。其中：
  * HOST: 你的Alist地址，必须添加协议头，且后面不能添加/。如`https://alist.nn.ci`；
  * TOKEN：参见[Alist](https://alist-doc.nn.ci/docs/driver/alist#token)部分的Token。


#### 通用二进制[​](https://alist-doc.nn.ci/docs/driver/base/#%E9%80%9A%E7%94%A8%E4%BA%8C%E8%BF%9B%E5%88%B6 "Direct link to heading")
你也可以使用另外一台机器进行代理，在<https://github.com/alist-org/alist-proxy/releases> 下载程序
`./alist-proxy -help`查看使用方法。
你也可以自己开发代理程序，一般的步骤为：
  * 下载时会请求`PROXY_URL/path?sign=sign_value`
  * 在代理程序中验证sign，sign的计算方式为:



```
const name = path.split('/').pop();const sign =md5(`alist-${TOKEN}-${name}`).slice(8,24)
```
Copy
  * 验证sign无误后，请求`HOST/api/admin/link`，可以得到文件的URL与需要携带的请求头
  * 使用得到的信息请求并返回


### api_proxy_url（API代理地址）[​](https://alist-doc.nn.ci/docs/driver/base/#api_proxy_urlapi%E4%BB%A3%E7%90%86%E5%9C%B0%E5%9D%80 "Direct link to heading")
同down_proxy_url，请求API使用的代理，专门为GoogleDrive和PikPak等国内无法直接访问的存储准备。
### extract_folder[​](https://alist-doc.nn.ci/docs/driver/base/#extract_folder "Direct link to heading")
  * front: 排序时将文件夹全部放到最前面
  * back: 排序时将文件夹全部放到最后面




