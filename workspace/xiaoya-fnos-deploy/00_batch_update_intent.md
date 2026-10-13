# 批量更新意图（run: update-xiaoya-fnos-alist）

```yaml
source_path: "workspace/xiaoya-fnos-deploy/chapters/"
source_scope: glob
source_glob: "*.md"
update_goal: >
  把「小雅 fnOS 单容器部署」整套笔记的部署路线，从已停止维护的 monlor 镜像
  （ghcr.io/monlor/xiaoya-alist，最后一次提交 2025-03-27）统一改写为持续维护的
  xiaoyaDev/xiaoya-alist（DDSRem 整合脚本，最后提交 2026-10-06），
  部署方式改用其 README 给出的一键菜单脚本，保持「单容器 / 不装 Emby / 飞牛影视当前端」主线。
destination_mode: patch-in-place  # chapters/ 为准，再经 publish_copies.py 同步 output/ 与 vault 三副本
batch_size: 3
shared_research: yes
moc_path: "流媒体与影音 MOC.md"
stale_threshold: "contains:monlor OR contains:ghcr.io/monlor OR contains:EMBY_ENABLED"
```

## 触发事实（核查结果）

| 项目 | 最后提交 | 状态 | 其他 |
| --- | --- | --- | --- |
| `monlor/docker-xiaoya`（笔记现用） | **2025-03-27** | 未归档但近 18 个月无提交 | `ghcr.io/monlor/xiaoya-alist`；README 只对 `docker run` 标「不推荐」 |
| `xiaoyaDev/xiaoya-alist`（改用） | **2026-10-06** | 活跃维护 | DDSRem 整合脚本，8.5k star；支持 fnOS ✅ |

## 用户确认（2026-10-07）

1. **改动范围**：整套 8 篇统一改写（保持 1→7 章节结构不变）。
2. **部署形态**：一键菜单脚本 `bash -c "$(curl --insecure -fsSL https://ddsrem.com/xiaoya_install.sh)"`，菜单 `1 1` 只装「小雅Alist」。
3. **主线**：保持「单容器 / 不装 Emby / 飞牛影视当前端」，不扩展为全家桶教程。

## 关键一手资料（已取）

- 项目 README（菜单全表、兼容性表、fnOS ✅）：`sources/01_raw_githubusercontent_com.md`
- 安装脚本 `all_in_one.sh` 6567 行：`1 1` → `install_xiaoya_alist()`，用 `xiaoyaliu/alist:latest` 镜像，
  端口 `5678:80 / 2345 / 2346 / 2347`，配置目录默认 `/etc/xiaoya`，`--restart=always`，
  WebDAV `http://ip:5678/dav`；`wait_xiaoya_start` 以日志行 `success load storage: [/©️` 判定就绪（60s~600s）。

## 副本同步机制

`chapters/*.md` 为正文唯一来源；`publish_copies.py --apply` 重建 `output/` 与 vault 副本（保留 frontmatter 与章首/章末导航行）；
`assemble_final.py --apply` 重建 `output/final_note.md`。总览页不在 `chapters/`，需在 `output/` 与 vault 直接改。
