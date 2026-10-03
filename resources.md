# Resources Catalog

## Summary

This workspace contains 12 validated papers, three locally available dataset collections, and five official research repositories. The resources support a behavioral story-outline experiment, activation mediation analysis, and causal representation intervention.

## Papers

Total PDFs: **12**. Every PDF was parsed successfully and read in full from three-page chunks. See `papers/README.md` and `papers/deep_read_notes.md`.

| Paper | Year | File | Key information |
|---|---:|---|---|
| Holtzman & West, *Can You Keep a Secret?* | 2026 | `papers/2605.10794_keep_a_secret.pdf` | Primary thematic story-leakage benchmark |
| Fairoze et al., *Inadvertent Context Leakage* | 2026 | `papers/2608.19857_inadvertent_context_leakage.pdf` | Adaptive black-box leakage and suppression mechanism |
| Gonen et al., *Semantic Leakage* | 2025 | `papers/2408.06518_semantic_leakage.pdf` | Matched control metric and human validation |
| Cywiński et al., *Towards Eliciting Latent Knowledge* | 2025 | `papers/2505.14352_latent_knowledge_mech_interp.pdf` | Logit-lens and SAE secret elicitation |
| Cywiński et al., *Eliciting Secret Knowledge* | 2025 | `papers/2510.01070_eliciting_secret_knowledge.pdf` | Expanded public secret-elicitation benchmark |
| Dong et al., *Emergent Response Planning* | 2025 | `papers/2502.06258_emergent_response_planning.pdf` | Future-property activation probes |
| Wu et al., *Plan Ahead for Future Tokens?* | 2024 | `papers/2404.00859_plan_ahead.pdf` | Myopic training and pre-caching/breadcrumb distinction |
| Xie & Riedl, *Creating Suspenseful Stories* | 2024 | `papers/2402.17119_suspenseful_stories.pdf` | Explicit plot/prose separation and narrative evaluation |
| Mann et al., *White Bear* | 2025 | `papers/2511.12381_white_bear_rebound.pdf` | Rebound benchmark and attention-head ablation |
| Mireshghallah et al., *ConfAIde* | 2023 | `papers/2310.17884_confaide.pdf` | Direct privacy leakage and utility benchmark |
| Baldelli et al., *Private Working Memory* | 2026 | `papers/2601.06973_private_working_memory.pdf` | Boundary case: persistent private state |
| Luo et al., *Stable Internal Beliefs* | 2026 | `papers/2603.25187_stable_internal_beliefs.pdf` | Behavioral probes and belief drift |

## Datasets

Total downloaded collections: **3**. Data files are present locally but excluded from Git; exact re-download commands and schemas are in `datasets/README.md`.

