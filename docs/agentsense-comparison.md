# AgentSense: paper results and the classmates

![AgentSense, all listed baselines sorted by accuracy](../assets/agentsense-comparison.png)

All 11 models in Table 1 are retained. Values come from **Info / Acc.**, not goal-completion scores or the PSI sensitivity statistic. The paper evaluates information reasoning after interactions between agents driven by the same model. CSIEE evaluates the released information MCQs without running those interactions; it retains 1,863 of 1,864 candidates after excluding one duplicate-option question. These protocols and denominators are not identical.

Source: [arXiv:2410.19346v2, Table 1, Info / Acc. column](https://arxiv.org/html/2410.19346v2). Model scores are cited, not rerun. All models/configurations in the selected source column(s) are shown; none are filtered by score. Sorting is visual ordering, not a claim of statistical superiority or equivalent agent capability.

## One table, both sources

| Method | Accuracy | Input / protocol | Source | Shuffled mean |
| :-- | --: | :-- | :-- | --: |
| GPT-4o | 76.86% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| Qwen2.5-72b | 76.05% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| Qwen2.5-14b | 75.02% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| Qwen2.5-7b | 74.82% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| Llama-3-70b | 73.08% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| Llama-3-8B | 69.68% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| GPT-3.5-turbo | 68.41% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| Mistral-7b | 66.59% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| **Xiaoming · longest** | **49.87%** | Options only | CSIEE: Saved CSIEE counts | 49.69% |
| **Xiaogang · outlier** | **49.44%** | Options only | CSIEE: Saved CSIEE counts | 49.57% |
| Llama-2-70b | 36.78% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| Llama-2-7b | 33.06% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| Llama-2-13b | 28.56% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| **Xiaohong · C** | **25.17%** | Options only | CSIEE: Saved CSIEE counts | 25.10% |
| Uniform chance | 25.00% | Options only | Analytical expectation | — |

Local bars use input-order results, seed 42. “—” means unavailable for this exact metric, not zero. Shuffled controls are reported only where the saved aggregate uses the same question set and weighting as the chart. Full-screen controls remain in the original reports.

## Reproduce and inspect

- [Paper-value transcription](../data/paper/agentsense-info.json)
- [Local summary](../results/classmates/agentsense/summary.json) and [predictions](../results/classmates/agentsense/predictions.jsonl)
- [PNG](../assets/agentsense-comparison.png) / [SVG](../assets/agentsense-comparison.svg)
- [Renderer](../scripts/render_benchmarks.py) / [all ten comparisons](benchmark-comparisons.md)

Local dataset SHA-256: `efbcf0bc3f37b093fe977f579990db79df6b8317a50b1a81f5a0e1ba384805cf`.

```bash
python -m pip install matplotlib==3.9.4
python scripts/render_benchmarks.py
```

Rendering uses committed numerical records only; no API calls or raw dataset downloads are required. Matplotlib is an optional figure-building dependency.
