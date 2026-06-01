---
archived-with: 2026-06-01-study-system-refactor
status: final
---
# Study System Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor Study System to reduce context overflow, add autonomy levels, support hybrid note types, and add requirement discovery.

**Architecture:** Hub-and-Spoke pattern with Main Agent as coordinator and dedicated Subagents for heavy computation. File-based communication between agents.

**Tech Stack:** Claude Code Agent tool, YAML config, Markdown templates

---
change: study-system-refactor
design-doc: docs/superpowers/specs/2026-06-01-study-system-refactor-design.md
base-ref: bcda7a9221ab10de5d5d60bf3fbbbf9b65aa4a3b

---

## File Structure

```
study-system/
├── .study-config.yaml                    # NEW: Configuration file
├── lib/
│   ├── config-loader.js                  # NEW: Config reader
│   ├── autonomy-manager.js               # NEW: Autonomy level manager
│   ├── subagent-dispatcher.js            # NEW: Subagent orchestrator
│   └── note-type-inferrer.js             # NEW: Note type inference
├── .claude/skills/
│   └── requirement-discovery/
│       └── SKILL.md                      # NEW: Discovery skill
├── templates/
│   └── hybrid-sections.yaml              # NEW: Hybrid section templates
└── tests/
    ├── config-loader.test.js             # NEW
    ├── autonomy-manager.test.js          # NEW
    ├── subagent-dispatcher.test.js       # NEW
    └── note-type-inferrer.test.js        # NEW
```

---

## Task 1: Configuration System

**Files:**
- Create: `.study-config.yaml`
- Create: `lib/config-loader.js`
- Create: `tests/config-loader.test.js`

- [ ] **Step 1: Create config file structure**

```yaml
# .study-config.yaml
autonomy:
  level: 1  # 0-3: 0=every step, 1=phase boundary, 2=key points, 3=auto
  overrides: []
  # Example override:
  # - phase: write
  #   level: 0

subagent:
  timeout: 300000  # 5 minutes in ms
  retry_count: 1

requirement_discovery:
  enabled: true
  min_questions: 4
  max_questions: 6
  allow_skip: true

hybrid_notes:
  max_types: 2
```

- [ ] **Step 2: Write config loader test**

```javascript
// tests/config-loader.test.js
const { loadConfig, getAutonomyLevel, getSubagentTimeout } = require('../lib/config-loader');
const fs = require('fs');
const path = require('path');

describe('config-loader', () => {
  const testConfigPath = path.join(__dirname, '.test-study-config.yaml');
  
  afterEach(() => {
    if (fs.existsSync(testConfigPath)) {
      fs.unlinkSync(testConfigPath);
    }
  });

  test('loadConfig returns default config when file missing', () => {
    const config = loadConfig('/nonexistent/.study-config.yaml');
    expect(config.autonomy.level).toBe(1);
    expect(config.subagent.timeout).toBe(300000);
  });

  test('loadConfig reads yaml file correctly', () => {
    fs.writeFileSync(testConfigPath, `
autonomy:
  level: 2
  overrides:
    - phase: write
      level: 0
`);
    const config = loadConfig(testConfigPath);
    expect(config.autonomy.level).toBe(2);
    expect(config.autonomy.overrides[0].phase).toBe('write');
    expect(config.autonomy.overrides[0].level).toBe(0);
  });

  test('getAutonomyLevel returns override when exists', () => {
    const config = {
      autonomy: {
        level: 1,
        overrides: [{ phase: 'write', level: 0 }]
      }
    };
    expect(getAutonomyLevel(config, 'write')).toBe(0);
    expect(getAutonomyLevel(config, 'collect')).toBe(1);
  });

  test('getSubagentTimeout returns configured value', () => {
    const config = { subagent: { timeout: 600000 } };
    expect(getSubagentTimeout(config)).toBe(600000);
  });
});
```

- [ ] **Step 3: Run test to verify it fails**

Run: `npm test tests/config-loader.test.js`
Expected: FAIL with "Cannot find module '../lib/config-loader'"

- [ ] **Step 4: Implement config loader**

