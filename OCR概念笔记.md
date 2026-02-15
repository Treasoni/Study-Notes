# OCR 概念笔记

> 📚 **关联笔记**：想了解如何在 Marker 工具中使用 OCR？请查看 [Marker使用笔记](./marker使用笔记.md)

## 什么是 OCR？

**OCR** 是 **Optical Character Recognition**（光学字符识别）的缩写。

简单来说，OCR 是一种技术，能够**从图像、扫描文档或 PDF 文件中自动识别并提取文字内容**。

### 核心思想

```
【图像】 → 【OCR技术】 → 【可编辑的文字】

例如：
扫描的PDF图片 → OCR → 你可以复制、编辑的文字
```

---

## OCR 原理简介

OCR 的工作流程大致如下：

### 1. 图像预处理
```
原始图像 → 去噪 → 二值化 → 规范化 → 清洁图像
```
- 去噪：去除图像中的噪点
- 二值化：将图像转为黑白两色
- 规范化：调整大小、角度等

### 2. 特征提取
```
清洁图像 → 识别字符特征 → 特征数据
```
- 识别字符的形状、笔画等特征

### 3. 字符识别
```
特征数据 → 匹配字符库 → 识别结果
```
- 将提取的特征与已知的字符进行比较

### 4. 后处理
```
识别结果 → 语言模型校正 → 最终文本
```
- 利用语法、上下文纠正错误

---

## 应用场景

| 场景 | 说明 |
|------|------|
| **文档数字化** | 将纸质书籍、合同扫描后转为可编辑文本 |
| **PDF 文字提取** | 从扫描版 PDF 中提取文字 |
| **车牌识别** | 自动识别汽车车牌号码 |
| **身份证/票据识别** | 自动提取证件信息 |
| **手写识别** | 识别手写文字（难度较高） |
| **图片文字提取** | 从截图中提取文字 |

---

## OCR 工具和技术

### 开源 OCR 工具

#### Tesseract OCR
- **特点**：最流行的开源 OCR 引擎，支持 100+ 种语言
- **开发者**：Google（最初由 HP 开发）
- **安装**：
  ```bash
  # macOS
  brew install tesseract

  # Ubuntu
  sudo apt-get install tesseract-ocr
  ```

#### EasyOCR
- **特点**：基于深度学习，易于使用，支持多语言
- **Python 示例**：
  ```python
  import easyocr

  reader = easyocr.Reader(['ch_sim', 'en'])
  result = reader.readtext('image.png')

  for detection in result:
      print(detection[1])  # 提取的文本
  ```

#### PaddleOCR
- **特点**：百度开源的 OCR 工具，中文识别效果好
- **官网**：https://github.com/PaddlePaddle/PaddleOCR

### 云服务 OCR

| 服务 | 提供商 |
|------|--------|
| Google Cloud Vision API | Google |
| Amazon Textract | AWS |
| Azure Computer Vision | Microsoft |
| 百度 OCR | 百度 |

---

## 在 Marker 中使用 OCR

Marker 转换 PDF 时会自动使用 OCR 来处理以下情况：

### 1. 扫描版 PDF
```
【扫描的 PDF（图片格式）】
    ↓
【使用 OCR 识别文字】
    ↓
【转换为 Markdown】
```

### 2. 嵌入图片的 PDF
```
【包含嵌入图片的 PDF】
    ↓
【提取图片内容】+【使用 OCR 识别图片中的文字】
    ↓
【转换为 Markdown】
```

### 3. OCR 相关参数
```bash
# 对所有页面使用 OCR（默认只在需要时使用）
marker_convert input.pdf output --ocr_all_pages

# 指定 OCR 引擎（如果支持）
marker_convert input.pdf output --ocr_engine tesseract
```

---

## OCR 的优缺点

### 优点
- ✓ 自动化文字提取，节省时间
- ✓ 支持批量处理大量文档
- ✓ 可处理手写文字（准确率相对较低）
- ✓ 与其他技术结合可实现更多应用

### 缺点
- ✗ 准确率不是 100%，可能出错
- ✗ 对复杂排版、手写文字识别效果差
- ✗ 对图片质量要求高
- ✗ 需要一定的计算资源

### 影响识别准确率的因素
1. **图片质量**：模糊、倾斜、低分辨率会降低准确率
2. **文字清晰度**：字体复杂、文字过小难以识别
3. **背景干扰**：背景复杂或有水印会影响识别
4. **语言复杂度**：混合语言、生僻字识别困难

---

## 实际使用示例

### 示例 1：使用 Tesseract 进行 OCR

```bash
# 安装 Tesseract 和 Python 包
brew install tesseract
pip install pytesseract

# 运行 OCR
tesseract input.png output.txt
```

```python
# Python 示例
import pytesseract
from PIL import Image

# 打开图片

text = pytesseract.image_to_string(image)

print(text)
```

### 示例 2：使用 Marker 转换扫描版 PDF

```bash
# 转换扫描版 PDF（自动使用 OCR）
marker_convert scanned_paper.pdf output

# 查看结果
cat output/scanned_paper.md
```

---

## 常见问题

### Q1：OCR 能识别手写文字吗？
**A**：可以，但准确率较低，特别是潦草的字迹。印刷体的识别准确率要高得多。

### Q2：OCR 需要联网吗？
**A**：取决于使用的工具。本地工具如 Tesseract 不需要联网；云服务 OCR 需要联网。

### Q3：如何提高 OCR 准确率？
**A**：
- 使用高质量、高分辨率的图片
- 确保文字清晰，对比度高
- 预处理图片（去噪、校正角度）
- 使用专门针对该语言训练的模型

### Q4：Marker 什么时候使用 OCR？
**A**：
- 当 PDF 中的页面是图像时（扫描版）
- 当无法直接提取文字时
- 使用 `--ocr_all_pages` 参数时强制对所有页面使用

---

## 总结

**OCR（光学字符识别）**是一种将图像中的文字转换为可编辑文本的技术。

核心要点：
- 📷 从图片/扫描文档中提取文字
- 🔄 工作流程：预处理 → 特征提取 → 字符识别 → 后处理
- 🛠️ 常用工具：Tesseract、EasyOCR、PaddleOCR
- ⚖️ 优点是自动化、批量处理；缺点是准确率非 100%
- 📄 在 Marker 中用于处理扫描版 PDF 和嵌入图片

---

*最后更新：2026-02-15*
