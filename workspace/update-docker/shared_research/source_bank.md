# 共享资料来源库

> 阶段：P3 共享资料收集
> 运行标识：update-docker
> 生成时间：2026-08-03
> 验证日期：2026-08-03（来源标注「2026 可用」的镜像站以实际拉取测试为准）

## 适用主题映射

| 主题 | 适用笔记 |
|------|---------|
| T1 版本现状 | mirror-config, windows-install, network |
| T2 国内镜像源 | mirror-config, windows-install, compare |
| T3 代理配置 | proxy, compare, windows-install |
| T4 WSL2 现状 | windows-install |

---

## T1 — Docker Engine / Docker Desktop 2026 版本现状

### S1. Docker Engine 29 release notes（官方）
- **URL**: https://docs.docker.com/engine/release-notes/29/
- **日期**: 2026-07（持续更新）
- **摘要**: Docker Engine 29 为 2026 当前稳定大版本（2025-11-10 发布首版），最新补丁 **29.6.2**（2026-07-16）。新增 BuildKit 改进、容器网络 IPv6 与 DNS 解析增强、更严格默认 seccomp、镜像层去重、CLI 增强。**Docker Engine 28 已于 2026-05-13 EOL**。

### S2. Docker Desktop release notes（官方）
- **URL**: https://docs.docker.com/desktop/release-notes/
- **日期**: 2026-07-20
- **摘要**: 最新 **Docker Desktop 4.83.0**（2026-07-20），内置 **Docker Engine v29.6.2、Docker Compose v5.3.1**。Windows 安装器默认改为 per-user 安装；4.80.0 移除 Mac 旧 osxfs 文件共享（迁移到 VirtioFS）；4.78.0 为 WSL2 后端新增 Synchronized file shares。版本滚动发布，官方站更新后约一周内可用。

### S3. Docker Engine 支持周期（社区汇总）
- **URL**: https://endoflife.date/docker-engine
- **日期**: 2026-08
- **摘要**: Docker Engine 生命周期：29.x 为当前维护线，28.x 已 EOL（2026-05-13）。确认笔记引用版本应至少为 29.x。

---

## T2 — 国内镜像加速器 2026 现状

### S4. 国内 Docker Hub 镜像站集体下线的背景
- **URL**: https://cloud.tencent.com/developer/article/2566168（及 huaweicloud/blogs/460516）
- **日期**: 2025-2026
- **摘要**: **2024-06-06 起**国内 Docker Hub 镜像加速器大面积关停：阿里云、腾讯云、中科大(USTC)、清华、网易、南大(NJU)、SJTU 等相继停服/转内部/不再同步。**原笔记中 `docker.mirrors.ustc.edu.cn`、`docker.nju.edu.cn`、SJTU 源均已失效**，必须替换。

### S5. 2025-2026 社区测试仍可用的镜像源
- **URL**: https://cloud.tencent.cn/developer/article/2644586 （2025.3 教程）；zachthinking.github.io（2026-03 教程）
- **日期**: 2025-03 ~ 2026-03
- **摘要**: 社区实测可用清单（个人/社区维护，**不保证长期有效**，建议配置多个）：
  - `https://docker.m.daocloud.io`（DaoCloud，白名单模式）
  - `https://docker.1ms.run`（毫秒镜像）
  - `https://docker.xuanyuan.me`（轩辕镜像）
  - `https://hub.rat.dev`（耗子面板）
  - `https://docker.1panel.live` / `https://docker.hlmirror.com` / `https://docker-0.unsee.tech` / `https://docker.imgdb.de` 等
  - 注意：这些源大多只支持 `docker pull`，不支持 `docker search`。
  - 个人可用**阿里云 ACR 个人免费版**配置自己的加速地址 `https://<your-id>.mirror.aliyuncs.com`。

### S6. registry-mirrors 配置机制仍受支持（官方 + 2026 教程）
- **URL**: https://docs.docker.com/engine/reference/commandline/dockerd/ ；zachthinking.github.io/posts/docker-desktop-mirror/（2026-03）
- **日期**: 2026
- **摘要**: **`registry-mirrors` 在 daemon.json 中仍受 Docker Engine 支持，未移除**。Docker Desktop 通过 **Settings → Docker Engine** 编辑 daemon.json 的 `registry-mirrors` 数组。仅 `dockerd --registry-mirror` **命令行 flag 自 17.06 起已弃用**，勿混用。配置不生效常见原因：JSON 语法错、未完全重启 Docker Desktop、镜像源已死、使用 `docker.io/xxx` 全限定名绕过镜像。

