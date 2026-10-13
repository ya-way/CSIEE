import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from csiee.data import Question, load_questions, shuffled
from csiee.evaluate import evaluate, save_report, wilson
from csiee.strategies import STRATEGIES, predict

ROOT = Path(__file__).resolve().parents[1]


class StrategyTests(unittest.TestCase):
    def test_lite_c_and_short_ballot(self):
        self.assertEqual(predict('lite', ['a', 'b', 'c', 'd', 'e']), 2)
        self.assertEqual(predict('lite', ['a', 'b']), 1)

    def test_pro_both_folklore_rules(self):
        self.assertEqual(predict('pro', ['a', 'bb', 'cc', 'long answer']), 3)
        self.assertEqual(predict('pro', ['long one', 'x', 'long two', 'long six']), 1)
        self.assertEqual(predict('pro', ['one', 'two', 'six', 'ten']), 2)

    def test_numeric_means_third_largest_not_third_position(self):
        self.assertEqual(predict('numeric', ['2', '8', '6', '4']), 3)
        self.assertEqual(predict('numeric', ['-10', '-40', '-20', '-30']), 3)
        self.assertEqual(predict('numeric', ['0.2', '80%', '6e-1', '40%']), 3)
        self.assertEqual(predict('numeric', ['1', '1', '2', '3']), 2)
        self.assertEqual(predict('numeric', ['1 cat', '2 cats', '3 cats', '4 cats']), 2)

    def test_cautious_word_boundaries(self):
        self.assertEqual(predict('cautious', ['Always yes', 'Maybe', 'Never', 'Must']), 1)
        self.assertEqual(predict('cautious', ['small', 'stone', 'forest', 'call']), 2)

    def test_deterministic_ties_and_valid_indices(self):
        for options in (['a', 'b'], ['a', 'b', 'c', 'd'], ['1', '2', '3', '4', '5']):
            for strategy in STRATEGIES:
                first = predict(strategy, options)
                self.assertIn(first, range(len(options)))
                self.assertEqual(first, predict(strategy, options))
        self.assertEqual(predict('promax', ['one', 'two', 'six', 'ten']), 2)

    def test_bad_inputs(self):
        for options in ([], ['a'], ['a', ''], ['a', None], 'abcd', ['x'] * 27):
            with self.assertRaises(ValueError):
                predict('pro', options)
        with self.assertRaises(ValueError):
            predict('ultra', ['a', 'b'])


