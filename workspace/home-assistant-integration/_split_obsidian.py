# -*- coding: utf-8 -*-
"""Split final_note.md into Obsidian chapter files + index page."""
import os

SRC = r"workspace/home-assistant-integration/output/final_note.md"
DEST_DIR = r"homeassistant/ha-integration"

# (chapter start line 1-indexed, filename, title)
CHAPTERS = [
    (19,   "01_认识HomeAssistant自定义集成.md", "第 1 章：认识 Home Assistant 自定义集成"),
    (101,  "02_开发环境搭建.md", "第 2 章：开发环境搭建"),
    (230,  "03_集成骨架与manifest.md", "第 3 章：集成骨架与 manifest.json"),
    (418,  "04_ConfigFlow配置流程.md", "第 4 章：Config Flow 配置流程"),
    (730,  "05_Entity平台与Sensor实体.md", "第 5 章：Entity 平台与 Sensor 实体"),
    (928,  "06_DataUpdateCoordinator数据轮询.md", "第 6 章：DataUpdateCoordinator 数据轮询"),
    (1249, "07_测试与调试.md", "第 7 章：测试与调试"),
    (1465, "08_HACS分发.md", "第 8 章：HACS 分发"),
    (1614, "09_常见坑与最佳实践.md", "第 9 章：常见坑与最佳实践"),
]

INDEX_NAME = "HA集成开发指南.md"

with open(SRC, encoding="utf-8") as f:
    lines = f.readlines()

total_lines = len(lines)
starts = [c[0] for c in CHAPTERS]
ends = starts[1:] + [total_lines + 1]

os.makedirs(DEST_DIR, exist_ok=True)


def frontmatter(title, tags):
    tag_block = "\n".join(f"  - {t}" for t in tags)
    return (
        "---\n"
        f'title: "{title}"\n'
        "tags:\n"
        f"{tag_block}\n"
        "created: 2026-08-08\n"
        "updated: 2026-08-08\n"
        "status: 完成\n"
        "source_project: home-assistant-integration\n"
        "---\n\n"
    )


def nav(prev, nxt):
    parts = []
    if prev:
        parts.append(f"[[{prev}|⬅️ 上一章]]")
    parts.append("[[HA集成开发指南|📑 目录]]")
    if nxt:
        parts.append(f"[[{nxt}|下一章 ➡️]]")
    return "> " + " | ".join(parts) + "\n\n"


for i, (start, fname, title) in enumerate(CHAPTERS):
    content = "".join(lines[start - 1: ends[i] - 1]).rstrip() + "\n"
    prev_name = CHAPTERS[i - 1][1].replace(".md", "") if i > 0 else None
    nxt_name = CHAPTERS[i + 1][1].replace(".md", "") if i < len(CHAPTERS) - 1 else None
    nav_line = nav(prev_name, nxt_name)
    tags = ["HomeAssistant", "集成开发", "学习笔记"]
    out = frontmatter(title, tags) + nav_line + content + "\n---\n\n" + nav_line
    with open(os.path.join(DEST_DIR, fname), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"wrote {fname}  ({len(content)} chars body)")

# ---- index page ----
index_title = "从零开发 Home Assistant 自定义集成"
index_tags = ["HomeAssistant", "集成开发", "学习笔记", "MOC"]
index_body = frontmatter(index_title, index_tags) + f"""# {index_title}（custom integration）

> [!summary] 本指南
> 面向会 Python + async/await、用过 HA 的读者，从零开发一个**可运行、可 HACS 分发**的 Home Assistant 自定义集成。主线终点：一个带 config flow + sensor + DataUpdateCoordinator + HACS 分发的最小集成。

## 📚 目录

| 章节 | 内容 | 篇幅 |
|------|------|------|
| [[01_认识HomeAssistant自定义集成\\|第 1 章：认识自定义集成]] | 概念 + 生态位置 + 学习路径总览 | 短 |
| [[02_开发环境搭建\\|第 2 章：开发环境搭建]] | Dev Container + 本地 venv + 官方脚手架 | 中 |
| [[03_集成骨架与manifest\\|第 3 章：集成骨架与 manifest.json]] | 目录结构 + manifest 核心字段 | 中 |
| [[04_ConfigFlow配置流程\\|第 4 章：Config Flow 配置流程]] | 表单流程 + 唯一性 + 异常语义 | 长 |
| [[05_Entity平台与Sensor实体\\|第 5 章：Entity 平台与 Sensor 实体]] | 实体状态机 + 声明式 SensorEntityDescription | 中 |
| [[06_DataUpdateCoordinator数据轮询\\|第 6 章：DataUpdateCoordinator 数据轮询]] | 统一轮询 + 异常映射 + 独立 API 库封装 | 长 |
| [[07_测试与调试\\|第 7 章：测试与调试]] | pytest-homeassistant-custom-component + debugpy + logger | 中 |
| [[08_HACS分发\\|第 8 章：HACS 分发]] | hacs.json + hassfest/hacs Action + Release | 短 |
| [[09_常见坑与最佳实践\\|第 9 章：常见坑与最佳实践]] | 10 坑 + 7 实践，排错手册收尾 | 中 |

> [!tip] 建议阅读顺序
> 按第 1 → 9 章顺序阅读；**第 4、6 章是重点**，值得放慢速度。

## 🎯 学完能做什么

- 用 Dev Container 一键搭好开发环境，F5 断点调试
- 读懂并手写合法的 `manifest.json`
- 用官方脚手架生成骨架 + 实现 config flow 配置流程
- 用 DataUpdateCoordinator 轮询外部 API，暴露 sensor 实体
- 用 pytest 写测试，用 debugpy/logger 定位问题
- 走通 HACS 分发，让集成可被一键安装

---
> [[01_认识HomeAssistant自定义集成|开始第 1 章 ➡️]]
"""
with open(os.path.join(DEST_DIR, INDEX_NAME), "w", encoding="utf-8") as f:
    f.write(index_body)
print(f"wrote {INDEX_NAME}")
print("DONE")
