# The complete report card

CSIEE 0.2.0 · seed 42 · ten label-preserving option permutations · all included questions.

This table shows **shuffled mean accuracy** for all eight completed screens. The [front page](../../README.md#report-card) shows input-order accuracy for the five featured families. No end-to-end agent evaluation is performed.

| Benchmark | Questions | Chance | Xiaoming | Xiaohong | Xiaogang | Seeded random |
| :-- | --: | --: | --: | --: | --: | --: |
| [PersonaMem-v2](personamem-v2/report.md) | 5,000 | 25.00% | 45.59% | 25.22% | 37.05% | 25.11% |
| [AgentSense](agentsense/report.md) | 1,863 | 25.00% | 49.69% | 25.10% | 49.57% | 24.78% |
| [ACPBench](acpbench/report.md) | 895 | 25.00% | 19.49% | 24.41% | 33.33% | 24.77% |
| [APTBench](aptbench/report.md) | 4,215 | 20.84% | 16.41% | 20.79% | 11.85% | 20.92% |
| [AgentHop](agenthop/report.md) | 1,011 | 25.00% | 0.98% | 25.00% | 18.46% | 24.81% |
| [BixBench](bixbench/report.md) | 205 | 25.00% | 27.66% | 24.98% | 19.32% | 25.32% |
| [Backtrader-Bench](backtrader/report.md) | 160 | 25.00% | 24.25% | 25.69% | 27.06% | 26.06% |
| [FDABench (labeled subset)](fdabench/report.md) | 237 | 25.00% | 14.09% | 25.61% | 10.51% | 25.44% |

Each linked report has input-order accuracy, Wilson intervals, permutation ranges and choice invariance. Adjacent `summary.json` files hold source provenance, hashes, exclusions and category counts; `predictions.jsonl` contains input-order predictions and gold indices, without raw option text.

The five featured families cover 12,984 included questions. All eight contain 13,586 included questions, with correlated questions and different task formats. Counts are not independent sample sizes, and we do not pool their scores.

See the [screening ledger](../../docs/screening.md) for exact components and [methods](../../docs/methodology.md) for assumptions. Additional datasets are retained even when the shortcuts do not help. These are exploratory measurements, not significance claims.
