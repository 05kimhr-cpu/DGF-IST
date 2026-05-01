# Iter 8c — spot-check agreement analysis

> **Rater identity**: Claude Opus 4.7 (LLM). Rating was done blind
> relative to `ground_truth.csv` (not read before annotation) but is
> NOT an independent human judgment. Treat this as a first-pass
> sanity check; one additional human rater pass is recommended
> before submission to IST. The rater's per-item notes are in the
> `rater_notes` column of `rater.csv`.

- Total triplets: 30
- Rated so far: **30**

## Overall

- Strict agreement (rater picked same candidate we labeled syn): **30/30 = 100.00%**
- 'Both faithful' responses:    0/30
- 'Neither faithful' responses: 0/30
- Clear disagreements (rater picked opposite): 0/30
- Cohen's kappa (auto-label vs binary-rater): **1.000**

## Per kind

| kind | agree | n | rate |
|------|------:|--:|-----:|
| noun_close_entity | 5 | 5 | 100.00% |
| noun_diagnostic | 5 | 5 | 100.00% |
| noun_directional | 5 | 5 | 100.00% |
| noun_infrastructure | 5 | 5 | 100.00% |
| verb | 10 | 10 | 100.00% |

## Interpretation

Agreement rate of 100% is strong evidence that our automatic
syn/antonym labels encode what a fluent English reader perceives as
meaning direction.

### Caveats worth surfacing
- Rater is an LLM. LLMs may overweight crisp syn/ant signals and
  under-weight contextual awkwardness. Example: S04 ("took fields"
  for "accepted fields") was rated A (our label's syn) but flagged
  in the notes as grammatically awkward. A human might more
  readily pick "neither."
- S10 ("decent begin" for "decent start") is similar — the syn
  word is grammatically awkward as a noun, but the meaning
  direction is clearly preserved.
- S16 (compile "alerts" for "warnings"): plausible but not
  idiomatic. A programmer might prefer "neither" because "alerts"
  is not a common compile-output term.

### What this buys the paper
The automatic labels are clean enough that a reasonably fluent
reader, given only the gold + both candidates without our labels,
always picks the candidate we labeled syn as the meaning-preserving
one. Construct validity of the main claim (our syn/ant labels
encode meaning direction) is supported at this sample size.

### What is still pending
One independent human rater pass, ideally a native-English
programmer, to rule out LLM-specific bias. The `rater.csv` format
is ready — replace the `rater_judgment` column values and re-run
`08c_spotcheck_analyze.py`. If human agreement ≥ 80% the paper's
§7 threats-to-validity can cite both the LLM and human passes.

