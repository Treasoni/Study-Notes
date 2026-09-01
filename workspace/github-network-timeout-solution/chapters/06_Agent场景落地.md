# 第 6 章：Agent 场景落地 — 给拉包工具配好网络

前几章把 git、npm、docker 等工具的单点代理配置拆开了，本章把它们落到你的真实场景：一个 agent 进程从大陆网络拉取 GitHub 包时连接超时。结论先行——给 agent 配好「环境变量 + git 全局配置」双保险，再单独处理 Docker daemon，就能覆盖绝大多数拉包路径。

## 6.1 环境变量 + git 全局配置的组合

agent 本质上是「一个父进程 + 一串子进程」：它调用的 git、curl、npm、pip 都是它的子进程。Linux/macOS 的子进程会无条件继承父进程的环境变量，所以只要在启动 agent 的 shell（或 agent 的 systemd unit / 运行时配置）里导出代理变量，agent 内部所有工具就会自动读到。

```bash
# 假设本机代理客户端（Clash/v2ray 类）监听 127.0.0.1:7890，按实际端口修改
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
export NO_PROXY=localhost,127.0.0.1
```

两个关键细节：

- **`http_proxy` 只认小写**：libcurl 的环境变量语义里，`http_proxy` 必须是小写才生效，其余变量（如 `HTTPS_PROXY`、`ALL_PROXY`）大小写都认（S11）。所以上面统一用全小写是刻意为之。
- **git 有自己的配置层**：git 的 `http.proxy` 配置项优先于所有 `http_proxy`/`https_proxy`/`all_proxy` 环境变量（S3）。也就是说，即便某个子进程没能继承到环境变量，git 仍然会走代理——这就是「双保险」。

```bash
# git 全局配置，同时覆盖 http/https 两种 remote
git config --global http.proxy http://127.0.0.1:7890

# 验证：能打印出代理地址说明已生效
git config --global --get http.proxy
```

>[!tip] 大白话
>把环境变量想成「公司张贴的全局规定」，git 全局配置想成「单独给 git 发的一张工牌」。规定贴了，有的工具不抬头看；工牌发了，别的工具又不认。两个都做才是真正的双保险——agent 这个「总包」带着一串「分包」，只要有一个机制生效，拉包就不会裸奔。

遇到某次想临时绕过代理时，git 支持用空串禁用（S3）：

```bash
git -c http.proxy= git fetch
```

## 6.2 浏览器能开但 git 超时的排查

「浏览器能打开 GitHub，终端 git clone 却超时」是最高频的困惑。原因很简单：**浏览器默认读系统的代理设置，而 git/curl 只认环境变量或自身配置，不读系统代理**（S5）。所以浏览器「能开」并不代表命令行也走了代理。

排查三步走：

```bash
# 1. 先确认 git 是否已有代理：无输出 = 没配
git config --global --get http.proxy

# 2. 没有就显式补上
git config --global http.proxy http://127.0.0.1:7890
```

3. 再用第 1 章提过的追踪命令确认流量确实经过代理：`GIT_TRACE_CURL=1 git fetch`，输出里出现 `Connected to 127.0.0.1 (127.0.0.1) port 7890` 之类的行即为生效。

## 6.3 Docker build/pull 的代理配置

最容易踩的坑：agent 里 `export http_proxy=...` 之后 `docker pull` 仍然超时。因为 **Docker daemon 是独立的后台进程，不读 shell 的环境变量**（S7）——你在终端导出的变量只影响当前 shell 及它启动的子进程，影响不到 daemon。所以 docker 必须走自己的配置通道。

方式一：systemd drop-in（推荐，可验证）：

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d

sudo tee /etc/systemd/system/docker.service.d/http-proxy.conf > /dev/null <<'EOF'
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1"
EOF

sudo systemctl daemon-reload
sudo systemctl restart docker

# 验证：输出 Environment 三行即生效
systemctl show --property=Environment docker
```

方式二：`daemon.json` 的 `proxies` 块：

```json
{
  "proxies": {
    "http-proxy": "http://127.0.0.1:7890",
    "https-proxy": "http://127.0.0.1:7890",
    "no-proxy": "localhost,127.0.0.1"
  }
}
```

改完重启 daemon（`sudo systemctl restart docker`）。daemon 的代理配置会传递给它启动的容器，因此 `docker pull` 拉镜像和 `docker build` 拉基础镜像、执行 RUN 阶段的网络请求都覆盖在内。

>[!tip] 大白话
>把 docker daemon 想成「装修总包公司」，你在终端 export 的变量只是「对现场的临时工喊的话」，总包在后台按自己的图纸（配置文件）干活。要让总包走代理，得改图纸——改 systemd/daemon.json，而不是在工地上喊。

注意：Docker Desktop（macOS/Windows 图形版）会忽略 `daemon.json` 的代理配置，必须在它的设置面板里配（S7）。

## 本章小结

- Agent 的拉包网络由「环境变量 + git 全局配置」双保险覆盖：环境变量靠子进程继承生效，git 的 `http.proxy` 独立兜底。
- `http_proxy` 只认小写（libcurl 语义），`HTTPS_PROXY`/`NO_PROXY` 大小写均可；统一用全小写最省心。
- 浏览器能开但 git 超时 = git 没读系统代理，显式 `git config --global http.proxy` 即可。
- Docker daemon 不读 shell 环境变量，必须用 systemd drop-in 或 `daemon.json` 配置；Docker Desktop 还要走图形设置。
- 所有改动都用 `git config --get` / `systemctl show` 验证，做到可复制、可回溯。

下一章我们把所有方案收拢成一张「决策速查表」：遇到超时先查哪步、有代理和无代理各走哪条路，以及全流程的坑位清单。
