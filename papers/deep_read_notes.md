# Deep-reading notes

All user-specified papers were split into three-page chunks. Notes below record the sequential full-text pass; chunk manifests are in `papers/pages/`.

## 2605.10794 — Can You Keep a Secret?

- Chunks 1–2 (pp. 1–6): Writer–guesser design with 15 curated secrets, four text tasks, five prompt conditions, free-response guessing and order-balanced 2AFC. Literal leakage was absent, but thematic leakage reached 79.3%. Active hiding often inverted the signal rather than eliminating it.
- Chunks 3–4 (pp. 7–12): Cross-model transfer supports a text-level signal; within-family scaling jumps around 12B+; short stock jokes are a negative-control task, while long-form stories/jokes/essays leak. User-prompt placement changes some model behavior. A decoy concept redirects part, not all, of the signal. Limitations include single-word toy secrets, API model drift, model-as-judge dependence, and limited mechanistic evidence.
- Chunks 5–6 (pp. 13–18): Exact prompts, binomial tests with FDR/Bonferroni corrections, qualitative examples, alternate COCA/model-chosen word sets, position-bias controls, and deterministic decoy pairings. Recommended reproduction controls: both presentation orders, no-secret baselines, literal-secret filtering, fixed pairings/seeds, and separate free-response from discrimination outcomes.

Actionable implication: the natural behavioral extension is a preregistered factorial test of `no plan / secret-free plan / secret-aware plan`, with plan content held fixed where possible. The key mechanistic prediction is that a plan should reduce leakage only if it reduces secret decodability in generation-time residual states.

## 2505.14352 — Towards eliciting latent knowledge from LLMs with mechanistic interpretability

- Chunks 1–2 (pp. 1–6): Twenty Gemma-2-9B QLoRA “Taboo” models each internalize a one-token secret absent from their prompts/training strings, using 3–5-turn synthetic hint dialogues. Black-box baselines include naive/adversarial prompting, prefill token forcing, and an external guesser. White-box methods average layer-32 logit-lens probabilities or rank Gemma Scope SAE features over response positions.
- Chunk 2 results: another-model guessing gives 95% Pass@10; post-game token forcing 70%; logit lens top-5 75%; SAE top-5 55%. Naive prompting is 0%. The SAE evaluation is not fully discovery-free: secret-to-latent mappings are manually identified, while logit lens is advantaged by single-token targets.
- Chunks 3–7 (pp. 7–19): Complete synthetic-data prompts, validation rules, QLoRA hyperparameters (rank 8, 10 epochs, batch 8, LR 2e-4, A100), rollout examples, attack prompts, token-forcing protocol, manually curated SAE mappings, and per-token activation plots. Limitations: simple organism, only 20 common one-token secrets, model outputs deliberately describe the secret, and no causal intervention.

Actionable implication: use layerwise linear probes as the primary low-cost internal-state measure; reserve SAE/logit-lens ranking as secondary analyses. Add activation steering/erasure with matched random-direction controls to establish causal rather than merely decodable secret representations.

## 2510.01070 — Eliciting Secret Knowledge from Language Models

