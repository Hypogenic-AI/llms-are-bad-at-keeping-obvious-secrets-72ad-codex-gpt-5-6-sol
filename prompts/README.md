# Prompt provenance

Exact prompt constructors are versioned in `src/run_behavioral.py`. Conditions
are `none`, externally supplied secret-blind `outline`, length-matched-ish
`irrelevant` context, and published-effect-inspired `decoy`. Plot trials omit
the decoy condition and compare twist-aware versus premise-only writers.

Writer: `google/gemma-3-12b-it`, temperature 0.8, maximum 900 tokens. Judge:
`openai/gpt-5.6-luna`, temperature 0, JSON output, both presentation orders.
