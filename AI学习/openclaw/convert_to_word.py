#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 数字人商业调查 - Markdown 转 Word (美化版)
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
import re
from pathlib import Path

def setup_styles(doc):
    """设置文档样式"""

    # 默认字体
    doc.styles['Normal'].font.name = '微软雅黑'
    doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    doc.styles['Normal'].font.size = Pt(11)
    doc.styles['Normal'].paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    doc.styles['Normal'].paragraph_format.space_after = Pt(6)

    # 标题 1
    title1 = doc.styles['Heading 1']
    title1.font.name = '微软雅黑'
    title1._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    title1.font.size = Pt(18)
    title1.font.bold = True
    title1.font.color.rgb = RGBColor(0, 51, 102)
    title1.paragraph_format.space_before = Pt(18)
    title1.paragraph_format.space_after = Pt(12)
    title1.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    # 标题 2
    title2 = doc.styles['Heading 2']
    title2.font.name = '微软雅黑'
    title2._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    title2.font.size = Pt(15)
    title2.font.bold = True
    title2.font.color.rgb = RGBColor(0, 76, 153)
    title2.paragraph_format.space_before = Pt(14)
    title2.paragraph_format.space_after = Pt(10)
    title2.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    # 标题 3
    title3 = doc.styles['Heading 3']
    title3.font.name = '微软雅黑'
    title3._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    title3.font.size = Pt(13)
    title3.font.bold = True
    title3.font.color.rgb = RGBColor(51, 102, 153)
    title3.paragraph_format.space_before = Pt(12)
    title3.paragraph_format.space_after = Pt(8)
    title3.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    # 标题 4
    title4 = doc.styles['Heading 4']
    title4.font.name = '微软雅黑'
    title4._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    title4.font.size = Pt(12)
    title4.font.bold = True
    title4.font.color.rgb = RGBColor(51, 102, 153)
    title4.paragraph_format.space_before = Pt(10)
    title4.paragraph_format.space_after = Pt(6)

    return doc

def add_cover_page(doc):
    """添加封面页"""
    # 封面不需要分页，后面内容会自然跟随

    # 标题
    title = doc.add_paragraph('OpenClaw 数字人商业调查')
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title.runs[0]
    title_run.font.size = Pt(26)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(0, 51, 102)
    title_run.font.name = '微软雅黑'

    # 副标题
    subtitle = doc.add_paragraph('基于 2026 年 2 月最新资料')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle_run = subtitle.runs[0]
    subtitle_run.font.size = Pt(14)
    subtitle_run.font.color.rgb = RGBColor(100, 100, 100)
    subtitle_run.font.name = '微软雅黑'

    # 空行
    for _ in range(3):
        doc.add_paragraph('')

    # 文档信息
    info_paragraph = doc.add_paragraph()
    info_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info_text = (
        f'更新时间：2026年2月25日\n'
        f'文档版本：v1.0.0\n'
        f'维护者：OpenClaw 中文社区\n'
        f'资料来源：阿里云开发者社区、CSDN、掘金、OpenClaw 官方文档'
    )
    info_run = info_paragraph.runs[0] if info_paragraph.runs else info_paragraph.add_run(info_text)
    info_run.font.size = Pt(11)
    info_run.font.color.rgb = RGBColor(80, 80, 80)

    # 分页
    doc.add_page_break()

