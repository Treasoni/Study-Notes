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
