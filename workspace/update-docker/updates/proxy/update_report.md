# update_report — docker进行代理.md

> 运行标识：update-docker
> 笔记：docker/docker进行代理.md
> 生成时间：2026-08-03
> 输出：workspace/update-docker/updates/proxy/updated_note.md

## 变更摘要

| 类别 | 数量 | 说明 |
|------|------|------|
| keep | 4 节 | 第 1、2、3 节 + 4.1（HTTP/SOCKS 容器代理、鉴权、原理、compose 重建） |
| update | 1 节 | 4.2 daemon 代理：限定 Linux daemon、补 NO_PROXY、加 Docker Desktop 提示 |
| add | 3 处 | 4.3 Docker Desktop 设置界面代理、4.4 config.json 容器内代理、文末更新记录 |
| delete | 0 | 无删除 |

## 关键修正（用户需知）

- **Docker Desktop（Windows / macOS）会忽略 daemon.json 里的代理配置**。原笔记只写了改 daemon 的 systemd 方法，会让 Docker Desktop 用户误以为有效。现新增 4.3 节，明确必须用 **Settings → Resources → Proxies → Manual proxy configuration**（HTTP/HTTPS/SOCKS5 + no-proxy 列表），然后 **Apply & Restart**。
- 原 4.2 的 systemd drop-in 方法保留，但限定为**非 Desktop 的 Linux daemon**，该方法 2026 年依然正确（官方）。
- 补充容器内代理标准做法：`~/.docker/config.json` 的 `proxies.default` 在构建 / 运行容器时自动注入。

## 使用到的资料来源（共享来源库）

- **S8**（官方）Docker Desktop 忽略 daemon.json 代理，须用 Settings → Resources → Proxies：https://docs.docker.com/engine/daemon/proxy/
- **S9**（官方）Linux daemon 用 systemd drop-in 设 HTTP_PROXY / HTTPS_PROXY / NO_PROXY：https://docs.docker.com/engine/daemon/proxy/
- **S10**（官方）容器 / 构建代理用 ~/.docker/config.json 的 proxies.default：https://docs.docker.com/engine/daemon/proxy/

来源库文件：`workspace/update-docker/shared_research/source_bank.md`（阶段 P3，2026-08-03）。

## 未解决问题与风险

1. **UI 文案差异**：4.3 的界面路径（Settings → Resources → Proxies）来自官方文档；不同 Docker Desktop 版本的界面文案可能略有差异，但入口稳定。
2. **未做真机验证**：本次为资料驱动的局部更新，未实际运行 Docker Desktop / Linux daemon 验证代理生效；建议用户在目标环境按 4.3 / 4.2 步骤实测。
3. **SOCKS5 在构建阶段的支持**：Docker Desktop 设置界面可填 SOCKS5，但部分构建场景以 HTTP/HTTPS 最稳；若 SOCKS5 不生效，回退 HTTP/HTTPS。
4. **no-proxy 语法**：`localhost,127.0.0.1,*.local` 为常见写法，具体按本地网络环境调整。
5. **未改动 Obsidian vault 原文件**：按 project-output-only 模式，输出到 `updates/proxy/`，原文 `docker/docker进行代理.md` 未动；如需发布到 vault，请在 P5 汇总时确认位置。
