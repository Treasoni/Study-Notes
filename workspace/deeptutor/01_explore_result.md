# DeepTutor 探测式收集结果（P1）

> 阶段：P1 探测式收集（learning-note-flow / run_id: deeptutor）
> 探测日期：2026-09-01
> 方法：3 个独立透镜 × 并行 subagent 网络搜索；共 8 个去重后候选源（Tier 1 ×4，Tier 2 ×4）

---

## 方向菜单

| 方向 | 内容 | 适合 |
|------|------|------|
| **A. 项目概览与功能全景** | DeepTutor 是什么、核心能力（六合一工作区、Book Engine、知识库、三层记忆、TutorBot）、适用场景与最新版本功能 | 先建立整体认知，判断值不值得深入 |
| **B. 部署与上手使用** | Docker 部署、环境要求、模型/Embedding API 接入、Web UI 基本使用流程与排错 | 动手实操，跑通第一个学习场景 |
| **C. 架构与原理** | Agent-Native 多智能体架构、共享个性化引擎、RAG 混合检索、三层持久记忆、双循环推理 | 理解设计原理与工程实现 |

---

## 候选源清单

### A. 项目概览与功能全景

| # | 源 | Tier | 日期 | 得分 |
|---|----|------|------|------|
| A1 | [GitHub 官方仓库 README](https://github.com/HKUDS/DeepTutor) | 1 | 2026-07 | 5 |
| A2 | [官网 deeptutor.info](https://deeptutor.info/) | 1 | unknown | 5 |
| A3 | [arXiv:2604.26962 - DeepTutor: Towards Agentic Personalized Tutoring](https://arxiv.org/abs/2604.26962) | 1 | 2026-04 | 4 |
| A4 | [newreleases.io - v1.5.1 发布追踪](https://newreleases.io/project/github/HKUDS/DeepTutor/release/v1.5.1) | 2 | 2026-07 | 3 |
| A5 | [DEV Community #153 - DeepTutor 深度解读](https://dev.to/wonderlab/open-source-project-153-deeptutor-agent-native-lifelong-learning-workspace-3-layer-memory--3dg0) | 2 | unknown | 3 |

### B. 部署与上手使用

| # | 源 | Tier | 日期 | 得分 |
|---|----|------|------|------|
| B1 | [官方文档 - Docker 部署（中文）](https://docs.deeptutor.info/zh-cn/get-started/docker/) | 1 | unknown | 5 |
| B2 | [官方文档 - 快速上手 / 故障排查（中文）](https://docs.deeptutor.info/zh-cn/get-started/troubleshooting/) | 1 | unknown | 4 |
| B3 | [CSDN - Docker 部署与 Web 使用实战](https://blog.csdn.net/weixin_27230891/article/details/160874436) | 2 | unknown | 4 |
| B4 | [威联通 NAS - docker-compose 完整部署实录](https://www.qnaptw.com/sys-nd/2404.html) | 2 | unknown | 3 |

### C. 架构与原理

| # | 源 | Tier | 日期 | 得分 |
|---|----|------|------|------|
| C1 | [arXiv:2604.26962（论文正文）](https://arxiv.org/abs/2604.26962) | 1 | 2026-04 | 5 |
| C2 | [GitHub README - 架构章节](https://github.com/HKUDS/DeepTutor) | 1 | 2026-06 | 5 |
| C3 | [官方文档 docs.deeptutor.info](https://docs.deeptutor.info/) | 1 | unknown | 4 |
| C4 | [BAAI 智源 - 多智能体协作架构解读](https://hub.baai.ac.cn/view/53930) | 2 | unknown | 4 |
| C5 | [DEV Community #153 - 三层记忆 + 多引擎 RAG](https://dev.to/wonderlab/open-source-project-153-deeptutor-agent-native-lifelong-learning-workspace-3-layer-memory--3dg0) | 2 | unknown | 3 |

> 注：GitHub README、arXiv 论文、官方文档为跨透镜共用的一手源，已去重（总数 8 个唯一源）。WebFetch 在本环境受限，URL 均经多次独立搜索确认存在，正文抓取留待 P2。

---

## 覆盖缺口

1. **本地资源要求**：GPU/显存、内存的最低要求与性能基准缺少一手数据，P2 需从 README / 官方文档确认。
2. **许可协议存疑**：任务参数记录为 AGPL-3.0，但探测发现 README 标注 Apache-2.0（子代理提示），P2 需核对仓库 LICENSE 文件。
3. **进阶功能实操细节**：Book Engine 14 种块类型、考试模拟的具体操作步骤在官方资料中较少，需以社区文章补充视角。

## 预估 P2 范围

- **选 A**：抓取官方 README + 官网 + arXiv 摘要/引言 → 产出功能地图与适用场景。
- **选 B**：抓取官方 Docker 文档 + 快速上手/排错 + 1 篇中文实战 → 产出部署步骤清单、模型接入配置与避坑清单。
- **选 C**：抓取 arXiv 论文 + README 架构章节 + 官方文档 + BAAI 教程 → 产出架构原理笔记。
- **组合方向**：合并对应收集范围，共享的一手源（README / arXiv / 官方文档）只抓取一次。