class DataTests(unittest.TestCase):
    def test_openbookqa_uses_labels_not_alphabetical_assumptions(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'obqa.jsonl'
            row = {'id': 'q', 'question': {'choices': [{'label': 'D', 'text': 'right'}, {'label': 'B', 'text': 'wrong'}]}, 'answerKey': 'D'}
            path.write_text(json.dumps(row), encoding='utf-8')
            self.assertEqual(load_questions(path, 'openbookqa')[0].answer, 0)
            row['answerKey'] = 'missing'
            path.write_text(json.dumps(row), encoding='utf-8')
            with self.assertRaises(ValueError):
                load_questions(path, 'openbookqa')

    def test_shuffle_keeps_correct_content(self):
        q = Question('q', ('first', 'second', 'third', 'fourth'), 1)
        observed = set()
        for seed in range(30):
            other = shuffled(q, seed)
            self.assertEqual(other.options[other.answer], 'second')
            self.assertEqual(other, shuffled(q, seed))
            observed.add(other.answer)
        self.assertEqual(observed, {0, 1, 2, 3})

    def test_strict_labels_and_duplicates(self):
        for answer in (-1, 3, 'C', True):
            with self.assertRaises(ValueError):
                Question('q', ('a', 'b', 'c'), answer)
        with self.assertRaises(ValueError):
            Question('q', ('same', ' same '), 0)

    def test_personamem_adapter_shuffles_and_preserves_labels(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'benchmark.csv'
            with path.open('w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['persona_id', 'user_query', 'correct_answer', 'incorrect_answers'])
                writer.writeheader()
                for i in range(30):
                    writer.writerow({'persona_id': i, 'user_query': '{"content":"unused"}', 'correct_answer': 'yes', 'incorrect_answers': '["no", "maybe", "unknown"]'})
            rows = load_questions(path, 'personamem-v2')
            self.assertEqual({q.answer for q in rows}, {0, 1, 2, 3})
            self.assertTrue(all(q.options[q.answer] == 'yes' for q in rows))

    def test_invalid_jsonl_does_not_silently_skip(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'broken.jsonl'
            for text in ('', '{}\n', '[]\n', '{"id":"a","options":"abcd","answer":2}\n'):
                path.write_text(text, encoding='utf-8')
                with self.assertRaises(ValueError):
                    load_questions(path)
            row = '{"id":"a","options":["x","y"],"answer":1}\n'
            path.write_text(row * 2, encoding='utf-8')
            with self.assertRaises(ValueError):
                load_questions(path)


class EvaluationTests(unittest.TestCase):
    def test_repeatable_and_no_answer_leakage(self):
        path = ROOT / 'data/demo.jsonl'
        self.assertEqual(evaluate(path, shuffles=2), evaluate(path, shuffles=2))
        calls = []
        def spy(options):
            calls.append(options)
            self.assertIsInstance(options, tuple)
            self.assertTrue(all(isinstance(o, str) for o in options))
            return 0
        with patch.dict(STRATEGIES, {'spy': spy}):
            evaluate(path, strategies=['spy'], shuffles=1)
        self.assertEqual(len(calls), 16)

    def test_known_scores_and_permutation_invariance(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'known.jsonl'
            rows = [{'id': str(i), 'options': ['a', 'b', 'longest answer', 'd'], 'answer': 2} for i in range(100)]
            path.write_text(''.join(json.dumps(r) + '\n' for r in rows), encoding='utf-8')
            report = evaluate(path, strategies=['lite', 'longest'], shuffles=10)
            lite, longest = report['results']
            self.assertEqual(lite['accuracy'], 1)
            self.assertLess(lite['shuffled_mean'], .4)
            self.assertEqual(longest['shuffled_mean'], 1)
            self.assertEqual(longest['choice_invariance'], 1)
            save_report(report, Path(temp) / 'out')
            self.assertEqual(len((Path(temp) / 'out/predictions.jsonl').read_text().splitlines()), 200)

    def test_mixed_choice_chance_and_limit(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'mixed.jsonl'
            path.write_text('{"id":"a","options":["x","y"],"answer":1}\n{"id":"b","options":["a","b","c","d"],"answer":2}\n', encoding='utf-8')
            self.assertEqual(evaluate(path, shuffles=1)['chance_accuracy'], .375)
            self.assertEqual(evaluate(path, shuffles=1, limit=1)['n'], 1)
            for kw in ({'shuffles': 0}, {'limit': 0}, {'strategies': []}):
                with self.assertRaises(ValueError):
                    evaluate(path, **kw)

    def test_manifest_mismatch(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'data.jsonl'
            path.write_bytes((ROOT / 'data/demo.jsonl').read_bytes())
            path.with_suffix('.jsonl.source.json').write_text('{"sha256":"wrong"}')
            with self.assertRaisesRegex(ValueError, 'hash'):
                evaluate(path, shuffles=1)

    def test_wilson_edges(self):
        self.assertAlmostEqual(wilson(0, 100)[0], 0)
        self.assertAlmostEqual(wilson(100, 100)[1], 1)
        self.assertLess(wilson(25, 100)[0], .25)
        self.assertGreater(wilson(25, 100)[1], .25)

    def test_cross_process_hash_seed_independence(self):
        code = "from csiee.data import stable_seed; print(stable_seed('hello', 42))"
        values = [subprocess.check_output([sys.executable, '-c', code], env=dict(os.environ, PYTHONHASHSEED=s), cwd=ROOT) for s in ('1', '987')]
        self.assertEqual(*values)

    def test_cli_success_and_friendly_errors(self):
        run = subprocess.run([sys.executable, '-m', 'csiee', 'guess', '2', '8', '6', '4', '--strategy', 'numeric'], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['label'], 'D')
        run = subprocess.run([sys.executable, '-m', 'csiee', 'eval', 'missing.jsonl'], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)
        self.assertNotIn('Traceback', run.stderr)


if __name__ == '__main__':
    unittest.main()
