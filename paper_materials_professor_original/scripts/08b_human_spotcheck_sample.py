"""Iter 8b — construct-validity spot-check sampler.

Stratified sample of 30 triplets for blind human rating:
  - 10 verb pairs (iter 5b, from ALL verb anchors)
  - 5 × 4 noun pairs, one batch per kind (iter 7)

For each sample: present (gold, cand_A, cand_B) with A/B order randomized.
Rater picks which candidate is more faithful to the gold (or neither/both).

Outputs:
  runs/iter08_calibration/spotcheck/rater.csv          (blind — for annotation)
  runs/iter08_calibration/spotcheck/ground_truth.csv   (hidden — our labels)
  runs/iter08_calibration/spotcheck/README.md          (instructions)
"""
from __future__ import annotations

import csv
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "src"))

from cmg_ist.io import load_samples, clean_msg  # noqa: E402
from cmg_ist.perturbation_pairs import apply_pair  # noqa: E402
from cmg_ist.perturbation_noun_pairs import apply_noun_pair, KINDS as NOUN_KINDS  # noqa: E402

RUNS = ROOT / "runs"
OUT = RUNS / "iter08_calibration" / "spotcheck"
OUT.mkdir(parents=True, exist_ok=True)

SEED = 1729
LANGUAGES = ["cpp", "cs", "go", "java", "js", "php", "py", "rust"]

VERB_N = 10
NOUN_PER_KIND = 5  # × 4 kinds = 20


def load_verb_pool() -> list[dict]:
    rows: list[dict] = []
    with (RUNS / "iter05b_nli" / "results.csv").open() as fh:
        for r in csv.DictReader(fh):
            rows.append({
                "diff_id": int(r["diff_id"]),
                "language": r["language"],
                "anchor": r["anchor"],
                "synonym": r["synonym"],
                "antonym": r["antonym"],
                "kind": "verb",
            })
    return rows


def load_noun_pool() -> list[dict]:
    rows: list[dict] = []
    with (RUNS / "iter07_noun" / "results.csv").open() as fh:
        for r in csv.DictReader(fh):
            rows.append({
                "diff_id": int(r["diff_id"]),
                "language": r["language"],
                "anchor": r["anchor"],
                "synonym": r["synonym"],
                "disjoint": r["disjoint"],
                "kind": f"noun_{r['kind']}",
                "noun_subkind": r["kind"],
            })
    return rows


def stratified_pick(pool: list[dict], n: int, rng: random.Random,
                    key=None) -> list[dict]:
    """Pick n rows trying to diversify by `key` (e.g. anchor or language)."""
    if key is None:
        return rng.sample(pool, n)
    buckets: dict[str, list[dict]] = {}
    for r in pool:
        buckets.setdefault(key(r), []).append(r)
    for k in buckets:
        rng.shuffle(buckets[k])
    ordered_keys = list(buckets.keys())
    rng.shuffle(ordered_keys)
    picked: list[dict] = []
    i = 0
    while len(picked) < n:
        k = ordered_keys[i % len(ordered_keys)]
        if buckets[k]:
            picked.append(buckets[k].pop())
        i += 1
        if i > 10000:
            break
    return picked[:n]


def reconstruct(sample: dict) -> tuple[str, str, str] | None:
    """Load gold, apply perturbation, return (gold, syn_cand, other_cand)."""
    for s in load_samples(sample["language"], limit=None):
        if s["diff_id"] != sample["diff_id"]:
            continue
        gold = clean_msg(s["msg"])
        if sample["kind"] == "verb":
            res = apply_pair(gold, sample["anchor"])
        else:
            res = apply_noun_pair(gold, sample["anchor"])
        if res is None:
            return None
        syn_cand, other_cand, _ = res
        return gold, syn_cand, other_cand
    return None


