# Marker 使用笔记

> 📚 **[关联笔记](./AI学习/OCR概念笔记.md)**：想了解 Marker 如何使用 OCR 识别技术？

## 项目简介

Marker 是一个开源工具，专门用于将 PDF 文档转换为高质量的 Markdown 格式。它利用深度学习模型来识别和处理 PDF 中的各种元素，包括文本、表格、公式、图片等。

### 主要功能特点

- **智能文本提取**：准确识别 PDF 中的文本内容
- **表格识别**：自动检测并转换表格为 Markdown 格式
- **公式转换**：支持将数学公式转换为 LaTeX 格式
- **图片提取**：保留文档中的图片
- **多语言支持**：支持中文等多种语言
- **批量处理**：支持批量转换多个 PDF 文件
- **LLM 增强**：支持使用 LLM 提高转换准确率
- **多种输出格式**：支持 Markdown、JSON、HTML、Chunks

### 应用场景

- 将学术论文转换为 Markdown 格式
- 电子书籍格式转换
- 文档归档和索引
- 知识库构建
- 扫描文档的数字识别

---

## 安装方法

### pip 安装方式

```bash
# 基本安装
pip install marker-pdf

# 支全支持所有文件类型（PDF、图片、PPTX、DOCX 等）
pip install marker-pdf[full]
```

### 系统依赖安装（OCR 支持）

为了获得最佳的 OCR 支持，建议安装以下系统依赖：

**macOS (使用 Homebrew):**

```bash
brew install tesseract
brew install poppler
```

**Ubuntu/Debian:**

```bash
sudo apt-get install tesseract-ocr
sudo apt-get install libpoppler-cpp-dev
sudo apt-get install pdftoppm
```

**Windows:**

下载并安装 Tesseract OCR 和 Poppler，将它们添加到系统 PATH。

---

## 命令行使用

### 交互式 GUI

```bash
pip install streamlit streamlit-ace
marker_gui
```

### 转换单个文件

```bash
marker_single /path/to/file.pdf [OPTIONS]
```

**选项：**

| 参数 | 说明 |
|------|------|
| `--page_range` | 指定页面，如 `"0,5-10,20"` |
| `--output_format` | 输出格式：`markdown`/`json`/`html`/`chunks` |
| `--output_dir` | 自定义输出目录 |
| `--paginate_output` | 按页编号输出 |
| `--use_llm` | 使用 LLM 提高准确率 |
| `--force_ocr` | 强制对整篇文档进行 OCR |
| `--block_correction_prompt` | 自定义块修正的 LLM 提示词 |
| `--strip_existing_ocr` | 移除现有 OCR 文本 |
| `--redo_inline_math` | 高质量数学公式转换（需 `--use_llm`） |
| `--disable_image_extraction` | 跳过图片保存 |
| `--debug` | 启用调试日志/可视化 |
| `--processors` | 自定义处理器（逗号分隔） |
| `--config_json` | JSON 配置文件路径 |
| `--converter_cls` | 转换器类，默认 `marker.converters.pdf.PdfConverter` |
| `--llm_service` | LLM 服务提供商 |
| `--help` | 显示所有可用选项 |

### 转换文件夹

```bash
marker /path/to/input/folder [OPTIONS]
```

**额外选项：**

| 参数 | 说明 |
|------|------|
| `--workers` | 并行转换的工作线程数 |

### 多 GPU 批量转换

```bash
NUM_DEVICES=4 NUM_WORKERS=15 marker_chunk_convert /path/to/input /path/to/output
```

### API 服务器

```bash
pip install -U uvicorn fastapi python-multipart
marker_server --port 8001
```

访问 `http://localhost:8001` 或使用 API：

```python
import requests
import json
post_data = {'filepath': '/path/to/file.pdf', 'output_format': 'markdown'}
response = requests.post("http://localhost:8001/marker", data=json.dumps(post_data))
```

---

## 使用示例

### 基本转换

```bash
# 转换单个 PDF
marker_single input.pdf

# 指定输出格式
marker_single input.pdf --output_format json

# 指定页面范围
marker_single input.pdf --page_range "0,5-10,20"

# 按页编号输出
marker_single input.pdf --paginate_output
```

### 使用 LLM 增强转换

```bash
# 使用 Gemini API（默认）
marker_single /data/research.pdf --use_llm --gemini_api_key YOUR_KEY

# 使用 OpenAI
marker_single input.pdf --use_llm \
  --llm_service marker.services.openai.OpenAIService \
  --openai_api_key KEY \
  --openai_model gpt-4o

# 使用 Claude
marker_single input.pdf --use_llm \
  --llm_service marker.services.claude.ClaudeService \
  --claude_api_key KEY \
  --claude_model_name claude-3-5-sonnet

# 使用 Ollama（本地）
marker_single input.pdf --use_llm \
  --llm_service marker.services.ollama.OllamaService \
  --ollama_model llama3 \
  --ollama_base_url http://localhost:11434
```