```javascript
// lib/config-loader.js
const fs = require('fs');
const yaml = require('js-yaml');

const DEFAULT_CONFIG = {
  autonomy: {
    level: 1,
    overrides: []
  },
  subagent: {
    timeout: 300000,
    retry_count: 1
  },
  requirement_discovery: {
    enabled: true,
    min_questions: 4,
    max_questions: 6,
    allow_skip: true
  },
  hybrid_notes: {
    max_types: 2
  }
};

function loadConfig(configPath) {
  try {
    if (fs.existsSync(configPath)) {
      const content = fs.readFileSync(configPath, 'utf8');
      const userConfig = yaml.load(content);
      return mergeConfig(DEFAULT_CONFIG, userConfig);
    }
  } catch (e) {
    console.warn(`Failed to load config from ${configPath}:`, e.message);
  }
  return DEFAULT_CONFIG;
}

function mergeConfig(defaults, user) {
  const result = { ...defaults };
  for (const key of Object.keys(user || {})) {
    if (typeof defaults[key] === 'object' && !Array.isArray(defaults[key])) {
      result[key] = mergeConfig(defaults[key], user[key]);
    } else {
      result[key] = user[key];
    }
  }
  return result;
}

function getAutonomyLevel(config, phase) {
  const override = config.autonomy.overrides.find(o => o.phase === phase);
  return override ? override.level : config.autonomy.level;
}

function getSubagentTimeout(config) {
  return config.subagent.timeout;
}

module.exports = { loadConfig, getAutonomyLevel, getSubagentTimeout, DEFAULT_CONFIG };
```

- [ ] **Step 5: Run test to verify it passes**

Run: `npm test tests/config-loader.test.js`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add .study-config.yaml lib/config-loader.js tests/config-loader.test.js
git commit -m "feat: add configuration system with autonomy levels"
```

---

## Task 2: Autonomy Manager

**Files:**
- Create: `lib/autonomy-manager.js`
- Create: `tests/autonomy-manager.test.js`

- [ ] **Step 1: Write autonomy manager test**

```javascript
// tests/autonomy-manager.test.js
const { AutonomyManager, CONFIRMATION_POINTS } = require('../lib/autonomy-manager');

