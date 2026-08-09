# update_report：docker/Windows-DockerDesktop安装指南-国内网络版.md

- **状态**：✅ 已完成（patch-in-place）
- **更新时间**：2026-08-08
- **改动摘要**：
  - 「方法二：命令行配置」修正为「仅 Linux 原生 dockerd」；新增 `[!warning]` 说明 Docker Desktop 不读取 `%USERPROFILE%\.docker\daemon.json`
  - 源状态表：USTC/NJU 标记「❌ 已失效」，新增 `docker.1ms.run` ✅
  - 问题 2「镜像加速器不生效」排查步骤改为 GUI 检查 + `docker context ls`
  - 追加「更新记录」，frontmatter `updated` → 2026-08-08
- **来源**：[docker/for-mac#2537](https://github.com/docker/for-mac/issues/2537) · [Docker daemon 配置文档](https://docs.docker.com/engine/daemon/) · [dongyubin/DockerHub](https://github.com/dongyubin/DockerHub)
- **未处理风险**：`docker.1panel.live` 保留为「✅ 可用」（GitHub 列表标注仅限中国地区，实测返回 403 可能为地区/UA 限制，需用户实地验证）
