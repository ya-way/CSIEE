# MMBench-GUI · L1: paper results and the classmates

![MMBench-GUI · L1, all listed baselines sorted by accuracy](../assets/mmbench-gui-l1-comparison.png)

All seven models in Table 5 are shown. Each model bar is the **arithmetic mean of its three printed Overall scores** (Easy, Medium, Hard); the paper gives equal difficulty counts, so no difficulty is selected for advantage. These bars are derived aggregates, not a separately printed total. Equations 3–4 discount each correct answer by `(m−1)/m`, with `m` choices. CSIEE and the chance line apply that same formula from saved per-option-count counts; the report card and screening criterion use ordinary accuracy. The released L1 file contains 3,561 questions, versus 3,582 described in the paper. The upstream repository flags figures for revalidation; these are specifically the cited v1 values, not a claim of validated current leaderboard performance. L2–L4 execution tasks are outside scope.

Source: [arXiv:2507.19478v1, Table 5, Overall columns; arithmetic mean of three difficulties](https://arxiv.org/html/2507.19478v1). Model scores are cited, not rerun. All models/configurations in the selected source column(s) are shown; none are filtered by score. Sorting is visual ordering, not a claim of statistical superiority or equivalent agent capability.

## One table, both sources

| Method | Accuracy | Input / protocol | Source | Shuffled mean |
| :-- | --: | :-- | :-- | --: |
| InternVL3-72B | 77.58% | Screenshot + question; mean of Easy/Medium/Hard | Paper: Table 5, Overall columns; arithmetic mean of three difficulties | — |
| Qwen2.5-VL-72B | 66.33% | Screenshot + question; mean of Easy/Medium/Hard | Paper: Table 5, Overall columns; arithmetic mean of three difficulties | — |
| Qwen-Max-VL | 65.76% | Screenshot + question; mean of Easy/Medium/Hard | Paper: Table 5, Overall columns; arithmetic mean of three difficulties | — |
| GPT-4o | 56.96% | Screenshot + question; mean of Easy/Medium/Hard | Paper: Table 5, Overall columns; arithmetic mean of three difficulties | — |
| Claude-3.5 | 40.12% | Screenshot + question; mean of Easy/Medium/Hard | Paper: Table 5, Overall columns; arithmetic mean of three difficulties | — |
| UI-TARS-72B-DPO | 39.24% | Screenshot + question; mean of Easy/Medium/Hard | Paper: Table 5, Overall columns; arithmetic mean of three difficulties | — |
| Claude-3.7 | 37.71% | Screenshot + question; mean of Easy/Medium/Hard | Paper: Table 5, Overall columns; arithmetic mean of three difficulties | — |
| **Xiaoming · longest** | **36.06%** | Options only | CSIEE: Saved CSIEE counts | — |
| **Xiaogang · outlier** | **28.11%** | Options only | CSIEE: Saved CSIEE counts | — |
| **Xiaohong · C** | **22.39%** | Options only | CSIEE: Saved CSIEE counts | — |
| Uniform chance | 17.13% | Options only | Analytical expectation | — |

Local bars use input-order results, seed 42. “—” means unavailable for this exact metric, not zero. Shuffled controls are reported only where the saved aggregate uses the same question set and weighting as the chart. Full-screen controls remain in the original reports.

## Reproduce and inspect

- [Paper-value transcription](../data/paper/mmbench-gui-l1.json)
- [Local summary](../results/classmates/mmbench-gui-l1/summary.json) and [predictions](../results/classmates/mmbench-gui-l1/predictions.jsonl)
- [PNG](../assets/mmbench-gui-l1-comparison.png) / [SVG](../assets/mmbench-gui-l1-comparison.svg)
- [Renderer](../scripts/render_benchmarks.py) / [all ten comparisons](benchmark-comparisons.md)

Local dataset SHA-256: `2a4d1d95b30d0b267e06fcd952ede4740571b87fadc9691f1fa30aa333eb068d`.

```bash
python -m pip install matplotlib==3.9.4
python scripts/render_benchmarks.py
```

Rendering uses committed numerical records only; no API calls or raw dataset downloads are required. Matplotlib is an optional figure-building dependency.
