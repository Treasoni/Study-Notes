#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一次性修正：把「docker cp 是必经步骤」的误导表述改对（绑定挂载下可跳过）。

范围（canonical 优先，下游机械回填）：
  1) chapters/02_docker-setup.md  —— 3 处（两处显式 docker cp 表述 + 出租屋比喻）
  2) chapters/03_enable-json.md   —— 3.1 收尾句、整节 3.3、新增脚注 c3-j/k/l
  3) chapters/_merged.md          —— 由 merge_files.py 重新生成（调用方负责）
  4) output/final_note.md         —— 同 1)2) 的替换 + 两处 SOURCE 标记字节数回填

每个替换都必须**恰好命中 1 次**，否则整脚本报错退出、不写任何文件。
"""
import pathlib
import re
import sys

ROOT = pathlib.Path("/Users/zhqznc/Documents/项目")
PROJ = ROOT / "workspace/searxng-hermes"

# ---------------------------------------------------------------- 替换文本

CH2_OLD_1 = "所以：**不要从零手写 `settings.yml`**。正确姿势是让容器先生成一份，再用 `docker cp` 把它取回来改——第 3 章开 JSON 就是干这件事。"
CH2_NEW_1 = "所以：**不要从零手写 `settings.yml`**。正确姿势是让容器先生成一份，再在宿主上直接改——第 3 章开 JSON 就是干这件事。"

CH2_OLD_2 = "> 路径② 的 `settings.yml` 生成在 `./searxng/core-config/settings.yml`，而路径① 生成在 `~/searxng/searxng/settings.yml`。后面的 `docker cp`、改 JSON 都按你实际用的那条路径来。"
CH2_NEW_2 = "> 路径② 的 `settings.yml` 生成在 `./searxng/core-config/settings.yml`，而路径① 生成在 `~/searxng/searxng/settings.yml`。这两个位置都在**宿主**上（配置目录已经挂进容器），所以第 3 章改 JSON 直接编辑对应文件即可，不用先把它从容器里复制出来。"

CH2_OLD_3 = "> 把容器想成**一间出租屋**：房东（镜像）入住前已经放好一份配置模板，你进屋第一件事不是从白纸写起，而是把这份模板拿出来、改两处、再放回去。"
CH2_NEW_3 = "> 把容器想成**一间出租屋**：房东（镜像）入住前已经放好一份配置模板，你进屋第一件事不是从白纸写起，而是把这份模板改两处、重启生效——而这份模板因为挂载，本来就摆在你宿主上。"

CH3_OLD_31 = "而且它改的是配置文件，不是重启个服务就行，得走「取回 → 改 → 写回 → 重启」四步。"
CH3_NEW_31 = "而且它改的是配置文件——得打开 `settings.yml` 改一行、再重启容器让它生效。"

CH3_OLD_33 = """### 3.3 照抄：取回 → 改 → 写回 → 重启

**第一步，把容器里生成的配置取回宿主**（容器名按你的实际来：路径① 是 `searxng`，路径② 是 `searxng-core`）：[^c3-d]

```bash
docker cp searxng:/etc/searxng/settings.yml ~/searxng/searxng/settings.yml
```

**第二步，在文件里追加这段覆盖块**——`search.formats` 同时保留 `html` 并加上 `json`：[^c3-e]

```yaml
search:
  formats:
    - html
    - json
```

**第三步，文件的完整样子应该类似下面这样**（`use_default_settings: true` + 一个 `server:` 块 + 刚加的 `search:` 块），只要结构对上即可：[^c3-f]

```yaml
# ~/searxng/searxng/settings.yml
use_default_settings: true

server:
  secret_key: "abcdef12345678"
  image_proxy: true

search:
  formats:
    - html
    - json
```

**第四步，写回容器并重启让它生效**：[^c3-g]

```bash
docker cp ~/searxng/searxng/settings.yml searxng:/etc/searxng/settings.yml
docker restart searxng
```"""

CH3_NEW_33 = """### 3.3 照抄：改配置 → 重启（本册两条路径都能省掉 `docker cp`）

> [!tip] 先说结论：本册两条路径都不用「取回 / 写回」
> 本册两条路径都把**宿主的一个目录挂到了容器的 `/etc/searxng/`**：路径① 挂的是 `~/searxng/searxng/`，路径② 挂的是 `./searxng/core-config/`。[^c3-j] 所以 `docker compose up -d` 起来之后，容器生成的那份 `settings.yml` **本来就落在你宿主上**——直接拿编辑器打开改就行，不需要先「取回来」。[^c3-k] 下面的 `docker cp` 只在**你没有把 `/etc/searxng` 挂到宿主**时才需要（那种情况下配置只活在容器里，复制出来改才不至于一重启就丢）。官方 Docker 安装文档里，路径② 的配置这步也是让你直接编辑 `core-config/settings.yml`，并没有 `docker cp`。[^c3-l]

**（可选）第一步，把容器里生成的配置取回宿主**——只有容器没把 `/etc/searxng` 挂到宿主时才需要（容器名按你的实际来：路径① 是 `searxng`，路径② 是 `searxng-core`）：[^c3-d]

```bash
docker cp searxng:/etc/searxng/settings.yml ~/searxng/searxng/settings.yml
```

**第二步，在文件里追加这段覆盖块**——`search.formats` 同时保留 `html` 并加上 `json`：[^c3-e]

