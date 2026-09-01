---
url: "https://npmmirror.com/"
title: "npmmirror 镜像站"
scraped_at: 2026-08-29T08:28:07+00:00
---

# npmmirror 镜像站
🍻「NPM Mirror」站点前后端应用代码均已开源，欢迎共建。
  1. 前端应用: [cnpmweb](https://github.com/cnpm/cnpmweb)
  2. 服务端应用: [cnpmcore](https://github.com/cnpm/cnpmcore)


> 这是一个完整 [npmjs.com](https://www.npmjs.com) 镜像，你可以用此代替官方版本(只读)，我们将尽量与官方服务**实时同步** 。
### 使用说明
你可以使用我们定制的[cnpm](https://npmmirror.com/package/cnpm)命令行工具代替默认的 npm。cnpm 支持除了写相关操作外的所有命令，例如 install、info、view 等。
```
$ npm install -g cnpm --registry=https://registry.npmmirror.com
```
或者你直接通过添加 npm 参数 alias 一个新命令:
```
alias cnpm="npm --registry=https://registry.npmmirror.com \ --cache=$HOME/.npm/.cache/cnpm \ --disturl=https://npmmirror.com/mirrors/node \ --userconfig=$HOME/.cnpmrc"
```
当然，你也可以使用任意你心仪的命令行工具，只要配置 registry 即可
```
$ npm config set registry https://registry.npmmirror.com
```

### 安装模块

```
$ cnpm install [name]
```

### 同步模块

```
$ cnpm sync cnpmcore
```
当然, 你可以直接通过 web 方式来同步, 界面打开时会自动比对版本信息
```
$ open https://npmmirror.com/sync/cnpmcore
```



  1. 累计同步包数量：
  2. 累计同步版本数量：
  3. 近7日下载量：
  4. 最近同步时间：
  5. 最近同步的包： 


