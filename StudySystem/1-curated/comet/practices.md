# Practices — Comet

## Practice 1: 安装与初始化

```bash
# 全局安装
npm install -g @rpamis/comet

# 在项目中初始化
cd your-project
comet init
```

`comet init` 会：
1. 选择 AI 平台（自动检测已有配置）
2. 选择安装范围（项目级/全局）
3. 选择语言（English/中文）
4. 安装 OpenSpec 和 Superpowers 技能
5. 部署 Comet 技能到所选平台
6. 创建 `docs/superpowers/specs/` 和 `docs/superpowers/plans/` 工作目录

[来源: 1][来源: 2]

## Practice 2: 启动工作流

```bash
# 主入口，自动检测阶段
/comet

# 或按阶段手动执行
/comet-open    # 开启变更
/comet-design  # 深度设计
/comet-build   # 计划与构建
/comet-verify  # 验证与收尾
/comet-archive # 归档变更
```

[来源: 1][来源: 2]

## Practice 3: 实战——看板系统搭建 (30分钟)

来自腾讯云实战指南 [来源: 5] 的完整流程：

### Step 1: OpenSpec 提案
```bash
/opsx:propose 搭建看板管理系统
```
生成：
- `proposal.md` — 为什么做、做什么
- `specs/` — Given/When/Then 格式场景
- `design.md` — 技术方案和架构决策
- `tasks.md` — 可执行任务清单

### Step 2: Comet 编排
- Comet 检测到 OpenSpec 产物后自动进入 Design 阶段
- 触发 Superpowers brainstorming
- 生成详细的 Design Doc

### Step 3: Superpowers TDD 执行
- Subagent 按任务清单逐个实现
- Implementer 写代码 + 测试
- Spec Reviewer 审查规格符合性
- Quality Reviewer 审查代码质量

### Step 4: 验证与归档
- Comet 运行 guard 脚本验证
- 通过后自动归档

## Practice 4: 技能组合参考

Comet 项目展示了如何自由组合不同的 Skill：
- 用 OpenSpec 的 Spec 管理能力（提案 + 归档）
- 用 Superpowers 的 TDD 驱动编码（而不是 OpenSpec 的 apply）
- 通过 Comet 自动串联

[来源: 1][来源: 2]

## Practice 5: 跨平台安装

Comet 支持多种 AI 编码平台的 Skill 分发：
- Claude Code
- Cursor
- Windsurf
- Copilot
- Cline
- 其他平台（Antigravity 等）

不同平台的项目级和全局路径差异由 Comet CLI 安装器自动处理。

[来源: 1][来源: 2]