```yaml
search:
  formats:
    - html
    - json
```

**第三步，文件的完整样子应该类似下面这样**（`use_default_settings: true` + 一个 `server:` 块 + 刚加的 `search:` 块），只要结构对上即可：[^c3-f]

```yaml
# ~/searxng/searxng/settings.yml
use_default_settings: true

server:
  secret_key: "abcdef12345678"
  image_proxy: true

search:
  formats:
    - html
    - json
```

**第四步，让它生效**——两条路径的配置文件已经是同一份，重启容器即可；只有你**真的**在第一步用 `docker cp` 把文件取出来过（未挂载的情况），才需要先写回、再重启：[^c3-g]

```bash
# 仅在未挂载、且前面确实用 docker cp 取出过时才需要这一行：
docker cp ~/searxng/searxng/settings.yml searxng:/etc/searxng/settings.yml
docker restart searxng
```"""

CH3_OLD_FN = "[^c3-i]: Search API 未设 format 返回 403，且许多公共实例禁用（`l2-6_search_api.html:444-448`）"
CH3_NEW_FN = """[^c3-i]: Search API 未设 format 返回 403，且许多公共实例禁用（`l2-6_search_api.html:444-448`）
[^c3-j]: 两条路径都把宿主目录挂到容器 `/etc/searxng`：路径① `l3-1_web-search.md:170-173`（`./searxng:/etc/searxng:rw`）；路径② `l2-2_container-docker-compose.yml:14-15`（`./core-config/:/etc/searxng/:Z`）
[^c3-k]: 首启会把模板生成进配置目录（`l2-9_entrypoint.sh:80-93`）——该目录正是挂载点，故生成物直接落在宿主
[^c3-l]: SearXNG 官方 Docker 安装文档 · 配置这步直接编辑宿主文件（`l2-1_installation-docker.html:527`）"""

# (文件名, [(old, new), ...])
PLAN = {
    "chapters/02_docker-setup.md": [
        (CH2_OLD_1, CH2_NEW_1),
        (CH2_OLD_2, CH2_NEW_2),
        (CH2_OLD_3, CH2_NEW_3),
    ],
    "chapters/03_enable-json.md": [
        (CH3_OLD_31, CH3_NEW_31),
        (CH3_OLD_33, CH3_NEW_33),
        (CH3_OLD_FN, CH3_NEW_FN),
    ],
    "output/final_note.md": [
        (CH2_OLD_1, CH2_NEW_1),
        (CH2_OLD_2, CH2_NEW_2),
        (CH2_OLD_3, CH2_NEW_3),
        (CH3_OLD_31, CH3_NEW_31),
        (CH3_OLD_33, CH3_NEW_33),
        (CH3_OLD_FN, CH3_NEW_FN),
    ],
}

MARK = re.compile(r"^<!-- SOURCE: (\S+) \| \d+ bytes -->$")


def check_all():
    """先全量预检：任一 old 在某目标文件里命中数 != 1 就报错。"""
    bad = []
    for rel, pairs in PLAN.items():
        p = PROJ / rel
        t = p.read_text(encoding="utf-8")
        for k, (old, new) in enumerate(pairs, 1):
            n = t.count(old)
            if n != 1:
                bad.append("%s 第 %d 条命中 %d 次（应为 1）" % (rel, k, n))
    return bad


def apply_plan():
    total = 0
    for rel, pairs in PLAN.items():
        p = PROJ / rel
        t = p.read_text(encoding="utf-8")
        n_file = 0
        for old, new in pairs:
            t = t.replace(old, new, 1)
            n_file += 1
        p.write_text(t, encoding="utf-8")
        print("  %-32s 改动 %d 处" % (rel, n_file))
        total += n_file
    return total


def fix_markers():
    """回填 final_note.md 里 SOURCE 标记的字节数（= 对应章文件的真实大小）。"""
    fn = PROJ / "output/final_note.md"
    lines = fn.read_text(encoding="utf-8").split("\n")
    sizes = {}
    for ch in (PROJ / "chapters").glob("0*_*.md"):
        sizes[ch.name] = len(ch.read_text(encoding="utf-8").encode("utf-8"))
    n = 0
    for i, l in enumerate(lines):
        m = MARK.match(l)
        if m and m.group(1) in sizes:
            want = "<!-- SOURCE: %s | %d bytes -->" % (m.group(1), sizes[m.group(1)])
            if l != want:
                print("  标记 %s: %s → %s" % (m.group(1), l, want))
                lines[i] = want
                n += 1
    fn.write_text("\n".join(lines), encoding="utf-8")
    return n


def main():
    step = sys.argv[1] if len(sys.argv) > 1 else "apply"
    if step == "check":
        bad = check_all()
        if bad:
            print("❌ 预检未通过（不写任何文件）：")
            for b in bad:
                print("  -", b)
            return 1
        print("✅ 预检通过：全部 old 串在目标文件里各命中 1 次")
        return 0
    if step == "apply":
        bad = check_all()
        if bad:
            print("❌ 预检未通过，未写任何文件：")
            for b in bad:
                print("  -", b)
            return 1
        total = apply_plan()
        print("→ 正文替换合计 %d 处" % total)
        n = fix_markers()
        print("→ SOURCE 标记回填 %d 处" % n)
        return 0
    print("用法: apply_bindmount_fix.py [check|apply]")
    return 2


if __name__ == "__main__":
    sys.exit(main())
