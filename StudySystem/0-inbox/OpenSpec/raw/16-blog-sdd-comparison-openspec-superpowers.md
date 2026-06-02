Source: https://www.cnblogs.com/kybs0/p/19770771 (search result summary)
also from: https://wnote.com/post/ai-sdd-openspec-speckit/

# SDD Tool Comparisons

## OpenSpec vs SuperPowers

**Source:** cnblogs.com/kybs0 (March 2026)

| Aspect | OpenSpec | SuperPowers |
|--------|----------|-------------|
| Approach | Spec-driven change management | Multi-agent (Controller + Implementer + Reviewer) |
| AI model | Single-agent | Multi-agent orchestration |
| Testing | Manual verification | Enforced TDD |
| Git strategy | Standard Git | git worktree |
| Strength | Decision traceability, knowledge accumulation | Review automation, TDD enforcement |

**Verdict:** They're complementary. Use OpenSpec for spec management, borrow Superpowers' review and TDD patterns.

## OpenSpec vs Spec Kit

**Source:** wnote.com (2026)

| Aspect | OpenSpec | Spec Kit |
|--------|----------|----------|
| Weight | Lightweight | Heavyweight |
| Phase gates | None (fluid) | Strict phase gates |
| Brownfield | Native (delta specs) | Requires full rewrites |
| Ecosystem | Tool-agnostic (30+ tools) | Tied to GitHub |
| Cost | Free (MIT) | Part of GitHub ecosystem |
| Learning curve | Low | Higher |

## OpenSpec vs Kiro (AWS)

| Aspect | OpenSpec | Kiro |
|--------|----------|------|
| IDE lock-in | None | Tied to Kiro IDE |
| Model lock-in | Any | Limited model selection |
| Brownfield | Native | Limited |
| Cost | Free (MIT) | AWS-linked |

## OpenSpec vs No SDD ("Vibe Coding")

| Aspect | OpenSpec | No SDD |
|--------|----------|--------|
| AI behavior | Predictable, scoped | Unpredictable, drifts |
| Context across sessions | Persistent (specs/) | Lost in chat history |
| Change traceability | Full audit trail | Non-existent |
| Rework frequency | Low | High |
| Setup time | ~5 minutes | None |
| Cognitive overhead | Moderate (write specs) | Low initially, high later |
