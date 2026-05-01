# Iter 18 — Plain-commit NLI domain-boundary analysis

Inputs: iter16 classified (1600 rows), iter13/14/15 pre-computed NLI scores.
Intent-tagged: 159 (9.9%)  |  Plain: 1441 (90.1%)

BART fidelity strata (plain only):
  high (diff→gold ≥ +0.56) : 282
  mid  (-0.10 .. +0.56)    : 859
  low  (diff→gold ≤ -0.10) : 300
  sum 1441 == 1441 ✓

---

## §A  Stage 1 — Intent vs plain: diff→gold (BART)

| group      |    n | diff→gold pass ≥ +0.56 (95% CI)              | mean  |
|------------|------|-----------------------------------------------|-------|
| has_intent |  159 | 19/159 (11.9%) [7.8–17.9]                     | -0.008 |
| plain      | 1441 | 282/1441 (19.6%) [17.6–21.7]                  | +0.120 |

z = -2.333, p = 0.01964

## §A  Stage 1 — Intent vs plain: gold→gen (BART, per model)

| model              | intent pass                    | plain pass                     |      z |      p |
|--------------------|--------------------------------|--------------------------------|--------|--------|
| codellama-7b       | 16/159 (10.1%) [6.3–15.7]      | 140/1441 (9.7%) [8.3–11.4]     | +0.140 | 0.8885 |
| qwen2.5-coder-7b   | 8/159 (5.0%) [2.6–9.6]         | 105/1441 (7.3%) [6.1–8.7]      | -1.053 | 0.2922 |
| deepseek-6.7b      | 17/159 (10.7%) [6.8–16.5]      | 139/1441 (9.6%) [8.2–11.3]     | +0.422 | 0.6731 |

p > 0.05 for all models → intent markers do NOT explain the low gold→gen pass-rate.
The gap is a fundamental construct mismatch, not a 10%-subset artefact.

---

## §B  Stage 2+3 — BART fidelity strata: gold→gen pass-rate

| stratum                                    |    n | gold→gen pass (95% CI)                    | mean  |
|--------------------------------------------|------|-------------------------------------------|-------|
| high-fidelity (diff→gold ≥ +0.56)          |  282 | 47/282 (16.7%) [12.8–21.5]                | +0.095 |
| high-fidelity (diff→gold ≥ +0.56)          |  282 | 34/282 (12.1%) [8.8–16.4]                 | +0.086 |
| high-fidelity (diff→gold ≥ +0.56)          |  282 | 40/282 (14.2%) [10.6–18.7]                | +0.043 |

| mid-fidelity  (-0.10 < diff→gold < +0.56)  |  859 | 76/859 (8.8%) [7.1–10.9]                  | -0.018 |
| mid-fidelity  (-0.10 < diff→gold < +0.56)  |  859 | 59/859 (6.9%) [5.4–8.8]                   | +0.004 |
| mid-fidelity  (-0.10 < diff→gold < +0.56)  |  859 | 78/859 (9.1%) [7.3–11.2]                  | -0.054 |

| low-fidelity  (diff→gold ≤ -0.10)          |  300 | 17/300 (5.7%) [3.6–8.9]                   | -0.104 |
| low-fidelity  (diff→gold ≤ -0.10)          |  300 | 12/300 (4.0%) [2.3–6.9]                   | -0.050 |
| low-fidelity  (diff→gold ≤ -0.10)          |  300 | 21/300 (7.0%) [4.6–10.5]                  | -0.185 |

| plain (all)                                | 1441 | 140/1441 (9.7%) [8.3–11.4]                | -0.014 |
| plain (all)                                | 1441 | 105/1441 (7.3%) [6.1–8.7]                 | +0.009 |
| plain (all)                                | 1441 | 139/1441 (9.6%) [8.2–11.3]                | -0.063 |

