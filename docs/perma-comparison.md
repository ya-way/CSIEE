# PERMA · Type 3: paper results and the classmates

![PERMA · Type 3, all listed baselines sorted by accuracy](../assets/perma-comparison.png)

All 17 Table 4 baselines are retained, including every GPT-4o-mini memory system. The chart uses the **423 single-domain Type-3 questions**; the report card includes all **580** single- and multi-domain Type-3 questions. Type 1 and Type 2 are separate checkpoint variants and are not counted as additional questions here. The clean/noisy histories never enter CSIEE. This is an answer-choice audit, not an interactive task-completion score. Published and local pipelines differ; item-by-item identity of paper runs is not independently established.

Source: [arXiv:2603.23231v1, Table 4, MCQ Acc. (Clean, single-domain)](https://arxiv.org/html/2603.23231v1). Model scores are cited, not rerun. All models/configurations in the selected source column(s) are shown; none are filtered by score. Sorting is visual ordering, not a claim of statistical superiority or equivalent agent capability.

## One table, both sources

| Method | Accuracy | Input / protocol | Source | Shuffled mean |
| :-- | --: | :-- | :-- | --: |
| **Xiaoming · longest** | **93.85%** | Options only | CSIEE: Saved CSIEE counts | — |
| **Xiaogang · outlier** | **91.96%** | Options only | CSIEE: Saved CSIEE counts | — |
| Kimi-K2.5 | 88.2% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| Gemini2.5-Flash | 87.0% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| Qwen3-32B | 87.0% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| GLM-4.7-Flash | 86.8% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| Llama3.3-70B | 81.8% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| GLM-5 | 81.1% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| MemOS | 81.1% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| MiniMax-M2.5 | 79.7% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| Qwen2.5-72B | 79.0% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| GPT-4o-mini | 78.0% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| Qwen2.5-14B-1M | 75.9% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| Memobase | 73.3% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| EverMemOS | 72.8% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| RAG (BGE-M3) | 70.2% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| Mem0 | 68.6% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| Lightmem | 65.7% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| Supermemory | 65.5% | Clean single-domain; history or memory | Paper: Table 4, MCQ Acc. (Clean, single-domain) | — |
| **Xiaohong · C** | **13.71%** | Options only | CSIEE: Saved CSIEE counts | — |
| Uniform chance | 12.50% | Options only | Analytical expectation | — |

Local bars use input-order results, seed 42. “—” means unavailable for this exact metric, not zero. Shuffled controls are reported only where the saved aggregate uses the same question set and weighting as the chart. Full-screen controls remain in the original reports.

## Reproduce and inspect

- [Paper-value transcription](../data/paper/perma-clean-sd.json)
- [Local summary](../results/classmates/perma/summary.json) and [predictions](../results/classmates/perma/predictions.jsonl)
- [PNG](../assets/perma-comparison.png) / [SVG](../assets/perma-comparison.svg)
- [Renderer](../scripts/render_benchmarks.py) / [all ten comparisons](benchmark-comparisons.md)

Local dataset SHA-256: `e72aee7e23bdc84ebe586a0219e59c414f61ffe0fee13533bfb8f699b458ae76`.

```bash
python -m pip install matplotlib==3.9.4
python scripts/render_benchmarks.py
```

Rendering uses committed numerical records only; no API calls or raw dataset downloads are required. Matplotlib is an optional figure-building dependency.
