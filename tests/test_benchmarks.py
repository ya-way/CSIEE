import csv
import io
import gzip
import json
import hashlib
import tempfile
import unittest
from pathlib import Path

from csiee.benchmarks import normalize, parse_apt_choices, prepare_benchmark, huggingface
from csiee.evaluate import evaluate


def payload(rows):
    return '\n'.join(json.dumps(row) for row in rows).encode()


class AdapterTests(unittest.TestCase):
    def test_personamem_csv_embedded_newlines_and_duplicate_exclusion(self):
        stream = io.StringIO()
        writer = csv.DictWriter(stream, fieldnames=['question_id', 'all_options', 'correct_answer', 'question_type'])
        writer.writeheader()
        writer.writerow(dict(question_id='q', all_options=repr(['(a) first', '(b) second\nline', '(c) third', '(d) fourth']), correct_answer='(b)', question_type='recall'))
        writer.writerow(dict(question_id='dup', all_options=repr(['(a) same', '(b) same', '(c) c', '(d) d']), correct_answer='(b)', question_type='recall'))
        qs, audit = normalize('personamem-v1', [('questions_128k.csv', stream.getvalue().encode())])
        self.assertEqual((qs[0].options[1], qs[0].answer), ('second\nline', 1))
        self.assertEqual(audit['excluded_count'], 1)

    def test_perma_multiline_options_type_and_url_encoding(self):
        row = dict(task_type=3, options='A: first\ncontinued\nB: second\nC: third\nD: fourth\nE: fifth\nF: sixth\nG: seventh\nH: eighth', gold_label='H')
        qs, _ = normalize('perma', [('SD-Rental Cars_3.json', json.dumps(row).encode())])
        self.assertEqual((qs[0].category, qs[0].answer, qs[0].options[0]), ('SD', 7, 'first\ncontinued'))
        self.assertIn('Rental%20Cars', huggingface('a/b', 'pin', 'SD-Rental Cars_3.json')[0]['url'])
        row['task_type'] = 1
        with self.assertRaisesRegex(ValueError, 'Type 3'):
            normalize('perma', [('SD_1.json', json.dumps(row).encode())])

    def test_gui_world_exact_text_letter_and_unmappable_gold(self):
        row = {'Reasoning': {'Options': ['a text', 'b text', 'c text', 'd text'], 'Correct Answer': 'b text'},
               'MCQA': {'Options': ['A. aa', 'B. bb', 'C. cc', 'D. dd'], 'Answer': '[[C]] cc'},
               'bad': {'Options': ['a', 'b', 'c', 'd'], 'Answer': 'A completely unrelated description'}}
        qs, audit = normalize('gui-world', [('benchmark/software.jsonl', payload([row]))])
        self.assertEqual([q.answer for q in qs], [1, 2])
        self.assertEqual(qs[1].options, ('aa', 'bb', 'cc', 'dd'))
        self.assertEqual(audit['excluded_count'], 1)

    def test_mmbench_groups_preserve_labels_and_platform(self):
        row = dict(index=9, platform='os_ios', groups=[dict(options={'C': 'cc', 'A': 'aa'}, answer='A')])
        qs, _ = normalize('mmbench-gui-l1', [('L1_annotations.json', json.dumps([row]).encode())])
        self.assertEqual((qs[0].id, qs[0].answer, qs[0].category), ('9:0', 1, 'os_ios'))

    def test_membench_list_options_match_upstream_interpolation(self):
        row = {'msa': [{'QA': {'choices': {'A': ['one', 'two'], 'B': ['three']}, 'ground_truth': 'B'}}]}
        qs, _ = normalize('membench-msa', [('RecMultiSession.json', json.dumps(row).encode())])
        self.assertEqual(qs[0].options, ("['one', 'two']", "['three']"))
        self.assertEqual(qs[0].answer, 1)

    def test_option_count_counts_support_adjusted_metric(self):
        rows = [dict(id='two', options=['longest', 'x'], answer=0), dict(id='four', options=['a', 'bb', 'ccc', 'dddd'], answer=0)]
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'q.jsonl'; p.write_bytes(payload(rows))
            report = evaluate(p, strategies=['xiaoming'], shuffles=1)
        counts = report['results'][0]['by_option_count']
        self.assertEqual(counts, {'2': {'n': 1, 'correct': 1}, '4': {'n': 1, 'correct': 0}})
        self.assertEqual(sum((int(m)-1)/int(m)*c['correct'] for m,c in counts.items())/2, .25)

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
