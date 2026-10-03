# Research Plan

## Motivation & Novelty Assessment

### Why This Research Matters

Subtle thematic leakage can disclose private context or spoil future plot events even when a model never repeats the protected words. Separating planning from prose could offer a cheap mitigation, while a causal account would distinguish genuine information removal from avoidance patterns that remain decodable.

### Gap in Existing Work

Holtzman and West (2026) establish behavioral secret-word leakage but do not test explicit plans, plot-level twists, or internals. Planning-probe and Taboo work shows future attributes and trained-in secrets are decodable, but has not linked naturally prompted secret representations to unrelated story prose or causally removed them. No reviewed work controls the extra-context dilution introduced by an outline.

### Our Novel Contribution

We test whether a secret-blind external outline reduces leakage beyond a length-matched irrelevant-context control, benchmark the effect against a decoy, and add plot-twist/no-secret controls. On the same open model, we measure secret-aligned residual activity during prose and intervene on that direction during generation, with norm-matched random controls and utility checks.

### Experiment Justification

- **Experiment 1 — behavioral factorial:** establishes the positive leakage anchor and isolates structured planning from mere context dilution; the decoy provides a published-effect yardstick.
- **Experiment 2 — representation trajectory:** tests whether secret information remains accessible throughout prose and whether its strength covaries with behavioral leakage. Decodability alone is explicitly treated as correlational.
- **Experiment 3 — causal removal:** tests the strongest mechanism claim by asking whether subtracting secret-aligned residual components lowers leakage without nonspecific quality collapse.
- **Plot-level pilot:** tests whether conclusions extend beyond isolated words while a premise-only/no-secret control measures twist guessability.

## Research Question

When Gemma 3 12B writes a roughly 450-word story while holding a forbidden secret, does an externally supplied outline reduce order-balanced 2AFC leakage beyond an equally long irrelevant context, and is any change associated with—and causally dependent on—secret-aligned residual-stream activity?

## Background and Motivation

The primary behavioral phenomenon is already known at 12B+ scale, so a replication alone has little value. The decisive contribution is a controlled plan manipulation plus white-box measurement on a model large enough to avoid the documented floor effect. The study uses the original 15 words for comparability and reports pilot-scale uncertainty rather than generalizing beyond the tested model and prompts.

## Hypothesis Decomposition

- **H1 (anchor):** secret/no-outline stories are discriminable from matched no-secret stories above 50%.
- **H2 (offloading):** secret-blind outlines lower discrimination relative to no outline and relative to length-matched irrelevant context.
- **H3 (decoy yardstick):** decoy context redirects or lowers real-secret evidence, giving a known mitigation comparison.
- **H4 (representation):** secret-aligned activation remains positive during prose and trial-level strength predicts judge correctness/confidence.
- **H5 (causality):** projection removal lowers both activation alignment and behavioral leakage more than norm-matched random removal while preserving narrative utility.
- **H6 (plot twist):** a hidden twist leaks above its premise-only control; a secret-blind outline reduces that excess.

Independent variables are secret presence, outline condition, presentation order, and intervention. Primary dependent variable is 2AFC correctness; secondary variables are judge confidence, exact mention rate, length, coherence, adherence, and residual alignment.

## Proposed Methodology

### Approach

Use the exact open-weight model family previously reported to leak strongly. Generate matched secret/no-secret stories from reusable neutral briefs under four contexts: none, secret-blind outline, length-matched irrelevant prose, and decoy. Evaluate with a different-family frontier judge in both A/B orders. Reuse the same prompts locally for residual collection and controlled intervention.

### Experimental Steps

1. Validate the local 12B model and prompts on a small anchor set; stop scale-up only if literal secret mentions make the protocol invalid.
2. Cross the 15 published secrets with reusable briefs and four conditions, using deterministic recorded seeds and matched control seeds.
3. Judge every pair in both presentation orders with structured JSON, cache all raw requests/responses, and score order agreement and position bias.
4. Run a small plot-twist extension with no-secret/premise-only controls.
5. Extract selected-layer residual states at prompt end and prose landmarks; define concept directions from independent carrier sentences, never from evaluation prose.
6. Intervene during prose generation by projection subtraction in preregistered middle/late layers; compare secret-direction and random-direction interventions on a subset.
7. Analyze and rerun key deterministic processing to verify reproducibility.

