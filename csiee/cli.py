import argparse
import json
import urllib.error

from . import __version__
from .download import download_personamem, download_openbookqa
from .evaluate import evaluate, markdown, save_report
from .strategies import STRATEGIES, predict


def main(argv=None):
    parser = argparse.ArgumentParser(prog='csiee', description='No reading comprehension. Just exam folklore.')
    parser.add_argument('--version', action='version', version=__version__)
    sub = parser.add_subparsers(dest='command', required=True)
    guess = sub.add_parser('guess', help='guess from options alone')
    guess.add_argument('options', nargs='+')
    guess.add_argument('--strategy', choices=STRATEGIES, default='promax')
    run = sub.add_parser('eval', help='evaluate a local dataset')
    run.add_argument('path')
    run.add_argument('--format', choices=['jsonl', 'personamem-v2', 'openbookqa'], default='jsonl')
    run.add_argument('--seed', type=int, default=42)
    run.add_argument('--shuffles', type=int, default=10)
    run.add_argument('--strategies', nargs='+', choices=list(STRATEGIES) + ['random'])
    run.add_argument('--limit', type=int)
    run.add_argument('--output', default='results/local')
    fetch = sub.add_parser('download', help='download a pinned public benchmark')
    fetch.add_argument('dataset', choices=['personamem-v2', 'openbookqa'])
    fetch.add_argument('--output')
    args = parser.parse_args(argv)
    try:
        if args.command == 'guess':
            index = predict(args.strategy, args.options)
            print(json.dumps({'strategy': args.strategy, 'index': index, 'label': chr(65 + index), 'option': args.options[index]}, ensure_ascii=False))
        elif args.command == 'download':
            downloader = download_personamem if args.dataset == 'personamem-v2' else download_openbookqa
            suffix = 'csv' if args.dataset == 'personamem-v2' else 'jsonl'
            print(json.dumps(downloader(args.output or f'data/raw/{args.dataset}.{suffix}'), indent=2))
        else:
            report = evaluate(args.path, args.format, args.seed, args.shuffles, args.strategies, args.limit)
            save_report(report, args.output)
            print(markdown(report))
    except (ValueError, OSError, urllib.error.URLError) as error:
        parser.exit(2, f'csiee: {error}\n')
