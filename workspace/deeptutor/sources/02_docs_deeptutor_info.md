---
url: "https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/"
title: "故障排查 | DeepTutor"
scraped_at: 2026-09-01T15:15:32+00:00
---

[跳转到内容](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#_top)
如果你的安装行为不太对劲，先跑一次 `deeptutor doctor` 看缺了什么。然后在下面找到对应的症状。错误按类别分组。
## 端口与进程
[Section titled “端口与进程”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E7%AB%AF%E5%8F%A3%E4%B8%8E%E8%BF%9B%E7%A8%8B)
###  `Address already in use :3782`（或 :8001）
[Section titled “Address already in use :3782（或 :8001）”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#address-already-in-use-3782%E6%88%96-8001)
有别的东西绑定到这个端口了。找出来：
Terminal window
```

# macOS



lsof-i:3782




# Linux



ss-ltnp|grep:3782




# Windows PowerShell



Get-NetTCPConnection-LocalPort3782


```

干掉它，或者通过重跑 setup 向导或编辑 `data/user/settings/system.json` 改 DeepTutor 端口：
Terminal window
```


deeptutorinit


```


```



"backend_port": 18001,




"frontend_port": 4000



```

如果只是一次性进程级覆盖，启动 DeepTutor 之前在 shell 里 export 环境变量即可：`BACKEND_PORT=18001 FRONTEND_PORT=4000 deeptutor start`。
如果在用 Docker，改 docker 专用的端口变量：
Terminal window
```


DEEPTUTOR_DOCKER_FRONTEND_PORT=4000




DEEPTUTOR_DOCKER_BACKEND_PORT=18001


```

### 后端起来了但前端连不上
[Section titled “后端起来了但前端连不上”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E5%90%8E%E7%AB%AF%E8%B5%B7%E6%9D%A5%E4%BA%86%E4%BD%86%E5%89%8D%E7%AB%AF%E8%BF%9E%E4%B8%8D%E4%B8%8A)
前端会在服务端把 `/api/*` 和 `/ws/*` 转发给后端，所以当你以另一个 hostname 提供服务时（云部署、局域网访问、反向代理），浏览器只用前端 origin 即可 —— 把客户端和反向代理都指向前端端口就行，不需要配置任何 API base。
只有**拆分部署** （后端和前端分开跑）才需要显式设置 API base。打开 **设置 - > Network**，或把 `data/user/settings/system.json` 里的 `next_public_api_base` 设成前端服务器访问后端用的内网地址，然后重启：

```



"next_public_api_base": "http://backend:8001"



```

`next_public_api_base_external`（及其别名 `public_api_base`）作为更低优先级的回退被接受。
如果 auth 已开启且前端 origin 与 API origin 不同，也要设置精确 CORS origins：

```



"cors_origins": ["https://deeptutor.example.com"]



```

## LLM / Embedding providers
[Section titled “LLM / Embedding providers”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#llm--embedding-providers)
### provider probe 时报 `HTTPError 401 Unauthorized`
[Section titled “provider probe 时报 HTTPError 401 Unauthorized”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#provider-probe-%E6%97%B6%E6%8A%A5-httperror-401-unauthorized)
provider 拒绝了你的 API key。常见坑：
  * **OpenAI** ：以 `sk-` 开头（project key 以 `sk-proj-` 开头）
  * **Anthropic** ：以 `sk-ant-` 开头
  * **Azure OpenAI** ：在 设置 → Models → LLM 的当前 profile 中填写 **API Version**
  * **Google Gemini** ：以 `AIza` 开头
  * **Ollama / 本地 OpenAI 兼容** ：API key 留空或用 `none`，base URL 设成像 `http://localhost:11434/v1`


重跑 `deeptutor init` 重新输入 key，或者直接编辑 `data/user/settings/model_catalog.json`。
### 配置时 `Failed to fetch /models`
[Section titled “配置时 Failed to fetch /models”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E9%85%8D%E7%BD%AE%E6%97%B6-failed-to-fetch-models)
DeepTutor 会 ping provider 的 model-list 端点来填充模型下拉框。如果你的网络把它挡了，会出现这个警告 —— 这是**非致命** 的。向导会 fallback 到一份硬编码的常见模型列表然后继续。
###  `host.docker.internal` 解析不了（Docker + 本地 Ollama）
[Section titled “host.docker.internal 解析不了（Docker + 本地 Ollama）”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#hostdockerinternal-%E8%A7%A3%E6%9E%90%E4%B8%8D%E4%BA%86docker--%E6%9C%AC%E5%9C%B0-ollama)  
| 宿主系统  | 用  |  
| --- | --- |  
| macOS、Windows  | `http://host.docker.internal:11434/v1`  |  
| Linux  |  `http://172.17.0.1:11434/v1` _（docker0 网桥）_ 或宿主机的 LAN IP  |  
Linux 用户也可以手动加 `host.docker.internal`：
docker-compose.ghcr.yml
```


services:




deeptutor:




extra_hosts:




- "host.docker.internal:host-gateway"


```

### 查询 KB 时报 `Embedding dimension mismatch`
[Section titled “查询 KB 时报 Embedding dimension mismatch”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E6%9F%A5%E8%AF%A2-kb-%E6%97%B6%E6%8A%A5-embedding-dimension-mismatch)
你用不同的 embedding 模型重建了 KB。缓存里的维度对不上了。
修复：在 Web UI 里，**Knowledge → 选 KB → Index versions → Re-index now** 。重建索引没有暴露成 CLI 命令。
### Embedding endpoint URL 老是出错
[Section titled “Embedding endpoint URL 老是出错”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#embedding-endpoint-url-%E8%80%81%E6%98%AF%E5%87%BA%E9%94%99)
Embedding adapter 会原样使用 profile 的 **Base URL** ，因此请在 设置 → Models → Embedding 中填写完整 endpoint，而不是只填 API root：  
| Provider  | 错误  | 正确  |  
| --- | --- | --- |  
| OpenAI  | `https://api.openai.com/v1`  | `https://api.openai.com/v1/embeddings`  |  
| Cohere  | `https://api.cohere.com`  | `https://api.cohere.com/v2/embed`  |  
| Jina  | `https://api.jina.ai/v1`  | `https://api.jina.ai/v1/embeddings`  |  
## 知识库
[Section titled “知识库”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E7%9F%A5%E8%AF%86%E5%BA%93)
### KB 卡在 `indexing` 状态
[Section titled “KB 卡在 indexing 状态”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#kb-%E5%8D%A1%E5%9C%A8-indexing-%E7%8A%B6%E6%80%81)
索引是后台任务跑的。看日志：
Terminal window
```


tail-fdata/user/logs/deeptutor.jsonl|grep-ikb


```

常见原因：embedding provider 返回 429（限流 —— 用更小的 batch 重试）、embedding host 不可达（检查网络）、或者 PDF parser 失败（确认文件没有密码保护）。
### 重建索引修不了维度不匹配
[Section titled “重建索引修不了维度不匹配”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E9%87%8D%E5%BB%BA%E7%B4%A2%E5%BC%95%E4%BF%AE%E4%B8%8D%E4%BA%86%E7%BB%B4%E5%BA%A6%E4%B8%8D%E5%8C%B9%E9%85%8D)
如果重建索引之后维度不匹配仍然存在，KB store 里可能有过期的配置文件。从 CLI：
Terminal window
```


deeptutorkbdeletephysics--force




deeptutorkbcreatephysics--docchapter1.pdf


```

## 多用户
[Section titled “多用户”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E5%A4%9A%E7%94%A8%E6%88%B7)
### 重启之后每个 API 调用都报 `401 Unauthorized`
[Section titled “重启之后每个 API 调用都报 401 Unauthorized”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E9%87%8D%E5%90%AF%E4%B9%8B%E5%90%8E%E6%AF%8F%E4%B8%AA-api-%E8%B0%83%E7%94%A8%E9%83%BD%E6%8A%A5-401-unauthorized)
`data/system/auth/auth_secret` 丢失或被重新生成了，所有 JWT 都失效了。
修复：从备份恢复 `data/system/auth/auth_secret`，或接受新的 secret 并让所有用户重新登录。项目根目录 `.env` 不会被运行时自动加载。
### 第一个用户没被提升为 admin
[Section titled “第一个用户没被提升为 admin”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E7%AC%AC%E4%B8%80%E4%B8%AA%E7%94%A8%E6%88%B7%E6%B2%A1%E8%A2%AB%E6%8F%90%E5%8D%87%E4%B8%BA-admin)
编辑 `data/system/auth/users.json`，把那个用户的 `"role": "admin"` 设好，然后重启。
### 登录成功但又跳回 `/login`
[Section titled “登录成功但又跳回 /login”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E7%99%BB%E5%BD%95%E6%88%90%E5%8A%9F%E4%BD%86%E5%8F%88%E8%B7%B3%E5%9B%9E-login)
auth cookie 没被设置上，通常因为：
  1. `auth.json: cookie_secure=false` 但你是跨站 HTTPS 部署 —— 设成 `true` 后重启，让 cookie 使用 `SameSite=None; Secure`
  2. 本地 HTTP 测试时误设了 `cookie_secure=true` —— 改回 `false`
  3. 浏览器拦了第三方 cookie，而你在子域上 —— 把前端和 API 部署在同一个 hostname 下（比如都在 `deeptutor.example.com`，前端在 `/`，API 通过 `/api/` 代理）


## Docker
[Section titled “Docker”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#docker)
### 容器立刻退出
[Section titled “容器立刻退出”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E5%AE%B9%E5%99%A8%E7%AB%8B%E5%88%BB%E9%80%80%E5%87%BA)
Terminal window
```


dockerlogsdeeptutor|tail-30


```

源码树 Compose 部署应保留 `./data:/app/data` bind mount；重试 wrapper 前先检查宿主机路径权限：
Terminal window
```


mkdir-pdata




pythonscripts/docker_compose.pyup-d


```

### 容器是 `Running` 但是 `unhealthy`
[Section titled “容器是 Running 但是 unhealthy”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E5%AE%B9%E5%99%A8%E6%98%AF-running-%E4%BD%86%E6%98%AF-unhealthy)
健康检查会从容器内探测后端，并设置了 60 秒 start period。如果启动更久，容器可能变成 `unhealthy`。
如果状态一直不恢复，直接运行镜像内置的 healthcheck，并查看容器日志：
Terminal window
```


dockerexecdeeptutorpython/app/healthcheck.py




dockerlogsdeeptutor|tail-40


```

### 构建时 npm install 超时
[Section titled “构建时 npm install 超时”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E6%9E%84%E5%BB%BA%E6%97%B6-npm-install-%E8%B6%85%E6%97%B6)
Next.js 依赖树很大。调大 npm 的网络超时：
Terminal window
```


npmconfigsetfetch-timeout600000


```

官方 `Dockerfile` 已经设了 —— 只在本地构建时才需要管。
## Python 安装
[Section titled “Python 安装”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#python-%E5%AE%89%E8%A3%85)
###  `Microsoft Visual C++ 14.0 is required`（Windows）
[Section titled “Microsoft Visual C++ 14.0 is required（Windows）”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#microsoft-visual-c-140-is-requiredwindows)
某个依赖回退到了 Windows 源码构建。安装 [**Build Tools for Visual Studio**](https://visualstudio.microsoft.com/visual-cpp-build-tools/)，勾选 “Desktop development with C++” workload，然后重试安装。
###  `libolm not found`（仅 Matrix E2EE 需要）
[Section titled “libolm not found（仅 Matrix E2EE 需要）”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#libolm-not-found%E4%BB%85-matrix-e2ee-%E9%9C%80%E8%A6%81)
Terminal window
```

# macOS



brewinstalllibolm




# Debian / Ubuntu



sudoaptinstalllibolm-dev




# 重装 matrix-e2e extra



pipinstall-e".[matrix-e2e]"--force-reinstall


```

###  `pip install` 慢到爆
[Section titled “pip install 慢到爆”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#pip-install-%E6%85%A2%E5%88%B0%E7%88%86)
网络慢的话，用本地 PyPI 镜像或 wheelhouse。中国大陆用户：
Terminal window
```


pipconfigsetglobal.index-urlhttps://pypi.tuna.tsinghua.edu.cn/simple


```

### Conda 环境已激活但 `python` 仍然指向别处
[Section titled “Conda 环境已激活但 python 仍然指向别处”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#conda-%E7%8E%AF%E5%A2%83%E5%B7%B2%E6%BF%80%E6%B4%BB%E4%BD%86-python-%E4%BB%8D%E7%84%B6%E6%8C%87%E5%90%91%E5%88%AB%E5%A4%84)
PATH 顺序可能盖住了 conda 的 python。验证：
/Users/you/miniconda3/envs/deeptutor/bin/python
```


whichpython


```

如果不是，在一个新 shell 里跑 `conda activate deeptutor`。
## 前端
[Section titled “前端”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E5%89%8D%E7%AB%AF)
### 前端显示空白页
[Section titled “前端显示空白页”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E5%89%8D%E7%AB%AF%E6%98%BE%E7%A4%BA%E7%A9%BA%E7%99%BD%E9%A1%B5)
打开浏览器开发者工具（⌥⌘I），看 Console 标签页。常见原因：
  * **CORS errors** —— 前端一个 origin，后端另一个 origin，而后端没把这个前端 origin 加进允许列表。编辑 `data/user/settings/system.json`，把你的前端 origin 加进 `cors_origins`。
  * **`/_next/...`404** —— 静态 bundle 没构建。从源码起的话：`cd web && npm run build`。
  * **后端连不上** —— 验证 `curl http://localhost:8001/` 是否返回 JSON。


### 每个页面都弹 “Failed to fetch” toast
[Section titled “每个页面都弹 “Failed to fetch” toast”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E6%AF%8F%E4%B8%AA%E9%A1%B5%E9%9D%A2%E9%83%BD%E5%BC%B9-failed-to-fetch-toast)
跟上面一样 —— 通常是后端没起来或者 CORS / API base URL 对不上。看 Network 标签页确认请求实际去了哪个 URL。
## Partners 与 channels
[Section titled “Partners 与 channels”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#partners-%E4%B8%8E-channels)
### Partner channel 在 Channels 面板置灰 / 报 “missing SDK”
[Section titled “Partner channel 在 Channels 面板置灰 / 报 “missing SDK””](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#partner-channel-%E5%9C%A8-channels-%E9%9D%A2%E6%9D%BF%E7%BD%AE%E7%81%B0--%E6%8A%A5-missing-sdk)
某个 channel 的 SDK import 不进来时，Partners 的 **Channels** 面板会把该 channel 置灰并显示 import 错误（如 `No module named 'lark_oapi'`）；从 CLI 启动 partner 也会报同样的错。装上缺的依赖集，然后重启 DeepTutor：
Terminal window
```


pipinstall-e".[partners]"# 全部内置 channel SDK（源码安装）




pipinstall-U"deeptutor[partners]"# PyPI 安装用这条




pipinstall-e".[matrix]"# Matrix channel；加密房间用 ".[matrix-e2e]"（需要 libolm）


```

如果你用的是 `packaging/deeptutor-cli` 的纯 CLI 包（它没有定义任何 extras），改从源码 checkout 装 requirements 镜像：
Terminal window
```


python-mpipinstall-rrequirements/partners.txt


```

装好包、重启 server 之后该 channel 即恢复。
### Partner 连上了但不响应
[Section titled “Partner 连上了但不响应”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#partner-%E8%BF%9E%E4%B8%8A%E4%BA%86%E4%BD%86%E4%B8%8D%E5%93%8D%E5%BA%94)
检查 channel card 里的 `allow_from`：

```


weixin:




enabled: true




allow_from# 空 = 全部拒绝




- "*"# 允许所有人




# - "sender-id"          # 测试后换成具体 user/chat ids


```

默认 `allow_from: []` 拒绝所有人 —— 你必须显式 opt in。
### Channel 跑几分钟就掉线
[Section titled “Channel 跑几分钟就掉线”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#channel-%E8%B7%91%E5%87%A0%E5%88%86%E9%92%9F%E5%B0%B1%E6%8E%89%E7%BA%BF)
Long-poll / WebSocket 连接偶尔会掉。channel manager 会带退避自动重连，但如果你看到频繁掉线：
  * 检查宿主机和 gateway provider 之间的网络稳定性
  * WeChat 检查 `state_dir` 是否可写、是否持久化
  * Teams / webhook 类 channel 检查公网 callback URL 是否能到达配置的 host/port/path
  * Matrix 检查 homeserver 是否有过于激进的超时


针对每个 gateway 的调试方法见 [**Partners 伙伴与渠道**](https://docs.deeptutor.info/zh-cn/partners/) 和 [**渠道矩阵**](https://docs.deeptutor.info/zh-cn/partners/channels/)。
## 记忆 / RAG 精度
[Section titled “记忆 / RAG 精度”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E8%AE%B0%E5%BF%86--rag-%E7%B2%BE%E5%BA%A6)
### Chat 忽略了挂上的 KB
[Section titled “Chat 忽略了挂上的 KB”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#chat-%E5%BF%BD%E7%95%A5%E4%BA%86%E6%8C%82%E4%B8%8A%E7%9A%84-kb)
确认：
  1. KB **挂上了** 这一轮（不只是在选择器里出现 —— 真的点进了激活集）
  2. `rag` 工具由上下文控制，不会出现在 设置 → 工具；请挂载使用它的 KB（PageIndex 使用自己的工具）
  3. KB 是 `status: ready`（不是还在索引）—— 通过 `deeptutor kb list` 检查


###  `read_memory` 返回空
[Section titled “read_memory 返回空”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#read_memory-%E8%BF%94%E5%9B%9E%E7%A9%BA)
`read_memory` 会拼接四份 L3 文档：
  * `preferences` 由 `write_memory` 直接写入
  * `recent`、`profile`、`scope` 只在 Memory Workbench 中手动整合


没有每 N 轮自动整合。
在那里运行 **Update** ，或通过 API 提交必填的 layer、key、mode：
Terminal window
```


curl-XPOSThttp://localhost:8001/api/v1/memory/runs/start\




-H'Content-Type: application/json'\




-d'{"layer":"L3","key":"recent","mode":"update"}'


```

### Memory writes 被标成 `unsafe_text`
[Section titled “Memory writes 被标成 unsafe_text”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#memory-writes-%E8%A2%AB%E6%A0%87%E6%88%90-unsafe_text)
`write_memory` 接受 1 到 240 字符的偏好文本。这里没有 `unsafe_text` 结果或内容安全过滤；超过上限时缩短文本即可。
## 还卡着？
[Section titled “还卡着？”](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/#%E8%BF%98%E5%8D%A1%E7%9D%80)
  * 在 [Discord](https://discord.gg/eRsjPgMU4t) 上提问
  * 在 [github.com/HKUDS/DeepTutor/issues](https://github.com/HKUDS/DeepTutor/issues) 报 bug
  * 长篇问题？开一个 [Discussion](https://github.com/HKUDS/DeepTutor/discussions)


求助时请附上：
  * 你的安装路径（PyPI / 从源码 / Docker / 仅 CLI）
  * `deeptutor config show` 的输出
  * `data/user/logs/deeptutor.jsonl` 的最后 40 行
  * Docker 的话：`docker logs deeptutor | tail -40`


