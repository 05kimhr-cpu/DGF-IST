# Paper Materials Manifest

Canonical result source: `runs_professor_original/`

Do not use `runs/` for paper tables or figures. The local rerun results differ from the professor-provided original results because the model source/environment differed.

## Writing Files

- `Paper.md`: current manuscript draft.
- `docs/references.bib`: bibliography for the manuscript.
- `README.md`: project overview.
- `requirements.txt`: Python package requirements used by the project.

## Canonical Result Files

Use these summaries for paper numbers:

- `runs_professor_original/iter03_paired_all/summary.md`: standard metrics on verb perturbation pairs.
- `runs_professor_original/iter04_bertscore/summary.md`: BERTScore perturbation results.
- `runs_professor_original/iter05_anchor_coverage/summary.md`: anchor coverage in MCMD.
- `runs_professor_original/iter05b_nli/summary.md`: BART-MNLI controlled-pair discrimination.
- `runs_professor_original/iter07_noun/summary.md`: noun perturbation results.
- `runs_professor_original/iter08_calibration/summary.md`: NLI calibration and threshold selection.
- `runs_professor_original/iter13_scaled_triad/summary.md`: main 1,600-sample three-model result.
- `runs_professor_original/iter14_deberta_sanity/summary.md`: DeBERTa NLI-backbone sensitivity.
- `runs_professor_original/iter15_prompt_ablation/summary.md`: prompt-sensitivity ablation.
- `runs_professor_original/iter16_intent_classifier/summary.md`: intent-marker classification.

## Main Figures

- `runs_professor_original/iter09_plots/fig1_delta_panel.png`: controlled perturbation delta distributions.
- `runs_professor_original/iter09_plots/fig2_sign_bars.png`: metric sign distributions.
- `runs_professor_original/iter09_plots/fig3_nli_per_kind.png`: NLI results by perturbation kind.
- `runs_professor_original/figures/fig4_gold_gen_pass.png` and `.pdf`: gold-to-generated pass rates.
- `runs_professor_original/figures/fig5_diff_x_pass.png` and `.pdf`: diff-to-gold/generated pass rates.
- `runs_professor_original/figures/fig6_diff_gold_per_lang.png` and `.pdf`: per-language diff-to-gold pass rates.

## Reproducibility Files

- `scripts/`: experiment scripts.
- `src/`: project library code.
- `configs/`: configuration files.
- `runs_professor_original/**/results.csv`: per-row result tables.
- `runs_professor_original/**/run.log`: available execution logs.
- `runs_professor_original/**/generations*.jsonl`: model generations used by original runs.

## Paper Result Priority

For manuscript tables, prioritize:

1. `iter13_scaled_triad` for the main result.
2. `iter14_deberta_sanity` for NLI-backbone sensitivity.
3. `iter15_prompt_ablation` for prompt sensitivity.
4. `iter16_intent_classifier` for intent-vs-content explanation.
5. `iter03` to `iter08` for the controlled metric-blindness and calibration sections.
