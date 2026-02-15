# Marker PDF 转换教学案例

## 案例概述

本案例演示如何使用 Marker 工具将 PDF 文档转换为高质量的 Markdown 格式，适用于学术论文、电子书籍、技术文档等场景。

---

## 实际案例记录

### 案例：张宇高等数学基础30讲 PDF 转换

**转换信息**：
- **输入文件**：`/Users/zhqznc/Documents/27张宇基础30讲高数.pdf`
- **输出文件**：`/Users/zhqznc/Documents/27张宇基础30讲高数.md`
- **转换命令**：
```bash
marker_single /Users/zhqznc/Documents/27张宇基础30讲高数.pdf \
  --force_ocr \
  --output_format markdown
```

**命令参数说明**：
- `--force_ocr`：强制使用 OCR 识别（适用于扫描型或图片型 PDF）
- `--output_format markdown`：指定输出格式为 Markdown


**输出位置**：
- 默认情况下，Marker 在输入文件所在目录生成同名 `.md` 文件
- 即：`/Users/zhqznc/Documents/27张宇基础30讲高数.md`

---

## 第一步：环境准备

### 1.1 安装 Marker

```bash
# 基本安装
pip install marker-pdf

# 支持所有文件类型（推荐）
pip install marker-pdf[full]
```

### 1.2 安装系统依赖（macOS）

```bash
# 安装 Tesseract OCR 引擎
brew install tesseract

# 安装 Poppler（PDF 处理库）
brew install poppler
```

---

## 第二步：首次运行（模型下载）

### 2.1 准备测试 PDF

将你要转换的 PDF 文件放在合适的位置，例如：
```
/Users/zhqznc/Documents/项目/测试文档.pdf
```

### 2.2 首次转换（自动下载模型）

```bash
# 进入 PDF 所在目录
cd /Users/zhqznc/Documents/项目

# 执行转换
marker_single 测试文档.pdf
```

**首次运行时会自动下载模型**：
- 下载大小：约 2-3GB
- 下载位置：`~/.cache/huggingface/`
- 下载时间：根据网速，通常需要几分钟

**预期输出**：
```
Downloading models...
[========================================] 100%
Models downloaded successfully!
Converting test.pdf...
```

---

## 第三步：基本转换操作

### 3.1 简单转换（推荐新手）

```bash
# 转换单个 PDF
marker_single 测试文档.pdf

# 输出：测试文档.md（默认在同一目录）
```

### 3.2 指定输出目录

```bash
# 创建输出目录
mkdir -p /Users/zhqznc/Documents/项目/markdown_output

# 转换并指定输出目录
marker_single 测试文档.pdf --output_dir /Users/zhqznc/Documents/项目/markdown_output
```

### 3.3 指定页面范围

```bash
# 只转换第 1 页、第 6-10 页、第 21 页
marker_single 测试文档.pdf --page_range "0,5-10,20"
```

> **注意**：页面索引从 0 开始

---

## 第四步：进阶功能

### 4.1 使用 LLM 提升转换质量

当 PDF 包含复杂的表格、公式或布局时，使用 LLM 可以显著提升转换准确率。

**使用 Gemini API**（默认，免费额度较大）：
```bash
# 获取 Gemini API Key：https://aistudio.google.com/app/apikey

marker_single 测试文档.pdf \
  --use_llm \
  --gemini_api_key YOUR_GEMINI_API_KEY
```

**使用 Claude API**：
```bash
marker_single 测试文档.pdf \
  --use_llm \
  --llm_service marker.services.claude.ClaudeService \
  --claude_api_key YOUR_CLAUDE_API_KEY \
  --claude_model_name claude-3-5-sonnet
```

**使用 Ollama 本地模型**（完全免费）：
```bash
# 首先安装 Ollama: https://ollama.ai

marker_single 测试文档.pdf \
  --use_llm \
  --llm_service marker.services.ollama.OllamaService \
  --ollama_model llama3 \
  --ollama_base_url http://localhost:11434
```

### 4.2 强制 OCR 处理

对于扫描型 PDF 或图片型 PDF，需要强制使用 OCR：

```bash
# 对整篇文档进行 OCR
marker_single 测试文档.pdf --force_ocr

# 移除现有 OCR 并重新处理
marker_single 测试文档.pdf --strip_existing_ocr
```

### 4.3 高质量数学公式转换

```bash
# 需要 --use_llm 支持
marker_single 测试文档.pdf \
  --use_llm \
  --redo_inline_math \
  --gemini_api_key YOUR_KEY
```

---

## 第五步：批量转换

### 5.1 转换整个文件夹

```bash
# 准备：将所有 PDF 放在一个文件夹中
mkdir -p pdf_input
# 将多个 PDF 文件移动到 pdf_input 目录

# 批量转换
marker /Users/zhqznc/Documents/项目/pdf_input \
  --output_dir /Users/zhqznc/Documents/项目/markdown_output
```

