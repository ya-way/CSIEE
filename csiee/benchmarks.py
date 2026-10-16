"""Pinned native MCQ components of agent benchmarks, with auditable exclusions."""

import ast
import csv
import gzip
import hashlib
import json
import re
import urllib.request
from urllib.parse import quote
from pathlib import Path

from .data import Question, shuffled

FEATURED = ['personamem-v2', 'agentsense', 'acpbench', 'aptbench', 'agenthop',
            'perma', 'membench-msa', 'personamem-v1', 'gui-world', 'mmbench-gui-l1']
EXTRA = ['bixbench', 'backtrader', 'fdabench']


def github(repo, revision, paths):
    return [{'path': path, 'url': f'https://raw.githubusercontent.com/{repo}/{revision}/{path}'} for path in paths]


def huggingface(repo, revision, path):
    return [{'path': path, 'url': f'https://huggingface.co/datasets/{repo}/resolve/{revision}/{quote(path, safe="/")}'}]


APT_TASKS = ['agentic_math/action_cal', 'agentic_math/planning_single', 'deepresearch/plan_en',
             'env_setup/error', 'env_setup/plan', 'issue_fix/locate', 'issue_fix/plan']
REGISTRY = {
    'fdabench': {
        'dataset': 'FDABench-Full (public labeled single-choice subset)', 'url': 'https://huggingface.co/datasets/FDAbench2026/FDAbench-Full',
        'revision': '0e05e5ec2c95fbe462bed0cba1882f99989ab34e', 'license': 'MIT (upstream dataset card)',
        'split': 'single/data.jsonl records with released correct_answer; unlabeled records explicitly excluded',
        'sources': huggingface('FDAbench2026/FDAbench-Full', '0e05e5ec2c95fbe462bed0cba1882f99989ab34e', 'single/data.jsonl'),
    },
    'agentsense': {
        'dataset': 'AgentSense', 'url': 'https://github.com/ljcleo/agent_sense', 'revision': '21b6ef909cabcd4a72cded7580869e1e28c0e628',
        'license': 'MIT (upstream repository)', 'split': 'all released information-reasoning MCQs; no simulated dialogue',
        'sources': github('ljcleo/agent_sense', '21b6ef909cabcd4a72cded7580869e1e28c0e628', ['SENSE/data/final_data.jsonl']),
    },
    'agenthop': {
        'dataset': 'AgentHop', 'url': 'https://huggingface.co/datasets/agenthop/agenthop', 'revision': '599b0659343a7a3cc852a60c2e527150121cccdf',
        'license': 'CC-BY-4.0', 'split': 'full 1011 MCQs; no paper/tool access',
        'sources': huggingface('agenthop/agenthop', '599b0659343a7a3cc852a60c2e527150121cccdf', 'qa/full.jsonl'),
    },
    'acpbench': {
        'dataset': 'ACPBench', 'url': 'https://github.com/IBM/ACPBench', 'revision': '2ed9c925962d57b275bf8c4e7b5d6f564aac9d6d',
        'license': 'CDLA-Permissive-2.0', 'split': 'all seven original MCQ test tasks; excludes boolean and generative tasks',
        'sources': github('IBM/ACPBench', '2ed9c925962d57b275bf8c4e7b5d6f564aac9d6d', [f'dataset/{task}/test.mcq.json.gz' for task in ['app', 'areach', 'just', 'land', 'prog', 'reach', 'val']]),
    },
    'aptbench': {
        'dataset': 'APTBench', 'url': 'https://github.com/TencentYoutuResearch/APTBench', 'revision': '9aab1301ab2c743be6bf11d1a2f3c3c6bc123ffc',
        'license': 'Apache-2.0 (upstream repository)', 'split': 'all seven English labeled-choice tasks; excludes Chinese, boolean, open completion and tool-name completion',
        'sources': github('TencentYoutuResearch/APTBench', '9aab1301ab2c743be6bf11d1a2f3c3c6bc123ffc', [f'data/{task}/input_data.jsonl' for task in APT_TASKS]),
    },
    'bixbench': {
        'dataset': 'BixBench v1.5', 'url': 'https://huggingface.co/datasets/futurehouse/BixBench', 'revision': 'f8cc3bdcc6357c88b8c3648306522b9c422dc95a',
        'license': 'Apache-2.0', 'split': 'full 205-question v1.5 release; native MCQ without optional refusal',
        'sources': huggingface('futurehouse/BixBench', 'f8cc3bdcc6357c88b8c3648306522b9c422dc95a', 'BixBench.jsonl'),
    },
    'backtrader': {
        'dataset': 'Backtrader-Bench', 'url': 'https://github.com/rzhao999/Backtrader-Bench', 'revision': 'a623e5d3e55126142a163c43f57ebc5d7178f316',
        'license': 'No explicit dataset license found; consult upstream terms', 'split': 'full 160-question base pool, not curated 30-question subset',
        'sources': github('rzhao999/Backtrader-Bench', 'a623e5d3e55126142a163c43f57ebc5d7178f316', ['datasets/backtrader_mcq_base_pool_all_strategies.jsonl']),
    },
}