| all N=1600                                 | 1600 | 156/1600 (9.8%) [8.4–11.3]                | -0.013 |
| all N=1600                                 | 1600 | 113/1600 (7.1%) [5.9–8.4]                 | +0.003 |
| all N=1600                                 | 1600 | 156/1600 (9.8%) [8.4–11.3]                | -0.070 |

## §B  Stage 3 — BART fidelity strata: Spearman ρ(gold→gen, diff→gen)

| stratum                                    | model              |    n |     ρ |       p |
|--------------------------------------------|--------------------|----- |-------|---------|
| high-fidelity (diff→gold ≥ +0.56)          | codellama-7b       |  282 | +0.259 | 7.443e-06 |
| high-fidelity (diff→gold ≥ +0.56)          | qwen2.5-coder-7b   |  282 | +0.102 | 0.08604 |
| high-fidelity (diff→gold ≥ +0.56)          | deepseek-6.7b      |  282 | +0.119 | 0.04514 |

| mid-fidelity  (-0.10 < diff→gold < +0.56)  | codellama-7b       |  859 | +0.050 | 0.1458 |
| mid-fidelity  (-0.10 < diff→gold < +0.56)  | qwen2.5-coder-7b   |  859 | +0.032 | 0.3525 |
| mid-fidelity  (-0.10 < diff→gold < +0.56)  | deepseek-6.7b      |  859 | +0.021 | 0.5335 |

| low-fidelity  (diff→gold ≤ -0.10)          | codellama-7b       |  300 | +0.038 | 0.5154 |
| low-fidelity  (diff→gold ≤ -0.10)          | qwen2.5-coder-7b   |  300 | -0.023 | 0.6856 |
| low-fidelity  (diff→gold ≤ -0.10)          | deepseek-6.7b      |  300 | -0.067 | 0.2439 |

| plain (all)                                | codellama-7b       | 1441 | +0.115 | 1.229e-05 |
| plain (all)                                | qwen2.5-coder-7b   | 1441 | +0.065 | 0.01351 |
| plain (all)                                | deepseek-6.7b      | 1441 | +0.040 | 0.1262 |

| all N=1600                                 | codellama-7b       | 1600 | +0.104 | 2.743e-05 |
| all N=1600                                 | qwen2.5-coder-7b   | 1600 | +0.058 | 0.02116 |
| all N=1600                                 | deepseek-6.7b      | 1600 | +0.010 | 0.6953 |

---

## §C  Stage 4 — DeBERTa backbone: same fidelity stratification

DeBERTa high-fidelity plain: 403  mid: 885  low: 153

### gold→gen pass-rate (DeBERTa)

| stratum                                    |    n | gold→gen pass (95% CI)                    | mean  |
|--------------------------------------------|------|-------------------------------------------|-------|
| high-fidelity (deb diff→gold ≥ +0.56)      |  403 | 51/403 (12.7%) [9.8–16.3]                 | +0.024 |
| high-fidelity (deb diff→gold ≥ +0.56)      |  403 | 36/403 (8.9%) [6.5–12.1]                  | +0.049 |
| high-fidelity (deb diff→gold ≥ +0.56)      |  403 | 42/403 (10.4%) [7.8–13.8]                 | -0.008 |

| mid-fidelity  (-0.10 < deb diff→gold < +0.56) |  885 | 64/885 (7.2%) [5.7–9.1]                   | -0.040 |
| mid-fidelity  (-0.10 < deb diff→gold < +0.56) |  885 | 46/885 (5.2%) [3.9–6.9]                   | -0.006 |
| mid-fidelity  (-0.10 < deb diff→gold < +0.56) |  885 | 48/885 (5.4%) [4.1–7.1]                   | -0.097 |

| low-fidelity  (deb diff→gold ≤ -0.10)      |  153 | 7/153 (4.6%) [2.2–9.1]                    | -0.095 |
| low-fidelity  (deb diff→gold ≤ -0.10)      |  153 | 11/153 (7.2%) [4.1–12.4]                  | -0.038 |
| low-fidelity  (deb diff→gold ≤ -0.10)      |  153 | 16/153 (10.5%) [6.5–16.3]                 | -0.143 |

