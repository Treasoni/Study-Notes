# Harness Engineering - 参考资料速查

## 评分说明

| 维度 | 分值范围 | 评估标准 |
|------|---------|---------|
| 权威性 | 1-5 | 官方(5) > 知名作者(4) > 行业分析(3) > 社区(2) |
| 时效性 | 1-5 | 半年内(5) > 1年(4) > 2年(3) |
| 完整性 | 1-5 | 全面覆盖(5) > 覆盖要点(3-4) > 部分(1-2) |
| 可读性 | 1-5 | 清晰易读(5) > 基本清晰(3-4) |
| **总评分** | **/20** | 满分20 |

## 评分表

| # | 来源 | 作者 | 日期 | 权威 | 时效 | 完整 | 可读 | **总分** | 保留? |
|---|------|------|------|------|------|------|------|---------|-------|
| 01 | OpenAI 官方实验报告 | OpenAI Codex 团队 | 2026-02 | 5 | 5 | 5 | 4 | **19** | ✅ 核心 |
| 02 | My AI Adoption Journey | Mitchell Hashimoto | 2026-02 | 5 | 5 | 4 | 5 | **19** | ✅ 核心 |
| 03 | Harness Engineering (Fowler) | Martin Fowler | 2026 | 5 | 5 | 5 | 5 | **20** | ✅ 核心 |
| 04 | The Anatomy of an Agent Harness | LangChain / Vivek Trivedy | 2026-03 | 4 | 5 | 4 | 4 | **17** | ✅ 核心 |
| 05 | Harness Engineering - first thoughts | Martin Fowler | 2026 | 5 | 5 | 3 | 5 | **18** | ✅ 补充 |
| 06 | Skill Issue: Harness Engineering | HumanLayer | 2026-03 | 3 | 5 | 4 | 5 | **17** | ✅ 实战 |
| 07 | Harness Engineering（驾驭工程） | 菜鸟教程 | 2026 | 3 | 5 | 4 | 5 | **17** | ✅ 中文入口 |
| 08 | Harness Engineering 学习指南 | deusyu (GitHub) | 2026 | 3 | 5 | 4 | 4 | **16** | ✅ 索引 |
| 09 | What is harness engineering? | SIG (Werner Heijstek) | 2026-04 | 4 | 5 | 4 | 4 | **17** | ✅ 治理视角 |
| 12 | Harness Engineering 来了，SDD 还有意义吗？ | 腾讯云开发者 | 2026 | 3 | 5 | 4 | 4 | **16** | ✅ 对比视角 |
| 14 | Harness Engineering 是什麼？ | ABMedia | 2026-04 | 3 | 5 | 4 | 4 | **16** | ✅ 繁体中文 |
| 16 | What is AI Harness Engineering? | Mohit Sewak (Medium) | 2026-03 | 3 | 5 | 4 | 4 | **16** | ❌ 舍弃 |

## 核心源 vs 补充源

### 核心源（4 份，必须阅读）
| # | 来源 | 不可替代的价值 |
|---|------|--------------|
| 01 | OpenAI 官方 | 唯一的一手实验数据、六大组件体系、效率指标 |
| 02 | Mitchell Hashimoto | 术语起源、AGENTS.md 规则法、个人实战心路 |
| 03 | Martin Fowler | 最完整的理论框架（Guides/Sensors、三类型、Harnessability） |
| 04 | LangChain | Harness 组件架构解剖、Agent = Model + Harness 公式 |

### 补充源（7 份，丰富视角）
| # | 来源 | 独特贡献 |
|---|------|---------|
| 05 | Fowler Memo | 早期思考、Harness 模板化预言、旧系统改造讨论 |
| 06 | HumanLayer | 最贴近实战的配置杠杆体系、子代理防火墙概念 |
| 07 | 菜鸟教程 | 最佳中文入门、Agent 失败模式总结、LangChain 数据 |
| 08 | GitHub 学习指南 | 结构化索引、六大概念的中英对照深度拆分 |
| 09 | SIG | 企业治理视角、软件组合治理 = Harness |
| 12 | 腾讯云 | SDD vs Harness 的独特对比视角 |
| 14 | ABMedia | 繁体中文、Claude Code Harness 剖析 |
