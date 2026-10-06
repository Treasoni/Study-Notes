#!/usr/bin/env python3
"""P6 拆分发布：output/final_note.md -> vault 子目录（索引页 + 10 章 + 附录）。

硬约束（来自 note-beautifier 的「分册 / 长文档发布」自检节）：
- 每个成品文件的正文与其源章节**逐字一致**（仅允许标题层级提升），脚本断言。
- 文件名的生成侧与校验侧共用**同一个** FILES 列表。
- 导航双链目标**逐条断言存在**后才写盘。
- 不覆盖已存在的成品文件。

标题层级规则：
- 章节文件：`## 第 N 章` -> `# 第 N 章`；`###` -> `##`；`####` -> `###`。
- 附录文件：新增 `# 附录`；两个 `## 附录 X` 保持 H2。
- 代码围栏内的 `#` 注释不参与层级调整。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "output", "final_note.md")
VAULT = r"D:\Study-Notes"
OUTDIR = os.path.join(VAULT, "自建代理节点", "VPS 自建节点零基础全流程")
DATE = "2026-09-24"
PROJECT = "vps-node-panel-tutorial"
INDEX = "00 VPS 自建节点零基础全流程"

TAGS = ["自建节点", "代理", "VPS", "3x-ui", "网络", "学习"]

# 顺序即 nav 顺序；(文件名, 一句话说明)
CHAPTERS = [
    ("01 VPS、节点、机场是什么", "四层关系、ECS 与 VPS 的对应、买到的资源项、机场是什么"),
    ("02 四种协议与 3x-ui 面板定位", "VLESS / VMess / Trojan / Shadowsocks 各自必须配合什么，面板站在哪一层"),
    ("03 购买 VPS（三家厂商对照）", "RackNerd / CloudCone / 搬瓦工，档位、计费周期与选机维度"),
    ("04 登录 VPS（SSH 与 FinalShell）", "SSH 认证的是什么、默认端口、首次登录的高频卡点"),
    ("05 安装面板 3x-ui 与放行端口", "一键脚本 vs Docker、随机凭据 vs 默认口令、端口放行"),
    ("06 搭建节点（面板入站）", "按字段顺序建第一个节点：协议、端口、凭据、传输安全"),
    ("07 搭建节点（带域名与 Cloudflare）", "橙云与灰云、代理资格限制、pending 期的源站 IP 风险"),
    ("08 使用节点（客户端导入与连通自检）", "订阅链接与分享链接、分层自检顺序"),
    ("09 节点被墙的判定与换 IP（分厂商分操作）", "经验性判定路径，DigitalOcean 与 Vultr 的换 IP 语义差异"),
    ("10 安全事项与最小加固", "SSH 加固、fail2ban、面板侧最小动作"),
]
APPENDIX = ("99 附录 速查表与内容边界", "命令与端口速查，以及本篇的内容边界")


def fail(msg):
    print(f"PUBLISH-FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def load_blocks():
    t = io.open(SRC, encoding="utf-8").read()
    parts = re.split(r"(?m)^(?=## )", t)
    preamble = parts[0].strip("\n")
    blocks = {}
    order = []
    for b in parts[1:]:
        title = b.splitlines()[0][3:].strip()
        # 组装时的块间分隔符 `---` 会挂到上一块尾部，这里剥掉，避免成品章尾出现双分隔线
        b = re.sub(r"(?:\n+-{3,}\s*)+$", "", b)
        blocks[title] = b.strip("\n")
        order.append(title)
    return preamble, blocks, order


def promote(body, chapter_title, is_appendix=False):
    """按规则提升标题层级；返回 (新正文, 提升计数 dict)。代码围栏内不动。"""
    out, fence, counts = [], False, {"h2": 0, "h3": 0, "h4": 0}
    for line in body.split("\n"):
        if line.startswith("```"):
            fence = not fence
            out.append(line)
            continue
        if not fence:
            if is_appendix:
                pass  # 附录：H2 保持，H3 保持，H1 由调用方补
            elif line.startswith("#### "):
                out.append("### " + line[5:]); counts["h4"] += 1; continue
            elif line.startswith("### "):
                out.append("## " + line[4:]); counts["h3"] += 1; continue
            elif line.startswith("## "):
                out.append("# " + line[3:]); counts["h2"] += 1; continue
        out.append(line)
    if fence:
        fail(f"{chapter_title}: 代码围栏未闭合")
    return "\n".join(out), counts


def vault_names():
    """Obsidian 按文件名全库解析 [[X]]。收集 vault 内所有 md 的 stem（跳过点目录）。"""
    names = set()
    for dirpath, dirnames, filenames in os.walk(VAULT):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".md"):
                names.add(fn[:-3])
    return names


def clean_previous(expected):
    """幂等：只删本脚本预期产出的文件；出现任何外来 md 一律失败退出。"""
    if not os.path.isdir(OUTDIR):
        return 0
    removed = 0
    for fn in sorted(os.listdir(OUTDIR)):
        if not fn.endswith(".md"):
            fail(f"目标目录出现非 md 文件: {fn}")
        if fn[:-3] not in expected:
            fail(f"目标目录出现非预期文件，拒绝删除: {fn}")
        os.remove(os.path.join(OUTDIR, fn))
        removed += 1
    return removed


def strip_heads(text):
    """去掉行首标题标记，用于「内容逐字一致」断言。"""
    out, fence = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            fence = not fence
        if not fence:
            line = re.sub(r"^#{1,6}\s*", "", line)
        out.append(line)
    return "\n".join(out).strip()


def fm(title, extra=None):
    lines = ["---", f'title: "{title}"', "tags:"] + [f"  - {t}" for t in TAGS]
    lines += [f"created: {DATE}", f"updated: {DATE}", "status: 完成",
              f"source_project: {PROJECT}"]
    if extra:
        lines += extra
    lines += ["---", ""]
    return "\n".join(lines)


def nav(prev, nxt):
    bits = []
    bits.append(f"上一篇：[[{prev}]]" if prev else "上一篇：—")
    bits.append(f"返回索引：[[{INDEX}]]")
    bits.append(f"下一篇：[[{nxt}]]" if nxt else "下一篇：—")
    return "> " + " ｜ ".join(bits)


def main():
    preamble, blocks, order = load_blocks()

    ch_titles = [t for t in order if re.match(r"^第 \d+ 章", t)]
    ap_titles = [t for t in order if t.startswith("附录")]
    if len(ch_titles) != 10:
        fail(f"期望 10 章，实际 {len(ch_titles)}: {ch_titles}")
    if len(ap_titles) != 2:
        fail(f"期望 2 个附录块，实际 {len(ap_titles)}: {ap_titles}")

    files = [INDEX] + [n for n, _ in CHAPTERS] + [APPENDIX[0]]
    removed = clean_previous(set(files))
    if removed:
        print(f"清理上一轮产物 {removed} 个")
    os.makedirs(OUTDIR, exist_ok=True)

    written, total_han = [], 0

    # ---- 索引页 ----
    toc = "\n".join(f"- [[{n}]] — {d}" for n, d in CHAPTERS + [APPENDIX])
    idx = (
        fm("VPS 自建节点零基础全流程")
        + f"# VPS 自建节点零基础全流程\n\n"
        + "> [!abstract] 一句话\n"
        + "> 从买一台 VPS 到客户端可用，全程用 3x-ui 面板点选，不手写配置文件。\n\n"
        + "> [!warning] 关于来源\n"
        + "> 本篇以一条 YouTube 教程的章节顺序为骨架。**该视频无任何字幕轨**，"
        + "口播内容未被引用；正文事实性内容全部来自官方文档与一手研究，"
        + "每条论断行内标注来源 ID（形如 `（来源：A-5 | flow）`）。"
        + "价格、套餐、版本号以 2026-09-23 观测值为准。\n\n"
        + "## 目录\n\n" + toc + "\n\n"
        + "## 怎么读\n\n"
        + "- **零基础**：从第 1 章顺序读，第 3–8 章是能照着做的主线。\n"
        + "- **只要跑通**：直接跳第 3 章，遇到不懂的名词回第 1–2 章查。\n"
        + "- **已经搭好**：看第 9 章（被墙处置）与第 10 章（最小加固），速查表在附录。\n\n"
        + "## 相关\n\n"
        + "- [[自建代理节点 MOC]] — 本目录的分类索引\n"
    )
    p = os.path.join(OUTDIR, INDEX + ".md")
    io.open(p, "w", encoding="utf-8", newline="").write(idx)
    written.append(INDEX)
    total_han += len(re.findall(r"[一-鿿]", idx))

    # ---- 章节 ----
    for i, (fname, _) in enumerate(CHAPTERS):
        title = ch_titles[i]
        src_block = blocks[title]
        body, counts = promote(src_block, title)
        # 内容一致性断言（只允许标题层级变化）
        if strip_heads(body) != strip_heads(src_block):
            fail(f"{fname}: 正文内容与源章节不一致（非标题层级差异）")
        if counts["h2"] != 1:
            fail(f"{fname}: 期望恰好 1 个 H2 提升，实际 {counts['h2']}")
        prev = files[i - 1] if i > 0 else None
        nxt = files[i + 2] if i + 2 < len(files) else APPENDIX[0]
        doc = (fm(title, [f"chapter: {i + 1}"]) + body + "\n\n---\n\n"
               + nav(prev, nxt) + "\n")
        io.open(os.path.join(OUTDIR, fname + ".md"), "w",
                encoding="utf-8", newline="").write(doc)
        written.append(fname)
        total_han += len(re.findall(r"[一-鿿]", doc))
        print(f"  {fname}.md  H2->H1 {counts['h2']}  H3->H2 {counts['h3']}  "
              f"H4->H3 {counts['h4']}")

    # ---- 附录 ----
    ap_body = "\n\n".join(blocks[t] for t in ap_titles)
    ap_body, ap_counts = promote(ap_body, "附录", is_appendix=True)
    for t in ap_titles:
        if ap_body.count("## " + t) != 1:
            fail(f"附录小标题 {t} 在成品中不是恰好 1 次")
    i = len(CHAPTERS)
    doc = (fm("附录 速查表与内容边界") + "# 附录\n\n" + ap_body + "\n\n---\n\n"
           + nav(files[i], None) + "\n")
    io.open(os.path.join(OUTDIR, APPENDIX[0] + ".md"), "w",
            encoding="utf-8", newline="").write(doc)
    written.append(APPENDIX[0])
    total_han += len(re.findall(r"[一-鿿]", doc))

    # ---- 导航与链接校验 ----
    on_disk = {f[:-3] for f in os.listdir(OUTDIR) if f.endswith(".md")}
    if on_disk != set(files):
        fail(f"落盘文件名与预期不符: 多 {on_disk - set(files)} 少 {set(files) - on_disk}")
    global_names = vault_names()
    bad = []
    for f in files:
        body = io.open(os.path.join(OUTDIR, f + ".md"), encoding="utf-8").read()
        for lk in re.findall(r"\[\[([^\]]+)\]\]", body):
            if lk.startswith("#"):
                bad.append((f, lk, "裸锚点，分册后无法解析"))
                continue
            target = lk.split("|")[0].strip()
            if target not in on_disk and target not in global_names:
                bad.append((f, lk, "目标不存在"))
    if bad:
        fail(f"存在无效链接: {bad}")

    print(f"\n发布目录 {OUTDIR}")
    print(f"文件 {len(written)} 个  中文字 {total_han}")
    print("链接校验：全部目标存在 ✓")


if __name__ == "__main__":
    main()
