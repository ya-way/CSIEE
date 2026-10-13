# CSIEE evaluation

Dataset: `openbookqa.jsonl` · n=500 · seed=42 · permutations=10
Expected uniform random accuracy: **25.00%**. Scope: option-only; no question, user history, retrieval, or LLM.

| Strategy | Accuracy | Wilson 95% | Lift (pp) | Shuffled mean | Shuffled range | Same choice |
| :-- | --: | :-- | --: | --: | :-- | --: |
| lite | 26.40% | 22.73%–30.43% | +1.40 | 24.88% | 22.20%–29.00% | 25.24% |
| pro | 28.20% | 24.43%–32.30% | +3.20 | 28.54% | 26.60%–31.20% | 44.06% |
| promax | 28.40% | 24.62%–32.51% | +3.40 | 28.24% | 26.40%–30.80% | 43.00% |
| longest | 36.60% | 32.49%–40.91% | +11.60 | 36.22% | 35.00%–37.20% | 92.14% |
| shortest | 17.00% | 13.96%–20.54% | -8.00 | 15.66% | 14.60%–16.60% | 86.06% |
| numeric | 26.40% | 22.73%–30.43% | +1.40 | 24.78% | 22.00%–28.80% | 25.48% |
| cautious | 26.40% | 22.73%–30.43% | +1.40 | 25.04% | 22.80%–28.80% | 25.74% |
| random | 23.20% | 19.71%–27.10% | -1.80 | 24.48% | 22.20%–25.80% | 24.58% |

Order: input order; labels mapped from source.

Wilson 95% intervals assume independent questions; shared personas can violate this. Shuffle spread is sensitivity to order, not extra independent data.

**Interpretation:** this audits answer-option artifacts. It does not measure memory or prove that a benchmark is invalid.

SHA-256: `feb2bd9bfa6161dca4c44ce90e51e8cdada83eb5061407fcdc5005e44aaf2313`
CSIEE 0.1.0 / Python 3.9.13

Source: [allenai/OpenBookQA](https://s3-us-west-2.amazonaws.com/ai2-website/data/OpenBookQA-V1-Sep2018.zip)
Revision: `V1-Sep2018` · License: Unspecified in upstream dataset card; consult upstream terms
