"""Render cited comparisons. Optional dependency: matplotlib==3.9.4."""
import json
import math
from pathlib import Path
from homepage_order import ORDER

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[1]
BG, INK, MUTED, GRID = '#F7F3E9', '#252927', '#6C726C', '#D9D8CD'
TEAL, RED = '#356C6B', '#AD493B'
STUDENTS = [('xiaoming', 'Xiaoming · longest'), ('xiaohong', 'Xiaohong · C'),
            ('xiaogang', 'Xiaogang · outlier')]
SPECS = [
    dict(key='personamem', dataset='personamem-v2', paper='personamem-v2-mcq',
         title='PersonaMem-v2', subtitle='Text-memory MCQs · 32k history setting', count=12,
         source='Jiang et al. / arXiv:2512.06688v1 / Figures 4 & 6',
         access='Paper: 32k history; Agentic Memory compresses it to 2k. CSIEE: options only, n=5,000.',
         note="All 12 paper configurations from Figures 4 and 6 are shown, including Base, SFT and both GRPO training ablations. The six frontier models use the 32k setting; 128k results remain in the appendix below. Agentic Memory builds up to 2k tokens of memory from 32k history. OE-only describes training; every plotted result is **MCQ** accuracy. CSIEE uses all 5,000 pinned text MCQs with reconstructed option order. Paper values have one decimal; the 45.62% local score versus 45.6% in the paper does not establish a meaningful win."),
    dict(key='agentsense', dataset='agentsense', paper='agentsense-info',
         title='AgentSense', subtitle='Information reasoning · Info / Acc.', count=11,
         source='Mou et al. / arXiv:2410.19346v2 / Table 1',
         access='Paper: agent interactions + MCQs. CSIEE: options only, n=1,863; one invalid MCQ excluded.',
         note="All 11 models in Table 1 are retained. Values come from **Info / Acc.**, not goal-completion scores or the PSI sensitivity statistic. The paper evaluates information reasoning after interactions between agents driven by the same model. CSIEE evaluates the released information MCQs without running those interactions; it retains 1,863 of 1,864 candidates after excluding one duplicate-option question. These protocols and denominators are not identical."),
    dict(key='acpbench', dataset='acpbench', paper='acpbench-mcq',
         title='ACPBench', subtitle='MCQ accuracy · macro-average across seven planning tasks', count=22,
         source='Kokel et al. / arXiv:2410.05669v3 / Table 2',
         access='Paper: 2-shot CoT. CSIEE: options only, n=895; equal weight per task, five invalid MCQs excluded.',
         note="All 22 models from Table 2 are shown, using the **Mean / MCQ** column for two-shot chain-of-thought prompting. Boolean scores and the zero-shot appendix are excluded. The paper averages seven task accuracies (five runs for most models; one for GPT models and Llama-3.1-405B). To align the aggregation, CSIEE is recomputed from the seven saved per-category correct/count pairs with **equal weight per task**. Thus the local bars differ slightly from the question-weighted report card. The released MCQ set has 900 candidates; CSIEE excludes five duplicate-option records and retains 895. Printed paper means are preserved as published rather than recalculated from rounded cells."),
    dict(key='aptbench', dataset='aptbench', paper='aptbench-plan-en',
         title='APTBench', subtitle='Deep research · closed-ended Plan_EN subset', count=14,
         source='Qin et al. / arXiv:2510.24397v1 / Table 3, first numeric column',
         access='Paper: base models + task context. CSIEE: options only, n=614; six choices per question.',
         note="All 14 base models from Table 3 are retained. Values use **Closed-ended Question / Plan_EN (ACC)**, the first numeric column, not the separate open-ended Plan_EN column or the mixed-metric Avg. The local bars use exactly the saved `deepresearch/plan_en` category: 614 questions, six options each, with no exclusions in this category. It was chosen for an explicit published MCQ accuracy and a direct released-task mapping, not to maximize a heuristic's score. This figure is **one subtask**, not the 4,215-question seven-task APTBench report card. The full screen and its reverse signal remain unchanged. Expected chance here is 1/6 (16.67%), not the full screen's 20.84%."),
    dict(key='agenthop', dataset='agenthop', paper='agenthop-accuracy',
         title='AgentHop', subtitle='Scientific research MCQs · answer accuracy', count=19,
         source='Park et al. / arXiv:2609.34428v1 / Table 2',
         access='Paper: agents with paper-search tools and resource caps. CSIEE: options only, n=1,011.',
         note="All 19 models from Table 2 are retained, including models below chance. The paper's **Outcome / Accuracy** fractions are multiplied by 100; three-decimal fractions become one-decimal percentages. This is neither paper recall nor synthesis conversion. The paper evaluates agents with a scientific-paper tool environment and resource caps; failed submissions count against accuracy. CSIEE evaluates the pinned 1,011 released MCQs without questions, tools or trajectories. We have not established item-by-item identity between that pinned release and every paper run, and these are not matched reruns."),
]

