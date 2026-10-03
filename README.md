# LLM secret leakage with outlines

This project tests whether an explicit story outline reduces involuntary secret leakage in Gemma 3 12B and probes/intervenes on secret-aligned residual directions. See [REPORT.md](REPORT.md) for complete methods and results.

Key findings:

- An unconstrained open-story anchor leaked (+16.3 score points, 95% CI +4.7 to +29.1).
- A neutral story brief already removed detectable leakage; outlines did not improve on the brief or length-matched irrelevant context.
- The decoy condition inverted the signal, qualitatively replicating prior work.
- Plot and residual-direction evidence was inconclusive.
- Projection removal damaged generation severely, so it did not establish selective causal removal.

## Reproduce

```bash
source .venv/bin/activate
python src/run_local.py --stage writer --batch-size 32
python src/run_local.py --stage judge --judge-model gemma --batch-size 8
python src/run_mechanism.py
python src/judge_interventions.py
python src/analyze.py
```

Local checkpoints are expected at `models/gemma-3-12b-it/` and `models/qwen3-14b/`. Revisions and dependency versions are in `REPORT.md`, `pyproject.toml`, and `uv.lock`.

## Structure

- `src/`: generation, judging, mechanism, and analysis code
- `results/model_outputs/`: raw real-model stories and judgments
- `results/evaluations/`: statistics and pair-level summaries
- `figures/`: report figures
- `planning.md`: preregistered design and direction budget
- `literature_review.md`, `resources.md`, `papers/`: gathered evidence
