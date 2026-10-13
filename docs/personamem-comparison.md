# PersonaMem-v2: paper results meet the classmates

![Combined paper and CSIEE MCQ comparison](../assets/personamem-comparison.png)

The compact figure retains four paper references: the agentic-memory model, mixed-reward GRPO, the strongest 32k frontier model (GPT-5-mini), and GPT-5-Chat. Base/SFT models, training ablations, and other frontier variants remain in the complete table below. This selection simplifies the presentation; it does not change any measured result.

## One table, with provenance

| Method | History / memory | MCQ accuracy | Shuffled mean | Source |
| :-- | :-- | --: | --: | :-- |
| GPT-5-mini | 32k history | 48.7% | — | Paper Fig. 4 |
| GPT-5-Chat | 32k history | 45.6% | — | Paper Fig. 4 |
| o4-mini | 32k history | 39.1% | — | Paper Fig. 4 |
| GPT-4.1 | 32k history | 38.7% | — | Paper Fig. 4 |
| GPT-5-nano | 32k history | 37.9% | — | Paper Fig. 4 |
| GPT-4.1-mini | 32k history | 37.6% | — | Paper Fig. 4 |
| Qwen3-4B · Agentic Memory | 2k memory* | 55.2% | — | Paper Fig. 6 |
| Qwen3-4B · GRPO | 32k history | 53.8% | — | Paper Fig. 6 |
| Qwen3-4B · GRPO (MCQ-only) | 32k history | 55.5% | — | Paper Fig. 6 |
| Qwen3-4B · GRPO (OE-only) | 32k history | 35.6% | — | Paper Fig. 6 |
| Qwen3-4B · SFT | 32k history | 35.0% | — | Paper Fig. 6 |
| Qwen3-4B · Base | 32k history | 30.5% | — | Paper Fig. 6 |
| **Xiaoming · longest** | **Options only** | **45.62%** | 45.59% | CSIEE, n=5,000 |
| **Xiaohong · C** | **Options only** | **24.68%** | 25.22% | CSIEE, n=5,000 |
| **Xiaogang · outlier** | **Options only** | **36.90%** | 37.05% | CSIEE, n=5,000 |
| Uniform chance | Options only | 25.00% | 25.00% (expected) | Analytical |

Paper rows are transcribed from the printed **MCQ** labels in [Figure 4](https://arxiv.org/html/2512.06688v1#S4.F4) and [Figure 6](https://arxiv.org/html/2512.06688v1#S4.F6) of Jiang et al., *PersonaMem-v2*, [arXiv:2512.06688v1](https://arxiv.org/abs/2512.06688v1). They are cited results, not our reruns. All six Qwen variants are retained, including both training ablations. OE-only means trained only on open-ended examples; the reported score here is still MCQ accuracy.

\* Agentic Memory constructs up to 2k tokens of memory from 32k history; “2k” is not the total history processed. The other paper rows use 32k conversation histories plus the question and choices. CSIEE sees only the choices and uses all 5,000 text MCQs at the pinned dataset revision, with seed 42 and a reconstructed option order. The local column reports accuracy on that order; the control averages ten label-preserving permutations. Paper permutation controls are unavailable (—), not zero.

The table places both sources on the same accuracy scale, with their different inputs and protocols visible. It does not establish statistical superiority, equivalent personalization ability, or a matched end-to-end comparison. Paper values retain their published one-decimal precision; local values retain two decimals. A 0.02-point difference between 45.62% and 45.6% is not a meaningful win claim, especially with the paper's rounding and different evaluation pipeline.

## The paper's 128k frontier setting

| Frontier model | Paper MCQ · 32k | Paper MCQ · 128k |
| :-- | --: | --: |
| GPT-5-mini | 48.7% | 44.1% |
| GPT-5-Chat | 45.6% | 41.4% |
| o4-mini | 39.1% | 38.9% |
| GPT-4.1 | 38.7% | 38.2% |
| GPT-5-nano | 37.9% | 33.9% |
| GPT-4.1-mini | 37.6% | 37.5% |

The main figure consistently selects the 32k frontier setting rather than choosing each model's best or worst context length. The paper's 128k values are retained here for completeness. Open-ended evaluation scores are excluded throughout.

## Data and rendering

- [Paper-value transcription](../data/paper/personamem-v2-mcq.json), including exact paper version and figure numbers.
- [Local summary](../results/classmates/personamem-v2/summary.json) and [prediction records](../results/classmates/personamem-v2/predictions.jsonl).
- [PNG](../assets/personamem-comparison.png) and [vector SVG](../assets/personamem-comparison.svg).
- [Rendering script](../scripts/render_personamem.py); it generates the image and both Markdown tables from the same records.

```bash
python -m pip install matplotlib==3.9.4
python scripts/render_personamem.py
```

Matplotlib is an optional figure-building dependency. The CSIEE evaluator still has no runtime dependencies. The comparison artwork is an original rendering of cited numerical results; it does not reuse the paper's images.
