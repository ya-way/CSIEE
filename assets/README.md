# Cover artwork

`cover.png` is an original AI-generated illustration made with the built-in image generation tool for this repository on 2026-10-13. It is committed locally and referenced by a relative path; no external image host is required.

Visual direction: a cream exam-paper zine, black ink, red teacher annotations, muted teal, and three original cartoon students. The README takes inspiration from the deadpan premise of [No Code](https://github.com/kelseyhightower/nocode) and the demonstration-first presentation of [The Fuck](https://github.com/nvbn/thefuck). Their artwork and copy are not reused.

The illustration is a joke, not a diagram of an evaluated example. See `cover-prompt.txt` for the exact generation prompt.

## Examination stationery

The admission ticket, three student cards, end-of-paper colophon, Python badge and license badge are original, self-contained SVG designs. They use the same cream, charcoal, red and teal palette as the illustration. The ticket's question count is derived from the five committed benchmark summaries. Candidate cards describe the actual rules; their decorative diagrams are not benchmark measurements.

The ticket and roster each have a mobile layout selected through GitHub's supported `picture` element. Text alternatives and the expandable plain-text rules keep the content accessible. All graphics load from this repository. The CI badge is supplied by GitHub Actions and reflects the actual workflow status.

Regenerate the SVG artwork with `python scripts/render_homepage_assets.py` (standard library only). The [source script](../scripts/render_homepage_assets.py) and [homepage design notes](../docs/plans/2026-10-14-public-homepage-design.md) are included.

## Five benchmark comparisons

`personamem-comparison`, `agentsense-comparison`, `acpbench-comparison`, `aptbench-comparison`, and `agenthop-comparison` each have PNG and SVG exports. These are original Matplotlib renderings of cited numerical results and local CSIEE counts, not generated illustrations or copies of paper figures. The cream, charcoal, teal and red palette carries the cover's visual direction into precise vertical bar charts. All selected paper baselines are retained and sorted by descending accuracy alongside the three classmates.

See the [five-figure gallery and source notes](../docs/benchmark-comparisons.md), [paper-value transcriptions](../data/paper), and [reproducible rendering script](../scripts/render_benchmarks.py). APTBench uses its Plan_EN subtask; ACPBench uses task-macro accuracy. Every figure labels its scope and distinguishes reported paper scores from measured options-only results.
