# 批量更新意图：小雅 fnOS 单容器部署 — 统一为 monlor 单一路线

- 创建时间：2026-10-06
- 工作流：batch-note-update-flow
- 运行标识：`update-xiaoya-fnos-routes`
- 状态文件：`workspace/workflow-runs/update-xiaoya-fnos-routes.workflow.md`

## 意图参数

```yaml
source_path: "workspace/xiaoya-fnos-deploy/chapters/"
source_scope: glob
source_glob: "*.md"
update_goal: "整套笔记统一采用 monlor 社区镜像 ghcr.io/monlor/xiaoya-alist 单一路线，彻底删除官方镜像 xiaoyaliu/alist 路线（含其文件凭据路线、docker run 示例、端口来源冲突段、双路线对照表、双列更新表）"
destination_mode: patch-in-place
batch_size: 3
shared_research: no
moc_path: "流媒体与影音 MOC.md"
publish_target: "流媒体与影音/小雅 fnOS 单容器部署/"
```

## 为什么 source_path 取 `chapters/` 而不是 vault 目录

本笔记集的产物链是 `chapters/` → `output/` → vault 发布目录，且既有纪律是
「清洗只归属最上游一层，`output/` 与 vault 副本机械重生成」。因此本次更新的
**唯一编辑面**是 `chapters/`；`output/` 与 vault 目录按同一套替换机械同步，避免三份漂移。

## 更新边界（本次明确不改）

- 第 2 章的「两条路线」指 **Emby 全家桶（E）vs 飞牛影视（F）**，与镜像路线无关，**不动**。
- `sources/` 下的素材文件是归档，不回改；官方镜像页 `sources/01_hub_docker_com.md` 保留在库内，
  仅从正文引用中移除。
- 第 5 章 5.6 的内容（夸克 / 115 / 小雅资源播放盘）与本次目标无关，仍按既有口径，**不动**。

## 待确认项（P0 检查点）

1. `destination_mode`：采用 `patch-in-place`（改 `chapters/` 并同步 `output/` + vault 三份副本）。
2. `batch_size`：默认 3。
