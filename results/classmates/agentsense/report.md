# CSIEE evaluation

Dataset: `agentsense.jsonl` · n=1863 · seed=42 · permutations=10
Expected uniform random accuracy: **25.00%**. Scope: option-only; no question, user history, retrieval, or LLM.

| Strategy | Accuracy | Wilson 95% | Lift (pp) | Shuffled mean | Shuffled range | Same choice |
| :-- | --: | :-- | --: | --: | :-- | --: |
| xiaoming | 49.87% | 47.60%–52.13% | +24.87 | 49.69% | 49.33%–50.08% | 97.90% |
| xiaohong | 25.17% | 23.26%–27.19% | +0.17 | 25.10% | 24.15%–26.57% | 25.14% |
| xiaogang | 49.44% | 47.17%–51.71% | +24.44 | 49.57% | 49.11%–49.87% | 96.82% |
| random | 23.13% | 21.28%–25.10% | -1.87 | 24.78% | 22.65%–26.95% | 24.91% |

Order: native option order.

Wilson 95% intervals assume independent questions; shared personas, scenarios, or task templates can violate this. Shuffle spread is sensitivity to order, not extra independent data.

**Interpretation:** this audits answer-option artifacts. It does not measure end-to-end agent capability or prove that a benchmark is invalid.

SHA-256: `efbcf0bc3f37b093fe977f579990db79df6b8317a50b1a81f5a0e1ba384805cf`
CSIEE 0.2.0 / Python 3.9.13

Source: [AgentSense](https://github.com/ljcleo/agent_sense)
Revision: `21b6ef909cabcd4a72cded7580869e1e28c0e628` · License: MIT (upstream repository)

Released MCQ candidates: 1864; included: 1863; excluded: 1. Every excluded ID/reason is in summary.json.