### 5.2 多线程批量转换

```bash
# 使用 4 个工作线程
marker /path/to/pdfs --workers 4
```

---

## 第六步：输出格式选择

### 6.1 支持的输出格式

| 格式 | 参数 | 适用场景 |
|------|------|----------|
| Markdown | `markdown` | 默认格式，易读易编辑 |
| JSON | `json` | 程序处理、结构化数据 |
| HTML | `html` | 网页展示 |
| Chunks | `chunks` | RAG 检索、知识库构建 |

### 6.2 使用示例

```bash
# 输出为 JSON
marker_single 测试文档.pdf --output_format json

# 输出为 HTML
marker_single 测试文档.pdf --output_format html

# 按页编号输出
marker_single 测试文档.pdf --paginate_output
```

---

## 第七步：使用 Python API

### 7.1 基本用法

```python
from marker.convert import convert_single_pdf
from marker.models import load_all_models

# 加载模型（首次会自动下载）
model_list = load_all_models()

# 转换 PDF
full_text, images, out_meta = convert_single_pdf(
    "测试文档.pdf",
    model_list,
    max_pages=None,  # 全部页面
    parallel_factor=1  # 并行因子
)

# 保存结果
with open("输出.md", "w", encoding="utf-8") as f:
    f.write(full_text)

print("转换完成！")
```

### 7.2 批量处理脚本

```python
import os
from pathlib import Path
from marker.convert import convert_single_pdf
from marker.models import load_all_models

def batch_convert(input_dir, output_dir):
    """批量转换 PDF 文件夹"""

    # 加载模型
    print("正在加载模型...")
    model_list = load_all_models()

    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 遍历并转换
    for pdf_file in Path(input_dir).glob("*.pdf"):
        print(f"正在转换: {pdf_file.name}")

        try:
            full_text, images, out_meta = convert_single_pdf(
                str(pdf_file),
                model_list,
                max_pages=None
            )

            # 保存 Markdown
            output_file = Path(output_dir) / f"{pdf_file.stem}.md"
            output_file.write_text(full_text, encoding="utf-8")

            print(f"✓ 完成: {output_file.name}")

        except Exception as e:
            print(f"✗ 失败: {pdf_file.name} - {e}")

# 使用
batch_convert(
    "/Users/zhqznc/Documents/项目/pdf_input",
    "/Users/zhqznc/Documents/项目/markdown_output"
)
```

---

## 常见问题与解决方案

### Q1: 转换速度太慢

**解决方案**：
- 使用 GPU（自动检测，需安装 CUDA/MPS）
- 减少页面范围：`--page_range "0-10"`
- 使用多线程：`--workers 4`

### Q2: 表格转换不准确

**解决方案**：
- 使用 LLM 增强：`--use_llm`
- 强制布局检测：`--force_ocr`

### Q3: 中文内容显示乱码

**解决方案**：
- 确保安装了中文语言包的 Tesseract
- 强制 OCR：`--force_ocr`

### Q4: 内存不足

**解决方案**：
- 分批处理页面
- 减少并行因子：`parallel_factor=1`
- 关闭其他占用内存的程序

---

## 实用技巧

### 技巧 1：查看所有可用选项

```bash
marker_single --help
```

### 技巧 2：调试模式

```bash
# 启用调试日志和可视化
marker_single 测试文档.pdf --debug
```

### 技巧 3：跳过图片提取

```bash
# 只提取文本，不保存图片
marker_single 测试文档.pdf --disable_image_extraction
```

### 技巧 4：使用 GUI 界面

```bash
# 安装依赖
pip install streamlit streamlit-ace

# 启动 GUI
marker_gui
```

---

## 总结

### 推荐工作流程

1. **首次使用**：安装依赖 → 运行转换 → 等待模型下载
2. **日常使用**：简单转换 → 检查结果 → 如有问题启用 LLM
3. **批量处理**：准备文件夹 → 批量转换 → 检查输出

### 关键参数速查

```bash
# 最常用
marker_single file.pdf                          # 基本转换
marker_single file.pdf --use_llm               # LLM 增强
marker_single file.pdf --page_range "0-10"     # 指定页面
marker_single file.pdf --force_ocr              # 强制 OCR

# 批量处理
marker input_dir                                # 批量转换
marker input_dir --workers 4                   # 多线程

# 输出控制
marker_single file.pdf --output_format json    # 输出格式
marker_single file.pdf --paginate_output       # 按页编号
```

---

## 相关资源

- [Marker 官方文档](https://github.com/VikParuchuri/marker)
- [OCR 概念笔记](./OCR概念笔记.md)
- [Marker 使用笔记](./marker使用笔记.md)

---

*创建时间：2026-02-15*
