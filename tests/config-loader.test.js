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

  test('mutation isolation: loadConfig returns independent copies', () => {
    const config1 = loadConfig('/nonexistent/.study-config.yaml');
    const config2 = loadConfig('/nonexistent/.study-config.yaml');

    // Mutate config1
    config1.autonomy.overrides.push({ phase: 'write', level: 0 });
    config1.autonomy.level = 99;

    // config2 should be unaffected
    expect(config2.autonomy.overrides).toHaveLength(0);
    expect(config2.autonomy.level).toBe(1);
  });

  test('loadConfig returns defaults for empty YAML file', () => {
    fs.writeFileSync(testConfigPath, '');
    const config = loadConfig(testConfigPath);
    expect(config.autonomy.level).toBe(1);
    expect(config.autonomy.overrides).toEqual([]);
    expect(config.subagent.timeout).toBe(300000);
    expect(config.requirement_discovery.enabled).toBe(true);
  });
});
