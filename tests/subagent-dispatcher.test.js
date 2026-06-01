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
