# CSIEE evaluation

Dataset: `gui-world.jsonl` · n=3643 · seed=42 · permutations=10
Expected uniform random accuracy: **25.00%**. Scope: option-only; no question, user history, retrieval, or LLM.

| Strategy | Accuracy | Wilson 95% | Lift (pp) | Shuffled mean | Shuffled range | Same choice |
| :-- | --: | :-- | --: | --: | :-- | --: |
| xiaoming | 51.03% | 49.41%–52.65% | +26.03 | 50.49% | 49.93%–50.92% | 95.18% |
| xiaohong | 41.20% | 39.61%–42.81% | +16.20 | 25.05% | 23.72%–26.30% | 24.98% |
| xiaogang | 41.53% | 39.94%–43.14% | +16.53 | 41.24% | 40.93%–41.70% | 95.35% |
| random | 25.28% | 23.90%–26.72% | +0.28 | 24.95% | 24.18%–26.08% | 24.45% |

Order: native option order.

Wilson 95% intervals assume independent questions; shared personas, scenarios, or task templates can violate this. Shuffle spread is sensitivity to order, not extra independent data.

**Interpretation:** this audits answer-option artifacts. It does not measure end-to-end agent capability or prove that a benchmark is invalid.

SHA-256: `9124023fd8a8df256117eff797628046415b0a4582825eb832c5f3dbd185c6d0`
CSIEE 0.2.0 / Python 3.9.13

Source: [GUI-World (released benchmark MCQs)](https://huggingface.co/datasets/ONE-Lab/GUI-World)
Revision: `7901fa3f0b9e36afa87d24ff9ecd48037c7fd6a0` · License: Consult upstream dataset card

Released MCQ candidates: 3646; included: 3643; excluded: 3. Every excluded ID/reason is in summary.json.
