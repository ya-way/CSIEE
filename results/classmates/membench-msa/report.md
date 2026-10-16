# CSIEE evaluation

Dataset: `membench-msa.jsonl` · n=500 · seed=42 · permutations=10
Expected uniform random accuracy: **25.00%**. Scope: option-only; no question, user history, retrieval, or LLM.

| Strategy | Accuracy | Wilson 95% | Lift (pp) | Shuffled mean | Shuffled range | Same choice |
| :-- | --: | :-- | --: | --: | :-- | --: |
| xiaoming | 100.00% | 99.24%–100.00% | +75.00 | 100.00% | 100.00%–100.00% | 100.00% |
| xiaohong | 24.60% | 21.03%–28.56% | -0.40 | 23.92% | 22.00%–26.60% | 24.98% |
| xiaogang | 63.80% | 59.50%–67.89% | +38.80 | 63.52% | 63.00%–64.20% | 98.72% |
| random | 26.60% | 22.92%–30.64% | +1.60 | 24.76% | 21.20%–29.00% | 24.02% |

Order: native option order.

Wilson 95% intervals assume independent questions; shared personas, scenarios, or task templates can violate this. Shuffle spread is sensitivity to order, not extra independent data.

**Interpretation:** this audits answer-option artifacts. It does not measure end-to-end agent capability or prove that a benchmark is invalid.

SHA-256: `773bc50897b8cbf1a253b5ef7ec5d1a748c8def7f2fd2263427214852e9a4c66`
CSIEE 0.2.0 / Python 3.9.13

Source: [MemBench (multi-session assistant subtask)](https://github.com/import-myself/Membench)
Revision: `f66d8d1028d3f68627d00f77a967b93fbb8694b6` · License: Consult upstream repository terms

Released MCQ candidates: 500; included: 500; excluded: 0. Every excluded ID/reason is in summary.json.
