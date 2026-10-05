# ERRORS.md

活跃错误记录：当前 **4** 条 —— `ERR-20260929-014` / `-015`（2026-09-29 记）与
`ERR-20261006-016` / `-017`（2026-10-06 记）。本文件里的 E 编号与
`LEARNINGS.md` 的 L 编号各自独立计数；`-016` / `-017` 的机制化（落 note-beautifier
结构自检）尚未完成，见各自 `预防措施`。

最近一次维护 2026-09-30（`/maintain-learnings`）：归档 `ERR-20260929-013`
（机制已机器化，改由共享引文校验器 `.codex/scripts/note-citation-check.py` 的 `V` 族强制，
并已验证），条目全文见 `.learnings/archive/2026-09-30-archived.md`，
处置路径与验证方式见 `.learnings/archive/2026-09-30-maintenance.md`。
再上一次 2026-09-29 归档 5 条旧记录（`-008` / `-009` / `-010` / `-011` / `ERR-20260924-012`），
见同目录对应文件。

新增错误追加到本文件末尾（错误 / 触发场景 / 根因 / 修复 / 预防措施）；
修复落到机制并验证通过后，才可移入 `.learnings/archive/`。

---

## [ERR-20260929-014] research-collector / P2 — 对照表行数把表头与分隔行也算进去（「17 轴」实为 15 行）

**Logged**: 2026-09-29T23:20:00+0800
**Priority**: medium
**Status**: fixed（全库 12 处订正；源头闸已落 research-collector）
**Area**: research-collector / 计数纪律

### Summary
OpenClaw 官方对照表被记作「17 轴」，实为 **15 条属性行**——17 是属性行计数时把表头与分隔行
也算了进去。错误数字从 `02_deep_research.md` 中转进 `01_explore_result.md`、`03_outline.md`
并扩散到全库 12 处。

### Error
```
(无报错) 「17 轴」在 3 份上游文件与 12 处下游引用里一致，看起来像已核实的数字
```

### Context
- 数字的来源是「数表格行」，没有区分数据行 / 表头 / 分隔行。
- 发现路径：第 6 章写作代理回原文核对时发现。
- 危险点：**同源错误在多处一致**会被误读成「多处印证」。数字一致 ≠ 数字正确。

### 修复
- 全库 12 处订正为「15 行属性对照表」，并在 `02_deep_research.md` 留「口径订正」块记录数错原因。
- 源头闸：research-collector 要求数值**重新计数**而非誊抄，并明确「数表格只数数据行，
  表头与分隔行不是属性」。

### 预防措施
- 落到产物里的每个数字都要有**计数依据**（数的是什么、怎么数的），不只是数值本身。
- 同一数字在多处出现不能作为正确性证据——要回原始载体重新数。

---

## [ERR-20260929-015] learning-note-flow / P7 后回修 — 判据举证段读不通：判据句的措辞与下游术语框架正面冲突

**Logged**: 2026-09-29T23:35:00+0800
**Priority**: high
**Status**: fixed（已按用户选定 A 案修根因并复测；机制已落 workflow 阶段 4）
**Area**: learning-note-flow / P4 验收 / 术语自洽

### Summary
用户读**已发布**笔记时指出第 1 章判据举证段「看的不是很明白」。复核出 3 个实质缺陷，
根因是：判据② 写「服务的用户数是单数还是复数」，而同段下方「多用户」三义 callout 说
同一批对象**都能**进多人（OpenClaw 有「多用户」①、Hermes 有「多用户」②）——判据与框架正面冲突。

### Error
```
用户：「**判据怎么落到具体产物上？** … 你这里这样写，我看的不是很明白」
```

### Context
- 根因：判据② 描述的对象（「能有几个人接触到这台实例」）**不是**下游框架真正切分的那个维度
  （应是「所有者 / 信任域个数」）。两个维度各自都自洽，合起来自相矛盾。
- 次因①：给 Octop 的判据① 引文用错句——`The whole stack is one process.` 说的是进程**个数**，
  判据① 问的是进程**存活方式**（本地 CLI 也是单进程，却属第 1 层）。
- 次因②：判据① 举三家、判据② 只举两家，第 2 层的 Hermes 在判据② 那半段完全缺席，
  结论却要落到「第 2 层与第 3 层分开」。
- 5 处引文本身逐字正确——**引文对 ≠ 论述通**。

### 修复
- 按 A 案改 5 份副本（章节 → 合并件 → 成品 → vault 笔记）：判据② 改述为「所有者 / 信任域个数」，
  补成 3×2 对称举证（补 Hermes 默认拒绝与多 profile 路径两处证据；Octop 换用
  `adr/001-single-process-model.md:14` + `cli.md:120`），第 2 章 L44 收紧为「示例用途**之一**是」。
- 复测：锚点 107→111（新增 4 处全部回原文逐字核对）、表格行 70/70、Callout 26/27、
  正文实义行缺失 0、裸用「多用户」0。
- 源头闸：`workflow.md` 阶段 4 跨章比对新增第 ③ 类「上游判据 / 分类 / 梯度句与下游术语框架
  逐条对读，确认两边能同时对同一对象成立」。