SPECS.extend([
    dict(key='perma', dataset='perma', paper='perma-clean-sd', title='PERMA · Type 3',
         subtitle='Clean single-domain MCQs · post-intervention checkpoint', count=17,
         source='arXiv:2603.23231v1 / Table 4, MCQ Acc.',
         access='Paper: history or memory. CSIEE: options only, n=423 single-domain Type-3 questions.',
         note='All 17 Table 4 baselines are retained, including every GPT-4o-mini memory system. The chart uses the **423 single-domain Type-3 questions**; the report card includes all **580** single- and multi-domain Type-3 questions. Type 1 and Type 2 are separate checkpoint variants and are not counted as additional questions here. The clean/noisy histories never enter CSIEE. This is an answer-choice audit, not an interactive task-completion score. Published and local pipelines differ; item-by-item identity of paper runs is not independently established.'),
    dict(key='membench-msa', dataset='membench-msa', paper='membench-msa', title='MemBench · multi-session assistant',
         subtitle='A selected subtask · factual participation / msa', count=7,
         source='arXiv:2506.21605v1 / Table 11, msa column',
         access='Paper: 10k memory context, sampled evaluation. CSIEE: all 500 released msa questions, options only.',
         note='This is **one selected subtask, not the whole MemBench benchmark**. All seven memory mechanisms in Table 11, `msa`, are retained, including the lowest result. CSIEE uses the full 500-question `FirstAgent/RecMultiSession.json` pool. The paper uses sampled trajectories with a 10k memory context, so these are different denominators and not paired runs. List-valued choices are rendered with Python `str`, matching upstream `MembenchAgent.py` string interpolation. The complete 25,874-question valid MemBench screen has only +2.60 pp best shuffled lift; the 100% result does not generalize to it. The subtask was selected after screening.'),
    dict(key='personamem-v1', dataset='personamem-v1', paper='personamem-v1-128k', title='PersonaMem-v1 · 128k',
         subtitle='An earlier version of the PersonaMem family · discriminative MCQs', count=15,
         source='Jiang et al. / arXiv:2504.14225v2 / Figure 4, upper-panel Overall column',
         access='Paper: 128k history + query. CSIEE: options only, n=2,612; 115 duplicate-option rows excluded.',
         note='All 15 model rows from Figure 4\'s **128k upper panel, Overall column**, are retained. The printed two-decimal fractions become integer percentages; neither the Average aggregate nor Random Guess is treated as another model. This is **PersonaMem-v1**, an earlier version of the same family as PersonaMem-v2, not an independent family. CSIEE evaluates 2,612 of 2,727 released 128k questions, excluding 115 duplicate-option records. The initial 32k screen is also retained in the screening ledger; 128k was selected to align with the paper\'s complete model comparison. Coarse printed precision and differing exclusions preclude a meaningful claimed win over a nearby paper score.'),
    dict(key='gui-world', dataset='gui-world', paper='gui-world-mcq', title='GUI-World',
         subtitle='Video GUI understanding · six-category macro-average MCQ accuracy', count=10,
         source='Chen et al. / arXiv:2406.10819v2 / Table 3, Avg. / MC',
         access='Paper: GUI video/keyframes + query. CSIEE: options only, n=3,643; six categories equally weighted.',
         note='All ten Table 3 models are retained, including the low-scoring video baselines. **Avg. / MC** is a macro-average across Software, Website, XR, Multi, IOS and Android; the CSIEE chart applies the same equal-category weighting. The report card is question-weighted. The pinned release contains 3,646 native MCQ candidates, of which three are excluded (one duplicate-option row and two unmappable gold answers). Exact answer text is mapped only on a unique exact match, never by semantic guessing. The release covers 1,823 video records, while the paper describes a 1,677-video test set: this release/paper difference is unresolved, so the comparison is contextual rather than item-matched.'),
    dict(key='mmbench-gui-l1', dataset='mmbench-gui-l1', paper='mmbench-gui-l1', title='MMBench-GUI · L1',
         subtitle='GUI content understanding · option-count-adjusted score', count=7,
         source='arXiv:2507.19478v1 / Table 5 + Equations 3–4',
         access='Paper: screenshots + query. CSIEE: options only, n=3,561; score = mean[(m−1)/m × correct].',
         note='All seven models in Table 5 are shown. Each model bar is the **arithmetic mean of its three printed Overall scores** (Easy, Medium, Hard); the paper gives equal difficulty counts, so no difficulty is selected for advantage. These bars are derived aggregates, not a separately printed total. Equations 3–4 discount each correct answer by `(m−1)/m`, with `m` choices. CSIEE and the chance line apply that same formula from saved per-option-count counts; the report card and screening criterion use ordinary accuracy. The released L1 file contains 3,561 questions, versus 3,582 described in the paper. The upstream repository flags figures for revalidation; these are specifically the cited v1 values, not a claim of validated current leaderboard performance. L2–L4 execution tasks are outside scope.'),
])


