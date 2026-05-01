"""Iter 8c — analyze human spot-check responses.

Consumes the filled-in rater.csv and computes:
  - Overall agreement with our automatic labels
  - Per-kind agreement
  - Confusion breakdown: "both" / "neither" responses flag vocab issues
  - Cohen's kappa with automatic labels treating picks as binary

This script is safe to run even when rater.csv is empty — it will print
a skeleton report saying "n=0 rated so far" so the pipeline is testable
before the real annotation pass.
"""
from __future__ import annotations

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT / "runs" / "iter08_calibration" / "spotcheck"


def load(path: Path) -> list[dict]:
    with path.open() as fh:
        return list(csv.DictReader(fh))


def cohens_kappa(a: list[int], b: list[int]) -> float:
    """Cohen's kappa for two binary label lists."""
    if not a:
        return float("nan")
    n = len(a)
    agree = sum(1 for x, y in zip(a, b) if x == y) / n
    pa = sum(a) / n
    pb = sum(b) / n
    chance = pa * pb + (1 - pa) * (1 - pb)
    if chance >= 1.0:
        return 1.0
    return (agree - chance) / (1 - chance)


def main() -> None:
    rater_rows = load(BASE / "rater.csv")
    truth_rows = load(BASE / "ground_truth.csv")
    truth_by_id = {r["sample_id"]: r for r in truth_rows}

    rated = [r for r in rater_rows if r["rater_judgment"].strip()]
    total = len(rater_rows)

    lines = [
        "# Iter 8c — spot-check agreement analysis",
        "",
        f"- Total triplets: {total}",
        f"- Rated so far: **{len(rated)}**",
        "",
    ]
    if not rated:
        lines += [
            "## Status",
            "rater.csv has not been filled in yet. Re-run this script after",
            "the human rater has annotated `rater.csv`.",
            "",
        ]
        (BASE / "agreement.md").write_text("\n".join(lines) + "\n")
        print("\n".join(lines))
        return

    agree = 0
    both = 0
    neither = 0
    disagree = 0
    per_kind: dict[str, list[int]] = {}
    auto_labels: list[int] = []
    rater_labels: list[int] = []

    for r in rated:
        t = truth_by_id[r["sample_id"]]
        judgment = r["rater_judgment"].strip().upper()
        expected = t["expected_rater_pick"].upper()
        kind = t["kind"]
        per_kind.setdefault(kind, [0, 0])  # [agree, total]
        per_kind[kind][1] += 1
        if judgment == expected:
            agree += 1
            per_kind[kind][0] += 1
            auto_labels.append(1); rater_labels.append(1)
        elif judgment == "BOTH":
            both += 1
            auto_labels.append(1); rater_labels.append(1)
        elif judgment == "NEITHER":
            neither += 1
            auto_labels.append(1); rater_labels.append(0)
        else:
            disagree += 1
            auto_labels.append(1); rater_labels.append(0)

    n = len(rated)
    acc = agree / n
    kappa = cohens_kappa(auto_labels, rater_labels)

    lines += [
        "## Overall",
        "",
        f"- Strict agreement (rater picked same candidate we labeled syn): **{agree}/{n} = {acc:.2%}**",
        f"- 'Both faithful' responses:    {both}/{n}",
        f"- 'Neither faithful' responses: {neither}/{n}",
        f"- Clear disagreements (rater picked opposite): {disagree}/{n}",
        f"- Cohen's kappa (auto-label vs binary-rater): **{kappa:.3f}**",
        "",
        "## Per kind",
        "",
        "| kind | agree | n | rate |",
        "|------|------:|--:|-----:|",
    ]
    for kind, (a, t) in sorted(per_kind.items()):
        lines.append(f"| {kind} | {a} | {t} | {a/t:.2%} |")
    lines += [
        "",
        "## Interpretation",
        "",
        f"Agreement rate of {acc:.0%} is {'strong' if acc >= 0.8 else 'marginal' if acc >= 0.6 else 'weak'} evidence that our automatic",
        "syn/antonym labels encode what a human reader perceives as",
        "meaning direction. Disagreements should be reviewed qualitatively",
        "— they are most likely cases where a synonym we chose is awkward",
        "in context (S04 'took fields' is a known example).",
        "",
    ]
    (BASE / "agreement.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
