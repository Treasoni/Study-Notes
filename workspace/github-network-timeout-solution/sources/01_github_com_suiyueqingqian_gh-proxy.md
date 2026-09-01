---
url: "https://github.com/suiyueqingqian/gh-proxy"
title: "GitHub - suiyueqingqian/gh-proxy: github release、archive以及项目文件的加速项目 · GitHub"
scraped_at: 2026-08-29T08:28:09+00:00
---

[Skip to content](https://github.com/suiyueqingqian/gh-proxy#start-of-content)
You signed in with another tab or window. [Reload](https://github.com/suiyueqingqian/gh-proxy) to refresh your session. You signed out in another tab or window. [Reload](https://github.com/suiyueqingqian/gh-proxy) to refresh your session. You switched accounts on another tab or window. [Reload](https://github.com/suiyueqingqian/gh-proxy) to refresh your session. Dismiss alert
/ Public
forked from [hunshcn/gh-proxy](https://github.com/hunshcn/gh-proxy)
  * [ Notifications ](https://github.com/login?return_to=%2Fsuiyueqingqian%2Fgh-proxy) You must be signed in to change notification settings
  * [ Fork 0 ](https://github.com/login?return_to=%2Fsuiyueqingqian%2Fgh-proxy)
  * [ Star  0 ](https://github.com/login?return_to=%2Fsuiyueqingqian%2Fgh-proxy)


Go to file
Open more actions menu
## Latest commit
## History
[76 Commits](https://github.com/suiyueqingqian/gh-proxy/commits/master/)
76 Commits
## Folders and files  
| Name  | Name  | Last commit message  | Last commit date  |  
| --- | --- | --- | --- |  
 |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
|   |   |  
| View all files |  
## Repository files navigation
# gh-proxy
github release、archive以及项目文件的加速项目，支持clone，有Cloudflare Workers无服务器版本以及Python版本
<https://gh.api.99988866.xyz/>
演示站为公共服务，如有大规模使用需求请自行部署，演示站有点不堪重负
当然也欢迎[捐赠](https://github.com/suiyueqingqian/gh-proxy#%E6%8D%90%E8%B5%A0)以支持作者
## python版本和cf worker版本差异
  * python版本支持进行文件大小限制，超过设定返回原地址 [issue #8](https://github.com/hunshcn/gh-proxy/issues/8)
  * python版本支持特定user/repo 封禁/白名单 以及passby [issue #41](https://github.com/hunshcn/gh-proxy/issues/41)


直接在copy出来的url前加`https://gh.api.99988866.xyz/`即可
也可以直接访问，在input输入
_**大量使用请自行部署，以上域名仅为演示使用。**_
访问私有仓库可以通过
`git clone https://user:TOKEN@ghproxy.com/https://github.com/xxxx/xxxx` [#71](https://github.com/hunshcn/gh-proxy/issues/71)
以下都是合法输入（仅示例，文件不存在）：
  * 分支源码：<https://github.com/hunshcn/project/archive/master.zip>
  * release源码：<https://github.com/hunshcn/project/archive/v0.1.0.tar.gz>
  * release文件：<https://github.com/hunshcn/project/releases/download/v0.1.0/example.zip>
  * 分支文件：<https://github.com/hunshcn/project/blob/master/filename>
  * commit文件：<https://github.com/hunshcn/project/blob/1111111111111111111111111111/filename>
  * gist：<https://gist.githubusercontent.com/cielpy/351557e6e465c12986419ac5a4dd2568/raw/cmd.py>


## cf worker版本部署
首页：<https://workers.cloudflare.com>
注册，登陆，`Start building`，取一个子域名，`Create a Worker`。
复制 [index.js](https://cdn.jsdelivr.net/gh/hunshcn/gh-proxy@master/index.js) 到左侧代码框，`Save and deploy`。如果正常，右侧应显示首页。
`ASSET_URL`是静态资源的url（实际上就是现在显示出来的那个输入框单页面）
`PREFIX`是前缀，默认（根路径情况为"/"），如果自定义路由为example.com/gh/*，请将PREFIX改为 '/gh/'，注意，少一个杠都会错！
## Python版本部署
### Docker部署

```
docker run -d --name="gh-proxy-py" \
  -p 0.0.0.0:80:80 \
  --restart=always \
  hunsh/gh-proxy-py:latest

```

第一个80是你要暴露出去的端口
安装依赖（请使用python3）
`pip install flask requests`
按需求修改`app/main.py`的前几项配置
_注意:_ 可能需要在`return Response`前加两行

```
if 'Transfer-Encoding' in headers:
    headers.pop('Transfer-Encoding')
```

python版本的机器如果无法正常访问github.io会启动报错，请自行修改静态文件url
python版本默认走服务器（2021.3.27更新）
## Cloudflare Workers计费
到 `overview` 页面可参看使用情况。免费版每天有 10 万次免费请求，并且有每分钟1000次请求的限制。
如果不够用，可升级到 $5 的高级版本，每月可用 1000 万次请求（超出部分 $0.5/百万次请求）。
## Changelog
  * 2020.04.10 增加对`raw.githubusercontent.com`文件的支持
  * 2020.04.09 增加Python版本（使用Flask）
  * 2020.03.23 新增了clone的支持
  * 2020.03.22 初始版本


## About
github release、archive以及项目文件的加速项目
### Resources
### Stars
**0** stars
### Watchers
**0** watching
### Forks
[ forks](https://github.com/suiyueqingqian/gh-proxy/forks)
## Releases
## Packages
## Contributors
## Languages
You can’t perform that action at this time. 
