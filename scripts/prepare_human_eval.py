"""Prepare stratified sample for human evaluation.

Draws 50 samples per fidelity stratum (high/mid/low) based on
diff→gold NLI signed score from iter19 results.

For each sampled commit, includes:
  - diff excerpt (first 600 chars, tokenized form cleaned to readable)
  - gold commit message
  - generated messages from 3 models (shuffled, blind)
  - stratum label and NLI scores (hidden from annotators in output CSV)

Outputs:
  runs/human_eval/sample_pool.csv    — full data for analysis
  runs/human_eval/annotation_sheet.csv — annotator-facing sheet (no scores)
"""
from __future__ import annotations

import csv
import os
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "src"))

os.environ.setdefault("CMG_IST_DATA_ROOT", "/home/selab/research/dgf-cmg/data/raw")

from cmg_ist.io import load_samples, clean_msg  # noqa: E402

RESULTS_CSV = ROOT / "runs" / "iter19_scaled_full" / "results.csv"
OUT_DIR = ROOT / "runs" / "human_eval"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODELS = ["codellama-7b", "qwen2.5-coder-7b", "deepseek-6.7b"]

N_PER_STRATUM = 50
RANDOM_SEED = 42

HIGH_THRESH = 0.56
LOW_THRESH = -0.2
MAX_DIFF_CHARS = 1000


def clean_diff(raw: str) -> str:
    """Convert MCMD tokenized diff back to readable form (best-effort)."""
    # <nl> tokens → actual newlines
    s = raw.replace(" <nl> ", "\n").replace(" <nl>", "\n").replace("<nl> ", "\n").replace("<nl>", "\n")
    # Collapse multiple spaces within each line (tokenizer artifacts)
    lines = []
    for line in s.splitlines():
        line = re.sub(r" +", " ", line).strip()
        if line:
            lines.append(line)
    joined = "\n".join(lines)
    if len(joined) > MAX_DIFF_CHARS:
        return joined[:MAX_DIFF_CHARS].strip() + "\n[... diff truncated]"
    return joined.strip()


def load_raw_diffs() -> dict[tuple, str]:
    """Build (lang, diff_id_str) → cleaned diff excerpt from raw MCMD data."""
    from cmg_ist.io import iter_samples
    langs = ["cpp", "cs", "go", "java", "js", "php", "py", "rust"]
    diffs = {}
    for lang in langs:
        for s in iter_samples(lang):
            key = (lang, str(s["diff_id"]))
            diffs[key] = clean_diff(s.get("diff", ""))
    return diffs


def main() -> None:
    random.seed(RANDOM_SEED)

    # Load iter19 results
    rows = []
    with RESULTS_CSV.open() as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            rows.append(r)

    print(f"Loaded {len(rows)} rows from iter19 results")

    # Stratify
    high = [r for r in rows if float(r["nli_signed_diff→gold"]) >= HIGH_THRESH]
    mid  = [r for r in rows if LOW_THRESH <= float(r["nli_signed_diff→gold"]) < HIGH_THRESH]
    low  = [r for r in rows if float(r["nli_signed_diff→gold"]) < LOW_THRESH]

    print(f"  High: {len(high)}  Mid: {len(mid)}  Low: {len(low)}")

    # Sample
    sampled_high = random.sample(high, N_PER_STRATUM)
    sampled_mid  = random.sample(mid,  N_PER_STRATUM)
    sampled_low  = random.sample(low,  N_PER_STRATUM)

    sampled = (
        [(r, "high") for r in sampled_high] +
        [(r, "mid")  for r in sampled_mid]  +
        [(r, "low")  for r in sampled_low]
    )
    random.shuffle(sampled)

    print(f"Sampled {len(sampled)} total. Loading raw diffs ...")
    diffs = load_raw_diffs()

    # Build annotation items: one row per (commit, model) triple
    # item_id: unique identifier for each annotation task
    pool_rows = []
    annotation_rows = []
    item_id = 1

    for r, stratum in sampled:
        diff_id = r["diff_id"]
        lang = r["language"]
        diff_text = diffs.get((lang, str(diff_id)), "")
        gold = r["gold"]
        nli_dg = float(r["nli_signed_diff→gold"])

        for model in MODELS:
            gen = r.get(f"gen_{model}", "")
            nli_signed_gen = float(r.get(f"nli_signed_diff→gen_{model}", 0))
            nli_signed_gold_gen = float(r.get(f"nli_signed_gold→gen_{model}", 0))

            pool_rows.append({
                "item_id": item_id,
                "diff_id": diff_id,
                "language": lang,
                "stratum": stratum,
                "model": model,
                "diff_excerpt": diff_text,
                "gold_message": gold,
                "generated_message": gen,
                "nli_signed_diff→gold": nli_dg,
                "nli_signed_diff→gen": nli_signed_gen,
                "nli_signed_gold→gen": nli_signed_gold_gen,
            })

            annotation_rows.append({
                "item_id": item_id,
                "language": lang,
                "diff_excerpt": diff_text,
                "generated_message": gen,
                # Annotator fills these in:
                "rating (0/1/2)": "",
                "comment (optional)": "",
            })

            item_id += 1

    # Write pool CSV (full data, for analysis)
    pool_path = OUT_DIR / "sample_pool.csv"
    pool_fields = [
        "item_id", "diff_id", "language", "stratum", "model",
        "diff_excerpt", "gold_message", "generated_message",
        "nli_signed_diff→gold", "nli_signed_diff→gen", "nli_signed_gold→gen",
    ]
    with pool_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=pool_fields)
        w.writeheader()
        w.writerows(pool_rows)
    print(f"Wrote {pool_path}  ({len(pool_rows)} items)")

    # Write annotation sheet (no NLI scores, no gold, no model name)
    ann_path = OUT_DIR / "annotation_sheet.csv"
    ann_fields = [
        "item_id", "language", "diff_excerpt",
        "generated_message", "rating (0/1/2)", "comment (optional)",
    ]
    with ann_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=ann_fields)
        w.writeheader()
        w.writerows(annotation_rows)
    print(f"Wrote {ann_path}  ({len(annotation_rows)} items)")

    print("\nStratum breakdown in pool:")
    for st in ["high", "mid", "low"]:
        n = sum(1 for pr in pool_rows if pr["stratum"] == st)
        print(f"  {st}: {n} items ({n // len(MODELS)} commits × {len(MODELS)} models)")

    print("\nDone. Next step: distribute annotation_sheet.csv to raters.")
    print("Each rater fills in 'rating (0/1/2)' independently.")
    print("  2 = Faithful  1 = Partial  0 = Unfaithful")


if __name__ == "__main__":
    main()
