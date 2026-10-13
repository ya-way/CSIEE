"""Only options go in. A zero-based choice index comes out. No labels, no LLMs."""

import re
import math
from collections import Counter
from decimal import Decimal
from statistics import median


def lite(options):
    return min(2, len(options) - 1)  # When in doubt, C. Two choices? B.


def _pick(indices, options):
    indices = list(indices)
    return lite(options) if lite(options) in indices else min(indices)


def longest(options):
    lengths = [len(o.strip()) for o in options]
    return _pick([i for i, n in enumerate(lengths) if n == max(lengths)], options)


def shortest(options):
    lengths = [len(o.strip()) for o in options]
    return _pick([i for i, n in enumerate(lengths) if n == min(lengths)], options)


def pro(options):
    lengths = sorted(len(o.strip()) for o in options)
    if lengths[-1] > 1.5 * lengths[-2]: return longest(options)
    if lengths[1] > 1.5 * lengths[0]: return shortest(options)
    return lite(options)


_NUMBER = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?%?")


def _numeric_vote(options):
    texts = [o.strip() for o in options]
    if len(texts) < 3 or not all(_NUMBER.fullmatch(t) for t in texts):
        return None
    numbers = [Decimal(t.rstrip('%')) / (100 if t.endswith('%') else 1) for t in texts]
    if len(set(numbers)) != len(numbers):
        return None  # No invented ordering for equal values.
    return sorted(range(len(numbers)), key=numbers.__getitem__, reverse=True)[2]


def numeric(options):
    vote = _numeric_vote(options)
    return lite(options) if vote is None else vote


def _cautious_vote(options):
    counts = [len(re.findall(r"\b(?:always|never|only|all|must|every|impossible|certainly)\b", o, re.I)) for o in options]
    if len(set(counts)) == 1:
        return None
    return _pick([i for i, count in enumerate(counts) if count == min(counts)], options)


def cautious(options):
    vote = _cautious_vote(options)
    return lite(options) if vote is None else vote


def promax(options):
    votes = Counter(v for v in [pro(options), _numeric_vote(options), _cautious_vote(options)] if v is not None)
    return _pick([i for i, count in votes.items() if count == max(votes.values())], options)


def xiaoming(options):
    return longest(options)


def xiaohong(options):
    return lite(options)


_SCALAR = re.compile(r'([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*([a-zA-Z%°]*)')


def classify_options(options):
    """Infer answer type without reading the question, metadata, or labels."""
    matches = [_SCALAR.fullmatch(option.strip()) for option in options]
    if all(matches):
        units = [match[2].lower() for match in matches]
        if len(set(units)) == 1 or set(units) <= {'', '%'}:
            values = [float(match[1]) / (100 if unit == '%' else 1) for match, unit in zip(matches, units)]
            if all(math.isfinite(value) for value in values):
                scale = max(abs(value) for value in values) or 1
                return 'numeric', [value / scale for value in values]
    return 'length', [len(option.strip()) for option in options]


def xiaogang(options):
    _, values = classify_options(options)
    distances = [abs(value - median(values)) for value in values]
    return _pick([i for i, distance in enumerate(distances) if distance == max(distances)], options)


STRATEGIES = {f.__name__: f for f in (xiaoming, xiaohong, xiaogang, lite, pro, promax, longest, shortest, numeric, cautious)}
DEFAULT_STRATEGIES = ['xiaoming', 'xiaohong', 'xiaogang', 'random']


def predict(name, options):
    if not isinstance(options, (list, tuple)) or not 2 <= len(options) <= 26:
        raise ValueError('options must contain 2 to 26 strings')
    if any(not isinstance(o, str) or not o.strip() for o in options):
        raise ValueError('every option must be a non-empty string')
    if name not in STRATEGIES:
        raise ValueError('unknown strategy: ' + name)
    return STRATEGIES[name](options)
