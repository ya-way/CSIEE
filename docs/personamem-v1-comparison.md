# PersonaMem-v1 · 128k: paper results and the classmates

![PersonaMem-v1 · 128k, all listed baselines sorted by accuracy](../assets/personamem-v1-comparison.png)

All 15 model rows from Figure 4's **128k upper panel, Overall column**, are retained. The printed two-decimal fractions become integer percentages; neither the Average aggregate nor Random Guess is treated as another model. This is **PersonaMem-v1**, an earlier version of the same family as PersonaMem-v2, not an independent family. CSIEE evaluates 2,612 of 2,727 released 128k questions, excluding 115 duplicate-option records. The initial 32k screen is also retained in the screening ledger; 128k was selected to align with the paper's complete model comparison. Coarse printed precision and differing exclusions preclude a meaningful claimed win over a nearby paper score.

Source: [arXiv:2504.14225v2, Figure 4, upper panel (128k), Overall column](https://arxiv.org/html/2504.14225v2). Model scores are cited, not rerun. All models/configurations in the selected source column(s) are shown; none are filtered by score. Sorting is visual ordering, not a claim of statistical superiority or equivalent agent capability.

## One table, both sources

| Method | Accuracy | Input / protocol | Source | Shuffled mean |
| :-- | --: | :-- | :-- | --: |
| **Xiaogang · outlier** | **52.53%** | Options only | CSIEE: Saved CSIEE counts | 52.51% |
| GPT-4.1 | 52% | 128k conversation history + question | Paper: Figure 4, upper panel (128k), Overall column | — |
| GPT-4.5 | 52% | 128k conversation history + question | Paper: Figure 4, upper panel (128k), Overall column | — |
| Gemini-1.5-Flash | 52% | 128k conversation history + question | Paper: Figure 4, upper panel (128k), Overall column | — |
| o1 | 50% | 128k conversation history + question | Paper: Figure 4, upper panel (128k), Overall column | — |
| Gemini-2.0-Flash | 49% | 128k conversation history + question | Paper: Figure 4, upper panel (128k), Overall column | — |
| Gemini-2.0-Flash-Lite | 48% | 128k conversation history + question | Paper: Figure 4, upper panel (128k), Overall column | — |
| o4-mini | 48% | 128k conversation history + question | Paper: Figure 4, upper panel (128k), Overall column | — |
| DeepSeek-R1-671B | 45% | 128k conversation history + question | Paper: Figure 4, upper panel (128k), Overall column | — |
| GPT-4o | 45% | 128k conversation history + question | Paper: Figure 4, upper panel (128k), Overall column | — |
| **Xiaoming · longest** | **44.33%** | Options only | CSIEE: Saved CSIEE counts | 44.29% |
| Llama-4-Maverick | 43% | 128k conversation history + question | Paper: Figure 4, upper panel (128k), Overall column | — |
| GPT-4o-mini | 39% | 128k conversation history + question | Paper: Figure 4, upper panel (128k), Overall column | — |
| o3-mini | 39% | 128k conversation history + question | Paper: Figure 4, upper panel (128k), Overall column | — |
| Llama-3.1-8B | 31% | 128k conversation history + question | Paper: Figure 4, upper panel (128k), Overall column | — |
| Claude-3.5-Haiku | 30% | 128k conversation history + question | Paper: Figure 4, upper panel (128k), Overall column | — |
| Claude-3.7-Sonnet | 26% | 128k conversation history + question | Paper: Figure 4, upper panel (128k), Overall column | — |
| **Xiaohong · C** | **21.09%** | Options only | CSIEE: Saved CSIEE counts | 24.69% |
| Uniform chance | 25.00% | Options only | Analytical expectation | — |

Local bars use input-order results, seed 42. “—” means unavailable for this exact metric, not zero. Shuffled controls are reported only where the saved aggregate uses the same question set and weighting as the chart. Full-screen controls remain in the original reports.

## Reproduce and inspect

- [Paper-value transcription](../data/paper/personamem-v1-128k.json)
- [Local summary](../results/classmates/personamem-v1/summary.json) and [predictions](../results/classmates/personamem-v1/predictions.jsonl)
- [PNG](../assets/personamem-v1-comparison.png) / [SVG](../assets/personamem-v1-comparison.svg)
- [Renderer](../scripts/render_benchmarks.py) / [all ten comparisons](benchmark-comparisons.md)

Local dataset SHA-256: `a76c3ea87017957e01d3813f18a5cc15d07742e1ae1daca6eb2b3b6ffdd878a0`.

```bash
python -m pip install matplotlib==3.9.4
python scripts/render_benchmarks.py
```

Rendering uses committed numerical records only; no API calls or raw dataset downloads are required. Matplotlib is an optional figure-building dependency.
