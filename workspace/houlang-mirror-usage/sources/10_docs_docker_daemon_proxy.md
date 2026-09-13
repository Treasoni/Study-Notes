---
url: "https://docs.docker.com/engine/daemon/proxy/"
title: "Daemon proxy configuration | Docker Docs"
scraped_at: 2026-09-14
tier: "一手（Docker 官方文档）"
note: "用于支撑第 1 章 §1.2 三类机制对照表中「HTTP/HTTPS 代理」一行的能力边界（缺口：该行原无一手来源）"
---

# Daemon proxy configuration（Docker 官方）

> 抓取说明：`docs.docker.com` 在本机网络下不稳定（曾出现 `curl: (35) Connection was reset` 与 HTTP 301 空响应），需 `curl -sSL --http1.1` 并重试。本页首次尝试返回 301/0B，重试后 HTTP 200 / 557213 B。

## 关键原文（逐字）

**能力边界——代理覆盖「Docker Hub 及其他 registry」**（与 `registry-mirrors` 仅限 Hub 形成对照）：

> If your organization uses a proxy server to connect to the internet, you may need to configure the Docker daemon to use the proxy server. The daemon uses a proxy server to access images stored on Docker Hub **and other registries**, and to reach other nodes in a Docker swarm. This page describes how to configure a proxy for the Docker daemon.

**配置位置——守护进程启动环境变量**：

> The Docker daemon checks the following environment variables in its start-up environment to configure HTTP or HTTPS proxy behavior:
> `HTTP_PROXY` `http_proxy` `HTTPS_PROXY` `https_proxy` `NO_PROXY` `no_proxy`

**systemd 场景的落地方式**（drop-in 文件）：

> Create a systemd drop-in directory for the docker service:
> `$ sudo mkdir -p /etc/systemd/system/docker.service.d`
> Create a file named `/etc/systemd/system/docker.service.d/http-proxy.conf` that adds the `HTTP_PROXY` environment variable:
> ```
> [Service]
> Environment="HTTP_PROXY=http://proxy.example.com:3128"
> ```
> To proxy HTTPS requests, set the `HTTPS_PROXY` environment variable.

**例外排除**：

> If you have internal Docker registries that you need to contact without proxying, you can specify them via the `NO_PROXY` environment variable.

## 对本笔记的作用

| 用途 | 结论 |
| --- | --- |
| 支撑 §1.2 表格「代理」行 | 配置位置 = 守护进程环境变量 / systemd drop-in（**非** `daemon.json`）；覆盖范围 = **Docker Hub 及其他 registry**（原文 "and other registries"） |
| 与 `registry-mirrors` 的对照 | `registry-mirrors` 仅 Hub（C1），代理则覆盖多上游——这正是 §1.2 表格里两类分野的官方依据 |
| 与「前缀重写」的对照 | 代理需要改环境变量/unit 文件（**配置一次**），前缀重写不改任何配置、但**每处地址要手改** |

## 未覆盖

- 本页**没有**说明代理是否对 HTTPS 做 TLS 中间人、也不讨论凭据可见性。因此 §1.2 表格「你的凭据流向」一列对代理写的「**取决于代理是否做 TLS 中间人**」仍是**通用机制推断**，不是本页原文。
- Docker Desktop 场景下的代理设置入口不在本页描述范围内。
