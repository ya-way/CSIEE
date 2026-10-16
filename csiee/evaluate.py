"""Reproducible descriptive evaluation, with separate option-order controls."""

import hashlib
import json
import math
import platform
import random
from collections import Counter
from pathlib import Path

from . import __version__
from .data import load_questions, shuffled, stable_seed
from .strategies import STRATEGIES, DEFAULT_STRATEGIES, predict, classify_options


def wilson(correct, total):
    z = 1.959963984540054
    p = correct / total
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    radius = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return [max(0, center - radius), min(1, center + radius)]


def _prediction(strategy, question, seed):
    if strategy == 'random':
        return random.Random(stable_seed('random-baseline', seed, question.id)).randrange(len(question.options))
    return predict(strategy, question.options)


def evaluate(path, format='jsonl', seed=42, shuffles=10, strategies=None, limit=None):
    if shuffles < 1:
        raise ValueError('shuffles must be at least 1')
    if limit is not None and limit < 1:
        raise ValueError('limit must be positive')
    names = list(DEFAULT_STRATEGIES) if strategies is None else list(dict.fromkeys(strategies))
    if not names or any(name not in list(STRATEGIES) + ['random'] for name in names):
        raise ValueError('select at least one known strategy')
    path = Path(path)
    questions = load_questions(path, format, seed)
    total_loaded = len(questions)
    if limit is not None:
        questions = questions[:limit]
    n = len(questions)
    report = {
        'schema_version': 1, 'csiee_version': __version__, 'python': platform.python_version(),
        'dataset': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'format': format, 'seed': seed, 'shuffle_repeats': shuffles, 'n': n,
        'total_loaded': total_loaded, 'selection': 'all' if limit is None else f'first {limit}',
        'scope': 'option-only; no question, user history, retrieval, or LLM',
        'source_order': 'seeded reconstruction; NOT official evaluation order' if format == 'personamem-v2' else 'input order; labels mapped from source',
        'chance_accuracy': sum(1 / len(q.options) for q in questions) / n,
        'answer_histogram': dict(sorted(Counter(chr(65 + q.answer) for q in questions).items())),
        'option_count_histogram': dict(sorted(Counter(str(len(q.options)) for q in questions).items())),
        'option_type_histogram': dict(sorted(Counter(classify_options(q.options)[0] for q in questions).items())),
        'interval_note': 'Wilson 95% intervals assume independent questions; shared personas, scenarios, or task templates can violate this. Shuffle spread is sensitivity to order, not extra independent data.',
        'results': [], 'predictions': [],
    }
    manifest = path.with_suffix(path.suffix + '.source.json')
    if manifest.exists():
        provenance = json.loads(manifest.read_text(encoding='utf-8'))
        if provenance.get('sha256') != report['sha256']:
            raise ValueError('source manifest hash does not match dataset')
        report['source'] = provenance
        if 'source_order' in provenance:
            report['source_order'] = provenance['source_order']
        if provenance.get('adapter') == 'bixbench' and provenance.get('source_order_seed') != seed:
            raise ValueError('BixBench source-order seed differs; download to a new path with the requested seed')
    controls = [[shuffled(q, stable_seed(seed, repeat)) for q in questions] for repeat in range(shuffles)]
    for name in names:
        predictions = [_prediction(name, q, seed) for q in questions]
        correct = sum(p == q.answer for p, q in zip(predictions, questions))
        scores, agreement = [], []
        for control in controls:
            cp = [_prediction(name, q, seed) for q in control]
            scores.append(sum(p == q.answer for p, q in zip(cp, control)) / n)
            agreement.append(sum(original.options[p] == changed.options[c] for original, changed, p, c in zip(questions, control, predictions, cp)) / n)
        report['results'].append({
            'strategy': name, 'correct': correct, 'accuracy': correct / n,
            'wilson_95': wilson(correct, n), 'lift_over_chance_pp': 100 * (correct / n - report['chance_accuracy']),
            'shuffled_mean': sum(scores) / shuffles, 'shuffled_min': min(scores), 'shuffled_max': max(scores),
            'shuffled_scores': scores, 'choice_invariance': sum(agreement) / shuffles,
            'by_category': {category: {'n': sum(q.category == category for q in questions),
                                      'correct': sum(p == q.answer and q.category == category for p, q in zip(predictions, questions))}
                            for category in sorted({q.category for q in questions})},
            'by_option_count': {str(m): {'n': sum(len(q.options) == m for q in questions),
                                        'correct': sum(p == q.answer and len(q.options) == m for p, q in zip(predictions, questions))}
                                for m in sorted({len(q.options) for q in questions})},
        })
        report['predictions'].extend({'id': q.id, 'strategy': name, 'predicted': p, 'answer': q.answer, 'correct': p == q.answer} for q, p in zip(questions, predictions))
    return report


def markdown(report):
    lines = [
        '# CSIEE evaluation', '',
        f"Dataset: `{report['dataset']}` · n={report['n']} · seed={report['seed']} · permutations={report['shuffle_repeats']}",
        f"Expected uniform random accuracy: **{report['chance_accuracy']:.2%}**. Scope: {report['scope']}.", '',
        '| Strategy | Accuracy | Wilson 95% | Lift (pp) | Shuffled mean | Shuffled range | Same choice |',
        '| :-- | --: | :-- | --: | --: | :-- | --: |',
    ]
    for row in report['results']:
        low, high = row['wilson_95']
        lines.append(f"| {row['strategy']} | {row['accuracy']:.2%} | {low:.2%}–{high:.2%} | {row['lift_over_chance_pp']:+.2f} | {row['shuffled_mean']:.2%} | {row['shuffled_min']:.2%}–{row['shuffled_max']:.2%} | {row['choice_invariance']:.2%} |")
    lines += ['', f"Order: {report['source_order']}.", '', report['interval_note'], '',
              '**Interpretation:** this audits answer-option artifacts. It does not measure end-to-end agent capability or prove that a benchmark is invalid.', '',
              f"SHA-256: `{report['sha256']}`", f"CSIEE {report['csiee_version']} / Python {report['python']}", '']
    if 'source' in report:
        source = report['source']
        lines += [f"Source: [{source['dataset']}]({source['url']})", f"Revision: `{source['revision']}` · License: {source['license']}", '']
        if 'normalization' in source:
            audit = source['normalization']
            lines += [f"Released MCQ candidates: {audit['candidate_count']}; included: {audit['included_count']}; excluded: {audit['excluded_count']}. Every excluded ID/reason is in summary.json.", '']
    return '\n'.join(lines)


def save_report(report, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    summary = {k: v for k, v in report.items() if k != 'predictions'}
    (output / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    (output / 'report.md').write_text(markdown(report), encoding='utf-8')
    (output / 'predictions.jsonl').write_text(''.join(json.dumps(p, ensure_ascii=False) + '\n' for p in report['predictions']), encoding='utf-8')
