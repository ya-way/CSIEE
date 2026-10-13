# CSIEE — Chinese Student in English Exam

**Zero parameters. Zero API calls. Full confidence.** Confidence is the joke; the scores are measured.

[中文](README.md) · [Full results](results/personamem-v2/report.md) · [Methodology](docs/methodology.md)

CSIEE turns multiple-choice exam folklore into tiny, option-only baselines. It does not read questions, chat histories, or memory. It counts characters, notices absolute wording, and occasionally chooses C.

| Edition | Technology |
| :-- | :-- |
| Lite | Always C; B for two-choice questions |
| Pro | Choose a conspicuous length outlier, otherwise C |
| Pro Max | Vote across length folklore, third-largest numeric choice, and less absolute wording |

The strategy bodies are a few lines. Parsing, validation, reporting and tests are additional code, all public. Pro Max does not promise higher accuracy.

## Actual results

Full PersonaMem-v2 text benchmark, 5,000 questions, seed 42, 10 option-order controls. Rules were fixed before the run.

| Strategy | Accuracy | Mean after reshuffling |
| :-- | --: | --: |
| Uniform random expectation | 25.00% | 25.00% |
| Seeded random realization | 24.44% | 25.11% |
| Lite | 24.68% | 25.22% |
| Pro | 24.08% | 24.63% |
| Pro Max | 24.24% | 24.76% |
| **Always longest** | **45.62%** | **45.59%** |
| Always shortest | 23.28% | 23.16% |
| Third-largest number | 24.68% | 25.22% |
| Less absolute wording | 24.28% | 25.02% |

The strongest heuristic was simpler than Pro Max. Pro uses a fixed 1.5× outlier threshold; always-longest does not. Non-numeric options make the numeric heuristic fall back to C.

These results suggest an answer-length signal worth investigating. They do **not** measure memory, prove benchmark invalidity, or establish an official leaderboard rank. We reconstruct choice order with a stable seed rather than use the official evaluator's runtime order. Wilson intervals in the [report](results/personamem-v2/report.md) assume independent questions and do not adjust for shared personas. Report all heuristics and confirm any interesting result on a held-out dataset.

## Run it

An additional run on the full **OpenBookQA test split (500 questions)** uses the same unchanged rules: Lite **26.40%**, Pro **28.20%**, Pro Max **28.40%**, always-longest **36.60%** (reshuffled mean **36.22%**), versus 25% chance. See [all results](results/openbookqa/report.md). This is a second dataset comparison, not a universal generalization claim.

```bash
csiee download openbookqa
csiee eval data/raw/openbookqa.jsonl --format openbookqa --seed 42 --shuffles 10 --output results/local/openbookqa
```

OpenBookQA is downloaded from the official V1-Sep2018 archive with a pinned SHA-256. Credit: [Mihaylov et al., 2018](https://arxiv.org/abs/1809.02789). Its [dataset card](https://huggingface.co/datasets/allenai/openbookqa) leaves the dataset license unspecified. Raw questions are not redistributed here; consult upstream terms for reuse.

Python 3.9+, no runtime dependencies, GPU, API key or model download.

```bash
git clone https://github.com/ya-way/CSIEE.git
cd CSIEE
python -m pip install .
csiee guess 2 8 6 4 --strategy numeric
# D: 4, the third-largest number
csiee eval data/demo.jsonl --seed 42 --shuffles 10
```

The demo contains eight deliberately synthetic examples. It is not benchmark evidence. You can also use `python -m csiee` from the checkout without installing.

Reproduce the real experiment:

```bash
csiee download personamem-v2
csiee eval data/raw/personamem-v2.csv --format personamem-v2 --seed 42 --shuffles 10 --output results/local/personamem-v2
```

The download pins revision `ed956dea41521fc4499acbc63f966e0fd3c053ba` and records a source manifest plus SHA-256. Raw upstream data are ignored by Git. Existing downloads are never overwritten. Only downloading needs network access.

For your own benchmark, write UTF-8 JSONL with unique IDs, 2–26 non-empty distinct options, and a **zero-based integer** answer:

```json
{"id":"q1","options":["2","8","6","4"],"answer":3}
```

```bash
csiee eval your-benchmark.jsonl --output results/local/custom
python -m unittest discover -s tests -v
```

Every evaluation writes `report.md`, `summary.json` and `predictions.jsonl`. The exact chance baseline handles mixed choice counts. `--limit N` selects the first N records, not a random sample. See [methodology](docs/methodology.md) for all tie rules, metric definitions and limitations, and [CONTRIBUTING](CONTRIBUTING.md) to add a heuristic or adapter.

## Credit and license

Thanks to the [PersonaMem-v2 authors](https://github.com/bowen-upenn/PersonaMem-v2) for releasing their work: [dataset](https://huggingface.co/datasets/bowen-upenn/PersonaMem-v2), [paper](https://arxiv.org/abs/2512.06688). Upstream data are CC-BY-4.0. CSIEE code and original demo are [MIT](LICENSE).

Every good benchmark deserves a baseline that never reads the question.
