"""Render the cited PersonaMem comparison. Optional dependency: matplotlib==3.9.4."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
PAPER = json.loads((ROOT / 'data/paper/personamem-v2-mcq.json').read_text(encoding='utf-8'))
LOCAL = json.loads((ROOT / 'results/classmates/personamem-v2/summary.json').read_text(encoding='utf-8'))
assert LOCAL['n'] == 5000 and LOCAL['seed'] == 42 and LOCAL['shuffle_repeats'] == 10
assert len(PAPER['rows']) == 12 and {r['figure'] for r in PAPER['rows']} == {4, 6}
students = []
for strategy, method in [('xiaoming', 'Xiaoming · longest'), ('xiaohong', 'Xiaohong · C'), ('xiaogang', 'Xiaogang · outlier')]:
    result = next(r for r in LOCAL['results'] if r['strategy'] == strategy)
    assert result['accuracy'] == result['correct'] / LOCAL['n']
    students.append(dict(method=method, group='csiee', context='Options only', accuracy=100 * result['accuracy'], shuffled=100 * result['shuffled_mean']))

BG, INK, MUTED, LINE = '#F7F3E9', '#252927', '#6C726C', '#D9D8CD'
TEAL, RED = '#356C6B', '#AD493B'
selected_names = ['Qwen3-4B · Agentic Memory', 'Qwen3-4B · GRPO', 'GPT-5-mini', 'GPT-5-Chat']
selected = [next(row for row in PAPER['rows'] if row['method'] == name) for name in selected_names]
matplotlib.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'svg.hashsalt': 'csiee-personamem-v1', 'axes.unicode_minus': False})
fig = plt.figure(figsize=(12.4, 8), facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set(xlim=(0, 1240), ylim=(800, 0))
ax.axis('off')
def text(x, y, value, size=12, color=INK, weight='normal', **kwargs):
    return ax.text(x, y, value, fontsize=size, color=color, weight=weight, va='center', **kwargs)
def rule(y, color=LINE, width=.7):
    ax.plot([48, 1192], [y, y], color=color, lw=width)

text(48, 36, 'CSIEE / BENCHMARK NOTES', 10, RED, 'bold')
text(48, 85, 'PersonaMem-v2, with a ruler.', 29, family='DejaVu Serif')
text(48, 128, 'MCQ accuracy · Selected paper results and three option-only baselines', 12, MUTED)
rule(156, INK, 1)

left, right = 435, 1095
def xpos(value):
    return left + (right - left) * value / 60
for tick in range(0, 61, 10):
    text(xpos(tick), 647, f'{tick}%', 10, MUTED, ha='center')
    ax.plot([xpos(tick), xpos(tick)], [206, 624], color=LINE, lw=.55, zorder=0)
ax.plot([xpos(25), xpos(25)], [206, 624], color=MUTED, lw=1, ls=(0, (3, 4)), zorder=4)
text(xpos(25), 185, '25% chance', 10, MUTED, ha='center')

groups = [('PAPER / REPORTED', selected, 185), ('CSIEE / MEASURED', students, 449)]
for title, members, header_y in groups:
    local = title.startswith('CSIEE')
    text(48, header_y, title, 10, RED if local else TEAL, 'bold')
    for i, row in enumerate(members):
        y = header_y + 41 + 56 * i
        color = RED if local else TEAL
        text(48, y - 7, row['method'], 12.5, INK, 'bold' if local else 'normal')
        text(48, y + 13, row['context'], 9.5, MUTED)
        ax.barh(y, xpos(row['accuracy']) - left, height=26, left=left, color=color, zorder=2)
        score = f"{row['accuracy']:.2f}%" if local else f"{row['accuracy']:.1f}%"
        text(xpos(row['accuracy']) + 12, y, score, 12.5, color, 'bold', family='DejaVu Sans Mono')

rule(681, INK, 1)
text(48, 708, 'Different inputs and evaluation pipelines; similar accuracy does not imply equivalent capability.', 10.5, INK)
text(48, 737, 'Paper: Jiang et al., arXiv:2512.06688v1, Figs. 4 & 6. *2k memory built from 32k history.', 10, MUTED)
text(48, 763, 'CSIEE: 5,000 text MCQs, seed 42, reconstructed option order. Full results and sources in the README.', 10, MUTED)

out = ROOT / 'assets'
fig.savefig(out / 'personamem-comparison.png', dpi=180, facecolor=BG)
fig.savefig(out / 'personamem-comparison.svg', facecolor=BG, metadata={'Date': None, 'Creator': 'CSIEE / Matplotlib'})
plt.close(fig)

table = ['| Method | History / memory | MCQ accuracy | Shuffled mean | Source |', '| :-- | :-- | --: | --: | :-- |']
for row in PAPER['rows']:
    table.append(f"| {row['method']} | {row['context']} | {row['accuracy']:.1f}% | — | Paper Fig. {row['figure']} |")
for row in students:
    table.append(f"| **{row['method']}** | **Options only** | **{row['accuracy']:.2f}%** | {row['shuffled']:.2f}% | CSIEE, n=5,000 |")
table.append('| Uniform chance | Options only | 25.00% | 25.00% (expected) | Analytical |')
table = '\n'.join(table)
compact_lines = [line for line in table.splitlines() if line.split('|')[1].strip() in selected_names or any(label in line for label in ['Method |', ':--', '**Xiao', 'Uniform chance'])]
assert len(compact_lines) == 10  # Two header lines, four paper rows, three students, chance.
compact_table = '\n'.join(compact_lines)

notes = r'''Paper rows are transcribed from the printed **MCQ** labels in [Figure 4](https://arxiv.org/html/2512.06688v1#S4.F4) and [Figure 6](https://arxiv.org/html/2512.06688v1#S4.F6) of Jiang et al., *PersonaMem-v2*, [arXiv:2512.06688v1](https://arxiv.org/abs/2512.06688v1). They are cited results, not our reruns. All six Qwen variants are retained, including both training ablations. OE-only means trained only on open-ended examples; the reported score here is still MCQ accuracy.

\* Agentic Memory constructs up to 2k tokens of memory from 32k history; “2k” is not the total history processed. The other paper rows use 32k conversation histories plus the question and choices. CSIEE sees only the choices and uses all 5,000 text MCQs at the pinned dataset revision, with seed 42 and a reconstructed option order. The local column reports accuracy on that order; the control averages ten label-preserving permutations. Paper permutation controls are unavailable (—), not zero.

The table places both sources on the same accuracy scale, with their different inputs and protocols visible. It does not establish statistical superiority, equivalent personalization ability, or a matched end-to-end comparison. Paper values retain their published one-decimal precision; local values retain two decimals. A 0.02-point difference between 45.62% and 45.6% is not a meaningful win claim, especially with the paper's rounding and different evaluation pipeline.
'''
extra = ['| Frontier model | Paper MCQ · 32k | Paper MCQ · 128k |', '| :-- | --: | --: |']
for row in PAPER['rows']:
    if 'mcq_128k' in row:
        extra.append(f"| {row['method']} | {row['accuracy']:.1f}% | {row['mcq_128k']:.1f}% |")
doc = '# PersonaMem-v2: paper results meet the classmates\n\n![Combined paper and CSIEE MCQ comparison](../assets/personamem-comparison.png)\n\nThe compact figure retains four paper references: the agentic-memory model, mixed-reward GRPO, the strongest 32k frontier model (GPT-5-mini), and GPT-5-Chat. Base/SFT models, training ablations, and other frontier variants remain in the complete table below. This selection simplifies the presentation; it does not change any measured result.\n\n## One table, with provenance\n\n' + table + '\n\n' + notes + '\n## The paper\'s 128k frontier setting\n\n' + '\n'.join(extra) + '''

The main figure consistently selects the 32k frontier setting rather than choosing each model's best or worst context length. The paper's 128k values are retained here for completeness. Open-ended evaluation scores are excluded throughout.

## Data and rendering

- [Paper-value transcription](../data/paper/personamem-v2-mcq.json), including exact paper version and figure numbers.
- [Local summary](../results/classmates/personamem-v2/summary.json) and [prediction records](../results/classmates/personamem-v2/predictions.jsonl).
- [PNG](../assets/personamem-comparison.png) and [vector SVG](../assets/personamem-comparison.svg).
- [Rendering script](../scripts/render_personamem.py); it generates the image and both Markdown tables from the same records.

```bash
python -m pip install matplotlib==3.9.4
python scripts/render_personamem.py
```

Matplotlib is an optional figure-building dependency. The CSIEE evaluator still has no runtime dependencies. The comparison artwork is an original rendering of cited numerical results; it does not reuse the paper's images.
'''
(ROOT / 'docs/personamem-comparison.md').write_bytes(doc.encode('utf-8'))
readme_path = ROOT / 'README.md'
readme = readme_path.read_text(encoding='utf-8')
start, end = '<!-- personamem:start -->', '<!-- personamem:end -->'
section = '''## PersonaMem-v2: a ruler enters the chat

![PersonaMem-v2: paper-reported MCQ results and the three CSIEE classmates, with input context and accuracy on a shared scale](assets/personamem-comparison.png)

**Xiaoming: 45.62%. GPT-5-Chat, as reported in the paper: 45.6%.** One brought a ruler; the other received 32k of conversation history. These are different evaluation pipelines, not a claim of equivalent capability.

<details>
<summary><strong>The same table, in text — paper values and our measurements</strong></summary>

''' + compact_table + '''

Paper: [Jiang et al., Figs. 4 & 6](https://arxiv.org/html/2512.06688v1#S4); MCQ only, with 32k frontier results. *Agentic Memory builds a 2k memory from 32k history. CSIEE uses seed 42 and reconstructed option order on all 5,000 text MCQs. Published model scores were not rerun. Paper values retain one decimal; local scores retain two. “—” means no paper permutation control is available.

</details>

[Full comparison, 128k results & source notes](docs/personamem-comparison.md) · [Vector figure](assets/personamem-comparison.svg)

Four paper references are shown for clarity; base/SFT models, training ablations and other frontier variants remain in the full comparison.
'''
if start in readme:
    before, rest = readme.split(start, 1)
    _, after = rest.split(end, 1)
    readme = before + start + '\n' + section + end + after
else:
    readme = readme.replace('## Report card\n', start + '\n' + section + end + '\n\n## Report card\n', 1)
readme_path.write_bytes(readme.encode('utf-8'))
print('Rendered PNG + SVG; generated one combined table in the README and source notes.')
