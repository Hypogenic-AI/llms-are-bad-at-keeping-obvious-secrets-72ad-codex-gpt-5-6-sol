# Cloned Repositories

All repositories were shallow-cloned on 2026-10-03 and passed `python -m compileall`. Full experiments were not run because they require model weights, API credentials, and/or a CUDA GPU. Commit hashes make the local snapshots reproducible.

## ConfAIde

- **URL:** <https://github.com/skywalker023/confaide>
- **Location/commit:** `code/confaide/` at `3174c63e689226189675a740b7bf9053f10bae50`
- **Purpose:** Four-tier contextual-privacy benchmark and evaluation harness
- **Key files:** `eval.py`, `agents/`, `benchmark/`
- **Requirements:** Legacy Python 3.9/OpenAI 0.27 stack, Hugging Face models, BLEURT/BERTScore; upstream documents Conda, but do not install it in this workspace
- **Use here:** Adapt its tier-3/4 privacy and utility evaluation patterns; do not treat direct disclosure as equivalent to thematic leakage
- **Validation:** Dataset files match the separately downloaded `datasets/confaide/` copies; source compiles

## Emergent Response Planning in LLMs

- **URL:** <https://github.com/niconi19/Emergent-Response-Planning-in-LLMs>
- **Location/commit:** `code/response-planning/` at `f3c8dbf85a9324a8c180b2e4e4b243d6dcc740ed`
- **Purpose:** Collect responses and residual activations, label future response properties, train/test linear probes
- **Key files:** `get_responses.py`, `add_labels.py`, `get_hidden_representations.py`, `test_probing.py`, `data_utils.py`
- **Requirements:** Pinned Transformers/Datasets/PEFT/scikit-learn stack, PyTorch 2.2/CUDA 11.8 in upstream instructions; model paths must be filled in `config.yaml`
- **Use here:** Best scaffold for tokenwise/layerwise secret probes. Add a story-secret dataset adapter and split by secret identity rather than using its default random row split.
- **Validation:** Source compiles; README pipeline and dataset adapters were inspected. Execution is blocked by absent model paths and GPU weights.

## Eliciting Secrets

- **URL:** <https://github.com/EmilRyd/eliciting-secrets>
- **Location/commit:** `code/eliciting-secrets/` at `5632f9d7c9993bdf46aec6de6bf7cc64a29d2eb9`
- **Purpose:** Train Taboo/SSC secret-keeping models and evaluate black-box prefills, logit lens, and SAE elicitation
- **Key files:** `evaluate_logit_lens.py`, `evaluate_sae_weighted.py`, `prefill_guess_secret_word.py`, `guess_secret_word.py`, `configs/taboo_*.yaml`
- **Requirements:** Python 3.10+, PyTorch 2.7, Transformers, PEFT, TRL, nnsight, sae-lens, bitsandbytes, Hugging Face models; GPU expected
- **Use here:** Reuse secret vocabulary/config conventions and white-box measurement code, while avoiding manual feature-selection leakage and using held-out concepts
- **Validation:** Source compiles and its `uv` project metadata resolves conceptually; heavyweight dependencies were not added to the shared experiment environment.

## Don't Think of the White Bear

- **URL:** <https://github.com/cesium132dot9/Dont-Think-of-the-White-Bear>
- **Location/commit:** `code/white-bear/` at `c6187468e380fc44869ddfd414c8efcd46d94da9`
- **Purpose:** ReboundBench prompts, forbidden-token log-probability experiments, and attention-head ablations
- **Key files:** `src/experiment.py`, `src/circuit_tracing.py`, `data/`
- **Requirements:** PyTorch, Transformers, TransformerLens, Hugging Face access, GPU for practical circuit tracing
- **Use here:** Source balanced single-token concepts and matched negative/neutral/positive controls; adapt its norm-matched ablation pattern as a supporting analysis
- **Validation:** Both CSVs load (5,000 and 500 rows), source compiles, and published outputs are present. The repository README says MIT, but no root `LICENSE` file is present in this snapshot; confirm licensing before redistribution.

## FutureGPT2

- **URL:** <https://github.com/wiwu2390/FutureGPT2-public>
- **Location/commit:** `code/futuregpt2/` at `22b86c13c59a47124ee074a3d8cf0be591e4196e`
- **Purpose:** Myopic-training and future-token pre-caching experiments from Wu et al. (2024)
- **Key files:** `src/models/myopic_model.py`, `src/models/future_model.py`, `src/data/synthetic.py`, `src/scripts/`
- **Requirements:** Not documented in a lockfile; inspection shows a research training stack and experiment-specific data/configuration
- **Use here:** Conceptual reference for separating future-loss-driven planning from ordinary breadcrumbs; not a direct experimental dependency
- **Validation:** Source compiles. No turnkey lightweight example or pinned environment is supplied, so it was not executed.

## Recommended Reuse Order

1. Adapt `response-planning` for residual collection and probes.
2. Borrow secret configurations and elicitation checks from `eliciting-secrets`.
3. Reuse matched controls and causal-ablation conventions from `white-bear`.
4. Use ConfAIde only for transfer/utility evaluation.
5. Treat FutureGPT2 as a methodological reference rather than imported infrastructure.
