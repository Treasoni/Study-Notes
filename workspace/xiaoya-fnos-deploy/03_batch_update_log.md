# 批量更新执行日志（run: update-xiaoya-fnos-alist）

对应 `02_batch_update_plan.md`。批次编排见其 §2.3；本文件只记**实际执行结果**，不改计划。

输出模式：**patch-in-place**——`updated_note` 即 `chapters/{file}`；整批计划即 `02_batch_update_plan.md`（故不再单列 `update_plan.md`）。

## 批 1 · 部署主线（ch04 → ch03 → ch07）

| 序 | note_id | 文件 | 动作 | 结果 | 校验 | 证据 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ch04 | `chapters/04_部署实战.md` | update（重写） | ✅ 完成 | `publish_copies.py --check --only 04` = OK；两张 monlor 截图经 Obsidian 回收站删除 | `updates/04_部署实战/{stale_map.md,update_report.md}` |
| 2 | ch03 | `chapters/03_动手前准备.md` | update | ✅ 完成 | `publish_copies.py --check --only 03` = OK（output==、vault==） | `updates/03_动手前准备/{stale_map.md,update_report.md}` |
| 3 | ch07 | `chapters/07_运维与收尾.md` | update | ✅ 完成 | `publish_copies.py --check --only 07` = OK（output==、vault==） | `updates/07_运维与收尾/{stale_map.md,update_report.md}` |

## 批 2 · 定位与选型（ch01 → ch02 → overview）

| 序 | note_id | 文件 | 动作 | 结果 | 校验 | 证据 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ch01 | `chapters/01_开篇定位.md` | update | ✅ 完成 | `publish_copies.py --check --only 01` = OK；引文对照 8→13 条，新增术语校正 note | `updates/01_开篇定位/{stale_map.md,update_report.md}` |
| 2 | ch02 | `chapters/02_选型对比.md` | update | ✅ 完成 | `publish_copies.py --check --only 02` = OK（output==、vault==）；引文对照 17→28 条 | `updates/02_选型对比/{stale_map.md,update_report.md}` |
| 3 | overview | `output/小雅 fnOS 单容器部署（总览）.md` + vault 同名 | update（**不在 `chapters/`，两处手改**） | ✅ 完成 | output 与 vault 两处 diff 一致；ch04 条目与读前须知换源 | `updates/02_选型对比/update_report.md`（overview 段） |

## 批 3 · 前端与避坑（ch05 → ch06）

| 序 | note_id | 文件 | 动作 | 结果 | 校验 | 证据 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ch05 | `chapters/05_前端接入.md` | update（轻） | ✅ 完成 | `publish_copies.py --check --only 05` = OK（output==、vault==）；5.6 三处换源，引文对照 23/24/28 行换挂 `all_in_one.sh` | `updates/05_前端接入/{stale_map.md,update_report.md}` |
| 2 | ch06 | `chapters/06_避坑清单.md` | update（轻） | ✅ 完成 | `publish_copies.py --check --only 06` = OK（output==、vault==）；6.2 清理口径分两处、新增 6.5 坑五、引文对照 12→22 条 | `updates/06_避坑清单/{stale_map.md,update_report.md}` |
| 3 | overview（回灌） | `output/…（总览）.md` + vault 同名；`chapters/05_前端接入.md` | update（章名/预告回灌） | ✅ 完成 | overview 章节目录第 6 条改章名、ch05「下一章预告」四类→五类；两处 overview diff 一致；ch05 已重发布 | `updates/06_避坑清单/update_report.md`（遗留 #5） |

## 批间复核记录

