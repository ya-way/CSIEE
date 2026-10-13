# CSIEE evaluation

Dataset: `fdabench.jsonl` · n=237 · seed=42 · permutations=10
Expected uniform random accuracy: **25.00%**. Scope: option-only; no question, user history, retrieval, or LLM.

| Strategy | Accuracy | Wilson 95% | Lift (pp) | Shuffled mean | Shuffled range | Same choice |
| :-- | --: | :-- | --: | --: | :-- | --: |
| xiaoming | 13.08% | 9.37%–17.97% | -11.92 | 14.09% | 12.66%–15.61% | 88.23% |
| xiaohong | 20.68% | 16.01%–26.28% | -4.32 | 25.61% | 21.10%–30.80% | 25.19% |
| xiaogang | 9.28% | 6.21%–13.65% | -15.72 | 10.51% | 8.86%–11.39% | 91.94% |
| random | 24.89% | 19.82%–30.77% | -0.11 | 25.44% | 20.68%–30.38% | 23.92% |

Order: native option order.

Wilson 95% intervals assume independent questions; shared personas, scenarios, or task templates can violate this. Shuffle spread is sensitivity to order, not extra independent data.

**Interpretation:** this audits answer-option artifacts. It does not measure end-to-end agent capability or prove that a benchmark is invalid.

SHA-256: `c3beac3645ece1bea6a6556dd940a12ec1b412c2060676da174bad5bc909943c`
CSIEE 0.2.0 / Python 3.9.13

Source: [FDABench-Full (public labeled single-choice subset)](https://huggingface.co/datasets/FDAbench2026/FDAbench-Full)
Revision: `0e05e5ec2c95fbe462bed0cba1882f99989ab34e` · License: MIT (upstream dataset card)

Released MCQ candidates: 579; included: 237; excluded: 342. Every excluded ID/reason is in summary.json.
