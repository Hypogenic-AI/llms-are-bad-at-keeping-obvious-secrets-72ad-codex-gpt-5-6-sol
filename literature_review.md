# Literature Review

## Review Scope

**Research question.** When an LLM writes while holding a secret it must not reveal, does an explicit outline reduce nonliteral leakage, and is any reduction mediated by—then causally dependent on—the secret's internal representation during prose generation?

**Inclusion criteria.** English-language work from 2023–2026 was included if it (a) measures unintended semantic/contextual influence on generation, (b) probes or intervenes on latent secret/future-response information, (c) separates narrative planning from realization, or (d) provides a directly reusable privacy/rebound benchmark. All ten user-specified papers were mandatory.

**Exclusion criteria.** Training-data memorization, ordinary jailbreak/prompt extraction, generic privacy surveys, and planning papers without measurable generation-state or story relevance were excluded. Closely duplicative follow-ups were screened out when they added neither a new mechanism nor reusable resource.

**Sources.** Paper-finder was attempted first, followed by arXiv/API search, author and GitHub pages, reference chasing, and targeted web search across Semantic Scholar/Papers with Code/Google Scholar discovery surfaces. Official paper and repository pages were used for final metadata.

## Search Log

| Date | Query/source | Result | Decision |
|---|---|---|---|
| 2026-10-03 | Paper-finder diligent: “large language models secret leakage fiction foreshadowing outline planning generation” | HTTP 500 twice; 0 returned | Recorded failure; manual fallback |
| 2026-10-03 | Ten supplied arXiv IDs via arXiv API | 10 records | All included and full-text screened |
| 2026-10-03 | “semantic leakage language models” / arXiv and web | Gonen et al. plus a small-model follow-up | Included foundational Gonen et al.; excluded redundant scaling follow-up |
| 2026-10-03 | “inadvertent context leakage language models” / recent arXiv | Fairoze et al. (August 2026) | Included; direct post-specification evidence |
| 2026-10-03 | Paper references and “response planning activations”, “ironic negation”, “story iterative planning” | Probe, rebound, and narrative-planning lines | Relevant papers already covered by supplied set; official code located |

## Screening Results

| Group | Title | Abstract | Full text | Outcome |
|---|---|---|---|---|
| 10 supplied papers | Include | Include | Include | Mandatory and directly/adjacently relevant |
| Gonen et al., semantic leakage | Include | Include | Include | Added as foundational behavioral baseline |
| Fairoze et al., inadvertent context leakage | Include | Include | Include | Added as closest new mechanism/threat-model result |
| Smilga, *Scaling Down Semantic Leakage* | Maybe | Include | Not required | Excluded: primarily repeats size comparison; low marginal information for outline mechanism |
| Prompt injection/training-data extraction literature | Maybe | Exclude | — | Different threat model: deliberate extraction or memorization |
| General story-generation/planning surveys | Maybe | Exclude | — | No secret-leakage or internal-state test |

## Research Area Overview

The target phenomenon is narrower than ordinary prompt extraction or direct privacy failure. A model can obey the literal instruction not to say a secret while allowing that secret to influence topic, imagery, wording, length, or other output statistics. Three adjacent literatures converge on this problem: behavioral semantic leakage, latent-knowledge/response-planning probes, and narrative planning. Together they support the hypothesis that a secret may remain active throughout generation, but they do not yet test whether an external outline reduces leakage by offloading future preparation, nor whether causally removing the secret representation removes the leak.

Holtzman and West (2026) provide the closest behavioral result. They give models a secret word, ask them not to reveal it, and use another model in an order-balanced binary discrimination task to infer the secret from stories. The secret never appears literally, yet five frontier models leak thematically at rates up to 79.3%. Stronger “actively hide it” instructions reverse the signal below chance because systematic avoidance is itself diagnostic; a decoy redirects some signal. Leakage disappears in short stock jokes, implicating open-ended content choice rather than inevitable token copying. The paper does not manipulate story planning or model internals.

Gonen et al. (2025) establish the broader category of semantic leakage: unrelated prompt concepts affect completions more than matched controls. Their 109-example suite yields significant leakage in 13 GPT/Llama variants and in multilingual, cross-lingual, story, and recipe settings. Human agreement is high enough to validate the effect, while embedding metrics only moderately track item-level judgments. This motivates matched controls and human/model 2AFC evaluation, but it does not involve an instruction to keep a secret.

Fairoze et al. (2026), published after the primary story-leakage paper, show that benign outputs can encode protected in-context values through model-specific statistical channels. Adaptive black-box decoders recover two-digit secrets perfectly for some models and four-digit secrets at 82% exact match. The authors propose suppression-induced probability redistribution: a model avoids the protected value, producing a value-dependent output distribution. Suppression correlates with leakage across eight models (rho 0.95), and more emphatic confidentiality instructions can worsen recovery. This is strong evidence that “trying not to say X” can preserve or amplify an X-dependent channel, though the main controlled task is numeric and adversarial decoding is trained per model.

## Key Papers

