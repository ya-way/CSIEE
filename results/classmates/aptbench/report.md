# CSIEE evaluation

Dataset: `aptbench.jsonl` · n=4215 · seed=42 · permutations=10
Expected uniform random accuracy: **20.84%**. Scope: option-only; no question, user history, retrieval, or LLM.

| Strategy | Accuracy | Wilson 95% | Lift (pp) | Shuffled mean | Shuffled range | Same choice |
| :-- | --: | :-- | --: | --: | :-- | --: |
| xiaoming | 16.39% | 15.31%–17.54% | -4.45 | 16.41% | 15.94%–16.73% | 88.79% |
| xiaohong | 20.76% | 19.56%–22.01% | -0.08 | 20.79% | 19.91%–21.71% | 20.83% |
| xiaogang | 11.81% | 10.88%–12.82% | -9.03 | 11.85% | 11.41%–12.10% | 91.54% |
| random | 19.62% | 18.45%–20.85% | -1.22 | 20.92% | 19.81%–21.64% | 20.93% |

Order: native option order.

Wilson 95% intervals assume independent questions; shared personas, scenarios, or task templates can violate this. Shuffle spread is sensitivity to order, not extra independent data.

**Interpretation:** this audits answer-option artifacts. It does not measure end-to-end agent capability or prove that a benchmark is invalid.

SHA-256: `35bf44c9b3c6337565c3871f3dab1d6edf66a165813037b1acdbc4dbf345842b`
CSIEE 0.2.0 / Python 3.9.13

Source: [APTBench](https://github.com/TencentYoutuResearch/APTBench)
Revision: `9aab1301ab2c743be6bf11d1a2f3c3c6bc123ffc` · License: Apache-2.0 (upstream repository)

Released MCQ candidates: 4273; included: 4215; excluded: 58. Every excluded ID/reason is in summary.json.
