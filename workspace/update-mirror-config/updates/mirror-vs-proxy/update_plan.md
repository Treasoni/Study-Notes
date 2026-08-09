# update_plan：docker/镜像加速器vs代理-概念对比.md

## 目标
修复 `~/.docker/daemon.json` 对 Docker Desktop 无效的误导 + 移除已失效镜像源 USTC。

## 动作
1. frontmatter `updated` → 2026-08-08
2. 快速结论表「配置位置」行补充 Docker Desktop 用 GUI
3. 3.3 配置方式：修正注释（Docker Desktop 不读 ~/.docker/daemon.json；仅 Linux dockerd）
4. 6.1 配置速查表：修正注释 + 移除 USTC + 新增 xuanyuan.me
5. 追加「更新记录」，更新「最后更新」

## 来源
- workspace/update-mirror-config/shared_research/source_bank.md
