# CSIEE evaluation

Dataset: `acpbench.jsonl` · n=895 · seed=42 · permutations=10
Expected uniform random accuracy: **25.00%**. Scope: option-only; no question, user history, retrieval, or LLM.

| Strategy | Accuracy | Wilson 95% | Lift (pp) | Shuffled mean | Shuffled range | Same choice |
| :-- | --: | :-- | --: | --: | :-- | --: |
| xiaoming | 20.22% | 17.72%–22.98% | -4.78 | 19.49% | 18.88%–20.11% | 83.74% |
| xiaohong | 25.25% | 22.51%–28.20% | +0.25 | 24.41% | 22.12%–26.26% | 25.73% |
| xiaogang | 34.08% | 31.05%–37.25% | +9.08 | 33.33% | 32.63%–34.41% | 91.25% |
| random | 29.50% | 26.60%–32.57% | +4.50 | 24.77% | 20.89%–28.60% | 24.64% |

Order: native option order.

Wilson 95% intervals assume independent questions; shared personas, scenarios, or task templates can violate this. Shuffle spread is sensitivity to order, not extra independent data.

**Interpretation:** this audits answer-option artifacts. It does not measure end-to-end agent capability or prove that a benchmark is invalid.

SHA-256: `ad74aefe95ba248961a7672f90d2709c166275b47d26cc3d723ed4aa7a88b9b6`
CSIEE 0.2.0 / Python 3.9.13

Source: [ACPBench](https://github.com/IBM/ACPBench)
Revision: `2ed9c925962d57b275bf8c4e7b5d6f564aac9d6d` · License: CDLA-Permissive-2.0

Released MCQ candidates: 900; included: 895; excluded: 5. Every excluded ID/reason is in summary.json.
