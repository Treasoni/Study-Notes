## 1. 配置系统

- [x] 1.1 创建 `.study-config.yaml` 配置文件结构
- [x] 1.2 实现配置读取工具函数
- [x] 1.3 添加 autonomy level 配置项（默认 Level 1）
- [x] 1.4 添加 per-phase override 配置支持

## 2. 需求发现阶段

- [x] 2.1 创建 `requirement-discovery` skill 框架
- [x] 2.2 实现结构化问答流程（4-6 个问题）
- [x] 2.3 实现笔记类型推断逻辑
- [x] 2.4 实现执行计划生成
- [x] 2.5 添加"跳过发现"支持（使用默认配置）

## 3. Subagent 调度系统

- [x] 3.1 创建 `subagent-dispatcher` 工具模块
- [x] 3.2 实现 Collect Subagent（读取 + 提取）
- [x] 3.3 实现 Curate Subagent（打分 + 分类）
- [x] 3.4 实现 Write Subagent（笔记生成）
- [x] 3.5 实现 Beautify Subagent（排版美化）
- [x] 3.6 添加 subagent 超时处理（5 分钟）
- [x] 3.7 添加输出验证逻辑

## 4. 自治级别系统

- [x] 4.1 创建 `autonomy-manager` 工具模块
- [x] 4.2 实现 Level 0：每步确认
- [x] 4.3 实现 Level 1：每阶段确认
- [x] 4.4 实现 Level 2：关键点确认
- [x] 4.5 实现 Level 3：全自动
- [x] 4.6 添加自治级别检查点逻辑

## 5. 混合笔记类型

- [x] 5.1 定义混合类型章节顺序模板
- [x] 5.2 实现章节合并逻辑（通过 hybrid-sections.yaml 模板定义）
- [x] 5.3 实现概念类型贡献的章节（在模板中定义）
- [x] 5.4 实现实战类型贡献的章节（在模板中定义）
- [x] 5.5 实现对比类型贡献的章节（在模板中定义）
- [x] 5.6 实现速查类型贡献的章节（在模板中定义）
- [x] 5.7 实现心得类型贡献的章节（在模板中定义）
- [x] 5.8 添加来源追踪逻辑（通过 write subagent prompt 实现）

## 6. 集成与测试

- [x] 6.1 更新 CLAUDE.md 文档
- [x] 6.2 更新 docs/phases.md
- [x] 6.3 创建集成测试用例
- [x] 6.4 测试需求发现 → 收集 → 整理 → 写作完整流程
- [x] 6.5 测试自治级别 0-3 的行为
- [x] 6.6 测试混合笔记类型生成
- [x] 6.7 性能测试：subagent 并行执行