| Name | Source | Size | Task | Location | Notes |
|---|---|---:|---|---|---|
| Semantic Leakage Prompt Suite | [author-hosted](https://gonenhila.github.io/files/semantic_leakage_prompts.txt) | 140 lines / 10.6 KB | Matched semantic completion | `datasets/semantic_leakage/` | 109 paper examples organized as prompt variants |
| ConfAIde | [GitHub](https://github.com/skywalker023/confaide/tree/main/benchmark) | 510 KB across 8 files | Contextual privacy | `datasets/confaide/` | Tiers 1–4, labels, controls, transcripts |
| ReboundBench | [GitHub](https://github.com/cesium132dot9/Dont-Think-of-the-White-Bear/tree/main/data) | 5,500 CSV rows / 634 KB | Negation/rebound | `datasets/reboundbench/` | 5,000 primary and 500 matched multi-question records |

## Code Repositories

Total repositories: **5**. All are shallow clones at recorded commits and pass Python bytecode compilation. See `code/README.md` for requirements and entry points.

| Name | URL | Purpose | Location | Status |
|---|---|---|---|---|
| ConfAIde | [GitHub](https://github.com/skywalker023/confaide) | Privacy benchmark/evaluators | `code/confaide/` | Compiles; API/model execution not attempted |
| Emergent Response Planning | [GitHub](https://github.com/niconi19/Emergent-Response-Planning-in-LLMs) | Residual collection and probes | `code/response-planning/` | Compiles; needs models/GPU |
| Eliciting Secrets | [GitHub](https://github.com/EmilRyd/eliciting-secrets) | Secret model organisms, logit lens, SAE | `code/eliciting-secrets/` | Compiles; needs heavyweight ML stack/GPU |
| White Bear | [GitHub](https://github.com/cesium132dot9/Dont-Think-of-the-White-Bear) | Rebound and head ablations | `code/white-bear/` | Compiles; datasets load |
| FutureGPT2 | [GitHub](https://github.com/wiwu2390/FutureGPT2-public) | Myopic/future-token training | `code/futuregpt2/` | Compiles; no pinned environment |

## Resource Gathering Notes

### Search Strategy

The required paper-finder service was tried first in diligent mode after installing its missing `httpx` dependency. The service returned HTTP 500 twice, leaving two empty diagnostic JSONL files under `paper_search_results/`. The fallback search used arXiv metadata/API, the ten user-provided arXiv identifiers, forward/related-paper web search, reference lists, author pages, GitHub, and Hugging Face links. Search concepts included *involuntary information leakage*, *semantic leakage*, *secret elicitation*, *response planning activations*, *future-token planning*, *ironic negation/rebound*, *contextual privacy*, and *story outline planning*.

Two high-relevance papers not in the original list were added: Gonen et al. (semantic leakage) and Fairoze et al. (inadvertent context leakage). The latter appeared after the primary May 2026 paper and directly strengthens the suppression-mechanism evidence.

### Selection Criteria

Resources were retained when they directly measured nonliteral secret influence, supplied a mechanism/probe/intervention, separated planning from prose, or provided a reusable benchmark/codebase. Preference went to official arXiv PDFs and author repositories with data. Generic prompt-injection, training-data memorization, and broad privacy surveys were excluded because they do not isolate involuntary thematic leakage.

### Challenges and Workarounds

- Paper-finder was unavailable server-side; manual multi-source search and arXiv API metadata replaced it.
- The primary Holtzman–West v1 paper says code is redacted for review and the arXiv record exposes no official repository. Its prompt design and analyses were reconstructed from the paper, but no unofficial substitute was cloned.
- Several repositories require large model weights, credentials, or GPUs. Validation was limited to source/README inspection, data loading, commit pinning, and compilation.
- ReboundBench's README claims MIT but the cloned snapshot lacks a root license file; its downloaded data should be treated as research-only until clarified.
- No established dataset crosses secrets, story briefs, and outline provenance. The primary dataset must therefore be generated, with existing resources used as concept seeds and transfer evaluations.

## Recommendations for Experiment Design

1. **Primary data:** Generate a crossed story corpus from 30–50 screened secrets and at least eight reusable briefs, with no-outline, secret-blind outline, secret-aware outline, self-outline, decoy, and no-secret conditions.
2. **Behavioral baseline:** Reproduce Holtzman–West order-balanced 2AFC leakage before adding outlines. Include exact/free guesses and no-secret controls.
3. **Mechanism code:** Adapt `code/response-planning/` for tokenwise residual collection, then borrow secret configurations from `code/eliciting-secrets/`.
4. **Causal tests:** Add projection removal/steering with norm-matched random and unrelated-concept controls. White Bear provides a useful ablation template, but its forbidden-token metric should remain secondary.
5. **Utility:** Score plan adherence, coherence, suspense, length, diversity, and refusal. ConfAIde can supply a separate privacy/utility transfer check.
6. **Statistics:** Split by secret identity, use mixed-effects logistic models, preregister layer/time regions or correct multiple comparisons, and report uncertainty/effect sizes.

## Executed Research Artifacts (2026-10-03)

The experiment runner used local Gemma 3 12B and Qwen3-14B checkpoints on an RTX A6000. Raw stories/judgments are in `results/model_outputs/`, processed statistics in `results/evaluations/`, figures in `figures/`, and executable pipelines in `src/`. `REPORT.md` documents API failures, excluded judge pilots, actual results, and limitations.

The final three-direction ranking and rejected alternatives are recorded in `planning.md`.
