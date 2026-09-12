---
url: "https://github.com/OpenListTeam/OpenList"
title: "OpenList 源码 — WebDAV 驱动（drivers/webdav, internal/driver, pkg/gowebdav）"
scraped_at: 2026-09-12T15:52:30+00:00
note: "代码片段逐字复制自 main 分支；片段外的解释文字为本笔记所加，非源码注释。"
---

# OpenList 源码（WebDAV 驱动相关）

**层级：T1 源码级**（不是文档，是代码本身）。本文件登记本次核对用到的位置，
用于支撑第 3 册 §3.6 的结论。

仓库：https://github.com/OpenListTeam/OpenList ，分支 `main`。

## 1. `drivers/webdav/meta.go` — 字段与默认值（逐字）

```go
package webdav

import (
	"github.com/OpenListTeam/OpenList/v4/internal/driver"
	"github.com/OpenListTeam/OpenList/v4/internal/op"
)

type Addition struct {
	Vendor   string `json:"vendor" type:"select" options:"sharepoint,other" default:"other"`
	Address  string `json:"address" required:"true"`
	Username string `json:"username" required:"true"`
	Password string `json:"password" required:"true"`
	driver.RootPath
	TlsInsecureSkipVerify bool `json:"tls_insecure_skip_verify" default:"false"`
}

var config = driver.Config{
	Name:        "WebDav",
	LocalSort:   true,
	DefaultRoot: "/",
	PreferProxy: true,
}

func init() {
	op.RegisterDriver(func() driver.Driver {
		return &WebDav{}
	})
}
```

要点：`Address` / `Username` / `Password` 三个都 `required:"true"`；
`TlsInsecureSkipVerify` 默认 `false`；`DefaultRoot: "/"` → 界面「根文件夹路径」默认值就是 `/`。

## 2. `internal/driver/item.go` — `root_folder_path` 的来历（逐字）

```go
type RootPath struct {
	RootFolderPath string `json:"root_folder_path"`
}

func (r RootPath) GetRootPath() string {
	return r.RootFolderPath
}
```

## 3. `drivers/webdav/util.go` — 地址被原样传入（逐字节选）

```go
func (d *WebDav) setClient() error {
	c := gowebdav.NewClient(d.Address, d.Username, d.Password)
	c.SetTransport(&http.Transport{
		Proxy:           http.ProxyFromEnvironment,
		TLSClientConfig: &tls.Config{InsecureSkipVerify: d.TlsInsecureSkipVerify},
	})
	...
}
```

`d.Address` **原样**作为 `uri` 传给 `gowebdav.NewClient`，中间没有任何补全逻辑。

## 4. `pkg/gowebdav/utils.go` + `client.go` — `FixSlash` 只补末尾斜杠（逐字）

```go
// FixSlash appends a trailing / to our string
func FixSlash(s string) string {
	if !strings.HasSuffix(s, "/") {
		s += "/"
	}
	return s
}
```

```go
func NewClient(uri, user, pw string) *Client {
	return &Client{FixSlash(uri), make(http.Header), nil, &http.Client{}, sync.Mutex{}, &NoAuth{user, pw}}
}
```

客户端对地址**只做补末尾 `/`**，**不会**补 `http://` / `https://`。
→ 「地址」必须自己写全协议头，否则会构造出无协议的 URL。
