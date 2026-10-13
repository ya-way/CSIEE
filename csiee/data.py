"""Strict local adapters. Loading never silently drops broken examples."""

import ast
import csv
import hashlib
import json
import random
from dataclasses import dataclass, replace
from pathlib import Path

from .strategies import predict


@dataclass(frozen=True)
class Question:
    id: str
    options: tuple
    answer: int
    category: str = 'unknown'

    def __post_init__(self):
        if not isinstance(self.id, str) or not self.id:
            raise ValueError('id must be a non-empty string')
        predict('lite', self.options)
        if isinstance(self.answer, bool) or not isinstance(self.answer, int) or not 0 <= self.answer < len(self.options):
            raise ValueError('answer must be a zero-based integer within options')
        if len({o.strip() for o in self.options}) != len(self.options):
            raise ValueError('duplicate options are ambiguous')


def stable_seed(*parts):
    return int.from_bytes(hashlib.sha256(json.dumps(parts, ensure_ascii=False).encode('utf-8')).digest()[:8], 'big')


def shuffled(question, seed, namespace='control'):
    order = list(range(len(question.options)))
    random.Random(stable_seed(namespace, seed, question.id)).shuffle(order)
    return replace(question, options=tuple(question.options[i] for i in order), answer=order.index(question.answer))


def _literal(value):
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return ast.literal_eval(value)


def load_questions(path, format='jsonl', seed=42):
    path = Path(path)
    questions = []
    with path.open(encoding='utf-8-sig', newline='') as stream:
        if format in ('jsonl', 'openbookqa'):
            for line, text in enumerate(stream, 1):
                if not text.strip():
                    continue
                try:
                    row = json.loads(text)
                    if format == 'openbookqa':
                        choices = row['question']['choices']
                        labels = [choice['label'] for choice in choices]
                        if len(set(labels)) != len(labels):
                            raise ValueError('choice labels must be unique')
                        questions.append(Question(row['id'], tuple(choice['text'] for choice in choices), labels.index(row['answerKey'])))
                        continue
                    if not isinstance(row.get('options'), list):
                        raise ValueError('options must be a JSON array')
                    questions.append(Question(row['id'], tuple(row['options']), row['answer'], str(row.get('category', 'unknown'))))
                except (ValueError, KeyError, TypeError, AttributeError) as error:
                    raise ValueError(f'line {line}: {error}') from error
        elif format == 'personamem-v2':
            csv.field_size_limit(16 * 1024 * 1024)
            reader = csv.DictReader(stream)
            required = {'persona_id', 'user_query', 'correct_answer', 'incorrect_answers'}
            if not required.issubset(reader.fieldnames or []):
                raise ValueError('PersonaMem-v2 CSV is missing required columns: ' + ', '.join(sorted(required)))
            for index, row in enumerate(reader):
                try:
                    wrong = _literal(row['incorrect_answers'])
                    if not isinstance(wrong, list) or not wrong:
                        raise ValueError('incorrect_answers must be a non-empty list')
                    question = Question(f"{row['persona_id']}:{index}", tuple([row['correct_answer']] + wrong), 0, row.get('topic_query') or 'unknown')
                    questions.append(shuffled(question, seed, 'personamem-source'))
                except (ValueError, TypeError, SyntaxError) as error:
                    raise ValueError(f'CSV record {index + 1}: {error}') from error
        else:
            raise ValueError('unsupported format: ' + format)
    if not questions:
        raise ValueError('dataset contains no questions')
    if len({q.id for q in questions}) != len(questions):
        raise ValueError('question IDs must be unique')
    return questions
