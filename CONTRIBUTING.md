# Contributing

New exam folklore is welcome. Test-set tuning disguised as folklore is not.

1. Add a small deterministic strategy to `csiee/strategies.py` and register it in `STRATEGIES`.
2. It may read option text only. Keep answer labels, question IDs, questions and histories out of the predictor.
3. Describe parsing, ties, abstentions and fallback behavior in `docs/methodology.md`.
4. Add focused tests, then run `python -m unittest discover -s tests -v`.
5. Run all strategies with the same data, seed and option-order controls. Include disappointing results.

For new dataset adapters, cite the official source, pin a version, respect its license, reject ambiguous records, and test that shuffling preserves the correct answer text. Never commit API keys, downloaded chat histories, or unlicensed dataset copies. CI must run offline after package installation.
