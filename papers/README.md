# Downloaded Papers

All 12 PDFs were downloaded from arXiv, opened successfully with `pypdf`, split into three-page chunks under `papers/pages/`, and read end-to-end. Per-chunk findings are in `deep_read_notes.md`.

1. **Can You Keep a Secret? Involuntary Information Leakage in Language Model Writing** — Ari Holtzman and Peter West (2026), [arXiv:2605.10794](https://arxiv.org/abs/2605.10794). [PDF](2605.10794_keep_a_secret.pdf). Primary behavioral result: literal compliance coexists with thematic story leakage; active hiding creates detectable inversion and decoys redirect leakage.
2. **Inadvertent Context Leakage in Language Models** — Jaiden Fairoze, Neal Mangaokar, Kamalika Chaudhuri, Sanjam Garg, and Saeed Mahloujifar (2026), [arXiv:2608.19857](https://arxiv.org/abs/2608.19857). [PDF](2608.19857_inadvertent_context_leakage.pdf). Direct follow-up: per-model black-box decoders recover protected context from benign output statistics; suppression is proposed as the mechanism.
3. **Does Liking Yellow Imply Driving a School Bus? Semantic Leakage in Language Models** — Hila Gonen, Terra Blevins, Alisa Liu, Luke Zettlemoyer, and Noah A. Smith (2025), [arXiv:2408.06518](https://arxiv.org/abs/2408.06518). [PDF](2408.06518_semantic_leakage.pdf). Establishes matched test/control semantic leakage and human validation across models, languages, and stories.
4. **Towards Eliciting Latent Knowledge from LLMs with Mechanistic Interpretability** — Bartosz Cywiński, Emil Ryd, Senthooran Rajamanoharan, and Neel Nanda (2025), [arXiv:2505.14352](https://arxiv.org/abs/2505.14352). [PDF](2505.14352_latent_knowledge_mech_interp.pdf). Shows Taboo secrets are recoverable with black-box guesses, logit lens, and SAE features.
5. **Eliciting Secret Knowledge from Language Models** — Bartosz Cywiński, Emil Ryd, Rowan Wang, Senthooran Rajamanoharan, Neel Nanda, Arthur Conmy, and Samuel Marks (2025), [arXiv:2510.01070](https://arxiv.org/abs/2510.01070). [PDF](2510.01070_eliciting_secret_knowledge.pdf). Larger public benchmark for black- and white-box secret elicitation across three model organisms.
6. **Emergent Response Planning in LLMs** — Zhichen Dong, Zhanhui Zhou, Zhixuan Liu, Chao Yang, and Chaochao Lu (2025), [arXiv:2502.06258](https://arxiv.org/abs/2502.06258). [PDF](2502.06258_emergent_response_planning.pdf). Demonstrates future response attributes can be decoded from residual activations before generation; explicitly correlational.
7. **Do Language Models Plan Ahead for Future Tokens?** — Wilson Wu, John X. Morris, and Lionel Levine (2024), [arXiv:2404.00859](https://arxiv.org/abs/2404.00859). [PDF](2404.00859_plan_ahead.pdf). Myopic training distinguishes deliberate pre-caching from ordinary semantic breadcrumbs.
8. **Creating Suspenseful Stories: Iterative Planning with Large Language Models** — Kaige Xie and Mark Riedl (2024), [arXiv:2402.17119](https://arxiv.org/abs/2402.17119). [PDF](2402.17119_suspenseful_stories.pdf). Strong precedent for separating iterative plot planning from prose elaboration and measuring narrative utility.
9. **Don't Think of the White Bear: Ironic Negation in Transformer Models Under Cognitive Load** — Logan Mann, Nayan Saxena, Sarah Tandon, Chenhao Sun, Savar Toteja, and Kevin Zhu (2025), [arXiv:2511.12381](https://arxiv.org/abs/2511.12381). [PDF](2511.12381_white_bear_rebound.pdf). Measures forbidden-token rebound and provides a narrow attention-head ablation mechanism.
10. **Can LLMs Keep a Secret? Testing Privacy Implications of Language Models via Contextual Integrity Theory** — Niloofar Mireshghallah et al. (2023), [arXiv:2310.17884](https://arxiv.org/abs/2310.17884). [PDF](2310.17884_confaide.pdf). ConfAIde benchmark for direct contextual disclosure and privacy–utility evaluation.
11. **LLMs Can't Play Hangman: On the Necessity of a Private Working Memory for Language Agents** — Davide Baldelli, Ali Parviz, Amal Zouaq, and Sarath Chandar (2026), [arXiv:2601.06973](https://arxiv.org/abs/2601.06973). [PDF](2601.06973_private_working_memory.pdf). Proves limits of persistent private state in a public transcript and evaluates explicit private-memory workflows.
12. **Probing the Lack of Stable Internal Beliefs in LLMs** — Yifan Luo, Kangping Xu, Yanzhen Lu, Yang Yuan, and Andrew Chi-Chih Yao (2026), [arXiv:2603.25187](https://arxiv.org/abs/2603.25187). [PDF](2603.25187_stable_internal_beliefs.pdf). Behavioral branch probes reveal target drift and motivate multiple measures of secret accessibility.

## Integrity Check

| arXiv ID | Pages | Bytes |
|---|---:|---:|
| 2310.17884 | 24 | 4,110,097 |
| 2402.17119 | 17 | 470,394 |
| 2404.00859 | 24 | 1,714,032 |
| 2408.06518 | 14 | 431,173 |
| 2502.06258 | 20 | 1,879,853 |
| 2505.14352 | 19 | 1,014,047 |
| 2510.01070 | 55 | 3,374,076 |
| 2511.12381 | 12 | 4,432,933 |
| 2601.06973 | 36 | 1,416,702 |
| 2603.25187 | 17 | 993,889 |
| 2605.10794 | 18 | 1,219,804 |
| 2608.19857 | 24 | 764,308 |
