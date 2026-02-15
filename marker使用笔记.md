# Marker 使用笔记

## 项目简介

Marker 是一个开源工具，专门用于将 PDF 文档转换为高质量的 Markdown 格式。它利用深度学习模型来识别和处理 PDF 中的各种元素，包括文本、表格、公式、图片等。

### 主要功能特点

- **智能文本提取**：准确识别 PDF 中的文本内容
- **表格识别**：自动检测并转换表格为 Markdown 格式
- **公式转换**：支持将数学公式转换为 LaTeX 格式
- **图片提取**：保留文档中的图片
- **多语言支持**：支持中文等多种语言
- **批量处理**：支持批量转换多个 PDF 文件

### 应用场景

- 将学术论文转换为 Markdown 格式
- 电子书籍格式转换
- 文档归档和索引
- 知识库构建

---

## 安装方法

### pip 安装方式

```bash
# 基本安装
pip install marker-pdf

# 从 GitHub 安装最新版本
pip install git+https://github.com/VikParuchuri/marker.git
```

### 系统依赖安装（可选的 OCR 支持）

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

### 基本命令结构

```bash
marker_convert <输入路径> <输出目录> [选项]
```

### 转换单个 PDF

```bash
# 转换单个 PDF 文件
marker_convert input.pdf output_dir

# 指定输出文件名
marker_convert input.pdf output_dir --output_filename my_document.md

# 使用特定页数范围
marker_convert input.pdf output_dir --pages 1-5

# 跳过页数
marker_convert input.pdf output_dir --max_pages 10
```

### 批量转换

```bash
# 转换目录下所有 PDF 文件
marker_convert input_directory output_directory

# 并行处理多个文件
marker_convert input_directory output_directory --workers 4
```

### 下载模型

首次使用时，Marker 会自动下载所需的模型。也可以手动指定模型目录：

```bash
marker_convert input.pdf output_dir --model_dir /path/to/models
```

---

## Python API 使用

### 基本用法示例

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

### 高级用法示例

```python
from marker.convert import convert_single_pdf
from marker.models import load_all_models

# 加载模型（可指定模型目录）
model_list = load_all_models(model_dir="./models")

# 转换 PDF 并使用更多选项
full_text, images, out_meta = convert_single_pdf(
    "input.pdf",
    model_list,
    max_pages=None,          # 不限制页数
    parallel_factor=2,       # 并行因子
2,       # 输出格式
)

# 处理提取的图片
for img_name, img_data in images.items():
    print(f"图片: {img_name}, 大小: {len(img_data)} bytes")
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

## 常用参数选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--max_pages` | 最大转换页数 | None (全部) |
| `--output_filename` | 指定输出文件名 | 自动生成 |
| `--pages` | 指定页数范围（如 1-5） | None |
| `--workers` | 并行工作数 | 1 |
| `--model_dir` | 模型文件目录 | 默认目录 |
| `--batch_multiplier` | 批量处理乘数 | 1 |
| `--dpi` | PDF 渲染 DPI | 96 |
| `--ocr_all_pages` | 对所有页面使用 OCR | False |
| `--extract_images` | 提取图片 | True |

---

## 注意事项

### 首次使用建议

1. **首次运行会下载模型**：首次使用时，Marker 会自动下载约 2-3GB 的模型文件，请确保网络连接稳定
2. **测试单个文件**：建议先转换单个 PDF 测试效果，确认无误后再批量处理
3. **检查输出格式**：查看转换后的 Markdown 文件，确认表格、公式等元素是否正确转换

### 性能优化建议

1. **限制并行数**：根据 CPU 核心数调整 `parallel_factor`，一般设置为 CPU 核心数的一半
2. **分批处理**：对于大量文件，可以分批处理以避免内存不足
3. **指定页数范围**：如果只需要部分内容，使用 `--pages` 或 `--max_pages` 加速处理

### 系统要求

- **Python**：3.8 或更高版本
- **内存**：建议至少 4GB 可用内存
- **存储空间**：模型文件需要约 2-3GB 空间
- **GPU**：可选，有 GPU 可以显著提升处理速度

---

## 实战示例

### 示例：转换学术论文

```bash
# 1. 安装 Marker
pip install marker-pdf

# 2. 下载一篇论文 PDF（示例）
# 假设已下载为 paper.pdf

# 3. 转换 PDF
marker_convert paper.pdf output

# 4. 查看结果
cat output/paper.md
```

### 示例：Python 批量处理

```python
from marker.convert import convert_single_pdf
from marker.models import load_all_models
from pathlib import Path

# 配置
INPUT_DIR = "papers"
OUTPUT_DIR = "converted"

# 初始化
model_list = load_all_models()
Path(OUTPUT_DIR).mkdir(exist_ok=True)

# 批量转换
for pdf in Path(INPUT_DIR).glob("*.pdf"):
    print(f"处理: {pdf.name}")

    text, images, meta = convert_single_pdf(
        str(pdf),
        model_list,
        max_pages=50  # 限制前 50 页
    )

    # 保存结果
    md_file = Path(OUTPUT_DIR) / f"{pdf.stem}.md"
    md_file.write_text(text, encoding="utf-8")

    print(f"完成: {md_file.name}")
```

---

## 相关资源

- **GitHub 仓库**：https://github.com/VikParuchuri/marker
- **PyPI 页面**：https://pypi.org/project/marker-pdf/
- **在线文档**: [查看官方文档获取最新信息](https://github.com/Vikparuchuri/marker/blob/main/README.md)
- **问题反馈**：https://github.com/VikParuchuri/marker/issues

---

*最后更新：2026-02-15*
