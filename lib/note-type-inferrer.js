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