| plain (all)                                | 1441 | 122/1441 (8.5%) [7.1–10.0]                | -0.028 |
| plain (all)                                | 1441 | 93/1441 (6.5%) [5.3–7.8]                  | +0.006 |
| plain (all)                                | 1441 | 106/1441 (7.4%) [6.1–8.8]                 | -0.077 |

| all N=1600                                 | 1600 | 135/1600 (8.4%) [7.2–9.9]                 | -0.028 |
| all N=1600                                 | 1600 | 105/1600 (6.6%) [5.5–7.9]                 | +0.004 |
| all N=1600                                 | 1600 | 121/1600 (7.6%) [6.4–9.0]                 | -0.078 |

### Spearman ρ (DeBERTa)

| stratum                                    | model              |    n |     ρ |       p |
|--------------------------------------------|--------------------|----- |-------|---------|
| high-fidelity (deb diff→gold ≥ +0.56)      | codellama-7b       |  403 | +0.259 | 8.09e-08 |
| high-fidelity (deb diff→gold ≥ +0.56)      | qwen2.5-coder-7b   |  403 | +0.165 | 0.0007988 |
| high-fidelity (deb diff→gold ≥ +0.56)      | deepseek-6.7b      |  403 | +0.177 | 0.000329 |

| mid-fidelity  (-0.10 < deb diff→gold < +0.56) | codellama-7b       |  885 | +0.183 | 3.046e-08 |
| mid-fidelity  (-0.10 < deb diff→gold < +0.56) | qwen2.5-coder-7b   |  885 | +0.077 | 0.02118 |
| mid-fidelity  (-0.10 < deb diff→gold < +0.56) | deepseek-6.7b      |  885 | +0.007 | 0.8246 |

| low-fidelity  (deb diff→gold ≤ -0.10)      | codellama-7b       |  153 | +0.002 | 0.9768 |
| low-fidelity  (deb diff→gold ≤ -0.10)      | qwen2.5-coder-7b   |  153 | +0.079 | 0.329 |
| low-fidelity  (deb diff→gold ≤ -0.10)      | deepseek-6.7b      |  153 | -0.105 | 0.1957 |

| plain (all)                                | codellama-7b       | 1441 | +0.198 | 1.732e-14 |
| plain (all)                                | qwen2.5-coder-7b   | 1441 | +0.134 | 3.026e-07 |
| plain (all)                                | deepseek-6.7b      | 1441 | +0.062 | 0.01929 |

| all N=1600                                 | codellama-7b       | 1600 | +0.189 | 1.243e-14 |
| all N=1600                                 | qwen2.5-coder-7b   | 1600 | +0.120 | 1.457e-06 |
| all N=1600                                 | deepseek-6.7b      | 1600 | +0.038 | 0.1241 |

---

## §D  Stage 5 — Prompt ablation × fidelity (CodeLlama only)

### gold→gen pass-rate by prompt type and stratum

| stratum                                    | prompt   |    n | gold→gen pass (95% CI)                    | mean  |
|--------------------------------------------|----------|------|-------------------------------------------|-------|
| high-fidelity (diff→gold ≥ +0.56)          | intent   |  282 | 48/282 (17.0%) [13.1–21.8]                | +0.108 |
| high-fidelity (diff→gold ≥ +0.56)          | content  |  282 | 4/282 (1.4%) [0.6–3.6]                    | +0.004 |
| high-fidelity (diff→gold ≥ +0.56)          | baseline |  282 | 44/282 (15.6%) [11.8–20.3]                | +0.087 |