def write(path, value):
    path.write_bytes(value.encode('utf-8'))


def load_rows(spec):
    paper = json.loads((ROOT / f"data/paper/{spec['paper']}.json").read_text(encoding='utf-8'))
    summary = json.loads((ROOT / f"results/classmates/{spec['dataset']}/summary.json").read_text(encoding='utf-8'))
    assert (summary['seed'], summary['shuffle_repeats']) == (42, 10)
    assert len(paper['rows']) == spec['count']
    rows = [dict(r, origin='Paper', precision=paper.get('precision', 1),
                 source=f"Figure {r['figure']}" if 'figure' in r else paper['source']) for r in paper['rows']]
    chance = 100 * summary['chance_accuracy']
    for strategy, label in STUDENTS:
        result = next(r for r in summary['results'] if r['strategy'] == strategy)
        n, accuracy = summary['n'], result['accuracy']
        shuffled = 100 * result['shuffled_mean']
        if spec['key'] == 'acpbench':
            categories = result['by_category']
            assert set(categories) == {'app', 'areach', 'just', 'land', 'prog', 'reach', 'val'}
            accuracy = sum(c['correct'] / c['n'] for c in categories.values()) / 7
            shuffled = None  # Only question-weighted shuffle aggregates were saved.
        elif spec['key'] in {'aptbench', 'perma'}:
            category = result['by_category'][paper['local_category']]
            n = category['n']
            assert n == paper['local_n']
            accuracy = category['correct'] / n
            chance = 100 / paper['local_options_per_question']
            shuffled = None  # The full-screen permutation mean is not this subset's mean.
        elif spec['key'] == 'gui-world':
            categories = result['by_category']
            assert set(categories) == {'software', 'website', 'XR', 'multi', 'IOS', 'android'}
            accuracy = sum(c['correct'] / c['n'] for c in categories.values()) / 6
            shuffled = None
        elif spec['key'] == 'mmbench-gui-l1':
            buckets = result['by_option_count']
            assert sum(c['n'] for c in buckets.values()) == n
            accuracy = sum((int(m)-1)/int(m) * c['correct'] for m, c in buckets.items()) / n
            chance = 100 * sum((int(m)-1)/(int(m)**2) * c['n'] for m, c in buckets.items()) / n
            shuffled = None
        rows.append(dict(method=label, origin='CSIEE', context='Options only',
                         accuracy=100 * accuracy, precision=2, n=n,
                         shuffled=shuffled, source='Saved CSIEE counts'))
    rows.sort(key=lambda r: (-r['accuracy'], r['method']))
    assert len({r['method'] for r in rows}) == len(rows) == spec['count'] + 3
    assert all(math.isfinite(r['accuracy']) and 0 <= r['accuracy'] <= 100 for r in rows)
    return paper, summary, rows, chance


