# Stale Map — DockerDesktop镜像加速器配置.md

> 工作流：batch-note-update-flow（update-docker）
> 笔记：`docker/DockerDesktop镜像加速器配置.md`
> 分析时间：2026-08-03
> 依据：`workspace/update-docker/shared_research/source_bank.md`（S1–S8）

## 过时项（update）

| # | 位置 | 现状内容 | 问题 | 处理 | 依据 |
|---|------|----------|------|------|------|
| S-1 | 二·步骤3 JSON 示例 | `https://docker.mirrors.ustc.edu.cn` | 中科大 Docker 加速器 2024-06 起停服 | 替换为 `https://docker.xuanyuan.me` | S4/S5 |
| S-2 | 三·3.2 写入示例 | `https://docker.mirrors.ustc.edu.cn` | 同上 | 替换 | S4/S5 |
| S-3 | 三·3.3 完整配置 | `https://docker.mirrors.ustc.edu.cn` | 同上 | 替换 | S4/S5 |
| S-4 | 三·3.5 一键脚本 | `https://docker.mirrors.ustc.edu.cn` | 同上 | 替换 | S4/S5 |
| S-5 | 四·4.1 预期输出 | `https://docker.mirrors.ustc.edu.cn` | 同上 | 替换 | S4/S5 |
| S-6 | 五·镜像源表 | 中科大 / 南大 / 上海交大 三行 | 三家均已停服 | 删除三行，换轩辕镜像 + 阿里云 ACR | S4/S5 |
| S-7 | 五·多源 JSON | `https://docker.nju.edu.cn` | 南大已停服 | 移除，仅保留当前可用源 | S4 |
| S-8 | 参考资料·第三方 | `mirrors.ustc.edu.cn/help/dockerhub.html` | 中科大 Docker 帮助页已失效 | 移除，补充 2026 社区教程与官方 release notes | S4/S5 |
| S-9 | frontmatter | 缺 title/status/source_project；`updated=2026-03-04` | 未满足规范 | 补 title/status/source_project，`updated` 改 2026-08-03 | 质量要求 |
| S-10 | 文末「最后更新」 | 2026-03-04 | 过时 | 更新为 2026-08-03 | 质量要求 |

## 需新增（add）

| # | 位置 | 新增内容 | 依据 |
|---|------|----------|------|
| A-1 | 概述 callout | Docker Desktop 4.83 / Engine 29.x 版本基线说明 | S1/S2 |
| A-2 | 二·步骤概览后 | tip：GUI 配置入口在 Mac/Windows 一致 | S6 |
| A-3 | 二·步骤3 JSON 后 | tip：`registry-mirrors` 数组仍受支持，仅 `dockerd --registry-mirror` flag 弃用 | S6 |
| A-4 | 五·表格前 | warning：国内镜像站大面积关停背景 + 社区源不保证长期有效 + 只支持 pull 不支持 search | S4/S5 |
| A-5 | 五·表格 | 轩辕镜像 `docker.xuanyuan.me`、阿里云 ACR 个人版 | S5 |
| A-6 | 五·表格后 | tip：阿里云 ACR 控制台获取个人加速地址 | S5 |
| A-7 | 六·Q1 | 排查项：全限定名 `docker.io/xxx` 会绕过镜像源 | S6 |
| A-8 | 六·Q3 | 替代方案：Settings→Resources→Proxies 代理、云镜像服务、Cmirror | S7/S8 |
| A-9 | 文末 | `## 更新记录` 章节 | 质量要求 |

## 保持不变（keep）

- 一、为什么需要镜像加速器（是什么/为什么/通俗理解/工作原理图）
- 二、GUI 四步流程结构与截图示意结构（仅镜像列表与提示新增）
- 三、命令行配置的目录位置、vim/nano 编辑、osascript 重启方式
- 四、验证配置的 4.2 测速、4.3 详细配置
- 六、Q2/Q4/Q5/Q6（Q4 措辞微调，Q3 增补方案）
- 个人笔记、相关文档双链
- 原有 `[!info]` / `[!personal]` callout 结构与语气

## 删除（delete）

| # | 内容 | 原因 |
|---|------|------|
| D-1 | 五·表格 USTC / 南大 / SJTU 三行 | 2024-06 起停服（S4） |
| D-2 | 参考资料中中科大镜像站链接 | 已失效（S4） |
