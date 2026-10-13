# Methods: a joke with an audit trail

CSIEE evaluates answer-option shortcuts in native multiple-choice components of agent-related benchmarks. It does not evaluate end-to-end agents. The three named predictors accept only a list of option strings: no question stem, conversation, tool output, dataset identity, gold label, or training step.

## The three rules

| Strategy | Exact rule |
| :-- | :-- |
| `xiaoming` | Maximize Python `len(option.strip())`: Unicode code points, not tokens or bytes. |
| `xiaohong` | Choose index 2 (C), or index 1 (B) if there are only two options. |
| `xiaogang` | Infer numeric versus textual answer type from the entire option set. Maximize absolute distance from the median of the values or stripped character lengths. |

Ties in Xiaoming and Xiaogang prefer C if it is among the tied candidates; otherwise choose the earliest tied index. For two choices, B receives the same tie preference. No abstention or benchmark-specific rule is used.

Xiaogang is experimental. The numeric parser accepts signed scalar decimals, scientific notation, and an optional alphabetic, percent, or degree unit suffix. Every option must parse and have the same case-insensitive suffix; bare values and percentages may mix, with percentages divided by 100. It does not convert units. Finite numeric values are scaled by their maximum absolute magnitude before computing distances. This improves numerical stability but uses floating-point arithmetic.

Everything else falls back to length: prose containing numbers, currency symbols, thousands separators, ranges, incompatible units, and nonfinite numeric values. This is a shallow **answer-type classifier**, not semantic classification of the question. All 12,984 featured questions use the length route. In the additional datasets, the numeric route handles 104/205 BixBench, 62/160 Backtrader-Bench, and 10/237 labeled FDABench questions. These results do not establish a benefit from numeric routing.

The strategy specification was written before the new screening runs. Dataset selection followed inspection of outcomes. This is exploratory work, not a preregistered study or a held-out benchmark validation.

## Data and exclusions

The [screening ledger](screening.md) names the evaluated releases, components, and excluded task types. Source revisions are pinned in the downloaders. Saved summaries include source URLs, revisions, SHA-256 hashes, and, for the new adapters, every excluded record ID and reason.

The canonical record has a unique string ID, 2–26 nonempty option strings, a zero-based integer answer index, and an optional category. Whitespace-stripped option text must be distinct. The adapters map explicit source labels to indices; they never infer a correct answer from its wording. Duplicate option texts are excluded because selecting the same content after a permutation would otherwise be ambiguous. APTBench additionally excludes unparseable choice markers and gold labels absent from the released choices. FDABench excludes rows without released gold answers. Remaining schema errors fail the run.

APTBench's parser accepts sequential `(A)`, `(B)`, … markers, including inline semicolon-separated options. It removes separator semicolons. A repeated source ID can appear more than once in the exclusion ledger because distinct invalid source rows share an ID; included normalized IDs must be unique. Exclusions are structural, not based on whether a strategy would answer correctly.

PersonaMem-v2 releases correct and wrong answers separately. We combine them and deterministically shuffle per question before evaluation. BixBench's native MCQ format is similarly reconstructed from `ideal` plus its released `distractors`, without an optional refusal answer. BixBench's boolean `answer` field belongs to a separate hypothesis task and is not used as MCQ gold. No new distractors are generated. Other adapters preserve native option order.

Downloaded source data is ignored by Git. Only code, provenance, metrics, and prediction indices are committed. Upstream data keeps its own license; see the ledger and each source manifest. Users should consult upstream terms before downloading or reusing data.

## Evaluation protocol

All current reports use CSIEE 0.2.0, seed **42**, all included records, and **10** independent deterministic permutations per question. The same questions and permutations are used for all strategies. A SHA-256-derived seed makes question-level randomness independent of Python's process hash randomization. Gold indices are remapped with the option text.

We report:

- **Input-order accuracy:** correct predictions divided by included questions. PersonaMem and BixBench use the seeded reconstruction described above.
- **Chance:** the mean of `1 / number_of_options` over questions. APTBench has varying option counts, so its chance is 20.84%, not 25%.
- **Seeded random:** a uniform random index per question; this observed score can differ from exact expected chance.
- **Shuffled mean and range:** accuracy over each of the ten option permutations. The range measures sensitivity to ordering, not sampling uncertainty.
- **Same choice:** the fraction selecting identical option content before and after permutation, averaged across repeats. Position preferences and length ties can reduce it.
- **Wilson 95% interval:** a descriptive binomial interval for input-order accuracy. Shared personas, scenarios, source problems, or task templates can violate the independence assumption. No cluster correction is claimed.
- **Per-category counts:** available in `summary.json`, alongside answer-position and option-count histograms.

`predictions.jsonl` stores one input-order record per question and strategy. Permutation aggregate scores are in `summary.json`. The source manifest's dataset hash is verified before evaluation. For BixBench, a requested evaluation seed must match its reconstruction seed; to change it, download to a fresh path with `--seed`, then evaluate that path.

## Interpretation and selection

The exploratory positive-signal rule was a shuffled mean more than **5 percentage points above chance** for a named strategy. PersonaMem-v2, AgentSense, and ACPBench meet it. APTBench and AgentHop are included for strong reverse signals: a named heuristic falls more than 5 points below chance after permutations. The reverse-signal presentation was chosen after inspecting outcomes; it is not an additional preregistered criterion.

We report all eight completed screens, including BixBench and Backtrader-Bench's weak results and FDABench's selected public-label subset. The front-page five are a showcase, not a representative sample of agent benchmarks. Do not infer how frequently these artifacts occur across the field. Do not treat multiple permutations, multiple strategies, or benchmark selection as independent confirmatory evidence.

High option-only accuracy can reflect answer verbosity, distractor construction, task format, or other correlations. Low accuracy can also reveal structure. Neither proves that a benchmark is invalid, that a model exploits the same shortcut, or that a ruler can perform an agent's underlying task. The [PersonaMem comparison](personamem-comparison.md) places cited paper MCQ values and local results in one table, with input access and provenance labeled; those model scores were not rerun under the CSIEE protocol. It is contextual evidence, not a matched agent leaderboard. We deliberately publish no pooled score across heterogeneous benchmark families.

## Reproduce

```bash
python -m pip install .
python -m unittest discover -s tests -v
csiee suite --seed 42 --shuffles 10 --output results/local/suite
csiee suite --all --seed 42 --shuffles 10 --output results/local/all
```

The suite downloads missing files to `data/raw/` and requires a valid adjacent `.source.json` manifest for reused files. It does not silently replace existing downloads. A source outage should fail visibly; previously downloaded official bytes can be normalized with `prepare_benchmark`, which records their actual hashes. Source hashes in the committed reports allow comparison with a later download.

## Legacy ablations

The CLI retains `lite` (C), `longest`, `shortest`, `pro` (1.5× length-gap rule), `numeric` (third-largest distinct numeric value), `cautious` (fewest absolute-word matches), and `promax` (a vote of the older rules). They are not the new Xiaogang policy. Request them explicitly with `--strategies` for ablations.

The [earlier PersonaMem report](../results/personamem-v2/report.md) and [OpenBookQA report](../results/openbookqa/report.md) are v0.1 archives. OpenBookQA is a general QA sanity check, not one of the five agent-related benchmark families. Current results live in [results/classmates](../results/classmates/README.md).
