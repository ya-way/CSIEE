# CSIEE evaluation

Dataset: `personamem-v2.csv` · n=5000 · seed=42 · permutations=10
Expected uniform random accuracy: **25.00%**. Scope: option-only; no question, user history, retrieval, or LLM.

| Strategy | Accuracy | Wilson 95% | Lift (pp) | Shuffled mean | Shuffled range | Same choice |
| :-- | --: | :-- | --: | --: | :-- | --: |
| lite | 24.68% | 23.50%–25.89% | -0.32 | 25.22% | 24.08%–26.08% | 25.03% |
| pro | 24.08% | 22.92%–25.28% | -0.92 | 24.63% | 23.62%–25.42% | 27.44% |
| promax | 24.24% | 23.07%–25.45% | -0.76 | 24.76% | 23.74%–25.50% | 26.86% |
| longest | 45.62% | 44.24%–47.00% | +20.62 | 45.59% | 45.48%–45.70% | 98.73% |
| shortest | 23.28% | 22.13%–24.47% | -1.72 | 23.16% | 23.06%–23.24% | 99.37% |
| numeric | 24.68% | 23.50%–25.89% | -0.32 | 25.22% | 24.08%–26.08% | 25.03% |
| cautious | 24.28% | 23.11%–25.49% | -0.72 | 25.02% | 23.64%–25.92% | 28.89% |
| random | 24.44% | 23.27%–25.65% | -0.56 | 25.11% | 24.70%–25.76% | 24.79% |

Order: seeded reconstruction; NOT official evaluation order.

Wilson 95% intervals assume independent questions; shared personas can violate this. Shuffle spread is sensitivity to order, not extra independent data.

**Interpretation:** this audits answer-option artifacts. It does not measure memory or prove that a benchmark is invalid.

SHA-256: `95f2a8a324aab7baf2af937feae12731369e2abf7cad5ab3e170594cb25a3e52`
CSIEE 0.1.0 / Python 3.9.13

Source: [bowen-upenn/PersonaMem-v2](https://huggingface.co/datasets/bowen-upenn/PersonaMem-v2/resolve/ed956dea41521fc4499acbc63f966e0fd3c053ba/benchmark/text/benchmark.csv)
Revision: `ed956dea41521fc4499acbc63f966e0fd3c053ba` · License: CC-BY-4.0 (upstream data)
