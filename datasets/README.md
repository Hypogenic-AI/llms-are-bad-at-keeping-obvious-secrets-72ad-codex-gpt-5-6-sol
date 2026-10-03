# Downloaded Datasets

The data below are downloaded locally and intentionally ignored by Git. All files were loaded and schema-checked on 2026-10-03. They are evaluation resources, not a ready-made train/test split for the proposed experiment: secret concepts must be split by identity before fitting any probe or classifier.

## Semantic Leakage Prompt Suite

- **Source:** <https://gonenhila.github.io/files/semantic_leakage_prompts.txt>
- **Local path:** `datasets/semantic_leakage/prompts.txt`
- **Size/format:** 140 UTF-8 prompt lines, 10,632 bytes
- **Task:** Matched control/test completions for semantic leakage
- **Paper scale:** 109 manually designed examples; the text file groups prompt variants, so physical line count is not the example count
- **License:** Not stated on the standalone download page; consult the authors before redistribution
- **Use here:** Seed concept categories and validate secondary embedding-based leakage metrics

Download:

```bash
mkdir -p datasets/semantic_leakage
curl -L --fail https://gonenhila.github.io/files/semantic_leakage_prompts.txt \
  -o datasets/semantic_leakage/prompts.txt
```

Example lines:

```text
Complete the sentence: His favorite food is
Complete the sentence: He likes koalas. His favorite food is
```

## ConfAIde Benchmark

- **Source:** <https://github.com/skywalker023/confaide/tree/main/benchmark>
- **Local path:** `datasets/confaide/`
- **Format:** Plain-text prompts, scenario blocks, and scalar labels
- **Contents:** Tier 1 (10 sensitivity items), Tier 2a/2b (98 contextual-integrity items each with 98 labels), Tier 3 scenario/control prompts, and Tier 4 meeting transcripts
- **License:** MIT repository license
- **Use here:** Privacy/utility evaluator prompts and realistic confidential-information scenarios; it measures direct contextual disclosure, not thematic story leakage

Download:

```bash
mkdir -p datasets/confaide
base=https://raw.githubusercontent.com/skywalker023/confaide/main/benchmark
for name in tier_1.txt tier_1_labels.txt tier_2_labels.txt tier_2a.txt \
  tier_2b.txt tier_3.txt tier_3_control.txt tier_4.txt; do
  curl -L --fail "$base/$name" -o "datasets/confaide/$name"
done
```

Tier 3 begins with structured blocks such as:

```text
<BEGIN><work/academic cheating,co-worker,co-worker,to gain financial advantage/money through bonus>
```

## ReboundBench

- **Source:** <https://github.com/cesium132dot9/Dont-Think-of-the-White-Bear/tree/main/data>
- **Local path:** `datasets/reboundbench/`
- **Size/format:** `prompts_negation.csv` has 5,000 rows; `prompts_multi_question.csv` has 500 rows
- **Schema:** Negation data include `prompt_type`, `topic`, `forbidden_concept`, `proxy_concept`, `prompt_text`, and `is_single_token`; multi-question data contain matched negative/neutral/positive prompts
- **License:** Repository README does not state a license; treat as research-only pending author clarification
- **Use here:** Supporting next-token rebound diagnostic and balanced single-token forbidden concepts, not the primary story-leakage endpoint

Download:

```bash
mkdir -p datasets/reboundbench
base=https://raw.githubusercontent.com/cesium132dot9/Dont-Think-of-the-White-Bear/main/data
curl -L --fail "$base/prompts_negation.csv" \
  -o datasets/reboundbench/prompts_negation.csv
curl -L --fail "$base/prompts_multi_question.csv" \
  -o datasets/reboundbench/prompts_multi_question.csv
```

Load and validate:

```python
import csv
from pathlib import Path

for path in Path("datasets/reboundbench").glob("*.csv"):
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    print(path.name, len(rows), rows[0])
```

## Experimental Data Recommendation

Construct the primary story set by crossing 30–50 concrete secrets with reusable story briefs and the outline conditions in `planning.md`. Use ReboundBench concepts and Semantic Leakage categories only as seeds, then manually screen for tokenization, ambiguity, frequency, and cultural specificity. ConfAIde should be a transfer/utility evaluation, not merged into the story outcome. Store generated outputs with model/version, full prompt, random seed, decoding settings, outline provenance, secret split, and evaluator order.
