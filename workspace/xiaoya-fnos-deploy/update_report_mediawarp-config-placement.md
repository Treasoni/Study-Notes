# 更新报告：小雅 fnOS 单容器部署 · MediaWarp 配置放置澄清 + 配置补全与用法（第 5 章 5.4.2 / 5.4.5）

- 更新日期：2026-10-06
- 目标文件：vault `流媒体与影音/小雅 fnOS 单容器部署/05 前端接入.md`
- destination_mode：`patch-in-place`；**03/04/05 三章均以 vault 为准同步到工作区**（chapters/ → output/ + vault + final_note）
- 同步方式：反向提取 vault 正文 → `chapters/` → `publish_copies.py --apply` + `assemble_final.py --apply`（`vault==` 自证无反退）
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
- **05 已同步**（用户选择「以 vault 为准」）：vault → chapters/05 → output/05 + final_note，四侧一致。
- **03、04 亦已同步**（用户后续确认「都按 vault 同步」）：
  - **03 动手前准备**：vault 侧把「WebDAV 用户名 `guest` / 路径 `/dav`」并成一句话，去掉了工作区里的原注释引文与 `[!warning] 用户名填 guest；dav 是路径` 提示框。按用户决定，以 vault 为准同步到工作区。
  - **04 部署实战**：vault 侧新增令牌文件落盘说明与两张截图（`assets/04 部署实战/file-*.png`，文件存在），同步到工作区。
- **收口校验**：`publish_copies.py --check` 七章全 `output== vault==`；`assemble_final.py --check` 0 章待更新。工作区与 vault 不再漂移。

## 追加更新：配置补全 + 客户端接入用法（2026-10-06，第 5 章 5.4.2 / 新增 5.4.5）

- 起因：用户问「我配置好了 mediawarp，怎么用啊」→ 回一手来源发现 **5.4.2 只给了 `server.type`，缺 `port` / `server.addr`**，照笔记配会「配完了不知道怎么用」。
- 新增来源存档：`sources/lens-b/mediawarp/04_config_yaml_example.md`（官方 `config/config.yaml.example` 逐字抓取，raw，87 行；去 BOM）。

| 位置 | 变更 |
| --- | --- |
| `05` **5.4.2** | `config.yaml` 代码块补全为 `port: 9000` + `server{type:FNTV, addr, auth}`；加**字段分工表**（`port` 监听口 / `type` 类型 / `addr` 上游地址 / `auth` FNTV 不需要）；新增 `[!warning]` **漏 `server.addr` 用不起来** |
| `05` **5.4.5（新增）** | 「装完不等于用上：让客户端改连中间件端口」：`客户端 → MediaWarp:9000 → 302 直连 / 回退推流` 链路图 + 「必须走 `port`」+ 与 fntv-proxy 同构 + 端口映射前提 + 回退为正常设计 + 验收方法 |
| `05` 引文对照 | 新增 43–45 行（`port` / `addr` / `auth` 三行逐字，含 FNTV 默认端口 8005 的注释） |
| `05` 更新记录 | 追加一行 |

- 未引用的来源：飞牛论坛 `tid=54781` / `tid=24834` 有 WAF 拦截，取不到逐字原句，故**不引用**；「客户端走代理端口」这条改由已存档官方来源支撑（README 前置反代定义 `01_github_com.md:51`、配置 `port` 字段 `04_config_yaml_example.md:8`、fntv-proxy 的「指向代理端口」`fntvproxy/01_github_com.md:71`）。
- 同步：反向提取 vault 05 → `chapters/05_前端接入.md` → `publish_copies.py --apply --only 05` + `assemble_final.py --apply`；`check-md-structure.py` 0 处可疑；`publish_copies --check` 七章全 `=`。
