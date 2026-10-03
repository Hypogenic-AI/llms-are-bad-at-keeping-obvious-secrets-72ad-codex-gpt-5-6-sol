"""Local open-weight writer and cross-family judge for the leakage experiment."""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoModelForImageTextToText, AutoTokenizer

from run_behavioral import (JUDGE, OUT, SEED, WRITER, append_jsonl, generation_jobs,
                            judge_prompt, load_jsonl, make_pairs)

ROOT = Path(__file__).resolve().parents[1]
GEMMA_PATH = ROOT / "models" / "gemma-3-12b-it"
QWEN_PATH = ROOT / "models" / "qwen3-14b"


def load_writer():
    tokenizer = AutoTokenizer.from_pretrained(GEMMA_PATH, padding_side="left")
    model = AutoModelForImageTextToText.from_pretrained(
        GEMMA_PATH, torch_dtype=torch.bfloat16, device_map="cuda", attn_implementation="sdpa"
    ).eval()
    return tokenizer, model


def format_chat(tokenizer, prompt: str, thinking: bool = False) -> str:
    messages = [{"role": "user", "content": prompt}]
    kwargs = {"tokenize": False, "add_generation_prompt": True, "enable_thinking": thinking}
    try:
        return tokenizer.apply_chat_template(messages, **kwargs)
    except TypeError:
        kwargs.pop("enable_thinking", None)
        return tokenizer.apply_chat_template(messages, **kwargs)


@torch.inference_mode()
def generate_writer(pilot: bool, batch_size: int) -> Path:
    path = OUT / ("stories_pilot.jsonl" if pilot else "stories.jsonl")
    done = load_jsonl(path)
    jobs = [x for x in generation_jobs(pilot) if x["id"] not in done]
    tokenizer, model = load_writer()
    for start in range(0, len(jobs), batch_size):
        batch = jobs[start:start + batch_size]
        rendered = [format_chat(tokenizer, x["prompt"]) for x in batch]
        inputs = tokenizer(rendered, return_tensors="pt", padding=True).to(model.device)
        torch.manual_seed(SEED + start)
        begun = time.time()
        outputs = model.generate(
            **inputs, do_sample=True, temperature=0.8, top_p=0.95,
            max_new_tokens=760, min_new_tokens=420,
            disable_compile=True,
            pad_token_id=tokenizer.pad_token_id, eos_token_id=tokenizer.eos_token_id,
        )
        new = outputs[:, inputs["input_ids"].shape[1]:]
        texts = tokenizer.batch_decode(new, skip_special_tokens=True)
        elapsed = time.time() - begun
        for job, text in zip(batch, texts):
            row = {**job, "model": WRITER, "revision": "9478e665381f42974aa06177b019352fb6291876",
                   "provider": "local-transformers", "finish_reason": "local_generate",
                   "text": text.strip(), "usage": {"prompt_tokens": None, "completion_tokens": int(len(tokenizer.encode(text)))},
                   "elapsed_batch_s": round(elapsed, 3), "batch_size": len(batch)}
            append_jsonl(path, row)
        print(f"writer {min(start + batch_size, len(jobs))}/{len(jobs)}", flush=True)
    del model
    torch.cuda.empty_cache()
    return path


def load_judge(judge_model: str):
    if judge_model == "gemma":
        return (*load_writer(), "google/gemma-3-12b-it")
    tokenizer = AutoTokenizer.from_pretrained(QWEN_PATH, padding_side="left")
    model = AutoModelForCausalLM.from_pretrained(
        QWEN_PATH, torch_dtype=torch.bfloat16, device_map="cuda", attn_implementation="sdpa"
    ).eval()
    return tokenizer, model, "Qwen/Qwen3-14B"


@torch.inference_mode()
def run_judge(story_path: Path, pilot: bool, batch_size: int, judge_model: str) -> Path:
    stories = load_jsonl(story_path)
    pairs = make_pairs(stories)
    stem = "judgments_pilot" if pilot else "judgments"
    path = OUT / f"{stem}_{judge_model}.jsonl"
    done = load_jsonl(path)
    jobs = []
    for pair in pairs:
        for order in [0, 1]:
            jid = f"{pair['id']}::order{order}"
            if jid not in done:
                jobs.append({"id": jid, "pair": pair, "order": order})
    tokenizer, model, model_id = load_judge(judge_model)
    for start in range(0, len(jobs), batch_size):
        batch = jobs[start:start + batch_size]
        prompts = [format_chat(tokenizer, judge_prompt(x["pair"], x["order"]), thinking=False) for x in batch]
        inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=12000).to(model.device)
        outputs = model.generate(**inputs, do_sample=False, max_new_tokens=240, disable_compile=True,
                                 pad_token_id=tokenizer.pad_token_id, eos_token_id=tokenizer.eos_token_id)
        new = outputs[:, inputs["input_ids"].shape[1]:]
        texts = tokenizer.batch_decode(new, skip_special_tokens=True)
        for job, raw in zip(batch, texts):
            match = re.search(r"\{.*?\}", raw, re.S)
            try:
                parsed = json.loads(match.group(0)) if match else {}
            except json.JSONDecodeError:
                parsed = {}
            choice = str(parsed.get("choice", "")).upper().strip()
            correct_choice = "A" if job["order"] == 0 else "B"
            pair = job["pair"]
            row: dict[str, Any] = {
                "id": job["id"], "pair_id": pair["id"], "task": pair["task"],
                "condition": pair["condition"], "secret": pair.get("secret"), "twist": pair.get("twist"),
                "brief": pair.get("brief"), "case": pair.get("case"), "order": job["order"],
                "choice": choice, "correct_choice": correct_choice, "correct": choice == correct_choice,
                "confidence": parsed.get("confidence"), "evidence": parsed.get("evidence"), "raw": raw,
                "score_a": parsed.get("score_a"), "score_b": parsed.get("score_b"),
                "evidence_a": parsed.get("evidence_a"), "evidence_b": parsed.get("evidence_b"),
                "model": model_id, "revision": "local snapshot", "provider": "local-transformers",
            }
            append_jsonl(path, row)
        print(f"judge {min(start + batch_size, len(jobs))}/{len(jobs)}", flush=True)
    return path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--pilot", action="store_true")
    p.add_argument("--stage", choices=["writer", "judge", "all"], default="all")
    p.add_argument("--batch-size", type=int, default=4)
    p.add_argument("--judge-model", choices=["qwen", "gemma"], default="qwen")
    args = p.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / ("stories_pilot.jsonl" if args.pilot else "stories.jsonl")
    if args.stage in {"writer", "all"}:
        path = generate_writer(args.pilot, args.batch_size)
    if args.stage in {"judge", "all"}:
        run_judge(path, args.pilot, args.batch_size, args.judge_model)


if __name__ == "__main__":
    main()
