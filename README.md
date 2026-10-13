<div align="center">

<img src="assets/cover.png" alt="CSIEE: Three students. Zero studying. Xiaoming picks the longest, Xiaohong picks C, and Xiaogang picks the odd one out." width="100%">

# Chinese Student in English Exam

**Your agent has a vector database. Xiaoming has a ruler.**

Zero parameters · Zero API calls · Suspiciously nonzero accuracy

[Meet the class](#meet-the-class) · [Five charts](#five-exams-three-students-no-studying) · [Report card](#report-card) · [Run it](#run-it) · [Methods](docs/methodology.md)

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
## Five exams. Three students. No studying.

Paper results and CSIEE measurements share each chart, sorted from highest to lowest. **Every baseline in the selected paper columns is retained, including low scores.** Teal is paper-reported; red is options-only. Different inputs and evaluation pipelines make these contextual comparisons, not matched agent leaderboards.

### PersonaMem-v2

![PersonaMem-v2: descending vertical bars, paper results and CSIEE](assets/personamem-comparison.png)

Text-memory MCQs · 32k history setting. Paper: 32k history; Agentic Memory compresses it to 2k. CSIEE: options only, n=5,000.

<details>
<summary>All values, in one table</summary>

| Method | Accuracy | Input / protocol | Source | Shuffled mean |
| :-- | --: | :-- | :-- | --: |
| Qwen3-4B · GRPO (MCQ-only) | 55.5% | 32k history | Paper: Figure 6 | — |
| Qwen3-4B · Agentic Memory | 55.2% | 2k memory* | Paper: Figure 6 | — |
| Qwen3-4B · GRPO | 53.8% | 32k history | Paper: Figure 6 | — |
| GPT-5-mini | 48.7% | 32k history | Paper: Figure 4 | — |
| **Xiaoming · longest** | **45.62%** | Options only | CSIEE: Saved CSIEE counts | 45.59% |
| GPT-5-Chat | 45.6% | 32k history | Paper: Figure 4 | — |
| o4-mini | 39.1% | 32k history | Paper: Figure 4 | — |
| GPT-4.1 | 38.7% | 32k history | Paper: Figure 4 | — |
| GPT-5-nano | 37.9% | 32k history | Paper: Figure 4 | — |
| GPT-4.1-mini | 37.6% | 32k history | Paper: Figure 4 | — |
| **Xiaogang · outlier** | **36.90%** | Options only | CSIEE: Saved CSIEE counts | 37.05% |
| Qwen3-4B · GRPO (OE-only) | 35.6% | 32k history | Paper: Figure 6 | — |
| Qwen3-4B · SFT | 35.0% | 32k history | Paper: Figure 6 | — |
| Qwen3-4B · Base | 30.5% | 32k history | Paper: Figure 6 | — |
| **Xiaohong · C** | **24.68%** | Options only | CSIEE: Saved CSIEE counts | 25.22% |
| Uniform chance | 25.00% | Options only | Analytical expectation | — |

</details>

[Source notes and exact scope](docs/personamem-comparison.md) · [Vector figure](assets/personamem-comparison.svg)

### AgentSense

![AgentSense: descending vertical bars, paper results and CSIEE](assets/agentsense-comparison.png)

Information reasoning · Info / Acc.. Paper: agent interactions + MCQs. CSIEE: options only, n=1,863; one invalid MCQ excluded.

<details>
<summary>All values, in one table</summary>

| Method | Accuracy | Input / protocol | Source | Shuffled mean |
| :-- | --: | :-- | :-- | --: |
| GPT-4o | 76.86% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| Qwen2.5-72b | 76.05% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| Qwen2.5-14b | 75.02% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| Qwen2.5-7b | 74.82% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| Llama-3-70b | 73.08% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| Llama-3-8B | 69.68% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| GPT-3.5-turbo | 68.41% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| Mistral-7b | 66.59% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| **Xiaoming · longest** | **49.87%** | Options only | CSIEE: Saved CSIEE counts | 49.69% |
| **Xiaogang · outlier** | **49.44%** | Options only | CSIEE: Saved CSIEE counts | 49.57% |
| Llama-2-70b | 36.78% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| Llama-2-7b | 33.06% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| Llama-2-13b | 28.56% | Agent interaction + question + choices | Paper: Table 1, Info / Acc. column | — |
| **Xiaohong · C** | **25.17%** | Options only | CSIEE: Saved CSIEE counts | 25.10% |
| Uniform chance | 25.00% | Options only | Analytical expectation | — |

</details>

[Source notes and exact scope](docs/agentsense-comparison.md) · [Vector figure](assets/agentsense-comparison.svg)

### ACPBench

![ACPBench: descending vertical bars, paper results and CSIEE](assets/acpbench-comparison.png)

MCQ accuracy · macro-average across seven planning tasks. Paper: 2-shot CoT. CSIEE: options only, n=895; equal weight per task, five invalid MCQs excluded.

<details>
<summary>All values, in one table</summary>

| Method | Accuracy | Input / protocol | Source | Shuffled mean |
| :-- | --: | :-- | :-- | --: |
| LLAMA-3.1 405B | 77.42% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| GPT-4o | 74.97% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| LLAMA-3 70B | 74.30% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| LLAMA-3.1 70B | 66.94% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| GPT-4o Mini | 56.50% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Mixtral 8x7B | 51.44% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| LLAMA-3 8B | 44.05% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| LLAMA-3.1 8B | 41.52% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Codestral 22B | 40.97% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Mixtral 8x22B | 39.25% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Mistral Inst. 7B | 37.30% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| LLAMA-c 34B | 35.71% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Deepseek Inst. 33B | 35.11% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Phi-3 128K | 34.75% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| **Xiaogang · outlier** | **34.25%** | Options only | CSIEE: Saved CSIEE counts | — |
| LLAMA-c 70B | 32.87% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Granite-c Inst. 8B | 32.63% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| LLAMA-2 70B | 29.71% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Granite 7B | 29.67% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Granite-c 8B | 29.21% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Gemma 7B | 28.93% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Mistral 7B | 28.67% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| Granite 13B | 26.66% | Question + choices; 2-shot CoT | Paper: Table 2, Mean / MCQ column | — |
| **Xiaohong · C** | **25.29%** | Options only | CSIEE: Saved CSIEE counts | — |
| **Xiaoming · longest** | **20.22%** | Options only | CSIEE: Saved CSIEE counts | — |
| Uniform chance | 25.00% | Options only | Analytical expectation | — |

</details>

[Source notes and exact scope](docs/acpbench-comparison.md) · [Vector figure](assets/acpbench-comparison.svg)

### APTBench

![APTBench: descending vertical bars, paper results and CSIEE](assets/aptbench-comparison.png)

Deep research · closed-ended Plan_EN subset. Paper: base models + task context. CSIEE: options only, n=614; six choices per question.

<details>
<summary>All values, in one table</summary>

| Method | Accuracy | Input / protocol | Source | Shuffled mean |
| :-- | --: | :-- | :-- | --: |
| Kimi K2-1TA32B | 86.64% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| GLM4.5-355BA32B | 85.50% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| DeepSeek-V3.1-671BA37B | 84.04% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| DeepSeek-V3-671BA37B | 82.31% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| Seed-OSS-36B | 81.60% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| Llama4-Scout-109BA17B | 78.01% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| GLM4.5-Air-106BA12B | 74.27% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| Qwen3-8B | 73.94% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| Gemma3-27B | 73.13% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| Qwen3-30BA3B | 73.13% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| Qwen3-4B | 72.48% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| Qwen3-1.7B | 53.09% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| SmolLM-3B | 48.70% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| Llama3.2-3B | 41.69% | Base model; task context + question + choices | Paper: Table 3, Closed-ended Question / Plan_EN (ACC), first numeric column | — |
| **Xiaoming · longest** | **20.36%** | Options only | CSIEE: Saved CSIEE counts | — |
| **Xiaohong · C** | **16.94%** | Options only | CSIEE: Saved CSIEE counts | — |
| **Xiaogang · outlier** | **7.33%** | Options only | CSIEE: Saved CSIEE counts | — |
| Uniform chance | 16.67% | Options only | Analytical expectation | — |

</details>

[Source notes and exact scope](docs/aptbench-comparison.md) · [Vector figure](assets/aptbench-comparison.svg)

### AgentHop

![AgentHop: descending vertical bars, paper results and CSIEE](assets/agenthop-comparison.png)

Scientific research MCQs · answer accuracy. Paper: agents with paper-search tools and resource caps. CSIEE: options only, n=1,011.

<details>
<summary>All values, in one table</summary>

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

</details>

[Source notes and exact scope](docs/agenthop-comparison.md) · [Vector figure](assets/agenthop-comparison.svg)

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
