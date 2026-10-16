"""Regenerate README score tables and the complete report index from saved counts."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from csiee.benchmarks import FEATURED, EXTRA
from homepage_order import ORDER

LABELS = ['PersonaMem-v2', 'AgentSense', 'ACPBench', 'APTBench', 'AgentHop',
          'PERMA · Type 3', 'MemBench · msa subtask', 'PersonaMem-v1 · 128k',
          'GUI-World · MCQs', 'MMBench-GUI · L1', 'BixBench', 'Backtrader-Bench', 'FDABench']
PARTS = ['text memory', 'information reasoning', 'seven planning tasks', 'seven English MCQ tasks',
         'research MCQs', 'single- and multi-domain', 'multi-session assistant only',
         'earlier PersonaMem version', 'six GUI categories', 'content understanding only']

def main():
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    cards = ['| Benchmark / evaluated component | Questions | Chance | Xiaoming | Xiaohong | Xiaogang |',
             '| :-- | --: | --: | --: | --: | --: |']
    shuffles = ['| Benchmark | Xiaoming | Xiaohong | Xiaogang | Seeded random |', '| :-- | --: | --: | --: | --: |']
    full = ['| Benchmark | Questions | Chance | Xiaoming | Xiaohong | Xiaogang | Seeded random |',
            '| :-- | --: | --: | --: | --: | --: | --: |']
    total = featured_n = 0
    records = {}
    for name in ORDER + EXTRA:
        i = (FEATURED + EXTRA).index(name)
        r = json.loads((ROOT / f'results/classmates/{name}/summary.json').read_text(encoding='utf-8'))
        assert (r['seed'], r['shuffle_repeats']) == (42, 10)
        assert [x['strategy'] for x in r['results']] == ['xiaoming', 'xiaohong', 'xiaogang', 'random']
        records[name] = r
        values = [f"{x['accuracy']:.2%}" for x in r['results']]
        shuffled = [f"{x['shuffled_mean']:.2%}" for x in r['results']]
        total += r['n']
        if name in FEATURED:
            featured_n += r['n']
            cards.append(f"| [{LABELS[i]}](results/classmates/{name}/report.md) · {PARTS[i]} | {r['n']:,} | {r['chance_accuracy']:.2%} | " + ' | '.join(values[:3]) + ' |')
            shuffles.append(f"| {LABELS[i]} | " + ' | '.join(shuffled) + ' |')
        full.append(f"| [{LABELS[i]}]({name}/report.md) | {r['n']:,} | {r['chance_accuracy']:.2%} | " + ' | '.join(shuffled) + ' |')
    lifts = ['| Added component | Best unchanged rule | Shuffled accuracy | Chance | Lift over chance |',
             '| :-- | :-- | --: | --: | --: |']
    ref = records['personamem-v2']
    threshold = max(x['shuffled_mean'] for x in ref['results'][:3]) - ref['chance_accuracy']
    for name in FEATURED[5:]:
        r = records[name]; best = max(r['results'][:3], key=lambda x: x['shuffled_mean'])
        lift = best['shuffled_mean'] - r['chance_accuracy']
        assert lift > threshold
        lifts.append(f"| [{LABELS[FEATURED.index(name)]}](results/classmates/{name}/report.md) | {best['strategy'].capitalize()} | {best['shuffled_mean']:.2%} | {r['chance_accuracy']:.2%} | **+{100*lift:.2f} pp** |")
    for block, rows in [('report-card', cards), ('shuffle-card', shuffles), ('added-signals', lifts)]:
        pattern = r'(<!-- ' + block + r':start -->)\n.*?(<!-- ' + block + r':end -->)'
        assert len(re.findall(pattern, readme, re.S)) == 1
        readme = re.sub(pattern, lambda m: m[1]+'\n'+'\n'.join(rows)+'\n'+m[2], readme, flags=re.S)
    (ROOT/'README.md').write_text(readme, encoding='utf-8')
    index = '# The complete report card\n\nSeed 42 · ten label-preserving permutations · all included questions. This table uses **shuffled mean accuracy**. The front page uses input-order accuracy.\n\n'+'\n'.join(full)
    index += f'\n\nThe ten featured components contain {featured_n:,} questions across nine families; PersonaMem-v1 and v2 share a family. All thirteen full reports contain {total:,} included questions. MemBench msa is a selected subtask. Counts are not independent sample sizes, and scores are never pooled.\n\n'
    index += 'Every report includes provenance, exclusions, source hashes and prediction indices. Additional exploratory pilots, including weak outcomes and the full MemBench screen, are recorded separately in the [screening ledger](../../docs/screening.md). Pilot and subset counts can overlap and must not be added to these totals.\n'
    (ROOT/'results/classmates/README.md').write_text(index, encoding='utf-8')
    print(f'Rendered 10 featured / 13 full reports; {featured_n:,} featured questions.')

if __name__ == '__main__':
    main()