- Chunks 1–4 (pp. 1–12): Three model-organism families: Gemma-2-9B Taboo words, Llama-3.3-70B Base64 secret side constraints, and Gemma-2-9B inferred user gender. Training mixes 10× unrelated Alpaca turns to reduce artificial fine-tuning traces. Auditing compares adversarial prompting, assistant prefills, user-persona sampling, many-shot jailbreaks, activation fuzzing, logit lens, activation–embedding similarity, and SAE descriptions/tokens.
- Core results: on standard prompts, white-box information improves auditing in most settings (e.g. Taboo I/O 42.1% versus activation tokens 85.1%; user-gender I/O 51.8% versus SAE descriptions 85.4%). On direct prompts, assistant prefill/user-persona attacks exceed 95% for side-constraint and gender models, but remain weak for Taboo. Fuzzing/high temperature/many-shot attacks are mostly ineffective. Untuned-base controls generally remove the white-box gains.
- Chunks 5–8 (pp. 13–24): LoRA and dataset details, internalization evaluations, held-out standard/direct prompt sets, and detailed score tables. The benchmark uses smaller auditors and GPT-4/4.1 judges; SSC evaluation is semantic similarity over five guesses rather than exact recovery.
- Chunks 9–15 (pp. 25–45): Layer/token-position choices are model-specific and tuned on validation: assistant control tokens for Taboo, Base64 spans for SSC, first-person pronouns for gender. Prefill results are highly prefix-sensitive. A multilingual prefill bypass reveals that Taboo suppresses an English token more than the underlying concept. Multi-stage auditor pipelines filter large white-box readouts, creating extra modeling choices.
- Chunks 16–19 (pp. 46–55): Raw readouts show decoded constraint words near completion of their Base64 spans and strongest secret signals at assistant control tokens. SAE coverage and description quality limit recovery; activation–embedding tokens can be noisy or surface both genders. The paper explicitly notes simple organisms, single SFT acquisition, easy multi-turn behavioral inference, and lack of organically learned secrets.

Actionable implication: probe the secret across prompt, outline, and generation positions; include base-model/random-direction controls; and test causal removal at the same positions. Do not infer causality from probe accuracy alone, and avoid selecting intervention layers on the final test set.

## 2601.06973 — LLMs Can't Play Hangman

- Chunks 1–2 (pp. 1–6): Defines Private State Interactive Tasks and proves that a public-only chat policy cannot guarantee both public underdetermination and consistency with a fixed privately generated secret. The theorem concerns persistence across turns, not one-shot thematic leakage.
- Chunks 3–4 (pp. 7–12): Forked self-consistency testing on Hangman and a DDXPlus diagnosis simulator. Across 50 episodes per condition, vanilla and retrieval-memory agents score poorly; explicit private-state workflows often reach 90–100%, while private chain-of-thought is a costly upper bound. Workflow updates outperform autonomous tool choice; explicit memory remains mostly under 100 tokens versus roughly 10× larger private-CoT context.
- Chunks 5–8 (pp. 13–24): Related work, structured working-memory design, qualitative memory snapshots, model/secret distributions, and robustness discussion. Retrieval systems preserve public utterances but omit the self-generated secret; overwrite/patch memory explicitly retains it.
- Chunks 9–12 (pp. 25–36): Fork-point ablations preserve method ordering; complete task/agent prompts and memory tool schemas are provided. Key limitations for this project: the theorem does not imply that an external outline reduces one-turn leakage, and explicit private memory may actually preserve secret activation rather than suppress it.

Actionable implication: distinguish `external plan` (public conditioning text) from `private persistent state`. The present hypothesis is about whether an outline offloads anticipatory generation, not whether a memory channel can remember a secret across turns.

## 2603.25187 — Probing the Lack of Stable Internal Beliefs in LLMs

- Chunks 1–2 (pp. 1–6): In number/entity 20-questions games, branch probes ask for the selected target index after every turn. Reported once-drift is typically near 100%, while per-turn drift ranges roughly 11–100%; reasoning can worsen latent drift even while improving visible consistency. Qwen-2.5-14B fine-tuning with a KL-to-initial-belief loss reduces drift more than CE alone.
- Chunks 3–6 (pp. 7–17): Appendices specify prompts, supplementary drift/KL metrics, training/evaluation details, broader impacts, and checklist. Main caveat: the “internal belief” is inferred through an explicit behavioral probe distribution, not a trained activation probe, and the branch question can measure answer instability rather than a causally persistent hidden state.

Actionable implication: for this project, measure the secret with both behavioral counterfactual probes and activation probes. Treat either alone as evidence of accessibility, not proof of a stable belief.

## 2511.12381 — Don't Think of the White Bear