describe('AutonomyManager', () => {
  test('Level 0 requires confirmation at every point', () => {
    const manager = new AutonomyManager(0);
    expect(manager.shouldConfirm('collect', 'start')).toBe(true);
    expect(manager.shouldConfirm('collect', 'mid')).toBe(true);
    expect(manager.shouldConfirm('collect', 'end')).toBe(true);
  });

  test('Level 1 requires confirmation only at phase boundaries', () => {
    const manager = new AutonomyManager(1);
    expect(manager.shouldConfirm('collect', 'start')).toBe(false);
    expect(manager.shouldConfirm('collect', 'end')).toBe(true);
    expect(manager.shouldConfirm('curate', 'start')).toBe(true);
  });

  test('Level 2 requires confirmation only at critical points', () => {
    const manager = new AutonomyManager(2);
    expect(manager.shouldConfirm('write', 'note_type_selection')).toBe(true);
    expect(manager.shouldConfirm('write', 'plan_approval')).toBe(true);
    expect(manager.shouldConfirm('write', 'final_review')).toBe(true);
    expect(manager.shouldConfirm('collect', 'start')).toBe(false);
  });

  test('Level 3 requires confirmation only at final review', () => {
    const manager = new AutonomyManager(3);
    expect(manager.shouldConfirm('any', 'final_review')).toBe(true);
    expect(manager.shouldConfirm('any', 'start')).toBe(false);
    expect(manager.shouldConfirm('any', 'end')).toBe(false);
  });

  test('getStatusMessage returns appropriate message', () => {
    const manager = new AutonomyManager(1);
    const msg = manager.getStatusMessage('collect', 'curate');
    expect(msg).toContain('Auto');
    expect(msg).toContain('collect');
    expect(msg).toContain('curate');
    expect(msg).toContain('1');
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npm test tests/autonomy-manager.test.js`
Expected: FAIL with "Cannot find module '../lib/autonomy-manager'"

- [ ] **Step 3: Implement autonomy manager**

```javascript
// lib/autonomy-manager.js

const CONFIRMATION_POINTS = {
  PHASE_BOUNDARY: 'phase_boundary',
  NOTE_TYPE_SELECTION: 'note_type_selection',
  PLAN_APPROVAL: 'plan_approval',
  FINAL_REVIEW: 'final_review'
};

const CRITICAL_POINTS = [
  CONFIRMATION_POINTS.NOTE_TYPE_SELECTION,
  CONFIRMATION_POINTS.PLAN_APPROVAL,
  CONFIRMATION_POINTS.FINAL_REVIEW
];

class AutonomyManager {
  constructor(level) {
    this.level = Math.max(0, Math.min(3, level));
  }

  shouldConfirm(phase, point) {
    switch (this.level) {
      case 0:
        return true;
      case 1:
        return point === CONFIRMATION_POINTS.PHASE_BOUNDARY;
      case 2:
        return CRITICAL_POINTS.includes(point);
      case 3:
        return point === CONFIRMATION_POINTS.FINAL_REVIEW;
      default:
        return true;
    }
  }

  getStatusMessage(fromPhase, toPhase) {
    return `[Auto] ${fromPhase} complete, proceeding to ${toPhase} (autonomy level: ${this.level})`;
  }

  getLevel() {
    return this.level;
  }
}

module.exports = { AutonomyManager, CONFIRMATION_POINTS, CRITICAL_POINTS };
```

- [ ] **Step 4: Run test to verify it passes**

Run: `npm test tests/autonomy-manager.test.js`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add lib/autonomy-manager.js tests/autonomy-manager.test.js
git commit -m "feat: add autonomy manager with 4 levels"
```

---

## Task 3: Note Type Inferrer

**Files:**
- Create: `lib/note-type-inferrer.js`
- Create: `tests/note-type-inferrer.test.js`

- [ ] **Step 1: Write note type inferrer test**

```javascript
// tests/note-type-inferrer.test.js
const { inferNoteType, NOTES_TYPES } = require('../lib/note-type-inferrer');

describe('note-type-inferrer', () => {
  test('exam purpose infers concept + cheat_sheet', () => {
    const answers = { purpose: 'exam', audience: 'self', depth: 'beginner', usage: 'review' };
    const types = inferNoteType(answers);
    expect(types).toContain('concept');
    expect(types).toContain('cheat_sheet');
    expect(types.length).toBeLessThanOrEqual(2);
  });

  test('work purpose infers practice + compare', () => {
    const answers = { purpose: 'work', audience: 'team', depth: 'advanced', usage: 'learning' };
    const types = inferNoteType(answers);
    expect(types).toContain('practice');
    expect(types).toContain('compare');
  });

  test('interest purpose infers concept', () => {
    const answers = { purpose: 'interest', audience: 'self', depth: 'intermediate', usage: 'learning' };
    const types = inferNoteType(answers);
    expect(types).toContain('concept');
  });

  test('sharing usage adds practice if not present', () => {
    const answers = { purpose: 'interest', audience: 'community', depth: 'advanced', usage: 'sharing' };
    const types = inferNoteType(answers);
    expect(types).toContain('practice');
  });

  test('limits to 2 types maximum', () => {
    const answers = { purpose: 'work', audience: 'community', depth: 'expert', usage: 'sharing' };
    const types = inferNoteType(answers);
    expect(types.length).toBeLessThanOrEqual(2);
  });

  test('returns valid note types', () => {
    const answers = { purpose: 'exam', audience: 'self', depth: 'beginner', usage: 'review' };
    const types = inferNoteType(answers);
    types.forEach(type => {
      expect(NOTES_TYPES).toContain(type);
    });
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npm test tests/note-type-inferrer.test.js`
Expected: FAIL with "Cannot find module '../lib/note-type-inferrer'"

- [ ] **Step 3: Implement note type inferrer**

```javascript
// lib/note-type-inferrer.js

const NOTES_TYPES = ['concept', 'practice', 'compare', 'cheat_sheet', 'experience'];

const PURPOSE_TYPE_MAP = {
  exam: ['concept', 'cheat_sheet'],
  work: ['practice', 'compare'],
  interest: ['concept']
};

function inferNoteType(answers) {
  const types = [];
  
  // Primary type from purpose
  const purposeTypes = PURPOSE_TYPE_MAP[answers.purpose] || ['concept'];
  types.push(...purposeTypes);
  
  // Add practice for sharing usage
  if (answers.usage === 'sharing' && !types.includes('practice')) {
    types.push('practice');
  }
  
  // Limit to 2 types
  const uniqueTypes = [...new Set(types)].filter(t => NOTES_TYPES.includes(t));
  return uniqueTypes.slice(0, 2);
}

function getNoteTypeDescription(type) {
  const descriptions = {
    concept: '核心概念解释、原理、关键思想',
    practice: '实战示例、代码片段、操作指南',
    compare: '对比分析、取舍讨论、决策框架',
    cheat_sheet: '速查清单、常见命令、快速参考',
    experience: '学习心得、踩坑经验、个人感悟'
  };
  return descriptions[type] || type;
}

module.exports = { inferNoteType, getNoteTypeDescription, NOTES_TYPES };
```

- [ ] **Step 4: Run test to verify it passes**

Run: `npm test tests/note-type-inferrer.test.js`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add lib/note-type-inferrer.js tests/note-type-inferrer.test.js
git commit -m "feat: add note type inference from user answers"
```

---

## Task 4: Requirement Discovery Skill

**Files:**
- Create: `.claude/skills/requirement-discovery/SKILL.md`

- [ ] **Step 1: Create skill directory**

```bash
mkdir -p .claude/skills/requirement-discovery
```

- [ ] **Step 2: Write skill definition**

```markdown
---
name: requirement-discovery
description: 需求发现阶段。通过结构化问答明确学习目的、目标读者、深度要求、笔记用途，推荐笔记类型组合。触发时机：用户说"我想学X"后，Phase 0。
---

# Skill: requirement-discovery（需求发现）

## 触发时机
用户说"我想学X"或类似表达后。

## 输入
用户的学习主题（topic）。

## 执行步骤

### Step 1: 评估 Topic 复杂度
根据 topic 长度和关键词判断复杂度：
- 简单（1-2 个词）→ 4 个问题
- 中等（3-4 个词）→ 5 个问题
- 复杂（短语或句子）→ 6 个问题

### Step 2: 结构化问答

**核心问题（4 个）：**

1. **学习目的**
   - 考试准备
   - 工作需要
   - 兴趣探索

2. **目标读者**
   - 自己（个人学习）
   - 团队（内部分享）
   - 社区（公开发布）

3. **深度要求**
   - 入门（基础概念 + 简单示例）
   - 进阶（原理 + 最佳实践）
   - 专家（深入机制 + 边界情况）

4. **笔记用途**
   - 快速回顾（速查表）
   - 深度学习（概念 + 实战）
   - 分享传播（完整 + 图表）

**扩展问题（2 个，根据复杂度）：**

5. **特定关注点**（开放题）
   > "这个主题中，你最想深入了解哪个方面？"

6. **已有知识水平**
   - 完全新手
   - 有一些基础
   - 已有经验，想深入

### Step 3: 推荐笔记类型
根据答案推断笔记类型组合：
- 考试 → concept + cheat_sheet
- 工作 → practice + compare
- 兴趣 → concept
- 分享 → 添加 practice

### Step 4: 生成执行计划
- 选定的笔记类型
- 各阶段自治级别
- 预估时间/精力
- 关键检查点

### Step 5: 用户确认
展示推荐结果，等待用户确认或调整。

## 产出
- 笔记类型组合
- 执行计划
- 用户确认状态

## 硬停止 (Hard Stop)
本阶段任务完成。向用户展示推荐结果。
**严禁直接进入 collect 阶段。**
必须等待用户明确确认后才能进入下一阶段。
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/requirement-discovery/
git commit -m "feat: add requirement discovery skill"
```

---

## Task 5: Subagent Dispatcher

**Files:**
- Create: `lib/subagent-dispatcher.js`
- Create: `tests/subagent-dispatcher.test.js`

- [ ] **Step 1: Write subagent dispatcher test**

```javascript
// tests/subagent-dispatcher.test.js
const { SubagentDispatcher, validateOutput } = require('../lib/subagent-dispatcher');

describe('SubagentDispatcher', () => {
  test('createCollectPrompt generates correct prompt', () => {
    const dispatcher = new SubagentDispatcher('/study');
    const prompt = dispatcher.createCollectPrompt('react', ['src1.md', 'src2.md']);
    expect(prompt).toContain('react');
    expect(prompt).toContain('src1.md');
    expect(prompt).toContain('/study/0-inbox/react/raw/');
  });

  test('createCuratePrompt generates correct prompt', () => {
    const dispatcher = new SubagentDispatcher('/study');
    const prompt = dispatcher.createCuratePrompt('react');
    expect(prompt).toContain('react');
    expect(prompt).toContain('/study/0-inbox/react/');
    expect(prompt).toContain('/study/1-curated/react/');
  });

  test('createWritePrompt generates correct prompt', () => {
    const dispatcher = new SubagentDispatcher('/study');
    const prompt = dispatcher.createWritePrompt('react', 'concept');
    expect(prompt).toContain('react');
    expect(prompt).toContain('concept');
    expect(prompt).toContain('/study/1-curated/react/');
    expect(prompt).toContain('/study/2-drafts/react/');
  });

  test('createBeautifyPrompt generates correct prompt', () => {
    const dispatcher = new SubagentDispatcher('/study');
    const prompt = dispatcher.createBeautifyPrompt('react');
    expect(prompt).toContain('react');
    expect(prompt).toContain('/study/2-drafts/react/');
    expect(prompt).toContain('/study/3-published/react/');
  });
});

describe('validateOutput', () => {
  const fs = require('fs');
  const path = require('path');
  const os = require('os');

  test('validateOutput returns true for existing non-empty files', () => {
    const tmpDir = os.tmpdir();
    const testFile = path.join(tmpDir, 'test-output.md');
    fs.writeFileSync(testFile, '# Test');
    
    const result = validateOutput(tmpDir, ['test-output.md']);
    expect(result.valid).toBe(true);
    
    fs.unlinkSync(testFile);
  });

  test('validateOutput returns false for missing files', () => {
    const result = validateOutput('/nonexistent', ['missing.md']);
    expect(result.valid).toBe(false);
    expect(result.errors).toContain('missing.md');
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npm test tests/subagent-dispatcher.test.js`
Expected: FAIL with "Cannot find module '../lib/subagent-dispatcher'"

- [ ] **Step 3: Implement subagent dispatcher**

```javascript
// lib/subagent-dispatcher.js
const fs = require('fs');
const path = require('path');

class SubagentDispatcher {
  constructor(systemRoot) {
    this.systemRoot = systemRoot;
  }

  createCollectPrompt(topic, sources) {
    const outputPath = path.join(this.systemRoot, '0-inbox', topic, 'raw');
    return `你是 Collect Subagent。任务：从以下源提取关键信息。

Topic: ${topic}
Sources: ${sources.join(', ')}
Output Path: ${outputPath}

步骤：
1. 读取每个源文件
2. 提取核心概念、代码示例、关键观点
3. 写入输出目录（每个源一个文件）
4. 完成后返回状态

注意：
- 保持原始含义不变
- 标注来源
- 不要添加自己的理解`;
  }

  createCuratePrompt(topic) {
    const inputPath = path.join(this.systemRoot, '0-inbox', topic);
    const outputPath = path.join(this.systemRoot, '1-curated', topic);
    return `你是 Curate Subagent。任务：整理和评分学习资料。

Input Path: ${inputPath}
Output Path: ${outputPath}

步骤：
1. 读取 raw/ 目录下所有文件
2. 四维度打分（权威性、时效性、完整性、可读性）
3. 去重（保留最高分）
4. 分类（核心概念、实战示例、进阶原理）
5. 标记信息缺口
6. 写入输出目录

产出文件：
- overview.md：知识地图
- core-concepts.md：核心概念
- practices.md：实战示例
- references.md：参考资料
- discarded.md：舍弃的资料`;
  }

  createWritePrompt(topic, noteType) {
    const inputPath = path.join(this.systemRoot, '1-curated', topic);
    const outputPath = path.join(this.systemRoot, '2-drafts', topic);
    return `你是 Write Subagent。任务：根据整理好的资料生成笔记。

Input Path: ${inputPath}
Output Path: ${outputPath}
Note Type: ${noteType}

步骤：
1. 读取整理好的资料
2. 选择对应的笔记模板
3. 提取关键信息
4. 用学习者友好的语言生成笔记
5. 生成思考题
6. 写入输出目录

注意：
- 每个观点标注来源
- 不要编造引用
- 不要添加资料中没有的内容`;
  }

  createBeautifyPrompt(topic) {
    const inputPath = path.join(this.systemRoot, '2-drafts', topic);
    const outputPath = path.join(this.systemRoot, '3-published', topic);
    return `你是 Beautify Subagent。任务：美化和优化笔记排版。

Input Path: ${inputPath}
Output Path: ${outputPath}

步骤：
1. 读取笔记初稿
2. 优化标题层级
3. 添加适当的格式（粗体、列表、代码块）
4. 优化表格排版
5. 添加分隔线
6. 确保 Obsidian 兼容性
7. 写入输出目录

注意：
- 保持内容不变
- 只优化格式和排版
- 确保 wikilink 正确`;
  }
}

function validateOutput(outputDir, expectedFiles) {
  const errors = [];
  for (const file of expectedFiles) {
    const filePath = path.join(outputDir, file);
    if (!fs.existsSync(filePath)) {
      errors.push(file);
    } else if (fs.statSync(filePath).size === 0) {
      errors.push(`${file} (empty)`);
    }
  }
  return {
    valid: errors.length === 0,
    errors
  };
}

module.exports = { SubagentDispatcher, validateOutput };
```

- [ ] **Step 4: Run test to verify it passes**

Run: `npm test tests/subagent-dispatcher.test.js`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add lib/subagent-dispatcher.js tests/subagent-dispatcher.test.js
git commit -m "feat: add subagent dispatcher for collect/curate/write/beautify"
```

---

## Task 6: Hybrid Note Templates

**Files:**
- Create: `templates/hybrid-sections.yaml`

- [ ] **Step 1: Create hybrid sections template**

```yaml
# templates/hybrid-sections.yaml
# Hybrid note type section ordering and merging rules

combinations:
  concept + practice:
    name: "概念实战型"
    sections:
      - id: core_concept
        title: "核心概念"
        source: concept
        priority: 1
      - id: practical_examples
        title: "实战示例"
        source: practice
        priority: 2
      - id: common_patterns
        title: "常见模式"
        source: merged
        priority: 3
      - id: thinking_questions
        title: "思考题"
        source: merged
        priority: 4

  compare + cheat_sheet:
    name: "对比速查型"
    sections:
      - id: comparison_table
        title: "对比分析"
        source: compare
        priority: 1
      - id: quick_reference
        title: "速查清单"
        source: cheat_sheet
        priority: 2
      - id: decision_framework
        title: "决策框架"
        source: merged
        priority: 3
      - id: references
        title: "参考资料"
        source: merged
        priority: 4

  experience + concept:
    name: "心得概念型"
    sections:
      - id: background
        title: "背景上下文"
        source: experience
        priority: 1
      - id: core_concept
        title: "核心概念"
        source: concept
        priority: 2
      - id: insights
        title: "学习心得"
        source: experience
        priority: 3
      - id: further_reading
        title: "延伸阅读"
        source: merged
        priority: 4

  concept + cheat_sheet:
    name: "概念速查型"
    sections:
      - id: core_concept
        title: "核心概念"
        source: concept
        priority: 1
      - id: key_points
        title: "关键要点"
        source: merged
        priority: 2
      - id: quick_reference
        title: "速查清单"
        source: cheat_sheet
        priority: 3
      - id: thinking_questions
        title: "思考题"
        source: merged
        priority: 4

single_types:
  concept:
    sections:
      - core_definition
      - key_principles
      - common_misconceptions
      - related_concepts

  practice:
    sections:
      - real_world_examples
      - code_snippets
      - step_by_step_guide
      - common_pitfalls

  compare:
    sections:
      - comparison_table
      - when_to_use
      - trade_offs
      - decision_framework

  cheat_sheet:
    sections:
      - quick_reference_commands
      - common_patterns
      - troubleshooting
      - one_liner_examples

  experience:
    sections:
      - background_context
      - learning_process
      - key_insights
      - lessons_learned
      - future_directions
```

- [ ] **Step 2: Commit**

```bash
git add templates/hybrid-sections.yaml
git commit -m "feat: add hybrid note type section templates"
```

---

## Task 7: Integration Tests

**Files:**
- Create: `tests/integration.test.js`

- [ ] **Step 1: Write integration test**

```javascript
// tests/integration.test.js
const { loadConfig } = require('../lib/config-loader');
const { AutonomyManager } = require('../lib/autonomy-manager');
const { inferNoteType } = require('../lib/note-type-inferrer');
const { SubagentDispatcher } = require('../lib/subagent-dispatcher');

describe('Integration: Full workflow', () => {
  test('config -> autonomy -> inference -> dispatch flow', () => {
    // Load config
    const config = loadConfig('/nonexistent/.study-config.yaml');
    expect(config.autonomy.level).toBe(1);

    // Create autonomy manager
    const autonomy = new AutonomyManager(config.autonomy.level);
    expect(autonomy.shouldConfirm('collect', 'end')).toBe(true);

    // Infer note type
    const answers = {
      purpose: 'work',
      audience: 'team',
      depth: 'advanced',
      usage: 'learning'
    };
    const noteTypes = inferNoteType(answers);
    expect(noteTypes).toContain('practice');
    expect(noteTypes).toContain('compare');

    // Create dispatcher
    const dispatcher = new SubagentDispatcher('/study');
    const collectPrompt = dispatcher.createCollectPrompt('react', ['doc1.md']);
    expect(collectPrompt).toContain('react');

    const writePrompt = dispatcher.createWritePrompt('react', noteTypes[0]);
    expect(writePrompt).toContain('practice');
  });

  test('autonomy level 3 bypasses most confirmations', () => {
    const autonomy = new AutonomyManager(3);
    
    // Should only confirm at final review
    expect(autonomy.shouldConfirm('collect', 'start')).toBe(false);
    expect(autonomy.shouldConfirm('collect', 'end')).toBe(false);
    expect(autonomy.shouldConfirm('curate', 'start')).toBe(false);
    expect(autonomy.shouldConfirm('write', 'note_type_selection')).toBe(false);
    expect(autonomy.shouldConfirm('any', 'final_review')).toBe(true);
  });

  test('hybrid note type inference limits to 2 types', () => {
    const answers = {
      purpose: 'work',
      audience: 'community',
      depth: 'expert',
      usage: 'sharing'
    };
    const noteTypes = inferNoteType(answers);
    expect(noteTypes.length).toBeLessThanOrEqual(2);
  });
});
```

- [ ] **Step 2: Run integration test**

Run: `npm test tests/integration.test.js`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/integration.test.js
git commit -m "test: add integration tests for full workflow"
```

---

## Task 8: Documentation Update

**Files:**
- Modify: `CLAUDE.md`
- Modify: `docs/phases.md`

- [ ] **Step 1: Update CLAUDE.md**

Add new sections to CLAUDE.md:
- Configuration section with .study-config.yaml
- Autonomy levels documentation
- Requirement discovery phase
- Hybrid note types

- [ ] **Step 2: Update docs/phases.md**

Add Phase 0: Requirement Discovery details.

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md docs/phases.md
git commit -m "docs: update documentation for new features"
```

---

## Summary

**Total Tasks:** 8
**Total Steps:** 32
**Estimated Time:** 4-6 hours

**Dependencies:**
- Task 1 (Config) → Task 2 (Autonomy)
- Task 1 (Config) → Task 3 (Inference)
- Task 2, 3 → Task 4 (Discovery Skill)
- Task 1 → Task 5 (Dispatcher)
- All → Task 7 (Integration)
- All → Task 8 (Docs)