from ._perma_sources import PATHS as PERMA_PATHS

REGISTRY.update({
    'personamem-v1': {
        'dataset': 'PersonaMem-v1 (128k)', 'url': 'https://huggingface.co/datasets/bowen-upenn/PersonaMem-v1',
        'revision': 'a8076d5608c93ba2a28983cd78aa99b01a163ae7', 'license': 'Consult upstream dataset card',
        'split': 'questions_128k.csv; duplicate choices excluded; same family as PersonaMem-v2',
        'sources': huggingface('bowen-upenn/PersonaMem-v1', 'a8076d5608c93ba2a28983cd78aa99b01a163ae7', 'questions_128k.csv'),
    },
    'perma': {
        'dataset': 'PERMA (Type 3)', 'url': 'https://huggingface.co/datasets/ustclsc/PERMA',
        'revision': '440e64e4fb8baec6f7ad10c1de135505f93e7cb1', 'license': 'Apache-2.0 (upstream repository)',
        'split': 'all 580 Type-3 overall MCQs, single- and multi-domain; excludes Type-1/2 checkpoint variants',
        'sources': [source for path in PERMA_PATHS for source in huggingface('ustclsc/PERMA', '440e64e4fb8baec6f7ad10c1de135505f93e7cb1', path)],
    },
    'membench-msa': {
        'dataset': 'MemBench (multi-session assistant subtask)', 'url': 'https://github.com/import-myself/Membench',
        'revision': 'f66d8d1028d3f68627d00f77a967b93fbb8694b6', 'license': 'Consult upstream repository terms',
        'split': 'all 500 FirstAgent/RecMultiSession questions; NOT the whole MemBench suite',
        'sources': github('import-myself/Membench', 'f66d8d1028d3f68627d00f77a967b93fbb8694b6', ['MemData/FirstAgent/RecMultiSession.json']),
    },
    'gui-world': {
        'dataset': 'GUI-World (released benchmark MCQs)', 'url': 'https://huggingface.co/datasets/ONE-Lab/GUI-World',
        'revision': '7901fa3f0b9e36afa87d24ff9ecd48037c7fd6a0', 'license': 'Consult upstream dataset card',
        'split': 'all native MCQs in six Annotation/benchmark files; no video or free-form tasks',
        'sources': [source for platform in ['IOS', 'XR', 'android', 'multi', 'software', 'website'] for source in huggingface('ONE-Lab/GUI-World', '7901fa3f0b9e36afa87d24ff9ecd48037c7fd6a0', f'Annotation/benchmark/{platform}.jsonl')],
    },
    'mmbench-gui-l1': {
        'dataset': 'MMBench-GUI (L1)', 'url': 'https://huggingface.co/datasets/OpenGVLab/MMBench-GUI',
        'revision': 'e27757e3910e0d5995b811f916b509b4e34a4690', 'license': 'Consult upstream dataset card',
        'split': 'all 3561 L1 questions across three difficulty levels; not L2-L4 agent tasks',
        'sources': huggingface('OpenGVLab/MMBench-GUI', 'e27757e3910e0d5995b811f916b509b4e34a4690', 'L1_annotations.json'),
    },
})


def parse_apt_choices(text):
    matches = list(re.finditer(r'(?:^|[\s;])\(([A-Z])\)\s*', text))
    labels = [match[1] for match in matches]
    if len(labels) < 2 or labels != [chr(65 + i) for i in range(len(labels))]:
        raise ValueError('ambiguous or nonconsecutive APT choice markers')
    options = [text[match.end():matches[i + 1].start() if i + 1 < len(matches) else len(text)].rstrip().rstrip(';').rstrip() for i, match in enumerate(matches)]
    return labels, options


