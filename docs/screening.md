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

The current [complete score table](../results/classmates/README.md) includes every completed screen. Rows are different benchmark families, not cherry-picked task slices counted as separate benchmarks. Components differ in scope and difficulty; there is no pooled leaderboard score.

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
