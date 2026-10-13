import gzip
import json
import hashlib
import tempfile
import unittest
from pathlib import Path

from csiee.benchmarks import normalize, parse_apt_choices, prepare_benchmark
from csiee.evaluate import evaluate


def payload(rows):
    return '\n'.join(json.dumps(row) for row in rows).encode()


class AdapterTests(unittest.TestCase):
    def test_apt_inline_and_multiline(self):
        labels, options = parse_apt_choices('(A) first; (B) second\n(C) third (D) fourth')
        self.assertEqual(labels, list('ABCD'))
        self.assertEqual(options, ['first', 'second', 'third', 'fourth'])
        with self.assertRaises(ValueError):
            parse_apt_choices('(A) one (B) two (B) ambiguous')

    def test_apt_exclusions_are_audited(self):
        rows = [
            {'uuid': 'good', 'choices': '(A) one (B) two', 'answer': 'B'},
            {'uuid': 'missing-gold', 'choices': '(A) one (B) two', 'answer': 'D'},
            {'uuid': 'duplicate', 'choices': '(A) same (B) same', 'answer': 'A'},
            {'uuid': 'ambiguous', 'choices': '(A) one (B) two (B) three', 'answer': 'A'},
        ]
        questions, audit = normalize('aptbench', [('data/issue_fix/locate/input_data.jsonl', payload(rows))])
        self.assertEqual(len(questions), 1)
        self.assertEqual(questions[0].answer, 1)
        self.assertEqual(audit['candidate_count'], 4)
        self.assertEqual(audit['excluded_count'], 3)
        self.assertEqual(len({x['reason'] for x in audit['exclusions']}), 3)

    def test_agentsense_nested_gold_and_duplicates(self):
        item = {'options': ['right', 'wrong'], 'answer_label': 0, 'answer': 'right'}
        row = {'sample_idx': 8, 'characters': [{'info_reason_questions': [item]}, {'info_reason_questions': []}]}
        questions, audit = normalize('agentsense', [('data.jsonl', payload([row]))])
        self.assertEqual(questions[0].id, '8:0:0')
        self.assertEqual(audit['included_count'], 1)
        item['answer'] = 'wrong'
        with self.assertRaisesRegex(ValueError, 'disagree'):
            normalize('agentsense', [('data.jsonl', payload([row]))])

    def test_acp_explicit_labels_and_namespaced_ids(self):
        row = {'id': 1, 'choices': {'text': ['one', 'two'], 'label': ['D', 'B']}, 'answer': 'B'}
        blob = gzip.compress(json.dumps([row]).encode())
        questions, _ = normalize('acpbench', [('dataset/app/test.mcq.json.gz', blob), ('dataset/prog/test.mcq.json.gz', blob)])
        self.assertEqual([q.id for q in questions], ['app:1', 'prog:1'])
        self.assertEqual([q.answer for q in questions], [1, 1])

    def test_bix_gold_not_confused_with_boolean_hypothesis(self):
        rows = [{'id': str(i), 'ideal': 'correct', 'distractors': ['wrong', 'no', 'maybe'], 'answer': False} for i in range(20)]
        questions, _ = normalize('bixbench', [('BixBench.jsonl', payload(rows))])
        self.assertTrue(all(q.options[q.answer] == 'correct' for q in questions))
        self.assertGreater(len({q.answer for q in questions}), 1)

    def test_backtrader_removes_final_instruction_from_last_option(self):
        row = {'question': 'Question?\n\nA. 1\nB. 2\nC. 3\nD. 4\n\nRespond in the form <<< X >>>', 'answer': 'D', 'type': 'test'}
        questions, _ = normalize('backtrader', [('data.jsonl', payload([row]))])
        self.assertEqual(questions[0].options, ('1', '2', '3', '4'))
        self.assertEqual(questions[0].answer, 3)

    def test_agenthop_ignores_distractor_type_gold_hints(self):
        row = {'id': 'q', 'options': ['a', 'bb', 'ccc', 'dddd'], 'correct_index': 0, 'reasoning_type': 'RESULT', 'distractor_types': ['correct', 'wrong', 'wrong', 'wrong']}
        questions, _ = normalize('agenthop', [('qa/full.jsonl', payload([row]))])
        self.assertEqual(questions[0].options, ('a', 'bb', 'ccc', 'dddd'))
        self.assertFalse(hasattr(questions[0], 'distractor_types'))

    def test_fda_missing_gold_is_audited_not_guessed(self):
        row = {'task_id': 'labeled', 'options': {'A': 'first', 'C': 'second'}, 'correct_answer': ['C'], 'database_type': 'test'}
        missing = dict(row, task_id='unlabeled', correct_answer=[])
        questions, audit = normalize('fdabench', [('single/data.jsonl', payload([row, missing]))])
        self.assertEqual(questions[0].answer, 1)
        self.assertEqual(audit['candidate_count'], 2)
        self.assertEqual(audit['exclusions'], [{'id': 'unlabeled', 'reason': 'no gold answer in public release'}])
        with self.assertRaisesRegex(ValueError, 'multiple gold'):
            normalize('fdabench', [('single/data.jsonl', payload([dict(row, correct_answer=['A', 'C'])]))])

    def test_preparation_pins_paths_hashes_and_refuses_overwrite(self):
        blob = payload([{'id': 'q', 'options': ['one', 'two'], 'correct_index': 1, 'reasoning_type': 'test'}])
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'hop.jsonl'
            with self.assertRaisesRegex(ValueError, 'paths/order'):
                prepare_benchmark('agenthop', [('wrong.jsonl', blob)], output)
            self.assertFalse(output.exists())
            manifest = prepare_benchmark('agenthop', [('qa/full.jsonl', blob)], output)
            self.assertEqual(manifest['sources'][0]['sha256'], hashlib.sha256(blob).hexdigest())
            self.assertEqual(manifest['sha256'], hashlib.sha256(output.read_bytes()).hexdigest())
            self.assertEqual(evaluate(output, shuffles=1)['n'], 1)
            with self.assertRaisesRegex(ValueError, 'already exists'):
                prepare_benchmark('agenthop', [('qa/full.jsonl', blob)], output)
            output.write_bytes(output.read_bytes() + b'\n')
            with self.assertRaisesRegex(ValueError, 'hash'):
                evaluate(output, shuffles=1)


if __name__ == '__main__':
    unittest.main()