- Chunks 1–2 (pp. 1–6): ReboundBench has about 5,000 templated English prompts with single-token forbidden nouns, three distractor types, and lengths to 1,024 tokens. It evaluates forbidden-token log probability, not generated-text leakage. Semantic distractors generally produce stronger/more persistent rebound; repetition usually supports suppression. Head ablations on Llama-3-8B-Instruct attribute much of the effect to a sparse set of middle-layer heads.
- Chunks 3–4 (pp. 7–12): Dataset construction, mixed/robust regression tables, model-specific peak/AUC/L50 results, limitations, and attention-head details. Important reservations: high-load values define the baseline used to call lower-load effects “rebound”; actual narrative generation and multi-token concepts are untested; head-ablation causality is narrow and only detailed for one model.

Actionable implication: include positive/decoy framing and secret-omission controls, because a literal “do not mention X” condition may create the very activation being measured. Use story-level discrimination as the primary outcome and next-token rebound only as a supporting mechanism measure.

## 2310.17884 — ConfAIde

- Chunks 1–3 (pp. 1–9): Four tiers progress from sensitivity ratings to contextual vignettes, theory-of-mind secret sharing, and meeting summaries/action items. Tier 3 uses 270 synthetic scenarios; Tier 4 uses 20 transcripts. GPT-4 leaks in 22% of Tier-3 generations and inappropriate information flows occur in 39% of Tier-4 summaries; ChatGPT rates are substantially higher. Explicit privacy prompts help but do not solve leakage.
- Main mitigation result: a simple chain-of-thought prompt slightly worsens leakage and utility. Manual error analysis finds many chains acknowledge privacy but fail to operationalize it, or falsely assume the recipient already knows the secret.
- Chunks 4–8 (pp. 10–24): References, exact factor sets/prompts, annotation details, metric tables, and context breakdowns. Inter-annotator Krippendorff alpha is low (0.07–0.34), emphasizing norm ambiguity. Leakage is direct contextual disclosure, distinct from the involuntary thematic channel in the target hypothesis.

Actionable implication: retain a clear utility–privacy tradeoff metric. An outline that suppresses all secret-adjacent content could lower leakage while degrading narrative quality or coherence, so both must be measured.

## 2502.06258 — Emergent Response Planning in LLMs

- Chunks 1–2 (pp. 1–6): One-hidden-layer MLP probes predict six future response attributes from prompt-end residual states: length, reasoning steps, animal character, final MCQ answer, answer correctness, and factual consistency. Results generalize across paired datasets and exceed class/random baselines for eight 7–8B base/instruction models.
- Chunks 3–4 (pp. 7–12): Planning decodability scales within model families, follows a high–low–high trajectory over generation, and substantially exceeds models’ verbalized self-predictions. Authors explicitly acknowledge that probes establish correlation, not causal influence, and greedy decoding removes sampling uncertainty.
- Chunks 5–7 (pp. 13–20): Exact models/datasets, prompts, filtering/augmentation, representation collection, and full regression plots. The character task is especially relevant but only predicts one of the four most frequent animals after balancing/filtering; prompt features may still contain predictive correlations.

Actionable implication: model the proposed mechanism as mediation: `outline condition → lower secret decodability during prose generation → lower story leakage`. Pre-register prompt-end and tokenwise probe locations, and add causal erasure because response-planning decodability alone is insufficient.

## 2404.00859 — Do Language Models Plan Ahead for Future Tokens?

- Chunks 1–3 (pp. 1–9): Separates deliberate “pre-caching” from “breadcrumbs” that are useful now and later. Myopic training removes off-diagonal future-loss gradients. Synthetic tasks show strong necessary pre-caching; GPT-2 natural-language loss shows a small myopia gap (3.40 versus 3.28) and near-zero local myopia bonus, favoring breadcrumbs at small scale.
- Chunks 4–5 (pp. 10–15): Pythia 14M–2.8B results suggest the vanilla–myopic gap grows with scale. Discussion, references, and formal decomposition clarify that future-token decodability is not by itself deliberate planning.
- Chunks 6–8 (pp. 16–24): Convergence assumptions/proofs, architecture/training details, multiplication/filler-token experiments, and gradient analysis. Natural-language experiments use short 64-token contexts and models at most 2.8B, limiting direct transfer to frontier story generation.

