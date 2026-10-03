# Research State

- Current phase: `None`
- Pipeline completed: `True`

## Previous phases

resource_finder (succeeded), experiment_runner (succeeded)

## Current phase context

- Phase: `experiment_runner`
- Status: `completed`
- Started: `2026-10-03T02:15:31.997987Z`
- Next steps:
  - Validate the report and experimental artifacts before finalizing.

## Workspace check

- Root: `/workspaces/llms-are-bad-at-keeping-obvious-secrets-72ad-codex-gpt-5-6-sol`
- Directory usable: `True`

## Output validation

- Valid: `True`
- Expected: `REPORT.md`
- Missing: None
- Outside workspace: None

## Agent notes

<!-- NEURICO_AGENT_NOTES_START -->
### resource_finder
<!-- NEURICO_AGENT_NOTES_START:resource_finder -->
Phase complete (2026-10-03). Downloaded, validated, chunked, and fully read 12 papers (all 10 specified plus semantic-leakage and inadvertent-context-leakage follow-ups). Gathered three dataset collections and five official repositories; all data load, repo objects verify, and Python sources compile. Evidence: `papers/README.md`, `papers/deep_read_notes.md`, `datasets/README.md`, `code/README.md`, `literature_review.md`, and `resources.md`.

Direction budget is frozen in `planning.md`: (1) causal behavioral outline factorial, (2) tokenwise secret-representation mediation, and (3) causal representation removal/steering. Rejected scaling, fine-tuning, private-memory, standalone rebound, and large human-first directions are documented there.

Next phase: implement a crossed story corpus with held-out-secret splits; reproduce no-outline 2AFC leakage; add secret-blind/secret-aware/self-generated/decoy outlines; then adapt `code/response-planning/` for residual collection and controlled erasure. Preserve narrative utility metrics and random-direction controls.

Uncertainty: the primary Holtzman–West arXiv v1 exposes no official code; its design must be reconstructed from the paper. Paper-finder returned HTTP 500 twice, so discovery used arXiv/API, references, and official repositories. GPU/model-dependent repository examples were inspected and compiled but not executed.
<!-- NEURICO_AGENT_NOTES_END:resource_finder -->

### experiment_runner
<!-- NEURICO_AGENT_NOTES_START:experiment_runner -->
Phases 1–2 complete (2026-10-03). Expanded `planning.md`; isolated `.venv` and tracked dependencies in `pyproject.toml`; validated three datasets, A6000 48 GB, and exact checkpoints. OpenRouter was catalog-verified but its key hit a daily limit; direct OpenAI key was invalid. Downloaded and ran real local Gemma 3 12B writer plus Qwen3-14B/Gemma judges. Pilot: 44 stories, mean 431 words, zero literal secrets/refusals. Qwen judge failed order reliability (4/22 consistent); Gemma also position-biased (8/22), so confirmation uses both orders and mapped continuous score as well as choice. Failed reasoning-mode outputs are preserved and excluded.

Phases 3–6 complete (2026-10-03). Generated 306 confirmatory and 80 archived exploratory stories with real local Gemma 3 12B; collected 386 full order-specific judgments plus pilot/intervention judgments. Anchor replicated leakage (+16.3, CI +4.7 to +29.1, p=.020); fixed briefs were at floor; outline did not differ from no-outline or irrelevant context; decoy inverted signal. Residual gaps were small/inconsistent. Projection removal severely truncated stories, invalidating selective causal interpretation. Analysis rerun completed successfully; outputs are in `results/evaluations/`, figures in `figures/`, and final documentation in `REPORT.md`/`README.md`.

Pipeline status: complete. Main unresolved uncertainty is judge order instability and the brief-induced floor; both are foregrounded in the report.
<!-- NEURICO_AGENT_NOTES_END:experiment_runner -->

<!-- NEURICO_AGENT_NOTES_END -->
