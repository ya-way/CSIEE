# AgentHop: paper results and the classmates

![AgentHop, all listed baselines sorted by accuracy](../assets/agenthop-comparison.png)

All 19 models from Table 2 are retained, including models below chance. The paper's **Outcome / Accuracy** fractions are multiplied by 100; three-decimal fractions become one-decimal percentages. This is neither paper recall nor synthesis conversion. The paper evaluates agents with a scientific-paper tool environment and resource caps; failed submissions count against accuracy. CSIEE evaluates the pinned 1,011 released MCQs without questions, tools or trajectories. We have not established item-by-item identity between that pinned release and every paper run, and these are not matched reruns.

Source: [arXiv:2609.34428v1, Table 2, Outcome / Accuracy column](https://arxiv.org/html/2609.34428v1). Model scores are cited, not rerun. All models/configurations in the selected source column(s) are shown; none are filtered by score. Sorting is visual ordering, not a claim of statistical superiority or equivalent agent capability.

## One table, both sources

| Method | Accuracy | Input / protocol | Source | Shuffled mean |
| :-- | --: | :-- | :-- | --: |
| Gemini-3 Pro | 89.1% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| GPT-5.3 codex | 82.5% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| GPT-5.4 | 79.0% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| Claude Opus 4.6 | 77.5% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| Claude Sonnet 4.6 | 76.6% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| GLM-5.1 | 69.6% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| Gemma-4-31B | 64.8% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| DeepSeek-reasoner | 59.6% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| DeepSeek-chat | 56.4% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| Gemini-3 Flash | 54.7% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| Qwen3.5-27B | 48.2% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| Kimi-K2.5 | 44.1% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| MiniMax-M2.7 | 41.3% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| Qwen3.6-35B-A3B | 38.1% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| Qwen3.5-35B-A3B | 32.0% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| **Xiaohong · C** | **27.50%** | Options only | CSIEE: Saved CSIEE counts | 25.00% |
| Gemma-4-26B-A4B | 23.6% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| Gemma-3-27B | 18.6% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| **Xiaogang · outlier** | **18.40%** | Options only | CSIEE: Saved CSIEE counts | 18.46% |
| Qwen3-30B-A3B | 16.0% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| Qwen3-32B | 13.3% | Question + choices + scientific-paper tools | Paper: Table 2, Outcome / Accuracy column | — |
| **Xiaoming · longest** | **0.89%** | Options only | CSIEE: Saved CSIEE counts | 0.98% |
| Uniform chance | 25.00% | Options only | Analytical expectation | — |

Local bars use input-order results, seed 42. “—” means unavailable for this exact metric, not zero. Shuffled controls are reported only where the saved aggregate uses the same question set and weighting as the chart. Full-screen controls remain in the original reports.

## Reproduce and inspect

- [Paper-value transcription](../data/paper/agenthop-accuracy.json)
- [Local summary](../results/classmates/agenthop/summary.json) and [predictions](../results/classmates/agenthop/predictions.jsonl)
- [PNG](../assets/agenthop-comparison.png) / [SVG](../assets/agenthop-comparison.svg)
- [Renderer](../scripts/render_benchmarks.py) / [all ten comparisons](benchmark-comparisons.md)

Local dataset SHA-256: `3f1ea9261f708d27c0d545cac238338abd9161f718be745804b6ec3b1e01147b`.

```bash
python -m pip install matplotlib==3.9.4
python scripts/render_benchmarks.py
```

Rendering uses committed numerical records only; no API calls or raw dataset downloads are required. Matplotlib is an optional figure-building dependency.
