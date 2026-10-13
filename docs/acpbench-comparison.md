# ACPBench: paper results and the classmates

![ACPBench, all listed baselines sorted by accuracy](../assets/acpbench-comparison.png)

All 22 models from Table 2 are shown, using the **Mean / MCQ** column for two-shot chain-of-thought prompting. Boolean scores and the zero-shot appendix are excluded. The paper averages seven task accuracies (five runs for most models; one for GPT models and Llama-3.1-405B). To align the aggregation, CSIEE is recomputed from the seven saved per-category correct/count pairs with **equal weight per task**. Thus the local bars differ slightly from the question-weighted report card. The released MCQ set has 900 candidates; CSIEE excludes five duplicate-option records and retains 895. Printed paper means are preserved as published rather than recalculated from rounded cells.

Source: [arXiv:2410.05669v3, Table 2, Mean / MCQ column](https://arxiv.org/html/2410.05669v3). Model scores are cited, not rerun. All models/configurations in the selected source column(s) are shown; none are filtered by score. Sorting is visual ordering, not a claim of statistical superiority or equivalent agent capability.

## One table, both sources

| Method | Accuracy | Input / protocol | Source | Shuffled mean |
| :-- | --: | :-- | :-- | --: |
| LLAMA-3.1 405B | 77.42% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| GPT-4o | 74.97% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| LLAMA-3 70B | 74.30% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| LLAMA-3.1 70B | 66.94% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| GPT-4o Mini | 56.50% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Mixtral 8x7B | 51.44% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| LLAMA-3 8B | 44.05% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| LLAMA-3.1 8B | 41.52% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Codestral 22B | 40.97% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Mixtral 8x22B | 39.25% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Mistral Inst. 7B | 37.30% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| LLAMA-c 34B | 35.71% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Deepseek Inst. 33B | 35.11% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Phi-3 128K | 34.75% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| **Xiaogang · outlier** | **34.25%** | Options only | CSIEE: Saved CSIEE counts | — |
| LLAMA-c 70B | 32.87% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Granite-c Inst. 8B | 32.63% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| LLAMA-2 70B | 29.71% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Granite 7B | 29.67% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Granite-c 8B | 29.21% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Gemma 7B | 28.93% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Mistral 7B | 28.67% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Granite 13B | 26.66% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| **Xiaohong · C** | **25.29%** | Options only | CSIEE: Saved CSIEE counts | — |
| **Xiaoming · longest** | **20.22%** | Options only | CSIEE: Saved CSIEE counts | — |
| Uniform chance | 25.00% | Options only | Analytical expectation | — |

Local bars use input-order results, seed 42. “—” means unavailable for this exact metric, not zero. Shuffled controls are reported only where the saved aggregate uses the same question set and weighting as the chart. Full-screen controls remain in the original reports.

## Reproduce and inspect

- [Paper-value transcription](../data/paper/acpbench-mcq.json)
- [Local summary](../results/classmates/acpbench/summary.json) and [predictions](../results/classmates/acpbench/predictions.jsonl)
- [PNG](../assets/acpbench-comparison.png) / [SVG](../assets/acpbench-comparison.svg)
- [Renderer](../scripts/render_benchmarks.py) / [all five comparisons](benchmark-comparisons.md)

Local dataset SHA-256: `ad74aefe95ba248961a7672f90d2709c166275b47d26cc3d723ed4aa7a88b9b6`.

```bash
python -m pip install matplotlib==3.9.4
python scripts/render_benchmarks.py
```

Rendering uses committed numerical records only; no API calls or raw dataset downloads are required. Matplotlib is an optional figure-building dependency.
