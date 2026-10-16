# PersonaMem-v2: paper results and the classmates

![PersonaMem-v2, all listed baselines sorted by accuracy](../assets/personamem-comparison.png)

All 12 paper configurations from Figures 4 and 6 are shown, including Base, SFT and both GRPO training ablations. The six frontier models use the 32k setting; 128k results remain in the appendix below. Agentic Memory builds up to 2k tokens of memory from 32k history. OE-only describes training; every plotted result is **MCQ** accuracy. CSIEE uses all 5,000 pinned text MCQs with reconstructed option order. Paper values have one decimal; the 45.62% local score versus 45.6% in the paper does not establish a meaningful win.

Source: [arXiv:2512.06688v1, Figures 4 and 6, MCQ labels](https://arxiv.org/abs/2512.06688v1). Model scores are cited, not rerun. All models/configurations in the selected source column(s) are shown; none are filtered by score. Sorting is visual ordering, not a claim of statistical superiority or equivalent agent capability.

## One table, both sources

| Method | Accuracy | Input / protocol | Source | Shuffled mean |
| :-- | --: | :-- | :-- | --: |
| Qwen3-4B · GRPO (MCQ-only) | 55.5% | 32k history | Paper: Figure 6 | — |
| Qwen3-4B · Agentic Memory | 55.2% | 2k memory* | Paper: Figure 6 | — |
| Qwen3-4B · GRPO | 53.8% | 32k history | Paper: Figure 6 | — |
| GPT-5-mini | 48.7% | 32k history | Paper: Figure 4 | — |
| **Xiaoming · longest** | **45.62%** | Options only | CSIEE: Saved CSIEE counts | 45.59% |
| GPT-5-Chat | 45.6% | 32k history | Paper: Figure 4 | — |
| o4-mini | 39.1% | 32k history | Paper: Figure 4 | — |
| GPT-4.1 | 38.7% | 32k history | Paper: Figure 4 | — |
| GPT-5-nano | 37.9% | 32k history | Paper: Figure 4 | — |
| GPT-4.1-mini | 37.6% | 32k history | Paper: Figure 4 | — |
| **Xiaogang · outlier** | **36.90%** | Options only | CSIEE: Saved CSIEE counts | 37.05% |
| Qwen3-4B · GRPO (OE-only) | 35.6% | 32k history | Paper: Figure 6 | — |
| Qwen3-4B · SFT | 35.0% | 32k history | Paper: Figure 6 | — |
| Qwen3-4B · Base | 30.5% | 32k history | Paper: Figure 6 | — |
| **Xiaohong · C** | **24.68%** | Options only | CSIEE: Saved CSIEE counts | 25.22% |
| Uniform chance | 25.00% | Options only | Analytical expectation | — |

Local bars use input-order results, seed 42. “—” means unavailable for this exact metric, not zero. Shuffled controls are reported only where the saved aggregate uses the same question set and weighting as the chart. Full-screen controls remain in the original reports.

## The paper's 128k frontier setting

| Frontier model | 32k MCQ | 128k MCQ |
| :-- | --: | --: |
| GPT-5-mini | 48.7% | 44.1% |
| GPT-5-Chat | 45.6% | 41.4% |
| o4-mini | 39.1% | 38.9% |
| GPT-4.1 | 38.7% | 38.2% |
| GPT-5-nano | 37.9% | 33.9% |
| GPT-4.1-mini | 37.6% | 37.5% |

The figure consistently uses 32k frontier scores; it does not select each model's best context length.

## Reproduce and inspect

- [Paper-value transcription](../data/paper/personamem-v2-mcq.json)
- [Local summary](../results/classmates/personamem-v2/summary.json) and [predictions](../results/classmates/personamem-v2/predictions.jsonl)
- [PNG](../assets/personamem-comparison.png) / [SVG](../assets/personamem-comparison.svg)
- [Renderer](../scripts/render_benchmarks.py) / [all ten comparisons](benchmark-comparisons.md)

Local dataset SHA-256: `95f2a8a324aab7baf2af937feae12731369e2abf7cad5ab3e170594cb25a3e52`.

```bash
python -m pip install matplotlib==3.9.4
python scripts/render_benchmarks.py
```

Rendering uses committed numerical records only; no API calls or raw dataset downloads are required. Matplotlib is an optional figure-building dependency.
