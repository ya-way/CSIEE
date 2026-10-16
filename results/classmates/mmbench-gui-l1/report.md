# CSIEE evaluation

Dataset: `mmbench-gui-l1.jsonl` · n=3561 · seed=42 · permutations=10
Expected uniform random accuracy: **22.08%**. Scope: option-only; no question, user history, retrieval, or LLM.

| Strategy | Accuracy | Wilson 95% | Lift (pp) | Shuffled mean | Shuffled range | Same choice |
| :-- | --: | :-- | --: | --: | :-- | --: |
| xiaoming | 46.28% | 44.65%–47.92% | +24.20 | 45.46% | 44.99%–45.97% | 91.77% |
| xiaohong | 28.39% | 26.93%–29.89% | +6.31 | 22.03% | 20.64%–23.34% | 22.34% |
| xiaogang | 36.06% | 34.50%–37.65% | +13.98 | 35.87% | 35.61%–36.06% | 92.97% |
| random | 21.85% | 20.52%–23.23% | -0.23 | 21.65% | 20.67%–23.22% | 22.24% |

Order: native option order.

Wilson 95% intervals assume independent questions; shared personas, scenarios, or task templates can violate this. Shuffle spread is sensitivity to order, not extra independent data.

**Interpretation:** this audits answer-option artifacts. It does not measure end-to-end agent capability or prove that a benchmark is invalid.

SHA-256: `2a4d1d95b30d0b267e06fcd952ede4740571b87fadc9691f1fa30aa333eb068d`
CSIEE 0.2.0 / Python 3.9.13

Source: [MMBench-GUI (L1)](https://huggingface.co/datasets/OpenGVLab/MMBench-GUI)
Revision: `e27757e3910e0d5995b811f916b509b4e34a4690` · License: Consult upstream dataset card

Released MCQ candidates: 3561; included: 3561; excluded: 0. Every excluded ID/reason is in summary.json.