| 时间 | 批次 | 复核项 | 结论 |
| --- | --- | --- | --- |
| 2026-10-07 | 批 1（ch04） | 引文锚点回源（`all_in_one.sh`） | 发现 `:1302`→`:1304`、`:1290-1292`→`:1293-1294` 等 3 处偏移，**已修正**；连带修正 `stale_map.md`、`update_report.md` |
| 2026-10-07 | 批 1（ch03） | 引文锚点回源（`all_in_one.sh`） | 发现 `:737`→`:742`、`:735-742`→`:740-742`、`:679-688`→`:680`、`:1302`→`:1304`、`:1291/:1292`→`:1293/:1294`、`:1240-1246`→`:1237-1245` 共 13 处偏移，**已修正**；连带修正 `shared_research/source_bank.md`（S2、S7 两处） |
| 2026-10-07 | 批 1（ch07） | 引文锚点回源（`01_github_com.md` / README / hub / `all_in_one.sh`） | 全部命中，无偏移；仅补正引文对照第 2 条原文末尾漏掉的 `！`，并修正手动命令出处为 `01_github_com.md:38/48/51/55/58` |
| 2026-10-07 | 批 1 收口 | 残留扫描 `rg -n "monlor\|ghcr.io/monlor" chapters/{03,04,07}*.md` | 03：仅 3 处有意保留（3.2 对照 warning、引文对照逐字引文、更新记录）；04：仅 4.1 背景/note + 引文对照第 7 行 + 更新记录；07：仅更新记录。**批 1 通过** |
| 2026-10-07 | 批 2（ch01） | 引文锚点回源（hub / README / `all_in_one.sh` / lens-b） | 全部命中，无偏移；引文对照 8→13 条，新增术语校正 note（官方＝`xiaoyaliu/alist`） |
| 2026-10-07 | 批 2（ch02） | 引文锚点回源（README `:75-181`、hub、`all_in_one.sh:3479/3485/6061`、lens-b、forum） | 全部命中，无偏移；硬解段与 2.4 资源门槛**整节重写**；引文对照 17→28 条。**批 2 定位与选型（ch01/ch02）通过**，overview 待续 |
| 2026-10-07 | 批 2 收口 | overview 两处副本一致 + 残留扫描 | overview `diff -q` = SYNCED；残留仅读前须知**有意保留**的「早期 `monlor/xiaoya-alist` 已停维护」一句 |
| 2026-10-07 | 批 3（ch05） | 引文锚点回源（`all_in_one.sh:895/912/1154`、`forum/tid-21673.md:11/13`） | 全部命中；首轮残留扫描发现 2 处正文漏改（`:360` `ALIYUN_TO_115`、`:416` 小结 `monlor-144.md:273`），**已定点修正**；复扫仅更新记录行 |
| 2026-10-07 | 批 3（ch06） | 引文锚点回源（`all_in_one.sh:1304/1377/1401/1403/3830`、README `:80/116/117/292`、hub `:18`、club `:51`） | 全部命中；body 无 `monlor` 字样，仅 6.2 `[!note]`（旧写法适用面）+ 引文对照第 17 行含 `AUTO_CLEAR_ENABLED` |
| 2026-10-07 | 批 3 收口 | 章名回灌扫描 `rg -n "避坑清单\|四类" chapters/` | ch06 H1 改「…、UA 与登录」后，overview 第 6 条与 ch05「下一章预告」**两处已回灌**并重发布；ch01:96 为泛指「避坑清单」，无需改。**批 3 前端与避坑通过** |
| 2026-10-07 | P4 收口 | 全量 `publish_copies.py --check` | 发现 **ch04 output/vault 副本滞留在旧锚点**（`:1302`、`:1290-1292`），而 `chapters/04` 已是批 1 修正后的 `:1304`、`:1293-1294`——即批 1 的锚点修正在 ch04 只落到了副本、漏回 `chapters/04`（或副本未随之重发布）。**已核对源码**（`all_in_one.sh:1304` = 强制登入用户名；`:1293-1294` = 两条 WARN）确认真值后 `--apply --only 04` 重发布，七章副本全部 `OK`；`assemble_final.py --apply/--check` 均 `需更新 0 章` |
