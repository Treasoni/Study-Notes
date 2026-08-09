# update_report：docker/镜像加速器vs代理-概念对比.md

- **状态**：✅ 已完成（patch-in-place）
- **更新时间**：2026-08-08
- **改动摘要**：
  - 修正 2 处 `~/.docker/daemon.json`（Mac Docker Desktop）错误前提 → 改为「Docker Desktop 用 GUI，仅 Linux dockerd 读 /etc/docker/daemon.json」
  - 快速结论表「配置位置」行补充 Docker Desktop GUI 入口
  - 配置示例移除已失效 `docker.mirrors.ustc.edu.cn`，新增 `docker.xuanyuan.me`
  - 追加「更新记录」，frontmatter `updated` → 2026-08-08
- **来源**：[docker/for-mac#2537](https://github.com/docker/for-mac/issues/2537) · [Docker daemon 配置文档](https://docs.docker.com/engine/daemon/) · [dongyubin/DockerHub](https://github.com/dongyubin/DockerHub)
- **未处理风险**：对比表/示意图中「daemon.json 的 registry-mirrors」作为概念表述保留（语境正确）；个人笔记为空待用户补充
