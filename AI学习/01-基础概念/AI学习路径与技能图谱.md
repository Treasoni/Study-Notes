---
title: AI学习路径与技能图谱
created: 2026-04-05
updated: 2026-04-05
tags: [ai, career, learning-path, skills, roadmap]
---

# AI学习路径与技能图谱

> [!info] 概述
> **一句话定义**：从零到 AI 工程师的系统化学习指南，涵盖核心技能、学习路径和项目实践。
> **通俗比喻**：就像建造一座大厦，需要先打地基（数学与编程），再搭建框架（ML/DL），最后装修应用（GenAI/Agent）。

## 核心概念

### 是什么

AI 职业发展是一条从数据处理到智能应用的完整技能链，涉及三个核心角色：
- **Data Scientist**：数据的"翻译官"，从数据中发现故事
- **ML Engineer**：模型的"建筑师"，将算法转化为生产系统
- **AI Engineer**：智能的"编排者"，用预训练模型构建应用

### 为什么需要

> [!note] 行业趋势
> 2026 年 AI 领域的核心技能已从"从零训练模型"转向"高效使用 AI 工具链"。掌握 Prompt Engineering、RAG、AI Agent 等技能成为求职标配。
>
> 来源：[Towards Data Science - AI Career 2026](https://towardsdatascience.com/a-realistic-roadmap-to-start-an-ai-career-in-2026/)

### 通俗理解

🎯 **比喻**：

| 角色 | 类比 | 核心产出 |
|------|------|---------|
| Data Scientist | 厨师 | 用食材（数据）烹饪出美味佳肴（洞察） |
| ML Engineer | 建筑师 | 将设计图纸（算法）建成高楼（系统） |
| AI Engineer | 指挥家 | 编排各类乐器（模型/API）演奏交响乐（应用） |

## AI 职业角色与技能矩阵

### 三大核心角色

#### Data Scientist
> [!abstract] 职责范围
> - 数据收集与清洗
> - 探索性数据分析（EDA）
> - 统计建模与假设检验
> - 可视化与洞察分享

**核心工具**：Python, SQL, Pandas, Matplotlib, Tableau

#### ML Engineer
> [!abstract] 职责范围
> - 编程与算法实现
> - 数学基础（线性代数、概率论）
> - 深度学习模型开发
> - MLOps 与生产部署

**核心工具**：PyTorch/TensorFlow, Docker, MLflow, Kubernetes

#### AI Engineer
> [!abstract] 职责范围
> - 预训练模型调用与微调
> - Prompt Engineering
> - API 集成与系统架构
> - RAG 系统与 Vector DB
> - AI Agent 设计与开发

**核心工具**：LangChain, OpenAI API, Pinecone/Weaviate, Vector DB

### 2026 年核心 AI 技能

> [!tip] 技能清单
> 1. **Prompt Engineering** - 与 AI 模型高效沟通
> 2. **Data Analysis with AI** - 用 AI 加速数据分析
> 3. **AI Automation** - 自动化工作流设计
> 4. **AI-Assisted Programming** - AI 辅助编程
> 5. **AI Content Creation** - AI 内容生成
> 6. **AI Design** - AI 辅助设计
> 7. **AI Ethics** - 伦理与合规

来源：[roadmap.sh AI Roadmap](https://roadmap.sh/ai-data-scientist)

## 四阶段学习路径（14 周）

> [!example] 完整路线图
> 来源：[roadmap.sh ML Roadmap](https://roadmap.sh/machine-learning)

### Phase 1: Advanced ML（3 周）

**目标**：掌握端到端 ML 流程

**核心内容**：
- 真实数据集处理（非玩具数据）
- 完整 ML Pipeline：数据清洗 → 特征工程 → 模型训练 → 评估 → 部署
- 工具栈：Pandas, Scikit-learn, XGBoost, SHAP

**关键产出**：
```python
# 端到端 ML 示例
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import shap

# 1. 数据加载与清洗
df = pd.read_csv("data.csv")
df = df.dropna()

# 2. 特征工程
X = df.drop("target", axis=1)
y = df["target"]

# 3. 模型训练
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 4. 评估
print(classification_report(y_test, model.predict(X_test)))

# 5. 可解释性分析
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
```

### Phase 2: MLOps & Deployment（3 周）

**目标**：将模型部署到生产环境

**核心内容**：
- 实验追踪：MLflow
- API 服务：FastAPI
- 前端展示：Streamlit
- 容器化：Docker

**关键产出**：
```python
# FastAPI 模型服务
from fastapi import FastAPI
from pydantic import BaseModel
import pickle

app = FastAPI()

class InputData(BaseModel):
    feature1: float
    feature2: float

@app.post("/predict")
def predict(data: InputData):
    model = pickle.load(open("model.pkl", "rb"))
    prediction = model.predict([[data.feature1, data.feature2]])
    return {"prediction": prediction[0]}
```

### Phase 3: GenAI & RAG（4 周）

**目标**：构建生成式 AI 应用

**核心内容**：
- LangChain 框架
- OpenAI API 集成
- Vector DB：Weaviate / Chroma / FAISS
- RAG 系统设计

**关键产出**：
```python
# RAG 系统示例
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# 1. 向量存储
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

# 2. 检索增强生成
llm = ChatOpenAI(model="gpt-4")
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)

# 3. 查询
answer = qa.run("What is the main topic?")
```

来源：[LangChain Tutorial 2026](https://blog.jetbrains.com/pycharm/2026/02/langchain-tutorial-2026/)

### Phase 4: Capstone Project（4 周）

**目标**：整合所有技能，完成端到端项目

**项目建议**：
1. **ML 系统**：端到端预测系统（数据 → 模型 → API → 前端）
2. **NLP 应用**：文档问答系统（RAG + LLM）
3. **计算机视觉**：图像分类/检测系统
4. **生成式 AI**：AI Agent 或多模态应用
5. **数据工程**：ETL Pipeline + 数据仓库

## 编程与数学基础

### Python 核心库

#### NumPy
> [!abstract] 核心能力
> - N 维数组（ndarray）
> - 线性代数运算
> - 广播机制
> - 高效数值计算

```python
import numpy as np

# 数组操作
arr = np.array([[1, 2], [3, 4]])
print(arr.shape)  # (2, 2)

# 线性代数
A = np.random.rand(3, 3)
B = np.random.rand(3, 3)
C = np.dot(A, B)  # 矩阵乘法
```

#### Pandas
> [!abstract] 核心能力
> - DataFrame 数据结构
> - 数据清洗与转换
> - 分组聚合
> - 时间序列处理

```python
import pandas as pd

# 数据清洗
df = pd.read_csv("data.csv")
df = df.dropna(subset=["column1"])
df["new_column"] = df["column1"].apply(lambda x: x * 2)

# 分组聚合
result = df.groupby("category")["value"].mean()
```

### 数学基础

| 领域 | 核心内容 | AI 应用 |
|------|---------|---------|
| **线性代数** | 向量、矩阵、特征值 | 神经网络权重、降维 |
| **微积分** | 导数、梯度、优化 | 梯度下降、反向传播 |
| **统计学** | 分布、假设检验 | 数据分析、A/B 测试 |
| **概率论** | 贝叶斯、条件概率 | 不确定性建模、生成模型 |

## 深度学习框架对比

| 框架 | 特点 | 适用场景 | 学习曲线 |
|------|------|---------|---------|
| **PyTorch** | 动态图、易调试、Pythonic | 研究、原型开发、教学 | 中等 |
| **TensorFlow** | 静态图、生产部署、Keras API | 工业应用、大规模部署 | 较陡 |
| **scikit-learn** | 传统 ML 算法、API 统一 | 数据预处理、基线模型 | 平缓 |

### PyTorch 示例

```python
import torch
import torch.nn as nn

# 定义模型
class SimpleNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

# 训练循环
model = SimpleNN()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters())

for epoch in range(10):
    outputs = model(inputs)
    loss = criterion(outputs, labels)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

来源：[PyTorch Tutorials](https://pytorch.org/tutorials/)

### TensorFlow 示例

```python
import tensorflow as tf

# 定义模型
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dense(10, activation='softmax')
])

# 编译与训练
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(x_train, y_train, epochs=10, batch_size=32)
```

来源：[TensorFlow Tutorials](https://www.tensorflow.org/tutorials)

## LangChain 框架

### 核心概念

> [!abstract] 三大支柱
> 1. **Agents** - 自主决策的智能体
> 2. **Tools** - 可调用的工具/函数
> 3. **Chains** - 任务执行链

### 应用场景

| 场景 | 说明 | 核心组件 |
|------|------|---------|
| **Chatbots** | 对话机器人 | LLM + Memory + Tools |
| **Document Q&A** | 文档问答 | RAG + Vector DB |
| **Content Generation** | 内容生成 | LLM + Templates |

### 高级特性

- **MCP Adapter** - 模型上下文协议适配器
- **Guardrails** - 输出安全与合规检查
- **Testing** - 链式测试与评估

来源：[LangChain Tutorial 2026](https://blog.jetbrains.com/pycharm/2026/02/langchain-tutorial-2026/)

## AI 项目作品集

> [!tip] 5 类核心项目
> 来源：[roadmap.sh AI Engineer](https://roadmap.sh/ai-engineer)

### 1. ML 系统
- 端到端预测系统
- 时间序列预测
- 推荐系统

### 2. NLP 应用
- 文档问答系统（RAG）
- 文本分类
- 命名实体识别

### 3. 计算机视觉
- 图像分类
- 目标检测
- 图像分割

### 4. 生成式 AI
- AI Agent
- 多模态应用
- 代码生成

### 5. 数据工程
- ETL Pipeline
- 数据仓库
- 实时数据处理

## 与其他概念的关系

| 概念 | 关系 | 说明 |
|------|------|------|
| [[Python]] | 基础 | AI 开发的核心编程语言 |
| [[深度学习]] | 进阶 | ML 的子领域，神经网络为核心 |
| [[MLOps]] | 实践 | 模型部署与运维 |
| [[RAG]] | 应用 | 检索增强生成技术 |
| [[LangChain]] | 工具 | LLM 应用开发框架 |
| [[Prompt Engineering]] | 技能 | 与 AI 模型高效沟通 |

## 最佳实践

### 学习建议

1. **循序渐进**：先掌握基础（Python、数学），再学 ML/DL，最后进阶 GenAI
2. **项目驱动**：每学完一个阶段，完成一个完整项目
3. **持续实践**：每周至少写代码，保持手感
4. **建立作品集**：将项目部署上线，积累 GitHub Stars

### 常见误区

> [!warning] 避坑指南
> - ❌ 只看视频不动手
> - ❌ 追求完美，迟迟不出成果
> - ❌ 忽视数学基础
> - ❌ 只学理论不实践
> - ❌ 频繁换方向，缺乏深度

## 常见问题

### Q1: 需要多少数学基础？
> [!note] 回答
> 基础阶段：线性代数、概率论、统计学（大学水平即可）
> 进阶阶段：优化理论、信息论（可边用边学）

### Q2: PyTorch 还是 TensorFlow？
> [!note] 回答
> - 研究与原型开发：PyTorch（更灵活）
> - 工业部署：TensorFlow（生态成熟）
> - 建议：先学 PyTorch，再了解 TensorFlow

### Q3: 需要学习传统 ML 吗？
> [!note] 回答
> 需要。深度学习不是万能的，传统 ML（如 XGBoost）在结构化数据上依然高效，且更易解释。

### Q4: 14 周能学会吗？
> [!note] 回答
> 14 周是"入门到能做项目"的时间。真正精通需要持续实践（6-12 个月）。建议：先完成 14 周计划，再根据兴趣深入特定领域。

## 参考资料

### 官方路线图
- [roadmap.sh AI Roadmap](https://roadmap.sh/ai-data-scientist) - AI 数据科学家路线图
- [roadmap.sh ML Roadmap](https://roadmap.sh/machine-learning) - 机器学习路线图
- [roadmap.sh AI Engineer](https://roadmap.sh/ai-engineer) - AI 工程师路线图

### 框架文档
- [PyTorch Tutorials](https://pytorch.org/tutorials/) - PyTorch 官方教程
- [TensorFlow Tutorials](https://www.tensorflow.org/tutorials) - TensorFlow 官方教程
- [scikit-learn](https://scikit-learn.org/stable/) - scikit-learn 官方文档

### 进阶资源
- [LangChain Tutorial 2026](https://blog.jetbrains.com/pycharm/2026/02/langchain-tutorial-2026/) - JetBrains LangChain 教程
- [Towards Data Science - AI Career 2026](https://towardsdatascience.com/a-realistic-roadmap-to-start-an-ai-career-in-2026/) - AI 职业规划

## 个人笔记

> [!personal] 💡 我的理解与感悟
>
> ### 当前阶段
> - [ ] Phase 1: Advanced ML
> - [ ] Phase 2: MLOps & Deployment
> - [ ] Phase 3: GenAI & RAG
> - [ ] Phase 4: Capstone Project
>
> ### 学习计划
> - 目标完成时间：
> - 每周投入时间：
> - 重点方向：
>
> ### 踩坑记录
> （此处记录学习过程中遇到的问题和解决方案）
>
> ### 待探索
> - [ ] 深入学习 Vector DB（Weaviate vs Chroma vs FAISS）
> - [ ] AI Agent 设计模式
> - [ ] 多模态模型应用
