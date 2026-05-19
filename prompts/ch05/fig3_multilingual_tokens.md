# Figure 5.3: Multilingual Token Efficiency

**Filename**: `multilingual_tokens.png`
**LaTeX label**: `fig:multilingual-tokens`
**Caption**: Multilingual token efficiency. The same semantic content requires dramatically different numbers of tokens across languages. English text is the most efficiently tokenized because most BPE vocabularies are trained primarily on English data.

## Prompt

```
Draw a multilingual tokenization efficiency comparison for a graduate-level
machine learning textbook. Use the course's blue-white visual system. Landscape
orientation, polished editorial style.

LAYOUT:
A horizontal bar chart showing approximate token counts for the SAME semantic
content in different languages, using a GPT-style English-heavy BPE tokenizer.

The phrase being tokenized: "Hello, how are you today?"
(shown at the top of the figure in a header box)

BARS (top to bottom). Treat these as illustrative counts, not benchmark claims:
1. English: "Hello, how are you today?" — 7 tokens
   Show the actual token pills: ["Hello", ",", " how", " are", " you", " today", "?"]
   Bar color: blue (#2D8CFF)

2. Spanish: "Hola, como estas hoy?" — 10 tokens
   Show token pills (can abbreviate): ["Hol", "a", ",", " como", " est", "as", " hoy", "?"]
   Bar color: lighter blue (#5BA3FF)

3. Chinese: "你好，你今天怎么样？" — 15 tokens
   Show token pills as mostly single-character or byte sequences
   Bar color: medium blue (#4A96FF)

4. Japanese: "こんにちは、今日はお元気ですか？" — 20 tokens
   Show many small tokens (most characters split into bytes)
   Bar color: steel blue (#3D8BF0)

5. Arabic: "مرحبا، كيف حالك اليوم؟" — 18 tokens
   Bar color: deeper blue (#2D7AE0)

RIGHT SIDE ANNOTATIONS:
- Next to English bar: "1x (baseline)"
- Next to Japanese bar: "~3x token cost" in orange (#FF9F43) — this is the
  orange accent, highlighting the unfairness

BOTTOM ANNOTATION (centered):
"Same meaning, different token budget. English-heavy vocabularies can create a
structural compute tax for other languages."

VISUAL DETAILS:
- Horizontal bar chart style
- Bars extend from left to right proportional to token count
- Each bar shows the number at its end (e.g., "7 tokens", "20 tokens")
- Token pills shown INSIDE or BELOW each bar
- English tokens are larger/wider (common words = single tokens)
- Japanese/Chinese tokens are tiny (characters split into bytes)
- Background: white (#FAFCFF)
- Grid lines: very faint gray
- The contrast between English (few large tokens) and Japanese (many tiny tokens)
  should be visually striking
- Only ONE orange element: the "~3x token cost" annotation
```

## Review Checklist

- [ ] 5 languages shown with same semantic content
- [ ] English has fewest tokens (~7), Japanese/Arabic most (~18-20)
- [ ] Token pills visible, showing English has large tokens vs CJK has tiny ones
- [ ] Bar lengths proportional to token counts
- [ ] Orange accent ONLY on the token-cost annotation (not on bars)
- [ ] Bottom annotation explains the structural unfairness
- [ ] Counts are presented as illustrative approximations, not exact benchmark data
- [ ] Clean bar chart layout, easy to read at a glance
- [ ] No extra colors beyond blue family + white + orange + gray
