<div align="center">

<img src="assets/cover.png" alt="CSIEE: Three students. Zero studying. Xiaoming picks the longest, Xiaohong picks C, and Xiaogang picks the odd one out." width="100%">

# Chinese Student in English Exam

**Your agent has a vector database. Xiaoming has a ruler.**

Zero parameters · Zero API calls · Suspiciously nonzero accuracy

[Meet the class](#meet-the-class) · [Report card](#report-card) · [Run it](#run-it) · [Methods](docs/methodology.md)

</div>

CSIEE turns exam-guessing folklore into **option-only baselines for agent benchmarks**. The students never see the question, conversation, tools, or environment. They see the choices. They make a choice. They go home.

The premise is a joke. The measurements are real.

## Meet the class

| Student | Entire research agenda | Equipment |
| :-- | :-- | :-- |
| **Xiaoming** | Pick the longest option. | A ruler |
| **Xiaohong** | Pick C. Only two options? Pick B. | Conviction |
| **Xiaogang** | Classify the choices as numbers or text; pick the value or length farthest from the median. | A slightly larger ruler |

Xiaogang is **experimental**. His “type classifier” is a regex, not an LLM. Ties prefer C (B for two choices) when it is a tied candidate, then the earliest tied option. [Exact rules →](docs/methodology.md#the-three-rules)

```console
$ csiee guess "Yes" "No" "It depends on a surprisingly elaborate series of circumstances" "Maybe" --strategy xiaoming
{"strategy": "xiaoming", "index": 2, "label": "C", "option": "It depends on a surprisingly elaborate series of circumstances"}

$ csiee guess "A reasonable answer" "Another reasonable answer" "C" "An excellent answer" --strategy xiaohong
{"strategy": "xiaohong", "index": 2, "label": "C", "option": "C"}

$ csiee guess 10 11 12 99 --strategy xiaogang
{"strategy": "xiaogang", "index": 3, "label": "D", "option": "99"}
```

<!-- personamem:start -->
## PersonaMem-v2: a ruler enters the chat

![PersonaMem-v2: paper-reported MCQ results and the three CSIEE classmates, with input context and accuracy on a shared scale](assets/personamem-comparison.png)

**Xiaoming: 45.62%. GPT-5-Chat, as reported in the paper: 45.6%.** One brought a ruler; the other received 32k of conversation history. These are different evaluation pipelines, not a claim of equivalent capability.

<details>
<summary><strong>The same table, in text — paper values and our measurements</strong></summary>

| Method | History / memory | MCQ accuracy | Shuffled mean | Source |
| :-- | :-- | --: | --: | :-- |
| GPT-5-mini | 32k history | 48.7% | — | Paper Fig. 4 |
| GPT-5-Chat | 32k history | 45.6% | — | Paper Fig. 4 |
| Qwen3-4B · Agentic Memory | 2k memory* | 55.2% | — | Paper Fig. 6 |
| Qwen3-4B · GRPO | 32k history | 53.8% | — | Paper Fig. 6 |
| **Xiaoming · longest** | **Options only** | **45.62%** | 45.59% | CSIEE, n=5,000 |
| **Xiaohong · C** | **Options only** | **24.68%** | 25.22% | CSIEE, n=5,000 |
| **Xiaogang · outlier** | **Options only** | **36.90%** | 37.05% | CSIEE, n=5,000 |
| Uniform chance | Options only | 25.00% | 25.00% (expected) | Analytical |

Paper: [Jiang et al., Figs. 4 & 6](https://arxiv.org/html/2512.06688v1#S4); MCQ only, with 32k frontier results. *Agentic Memory builds a 2k memory from 32k history. CSIEE uses seed 42 and reconstructed option order on all 5,000 text MCQs. Published model scores were not rerun. Paper values retain one decimal; local scores retain two. “—” means no paper permutation control is available.

</details>

[Full comparison, 128k results & source notes](docs/personamem-comparison.md) · [Vector figure](assets/personamem-comparison.svg)

Four paper references are shown for clarity; base/SFT models, training ablations and other frontier variants remain in the full comparison.
<!-- personamem:end -->

## Report card

Five agent-related benchmark families. Memory, social reasoning, planning, agentic subtasks, and scientific research. **Native multiple-choice components only**; these are not end-to-end agent scores.

Accuracy on the recorded input order, seed **42**. “Chance” is the exact expected score of uniform guessing for each question's number of options.

<!-- report-card:start -->
| Benchmark / evaluated component | Questions | Chance | Xiaoming | Xiaohong | Xiaogang |
| :-- | --: | --: | --: | --: | --: |
| [PersonaMem-v2](results/classmates/personamem-v2/report.md) · text memory | 5,000 | 25.00% | 45.62% | 24.68% | 36.90% |
| [AgentSense](results/classmates/agentsense/report.md) · information reasoning | 1,863 | 25.00% | 49.87% | 25.17% | 49.44% |
| [ACPBench](results/classmates/acpbench/report.md) · seven planning tasks | 895 | 25.00% | 20.22% | 25.25% | 34.08% |
| [APTBench](results/classmates/aptbench/report.md) · seven English MCQ tasks | 4,215 | 20.84% | 16.39% | 20.76% | 11.81% |
| [AgentHop](results/classmates/agenthop/report.md) · research MCQs | 1,011 | 25.00% | 0.89% | 27.50% | 18.40% |
<!-- report-card:end -->

> **Teacher's note:** Xiaoming gets 49.87% on AgentSense and 0.89% on AgentHop. The ruler has range. Unfortunately, so do the consequences.

Three families show a positive shortcut signal. Two show a strong **reverse signal**: the heuristic systematically underperforms chance. Five interesting results, not five victories.

<details>
<summary><strong>We moved the answers around. Here is what happened.</strong></summary>

Mean accuracy across **10 label-preserving option permutations** per question, using the same seed and unchanged strategies:

<!-- shuffle-card:start -->
| Benchmark | Xiaoming | Xiaohong | Xiaogang | Seeded random |
| :-- | --: | --: | --: | --: |
| PersonaMem-v2 | 45.59% | 25.22% | 37.05% | 25.11% |
| AgentSense | 49.69% | 25.10% | 49.57% | 24.78% |
| ACPBench | 19.49% | 24.41% | 33.33% | 24.77% |
| APTBench | 16.41% | 20.79% | 11.85% | 20.92% |
| AgentHop | 0.98% | 25.00% | 18.46% | 24.81% |
<!-- shuffle-card:end -->

Xiaohong's faith in C returns to roughly chance. The length-based signals survive. PersonaMem's initial order is a seeded reconstruction from its released correct/wrong answer fields, not the official evaluation order.

The [individual reports](results/classmates/README.md) include uncertainty intervals, permutation ranges, choice invariance, per-category counts, source revisions, and data hashes. Repeated permutations are sensitivity checks, not extra independent questions.

</details>

This showcase is **exploratory and selected after screening**. BixBench, Backtrader-Bench, and the publicly labeled FDABench subset are also reported, including weak and negative outcomes. Read the [screening ledger](docs/screening.md) for all eight, exclusions, and scope. We did not invent MCQs for open-ended tasks or tune a rule per benchmark.

## Run it

Python **3.9+**. No runtime dependencies. No API key. No motivational speech.

```bash
git clone https://github.com/ya-way/CSIEE.git
cd CSIEE
python -m pip install .

# A tiny synthetic fixture: tests the plumbing, proves no scientific point.
csiee eval data/demo.jsonl --shuffles 10 --output results/local/demo

# Download pinned releases and reproduce the five-family report card.
csiee suite --seed 42 --shuffles 10 --output results/local/suite

# Include all three additional screened datasets.
csiee suite --all --seed 42 --shuffles 10 --output results/local/all
```

Cloning requires repository access while this project is private. Dataset downloads require internet access; guessing and evaluation run locally. Downloads stay in ignored `data/raw/`. Existing suite inputs are checked against their source manifests. Reports contain `summary.json`, `report.md`, and `predictions.jsonl`.

<details>
<summary><strong>Bring your own exam</strong></summary>

One question per JSONL line, with a **zero-based** answer index:

```json
{"id":"q1","options":["10","11","12","99"],"answer":3,"category":"demo"}
```

```bash
csiee eval my-exam.jsonl --seed 42 --shuffles 10 --output results/local/my-exam
python -m unittest discover -s tests -v
```

Options must contain 2–26 nonempty, distinct strings. IDs must be unique. The predictor receives only the option strings; answer labels stay in the evaluator. The default report includes all three students and a seeded random baseline.

</details>

## Questions from the back row

**Did you beat an agent?**

We measured guessing from choices alone. We did not run agents, tools, retrieval, or environments. There is no apples-to-agents leaderboard here.

**Does this prove a benchmark is broken?**

No. It identifies answer-option patterns worth investigating. Correlated questions, subset selection, and exploratory screening limit the conclusions. [Methods and limitations →](docs/methodology.md)

**Is Xiaogang intelligent?**

He brought `statistics.median` to an exam. Please respect his journey. All five featured datasets route to his length rule; numeric routing is exercised in the additional datasets.

**Where did Lite / Pro / Pro Max go?**

They graduated into [legacy ablations](docs/methodology.md#legacy-ablations). Their CLI names and earlier reports still work; the current cast is Xiaoming, Xiaohong, and Xiaogang.

---

[Contribute](CONTRIBUTING.md) · [Source credits & scope](docs/screening.md) · [Artwork & prompt](assets/README.md) · [MIT license](LICENSE)

Original code is MIT-licensed. Upstream datasets retain their own terms; raw benchmark content is not committed.

<div align="center"><sub>Built with no understanding of the question.</sub></div>
