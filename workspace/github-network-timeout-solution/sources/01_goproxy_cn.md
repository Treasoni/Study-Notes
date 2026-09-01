---
url: "https://goproxy.cn/"
title: "Goproxy.cn"
scraped_at: 2026-08-29T08:28:01+00:00
---

# Goproxy.cn
The most trusted Go module proxy in China.
52,681,404 module versions cached
[Star](https://github.com/goproxy/goproxy.cn)
###  Blazing Fast
We are using [Qiniu Cloud CDN](https://www.qiniu.com/en/products/qcdn) to accelerate our service globally without placing any bandwidth limits. With thousands of CDN nodes and **100Gbps+ single-node bandwidth** , you will be given the ability to download module versions at a blazing fast speed.
###  No Limit
We do not just place no bandwidth limits. Furthermore, we **have not placed any rate limits**. This means that you can use our service in any scenario, like CI/CD. You can even use our service as an upstream proxy, just like [goproxy.baidu.com](https://goproxy.baidu.com) does.
###  Full Featured
We are always using the latest Go version, even the unstable version. Because we provide **cutting-edge feature support**. In particular, we support [proxying](https://golang.org/design/25530-sumdb#proxying-a-checksum-database) the default checksum database [sum.golang.org](https://sum.golang.org). You don't need to do anything extra, it just works.
###  Data Visualized
For everyone to better understand the activity of all modules in our service, we have launched the very first [Statistics API](https://goproxy.cn/stats) of the Go module proxy world. With the decent RESTful API design, you will be able to easily query statistics for all module versions in our service.
[Go 1.13 and above (RECOMMENDED)](https://goproxy.cn/#usage-go-113-and-above-recommended)
Open your terminal and execute

```
$ go env -w GO111MODULE=on
$ go env -w GOPROXY=https://goproxy.cn,direct
```

done.
[macOS or Linux](https://goproxy.cn/#usage-macos-or-linux)
Open your terminal and execute

```
$ export GO111MODULE=on
$ export GOPROXY=https://goproxy.cn
```

or

```
$ echo "export GO111MODULE=on" >> ~/.profile
$ echo "export GOPROXY=https://goproxy.cn" >> ~/.profile
$ source ~/.profile
```

done.
Open your terminal and execute

```
C:\> $env:GO111MODULE = "on"
C:\> $env:GOPROXY = "https://goproxy.cn"
```

or

```
1. Open the Start Search, type in "env"
2. Choose the "Edit the system environment variables"
3. Click the "Environment Variables…" button
4. Under the "User variables for <YOUR_USERNAME>" section (the upper half)
5. Click the "New..." button
6. Choose the "Variable name" input bar, type in "GO111MODULE"
7. Choose the "Variable value" input bar, type in "on"
8. Click the "OK" button
9. Click the "New..." button
10. Choose the "Variable name" input bar, type in "GOPROXY"
11. Choose the "Variable value" input bar, type in "https://goproxy.cn"
12. Click the "OK" button
```

done.
### [Self-hosted Go module proxy](https://goproxy.cn/#self-hosted-go-module-proxy)
Your code is always yours, so we provide you with the coolest self-hosted Go module proxy building solution in the world. By using [Goproxy](https://github.com/goproxy/goproxy), a minimalist project, you can easily add Go module proxy support to any existing web service, you know that Goproxy.cn is built on it.
Create a file named `goproxy.go`

```
package main

import (
	"net/http"
	"os"

	"github.com/goproxy/goproxy"
)

func main() {
	http.ListenAndServe("localhost:8080", &goproxy.Goproxy{
		GoBinEnv: append(
			os.Environ(),
			"GOPROXY=https://goproxy.cn,direct", // Use Goproxy.cn as the upstream proxy
			"GOPRIVATE=git.example.com",         // Solve the problem of pulling private modules
		),
		ProxiedSUMDBs: []string{
			"sum.golang.org https://goproxy.cn/sumdb/sum.golang.org", // Proxy the default checksum database
		},
	})
}
```

and run it

```
$ go run goproxy.go
```

then try it by setting `GOPROXY` to `http://localhost:8080`. In addition, we also recommend that you set `GO111MODULE` to `on`.
That's it, a fully functional Go module proxy is successfully built. In fact, you can use [Goproxy](https://github.com/goproxy/goproxy) with your favorite web frameworks, such as [Gin](https://pkg.go.dev/github.com/gin-gonic/gin#WrapH) and [Echo](https://pkg.go.dev/github.com/labstack/echo/v4#WrapHandler), all you need to do is add one more route. For more advanced usage please check the [documentation](https://pkg.go.dev/github.com/goproxy/goproxy).