### Behavioral Leakage and Privacy

**Holtzman & West (2026), “Can You Keep a Secret?”** The study crosses 15 secrets with story, essay, and joke tasks under secret-present, no-secret, active-hiding, and decoy controls. Leakage is scored through blinded 2AFC discrimination with both candidate orders, binomial testing, and multiple-comparison correction. Cross-model judge transfer and within-family scaling argue against a single evaluator artifact. Key limitations are a small secret set, reliance on model judges, and no released code link in the inspected v1 PDF. It defines the primary behavioral endpoint for this project.

**Mireshghallah et al. (2023), ConfAIde.** Four tiers move from sensitivity ratings to contextual norms, theory-of-mind sharing, and meeting summaries. Tier 3 contains 270 synthetic scenarios and Tier 4 contains 20 transcripts. GPT-4 leaks in 22% of Tier-3 generations and produces inappropriate flows in 39% of Tier-4 summaries; a chain-of-thought prompt slightly worsens both leakage and utility. Low annotation agreement on some norm judgments (Krippendorff alpha 0.07–0.34) warns that privacy evaluation can be subjective. ConfAIde is best used as a transfer and utility benchmark, since it measures explicit contextual disclosure rather than subtle thematic influence.

**Mann et al. (2025), White Bear.** ReboundBench has 5,000 templated negation prompts plus 500 matched multi-question prompts. It measures forbidden-token log probability after semantic, syntactic, or repetitive distractors. Semantic load generally strengthens rebound, while repetition can support suppression. Attention-head ablations on Llama-3-8B-Instruct suggest a sparse middle-layer contribution. The outcome is next-token salience, not story leakage, and the causal result is narrow; the matched positive/neutral/negative controls remain valuable.

**Fairoze et al. (2026), Inadvertent Context Leakage.** Six decoder strategies combine frequency statistics and Qwen LoRA classifiers, with shuffled-label controls. The work also tests digit-stripped length/style/embedding channels, confidentiality wording, co-present distractors, and semantic predicates over user memories. It provides a strong threat-model and split discipline, but trained adaptive attackers answer a different question from ordinary reader-perceived foreshadowing. Its main lesson is to evaluate suppression and active hiding as potentially informative channels, not merely mitigations.

### Internal State, Secret Elicitation, and Planning

**Cywiński et al. (2025), latent knowledge.** Gemma-2-9B models are QLoRA-trained to play Taboo while hiding one of 20 single-token secrets. An external model reaches 95% Pass@10 guessing, postgame token forcing reaches 70%, final-layer logit lens reaches 75% top-5, and Gemma Scope SAE features reach 55% top-5. These results demonstrate accessible secret information but rely on a small, fine-tuned model organism and manually mapped SAE features.

**Cywiński et al. (2025), Eliciting Secret Knowledge.** The expanded benchmark uses three model-organism families: Taboo, secret-selection/concealment, and user-gender knowledge. Prefill attacks often exceed 95% on the latter two settings; logit-lens and SAE methods consistently beat input/output baselines but are weaker. For Taboo, activation-token elicitation reaches 85.1% versus 42.1% for ordinary input/output elicitation. This establishes methods and controls for locating secret representations, but it asks whether knowledge is recoverable, not whether it causally shapes prose.

**Dong et al. (2025), Emergent Response Planning.** Linear/MLP probes predict response length, reasoning steps, final answers, correctness, consistency, and animal characters from prompt-end residual states across eight 7–8B models. Decodability scales and often follows a high–low–high temporal trajectory. Greedy decoding and prompt correlations limit causal interpretation. For this project the important contribution is the reusable activation-collection/probing pipeline and the explicit warning that decodability alone is correlational.

**Wu et al. (2024), FutureGPT2.** Myopic training removes gradients from future-token losses to earlier computations. Synthetic tasks show necessary “pre-caching,” whereas small-model natural-language results show only a modest myopia gap and near-zero local bonus, consistent with semantic breadcrumbs rather than deliberate plans. The gap grows with Pythia scale up to 2.8B. Thus an outline might reduce deliberate pre-caching without removing ordinary associative breadcrumbs; behavioral and activation measurements must be collected together.

**Luo et al. (2026), Stable Internal Beliefs.** Branch probes during 20-questions games find that once a target belief drifts it nearly always remains drifted, and KL-to-initial-belief fine-tuning reduces drift. The “internal belief” is inferred behaviorally, so instability may partly reflect the probe response. This motivates measuring the secret with both activation probes and behavioral counterfactuals.

**Baldelli et al. (2026), Private Working Memory.** A formal result shows that a persistent private state cannot be guaranteed when all durable state is exposed through a public transcript. Hangman and diagnostic tasks improve with explicit private-memory channels. This is relevant boundary-setting: private state solves a multi-turn memory architecture problem, while the present question concerns offloading prose planning into a public outline.

### Narrative Planning

