# Paper Outline: Content Constraints Suppress Detectable Secret Leakage in Gemma 3 12B

## Evidence map

- Behavioral estimates: `results/evaluations/behavior_summary.csv` and `condition_contrasts.csv`.
- Residual-stream estimates: `results/evaluations/residual_summary.csv` and `residual_projections_long.csv`.
- Intervention estimates: `results/evaluations/intervention_summary.csv`, `intervention_summary_pairs.csv`, and generated-story lengths.
- Generation validity: `results/evaluations/story_quality.csv`, raw stories, and `REPORT.md`.
- Visuals: `figures/behavior_delta.png` and `figures/residual_trajectory.png`.

## Abstract

- Motivate nonliteral leakage despite literal compliance.
- Describe the crossed word experiment, plot pilot, residual measurements, and projection intervention.
- Report the open-anchor effect (+16.33), briefed no-outline floor (-0.15), outline contrasts, and intervention length collapse.
- State the calibrated conclusion: content constraints moderate leakage; planning offload and selective causal removal remain unproven.

## 1. Introduction

- Hook: a model can avoid a forbidden word while still revealing it through content choices.
- Explain why an outline could offload anticipatory decisions, and why extra context is a confound.
- Identify gaps in prior behavioral leakage, planning-probe, and secret-elicitation work.
- Preview the design and quantitative results.
- Contributions: controlled behavioral study, plot/internal-state extensions, and causal intervention with utility checks.
- Roadmap.

## 2. Related Work

- Semantic and confidentiality leakage: Holtzman & West; Gonen et al.; Mireshghallah et al.; Fairoze et al.; Mann et al.
- Planning and narrative structure: Dong et al.; Wu et al.; Xie & Riedl; Baldelli et al.
- Internal secret representations: both Cywinski et al. papers and Luo et al.
- Position the present work as the first outline-versus-length-matched-context test coupled to residual and intervention diagnostics.

## 3. Methodology

- Formalize pair-level, order-balanced influence score.
- Describe 15 secrets, two briefs, four contexts, open anchor, and six plot twists.
- Explain secret/no-secret matching and the role of each baseline.
- Detail writer/judge model, decoding, hardware, exact story counts, literal-leak checks, and output lengths.
- Detail bootstrap intervals and sign-permutation tests; explain why the planned mixed model was not fit.
- Define carrier-prompt directions, layers/landmarks, and projection-removal/random controls.

## 4. Results

- Main behavioral table with all word and plot conditions; bold statistically separated anchor and decoy rows.
- Behavioral figure and interpretation: anchor replicated, neutral brief induced a floor, outline did not beat no-outline or irrelevant context.
- Report judge order instability and failed Qwen pilot.
- Plot pilot as underpowered and null.
- Residual figure: tiny inconsistent gaps, largest +0.0132 at layer 47 late; outline -0.00144 there.
- Intervention table: secret removal -77.5 versus random -10.8, but 102 versus 488 words; reject selective-causality claim.

## 5. Discussion

- Interpret content-choice freedom as the best-supported moderator.
- Explain why the floor prevents a clean test of planning offload.
- Discuss what null residual gaps do and do not imply.
- Limitations: one model/judge, low power, judge instability, long outputs, linear carrier directions, intervention damage, no frontier/human validation.
- Broader implications: confidentiality evaluation needs matched controls, context controls, and utility-preserving interventions.

## 6. Conclusion

- Summarize the replicated leakage and brief-induced suppression.
- State that outlining and selective causal erasure were not demonstrated.
- Recommend broad premise screening, 100+ pairs, calibrated independent judges and humans, larger plot sets, and disjoint-secret subspace methods with utility gates.

## Appendix

- Reproducibility and access details.
- Experimental inventory and evidence-strength statement.
