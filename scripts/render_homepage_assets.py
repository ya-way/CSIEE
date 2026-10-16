"""Build the README's original SVG stationery using the Python standard library."""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
INK, PAPER, RED, TEAL, RULE = '#252927', '#F7F3E9', '#AD493B', '#356C6B', '#D9D8CD'


def text(x, y, value, size=16, color=INK, font='sans-serif', weight='400', extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{font}" font-size="{size}" font-weight="{weight}" {extra}>{escape(value)}</text>'


def save(name, width, height, title, parts):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>'
    svg += ''.join(parts) + '</svg>\n'
    (OUT / name).write_bytes(svg.encode('utf-8'))


def ticket(mobile=False):
    families = ['personamem-v2', 'agentsense', 'acpbench', 'aptbench', 'agenthop', 'perma', 'membench-msa', 'personamem-v1', 'gui-world', 'mmbench-gui-l1']
    n = sum(json.loads((ROOT/f'results/classmates/{key}/summary.json').read_text())['n'] for key in families)
    w, h = (420, 282) if mobile else (1200, 190)
    parts = [f'<rect width="{w}" height="{h}" rx="4" fill="{INK}"/>']
    parts += [text(28, 34, 'CSIEE / EXAMINATION ADMISSION TICKET', 12 if mobile else 16, PAPER, 'monospace'),
              f'<path d="M28 53H{w-28}" stroke="#59605A" stroke-dasharray="4 5"/>']
    if mobile:
        stats = [('0', 'PARAMETERS', 28, 108), ('0', 'API CALLS', 230, 108),
                 ('10', 'BENCHMARK COMPONENTS', 28, 200), (f'{n:,}', 'QUESTIONS SCREENED', 230, 200)]
    else:
        stats = [('0', 'PARAMETERS', 32, 121), ('0', 'API CALLS', 310, 121),
                 ('10', 'BENCHMARK COMPONENTS', 588, 121), (f'{n:,}', 'QUESTIONS SCREENED', 866, 121)]
    for value, label, x, y in stats:
        parts += [text(x, y, value, 44, '#E3A58A' if value=='0' else PAPER, 'Georgia, serif'),
                  text(x, y+28, label, 12 if mobile else 15, '#C6CABE', 'monospace')]
    if mobile:
        parts += [text(28, 263, 'ALLOWED MATERIALS: THE ANSWER CHOICES.', 11, '#C6CABE', 'monospace')]
    save('exam-ticket-mobile.svg' if mobile else 'exam-ticket.svg', w, h,
         f'Zero parameters. Zero API calls. Ten featured benchmark components. {n:,} questions screened.', parts)


def card(index, x, y):
    names = ['Xiaoming', 'Xiaohong', 'Xiaogang']
    colors = [TEAL, RED, INK]
    roles = ['THE MEASURER', 'THE BELIEVER', 'THE ANALYST*']
    strategies = ['Pick the longest.', 'Pick C. Commit fully.', 'Pick the odd one out.']
    notes = [('Research budget: one ruler.', 'More characters. More confidence.'),
             ('Two choices? B will do.', 'A position. A principle. A lifestyle.'),
             ('Numbers or lengths; farthest', 'from the median. *Experimental.')]
    c = colors[index]
    p = [f'<g transform="translate({x} {y})"><rect x="1" y="1" width="378" height="416" rx="4" fill="{PAPER}" stroke="{RULE}"/>',
         f'<path d="M1 1H379V10H1Z" fill="{c}"/>',
         text(25, 42, f'CANDIDATE / 00{index+1}', 13, c, 'monospace'),
         text(25, 92, names[index], 38, INK, 'Georgia, serif'),
         text(25, 119, roles[index], 12, c, 'monospace', extra='letter-spacing="2"')]
    if index == 0:
        p += [f'<g transform="translate(29 166) rotate(-7 156 36)"><rect width="316" height="66" fill="#E3D8BD" stroke="{INK}" stroke-width="2"/>']
        for i in range(26):
            xx = 8 + i*12
            p += [f'<path d="M{xx} 0v{26 if i%5==0 else 13}" stroke="{INK}" stroke-width="1.5"/>']
        for i in range(6):
            p += [text(8+i*60, 53, str(i*10), 14, INK, 'monospace', extra='text-anchor="middle"')]
        p += ['</g>']
    elif index == 1:
        p += [f'<g transform="rotate(-8 190 208)"><rect x="133" y="147" width="114" height="114" rx="6" fill="none" stroke="{RED}" stroke-width="4"/>',
              text(190, 235, 'C', 90, RED, 'Georgia, serif', '700', 'text-anchor="middle"'), '</g>']
    else:
        for i, height in enumerate([32, 38, 43, 97]):
            p += [f'<rect x="{62+i*66}" y="{253-height}" width="37" height="{height}" fill="{RED if i==3 else TEAL}"/>']
        p += [f'<path d="M43 216H335" stroke="{INK}" stroke-dasharray="5 5"/>',
              text(325, 147, '?', 30, RED, 'Georgia, serif')]
    p += [f'<path d="M25 282H355" stroke="{RULE}"/>',
          text(25, 316, strategies[index], 21, c, 'Georgia, serif', '700'),
          text(25, 351, notes[index][0], 15), text(25, 376, notes[index][1], 15), '</g>']
    return p


def roster(mobile=False):
    parts = []
    for i in range(3):
        parts += card(i, 0 if mobile else i*410, i*442 if mobile else 0)
    save('class-roster-mobile.svg' if mobile else 'class-roster.svg',
         380 if mobile else 1200, 1302 if mobile else 418,
         'Xiaoming picks the longest. Xiaohong picks C, or B with two options. Xiaogang picks the number or length farthest from the median.', parts)


def main():
    for mobile in [False, True]:
        ticket(mobile)
        roster(mobile)
    save('end-of-paper.svg', 1200, 146, 'End of paper. No questions were understood.', [
        f'<rect width="1200" height="146" fill="{PAPER}"/>',
        f'<path d="M35 37H465M735 37H1165" stroke="{RULE}"/>',
        text(600, 43, 'END OF PAPER', 17, RED, 'monospace', '700', 'text-anchor="middle" letter-spacing="4"'),
        text(600, 93, 'No questions were understood.', 34, INK, 'Georgia, serif', extra='text-anchor="middle"'),
        text(600, 124, 'PLEASE HAND IN YOUR RULER.', 12, TEAL, 'monospace', extra='text-anchor="middle" letter-spacing="2"')])
    for filename, left, right in [('python-badge.svg','PYTHON','3.9+'), ('license-badge.svg','LICENSE','MIT')]:
        save(filename, 124, 24, f'{left}: {right}', [
            f'<rect width="124" height="24" rx="3" fill="{INK}"/><path d="M73 0h48q3 0 3 3v18q0 3-3 3H73Z" fill="{TEAL}"/>',
            text(36, 16, left, 10, PAPER, 'monospace', extra='text-anchor="middle"'),
            text(98, 16, right, 11, PAPER, 'monospace', extra='text-anchor="middle"')])
    print('Rendered seven original SVG assets, including mobile ticket and roster.')


if __name__ == '__main__':
    main()
