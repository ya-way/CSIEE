# PersonaMem-v2 comparison figure

Historical plan, superseded by the [five-figure revision](2026-10-13-five-benchmark-figures.md): all 12 PersonaMem baselines are now restored and displayed as descending vertical bars.

Create an English figure and one combined table showing the paper's reported MCQ values alongside CSIEE's measured option-only results. Following the user's simplification request, the figure and README table retain GPT-5-mini, GPT-5-Chat, Qwen3-4B GRPO and Agentic Memory, plus all three classmates. Preserve all twelve paper configurations in the full source document, and the six 128k frontier values in a supplementary table. Exclude open-ended evaluation scores.

Design: compact horizontal bars, cream paper, charcoal typography, muted teal paper results, dark red classmates, a shared zero-based 0–60% axis and a 25% chance line. Group by provenance rather than implying a single controlled leaderboard. Small labels record history/memory access. Preserve one decimal for paper values and two for local measurements. Export reproducible PNG and SVG using Matplotlib; keep a machine-readable transcription and generate the Markdown tables from the same records.

Caption: the paper's model scores are cited, not rerun; CSIEE uses all 5,000 pinned text MCQs with seeded reconstructed option order. The 2k agentic memory is constructed from 32k history. Similar accuracy is not evidence of equivalent personalization ability or statistical superiority. Link the exact source figures and local summary.