def normalize(name, payloads, seed=42):
    """Return validated questions plus every excluded ID and reason; never infer gold."""
    questions, exclusions = [], []
    candidate_count = 0

    def add(id, options, answer, category='unknown', source_shuffle=False):
        nonlocal candidate_count
        candidate_count += 1
        # Exact duplicate texts make option-content invariance ambiguous.
        # Adapter-specific exclusions below are also recorded explicitly.
        if len(set(option.strip() for option in options)) != len(options):
            exclusions.append({'id': id, 'reason': 'duplicate option text after stripping'})
            return
        q = Question(id, tuple(options), answer, category)
        questions.append(shuffled(q, seed, name + '-source') if source_shuffle else q)

    for path, payload in payloads:
        if name == 'personamem-v1':
            rows = list(csv.DictReader(payload.decode('utf-8-sig').splitlines()))
        elif name in {'mmbench-gui-l1', 'membench-msa', 'perma'}:
            decoded = json.loads(payload)
            rows = decoded if isinstance(decoded, list) else [decoded]
        elif path.endswith('.gz'):
            rows = json.loads(gzip.decompress(payload))
        else:
            rows = [json.loads(line) for line in payload.decode('utf-8-sig').splitlines() if line.strip()]
        for index, row in enumerate(rows):
            if name == 'personamem-v1':
                raw = ast.literal_eval(row['all_options'])
                matches = [re.fullmatch(r'\(([a-d])\)\s*(.*)', value, re.S) for value in raw]
                if not all(matches) or [m[1] for m in matches] != list('abcd'):
                    raise ValueError('unexpected PersonaMem choice labels')
                add(str(row['question_id']), [m[2] for m in matches], 'abcd'.index(row['correct_answer'].strip('()')), row['question_type'])
            elif name == 'perma':
                if row['task_type'] != 3:
                    raise ValueError('PERMA adapter requires Type 3')
                parts = re.split(r'(?:^|\n)([A-H]):\s*', row['options'])
                labels, options = parts[1::2], [x.strip() for x in parts[2::2]]
                if labels != list('ABCDEFGH') or parts[0].strip():
                    raise ValueError('unexpected PERMA option layout')
                add(path, options, labels.index(row['gold_label']), Path(path).stem[:2])
            elif name == 'membench-msa':
                for category, items in row.items():
                    for i, item in enumerate(items):
                        qa = item['QA']
                        labels = list(qa['choices'])
                        # Upstream MembenchAgent.py interpolates choices via str.format,
                        # including Python's string representation of list-valued options.
                        add(f'{category}:{i}', [str(v) for v in qa['choices'].values()], labels.index(qa['ground_truth']), category)
            elif name == 'mmbench-gui-l1':
                for i, item in enumerate(row['groups']):
                    labels = list(item['options'])
                    add(f"{row['index']}:{i}", list(item['options'].values()), labels.index(item['answer']), row['platform'])
            elif name == 'gui-world':
                for key, item in row.items():
                    if not isinstance(item, dict) or 'Options' not in item:
                        continue
                    gold = item.get('Correct Answer', item.get('Answer', ''))
                    match = re.match(r'^(?:\[\[|\[|\()?([A-D])(?:[\].):]|$)', gold.strip())
                    label = match[1] if match else None
                    raw = item['Options']
                    labels = list(raw) if isinstance(raw, dict) else list('ABCD')[:len(raw)]
                    options = list(raw.values()) if isinstance(raw, dict) else [re.sub(r'^[A-D][.):]\s*', '', v) for v in raw]
                    id = f'{Path(path).stem}:{index}:{key}'
                    # Some official records use exact answer text instead of a letter.
                    exact = [i for i, option in enumerate(options) if option.strip() == gold.strip()]
                    if len(exact) == 1:
                        answer = exact[0]
                    elif label in labels:
                        answer = labels.index(label)
                    else:
                        candidate_count += 1
                        exclusions.append({'id': id, 'reason': 'gold is neither a released label nor unique exact option text'})
                        continue
                    add(id, options, answer, Path(path).stem)
            elif name == 'agentsense':
                for ci, character in enumerate(row['characters']):
                    for qi, item in enumerate(character['info_reason_questions']):
                        if item['options'][item['answer_label']] != item['answer']:
                            raise ValueError('AgentSense text and label disagree')
                        add(f"{row['sample_idx']}:{ci}:{qi}", item['options'], item['answer_label'], str(item.get('difficulty', 'unknown')))
            elif name == 'agenthop':
                add(row['id'], row['options'], row['correct_index'], row['reasoning_type'])
            elif name == 'acpbench':
                labels = row['choices']['label']
                if len(set(labels)) != len(labels):
                    raise ValueError('duplicate ACPBench labels')
                add(path.split('/')[1] + ':' + str(row['id']), row['choices']['text'], labels.index(row['answer']), path.split('/')[1])
            elif name == 'aptbench':
                category = '/'.join(path.split('/')[1:-1])
                try:
                    labels, options = parse_apt_choices(row['choices'])
                except ValueError as error:
                    candidate_count += 1
                    exclusions.append({'id': category + ':' + row['uuid'], 'reason': str(error)})
                    continue
                if row['answer'] not in labels:
                    candidate_count += 1
                    exclusions.append({'id': category + ':' + row['uuid'], 'reason': 'source gold label absent from released choices', 'gold_label': row['answer'], 'available_labels': labels})
                    continue
                add(category + ':' + row['uuid'], options, labels.index(row['answer']), category)
            elif name == 'bixbench':
                add(row['id'], [row['ideal']] + row['distractors'], 0, row.get('eval_mode', 'unknown'), True)
            elif name == 'backtrader':
                parts = re.split(r'\n([A-D])\. ', row['question'])
                labels, options = parts[1::2], parts[2::2]
                if labels != ['A', 'B', 'C', 'D'] or '\n\nRespond' not in options[-1]:
                    raise ValueError('unexpected Backtrader option layout')
                options[-1] = options[-1].split('\n\nRespond')[0]
                add(str(index), options, labels.index(row['answer']), row['type'])
            elif name == 'fdabench':
                if not row.get('correct_answer'):
                    candidate_count += 1
                    exclusions.append({'id': row['task_id'], 'reason': 'no gold answer in public release'})
                    continue
                if len(row['correct_answer']) != 1:
                    raise ValueError('FDABench single-choice row has multiple gold labels')
                labels = list(row['options'])
                add(row['task_id'], list(row['options'].values()), labels.index(row['correct_answer'][0]), row['database_type'])
            else:
                raise ValueError('unknown dataset adapter: ' + name)
    if not questions or len({q.id for q in questions}) != len(questions):
        raise ValueError('empty dataset or duplicate normalized IDs')
    return questions, {'candidate_count': candidate_count, 'included_count': len(questions), 'excluded_count': len(exclusions), 'exclusions': exclusions}