### 预防措施
- 判据句描述的对象，必须是下游框架真正切分的那个维度；两处各自自洽不算过关，
  要能**同时对同一对象成立**。
- 「引文逐字正确」不能替代「论述可读」——校验绿灯与引文核对都通过，成品仍可能读不通。

---

## [ERR-20261006-016] learning-note-flow / P6 发布 — Obsidian callout 续行缺 `>`，表格掉出框外；内容校验全绿仍被用户读到才发现

**Logged**: 2026-10-06
**Priority**: high
**Status**: fixed（上游 `chapters/` 修，下游机械重生成并重新发布；机制待落 note-beautifier 结构自检）
**Area**: learning-note-flow / P6 发布 / Obsidian 结构

### Summary
已发布的第 3 章 `> [!note] 「dav 还是 guest」…` callout 里，引导句与表格之间的**空行没带 `>`**。
Obsidian 在裸空行处终止 callout，其后的表格掉出框外、渲染散架。用户读**已发布**笔记时才报「渲染有问题」。

### Error
```
用户：（贴出 callout 内的对照表）渲染有问题你
```

### Context
- 触发点：callout 内嵌表格时，表格前的空行写成了裸空行（无 `>`）。
- 为什么没被拦住：行尾无关的引文校验器（V/S/C 族）与「8 份副本逐字一致」全部绿灯——
  它们查的是**内容**（引文可回源、副本一致），**不查 Markdown 结构是否可渲染**。
  这是 RULES「Do：校验通过 ≠ 产物正确」的又一实例。
- 全 8 文件扫描：此形态**仅 1 处**（`chapters/03` L103），属个案而非系统性。

### 修复
- 在最上游 `chapters/03_动手前准备.md` 把该裸空行改成 `>`（只加 1 个 ASCII 字符）。
- 从 `chapters/` 机械重生成 `output/01–07` + `final_note.md`，重新发布 7 章到 vault，入口页不变。
- 复验：8/8 成品与 `output/` 逐字一致；`--mode all` ✅ 无硬失败；7 章 `--vault-note` 全 EXIT=0。

### 预防措施
- 发布前跑**结构自检**（本次新增，可复用；在成品目录内运行）：
  ```bash
  PYTHONIOENCODING=utf-8 python - <<'PY'
  import glob
  for f in glob.glob("*.md"):
      L = open(f, encoding="utf-8").read().split("\n")
      for i, l in enumerate(L):
          if l.startswith("|") and i and L[i-1].strip() and not L[i-1].startswith("|"):
              print(f"[{f}] L{i+1} 表格前缺空行")          # 表格不渲染
          if l.startswith("> |") and not L[i-1].startswith(">"):
              print(f"[{f}] L{i+1} callout 内表格未续接 `>`")  # 掉出 callout
  PY
  ```
- callout 内**每个空行**（分段、表格前后）一律写 `>`；与 RULES「Don't：表格不嵌列表」同类——
  **合法 Markdown 却渲染异常的两种形态**。

---

## [ERR-20261006-017] note-citation-check.py — 分册导航尾行 `> 📖` 被当正文，`--vault-note` 每章误报 1 处差异

**Logged**: 2026-10-06
**Priority**: medium
**Status**: fixed（改 canonical 校验器 `FOOTER` 判据 + `.agent-sync` 同步，全量 `--check` 通过）
**Area**: shared checker / P6 副本一致（C 族）

### Summary
分册模式下每章文件底部有一行导航尾行 `> 📖 返回总览：…`。共享校验器
`note-citation-check.py` 的 `FOOTER` 只认 `## 参考/相关文档`，把该行当**正文**，于是
`--vault-note` 逐章报 `行数 119 vs 121` 之类的 1 处差异——**校验器假阳性**，产物本身正确。

### Error
```
[C] … 发现 1 处差异（行数 119 vs 121）    # 7 章一致复现，每章都停在同一行
```

### Context
- 触发场景：拆分多文件发布（每章带 callout 导航尾行），C 族拿 vault 成品与章节源比对。
- 根因：判据（装饰 / 页脚识别）没覆盖这种新布局形态——与「校验器必须覆盖每种布局」同类。
- 假阳性与假阴性同为缺陷：C 误报会逼人给**正确的**产物打 waiver，久了门就废了。

### 修复
- 改 canonical `.codex/scripts/note-citation-check.py`：
  `FOOTER = re.compile(r"^(?:## (参考文档|相关文档|参考资料)|>\s*📖)")`。
- `.agent-sync --apply --scope scripts` 同步到 `.claude/scripts/`，全量 `--check` 通过；
  复跑 7 章 `--vault-note` 全 EXIT=0（C 0 差异，compared 8 组）。

### 预防措施
- 出现一种新布局形态（导航尾行、新装饰行）时，先问「校验器的**装饰 / 页脚判据**认不认它」，
  认不出就补判据（RULES「Do」第 38 条），**不要**改用 waiver 或临场删行来迁就校验器。

---
