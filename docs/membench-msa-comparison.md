# MemBench · multi-session assistant: paper results and the classmates

![MemBench · multi-session assistant, all listed baselines sorted by accuracy](../assets/membench-msa-comparison.png)

This is **one selected subtask, not the whole MemBench benchmark**. All seven memory mechanisms in Table 11, `msa`, are retained, including the lowest result. CSIEE uses the full 500-question `FirstAgent/RecMultiSession.json` pool. The paper uses sampled trajectories with a 10k memory context, so these are different denominators and not paired runs. List-valued choices are rendered with Python `str`, matching upstream `MembenchAgent.py` string interpolation. The complete 25,874-question valid MemBench screen has only +2.60 pp best shuffled lift; the 100% result does not generalize to it. The subtask was selected after screening.

Source: [arXiv:2506.21605v1, Table 11, msa (multi-session assistant) column](https://arxiv.org/html/2506.21605v1). Model scores are cited, not rerun. All models/configurations in the selected source column(s) are shown; none are filtered by score. Sorting is visual ordering, not a claim of statistical superiority or equivalent agent capability.

## One table, both sources

| Method | Accuracy | Input / protocol | Source | Shuffled mean |
| :-- | --: | :-- | :-- | --: |
| **Xiaoming · longest** | **100.00%** | Options only | CSIEE: Saved CSIEE counts | 100.00% |
| **Xiaogang · outlier** | **63.80%** | Options only | CSIEE: Saved CSIEE counts | 63.52% |
| FullMemory | 55.0% | 10k factual participation; memory mechanism | Paper: Table 11, msa (multi-session assistant) column | — |
| GenerativeAgent | 55.0% | 10k factual participation; memory mechanism | Paper: Table 11, msa (multi-session assistant) column | — |
| RecentMemory | 50.0% | 10k factual participation; memory mechanism | Paper: Table 11, msa (multi-session assistant) column | — |
| MemGPT | 45.0% | 10k factual participation; memory mechanism | Paper: Table 11, msa (multi-session assistant) column | — |
| MemoryBank | 40.0% | 10k factual participation; memory mechanism | Paper: Table 11, msa (multi-session assistant) column | — |
| RetrievalMemmory | 30.0% | 10k factual participation; memory mechanism | Paper: Table 11, msa (multi-session assistant) column | — |
| **Xiaohong · C** | **24.60%** | Options only | CSIEE: Saved CSIEE counts | 23.92% |
| SCMemory | 10.0% | 10k factual participation; memory mechanism | Paper: Table 11, msa (multi-session assistant) column | — |
| Uniform chance | 25.00% | Options only | Analytical expectation | — |

Local bars use input-order results, seed 42. “—” means unavailable for this exact metric, not zero. Shuffled controls are reported only where the saved aggregate uses the same question set and weighting as the chart. Full-screen controls remain in the original reports.

## Reproduce and inspect

- [Paper-value transcription](../data/paper/membench-msa.json)
- [Local summary](../results/classmates/membench-msa/summary.json) and [predictions](../results/classmates/membench-msa/predictions.jsonl)
- [PNG](../assets/membench-msa-comparison.png) / [SVG](../assets/membench-msa-comparison.svg)
- [Renderer](../scripts/render_benchmarks.py) / [all ten comparisons](benchmark-comparisons.md)

Local dataset SHA-256: `773bc50897b8cbf1a253b5ef7ec5d1a748c8def7f2fd2263427214852e9a4c66`.

```bash
python -m pip install matplotlib==3.9.4
python scripts/render_benchmarks.py
```

Rendering uses committed numerical records only; no API calls or raw dataset downloads are required. Matplotlib is an optional figure-building dependency.
