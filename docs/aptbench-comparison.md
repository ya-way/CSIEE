# APTBench: paper results and the classmates

![APTBench, all listed baselines sorted by accuracy](../assets/aptbench-comparison.png)

All 14 base models from Table 3 are retained. Values use **Closed-ended Question / Plan_EN (ACC)**, the first numeric column, not the separate open-ended Plan_EN column or the mixed-metric Avg. The local bars use exactly the saved `deepresearch/plan_en` category: 614 questions, six options each, with no exclusions in this category. It was chosen for an explicit published MCQ accuracy and a direct released-task mapping, not to maximize a heuristic's score. This figure is **one subtask**, not the 4,215-question seven-task APTBench report card. The full screen and its reverse signal remain unchanged. Expected chance here is 1/6 (16.67%), not the full screen's 20.84%.

Source: [arXiv:2510.24397v1, Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column](https://arxiv.org/html/2510.24397v1). Model scores are cited, not rerun. All models/configurations in the selected source column(s) are shown; none are filtered by score. Sorting is visual ordering, not a claim of statistical superiority or equivalent agent capability.

## One table, both sources

| Method | Accuracy | Input / protocol | Source | Shuffled mean |
| :-- | --: | :-- | :-- | --: |
| Kimi K2-1TA32B | 86.64% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| GLM4.5-355BA32B | 85.50% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| DeepSeek-V3.1-671BA37B | 84.04% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| DeepSeek-V3-671BA37B | 82.31% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| Seed-OSS-36B | 81.60% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| Llama4-Scout-109BA17B | 78.01% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| GLM4.5-Air-106BA12B | 74.27% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| Qwen3-8B | 73.94% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| Gemma3-27B | 73.13% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| Qwen3-30BA3B | 73.13% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| Qwen3-4B | 72.48% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| Qwen3-1.7B | 53.09% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| SmolLM-3B | 48.70% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| Llama3.2-3B | 41.69% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| **Xiaoming · longest** | **20.36%** | Options only | CSIEE: Saved CSIEE counts | — |
| **Xiaohong · C** | **16.94%** | Options only | CSIEE: Saved CSIEE counts | — |
| **Xiaogang · outlier** | **7.33%** | Options only | CSIEE: Saved CSIEE counts | — |
| Uniform chance | 16.67% | Options only | Analytical expectation | — |

Local bars use input-order results, seed 42. “—” means unavailable for this exact metric, not zero. Shuffled controls are reported only where the saved aggregate uses the same question set and weighting as the chart. Full-screen controls remain in the original reports.

## Reproduce and inspect

- [Paper-value transcription](../data/paper/aptbench-plan-en.json)
- [Local summary](../results/classmates/aptbench/summary.json) and [predictions](../results/classmates/aptbench/predictions.jsonl)
- [PNG](../assets/aptbench-comparison.png) / [SVG](../assets/aptbench-comparison.svg)
- [Renderer](../scripts/render_benchmarks.py) / [all five comparisons](benchmark-comparisons.md)

Local dataset SHA-256: `35bf44c9b3c6337565c3871f3dab1d6edf66a165813037b1acdbc4dbf345842b`.

```bash
python -m pip install matplotlib==3.9.4
python scripts/render_benchmarks.py
```

Rendering uses committed numerical records only; no API calls or raw dataset downloads are required. Matplotlib is an optional figure-building dependency.
