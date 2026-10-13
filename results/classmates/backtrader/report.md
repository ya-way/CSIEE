# CSIEE evaluation

Dataset: `backtrader.jsonl` · n=160 · seed=42 · permutations=10
Expected uniform random accuracy: **25.00%**. Scope: option-only; no question, user history, retrieval, or LLM.

| Strategy | Accuracy | Wilson 95% | Lift (pp) | Shuffled mean | Shuffled range | Same choice |
| :-- | --: | :-- | --: | --: | :-- | --: |
| xiaoming | 22.50% | 16.72%–29.57% | -2.50 | 24.25% | 18.12%–29.38% | 34.56% |
| xiaohong | 26.88% | 20.61%–34.23% | +1.87 | 25.69% | 16.88%–31.25% | 25.13% |
| xiaogang | 24.38% | 18.37%–31.58% | -0.63 | 27.06% | 25.00%–31.25% | 62.69% |
| random | 25.62% | 19.49%–32.91% | +0.62 | 26.06% | 18.12%–29.38% | 26.19% |

Order: native option order.

Wilson 95% intervals assume independent questions; shared personas, scenarios, or task templates can violate this. Shuffle spread is sensitivity to order, not extra independent data.

**Interpretation:** this audits answer-option artifacts. It does not measure end-to-end agent capability or prove that a benchmark is invalid.

SHA-256: `50604b8731830e276f61e5ba5ce1275da9386aa2db95d42b54b6e74bcdbfec66`
CSIEE 0.2.0 / Python 3.9.13

Source: [Backtrader-Bench](https://github.com/rzhao999/Backtrader-Bench)
Revision: `a623e5d3e55126142a163c43f57ebc5d7178f316` · License: No explicit dataset license found; consult upstream terms

Released MCQ candidates: 160; included: 160; excluded: 0. Every excluded ID/reason is in summary.json.