**Xie & Riedl (2024), Suspenseful Stories.** Their pipeline separates background generation, iterative action–failure plotting, and detail elaboration with planted clues and delayed explanations. Human evaluation favors the full method over direct ChatGPT generation for suspense (84.9%), novelty (76.6%), and enjoyment (67.9%), while ablations show both outline and detail stages matter. This is direct evidence that plan/prose separation changes narrative behavior. However, every stage is model-generated; it does not independently manipulate what information the plan contains. The proposed experiment therefore needs secret-blind, secret-aware, and self-generated outlines.

## Common Methodologies and Baselines

The literature suggests four complementary measurement families:

- **Matched behavioral controls:** secret-present versus no-secret, ordinary suppression versus active hiding, and real-secret versus decoy. Hold story brief, length target, model, and decoding settings fixed.
- **Blinded discrimination:** order-balanced 2AFC inference is more sensitive than literal-string checks and avoids requiring an exhaustive paraphrase ontology. Exact/free guesses add ecological validity.
- **Representation probes:** collect residual streams at prompt end and throughout generation, use simple preregistered classifiers, evaluate on held-out secrets, and include shuffled labels and prompt-only baselines.
- **Causal interventions:** ablate or project out a learned direction, compare against norm-matched random/unrelated directions, and jointly measure target reduction and utility damage.

Standard baselines should be: no secret, secret with no outline, secret-blind fixed outline, secret-aware fixed outline, self-generated outline, active hiding, and decoy. Random subspace interventions and sign-reversed steering are essential for the white-box study. A model-size sweep is secondary because prior work already finds larger or more capable models leak more.

## Evaluation Metrics

The primary endpoint should be 2AFC secret-identification accuracy with candidate order counterbalanced. Analyze it with mixed-effects logistic regression using outline condition and candidate order as fixed effects and secret/story brief as random effects. Report effect sizes and bootstrap confidence intervals, not only significance.

Secondary leakage metrics are exact secret guess, top-k guess, calibrated judge log odds, and matched semantic similarity. Mechanism metrics are cross-validated secret-probe accuracy/AUROC, layerwise decodability, and trial-level association between decodability and leakage. Intervention success requires both reduced decodability and reduced behavioral leakage. Utility metrics should cover plan adherence, coherence, suspense/foreshadowing quality, diversity, length, and refusal rate. Layer/time scans require false-discovery correction or a preregistered region of interest.

## Datasets in the Literature

The downloaded Semantic Leakage suite supplies 109 handcrafted semantic examples and categories. ReboundBench supplies 5,000 single-token forbidden-concept prompts plus 500 matched negative/neutral/positive prompts. ConfAIde supplies privacy-sensitivity, contextual-integrity, sharing, and meeting-summary scenarios. None directly implements the required crossed story-outline experiment, so the primary dataset should be generated from screened concrete secrets and reusable story briefs. Existing datasets are best used for concept seeding, controls, and transfer validation.

## Gaps and Opportunities

1. No paper tests whether an externally supplied outline reduces involuntary story leakage while holding secret exposure constant.
2. Existing planning probes and secret elicitation studies are correlational; story-level causal mediation has not been shown.
3. Active hiding can invert or amplify signal, so “lower semantic similarity” alone is not evidence that information was removed.
4. Most classifiers split by example, not by secret identity, allowing concept-specific memorization to inflate apparent generalization.
5. Privacy and narrative quality are rarely evaluated jointly; an intervention can appear safe by making prose generic, incoherent, or refusal-heavy.

## Recommendations for the Experiment

Follow the three ranked directions in `planning.md`. Begin with a crossed behavioral factorial using an open 7–14B instruction model and one frontier API replication. The decisive contrast is no outline versus an externally supplied secret-blind outline. Then collect tokenwise residual activations on the same trials and test whether reduced decodability mediates any behavioral effect. Finally, remove or steer the secret subspace during prose generation with random-direction controls.

Use 30–50 secrets across semantic categories, at least eight reusable briefs per secret, and held-out-secret splits. Use multiple independent judges and a small blinded human audit. Preserve full prompts, outlines, seeds, model revisions, and decoding parameters. Treat semantic similarity and forbidden-token rebound as supporting metrics only; the central claim requires story-level inference and quality-preserving causal intervention.

## Key Citations

- Holtzman & West, 2026, [arXiv:2605.10794](https://arxiv.org/abs/2605.10794) — primary involuntary story-leakage result.
- Gonen et al., 2025, [arXiv:2408.06518](https://arxiv.org/abs/2408.06518) — semantic-leakage definition and matched evaluation.
- Fairoze et al., 2026, [arXiv:2608.19857](https://arxiv.org/abs/2608.19857) — adaptive decoding and suppression hypothesis.
- Dong et al., 2025, [arXiv:2502.06258](https://arxiv.org/abs/2502.06258) — response-planning activation probes.
- Cywiński et al., 2025, [arXiv:2510.01070](https://arxiv.org/abs/2510.01070) — public secret-elicitation benchmark.
- Xie & Riedl, 2024, [arXiv:2402.17119](https://arxiv.org/abs/2402.17119) — explicit story plan/prose separation.
