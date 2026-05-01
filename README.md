# CMG/IST — Controlled Perturbation Study of CMG Evaluation Metrics

**Target venue**: Information and Software Technology (IST)
**Status**: Iteration 1 — scaffolding + first smoke experiment
**Independence**: Built from scratch. `CMG/TEMP/` is reference-only, not imported or modified.
**Data**: `Research/Data/CMG/raw/` (symlinked, single source of truth)

## Directory
- `src/cmg_ist/` — core library (perturbations, metrics, io, eval loop)
- `scripts/` — runnable experiments (numbered: `01_...`, `02_...`)
- `configs/` — JSON configs per experiment
- `docs/` — paper plan, RQ notes, iteration logs
- `runs/` — experiment outputs (CSV, logs) — git-ignored if repo'd
- `data/interim/` — preprocessed intermediates (not checked in)

## Iteration log
- `docs/iteration_01_plan.md` — current iteration RQ + design
- After each iteration, append findings and reframing notes.

See `docs/paper_plan_v0.md` for the working paper outline.
