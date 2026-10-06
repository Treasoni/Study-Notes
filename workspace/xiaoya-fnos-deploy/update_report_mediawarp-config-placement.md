# 更新报告：小雅 fnOS 单容器部署 · MediaWarp 配置文件放置澄清（第 5 章 5.4.2）

- 更新日期：2026-10-06
- 目标文件：vault `流媒体与影音/小雅 fnOS 单容器部署/05 前端接入.md`
- destination_mode：`patch-in-place`，**第 5 章三侧已同步**（chapters/ → output/ + vault + final_note）
- 同步方式：反向提取 vault 05 正文 → `chapters/05_前端接入.md` → `publish_copies.py --apply --only 05` + `assemble_final.py --apply`（`vault==` 自证无反退）
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
- **05 已同步**（用户选择「以 vault 为准」）：vault → chapters/05 → output/05 + final_note，四侧一致（`publish_copies --check` 05 全 `=`）。
- **其余漂移仍在**：`publish_copies --check` 显示 **03、04** 仍是 `vault=≠`（vault 比工作区新，mtime 21:27 / 21:40，均在 run 21:16 收口之后）：
  - **03 动手前准备**：vault 比 chapters **少** ~519 字节——vault 把「WebDAV 用户名 `guest` / 路径 `/dav`」一段**并成一句话**，去掉了 output 里的原注释引文与 `[!warning] 用户名填 guest；dav 是路径` 提示框。
  - **04 部署实战**：vault 比 chapters **多** ~272 字节——vault 新增令牌文件落盘说明与两张截图（`assets/04 部署实战/file-*.png`）。
- 03/04 的处置**待用户决定**（尤其 03 方向存疑：vault 是删内容的那侧）。本报告不擅自覆盖。
