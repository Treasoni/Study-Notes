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

  test('Level 1 does not confirm mid-phase points', () => {
    const manager = new AutonomyManager(1);
    expect(manager.shouldConfirm('collect', 'mid')).toBe(false);
    expect(manager.shouldConfirm('write', 'mid')).toBe(false);
  });

  test('Level 1 confirms start at non-first phases', () => {
    const manager = new AutonomyManager(1);
    expect(manager.shouldConfirm('write', 'start')).toBe(true);
    expect(manager.shouldConfirm('beautify', 'start')).toBe(true);
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
