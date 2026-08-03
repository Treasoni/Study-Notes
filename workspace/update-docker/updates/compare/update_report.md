# update_report — 镜像加速器vs代理-概念对比.md

> 运行标识：update-docker
> 笔记：docker/镜像加速器vs代理-概念对比.md
> 生成时间：2026-08-04
> 输出：workspace/update-docker/updates/compare/updated_note.md

## 变更摘要

| 类别 | 数量 | 说明 |
|------|------|------|
| keep | 8 处 | 核心区别表、作用范围图、功能对比表、决策流程图、典型场景推荐、误区 1/3、一张图总结 |
| update | 6 处 | 概述 callout、3.3 配置方式对比（镜像/daemon/容器）、6.1/6.2/6.3 速查表、参考资料 |
| add | 4 处 | 2.1 镜像源现状 warning、3.3/6.3 容器代理 config.json 方案、误区 2 例外说明、文末更新记录 |
| delete | 1 处 | 失效镜像源 `docker.mirrors.ustc.edu.cn`（6.1 列表） |

## 关键修正（用户需知）

- **镜像源现状**：2024-06 起国内公共 Docker Hub 镜像站大面积关停（USTC/NJU/SJTU/阿里云/腾讯云）。原 6.1 速查表中的 `docker.mirrors.ustc.edu.cn` 已失效并删除；当前以社区源 `docker.m.daocloud.io`、`docker.1ms.run`、`docker.xuanyuan.me` 为主，均只支持 `docker pull` 不支持 `docker search`；个人可用阿里云 ACR 免费版配置专属加速地址 `https://<your-id>.mirror.aliyuncs.com`。
- **Docker Desktop 代理配置修正**：Docker Desktop（Windows / macOS）**忽略 daemon.json 里的代理设置**，原笔记 3.3 / 6.2 的 systemd 方法只适用于非 Desktop Linux daemon。Docker Desktop 用户必须用 **Settings → Resources → Proxies → Manual proxy configuration**（HTTP/HTTPS/SOCKS5 + no-proxy），并 Apply & Restart。
- **容器代理补充**：除 compose 环境变量外，`~/.docker/config.json` 的 `proxies.default` 可在构建/运行容器时自动注入代理。
- **误区 2 例外澄清**：Docker Desktop 的 Settings → Resources → Proxies 配置会自动把代理传播给容器；误区 2 的「daemon 代理不影响容器内」针对的是 daemon.json / systemd 方式，两者不矛盾。

## 使用到的资料来源（共享来源库）

- **S1**（官方）Docker Engine 29 release notes（当前 29.6.2）：https://docs.docker.com/engine/release-notes/29/
- **S2**（官方）Docker Desktop 4.83 release notes：https://docs.docker.com/desktop/release-notes/
- **S4**（社区）国内 Docker Hub 镜像站 2024-06 起大面积关停：https://cloud.tencent.com/developer/article/2566168
- **S5**（社区）2025-2026 社区可用镜像源清单：https://cloud.tencent.cn/developer/article/2644586
- **S6**（官方）registry-mirrors 机制仍受支持：https://docs.docker.com/engine/reference/commandline/dockerd/
- **S8**（官方）Docker Desktop 忽略 daemon.json 代理：https://docs.docker.com/engine/daemon/proxy/
- **S9**（官方）Linux daemon systemd drop-in 代理：https://docs.docker.com/engine/daemon/proxy/
- **S10**（官方）~/.docker/config.json proxies.default：https://docs.docker.com/engine/daemon/proxy/

来源库文件：`workspace/update-docker/shared_research/source_bank.md`（阶段 P3，2026-08-03）。

## 未解决问题与风险

1. **社区镜像源时效波动**：S5 清单中的社区源（daoCloud 白名单模式等）不保证长期有效，须实际拉取测试；建议用户配置多个源并定期验证。来源库标注「2026 可用」的镜像站以实际拉取测试为准。
2. **未做真机验证**：本次为资料驱动的局部更新，未实际运行 Docker Desktop / Linux daemon 验证代理生效；UI 界面文案可能因版本略有差异（入口 Settings → Resources → Proxies 稳定）。
3. **原文 ASCII 图乱码修复**：2.1 原理图中一处箭头字符在原文件中已损坏（显示为 �），本次清理为 ASCII 箭头；不影响语义。
4. **source_project 取值**：批内其余笔记分别用过 `Study-Notes` 与 `study-notes`，本笔记采用 `study-notes`；如需统一，建议 P5 汇总时对齐。
5. **未改动 Obsidian vault 原文件**：按 project-output-only 模式，输出到 `updates/compare/`，原文 `docker/镜像加速器vs代理-概念对比.md` 未动；如需发布到 vault，请在 P5 汇总时确认位置。
