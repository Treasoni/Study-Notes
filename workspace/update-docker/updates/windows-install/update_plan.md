# update_plan — Windows Docker Desktop 安装指南（国内网络版）

> 运行：update-docker / Batch 1 / windows-install
> 生成时间：2026-08-03
> 目标：全面刷新到 2026 最新版本与最佳实践，保持原有「步骤式安装指南 + 国内网络专项提示」结构与文风。

## 更新策略

- **局部 patch**：只改过期/失效内容，保留原笔记的结构、写作风格与个人语气。
- **不覆盖原文件**：输出到 `updates/windows-install/updated_note.md`，原文件不动（destination_mode = project-output-only）。
- **不联网补充**：所有 2026 事实来自共享来源库 source_bank.md（S1–S12），不虚构镜像直链。

## 具体变更项

### 1. Frontmatter 补齐（→ updated_note.md 顶部）
- 保留 `tags`、`created: 2026-03-29`。
- `updated` 改为 2026-08-03。
- 新增 `title`、`status: active`、`source_project: update-docker`。

### 2. 安装前准备（一、）
- 在 1.1 系统要求表格下新增 2026 版本基线 callout：
  - Docker Desktop 4.83.0（2026-07-20）/ 内置 Engine 29.6.2 / Compose v5.3.1；Engine 28 已于 2026-05 EOL（S1/S2/S3）。
  - 安装器默认 per-user 安装。
- 1.2 步骤 1 WSL2 主流程改为现代三件套：`wsl --install` → `wsl --update` → `wsl --version`（S11）。
  - 新增推荐说明：Microsoft Store 版 WSL 为默认推荐，更新更快、内置 WSLg（S11）。
  - 新增常见错误 callout：0x80370114、内核下载超时（手动装 `wsl_update_x64.msi`）、0x80070422（S12）。
  - 删除/弱化 `wsl --set-default-version 2`（已由 install 自动完成）。
- 1.2 步骤 2「启用虚拟机平台」降级为备用步骤，注明 `wsl --install` 一般已自动启用（S11）。
- 1.2 步骤 4 验证追加 `wsl --version`。

### 3. 下载方案（二、）
- 方案 A 官方直链表保留，新增「核对版本」warning：下载前查 Docker Desktop Release Notes（S2）。
- 方案 B 第三方镜像站表格保留，新增 warning：安装包不一定在镜像站同步，官方安装包优先 `desktop.docker.com` / Release Notes；第三方链接**需自行验证**（不虚构可用直链）。
- 方案 C 补充官方 Release Notes 链接作为版本权威来源，说明安装包以官方渠道分发为主。

### 4. 镜像加速器配置（四、）
- 方法一 GUI（Settings → Docker Engine）JSON 中的 `registry-mirrors` 更新为 2026 可用源：
  `docker.m.daocloud.io`、`docker.1ms.run`、`docker.xuanyuan.me`、`docker.1panel.live`（S5）。
- 方法二原「`notepad %USERPROFILE%\.docker\daemon.json`」是错误路径（该目录是 CLI 配置目录，Docker Desktop 引擎不读取），改为：
  - 明确 Docker Desktop 通过 **Settings → Docker Engine** 修改 `registry-mirrors`（S6）；
  - daemon.json 手动编辑仅适用于 Linux Docker Engine（保留 JSON 示例，去掉失效 USTC 源）。
- 4.2 可用镜像源列表重写：
  - 失效源标记删除：中科大 `docker.mirrors.ustc.edu.cn`、南大 `docker.nju.edu.cn`、SJTU（2024-06 起停服，S4）。
  - 保留/新增社区可用源：DaoCloud、1ms.run、XuanYuan、1Panel、耗子面板 hub.rat.dev（S5）。
  - 新增阿里云 ACR 个人免费版 `https://<your-id>.mirror.aliyuncs.com`（S5）。
  - 补充说明：多数社区源只支持 `docker pull`、不支持 `docker search`（S5）。
- 验证配置的预期输出同步为新的镜像源地址。

### 5. 常见问题（五、）
- 5.3 问题 1 补充 0x80370114 / 内核超时 / 0x80070422（S12）。
- 5.5 问题 2 排查路径改为 Settings → Docker Engine（S6）；JSON 格式校验提示保留。
- 其余（5.1/5.2/5.4/5.5 问题 1/3）保留。

### 6. 使用中问题（六、）
- 6.2 保留 compose 环境变量代理示例，新增 `~/.docker/config.json` 的 `proxies.default` 方案作为替代（S10）。

### 7. 其它
- 参考资料新增官方 Release Notes（Docker Desktop / Engine 29）与 2026 社区教程（S5）；原镜像源文章标注「需复核」。
- 结尾新增 `## 更新记录`（2026-08-03 + 变更摘要）；「最后更新」改为 2026-08-03。
- `[!info]`/`[!personal]` callout 统一到项目允许类型（`[!summary]`/`[!note]`）。

## 明确不做

- 不改写未过时的章节（3.3 验证、5.2、5.4、6.1、6.3、七、八、个人笔记）。
- 不虚构任何具体的国内安装包镜像直链。
- 不触碰原 vault 文件。
