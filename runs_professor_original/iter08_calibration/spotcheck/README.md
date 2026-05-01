# Construct-validity spot-check (30 triplets)

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