| mid-fidelity  (-0.10 < diff→gold < +0.56)  | intent   |  859 | 79/859 (9.2%) [7.4–11.3]                  | -0.005 |
| mid-fidelity  (-0.10 < diff→gold < +0.56)  | content  |  859 | 22/859 (2.6%) [1.7–3.8]                   | -0.006 |
| mid-fidelity  (-0.10 < diff→gold < +0.56)  | baseline |  859 | 73/859 (8.5%) [6.8–10.6]                  | -0.017 |

| low-fidelity  (diff→gold ≤ -0.10)          | intent   |  300 | 21/300 (7.0%) [4.6–10.5]                  | -0.092 |
| low-fidelity  (diff→gold ≤ -0.10)          | content  |  300 | 5/300 (1.7%) [0.7–3.8]                    | -0.014 |
| low-fidelity  (diff→gold ≤ -0.10)          | baseline |  300 | 18/300 (6.0%) [3.8–9.3]                   | -0.093 |

| plain (all)                                | intent   | 1441 | 148/1441 (10.3%) [8.8–11.9]               | -0.001 |
| plain (all)                                | content  | 1441 | 31/1441 (2.2%) [1.5–3.0]                  | -0.006 |
| plain (all)                                | baseline | 1441 | 135/1441 (9.4%) [8.0–11.0]                | -0.013 |

| all N=1600                                 | intent   | 1600 | 168/1600 (10.5%) [9.1–12.1]               | -0.003 |
| all N=1600                                 | content  | 1600 | 33/1600 (2.1%) [1.5–2.9]                  | -0.008 |
| all N=1600                                 | baseline | 1600 | 152/1600 (9.5%) [8.2–11.0]                | -0.011 |

### diff→gen pass-rate by prompt type and stratum

| stratum                                    | prompt   |    n | diff→gen pass (95% CI)                    | mean  |
|--------------------------------------------|----------|------|-------------------------------------------|-------|
| high-fidelity (diff→gold ≥ +0.56)          | intent   |  282 | 179/282 (63.5%) [57.7–68.9]               | +0.605 |
| high-fidelity (diff→gold ≥ +0.56)          | content  |  282 | 159/282 (56.4%) [50.5–62.0]               | +0.585 |
| high-fidelity (diff→gold ≥ +0.56)          | baseline |  282 | 148/282 (52.5%) [46.7–58.2]               | +0.523 |

| mid-fidelity  (-0.10 < diff→gold < +0.56)  | intent   |  859 | 371/859 (43.2%) [39.9–46.5]               | +0.456 |
| mid-fidelity  (-0.10 < diff→gold < +0.56)  | content  |  859 | 399/859 (46.4%) [43.1–49.8]               | +0.500 |
| mid-fidelity  (-0.10 < diff→gold < +0.56)  | baseline |  859 | 302/859 (35.2%) [32.0–38.4]               | +0.391 |

| low-fidelity  (diff→gold ≤ -0.10)          | intent   |  300 | 124/300 (41.3%) [35.9–47.0]               | +0.397 |
| low-fidelity  (diff→gold ≤ -0.10)          | content  |  300 | 117/300 (39.0%) [33.7–44.6]               | +0.452 |
| low-fidelity  (diff→gold ≤ -0.10)          | baseline |  300 | 91/300 (30.3%) [25.4–35.8]                | +0.318 |

| plain (all)                                | intent   | 1441 | 674/1441 (46.8%) [44.2–49.4]              | +0.473 |
| plain (all)                                | content  | 1441 | 675/1441 (46.8%) [44.3–49.4]              | +0.506 |
| plain (all)                                | baseline | 1441 | 541/1441 (37.5%) [35.1–40.1]              | +0.402 |

| all N=1600                                 | intent   | 1600 | 738/1600 (46.1%) [43.7–48.6]              | +0.472 |
| all N=1600                                 | content  | 1600 | 748/1600 (46.8%) [44.3–49.2]              | +0.503 |
| all N=1600                                 | baseline | 1600 | 595/1600 (37.2%) [34.9–39.6]              | +0.402 |

