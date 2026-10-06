# 更新报告：小雅 fnOS 单容器部署 · MediaWarp 配置文件放置澄清（第 5 章 5.4.2）

- 更新日期：2026-10-06
- 目标文件：vault `流媒体与影音/小雅 fnOS 单容器部署/05 前端接入.md`
- destination_mode：本次为 **vault 单侧 `patch-in-place`**（工作区副本未动，见文末漂移）
- update_goal：回答用户「mediawrap 的 docker 不是这么写的吗？」——用户把 **`docker-compose.yml`** 与 **MediaWarp 的 `config.yaml`** 抄成了一个文件

## 触发与决策

- 用户贴出合并后的片段（`services:` 块 + `server: type: FNTV`），问 MediaWarp 的 Docker 是不是这么写。
- 回一手来源核对（`sources/lens-b/mediawarp/03_blog_akimio_top.md`）确认：`server.type` 属于**配置文件 `config.yaml`**（「需要映射进容器的 `/config` 目录下」，`:54`），不在 compose 里。
- 用户确认「可以」，要求把这条澄清写进 5.4.2。

## 变更摘要

| 位置 | 变更 |
| --- | --- |
| `05 前端接入.md` **5.4.2** | `server: type: FNTV` 代码块加首行注释 `# config.yaml（…不是 docker-compose.yml）`；其后新增 `[!warning] server.type 属于 config.yaml，别贴进 docker-compose.yml`：说明两个代码块分属两个文件、`server.type` 需映射进容器 `/config`、贴进 compose 的实测报错、以及 `volumes:` 左侧宿主机路径可自定义 |
| `05` 引文对照 | 新增第 42 行（`:54` 逐字原文） |
| `05` 更新记录 | 追加一行 |

## 实测记录（非凭常识）

把 `server:` / `type:` 贴到 compose 顶层后实测：

```text
$ docker compose -f mw-test.yml config
validating /tmp/mw-test.yml:  additional properties 'server' not allowed
```

Compose v5.0.2。结论：`server` 不是 Compose 合法顶层键，`docker compose up` 会直接报错。该结论已写入正文 `[!warning]`。

## 未动文件（说明为何不因此澄清而错）

- `02 选型对比.md` / `06 避坑清单.md` / `07 运维与收尾.md` 提及 MediaWarp，但只涉定位与并列介绍，不含 compose / config 放置细节，措辞不因此澄清而错。

## 登记的工作区漂移

- 上游 run `update-xiaoya-fnos-routes`（`batch-note-update-flow`）已 `current_phase: done` / `quality_gate: passed`（2026-10-06 21:16），不会再被任何流程更新。
- **vault 侧** `05 前端接入.md` 已于 **2026-10-06 22:09 之后**继续更新（含本次澄清）；**工作区副本停留在 21:12**：`workspace/xiaoya-fnos-deploy/chapters/05_前端接入.md`、`output/05 前端接入.md`、`output/final_note.md`。
- 漂移**不止本次澄清**：vault 在 run 收口后还改过第 5 章（5.6 夸克等）。两侧文件名相同，易被误当权威稿。
- 处置交由用户二选一：**重跑 note-assembler 同步工作区**，或**明确弃用工作区副本**。本报告不擅自回写工作区。