### S7. 替代方案（镜像源之外）
- **URL**: https://developer.baidu.com/article/detail.html?id=5126714 ；https://github.com/ox01024/cmirror
- **日期**: 2025-2026
- **摘要**: ① **配置 daemon 代理**（更稳定，推荐，见 T3）；② 自建镜像代理/缓存服务；③ 私有仓库 Harbor / Nexus；④ 云厂商容器镜像服务（阿里云 ACR / 腾讯 TCR / 华为 SWR）；⑤ 一键换源工具 **Cmirror**（`sudo cmirror use docker --fastest`）。

---

## T3 — Docker 代理 2026 现状

### S8. Docker Desktop 忽略 daemon.json 代理设置（官方）
- **URL**: https://docs.docker.com/engine/daemon/proxy/
- **日期**: 2026（持续更新）
- **摘要**: **Docker Desktop 忽略 daemon.json 中的代理配置**。Mac/Windows 必须用 **Settings → Resources → Proxies** 开启 Manual proxy configuration，填 HTTP/HTTPS/SOCKS5 与 no-proxy 列表，Apply & Restart。该设置影响 `docker pull` 与 `docker build` 拉取阶段，并自动传播代理环境变量到容器。**原笔记中「Docker Desktop 改 daemon.json/CLI 代理」的做法需修正。**

### S9. Linux daemon 代理（非 Desktop）
- **URL**: https://docs.docker.com/engine/daemon/proxy/ ；https://github.com/antgroup/Agent3Sigma-Canary/blob/master/docs/docker_proxy_en.md
- **日期**: 2026
- **摘要**: 推荐 **systemd drop-in** `/etc/systemd/system/docker.service.d/http-proxy.conf` 设 `HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY`，`daemon-reload` + `restart docker`；或 daemon.json `"proxies"` 块（http-proxy/https-proxy/no-proxy）。只影响 `docker pull/build`，不影响容器内。与原笔记 `docker进行代理.md` 的 daemon 代理方法一致，无需大改。

### S10. 容器/构建代理
- **URL**: https://docs.docker.com/engine/daemon/proxy/ ；go2proxy.com/blog/article/2026012920776
- **日期**: 2026
- **摘要**: 容器内代理用 `~/.docker/config.json` 的 `proxies.default`（httpProxy/httpsProxy/noProxy），`docker run`/`docker compose` 构建时自动注入。验证：`docker info | grep -i proxy` 或进容器 `env | grep -i proxy`。

---

## T4 — WSL2 2026 现状

### S11. WSL 安装与更新（官方）
- **URL**: https://learn.microsoft.com/windows/wsl/install
- **日期**: 2026
- **摘要**: 现代 Windows（10 1903+/11）最简单：管理员 PowerShell 运行 `wsl --install`（自动装 WSL2、启用组件、装默认 Ubuntu）。更新用 `wsl --update`，检查用 `wsl --version`。**Microsoft Store 版 WSL 为默认推荐**，更新更快，内置 WSLg（GUI）。原笔记的手动 DISM 启用流程仍有效但已非首选。

### S12. WSL 版本与常见错误（社区）
- **URL**: https://www.cnblogs.com/Ayeking/p/19617997 ；https://www.digitalcitizen.life/how-to-manually-update-wsl-on-windows-11-command-prompt-method/
- **日期**: 2026-01
- **摘要**: 2026 年初 WSL 版本约 **2.6.3**（Windows 11 25H2），以 `wsl --version` 实际输出为准。常见错误：**0x80370114**（未启用虚拟机平台/BIOS 虚拟化）；内核下载超时可手动装 `wsl_update_x64.msi`；0x80070422（LxssManager 服务未启动）。Docker Desktop 4.83 修复了 WSL 2.6.x 集成下 0 字节代理二进制导致的 Permission denied / Exec format error。

---

## 可信度标注

| 级别 | 条目 |
|------|------|
| ✅ 官方/一手 | S1, S2, S6, S8, S9, S10, S11 |
| 🟡 社区汇总（较可信） | S3, S4, S5, S7, S12 |
| ⚠️ 时效波动 | S5 镜像源清单（须实测） |

## 结论要点（供 note-updater 直接引用）

1. 版本基线：**Docker Engine 29.x（当前 29.6.2）/ Docker Desktop 4.83 / Compose v5.x**；28 已 EOL。
2. 镜像源：**原笔记 USTC/NJU/SJTU 源全部失效**；2026 可用以 DaoCloud `docker.m.daocloud.io`、`docker.1ms.run` 等社区源 + 个人阿里云 ACR 为主；registry-mirrors 机制仍有效（Docker Desktop 在 Settings→Docker Engine 配置）。
3. 代理：**Docker Desktop 必须用 Settings→Resources→Proxies**，daemon.json 代理对它无效；Linux daemon 用 systemd drop-in；容器内用 `~/.docker/config.json`。
4. WSL：`wsl --install` + `wsl --update`，Store 版默认推荐，版本以 `wsl --version` 为准。