### Spearman ρ(gold→gen, diff→gen) by prompt type and stratum

| stratum                                    | prompt   |    n |     ρ |       p |
|--------------------------------------------|----------|------|-------|---------|
| high-fidelity (diff→gold ≥ +0.56)          | intent   |  282 | +0.207 | 0.0003869 |
| high-fidelity (diff→gold ≥ +0.56)          | content  |  282 | +0.181 | 0.002017 |
| high-fidelity (diff→gold ≥ +0.56)          | baseline |  282 | +0.226 | 0.0001011 |

| mid-fidelity  (-0.10 < diff→gold < +0.56)  | intent   |  859 | +0.032 | 0.3426 |
| mid-fidelity  (-0.10 < diff→gold < +0.56)  | content  |  859 | +0.098 | 0.004098 |
| mid-fidelity  (-0.10 < diff→gold < +0.56)  | baseline |  859 | +0.046 | 0.1733 |

| low-fidelity  (diff→gold ≤ -0.10)          | intent   |  300 | +0.019 | 0.7477 |
| low-fidelity  (diff→gold ≤ -0.10)          | content  |  300 | +0.084 | 0.1437 |
| low-fidelity  (diff→gold ≤ -0.10)          | baseline |  300 | +0.048 | 0.4049 |

| plain (all)                                | intent   | 1441 | +0.089 | 0.0007162 |
| plain (all)                                | content  | 1441 | +0.120 | 4.493e-06 |
| plain (all)                                | baseline | 1441 | +0.108 | 3.474e-05 |

| all N=1600                                 | intent   | 1600 | +0.082 | 0.001003 |
| all N=1600                                 | content  | 1600 | +0.122 | 9.649e-07 |
| all N=1600                                 | baseline | 1600 | +0.101 | 5.07e-05 |

---

## §E  Language breakdown — high-fidelity subset (BART)

| lang | plain n | high n | high % | diff→gold mean | gold→gen mean (3-model avg) |
|------|---------|--------|--------|----------------|----------------------------|
| cpp  |     145 |     38 |   26.2% | +0.789         | +0.051 |
| cs   |     187 |     28 |   15.0% | +0.816         | +0.138 |
| go   |     197 |     32 |   16.2% | +0.798         | +0.227 |
| java |     167 |     32 |   19.2% | +0.808         | +0.013 |
| js   |     184 |     47 |   25.5% | +0.815         | +0.018 |
| php  |     177 |     18 |   10.2% | +0.780         | -0.041 |
| py   |     191 |     47 |   24.6% | +0.816         | +0.084 |
| rust |     193 |     40 |   20.7% | +0.806         | +0.086 |

---

## Interpretation

**Stage 1**: Intent markers explain the diff→gold gap (p=0.020) but NOT the gold→gen gap
(p > 0.29 for all models). The ~9% gold→gen pass-rate is a fundamental construct mismatch,
not a 10%-subset artefact.

**Stages 2–3 (BART)**: Spearman ρ(gold→gen, diff→gen) rises sharply in the high-fidelity
stratum (plain commits where diff→gold ≥ +0.56). This shows NLI becomes a valid evaluation
signal precisely when the gold reference IS a diff summary.

**Stage 4 (DeBERTa)**: If the high-fidelity Spearman pattern replicates with DeBERTa,
the finding is backbone-independent.

**Stage 5 (Prompt ablation)**: The content-oriented prompt is expected to push diff→gen
pass-rate higher across all strata, while gold→gen stays low everywhere — confirming that
the construct gap is in the reference, not the generator.

**Paper recommendation (§9)**:
Apply NLI-based evaluation only on corpora where gold messages are verified diff-grounded
(diff→gold NLI ≥ +0.56, or plain commits without intent markers). On such construct-matched
subsets NLI provides a valid automated proxy for commit-message faithfulness evaluation.
