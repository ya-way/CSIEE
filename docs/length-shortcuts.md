# Why can a ruler top these particular charts?

The scores are real measurements of the selected released MCQs. They are not evidence of state-of-the-art agent ability. The longest-choice rule exploits answer construction, while the paper systems attempt to recover the information needed to answer the task.

## PERMA: the most complete response is usually the longest

Across all **580 Type-3 questions**, the gold response is the **unique longest option in 544 cases** and tied for longest in one more. Gold responses average **737.7 characters**, versus **431.8** for distractors. Xiaoming scores **93.97%** in the released order and **93.93%** across ten permutations. Shuffling moves labels; it cannot remove a length cue attached to the text.

The [paper's Section 4.3.3](https://arxiv.org/html/2603.23231v1#S4.SS3.SSS3) describes eight choices formed by binary combinations of task completion, preference consistency and informational confidence. A plausible explanation is that expressing the complete, personalized response takes more text than many of these deliberately impaired alternatives. The length correlation is directly measured; the generation-process explanation is an inference, not a controlled causal finding.

The comparison chart uses **423 single-domain Type-3 questions** to align with Table 4; its local input-order score is **93.85%**, alongside the highest cited Table 4 value of **88.2%**. The headline uses all 580 Type-3 questions, including multi-domain queries. Type 1/2, interactive success and other memory metrics are outside this result. Published model pipelines were not rerun or item-matched by CSIEE.

## MemBench msa: the complete list gives itself away

All **500** gold choices are uniquely longest. Of the **1,500** distractors, **1,385 are lists that omit exactly one item from the gold list**; the other **115 are non-list replies**. The item-count patterns are:

| Questions | Gold list size | Distractor list sizes (-1 = non-list reply) |
| --: | --: | :-- |
| 115 | 3 | -1, 2, 2 |
| 208 | 4 | 3, 3, 3 |
| 145 | 5 | 4, 4, 4 |
| 32 | 6 | 5, 5, 5 |

The rule need not remember which items were recommended: the complete list is longer. It scores **500/500 before and after shuffling**. The published adapter uses Python's string rendering of lists, matching the upstream prompt interpolation. As a diagnostic check, replacing list brackets and quotes with comma-joined items still leaves gold uniquely longest in all 500 cases. This is not a bracket-formatting trick.

This is **one selected multi-session assistant subtask**. The full valid 25,874-question MemBench pilot has only **+2.60 percentage points** best shuffled lift over chance. The [paper's Table 11](https://arxiv.org/html/2506.21605v1#A4.T11) reports sampled 10k-context msa runs (highest cited value **55%**), while CSIEE uses the full released 500-question pool. Different samples and inputs prevent a matched SOTA claim.

## What was curated, and what was not

- **Presentation was curated:** colors, large headline figures, descending bars and this front-page ordering emphasize memorable findings.
- **The showcase was selected after observing scores:** candidates were screened for strong positive lift, the best of three fixed rules was used for selection, and MemBench msa was selected from a much weaker full suite. This is selection bias, disclosed in the [screening ledger](screening.md), not held-out confirmation.
- **These two components were not filtered question by question:** all 580 PERMA Type-3 questions and all 500 MemBench msa questions were included, with zero record exclusions. Other adapters have documented structural exclusions.
- **The rule and measured scores were not adjusted for the headline:** the predictor sees only choice strings. Gold labels are used by the evaluator and this post-hoc diagnostic, never passed into the predictor. All source-column paper baselines, including weak ones, remain in the figures.

A fair conclusion is that these particular choice sets contain powerful shortcuts. It does not follow that a ruler remembers users, that the full benchmark is solved, or that the displayed paper scores constitute today's complete SOTA leaderboard.

## Audit and reproduce

[Saved structural counts](../results/diagnostics/length-signals.json) · [Diagnostic script](../scripts/audit_length_signal.py) · [Evaluation methods](methodology.md)

After downloading the pinned normalized `perma` and `membench-msa` components with `csiee download`, run:

```bash
python scripts/audit_length_signal.py --output results/local/length-signals.json
```

The script verifies the normalized input hashes against the published reports and emits only counts, not benchmark text. It changes no evaluation files or prediction rules.
