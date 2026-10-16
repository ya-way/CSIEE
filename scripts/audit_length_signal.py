"""Describe the two spotlight signals without changing the prediction rules."""
import argparse
import ast
import hashlib
import json
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def audit(data_dir):
    output = {'scope': 'Post-hoc structural diagnostics, not new predictors or agent evaluations', 'datasets': {}}
    for key in ['perma', 'membench-msa']:
        path = data_dir / f'{key}.jsonl'
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        summary = json.loads((ROOT/f'results/classmates/{key}/summary.json').read_text(encoding='utf-8'))
        if digest != summary['sha256']:
            raise ValueError('Normalized data differs from the published snapshot: '+key)
        rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
        gold_lengths, wrong_lengths, ratios = [], [], []
        unique = tied = 0
        for row in rows:
            lengths = [len(x.strip()) for x in row['options']]
            gold = lengths[row['answer']]
            other = [x for i,x in enumerate(lengths) if i != row['answer']]
            unique += gold > max(other)
            tied += gold == max(lengths) and lengths.count(gold) > 1
            gold_lengths.append(gold); wrong_lengths.extend(other)
            ratios.append(gold/statistics.mean(other))
        result = dict(n=len(rows), normalized_sha256=digest, unique_longest_gold=unique,
                      tied_longest_gold=tied, mean_gold_characters=statistics.mean(gold_lengths),
                      mean_distractor_characters=statistics.mean(wrong_lengths),
                      median_gold_to_mean_distractor_length=statistics.median(ratios))
        if key == 'membench-msa':
            patterns = Counter(); omission = list_count = nonlist_count = joined_unique = 0
            for row in rows:
                values = [ast.literal_eval(x) if x.startswith('[') else x for x in row['options']]
                gold = values[row['answer']]
                if not isinstance(gold, list):
                    raise ValueError('Expected list-valued gold in msa')
                counts = [len(x) if isinstance(x,list) else -1 for x in values]
                patterns[(counts[row['answer']], tuple(sorted(v for i,v in enumerate(counts) if i != row['answer'])))]+=1
                lengths = [len(', '.join(x)) if isinstance(x,list) else len(x) for x in values]
                joined_unique += lengths[row['answer']] > max(v for i,v in enumerate(lengths) if i != row['answer'])
                for i,value in enumerate(values):
                    if i == row['answer']: continue
                    if isinstance(value,list):
                        list_count += 1
                        omission += len(value)==len(gold)-1 and set(value).issubset(set(gold))
                    else: nonlist_count += 1
            result.update(list_distractors=list_count, list_distractors_omitting_one_gold_item=omission,
                          nonlist_distractors=nonlist_count, unique_longest_gold_with_comma_joined_lists=joined_unique,
                          item_count_patterns=[dict(gold_items=k[0],distractor_items=k[1],n=v) for k,v in sorted(patterns.items())],
                          serialization_note='-1 denotes a non-list answer. Comma joining is a diagnostic format check, not a changed published run.')
        output['datasets'][key] = result
    return output

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path,default=ROOT/'data/raw')
    parser.add_argument('--output',type=Path,default=ROOT/'results/local/length-signals.json')
    args=parser.parse_args(); result=audit(args.data_dir)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