Actionable implication: the outline hypothesis has two competing mechanisms: it may reduce deliberate pre-caching, or it may leave semantic breadcrumbs unchanged. A successful experiment must measure both behavior and the temporal profile of secret representations.

## 2402.17119 — Suspenseful Story Generation by Iteratively Refining a Plot

- Chunks 1–2 (pp. 1–6): The method first generates a background, then iteratively constructs action–failure pairs that make the protagonist's goal progressively less likely, and finally elaborates details that plant clues while delaying their explanation. This explicit separation of plot construction from prose realization is the closest methodological precedent for testing whether an external plan reduces anticipatory leakage.
- Chunks 3–4 (pp. 7–12): Human pairwise evaluation strongly favors the full pipeline over direct ChatGPT generation for suspense (84.9%), novelty (76.6%), and enjoyment (67.9%). Logical consistency is 49.2% versus 27.8%, with naturalness mostly tied. It also beats Llama-2 and Re3 baselines on suspense. Ablations show that both iterative outlining and detail elaboration contribute.
- Chunks 5–6 (pp. 13–17): Outline diagnostics find 96.5% action relevance, 89.8% plausible failures, but only 55.1% of consecutive steps clearly decrease goal likelihood. Planted clues improve suspense judgments (57.9% versus 10.9%); information-timing gains are not significant. Appendices provide generation and evaluation prompts, examples, and annotator instructions.

Actionable implication: reuse the plan/prose separation, but independently control whether the outline is secret-blind or secret-aware. Otherwise an apparent benefit of planning could merely reflect changing how often the model is exposed to the secret.

## 2408.06518 — Does Liking Yellow Imply Driving a School Bus?

- Chunks 1–2 (pp. 1–6): Defines semantic leakage as an unrelated prompt concept exerting excess semantic influence on a completion. The 109 paired test/control prompts cover colors, food, animals, names, music, occupations, and idioms. Leak-Rate is the fraction for which a test completion is closer to the concept than its matched control under BERTScore, Sentence-BERT, or OpenAI embeddings. Across 13 GPT/Llama variants and four temperatures, all models exceed the 50% null; instruction-tuned variants generally leak more.
- Chunks 3–5 (pp. 7–14): Human leakage judgments reach 71.8% on a validation subset (inter-annotator Kendall tau 0.68), while automatic metrics range 70.5–84.9%. Leakage persists in Hebrew, Chinese, cross-lingual prompts, stories, and recipes. A 23-name story test yields 60.9–78.7% depending on embedding metric. The test set is small and handcrafted, automatic scores can confound prompt repetition, and the work tests association rather than secrecy or causal mechanisms.

Actionable implication: use matched secret/no-secret outputs and blinded 2AFC judgments as the primary leakage measure; embedding similarity is a useful secondary metric but should not stand alone.

## 2608.19857 — Inadvertent Context Leakage in Language Models

- Chunks 1–3 (pp. 1–9): Formalizes black-box predicate inference from benign outputs conditioned on protected in-context data. Per-model decoders trained on self-authored contexts reconstruct two-digit secrets perfectly for some frontier models and four-digit secrets at up to 82% exact match; randomized-label controls remain at chance. A semantic-memory experiment improves advantage over a model-agnostic linguistic judge (0.319 versus 0.058). An active prompt-injection attack additionally extracts SSNs, but that is a distinct, stronger threat model.
- Chunks 4–8 (pp. 10–24): Proposes suppression-induced probability redistribution as the passive mechanism. Suppression and leakage correlate across eight models (Spearman rho 0.95), though the small sample and tier separation drive the result. More emphatic confidentiality instructions can increase leakage; co-present distractors stay at chance while the protected value is recoverable. Appendices detail LoRA decoders, shuffled-label controls, instruction transfer, digit-stripped length/style/embedding channels, costs, and limitations. The study is black-box, primarily numeric, and does not test free-text story plans or representation-level interventions.

Actionable implication: include a secret-free control and an active-hiding condition, test classifiers on held-out secrets rather than only held-out generations, and distinguish passive prose leakage from an optimized adversarial exfiltration channel.
