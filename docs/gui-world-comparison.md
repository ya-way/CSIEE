# GUI-World: paper results and the classmates

![GUI-World, all listed baselines sorted by accuracy](../assets/gui-world-comparison.png)

All ten Table 3 models are retained, including the low-scoring video baselines. **Avg. / MC** is a macro-average across Software, Website, XR, Multi, IOS and Android; the CSIEE chart applies the same equal-category weighting. The report card is question-weighted. The pinned release contains 3,646 native MCQ candidates, of which three are excluded (one duplicate-option row and two unmappable gold answers). Exact answer text is mapped only on a unique exact match, never by semantic guessing. The release covers 1,823 video records, while the paper describes a 1,677-video test set: this release/paper difference is unresolved, so the comparison is contextual rather than item-matched.

Source: [arXiv:2406.10819v2, Table 3, Avg. / MC (macro-average of six categories)](https://arxiv.org/html/2406.10819v2). Model scores are cited, not rerun. All models/configurations in the selected source column(s) are shown; none are filtered by score. Sorting is visual ordering, not a claim of statistical superiority or equivalent agent capability.

## One table, both sources

| Method | Accuracy | Input / protocol | Source | Shuffled mean |
| :-- | --: | :-- | :-- | --: |
| GPT-4o | 84.8% | GUI video / keyframes + question | Paper: Table 3, Avg. / MC (macro-average of six categories) | — |
| Gemini-Pro-1.5 | 81.3% | GUI video / keyframes + question | Paper: Table 3, Avg. / MC (macro-average of six categories) | — |
| GPT-4V | 81.2% | GUI video / keyframes + question | Paper: Table 3, Avg. / MC (macro-average of six categories) | — |
| Qwen-VL-Max | 74.0% | GUI video / keyframes + question | Paper: Table 3, Avg. / MC (macro-average of six categories) | — |
| GUI-Vid | 54.6% | GUI video / keyframes + question | Paper: Table 3, Avg. / MC (macro-average of six categories) | — |
| **Xiaoming · longest** | **52.51%** | Options only | CSIEE: Saved CSIEE counts | — |
| LLaVA-OV-7B | 50.0% | GUI video / keyframes + question | Paper: Table 3, Avg. / MC (macro-average of six categories) | — |
| Video-LLaVA | 49.4% | GUI video / keyframes + question | Paper: Table 3, Avg. / MC (macro-average of six categories) | — |
| VideoChat2 | 42.9% | GUI video / keyframes + question | Paper: Table 3, Avg. / MC (macro-average of six categories) | — |
| **Xiaogang · outlier** | **42.44%** | Options only | CSIEE: Saved CSIEE counts | — |
| **Xiaohong · C** | **40.10%** | Options only | CSIEE: Saved CSIEE counts | — |
| ChatUnivi | 22.4% | GUI video / keyframes + question | Paper: Table 3, Avg. / MC (macro-average of six categories) | — |
| Minigpt4Video | 16.8% | GUI video / keyframes + question | Paper: Table 3, Avg. / MC (macro-average of six categories) | — |
| Uniform chance | 25.00% | Options only | Analytical expectation | — |

Local bars use input-order results, seed 42. “—” means unavailable for this exact metric, not zero. Shuffled controls are reported only where the saved aggregate uses the same question set and weighting as the chart. Full-screen controls remain in the original reports.

## Reproduce and inspect

- [Paper-value transcription](../data/paper/gui-world-mcq.json)
- [Local summary](../results/classmates/gui-world/summary.json) and [predictions](../results/classmates/gui-world/predictions.jsonl)
- [PNG](../assets/gui-world-comparison.png) / [SVG](../assets/gui-world-comparison.svg)
- [Renderer](../scripts/render_benchmarks.py) / [all ten comparisons](benchmark-comparisons.md)

Local dataset SHA-256: `9124023fd8a8df256117eff797628046415b0a4582825eb832c5f3dbd185c6d0`.

```bash
python -m pip install matplotlib==3.9.4
python scripts/render_benchmarks.py
```

Rendering uses committed numerical records only; no API calls or raw dataset downloads are required. Matplotlib is an optional figure-building dependency.
