# Screening ledger

Eight benchmark families were evaluated during the classmates redesign. The five on the front page were selected after observing results. “Signal” describes answer-option structure, not an agent's competence. All measurements use seed 42, ten option permutations, and the same three rules.

## Evaluated sources

| Official release | Included / candidates | Evaluated component | Outcome after shuffling |
| :-- | --: | :-- | :-- |
| [PersonaMem-v2](https://huggingface.co/datasets/bowen-upenn/PersonaMem-v2) | 5,000 / 5,000 | Full text-memory benchmark CSV; no history input | Positive length signal |
| [AgentSense](https://github.com/ljcleo/agent_sense) | 1,863 / 1,864 | All released information-reasoning questions inside character scenarios; no simulated interaction | Positive length signal |
| [ACPBench](https://github.com/IBM/ACPBench) | 895 / 900 | Original MCQ test splits: app, areach, just, land, prog, reach, val | Positive length-outlier signal |
| [APTBench](https://github.com/TencentYoutuResearch/APTBench) | 4,215 / 4,273 | Seven English tasks with explicit labeled choices | Reverse outlier signal |
| [AgentHop](https://huggingface.co/datasets/agenthop/agenthop) | 1,011 / 1,011 | Full research MCQ release; no papers, retrieval, or tools | Strong reverse length signal |
| [BixBench v1.5](https://huggingface.co/datasets/futurehouse/BixBench) | 205 / 205 | Native MCQ: ideal answer + three released distractors; no optional refusal | No positive signal above the +5 pp screening threshold |
| [Backtrader-Bench](https://github.com/rzhao999/Backtrader-Bench) | 160 / 160 | Full MCQ base pool, not the curated 30-question subset | No positive signal above the +5 pp screening threshold |
| [FDABench-Full](https://huggingface.co/datasets/FDAbench2026/FDAbench-Full) | 237 / 579 | Publicly labeled single-choice rows only | Reverse signal on a label-availability subset |

The initial eight production screens are preserved in the [complete score table](../results/classmates/README.md). The expansion below distinguishes full components, versions, selected subtasks and exploratory pilots. Components differ in scope and difficulty; there is no pooled leaderboard score.

## Exclusions and boundaries

- **AgentSense:** one question has duplicate option text after stripping whitespace. Its 1,225 source scenarios contain multiple characters and questions; 1,863 questions are not 1,863 independent scenarios.
- **ACPBench:** five duplicate-option questions excluded. Boolean, generative, and newer extended variants are outside this adapter's scope.
- **APTBench:** 58 excluded records: 47 duplicate-option rows, 10 rows with gold labels absent from the released choices, and one ambiguous/nonconsecutive marker layout. Every ID and reason is saved in the summary. Included task paths are `agentic_math/action_cal`, `agentic_math/planning_single`, `deepresearch/plan_en`, `env_setup/error`, `env_setup/plan`, `issue_fix/locate`, and `issue_fix/plan`. Chinese tasks, boolean feedback, open completion, and tool-name completion are outside scope. No distractors were constructed for those tasks.
- **FDABench:** 342 single-choice records lack public gold labels and are excluded. The 237 scored records are a selected public-label subset, not the full benchmark; multiple-choice and report-generation tasks are outside scope.
- **PersonaMem-v2, AgentHop, BixBench, Backtrader-Bench:** no record-level exclusions from the listed components.

Early adapter pilots were exploratory. Final APTBench scores use a parser that handles both inline and multiline choice markers, with explicit malformed-record exclusions. The final FDA run uses only released gold labels. Preliminary counts and scores are superseded by the committed reports; they are not additional independent experiments.

OpenBookQA was evaluated in the earlier v0.1 project as a general QA control. Its [archived report](../results/openbookqa/report.md) remains available, but it is not counted as an agent benchmark. No end-to-end score is claimed for open-ended agent environments, and no inaccessible or unlabeled component is assigned a fabricated score.

## Revisions and terms

| Source | Pinned revision | Upstream terms recorded |
| :-- | :-- | :-- |
| PersonaMem-v2 | `ed956dea41521fc4499acbc63f966e0fd3c053ba` | CC-BY-4.0 |
| AgentSense | `21b6ef909cabcd4a72cded7580869e1e28c0e628` | MIT, repository |
| ACPBench | `2ed9c925962d57b275bf8c4e7b5d6f564aac9d6d` | CDLA-Permissive-2.0 |
| APTBench | `9aab1301ab2c743be6bf11d1a2f3c3c6bc123ffc` | Apache-2.0, repository |
| AgentHop | `599b0659343a7a3cc852a60c2e527150121cccdf` | CC-BY-4.0 |
| BixBench | `f8cc3bdcc6357c88b8c3648306522b9c422dc95a` | Apache-2.0 |
| Backtrader-Bench | `a623e5d3e55126142a163c43f57ebc5d7178f316` | No explicit dataset license found; consult upstream |
| FDABench-Full | `0e05e5ec2c95fbe462bed0cba1882f99989ab34e` | MIT, dataset card |

These links credit the benchmark creators; CSIEE is not affiliated with them. Pinned per-file URLs and hashes live in each `summary.json`. We commit no raw benchmark corpus. The project's MIT license covers its original code, not a relicensing of upstream data.


## October 16 expansion: selected after screening

The original eight screens above are retained. Five additional **components** were selected using best-of-three shuffled accuracy minus the analytical chance score. The reference is PersonaMem-v2: **+20.592 pp**. No strategy was changed. Ten permutations are order controls, not held-out validation. This search was requested for positive signals and is deliberately not representative.

| Added component | Included / candidates | Best shuffled score | Chance | Lift |
| :-- | --: | --: | --: | --: |
| [PERMA (Type 3)](../results/classmates/perma/report.md) | 580 / 580 | 93.93% | 12.50% | +81.43 pp |
| [MemBench (multi-session assistant subtask)](../results/classmates/membench-msa/report.md) | 500 / 500 | 100.00% | 25.00% | +75.00 pp |
| [PersonaMem-v1 (128k)](../results/classmates/personamem-v1/report.md) | 2,612 / 2,727 | 52.51% | 25.00% | +27.51 pp |
| [GUI-World (released benchmark MCQs)](../results/classmates/gui-world/report.md) | 3,643 / 3,646 | 50.49% | 25.00% | +25.49 pp |
| [MMBench-GUI (L1)](../results/classmates/mmbench-gui-l1/report.md) | 3,561 / 3,561 | 45.46% | 22.08% | +23.38 pp |

PersonaMem-v1 and v2 are one family. MemBench msa is a selected subtask; the full screen below does not show a comparable signal. These additions therefore bring the gallery to **ten components across nine families**, not ten independent full benchmarks. MMBench-GUI clears the criterion because of its lower chance baseline, despite a slightly lower shuffled raw accuracy than PersonaMem-v2.

### Additional exploratory screens, including unsuccessful candidates

These are screening-stage measurements, not promoted production evaluations. Source pins, all three rules, exclusions and normalized-file hashes are preserved in the [machine-readable screening record](../results/screening/2026-10-16.json). Provisional adapter assumptions are labeled; these are not claims of fully validated null results.

| Candidate / pilot scope | Included | Best shuffled score | Chance | Lift |
| :-- | --: | --: | --: | --: |
| prefeval | 1,000 | 42.00% | 25.00% | +17.00 pp |
| socialbench-en | 2,935 | 39.42% | 23.41% | +16.01 pp |
| tombench-en | 2,375 | 29.69% | 25.00% | +4.69 pp |
| membench-all | 25,874 | 27.60% | 25.00% | +2.60 pp |
| membench-ThirdAgent-highlevel | 1,500 | 25.08% | 25.00% | +0.08 pp |
| memeye | 371 | 32.26% | 25.00% | +7.26 pp |
| agentdrive-checked | 200 | 40.10% | 25.00% | +15.10 pp |
| robobench-mcq | 1,892 | 24.99% | 25.00% | -0.01 pp |
| agentvidbench | 100 | 4.70% | 3.85% | +0.85 pp |
| gui-knowledge-mcq | 2,425 | 28.68% | 22.85% | +5.83 pp |
| personamem-v1-32k | 572 | 57.38% | 25.00% | +32.38 pp |

PrefEval assumes the first stored choice is gold; GUI-Knowledge uses `option_text` and needs further reconciliation with its message template. Neither was promoted. The 32k PersonaMem pilot is positive but is not counted as a sixth addition. The early MemBench highlevel pilot overlaps the full MemBench screen. Early GUI-World scores that did not map exact-text gold are superseded by the complete production adapter.

GuideBench annotations were gated (HTTP 401). AMA-Bench exposed open-ended QA in the inspected release. InMind, LLM-Coordination and WhodunitBench were inspected but not scored. These candidates have no invented scores.

### New adapter boundaries

- **PERMA:** all 580 Type-3 overall MCQs (423 single-domain, 157 multi-domain); Type-1/2 checkpoint variants are outside this component. The chart uses the single-domain category to align Table 4.
- **MemBench msa:** full 500-question RecMultiSession pool. List options use upstream-compatible Python string interpolation. The paper compares sampled 10k-context runs, not this full pool.
- **PersonaMem-v1:** 2,612 of 2,727 128k rows; all 115 exclusions are duplicate option text. This earlier dataset version is not arXiv paper version v1: the cited paper is arXiv v2.
- **GUI-World:** 3,643 of 3,646 MCQs from 1,823 video records. One duplicate option row and two answers without an explicit label or unique exact text match are excluded. The paper describes 1,677 test videos; release/paper identity is unresolved.
- **MMBench-GUI:** all 3,561 L1 questions; no record exclusions. Paper describes 3,582. Its adjusted score and ordinary accuracy are kept separate. L2–L4 are outside scope.

The new pinned URLs, SHA-256 hashes and every exclusion are embedded in the linked production summaries. No raw benchmark corpus is committed.
