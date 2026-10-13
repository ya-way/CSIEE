"""Download the public, pinned upstream CSV; no third-party runtime packages."""

import hashlib
import io
import json
import urllib.request
import zipfile
from pathlib import Path

REVISION = 'ed956dea41521fc4499acbc63f966e0fd3c053ba'
DATASET = 'bowen-upenn/PersonaMem-v2'


def download_personamem(output):
    output = Path(output)
    if output.exists() or output.with_suffix(output.suffix + '.source.json').exists():
        raise ValueError('output already exists; choose a new path or reuse the existing download')
    url = f'https://huggingface.co/datasets/{DATASET}/resolve/{REVISION}/benchmark/text/benchmark.csv'
    request = urllib.request.Request(url, headers={'User-Agent': 'CSIEE/0.1 (benchmark audit)'})
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = response.read(100 * 1024 * 1024 + 1)
    if len(payload) > 100 * 1024 * 1024:
        raise ValueError('download exceeded 100 MiB')
    if not payload.startswith(b'persona_id,'):
        raise ValueError('download did not return the expected PersonaMem CSV')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(payload)
    manifest = {'dataset': DATASET, 'revision': REVISION, 'split': 'benchmark_text', 'url': url,
                'license': 'CC-BY-4.0 (upstream data)', 'sha256': hashlib.sha256(payload).hexdigest()}
    output.with_suffix(output.suffix + '.source.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return manifest


def download_openbookqa(output):
    output = Path(output)
    if output.exists() or output.with_suffix(output.suffix + '.source.json').exists():
        raise ValueError('output already exists; choose a new path or reuse the existing download')
    url = 'https://s3-us-west-2.amazonaws.com/ai2-website/data/OpenBookQA-V1-Sep2018.zip'
    expected = '82368cf05df2e3b309c17d162e10b888b4d768fad6e171e0a041954c8553be46'
    with urllib.request.urlopen(url, timeout=120) as response:
        archive = response.read(100 * 1024 * 1024 + 1)
    if hashlib.sha256(archive).hexdigest() != expected:
        raise ValueError('OpenBookQA archive hash changed; refusing an unpinned version')
    member = 'OpenBookQA-V1-Sep2018/Data/Main/test.jsonl'
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        payload = zipped.read(member)  # Read one fixed member; never extract archive paths.
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(payload)
    manifest = {'dataset': 'allenai/OpenBookQA', 'revision': 'V1-Sep2018', 'split': 'test',
                'url': url, 'archive_sha256': expected, 'member': member,
                'license': 'Unspecified in upstream dataset card; consult upstream terms', 'sha256': hashlib.sha256(payload).hexdigest()}
    output.with_suffix(output.suffix + '.source.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return manifest
