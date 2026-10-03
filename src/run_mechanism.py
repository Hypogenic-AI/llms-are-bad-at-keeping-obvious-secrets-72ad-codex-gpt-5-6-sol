"""Residual-stream measurement and causal projection-removal pilot.

Concept directions are learned only from independent carrier prompts. Evaluation
uses held-out story prose; no judge labels or story text enter direction fitting.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

import torch

from run_behavioral import OUT, SEED, append_jsonl, load_jsonl
from run_local import ROOT, format_chat, load_writer

EVAL = ROOT / "results" / "evaluations"
LAYERS = [12, 24, 36, 47]
CARRIER_TEMPLATES = [
    "A private note identifies the protected concept as {value}.",
    "The confidential topic for this exercise is {value}.",
    "Remember internally that the designated idea is {value}.",
    "The hidden subject, which must not be repeated, is {value}.",
]
NEUTRAL = "unspecified"


@torch.inference_mode()
def fit_directions(tokenizer, model, secrets: list[str]) -> dict[str, dict[int, torch.Tensor]]:
    directions: dict[str, dict[int, torch.Tensor]] = {}
    for secret in secrets:
        diffs = {layer: [] for layer in LAYERS}
        for template in CARRIER_TEMPLATES:
            texts = [template.format(value=secret), template.format(value=NEUTRAL)]
            rendered = [format_chat(tokenizer, x) for x in texts]
            inputs = tokenizer(rendered, return_tensors="pt", padding=True).to(model.device)
            outputs = model(**inputs, output_hidden_states=True, return_dict=True)
            for layer in LAYERS:
                h = outputs.hidden_states[layer + 1][:, -1, :].float()
                diffs[layer].append(h[0] - h[1])
        directions[secret] = {}
        for layer in LAYERS:
            d = torch.stack(diffs[layer]).mean(0)
            directions[secret][layer] = d / d.norm().clamp_min(1e-8)
        print("direction", secret, flush=True)
    return directions


@torch.inference_mode()
def measure_stories(tokenizer, model, stories: dict, directions: dict) -> Path:
    path = EVAL / "residual_projections.jsonl"
    done = load_jsonl(path)
    rows = [x for x in stories.values() if x["task"] == "word" and x["brief"] == "station"
            and x["condition"] in {"none", "outline"}]
    for i, row in enumerate(rows):
        if row["id"] in done:
            continue
        prefix = format_chat(tokenizer, row["prompt"])
        prefix_ids = tokenizer(prefix, return_tensors="pt")["input_ids"]
        story_ids = tokenizer(row["text"], add_special_tokens=False, return_tensors="pt")["input_ids"]
        ids = torch.cat([prefix_ids, story_ids], dim=1).to(model.device)
        outputs = model(input_ids=ids, attention_mask=torch.ones_like(ids),
                        output_hidden_states=True, return_dict=True, use_cache=False)
        n = story_ids.shape[1]
        positions = {"early": prefix_ids.shape[1] + max(0, int(n * .1) - 1),
                     "middle": prefix_ids.shape[1] + max(0, int(n * .5) - 1),
                     "late": prefix_ids.shape[1] + max(0, int(n * .9) - 1)}
        projections = {}
        for layer in LAYERS:
            d = directions[row["secret"]][layer].to(model.device)
            for landmark, pos in positions.items():
                h = outputs.hidden_states[layer + 1][0, pos].float()
                projections[f"L{layer}_{landmark}"] = float(torch.dot(h / h.norm().clamp_min(1e-8), d))
        append_jsonl(path, {"id": row["id"], "secret": row["secret"], "condition": row["condition"],
                            "secret_present": row["secret_present"], "brief": row["brief"],
                            "story_tokens": n, "projections": projections})
        del outputs
        print(f"measure {i+1}/{len(rows)}", flush=True)
    return path


class ProjectionHook:
    def __init__(self, direction: torch.Tensor):
        self.d = direction

    def __call__(self, module, args, output):
        hidden = output[0] if isinstance(output, tuple) else output
        d = self.d.to(device=hidden.device, dtype=hidden.dtype)
        # Only alter the position used to predict the next prose token.
        last = hidden[:, -1:, :]
        corrected = last - torch.einsum("btd,d->bt", last, d).unsqueeze(-1) * d
        hidden = torch.cat([hidden[:, :-1, :], corrected], dim=1)
        if isinstance(output, tuple):
            return (hidden, *output[1:])
        return hidden


@torch.inference_mode()
def intervene(tokenizer, model, stories: dict, directions: dict) -> Path:
    path = OUT / "intervention_stories.jsonl"
    done = load_jsonl(path)
    secrets = list(directions)[:6]
    rng = torch.Generator(device=model.device).manual_seed(SEED)
    jobs = []
    for secret in secrets:
        for brief in ["station"]:
            source_id = f"word::{secret}::{brief}::none::1"
            source = stories[source_id]
            for intervention in ["secret_remove", "random_remove"]:
                jobs.append((source, intervention))
    layers = model.model.language_model.layers
    for i, (source, intervention) in enumerate(jobs):
        jid = f"intervene::{source['secret']}::{source['brief']}::{intervention}"
        if jid in done:
            continue
        handles = []
        for layer in [24, 36]:
            d = directions[source["secret"]][layer].to(model.device)
            if intervention == "random_remove":
                d = torch.randn(d.shape, generator=rng, device=d.device)
                d = d / d.norm()
            handles.append(layers[layer].register_forward_hook(ProjectionHook(d)))
        rendered = format_chat(tokenizer, source["prompt"])
        inputs = tokenizer(rendered, return_tensors="pt").to(model.device)
        torch.manual_seed(source["seed"])
        output = model.generate(**inputs, do_sample=True, temperature=.8, top_p=.95,
                                max_new_tokens=620, min_new_tokens=350, disable_compile=True,
                                pad_token_id=tokenizer.pad_token_id, eos_token_id=tokenizer.eos_token_id)
        for handle in handles:
            handle.remove()
        text = tokenizer.decode(output[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
        append_jsonl(path, {"id": jid, "task": "word", "secret": source["secret"], "brief": source["brief"],
                            "condition": "intervention", "intervention": intervention, "secret_present": True,
                            "prompt": source["prompt"], "seed": source["seed"], "text": text,
                            "model": source["model"], "provider": "local-transformers"})
        print(f"intervene {i+1}/{len(jobs)}", flush=True)
    return path


def main() -> None:
    random.seed(SEED)
    torch.manual_seed(SEED)
    EVAL.mkdir(parents=True, exist_ok=True)
    stories = load_jsonl(OUT / "stories.jsonl")
    if not stories:
        raise RuntimeError("Run the full writer experiment first")
    secrets = sorted({x["secret"] for x in stories.values() if x["task"] == "word"})
    tokenizer, model = load_writer()
    directions = fit_directions(tokenizer, model, secrets)
    torch.save({s: {l: d.cpu() for l, d in ds.items()} for s, ds in directions.items()},
               EVAL / "concept_directions.pt")
    measure_stories(tokenizer, model, stories, directions)
    intervene(tokenizer, model, stories, directions)


if __name__ == "__main__":
    main()