def parse_markdown_to_doc(md_file, docx_file):
    """解析 Markdown 文件并生成格式化的 Word 文档"""

    # 读取 Markdown 文件
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 创建文档
    doc = Document()

    # 设置页面
    sections = doc.sections
    for section in sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

    # 设置样式
    doc = setup_styles(doc)

    # 添加封面
    add_cover_page(doc)

    # 添加目录页
    toc = doc.add_paragraph('目录')
    toc.style = 'Heading 1'
    doc.add_paragraph('（请在 Word 中手动更新目录：右键目录 → 更新域 → 更新整个目录）')
    doc.add_paragraph('')
    doc.add_page_break()

    # 解析 Markdown 内容
    lines = content.split('\n')
    in_code_block = False
    in_table = False
    table_rows = []
    in_callout = False
    callout_type = None
    in_details = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # 代码块处理
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_lang = line.strip()[3:].strip() or 'text'
            else:
                in_code_block = False
            i += 1
            continue

        if in_code_block:
            p = doc.add_paragraph(line.strip())
            for run in p.runs:
                run.font.name = 'Consolas'
                run.font.size = Pt(9)
            p.paragraph_format.left_indent = Inches(0.5)
            p.paragraph_format.line_spacing = 1.0
            i += 1
            continue

        # 详情标签处理
        if line.strip().startswith('<details>'):
            in_details = True
            i += 1
            continue
        if line.strip().startswith('</details>'):
            in_details = False
            i += 1
            continue
        if line.strip().startswith('<summary>'):
            # 提取摘要文本
            summary_text = line.replace('<summary>', '').replace('</summary>', '').replace('<b>', '').replace('</b>', '')
            p = doc.add_paragraph(summary_text)
            p.runs[0].font.bold = True
            p.runs[0].font.color.rgb = RGBColor(0, 76, 153)
            i += 1
            continue

        # 标注处理
        if line.strip().startswith('%%'):
            i += 1
            continue

        # Callout 处理
        if line.strip().startswith('> [!'):
            match = re.search(r'\[!(\w+)\](?:\s+(.+))?', line)
            if match:
                callout_type = match.group(1)
                title_text = match.group(2) if match.group(2) else ''

                # 根据类型设置颜色
                color_map = {
                    'note': (51, 102, 153),
                    'tip': (0, 102, 51),
                    'important': (153, 51, 0),
                    'warning': (153, 102, 0),
                    'danger': (153, 0, 0),
                    'success': (0, 102, 0),
                    'info': (0, 76, 153),
                    'summary': (51, 102, 153),
                    'question': (153, 102, 0),
                    'example': (102, 51, 153),
                }

                title_map = {
                    'note': '注意',
                    'tip': '提示',
                    'important': '重要',
                    'warning': '警告',
                    'danger': '危险',
                    'success': '成功',
                    'info': '信息',
                    'summary': '摘要',
                    'question': '问题',
                    'example': '示例',
                }

                color = color_map.get(callout_type, (80, 80, 80))
                display_title = title_map.get(callout_type, callout_type.upper())

                p = doc.add_paragraph()
                if title_text:
                    p.add_run(f'{display_title}：{title_text}')
                else:
                    p.add_run(display_title)

                run = p.runs[0]
                run.font.bold = True
                run.font.size = Pt(11)
                run.font.color.rgb = RGBColor(*color)
                p.paragraph_format.left_indent = Inches(0.25)
                p.paragraph_format.top_space = Pt(8)
                p.paragraph_format.bottom_space = Pt(4)
            i += 1
            continue

        # 引用块（普通 > 开头）
        if line.strip().startswith('> ') and not line.strip().startswith('> [!'):
            p = doc.add_paragraph(line.strip()[2:])
            p.runs[0].font.color.rgb = RGBColor(80, 80, 80)
            p.runs[0].font.italic = True
            p.paragraph_format.left_indent = Inches(0.5)
            i += 1
            continue

        # 标题处理
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            if level <= 4:
                title_text = line.lstrip('#').strip()
                heading = doc.add_heading(title_text, level=level)
                i += 1
                continue

        # 表格处理
        if '|' in line and line.strip():
            if not in_table:
                in_table = True
                table_rows = []

            # 跳过分隔行
            if re.match(r'^\|[\s\-:]+\|$', line.strip()):
                i += 1
                continue

            # 解析表格行
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            table_rows.append(cells)
            i += 1

            # 检查是否还有更多表格行
            if i < len(lines) and '|' in lines[i] and not lines[i].strip().startswith('```'):
                continue

            # 创建表格
            if table_rows:
                table = doc.add_table(rows=len(table_rows), cols=len(table_rows[0]))
                table.style = 'Light Grid Accent 1'

                for row_idx, row_data in enumerate(table_rows):
                    row = table.rows[row_idx]
                    for col_idx, cell_data in enumerate(row_data):
                        cell = row.cells[col_idx]
                        cell.text = cell_data

                        # 设置单元格格式
                        for paragraph in cell.paragraphs:
                            paragraph.paragraph_format.space_before = Pt(2)
                            paragraph.paragraph_format.space_after = Pt(2)
                            for run in paragraph.runs:
                                run.font.size = Pt(10)
                                run.font.name = '微软雅黑'
                                if row_idx == 0:  # 表头
                                    run.font.bold = True
                                    run.font.color.rgb = RGBColor(255, 255, 255)

                table.autofit = False
                for row in table.rows:
                    for cell in row.cells:
                        cell.width = Inches(1.5)

                table_rows = []
                in_table = False
            continue

        # 列表处理
        list_match = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.+)', line)
        if list_match:
            indent, marker, text = list_match.groups()
            level = len(indent) // 2
            p = doc.add_paragraph(text, style='List Bullet')
            p.paragraph_format.left_indent = Inches(0.25 * (level + 1))
            i += 1
            continue

        # 任务列表
        task_match = re.match(r'^\s*-\s*\[([ x])\]\s*(.+)', line)
        if task_match:
            checked, text = task_match.groups()
            p = doc.add_paragraph()
            checkbox = '☑ ' if checked == 'x' else '☐ '
            p.add_run(checkbox).font.size = Pt(12)
            p.add_run(text).font.size = Pt(11)
            p.paragraph_format.left_indent = Inches(0.5)
            i += 1
            continue

        # 水平线
        if line.strip() in ['---', '***', '___']:
            p = doc.add_paragraph('_' * 80)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.color.rgb = RGBColor(150, 150, 150)
            i += 1
            continue

        # 空行
        if not line.strip():
            doc.add_paragraph('')
            i += 1
            continue

        # 普通段落
        if line.strip():
            p = doc.add_paragraph(line.strip())

            # 检查并处理加粗、斜体、高亮、代码等
            for run in p.runs:
                run.font.name = '微软雅黑'
                run.font.size = Pt(11)

            # 处理内联格式
            text = line.strip()
            if '**' in text or '==' in text or '`' in text:
                p.clear()

                # 简单处理：分割并添加格式
                parts = re.split(r'(\*\*[^*]+\*\*|==[^=]+==|`[^`]+`)', text)
                for part in parts:
                    if not part:
                        continue

                    if part.startswith('**') and part.endswith('**'):
                        run = p.add_run(part[2:-2])
                        run.font.bold = True
                    elif part.startswith('==') and part.endswith('=='):
                        from docx.oxml import OxmlElement
                        run = p.add_run(part[2:-2])
                        run.font.highlight_color = 7  # Yellow
                    elif part.startswith('`') and part.endswith('`'):
                        run = p.add_run(part[1:-1])
                        run.font.name = 'Consolas'
                        run.font.size = Pt(10)
                        run.font.color.rgb = RGBColor(163, 21, 21)
                    else:
                        run = p.add_run(part)

                    run.font.size = Pt(11)
                    run.font.name = '微软雅黑'

        i += 1

    # 保存文档
    doc.save(docx_file)
    print(f'✅ Word 文档已生成：{docx_file}')
    print(f'📄 包含内容：')
    print(f'   - 专业封面页')
    print(f'   - 自动目录（需在 Word 中更新）')
    print(f'   - 格式化的标题和段落')
    print(f'   - 美化的表格')
    print(f'   - 彩色提示框')
    print(f'   - 代码高亮')

if __name__ == '__main__':
    md_file = '/Users/zhqznc/Documents/项目/AI学习/openclaw/OpenClaw数字人商业调查.md'
    docx_file = '/Users/zhqznc/Documents/项目/AI学习/openclaw/OpenClaw数字人商业调查.docx'

    parse_markdown_to_doc(md_file, docx_file)
