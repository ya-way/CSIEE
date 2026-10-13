# CSIEE evaluation

Dataset: `agenthop.jsonl` · n=1011 · seed=42 · permutations=10
Expected uniform random accuracy: **25.00%**. Scope: option-only; no question, user history, retrieval, or LLM.

| Strategy | Accuracy | Wilson 95% | Lift (pp) | Shuffled mean | Shuffled range | Same choice |
| :-- | --: | :-- | --: | --: | :-- | --: |
| xiaoming | 0.89% | 0.47%–1.68% | -24.11 | 0.98% | 0.89%–0.99% | 99.83% |
| xiaohong | 27.50% | 24.83%–30.33% | +2.50 | 25.00% | 23.74%–27.00% | 25.38% |
| xiaogang | 18.40% | 16.13%–20.90% | -6.60 | 18.46% | 18.40%–18.50% | 99.88% |
| random | 26.31% | 23.69%–29.11% | +1.31 | 24.81% | 22.55%–27.00% | 24.69% |

Order: native option order.

Wilson 95% intervals assume independent questions; shared personas, scenarios, or task templates can violate this. Shuffle spread is sensitivity to order, not extra independent data.

**Interpretation:** this audits answer-option artifacts. It does not measure end-to-end agent capability or prove that a benchmark is invalid.

SHA-256: `3f1ea9261f708d27c0d545cac238338abd9161f718be745804b6ec3b1e01147b`
CSIEE 0.2.0 / Python 3.9.13

Source: [AgentHop](https://huggingface.co/datasets/agenthop/agenthop)
Revision: `599b0659343a7a3cc852a60c2e527150121cccdf` · License: CC-BY-4.0

Released MCQ candidates: 1011; included: 1011; excluded: 0. Every excluded ID/reason is in summary.json.