def download_benchmark(name, output, seed=42):
    spec = REGISTRY[name]
    output = Path(output)
    manifest_path = output.with_suffix(output.suffix + '.source.json')
    if output.exists() or manifest_path.exists():
        raise ValueError('output already exists; reuse it or choose a new path')
    payloads = []
    for source in spec['sources']:
        request = urllib.request.Request(source['url'], headers={'User-Agent': 'CSIEE/0.2 benchmark audit'})
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = response.read(100 * 1024 * 1024 + 1)
        if len(payload) > 100 * 1024 * 1024:
            raise ValueError('source exceeds 100 MiB')
        payloads.append((source['path'], payload))
    return prepare_benchmark(name, payloads, output, seed)


def prepare_benchmark(name, payloads, output, seed=42):
    """Normalize official source bytes, also allowing a previously downloaded cache."""
    spec = REGISTRY[name]
    output = Path(output)
    manifest_path = output.with_suffix(output.suffix + '.source.json')
    if output.exists() or manifest_path.exists():
        raise ValueError('output already exists; reuse it or choose a new path')
    if [path for path, _ in payloads] != [source['path'] for source in spec['sources']]:
        raise ValueError('source paths/order do not match the pinned registry')
    sources = [dict(source, sha256=hashlib.sha256(payload).hexdigest()) for source, (_, payload) in zip(spec['sources'], payloads)]
    questions, audit = normalize(name, payloads, seed)
    content = ''.join(json.dumps({'id': q.id, 'options': q.options, 'answer': q.answer, 'category': q.category}, ensure_ascii=False) + '\n' for q in questions).encode('utf-8')
    manifest = {k: v for k, v in spec.items() if k != 'sources'}
    manifest.update(sources=sources, normalization=audit, sha256=hashlib.sha256(content).hexdigest(),
                    adapter_version=1, adapter=name, source_order_seed=seed if name == 'bixbench' else None,
                    source_order='seeded native MCQ reconstruction' if name == 'bixbench' else 'native option order')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(content)
    manifest_path.write_bytes((json.dumps(manifest, indent=2) + '\n').encode('utf-8'))
    return manifest
