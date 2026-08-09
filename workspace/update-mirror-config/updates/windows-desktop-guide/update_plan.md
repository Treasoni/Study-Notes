# update_plan：docker/Windows-DockerDesktop安装指南-国内网络版.md

## 目标
修复 `%USERPROFILE%\.docker\daemon.json` 对 Docker Desktop 无效的误导 + 移除已失效镜像源 USTC/NJU。

## 动作
1. frontmatter `updated` → 2026-08-08
2. 「方法二：命令行配置」改为「仅 Linux 原生 dockerd」，加 `[!warning]` 说明 Docker Desktop 不读该文件，并给 Linux 示例
3. 源状态表：USTC/NJU 标记「❌ 已失效」，新增 1ms.run
4. 问题 2 排查步骤改为 GUI 检查 + docker context
5. 追加「更新记录」，更新「最后更新」

## 来源
- workspace/update-mirror-config/shared_research/source_bank.md
