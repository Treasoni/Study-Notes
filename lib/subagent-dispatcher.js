const fs = require('fs');
const path = require('path');

class SubagentDispatcher {
  constructor(systemRoot) {
    this.systemRoot = systemRoot;
  }

  createCollectPrompt(topic, sources) {
    const outputPath = path.join(this.systemRoot, '0-inbox', topic, 'raw') + '/';
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
    const inputPath = path.join(this.systemRoot, '0-inbox', topic) + '/';
    const outputPath = path.join(this.systemRoot, '1-curated', topic) + '/';
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
    const inputPath = path.join(this.systemRoot, '1-curated', topic) + '/';
    const outputPath = path.join(this.systemRoot, '2-drafts', topic) + '/';
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
    const inputPath = path.join(this.systemRoot, '2-drafts', topic) + '/';
    const outputPath = path.join(this.systemRoot, '3-published', topic) + '/';
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