def main() -> None:
    rng = random.Random(SEED)

    verb_pool = load_verb_pool()
    noun_pool = load_noun_pool()
    print(f"verb pool: {len(verb_pool)}, noun pool: {len(noun_pool)}")

    # Select verbs stratified by anchor, then by language
    verb_picks = stratified_pick(verb_pool, VERB_N, rng, key=lambda r: r["anchor"])

    # Select nouns: N per kind, stratified by anchor within kind
    noun_picks: list[dict] = []
    for kind in sorted({f"noun_{v}" for v in set(NOUN_KINDS.values())}):
        sub = [r for r in noun_pool if r["kind"] == kind]
        picks = stratified_pick(sub, NOUN_PER_KIND, rng, key=lambda r: r["anchor"])
        noun_picks.extend(picks)

    all_picks = verb_picks + noun_picks
    print(f"picked {len(all_picks)} triplets")

    rater_rows: list[dict] = []
    truth_rows: list[dict] = []

    for idx, s in enumerate(all_picks, start=1):
        rec = reconstruct(s)
        if rec is None:
            print(f"  skip sample {s['diff_id']}/{s['anchor']} — reconstruction failed")
            continue
        gold, syn_cand, other_cand = rec
        # Randomize A/B
        flip = rng.random() < 0.5
        if flip:
            cand_a, cand_b = other_cand, syn_cand
            a_is_syn = False
        else:
            cand_a, cand_b = syn_cand, other_cand
            a_is_syn = True

        other_word = s.get("antonym") or s.get("disjoint")

        rater_rows.append({
            "sample_id": f"S{idx:02d}",
            "kind": s["kind"],
            "gold": gold,
            "candidate_A": cand_a,
            "candidate_B": cand_b,
            "rater_judgment": "",  # "A", "B", "both", "neither"
            "rater_notes": "",
        })
        truth_rows.append({
            "sample_id": f"S{idx:02d}",
            "kind": s["kind"],
            "language": s["language"],
            "diff_id": s["diff_id"],
            "anchor": s["anchor"],
            "syn_word": s["synonym"],
            "other_word": other_word,
            "cand_A_is_syn": a_is_syn,
            "expected_rater_pick": "A" if a_is_syn else "B",
        })

    with (OUT / "rater.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=[
            "sample_id", "kind", "gold", "candidate_A", "candidate_B",
            "rater_judgment", "rater_notes",
        ])
        w.writeheader()
        w.writerows(rater_rows)

    with (OUT / "ground_truth.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=[
            "sample_id", "kind", "language", "diff_id", "anchor",
            "syn_word", "other_word", "cand_A_is_syn", "expected_rater_pick",
        ])
        w.writeheader()
        w.writerows(truth_rows)

    readme = """# Construct-validity spot-check (30 triplets)

## Goal
Check that our automatic labelling — the near-synonym candidate is
meaning-preserving relative to the gold commit message, and the
antonym/disjoint candidate is meaning-changing — matches an independent
human judgment. This protects the main claim ("NLI probe discriminates
meaning direction where word-metric evaluators do not") from a reviewer
critique that says our labels themselves are noisy.

## Task
For each row in `rater.csv`:
  1. Read the `gold` commit message.
  2. Read candidates A and B.
  3. Fill `rater_judgment` with one of:
       - `A` — A is more faithful to the gold message's meaning
       - `B` — B is more faithful
       - `both` — both preserve the meaning
       - `neither` — neither preserves the meaning
  4. Optional `rater_notes` for edge cases.

**Do not look at `ground_truth.csv` before rating.**

## Scoring
After rating, run (future script) `08c_spotcheck_analyze.py` to compute:
  - Agreement rate between rater and our automatic labels
  - Per-kind agreement (verb / noun_close_entity / ... / noun_directional)
  - Identify disagreements for qualitative discussion

Target: ≥ 80% agreement on the pick = our label is trustworthy enough
for the main claim. Lower than that → paper needs a caveat in the
threats-to-validity section.
"""
    (OUT / "README.md").write_text(readme)

    print(f"wrote {OUT / 'rater.csv'}")
    print(f"wrote {OUT / 'ground_truth.csv'}")
    print(f"wrote {OUT / 'README.md'}")
    # Print first 5 rater rows for eyeball
    print()
    print("first 5 rater rows:")
    for r in rater_rows[:5]:
        print(f"  {r['sample_id']} [{r['kind']}]")
        print(f"    gold: {r['gold']}")
        print(f"    A:    {r['candidate_A']}")
        print(f"    B:    {r['candidate_B']}")


if __name__ == "__main__":
    main()
