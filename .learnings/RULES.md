# Rules
Compressed, deduplicated learnings from past sessions.

## Do
- Use subagents (researcher/curator/writer/editor) for Study System phases — do not skip (3x)
- Use opencli web read as fallback when defuddle returns 403/timeout

## Don't
- Never skip subagent invocation in /learn or /update workflows — every phase must use its designated subagent (3x)
- Never use WebSearch/WebFetch when opencli tools are available for network operations

## Watch For
- Vault config path may be incorrect on first run — validate before starting
- defuddle can return 403 for some official sites (e.g. openai.com); have `opencli web read` ready as fallback (2x)
- Chinese community sites (zhihu, cnblogs) may block defuddle — prepare alternative fetch strategy
- In beautify phase, verify section headings match their content to catch typos