### OCR 相关

```bash
# 强制 OCR 整篇文档
marker_single input.pdf --force_ocr

# 移除现有 OCR 并重新处理
marker_single input.pdf --strip_existing_ocr

# 高质量数学公式转换
marker_single input.pdf --use_llm --redo_inline_math
```

### 仅提取特定内容

```bash
# 仅提取表格
marker_single input.pdf \
  --converter_cls marker.converters.table.TableConverter \
  --use_llm \
  --output_format json \
  --force_layout_block Table

# 仅 OCR 处理
marker_single input.pdf \
  --converter_cls marker.converters.ocr.OCRConverter \
  --keep_chars
```

### 批量转换

```bash
# 转换整个文件夹
marker /data/documents

# 使用多线程
marker /data/documents --workers 4

# 转换为 JSON 并强制 OCR
marker /data/documents --output_format json --force_ocr --paginate_output
```

---

## Python API 使用

### 基本用法

```python
from marker.convert import convert_single_pdf
from marker.models import load_all_models

# 加载模型
model_list = load_all_models()

# 转换单个 PDF
full_text, images, out_meta = convert_single_pdf(
    "input.pdf",
    model_list,
    max_pages=10,
    parallel_factor=1
)

# 输出结果
print(full_text)
```

### 批量处理脚本

```python
import os
from pathlib import Path
from marker.convert import convert_single_pdf
from marker.models import load_all_models

def batch_convert_pdfs(input_dir, output_dir):
    """批量转换 PDF 文件"""

    # 加载模型
    print("正在加载模型...")
    model_list = load_all_models()

    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 遍历输入目录
    for pdf_file in Path(input_dir).glob("*.pdf"):
        print(f"正在转换: {pdf_file.name}")

        try:
            # 转换 PDF
            full_text, images, out_meta = convert_single_pdf(
                str(pdf_file),
                model_list,
                max_pages=None
            )

            # 保存 Markdown
            output_file = Path(output_dir) / f"{pdf_file.stem}.md"
            output_file.write_text(full_text, encoding="utf-8")

            print(f"✓ 已保存: {output_file}")

        except Exception as e:
            print(f"✗ 转换失败: {pdf_file.name} - {e}")

# 使用示例
if __name__ == "__main__":
    batch_convert_pdfs("pdfs", "markdown_output")
```

---

## LLM 服务配置

使用 `--use_llm` 时可配置以下服务：

| 服务 | 命令 |
|------|------|
| **Gemini** | `--llm_service marker.services.gemini.GoogleGeminiService --gemini_api_key KEY` |
| **Ollama** | `--llm_service marker.services.ollama.OllamaService --ollama_model llama3 --ollama_base_url http://localhost:11434` |
| **OpenAI** | `--llm_service marker.services.openai.OpenAIService --openai_api_key KEY --openai_model gpt-4o` |
| **Claude** | `--llm_service marker.services.claude.ClaudeService --claude_api_key KEY --claude_model_name claude-3-5-sonnet` |
| **Vertex AI** | `--llm_service marker.services.vertex.VertexAIService` |
| **Azure OpenAI** | `--llm_service marker.services.azure_openai.AzureOpenAIService` |

---

## 配置说明

- `TORCH_DEVICE` 环境变量可指定设备：`cuda`/`cpu`/`mps`（默认自动检测）
- 运行 `marker_single --help` 或 `marker --help` 查看所有选项

---

## 首次使用

### 模型下载说明

**首次运行时会发生什么？**

当你首次运行 `marker_single` 命令时：

1. **自动检查**：Marker 会检查本地是否有所需的模型文件
2. **自动下载**：如果没有找到，会自动从 Hugging Face 下载模型
3. **下载大小**：约 2-3GB，需要稳定的网络连接
4. **下载位置**：默认存储在 `~/.cache/huggingface/` 目录下
5. **下载时间**：根据网速，通常需要几分钟

**示例输出：**
```
Downloading models...
[========================================] 100%
Models downloaded successfully!
```

### 指定模型目录

你可以手动指定模型文件的存储位置：

```bash
# 指定模型目录
marker_single input.pdf --model_dir /path/to/your/models
```

**什么时候需要指定模型目录？**
- 多台电脑共享模型
- 首次下载后想把模型移到其他位置
- 网络受限，需要手动下载模型

---

## 系统要求

- **Python**：3.10 或更高版本
- **PyTorch**：自动安装
- **内存**：建议至少 4GB 可用内存
- **存储空间**：模型文件需要约 2-3GB 空间
- **GPU**：可选，有 GPU 可以显著提升处理速度

---

## 相关资源

- **GitHub 仓库**：https://github.com/VikParuchuri/marker
- **PyPI 页面**：https://pypi.org/project/marker-pdf/
- **官方文档**：https://github.com/VikParuchuri/marker/blob/main/README.md
- **问题反馈**：https://github.com/VikParuchuri/marker/issues

---

*最后更新：2026-02-15*
