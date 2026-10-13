# 方法与复现 / Methodology

## What is being tested?

CSIEE asks whether answer-option structure alone carries a useful signal. Its strategies receive **only a tuple of option strings**. They cannot see the question, correct index, user history, persona, category, or any LLM output. The evaluator holds labels separately. The implementation includes no trainable parameters, external inference calls, or test-set search.

This is an option-only diagnostic baseline, not an equivalent replacement for a memory system. A score above chance does not establish that a benchmark is invalid, that a model cheated, or that the same effect generalizes. A poor score is also a legitimate result. In particular, an artifact audit cannot infer whether data were AI-generated.

## Fixed heuristics

All lengths count Unicode code points after stripping outer whitespace. Internal whitespace and punctuation count. Thresholds and voting were fixed before the first benchmark run.

| Strategy | Rule | Fallback |
| :-- | :-- | :-- |
| `lite` | Choose C | With only two choices, B |
| `pro` | If the longest is strictly >1.5× second-longest, choose it; otherwise if second-shortest is >1.5× shortest, choose shortest | C |
| `promax` | One vote each from Pro, numeric rule, and cautious-wording rule; the latter two can abstain | A voting tie prefers C if tied, then lowest index |
| `longest` / `shortest` | Always choose a length extremum | Tie prefers C, then lowest index |
| `numeric` | When every option is a distinct pure number, choose the third-largest | C; fewer than three or tied values abstain in Pro Max |
| `cautious` | Minimize whole-word occurrences of `always never only all must every impossible certainly` | Abstain if all counts match; otherwise tie prefers C, then lowest index |
| `random` | Seeded uniform choice for each question | None |

The numeric rule accepts signs, decimals, scientific notation and percentages, normalizing percentages to fractions. It deliberately does not parse numbers embedded in sentences, units, currency, ranges, or thousands separators. Third-largest means descending rank 3, **not** the third option. Example: `[2, 8, 6, 4] → 4`.

Pro generalizes the four-choice folklore to 2–26 options. Both outliers can exist; the longest rule has priority. Pro Max is a tiny fixed ensemble, not an exhaustive implementation of every folk saying. “Pro” is a product joke, not a promised accuracy ordering. Helper parsing and evaluation code are not included in the few-line strategy-body joke; all of it is visible in the repository.

## PersonaMem-v2 adapter

Official sources:

- [Dataset and license](https://huggingface.co/datasets/bowen-upenn/PersonaMem-v2)
- [Official evaluation implementation](https://github.com/bowen-upenn/PersonaMem-v2/blob/main/inference.py)
- [Paper](https://arxiv.org/abs/2512.06688)

The source CSV stores `correct_answer` and `incorrect_answers` separately. CSIEE combines these into a choice set, then shuffles using a per-record SHA-256-derived seed. The correct index is remapped along with the options. It uses row index and persona ID as the record identity. JSON and Python literal lists are accepted; no `eval()` is used.

The pinned text benchmark revision is `ed956dea41521fc4499acbc63f966e0fd3c053ba`, path `benchmark/text/benchmark.csv`. The downloader saves an adjacent `.source.json` manifest with revision, source URL, split, license and SHA-256. Evaluation verifies the hash before copying this provenance into the report. No chat histories are downloaded. Upstream data remain under their upstream CC-BY-4.0 license; the MIT license covers this project's code and original demo only.

The official evaluator constructs MCQ order at runtime using a seed involving Python's `hash()`. CSIEE uses its own stable SHA-256-derived order to make separate-process runs reproducible. **Our accuracy uses a reconstructed order, not the official evaluation order.** Compare systems on the same exported choice order before making a head-to-head claim.

## Metrics and controls

### OpenBookQA comparison

The second experiment uses the complete 500-question test split from the official [OpenBookQA V1-Sep2018 archive](https://s3-us-west-2.amazonaws.com/ai2-website/data/OpenBookQA-V1-Sep2018.zip). The archive SHA-256 is pinned in the downloader, which reads only `Data/Main/test.jsonl`. The adapter preserves source option order and maps `answerKey` using each choice's explicit label, not an assumption about alphabetical order. The same unchanged strategies and permutation controls are used.

Credit: [Mihaylov et al., EMNLP 2018](https://arxiv.org/abs/1809.02789), [official code](https://github.com/allenai/OpenBookQA). The [upstream dataset card](https://huggingface.co/datasets/allenai/openbookqa) lists the dataset license as unknown. We do not redistribute its question/answer text or apply the repository's MIT license to it; consult the upstream terms for reuse. Public results contain derived metrics and indices only.

### Metric definitions

- Accuracy is the fraction of correctly selected option indices. There is no LLM judge.
- The exact expected uniform-random baseline is `mean(1 / number_of_options)`. Mixed choice counts need not have a 25% chance level.
- A separate seeded random run gives one realization of that baseline.
- Each strategy is evaluated on the source order and the same 10 independently seeded option permutations. Labels move with their answer text.
- Shuffled mean/min/max describe sensitivity to option order. These repeated evaluations are **not independent new questions**.
- Choice invariance compares selected answer **text**, not letters, across source and permuted inputs.
- Wilson 95% intervals are descriptive question-level intervals. Questions from a shared persona can be correlated; these are not persona-cluster-adjusted intervals or claims of statistical significance.
- Testing multiple heuristics and highlighting the best one introduces selection effects. Report every predeclared strategy, and confirm interesting signals on another dataset or a held-out split.

`--limit N` explicitly selects the **first N records**, not a random subsample. The full dataset hash, number loaded and selection rule are retained. Input errors and duplicate choices/IDs fail loudly rather than being silently excluded from the denominator.

## Reports

Each run writes `summary.json`, `report.md`, and `predictions.jsonl`. Predictions record strategy, question ID, predicted index and correct index; they do not redistribute answer text or user histories. Summaries include software/Python version, input hash, source revision when available, seed, option count distribution, answer distribution, controls and metrics.

The repository's committed PersonaMem-v2 results were generated using the commands in the README. `data/demo.jsonl` is deliberately synthetic and must never be described as real benchmark evidence. To add another benchmark, adapt it to the documented JSONL schema while preserving its official split and license, then use the same evaluation command.
