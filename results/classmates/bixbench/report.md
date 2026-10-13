# CSIEE evaluation

Dataset: `bixbench.jsonl` · n=205 · seed=42 · permutations=10
Expected uniform random accuracy: **25.00%**. Scope: option-only; no question, user history, retrieval, or LLM.

| Strategy | Accuracy | Wilson 95% | Lift (pp) | Shuffled mean | Shuffled range | Same choice |
| :-- | --: | :-- | --: | --: | :-- | --: |
| xiaoming | 26.83% | 21.23%–33.28% | +1.83 | 27.66% | 21.95%–31.71% | 48.83% |
| xiaohong | 26.34% | 20.79%–32.77% | +1.34 | 24.98% | 20.49%–31.71% | 26.59% |
| xiaogang | 19.51% | 14.67%–25.48% | -5.49 | 19.32% | 16.10%–22.44% | 79.51% |
| random | 23.41% | 18.14%–29.67% | -1.59 | 25.32% | 18.54%–27.80% | 28.59% |

Order: seeded native MCQ reconstruction.

Wilson 95% intervals assume independent questions; shared personas, scenarios, or task templates can violate this. Shuffle spread is sensitivity to order, not extra independent data.

**Interpretation:** this audits answer-option artifacts. It does not measure end-to-end agent capability or prove that a benchmark is invalid.

SHA-256: `7ac0c0685911960445adcc3878ce30e785b04cc462741e70129c6605c3aa9732`
CSIEE 0.2.0 / Python 3.9.13

Source: [BixBench v1.5](https://huggingface.co/datasets/futurehouse/BixBench)
Revision: `f8cc3bdcc6357c88b8c3648306522b9c422dc95a` · License: Apache-2.0

Released MCQ candidates: 205; included: 205; excluded: 0. Every excluded ID/reason is in summary.json.
