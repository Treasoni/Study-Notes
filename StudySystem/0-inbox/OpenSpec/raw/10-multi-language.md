Source: https://deepwiki.com/Fission-AI/OpenSpec/7.5-multi-language-support

# Multi-Language Support

OpenSpec supports generating planning artifacts (proposals, specs, designs, tasks) in languages other than English through its **Instruction Enrichment Pipeline**. This is configured via the `context` and `rules` fields in the project-level `openspec/config.yaml` file.

## How It Works

The feature leverages the AI's natural language capabilities by injecting linguistic instructions into the prompt. When commands like `/opsx:continue` or `/opsx:propose` are executed, the CLI assembles a prompt combining the base artifact template with project-level context and artifact-specific rules.

## Configuration

To set a global language for all artifacts, add a "Language and Localization" section to the `context` field in `openspec/config.yaml`:

```yaml
# openspec/config.yaml
schema: spec-driven
context: |
  Language Requirements:
  - All artifacts (proposals, specs, designs, tasks) MUST be written in Japanese.
  - Use "Desu/Masu" (polite) tone for proposals and designs.
  - Use "Da/Dearu" (plain/formal) tone for technical specifications.
  - Keep technical terms (e.g., "middleware", "endpoint", "payload") in English where standard.
rules:
  specs:
    - Use Japanese 'Shall' equivalents (〜するものとする) for requirements.
  tasks:
    - Task descriptions should be concise Japanese imperatives.
```

## Language Examples

| Language | Context Instruction Example |
|---|---|
| Spanish | `Escribe todos los documentos en espanol. Utiliza un tono profesional y tecnico.` |
| French | `Redigez tous les documents en francais. Utilisez le futur simple pour les exigences (SHALL).` |
| German | `Alle Dokumente mussen auf Deutsch verfasst sein. Fachbegriffe konnen auf Englisch bleiben.` |
| Chinese | `所有文档必须使用中文编写。需求描述应使用"应当"或"必须"等词汇。` |
| Japanese | `All artifacts MUST be written in Japanese. Use "Desu/Masu" for proposals, "Da/Dearu" for specs.` |
| Traditional Chinese | `所有文件必須使用繁體中文編寫。` |

## Key Customization Details

- **`context` field**: Global background info (<=50KB) injected into all AI instructions -- used for language directives.
- **`rules` field**: Per-artifact constraints (e.g., specific language rules for specs vs. tasks).
- **Technical Terms**: Use `rules` to provide a glossary or translation strategy to avoid "translation fatigue" of industry-standard terms. You can preserve English keywords like `SHALL`/`MUST` for parser compatibility.

## Verification

You can verify the output by running:

```bash
openspec instructions --change <change-id> --artifact proposal
```

This shows the raw instructions being sent to the AI, confirming your language context and rules are correctly injected.

## Community Localization

A community-maintained Chinese localization fork exists: https://github.com/studyzy/OpenSpec-cn (v1.3.1, `@studyzy/openspec-cn` on npm).

Chinese documentation site: https://radebit.github.io/OpenSpec-Docs-zh/
