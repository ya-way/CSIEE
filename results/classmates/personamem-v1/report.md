# CSIEE evaluation

Dataset: `personamem-v1.jsonl` · n=2612 · seed=42 · permutations=10
Expected uniform random accuracy: **25.00%**. Scope: option-only; no question, user history, retrieval, or LLM.

| Strategy | Accuracy | Wilson 95% | Lift (pp) | Shuffled mean | Shuffled range | Same choice |
| :-- | --: | :-- | --: | --: | :-- | --: |
| xiaoming | 44.33% | 42.44%–46.25% | +19.33 | 44.29% | 44.07%–44.45% | 99.06% |
| xiaohong | 21.09% | 19.57%–22.70% | -3.91 | 24.69% | 23.77%–25.92% | 24.52% |
| xiaogang | 52.53% | 50.61%–54.44% | +27.53 | 52.51% | 52.41%–52.68% | 99.47% |
| random | 25.11% | 23.49%–26.81% | +0.11 | 25.34% | 23.77%–26.80% | 24.32% |

Order: native option order.

Wilson 95% intervals assume independent questions; shared personas, scenarios, or task templates can violate this. Shuffle spread is sensitivity to order, not extra independent data.

**Interpretation:** this audits answer-option artifacts. It does not measure end-to-end agent capability or prove that a benchmark is invalid.

SHA-256: `a76c3ea87017957e01d3813f18a5cc15d07742e1ae1daca6eb2b3b6ffdd878a0`
CSIEE 0.2.0 / Python 3.9.13

Source: [PersonaMem-v1 (128k)](https://huggingface.co/datasets/bowen-upenn/PersonaMem-v1)
Revision: `a8076d5608c93ba2a28983cd78aa99b01a163ae7` · License: Consult upstream dataset card

Released MCQ candidates: 2727; included: 2612; excluded: 115. Every excluded ID/reason is in summary.json.
