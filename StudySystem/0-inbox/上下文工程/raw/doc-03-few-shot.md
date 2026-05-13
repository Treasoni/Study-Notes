# Few-Shot Prompting

- **Source**: https://www.promptingguide.ai/guide/techniques/few-shot
- **Author**: PromptingGuide.ai
- **Date**: 2024
- **Type**: guide

---

## Definition

Few-shot prompting enables in-context learning by providing demonstrations in prompts to improve model performance.

## Key Points

- Works by showing examples (1-shot, 3-shot, 5-shot, etc.) before asking the model to respond
- First emerged when models were scaled to sufficient size
- The label space and input text distribution matter, regardless of label correctness
- Random labels outperform no labels entirely
- Format consistency helps, though newer models show robustness to format variations

## Example (1-shot)

_Prompt:_ "A 'farduddle' means to jump up and down really fast..."
_Output:_ "When we won the game, we all started to farduddle in celebration."

## Limitation

Few-shot prompting struggles with complex reasoning tasks involving multiple steps. For arithmetic and multi-step problems, chain-of-thought prompting is recommended instead.