### Baselines

Chance (50%), matched no-secret outputs, no-outline positive anchor, length-matched irrelevant context, and decoy context. Mechanistic controls are no intervention, norm-matched random direction, and quality/length checks. Plot twists use premise-only/no-twist controls.

### Evaluation Metrics

Primary: order-balanced pair accuracy, Wilson 95% CI, order-consistent accuracy, and exact binomial test versus 0.5. Comparisons: paired accuracy differences with cluster bootstrap by secret and paired permutation/McNemar tests where appropriate. Secondary: position bias, order disagreement, judge confidence, literal mentions, word count, refusal, coherence, and plan adherence. Mechanism: normalized projection on the independent secret direction by layer/time and intervention effect on leakage and utility.

### Statistical Analysis Plan

The preregistered primary contrast is outline minus no-outline; the dilution contrast is outline minus irrelevant context. Two-sided alpha is .05 with Holm correction across the two primary mitigation comparisons. Confidence intervals are clustered by secret. Layer/time scans are descriptive unless corrected with Benjamini–Hochberg. Because API judgments in opposite orders are repeated measures, the pair—not each order—is the inferential unit; both orders quantify bias. Any underpowered pilot result will be labeled exploratory.

## Expected Outcomes

H1 is supported by an anchor CI mostly above chance. H2 requires a negative outline effect that is also lower than irrelevant context; equality with irrelevant context supports dilution rather than planning offload. H4 requires persistent alignment plus a positive trial-level association. H5 requires a selective reduction versus random intervention without material quality loss. Null, inverted, and quality-confounded outcomes are reportable findings.

## Timeline and Milestones

1. Planning and environment/model validation (20%).
2. Behavioral generation and cached judging (35%).
3. Activation/intervention pilot (25%).
4. Statistical analysis, figures, documentation, rerun validation (20%).

## Potential Challenges

- Model download/tooling failure: use the ungated `unsloth/gemma-3-12b-it` or OpenRouter behavioral endpoint and document why white-box work is reduced.
- Anchor floor: retain the documented 12B model; do not silently substitute a smaller model.
- Outline dilution: the length-matched irrelevant context is mandatory.
- Judge noise/bias: both candidate orders, structured parsing, order-agreement reporting, and cluster-level inference.
- Literal disclosure: flag and report separately; do not count it as subtle leakage.
- Intervention damage: random-direction and utility controls; no causal claim if quality collapses.

## Success Criteria

The research cycle succeeds if it produces real-model outputs, an order-balanced behavioral comparison with uncertainty, at least a validated white-box representation or intervention pilot, complete raw artifacts/prompts/configuration, and conclusions calibrated to the achieved sample size. Scientific success does not require a positive hypothesis result.

## Research Direction Ranking

Scores use a 1–5 scale. The total weights literature support (25%), hypothesis relevance (30%), expected information gain (25%), and implementation feasibility (20%). The search space is frozen to the top three directions below unless new evidence invalidates this ranking.

| Rank | Direction | Literature | Relevance | Information gain | Feasibility | Weighted total | Decision |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | Causal behavioral outline experiment | 5 | 5 | 5 | 5 | 5.00 | Keep |
| 2 | Tokenwise secret-representation mediation | 4 | 5 | 5 | 4 | 4.55 | Keep |
| 3 | Causal representation removal/steering | 4 | 5 | 5 | 3 | 4.35 | Keep |
| 4 | Broad model-size scaling survey | 4 | 3 | 3 | 2 | 3.10 | Reject: expensive and mostly replicates established scaling results before testing the outline mechanism |
| 5 | Fine-tune models to keep secrets | 3 | 3 | 3 | 2 | 2.80 | Reject: training introduces capability and data confounds; mitigation is premature before mechanism identification |
| 6 | Multi-turn private-memory architecture | 4 | 2 | 3 | 2 | 2.75 | Reject: tests persistent hidden state, not whether a public outline offloads prose planning |
| 7 | Ironic-rebound next-token benchmark | 4 | 3 | 2 | 4 | 3.20 | Reject as a standalone direction: useful supporting diagnostic, but not the story-level outcome in the hypothesis |
| 8 | Large human creative-writing study first | 3 | 4 | 3 | 2 | 3.10 | Reject for the first pass: costly and slow; use blinded model judges plus a small human validation after effect sizing |

