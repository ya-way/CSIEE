# CSIEE evaluation

Dataset: `personamem-v2.csv` · n=5000 · seed=42 · permutations=10
Expected uniform random accuracy: **25.00%**. Scope: option-only; no question, user history, retrieval, or LLM.

| Strategy | Accuracy | Wilson 95% | Lift (pp) | Shuffled mean | Shuffled range | Same choice |
| :-- | --: | :-- | --: | --: | :-- | --: |
| xiaoming | 45.62% | 44.24%–47.00% | +20.62 | 45.59% | 45.48%–45.70% | 98.73% |
| xiaohong | 24.68% | 23.50%–25.89% | -0.32 | 25.22% | 24.08%–26.08% | 25.03% |
| xiaogang | 36.90% | 35.57%–38.25% | +11.90 | 37.05% | 36.92%–37.20% | 99.13% |
| random | 24.44% | 23.27%–25.65% | -0.56 | 25.11% | 24.70%–25.76% | 24.79% |

Order: seeded reconstruction; NOT official evaluation order.

Wilson 95% intervals assume independent questions; shared personas, scenarios, or task templates can violate this. Shuffle spread is sensitivity to order, not extra independent data.

**Interpretation:** this audits answer-option artifacts. It does not measure end-to-end agent capability or prove that a benchmark is invalid.

SHA-256: `95f2a8a324aab7baf2af937feae12731369e2abf7cad5ab3e170594cb25a3e52`
CSIEE 0.2.0 / Python 3.9.13

Source: [bowen-upenn/PersonaMem-v2](https://huggingface.co/datasets/bowen-upenn/PersonaMem-v2/resolve/ed956dea41521fc4499acbc63f966e0fd3c053ba/benchmark/text/benchmark.csv)
Revision: `ed956dea41521fc4499acbc63f966e0fd3c053ba` · License: CC-BY-4.0 (upstream data)
