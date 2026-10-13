# Verification record

Final verification:

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python scripts/run_evaluation.py
```

The final branch includes six tests, a reproducible evaluation JSON, a CI workflow, and a historical failure transcript. The failure was caused by an asymmetric revision comparator and was fixed by computing both added and removed entity sets.
