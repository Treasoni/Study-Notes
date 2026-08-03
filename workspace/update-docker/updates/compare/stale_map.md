# stale_map — 镜像加速器vs代理-概念对比.md

> 运行标识：update-docker
> 笔记：docker/镜像加速器vs代理-概念对比.md
> 更新目标：全面刷新到 2026 最新（镜像加速器与代理概念对比）
> 生成时间：2026-08-04

## 过时项 / 变更映射

| 原文位置 | 状态 | 说明 | 依据 |
|---|---|---|---|
| frontmatter（缺 title/status/source_project，updated=2026-03-28） | 🔄 update / ➕ add | 补 `title`、`status`、`source_project`；`updated` → 2026-08-04；保留 `created=2026-03-28` 与 tags | 项目 Obsidian 规范 |
| 概述 callout | 🔄 update | 补充版本基线：Docker Desktop 4.83 / Docker Engine 29.x（2026-08 现状） | S1/S2 |
| 一、快速结论：核心区别表 | ✅ keep | 概念性对比，2026 仍成立 | 非时效 |
| 2.1 镜像加速器（比喻 / 示例配置 / 原理图） | ✅ keep（+补充） | 示例配置的 daoCloud / 1ms.run 仍可用；新增「2026 镜像源现状」warning | S5 |
| 2.1 后 | ➕ add | 新增 [!warning]：2024-06 起国内镜像站大面积关停（USTC/NJU/SJTU/阿里云/腾讯云）；社区源只支持 pull 不支持 search、不保证长期有效；阿里云 ACR 个人版稳定选项 | S4/S5 |
| 2.2 代理（比喻 / Compose 示例 / 原理图） | ✅ keep | 容器 env 代理写法 2026 仍正确 | 非时效 |
| 3.1 作用范围对比图 | ✅ keep | 概念性内容 | 非时效 |
| 3.2 功能对比表 | ✅ keep | 概念性内容 | 非时效 |
| 3.3 镜像加速器配置 | 🔄 update（澄清） | 配置入口注释改为 Docker Desktop Settings → Docker Engine / Linux /etc/docker/daemon.json；补 tip：`registry-mirrors` 机制仍受支持（仅 CLI flag 弃用） | S6 |
| 3.3 Docker Daemon 代理配置 | 🔄 update（澄清） | 明确 systemd 方式只适用于**非 Desktop 的 Linux daemon**；Docker Desktop 必须用 Settings → Resources → Proxies | S8/S9 |
| 3.3 容器代理配置 | 🔄 update（补充） | 补 `~/.docker/config.json` 的 `proxies.default` 统一注入方案 | S10 |
| 4.1 决策流程图 | ✅ keep | 概念性内容 | 非时效 |
| 4.2 典型场景推荐表 | ✅ keep（+说明） | 表保持不变；表后补镜像源稳定性说明 | S5 |
| 5.1 误区 1（加速器 ≠ 容器内访问 Google） | ✅ keep（+补充） | 结论仍准确；补充社区源只支持 pull 不支持 search，更不可能替代代理 | S5 |
| 5.2 误区 2（daemon 代理 ≠ 容器内访问外网） | ✅ keep（+补充） | 结论仍准确；补例外说明：Docker Desktop 的 Settings → Resources → Proxies 会自动把代理传播给容器 | S8 |
| 5.3 误区 3（加速器与代理不冲突） | ✅ keep | 仍准确 | 非时效 |
| 6.1 镜像加速器配置速查 | 🔄 update | 删除失效源 `docker.mirrors.ustc.edu.cn`，替换为 `docker.xuanyuan.me`；入口注释修正为 Docker Desktop Settings → Docker Engine；补镜像源稳定性 warning | S4/S5/S6 |
| 6.2 Docker Daemon 代理速查 | 🔄 update（澄清） | systemd 方式保留并加 Docker Desktop 警告；补 daemon.json `proxies` 块替代方案 | S8/S9 |
| 6.3 容器代理速查 | 🔄 update（补充） | 补 `~/.docker/config.json` 统一注入方案 | S10 |
| 七、一张图总结 | ✅ keep | 概念性总结图，保持不变 | 非时效 |
| 参考资料 | 🔄 update | 保留官方资源；补充 2026 社区来源（zachthinking 教程、镜像站关停背景） | S4/S5/S6 |
| 文末 | ➕ add | 追加 `## 更新记录`（2026-08-04）；「最后更新」改 2026-08-04 | 项目规范 |
| 删除项 | 🗑️ delete | 6.1 列表删除失效镜像源 `docker.mirrors.ustc.edu.cn` | S4 |
