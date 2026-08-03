# update_report — Windows Docker Desktop 安装指南（国内网络版）

> 运行：update-docker / Batch 1 / windows-install
> 生成时间：2026-08-03
> 输入：`C:\note\Study-Notes\docker\Windows-DockerDesktop安装指南-国内网络版.md`
> 输出：`C:\note\Study-Notes\workspace\update-docker\updates\windows-install\updated_note.md`
> 原文件：未改动（destination_mode = project-output-only）

## 一、变更摘要

本次为**局部 patch**，共 4 类实质变更，未重写未过时章节：

1. **Frontmatter 补齐**
   - `updated` → 2026-08-03；新增 `title`、`status: active`、`source_project: update-docker`；保留 `tags` 与 `created`。

2. **WSL2 安装主流程（一、）**
   - 主流程改为 `wsl --install` → `wsl --update` → `wsl --version`（S11），移除已被 install 自动完成的 `wsl --set-default-version 2`。
   - 新增 Microsoft Store 版 WSL 推荐说明（默认、更新更快、内置 WSLg）。
   - 新增常见错误：0x80370114 / 内核下载超时（`wsl_update_x64.msi`）/ 0x80070422（S12）。
   - 「启用虚拟机平台」DISM 步骤降级为备用。

3. **下载方案（二、）**
   - 官方直链保留，新增「核对 Docker Desktop Release Notes」提示（S2）。
   - 第三方镜像站标注「需验证」，明确官方安装包优先官方渠道；**未虚构任何安装包镜像直链**。

4. **镜像加速器（四、）**
   - `registry-mirrors` 列表更新为 2026 可用社区源：daocloud、1ms.run、xuanyuan、1panel（S5）。
   - 移除失效源：中科大 USTC、南京大学 NJU、上海交大 SJTU（2024-06 起停服，S4）。
   - 新增阿里云 ACR 个人免费版与耗子面板（S5）。
   - 纠正配置路径：Docker Desktop 通过 **Settings → Docker Engine** 配置（S6）；`%USERPROFILE%\.docker\daemon.json` 是 CLI 配置目录，Desktop 引擎不读取，原「方法二 notepad」已修正并限用于 Linux Engine。

5. **其它**
   - 版本基线新增：Docker Desktop 4.83 / Engine 29.x / Compose v5.x（S1/S2/S3）。
   - 5.3 安装失败补充 2026 WSL 常见错误；5.5 配置排查路径改为 Settings → Docker Engine。
   - 6.2 补充 `~/.docker/config.json` 的 `proxies.default` 容器代理方案（S10）。
   - 参考资料新增官方 Release Notes 与 2026 社区教程；callout 类型统一到项目允许集合（[!summary]/[!note]）。
   - 新增 `## 更新记录` 章节。

## 二、使用到的来源（source_bank.md）

| 来源编号 | 内容 | 用途 |
|---------|------|------|
| S1 | Docker Engine 29 release notes（29.6.2） | 版本基线、Engine 28 EOL |
| S2 | Docker Desktop release notes（4.83.0，per-user 默认） | 版本基线、下载提示、安装方式 |
| S3 | Docker Engine 支持周期 | 版本基线（29.x 当前维护线） |
| S4 | 国内 Docker Hub 镜像站集体下线背景 | USTC/NJU/SJTU 失效判定 |
| S5 | 2025-2026 社区可用镜像源清单 | registry-mirrors 替换源、只支持 pull 说明、阿里云 ACR |
| S6 | registry-mirrors 配置机制仍受支持 | Settings → Docker Engine 配置路径、配置不生效原因 |
| S10 | 容器/构建代理（config.json proxies.default） | 6.2 补充方案 |
| S11 | WSL 安装与更新（Store 版默认推荐） | WSL2 主流程重写 |
| S12 | WSL 版本 2.6.x 与常见错误 | 版本参考、0x80370114 / 内核超时 / 0x80070422 |

未使用：S7（替代方案，已在 [[docker进行代理]] 覆盖）、S8（Docker Desktop 忽略 daemon.json 代理）、S9（Linux daemon 代理）。

## 三、未解决风险 / 需用户复核

| 风险 | 等级 | 说明 |
|------|------|------|
| 镜像源时效波动 | 🟡 中 | S5 清单为社区实测，**不保证长期有效**。笔记已提示配置多个并实测，但具体可用性仍须以实际 `docker pull` 为准。 |
| 第三方安装包镜像站 | 🟡 中 | 2.3 中阿里云/清华/华为镜像站是否同步 Docker Desktop 安装包**未经验证**，已标注需自行验证；未提供任何具体可用直链。 |
| WSL 具体版本号 | 🟢 低 | 以 `wsl --version` 实际输出为准（2026 年初约 2.6.x），未写死具体数字。 |
| `hello-world` 拉取 | 🟢 低 | 验证命令保留，但首次 `docker run hello-world` 需能访问镜像源，否则可能拉取失败（属预期网络问题，见第五章）。 |
| daemon.json 路径细节 | 🟢 低 | 5.5 问题 2 中 `%ProgramData%\docker\config\daemon.json` 路径为推断，Windows 版本间可能有差异；正文已强调以 **Settings → Docker Engine** 为权威入口。 |

## 四、质量自检

- [x] 原文件未修改，输出到新路径 `updated_note.md`
- [x] YAML frontmatter 含 title/tags/created/updated/status/source_project，updated=2026-08-03
- [x] 保留原有结构、步骤式文风与国内网络专项提示
- [x] 代码块均带语言标识（powershell/json/yaml/mermaid 等）
- [x] callout 均为结构意义且属于允许类型（[!summary] [!note] [!tip] [!warning]）
- [x] 未在列表项内嵌套表格
- [x] 未新增来源库之外的事实；未虚构镜像直链
- [x] 末尾追加 `## 更新记录` 章节
