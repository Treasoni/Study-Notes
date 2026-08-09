# stale_map：docker/Windows-DockerDesktop安装指南-国内网络版.md

> 生成：2026-08-08 ｜ 模式：patch-in-place（已应用）

## 保留
- 快速导航、安装章节、WSL2 配置、资源配置、验证命令
- ASCII 示意图（1panel/xuanyuan/daocloud 均可用）
- 常见配置错误示例（1panel/xuanyuan 仍可用）

## 需要更新
| 位置 | 旧内容 | 新内容 |
|------|--------|--------|
| L257-274 「方法二：命令行配置」 | `notepad %USERPROFILE%\.docker\daemon.json` + JSON 含 USTC | 改为「仅 Linux 原生 dockerd」+ `[!warning]` 说明 Docker Desktop 不读取该文件 + Linux 示例 |
| L292-300 源状态表 | USTC「⚠️ 时好时坏」、NJU「⚠️ 需验证」 | 两者改「❌ 已失效」；新增 1ms.run ✅ |
| L498-506 问题2排查 | `notepad %USERPROFILE%\.docker\daemon.json` + Get-Content | 改为 GUI 检查 + docker context ls |

## 需要删除
- `docker.mirrors.ustc.edu.cn`（JSON 中）、`docker.nju.edu.cn`（状态表标记失效）

## 需要新增
- `docker.1ms.run`（可用源）
- `## 更新记录` 段
- Docker Desktop 不读 `%USERPROFILE%\.docker\daemon.json` 的说明