def render(spec, rows, chance, number):
    matplotlib.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                               'svg.hashsalt': 'csiee-five-benchmarks-v1', 'axes.unicode_minus': False})
    fig = plt.figure(figsize=(16, 9.5), facecolor=BG)
    fig.text(.06, .95, f'CSIEE / BENCHMARK NOTES                                      {number:02d} / {len(SPECS):02d}',
             fontsize=11, color=RED, weight='bold')
    fig.text(.06, .893, spec['title'], fontsize=30, color=INK, family='DejaVu Serif')
    fig.text(.06, .852, spec['subtitle'], fontsize=13, color=MUTED)
    ax = fig.add_axes([.065, .355, .91, .405], facecolor=BG)
    colors = [RED if r['origin'] == 'CSIEE' else TEAL for r in rows]
    ax.bar(range(len(rows)), [r['accuracy'] for r in rows], color=colors, width=.7, zorder=3)
    ax.set_ylim(0, 100)
    ax.set_xlim(-.65, len(rows) - .35)
    ax.set_yticks(range(0, 101, 20), [f'{v}%' for v in range(0, 101, 20)], color=MUTED)
    ax.yaxis.grid(True, color=GRID, linewidth=.65, zorder=0)
    ax.axhline(chance, color=MUTED, ls=(0, (4, 4)), lw=1, zorder=4)
    labels = []
    for row in rows:
        label = row['method'].replace(' · ', '\n')
        if '\n' not in label and len(label) > 19 and '-' in label:
            name, size = label.rsplit('-', 1)
            label = name + '\n' + size
        labels.append(label)
    ax.set_xticks(range(len(rows)), labels, rotation=55, ha='right', rotation_mode='anchor')
    for tick, row in zip(ax.get_xticklabels(), rows):
        tick.set_color(RED if row['origin'] == 'CSIEE' else INK)
        tick.set_fontweight('bold' if row['origin'] == 'CSIEE' else 'normal')
        tick.set_fontsize(11.5)
    ax.tick_params(axis='both', length=0, pad=9)
    for side in ['top', 'left', 'right']:
        ax.spines[side].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    for x, row in enumerate(rows):
        ax.text(x, row['accuracy'] + 1.5, f"{row['accuracy']:.{row['precision']}f}",
                ha='center', va='bottom', fontsize=10.5,
                color=RED if row['origin'] == 'CSIEE' else INK,
                weight='bold' if row['origin'] == 'CSIEE' else 'normal')
    legend = [Patch(color=TEAL, label=f"Paper / {'derived' if spec['key'] == 'mmbench-gui-l1' else 'reported'} ({spec['count']})"),
              Patch(color=RED, label='CSIEE / options only (3)'),
              Line2D([0], [0], color=MUTED, ls=(0, (4, 4)), label=f'Uniform chance / {chance:.2f}%')]
    fig.legend(handles=legend, loc='upper left', bbox_to_anchor=(.06, .819), frameon=False,
               ncol=3, fontsize=11, handlelength=1.8, columnspacing=2.6, borderaxespad=0)
    fig.add_artist(Line2D([.06, .975], [.16, .16], transform=fig.transFigure, color=INK, lw=.7))
    fig.text(.06, .126, spec['access'], fontsize=11, color=INK)
    fig.text(.06, .092, 'Different inputs and evaluation pipelines. Published scores are cited, not rerun.', fontsize=11, color=MUTED)
    fig.text(.06, .058, spec['source'], fontsize=10, color=MUTED)
    fig.text(.975, .058, 'HIGH → LOW / ALL LISTED BASELINES', fontsize=9, color=MUTED, ha='right')
    output = ROOT / f"assets/{spec['key']}-comparison"
    fig.savefig(output.with_suffix('.png'), dpi=180, facecolor=BG)
    fig.savefig(output.with_suffix('.svg'), facecolor=BG, metadata={'Date': None, 'Creator': 'CSIEE / Matplotlib'})
    svg = output.with_suffix('.svg')
    write(svg, '\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines()) + '\n')
    plt.close(fig)


def document(spec, paper, summary, rows, chance):
    title, key = spec['title'], spec['key']
    source = paper.get('source', 'Figures 4 and 6, MCQ labels')
    table = ['| Method | Accuracy | Input / protocol | Source | Shuffled mean |',
             '| :-- | --: | :-- | :-- | --: |']
    for row in rows:
        score = f"{row['accuracy']:.{row['precision']}f}%"
        name = row['method']
        if row['origin'] == 'CSIEE':
            name, score = f'**{name}**', f'**{score}**'
        shuffled = f"{row['shuffled']:.2f}%" if row.get('shuffled') is not None else '—'
        table.append(f"| {name} | {score} | {row['context']} | {row['origin']}: {row['source']} | {shuffled} |")
    table.append(f'| Uniform chance | {chance:.2f}% | Options only | Analytical expectation | — |')
    text = f"# {title}: paper results and the classmates\n\n![{title}, all listed baselines sorted by accuracy](../assets/{key}-comparison.png)\n\n"
    text += spec['note'] + '\n\n'
    text += f"Source: [{paper['version']}, {source}]({paper['url']}). Model scores are cited, not rerun. All models/configurations in the selected source column(s) are shown; none are filtered by score. Sorting is visual ordering, not a claim of statistical superiority or equivalent agent capability.\n\n"
    text += '## One table, both sources\n\n' + '\n'.join(table) + '\n\n'
    text += 'Local bars use input-order results, seed 42. “—” means unavailable for this exact metric, not zero. Shuffled controls are reported only where the saved aggregate uses the same question set and weighting as the chart. Full-screen controls remain in the original reports.\n\n'
    if key == 'personamem':
        text += "## The paper's 128k frontier setting\n\n| Frontier model | 32k MCQ | 128k MCQ |\n| :-- | --: | --: |\n"
        for row in paper['rows']:
            if 'mcq_128k' in row:
                text += f"| {row['method']} | {row['accuracy']:.1f}% | {row['mcq_128k']:.1f}% |\n"
        text += '\nThe figure consistently uses 32k frontier scores; it does not select each model\'s best context length.\n\n'
    text += f"## Reproduce and inspect\n\n- [Paper-value transcription](../data/paper/{spec['paper']}.json)\n- [Local summary](../results/classmates/{spec['dataset']}/summary.json) and [predictions](../results/classmates/{spec['dataset']}/predictions.jsonl)\n- [PNG](../assets/{key}-comparison.png) / [SVG](../assets/{key}-comparison.svg)\n- [Renderer](../scripts/render_benchmarks.py) / [all ten comparisons](benchmark-comparisons.md)\n\n"
    text += f"Local dataset SHA-256: `{summary['sha256']}`.\n\n```bash\npython -m pip install matplotlib==3.9.4\npython scripts/render_benchmarks.py\n```\n\nRendering uses committed numerical records only; no API calls or raw dataset downloads are required. Matplotlib is an optional figure-building dependency.\n"
    write(ROOT / f'docs/{key}-comparison.md', text)
    return '\n'.join(table)


def main():
    section = '## Ten exams. Three students. No studying.\n\n'
    anchors = {'perma': 'perma--type-3', 'membench-msa': 'membench--multi-session-assistant',
               'personamem-v1': 'personamem-v1--128k', 'mmbench-gui-l1': 'mmbench-gui--l1'}
    specs = sorted(SPECS, key=lambda spec: ORDER.index(spec['dataset']))
    section += ' · '.join(f"[{i:02d} {spec['title']}](#{anchors.get(spec['dataset'], spec['dataset'])})" for i, spec in enumerate(specs, 1)) + '\n\n'
    section += '**The literature meets the stationery aisle.** Teal bars are published model results; red bars are our three option-only rules. Every baseline in the selected paper columns stays on the page, sorted high to low. Different inputs and evaluation pipelines mean these are contextual comparisons, not a matched agent leaderboard.\n\n'
    quips = ['5,000 memory questions. No memories consulted.',
             'No conversation. Still 49.87% for Xiaoming.',
             'Xiaogang brought a slightly larger ruler.',
             'This is the part where the ruler loses.',
             '0.89%. Even a ruler has a bad day.',
             'Your memory system remembers preferences. The ruler remembers nothing.',
             'A perfect score. On one very specific exam.',
             'Same family. Earlier syllabus. Still suspiciously measurable.',
             'The screen is off. The ruler is on.',
             'No screenshot was harmed in this evaluation.']
    gallery = '# Ten benchmark comparisons\n\nVertical bars, descending accuracy, and all listed paper baselines. Each chart uses a zero-based 0–100% scale. Source notes explain differences in inputs, subsets and aggregation.\n\n'
    quips = {spec['dataset']: quip for spec, quip in zip(SPECS, quips)}
    for i, spec in enumerate(specs, 1):
        paper, summary, rows, chance = load_rows(spec)
        render(spec, rows, chance, i)
        table = document(spec, paper, summary, rows, chance)
        key, title = spec['key'], spec['title']
        caption = spec['subtitle']
        quip = quips[spec['dataset']]
        section += f'### {title}\n\n*{quip}*\n\n![{title}: descending vertical bars, paper results and CSIEE](assets/{key}-comparison.png)\n\n'
        section += f"{caption.rstrip('.')}. {spec['access']}\n\n"
        if key in {'perma', 'membench-msa'}:
            section += '**Spotlight:** ' + ('The 580-question Type-3 shuffled score is **93.93%**; this paper comparison uses the **423 single-domain** questions.' if key == 'perma' else '**100% on all 500 released msa questions**, including after shuffling. This is one selected subtask; the full MemBench screen has only **+2.60 pp** lift.') + ' [Why the ruler works →](docs/length-shortcuts.md)\n\n'
        section += f'<details>\n<summary><strong>Open the mark scheme — all {len(rows)} results and their sources</strong></summary>\n\n{table}\n\n</details>\n\n'
        section += f'[Source notes & exact scope](docs/{key}-comparison.md) · [PNG](assets/{key}-comparison.png) · [SVG](assets/{key}-comparison.svg) · [Back to results](#report-card)\n\n'
        gallery += f'## {title}\n\n![{title}](../assets/{key}-comparison.png)\n\n{caption}. [Full table and sources]({key}-comparison.md).\n\n'
        print(f"{title}: {spec['count']} paper + 3 CSIEE bars; descending; chance {chance:.2f}%")
    gallery += 'PERMA shows its single-domain Type-3 subset; MemBench shows only msa; PersonaMem-v1 is an earlier version of an existing family. GUI-World uses category-macro accuracy and MMBench-GUI uses the paper\'s adjusted score. APTBench shows the 614-question closed-ended Plan_EN subtask; ACPBench uses a seven-task macro-average. The full-screen report card keeps its original scope and question-weighted accuracy.\n'
    write(ROOT / 'docs/benchmark-comparisons.md', gallery)
    readme_path = ROOT / 'README.md'
    readme = readme_path.read_text(encoding='utf-8')
    start, end = '<!-- personamem:start -->', '<!-- personamem:end -->'
    before, rest = readme.split(start, 1)
    _, after = rest.split(end, 1)
    write(readme_path, before + start + '\n' + section + end + after)


if __name__ == '__main__':
    main()
