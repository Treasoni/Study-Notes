---
url: "https://docs.deeptutor.info/zh-cn/get-started/docker/"
title: "Docker | DeepTutor"
scraped_at: 2026-09-01T15:15:32+00:00
---

[跳转到内容](https://docs.deeptutor.info/zh-cn/get-started/docker/#_top)
# Docker
一个容器跑完整 Web 应用。镜像在 GitHub Container Registry 上：
  * `ghcr.io/hkuds/deeptutor:latest` —— 当前稳定版
  * `ghcr.io/hkuds/deeptutor:<version>` —— 精确版本；预发布只发版本 tag，不更新 `latest`


## 运行
[Section titled “运行”](https://docs.deeptutor.info/zh-cn/get-started/docker/#%E8%BF%90%E8%A1%8C)
Terminal window
```


dockerrun--rm--namedeeptutor\




-p127.0.0.1:3782:3782\




-vdeeptutor-data:/app/data\




ghcr.io/hkuds/deeptutor:latest


```

> **只需要映射`3782` 。** 浏览器只跟前端 origin 通信；容器里的 Next.js 中间件（`web/proxy.ts`）会把每个 `/api/*` 和 `/ws/*` 请求**在容器内部** 转发给 FastAPI 后端，所以为了让 UI 正常工作，你不需要把 `8001` 暴露到宿主机。映射它（`-p 127.0.0.1:8001:8001`）是可选的 —— 只在你想用 curl 或脚本直接调 API 时才有用。
打开 <http://127.0.0.1:3782>。容器首次启动时会创建 `/app/data/user/settings/*.json`；从 Web 的设置页面里配置模型 provider。配置、API key、日志、工作区文件、记忆、知识库、Partner 工作区（`data/partners/<id>/`）全部持久化在 `deeptutor-data` volume 里。可选依赖声明在部署上，别钻进容器里装：设好 `DEEPTUTOR_EXTRAS`（系统库用 `DEEPTUTOR_APT_PACKAGES`），每个容器启动时自动补齐。
## 后台模式
[Section titled “后台模式”](https://docs.deeptutor.info/zh-cn/get-started/docker/#%E5%90%8E%E5%8F%B0%E6%A8%A1%E5%BC%8F)
加 `-d` 让它在后台跑：
Terminal window
```


dockerrun-d--namedeeptutor\




-p127.0.0.1:3782:3782\




-vdeeptutor-data:/app/data\




ghcr.io/hkuds/deeptutor:latest





dockerlogs-fdeeptutor# 跟踪日志




dockerstopdeeptutor# 停止




dockerrmdeeptutor# 删除（volume 仍保留）


```

`deeptutor-data` volume 会在 `stop` / `rm` 之间保留设置和工作区。如果真要从头来：`docker volume rm deeptutor-data`。
## 远程 Docker / 反向代理
[Section titled “远程 Docker / 反向代理”](https://docs.deeptutor.info/zh-cn/get-started/docker/#%E8%BF%9C%E7%A8%8B-docker--%E5%8F%8D%E5%90%91%E4%BB%A3%E7%90%86)
浏览器始终只跟前端 origin（`:3782`）通信；容器里的 Next.js 中间件会在服务端把 `/api/*` 和 `/ws/*` 转发给 `localhost:8001` 上的后端。所以常见的**单容器** 场景下，你完全**不需要** 配置任何 API base —— 把反向代理 / TLS 终止器指向发布出来的 `:3782` 即可：

```

deeptutor.example.com {



reverse_proxy localhost:3782



```

只有**拆分部署** （后端跑在另一个容器或主机上）才需要设置 API base。在挂载 volume 里的 `data/user/settings/system.json` 中，把它设成**前端服务器** 用来访问后端的内网地址 —— 这个值由代理在服务端读取，不会发给浏览器：

```



"next_public_api_base": "http://backend:8001"



```

`next_public_api_base_external`（及其别名 `public_api_base`）作为更低优先级的回退被接受，保存时会归一化。
CORS 只在开启 auth 且前端跨 origin 时才有意义：`cors_origins` 列出哪些前端页面 origin 可以调用后端。未开启 auth 时，DeepTutor 默认允许正常 HTTP/HTTPS 浏览器 origin。

```



"cors_origins": ["https://deeptutor.example.com"]



```

## 改宿主机端口
[Section titled “改宿主机端口”](https://docs.deeptutor.info/zh-cn/get-started/docker/#%E6%94%B9%E5%AE%BF%E4%B8%BB%E6%9C%BA%E7%AB%AF%E5%8F%A3)
改 `-p host:container` 映射的左边即可：
Terminal window
```


dockerrun--rm--namedeeptutor\




-p127.0.0.1:8088:3782\




-vdeeptutor-data:/app/data\




ghcr.io/hkuds/deeptutor:latest


```

如果还想把 API 暴露到宿主机，再加 `-p 127.0.0.1:8089:8001`。如果你在 `/app/data/user/settings/system.json` 里改了容器侧端口，重启并把每条映射右侧同步改掉。
## 连本地 LLM（Ollama / LM Studio / llama.cpp / vLLM）
[Section titled “连本地 LLM（Ollama / LM Studio / llama.cpp / vLLM）”](https://docs.deeptutor.info/zh-cn/get-started/docker/#%E8%BF%9E%E6%9C%AC%E5%9C%B0-llmollama--lm-studio--llamacpp--vllm)
Docker 里的 `localhost` 指的是容器本身，不是宿主机。要访问宿主机上跑的模型服务，用 host gateway：
Terminal window
```


dockerrun--rm--namedeeptutor\




-p127.0.0.1:3782:3782\




--add-host=host.docker.internal:host-gateway\




-vdeeptutor-data:/app/data\




ghcr.io/hkuds/deeptutor:latest


```

然后在 **设置 → LLM** （或 **Embedding** ）里，把 provider Base URL 指到 `host.docker.internal`：  
| 服务  | Base URL  |  
| --- | --- |  
| Ollama LLM  | `http://host.docker.internal:11434/v1`  |  
| Ollama embedding  | `http://host.docker.internal:11434/api/embed`  |  
| LM Studio  | `http://host.docker.internal:1234/v1`  |  
| llama.cpp  | `http://host.docker.internal:8080/v1`  |  
Docker Desktop（macOS / Windows）通常**不需要** `--add-host` 就能解析 `host.docker.internal`。Linux 上，这个 flag 是在现代 Docker Engine 上创建这个 hostname 的可移植方式。
### Linux 替代方案 —— host networking
[Section titled “Linux 替代方案 —— host networking”](https://docs.deeptutor.info/zh-cn/get-started/docker/#linux-%E6%9B%BF%E4%BB%A3%E6%96%B9%E6%A1%88--host-networking)
加 `--network=host`，去掉 `-p` flags：
Terminal window
```


dockerrun--rm--namedeeptutor\




--network=host\




-vdeeptutor-data:/app/data\




ghcr.io/hkuds/deeptutor:latest


```

容器直接共享宿主机网络，所以打开 <http://127.0.0.1:3782>（或 `system.json` 里的 `frontend_port`），宿主机服务也能用普通的 localhost URL 访问，比如 `http://127.0.0.1:11434/v1`。
> Host networking 把容器端口直接暴露在宿主机上，可能跟已有服务冲突。
## 升级
[Section titled “升级”](https://docs.deeptutor.info/zh-cn/get-started/docker/#%E5%8D%87%E7%BA%A7)
Terminal window
```


dockerpullghcr.io/hkuds/deeptutor:latest




dockerrm-fdeeptutor2>/dev/null




dockerrun--rm--namedeeptutor\




-p127.0.0.1:3782:3782\




-vdeeptutor-data:/app/data\




ghcr.io/hkuds/deeptutor:latest


```

volume 会保留 —— 你的设置、KB、记忆都能撑过升级。
**设置 → 关于** 会识别 Docker 镜像并检查是否有新版本，但替换容器仍属于部署操作：按上面的步骤拉取新镜像并重建容器。DeepTutor 不会在运行中的容器里原地升级包。
## 常见错误
[Section titled “常见错误”](https://docs.deeptutor.info/zh-cn/get-started/docker/#%E5%B8%B8%E8%A7%81%E9%94%99%E8%AF%AF)
### `Bind for 0.0.0.0:3782 failed: port is already allocated`
[Section titled “Bind for 0.0.0.0:3782 failed: port is already allocated”](https://docs.deeptutor.info/zh-cn/get-started/docker/#bind-for-00003782-failed-port-is-already-allocated)
Terminal window
```


lsof-i:3782# macOS




ss-ltnp|grep:3782# Linux


```

干掉冲突进程，或者在 `-p` 映射里换一个宿主机端口。
### 容器立刻退出
[Section titled “容器立刻退出”](https://docs.deeptutor.info/zh-cn/get-started/docker/#%E5%AE%B9%E5%99%A8%E7%AB%8B%E5%88%BB%E9%80%80%E5%87%BA)
Terminal window
```


dockerlogsdeeptutor|tail-30


```

无效的 LLM 凭据会被捕获并记为 warning，**不会** 让后端启动失败。如果容器已经退出，请从日志中寻找其他致命错误。Web UI 可用后，到 **设置 → Models** 修正凭据即可。
### 前端能加载但 API 调用失败（拆分部署）
[Section titled “前端能加载但 API 调用失败（拆分部署）”](https://docs.deeptutor.info/zh-cn/get-started/docker/#%E5%89%8D%E7%AB%AF%E8%83%BD%E5%8A%A0%E8%BD%BD%E4%BD%86-api-%E8%B0%83%E7%94%A8%E5%A4%B1%E8%B4%A5%E6%8B%86%E5%88%86%E9%83%A8%E7%BD%B2)
用单容器镜像时不该出现这种情况 —— 容器内的代理会自动把 `/api/*` 转发给后端。如果你跑的是**拆分部署** （后端在另一个容器或主机上），在 volume 里的 `data/user/settings/system.json` 把 `next_public_api_base` 设成前端服务器访问后端用的内网地址，然后重启。
### Docker 里的多用户模式
[Section titled “Docker 里的多用户模式”](https://docs.deeptutor.info/zh-cn/get-started/docker/#docker-%E9%87%8C%E7%9A%84%E5%A4%9A%E7%94%A8%E6%88%B7%E6%A8%A1%E5%BC%8F)
直接在 volume 的 `data/user/settings/auth.json` 里把 auth 开关打开（`"enabled": true`），然后重启。容器会自动 pick up。完整配置见 [**多用户部署**](https://docs.deeptutor.info/zh-cn/get-started/multi-user/)。
更多：[**故障排查**](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/)。
## 下一步
[Section titled “下一步”](https://docs.deeptutor.info/zh-cn/get-started/docker/#%E4%B8%8B%E4%B8%80%E6%AD%A5)
  * [**多用户部署**](https://docs.deeptutor.info/zh-cn/get-started/multi-user/) —— 团队配置
  * [**探索 DeepTutor**](https://docs.deeptutor.info/zh-cn/explore/) —— 看看跑起来的应用


