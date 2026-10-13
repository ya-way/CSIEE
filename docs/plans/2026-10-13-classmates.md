# CSIEE classmates redesign

Goal: keep ya-way/CSIEE private; present three exam-taking characters in English; expand to five distinct agent-related benchmark families with observable option-only signals.

## Fixed strategy specification, before new screening

- Xiaoming: select the longest stripped option, ties prefer C then earliest index.
- Xiaohong: select C (or B for two options).
- Xiaogang (experimental): infer numeric versus textual answer type from the option set alone. If every option is a compatible scalar number, use numeric distance from the median; otherwise use character-length distance from the median. Choose the most distant option; ties prefer C then earliest index. No question/label/history access, no per-benchmark fitting.
- Keep the previous rules as explicitly legacy ablations, not the main cast. Default reporting shows the three named strategies and random.

## Research and reporting

Inspect official releases for agent planning, tool/action selection, research, social reasoning, and memory. Use native MCQ components only, describe any subset, never manufacture distractors for open-ended tasks. A five-row showcase must comprise five benchmark families, not five slices of one dataset. Record every screened candidate including null results, failures and inaccessible data. Define exploratory signal as >5 percentage points above chance after option permutations, and display order-only signals separately. Dataset selection is exploratory and must be disclosed.

## Build and verify

1. Add named strategies and tests for type routing, numeric units, outliers, ties and answer isolation.
2. Pin source revisions/hashes; add strict adapters and source manifests.
3. Run unchanged strategies on full supported splits, save summaries and predictions, then build a five-family comparison and screening ledger.
4. Replace the front page with an English exam-paper parody: illustrated cast, minimal premise, actual tiny algorithm, measured report card, runnable commands, methods in a separate document.
5. Use the built-in image generator for the cover; preserve the image and prompt in the repository. Visual references: the deadpan minimalism of kelseyhightower/nocode and demonstration-first README of nvbn/thefuck, without copying their copy or artwork.
6. Test, push to private origin, verify privacy and CI. Do not publish or change visibility back to public.
