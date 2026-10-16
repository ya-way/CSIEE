# CSIEE evaluation

Dataset: `perma.jsonl` · n=580 · seed=42 · permutations=10
Expected uniform random accuracy: **12.50%**. Scope: option-only; no question, user history, retrieval, or LLM.

| Strategy | Accuracy | Wilson 95% | Lift (pp) | Shuffled mean | Shuffled range | Same choice |
| :-- | --: | :-- | --: | --: | :-- | --: |
| xiaoming | 93.97% | 91.72%–95.63% | +81.47 | 93.93% | 93.79%–93.97% | 99.97% |
| xiaohong | 14.14% | 11.54%–17.21% | +1.64 | 12.31% | 10.17%–14.31% | 12.47% |
| xiaogang | 91.38% | 88.81%–93.40% | +78.88 | 91.31% | 91.21%–91.38% | 99.93% |
| random | 13.79% | 11.22%–16.84% | +1.29 | 12.17% | 11.03%–13.97% | 12.40% |

Order: native option order.

Wilson 95% intervals assume independent questions; shared personas, scenarios, or task templates can violate this. Shuffle spread is sensitivity to order, not extra independent data.

**Interpretation:** this audits answer-option artifacts. It does not measure end-to-end agent capability or prove that a benchmark is invalid.

SHA-256: `e72aee7e23bdc84ebe586a0219e59c414f61ffe0fee13533bfb8f699b458ae76`
CSIEE 0.2.0 / Python 3.9.13

Source: [PERMA (Type 3)](https://huggingface.co/datasets/ustclsc/PERMA)
Revision: `440e64e4fb8baec6f7ad10c1de135505f93e7cb1` · License: Apache-2.0 (upstream repository)

Released MCQ candidates: 580; included: 580; excluded: 0. Every excluded ID/reason is in summary.json.
