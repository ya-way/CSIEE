import argparse
import json
import urllib.error

from . import __version__
from .download import download_personamem, download_openbookqa
from .benchmarks import REGISTRY, FEATURED, EXTRA, download_benchmark
from .evaluate import evaluate, markdown, save_report
from .strategies import STRATEGIES, predict


def main(argv=None):
    parser = argparse.ArgumentParser(prog='csiee', description='No reading comprehension. Just exam folklore.')
    parser.add_argument('--version', action='version', version=__version__)
    sub = parser.add_subparsers(dest='command', required=True)
    guess = sub.add_parser('guess', help='guess from options alone')
    guess.add_argument('options', nargs='+')
    guess.add_argument('--strategy', choices=STRATEGIES, default='xiaogang')
    run = sub.add_parser('eval', help='evaluate a local dataset')
    run.add_argument('path')
    run.add_argument('--format', choices=['jsonl', 'personamem-v2', 'openbookqa'], default='jsonl')
    run.add_argument('--seed', type=int, default=42)
    run.add_argument('--shuffles', type=int, default=10)
    run.add_argument('--strategies', nargs='+', choices=list(STRATEGIES) + ['random'])
    run.add_argument('--limit', type=int)
    run.add_argument('--output', default='results/local')
    fetch = sub.add_parser('download', help='download a pinned public benchmark')
    fetch.add_argument('dataset', choices=['personamem-v2', 'openbookqa'] + list(REGISTRY))
    fetch.add_argument('--output')
    fetch.add_argument('--seed', type=int, default=42, help='source-order seed for answer-first native MCQ data')
    suite = sub.add_parser('suite', help='download and evaluate the ten featured benchmark components')
    suite.add_argument('--all', action='store_true', help='also include BixBench, Backtrader and the public labeled FDABench subset')
    suite.add_argument('--seed', type=int, default=42)
    suite.add_argument('--shuffles', type=int, default=10)
    suite.add_argument('--output', default='results/local/suite')
    args = parser.parse_args(argv)
    try:
        if args.command == 'guess':
            index = predict(args.strategy, args.options)
            print(json.dumps({'strategy': args.strategy, 'index': index, 'label': chr(65 + index), 'option': args.options[index]}, ensure_ascii=False))
        elif args.command == 'download':
            suffix = 'csv' if args.dataset == 'personamem-v2' else 'jsonl'
            output = args.output or f'data/raw/{args.dataset}.{suffix}'
            if args.dataset in REGISTRY:
                result = download_benchmark(args.dataset, output, args.seed)
            else:
                downloader = download_personamem if args.dataset == 'personamem-v2' else download_openbookqa
                result = downloader(output)
            print(json.dumps(result, indent=2))
        elif args.command == 'suite':
            from pathlib import Path
            for name in FEATURED + (EXTRA if args.all else []):
                path = Path('data/raw') / (name + ('.csv' if name == 'personamem-v2' else '.jsonl'))
                if not path.exists():
                    if name == 'personamem-v2':
                        download_personamem(path)
                    else:
                        download_benchmark(name, path, args.seed)
                if not path.with_suffix(path.suffix + '.source.json').exists():
                    raise ValueError(f'{path}: source manifest required for suite')
                report = evaluate(path, 'personamem-v2' if name == 'personamem-v2' else 'jsonl', args.seed, args.shuffles)
                save_report(report, Path(args.output) / name)
                print(markdown(report))
        else:
            report = evaluate(args.path, args.format, args.seed, args.shuffles, args.strategies, args.limit)
            save_report(report, args.output)
            print(markdown(report))
    except (ValueError, OSError, urllib.error.URLError) as error:
        parser.exit(2, f'csiee: {error}\n')
