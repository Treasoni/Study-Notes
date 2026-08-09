# 共享资料库：镜像加速器配置（2026-08-08 核实）

> 适用笔记：`docker/镜像加速器vs代理-概念对比.md`、`docker/Windows-DockerDesktop安装指南-国内网络版.md`

## 资料 1：Docker Desktop 不读取宿主机的 `~/.docker/daemon.json`

- **日期**：2026-08-08 核实
- **来源**：[docker/for-mac#2537](https://github.com/docker/for-mac/issues/2537)、[Docker daemon 配置文档](https://docs.docker.com/engine/daemon/)
- **摘要**：Docker Desktop（Mac/Windows）的 dockerd 运行在内置 Linux VM（HyperKit/VZ/WSL2）中，宿主机的 `~/.docker/daemon.json` 或 `/etc/docker/daemon.json` **不会被 daemon 读取**。`~/.docker/` 是 Docker CLI 配置目录（存放 `config.json`）。官方支持的唯一配置入口是 GUI `Settings → Docker Engine → Apply & Restart`（新版底层文件在 `~/Library/Group Containers/group.com.docker/settings*.json` 或 `%USERPROFILE%\AppData\Roaming\Docker\settings-store.json`，**不要手改**）。命令行写 `daemon.json` 仅适用于 Linux 原生 dockerd（`/etc/docker/daemon.json` + `systemctl restart docker`）。
- **适用**：两篇笔记的「命令行配置」章节全部需按此修正

## 资料 2：2026 年国内 Docker 镜像源可用性实测

- **日期**：2026-08-08 用户网络 curl 实测
- **来源**：[dongyubin/DockerHub（2026-08 更新）](https://github.com/dongyubin/DockerHub)、[2026 年 5 月国内可用 Docker 镜像源列表](https://nanhubrain.csdn.net/6a3cf7d210ee7a33f2825e57.html)
- **摘要**：
  - 实测方法：`curl -s -o /dev/null -w "%{http_code}" -m 10 https://<镜像>/v2/`，401/200 = 可用，000/超时 = 不可用，403 = 受限
  - ✅ 可用：`docker.1ms.run`(401)、`docker.m.daocloud.io`(401)、`docker.xuanyuan.me`(401)、`docker.jiaxin.site`(401)、`dockerproxy.net`(200)、`dockerproxy.link`(200)
  - ❌ 已失效：`docker.mirrors.ustc.edu.cn`（000 超时）、`docker.mirrors.sjtug.sjtu.edu.cn`（000 超时）、`docker.nju.edu.cn`（403 受限）
  - ⚠️ 有争议：`docker.1panel.live`（403，GitHub 列表标注「仅限中国地区」）
- **适用**：两篇笔记的镜像源列表、JSON 示例、状态表

## 资料 3：registry-mirrors 边界

- **日期**：2026-08-08
- **来源**：[Docker Engine daemon](https://docs.docker.com/engine/daemon/)、[docker/for-mac#2537](https://github.com/docker/for-mac/issues/2537)
- **摘要**：`registry-mirrors` 只加速 Docker Hub（`docker.io`）；显式 `docker pull docker.io/xxx` 会绕过镜像源；`ghcr.io`、`gcr.io`、`mcr.microsoft.com` 等不经过镜像源。
- **适用**：可作为「常见误区」补充进两篇笔记

## 推荐统一镜像源配置（patch 用）

```json
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.m.daocloud.io",
    "https://docker.xuanyuan.me"
  ]
}
```
