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