## Direction 1 — Causal Behavioral Outline Experiment

Use a within-secret factorial design with identical story briefs and decoding settings:

1. no outline;
2. externally supplied secret-blind outline;
3. externally supplied secret-aware outline;
4. model-generated outline;
5. decoy-outline control;
6. no-secret control.

The crucial comparison is no outline versus a secret-blind fixed outline. It tests the offloading hypothesis without adding a second exposure to the secret. Secret-aware and self-generated outlines identify whether planning helps because it structures prose or hurts because it entangles the secret with the plan. Primary outcome: order-balanced, blinded 2AFC secret identification on held-out stories, with exact/free secret guesses and semantic similarity as secondary outcomes. Measure coherence, plan adherence, suspense, and style so suppression cannot masquerade as success by destroying story quality.

Evidence: Holtzman and West (2026) establish story-level leakage and appropriate controls; Gonen et al. (2025) validate matched semantic-leakage measurement; Xie and Riedl (2024) show explicit iterative plots improve suspense and consistency; ConfAIde shows privacy prompts can trade off with utility.

## Direction 2 — Tokenwise Secret-Representation Mediation

On an open-weight instruction model, collect residual-stream activations at prompt end, outline tokens, and fixed prose-generation landmarks. Train cross-validated probes to identify the secret from held-out secret classes, with shuffled-label, prompt-only, lexical-overlap, and random-direction controls. Test the preregistered mediation chain:

`outline condition → secret decodability during prose → behavioral leakage`.

Estimate decodability trajectories per layer and token position, and relate trial-level probe scores to story leakage while controlling for story length, outline adherence, and secret frequency. Treat probe success as accessibility, not causality.

Evidence: Dong et al. (2025) demonstrate future-response decodability and its temporal profile; Cywiński et al. (2025) show hidden secrets are recoverable with logit-lens/SAE methods; Wang et al. (2026) warn that behaviorally probed internal states can drift; Wu et al. (2024) distinguish deliberate pre-caching from ordinary breadcrumbs.

## Direction 3 — Causal Representation Removal/Steering

Learn a secret subspace on disjoint training secrets, then intervene only during prose generation using at least two methods (for example, mean-difference projection removal and LEACE/INLP-style erasure). Compare with norm-matched random subspaces, unrelated-concept removal, sign-reversed steering, and prompt-level no-secret controls. Evaluate whether intervention lowers both probe decodability and 2AFC leakage while preserving plan adherence and prose quality. Apply interventions across layer/time windows to localize when secret information is causally used.

This direction answers the strongest mechanism claim: whether removing the active concept removes leakage. It should follow the behavioral and correlational studies because aggressive erasure can damage generation nonspecifically.

Evidence: the elicitation papers show recoverable secret representations but remain largely correlational; White Bear provides a narrow head-ablation precedent; inadvertent-context leakage links suppression to detectable output distortions but does not manipulate internal representations.

## Minimal First Experiment

- Secrets: 30–50 concrete concepts, balanced by semantic category and tokenization.
- Story briefs: at least 8 per secret, crossed across conditions.
- Generation model: one open-weight 7–14B instruction model for white-box work; add one frontier API model only for behavioral replication.
- Leakage: order-balanced 2AFC judges from at least two model families; exact secret guess; embedding score; preregistered human audit subset.
- Statistics: mixed-effects logistic regression with fixed effects for outline condition and order, random intercepts for secret and brief; report bootstrap confidence intervals and false-discovery correction for layer/time scans.
- Split discipline: hold out secrets—not merely outputs—when fitting probes or leakage classifiers.
