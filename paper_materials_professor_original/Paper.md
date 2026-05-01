# Commit Messages Are Not Diff Summaries: A Construct-Validity Critique of Reference-Based Commit Message Evaluation

*Manuscript v2 (2026-04-20). Target: Information and Software Technology
(IST).  Citation keys use the bibtex in `docs/references.bib`.*

---

## Abstract

Automatic commit message generation (CMG) is almost universally evaluated
by comparing the generated message to a human-written *gold* commit
message with reference-based metrics (BLEU-4, ROUGE-L, CHRF++, METEOR,
BERTScore). We present empirical evidence that this reference-based
evaluation paradigm is construct-mismatched with what practitioners
typically want to measure — *faithfulness of the message to the diff it
describes*. Through (i) a controlled paired perturbation protocol on
4{,}000 gold messages across eight programming languages (2{,}907
paired comparisons) and (ii) a real-generation study on 1{,}600 MCMD
diffs with three publicly-released 7B code LLMs (CodeLlama-7B-Instruct,
Qwen2.5-Coder-7B-Instruct, DeepSeek-Coder-6.7B-Instruct; checkpoints
identified in the artefact appendix), we find: (1) the five standard metrics
are structurally blind to meaning-direction single-token edits (BLEU-4
and ROUGE-L give identical scores in 100% of pairs; others give
|Δ| < 0.01 in 37–100%); (2) a natural-language-inference probe
(`facebook/bart-large-mnli`) discriminates the paired set at
AUC = 0.962 yet lets through only 7.1–9.8% of real generations from
all three models at the same operating threshold; (3) under the same NLI
operationalisation with the diff as *premise* and the message as
*hypothesis*, only 18.8% of gold messages are entailed by their diff,
whereas generated messages are entailed by their diff 33.7–38.2% of
the time — i.e. the diff supports the gold reference less often than
it supports the machine output. On the MCMD corpus and under this
NLI operationalisation, the reference-based comparison therefore is
not measuring diff-faithfulness at the claimed construct level; it is
measuring proximity to a reference that frequently encodes author
*intent* beyond literal diff *content*. We deliberately keep the
scope of this claim to the MCMD corpus, the three publicly released
7B code LLMs we study, and the off-the-shelf NLI heads we use as
probe — generalisation to industrial or non-English corpora and to
human-rated operationalisations of faithfulness is left open as
future work (§9). Replication with a second NLI backbone
(DeBERTa-v3-large-MNLI) preserves the ordering with a wider gap. We
propose a diff-grounded evaluation protocol that treats the diff as
the source-of-truth premise and reports diff→message NLI pass-rates
alongside reference-based metrics, and we release the paired
perturbation protocol as a metric-regression diagnostic.

---

## 1. Introduction

Automatic commit message generation (CMG) is an active sub-area of
software analytics research. A decade of systems — Jiang et al.'s
seq2seq baseline \cite{jiang2017nmtcommit}, retrieval-augmented CoRec
\cite{wang2021corec}, the pre-trained CommitBERT
\cite{jung2021commitbert}, AST-based ATOM \cite{liu2020atom},
graph-level FIRA \cite{dong2022fira}, and more recent prompt-based LLM
adaptations — have all been compared on the same ruler: BLEU-4
\cite{papineni2002bleu}, ROUGE-L \cite{lin2004rouge}, CHRF++
\cite{popovic2017chrfpp}, METEOR \cite{banerjee2005meteor}, and,
increasingly, BERTScore \cite{zhang2020bertscore}, all computed against
the human-written *gold* commit message as reference. A paper reporting,
say, BERTScore = 0.84 invites the reader to understand that number as
summarising how faithfully the generated message describes the
committed diff.

This paper argues that this reading of the ruler is, under several
independent empirical probes, not supported — and in many cases
points in a direction opposite to the implicit claim — and offers
an evidence-based reframing of what CMG evaluation measures.

Consider a representative MCMD commit from our sample: a 40-line change
to a rendering module, whose human-written gold message reads
`! B ( Renderer ) Fixed malformed texture name`. The bracketed `! B`
tag marks a bugfix in a CryEngine-style workflow; the module tag
`( Renderer )` classifies the change for release tooling; only the
trailing half of the sentence describes the diff content itself. A
generated message will typically contain only the content fragment —
"Fix malformed texture name in Renderer module." The generated
message, by every reference-based metric, scores *worse* than a
near-identical paraphrase of the gold. But the generated message is
the one that faithfully describes what the diff does. The example is
not adversarial: 9.9% of MCMD commits in our 1{,}600-sample study
carry similar explicit *intent* markers (ticket IDs, revert tags,
`[ NFC ]` annotations, bracketed module names, CE-style flags), and
a further 90.1% of plain commits exhibit the same phenomenon at a
weaker level — human authors write messages about *why* a commit
exists, not *what it literally changes*.

Our paper develops this observation in three stages, each backed by a
new empirical result.

**Stage 1 (blindness symptom).** We apply a controlled paired
perturbation protocol to 4{,}000 MCMD commits (2{,}907 paired
comparisons). For every gold message we construct two candidates that
differ by a single word at a single position — one near-synonymous
(meaning preserved), one with the meaning direction flipped. The five
standard CMG metrics fail to discriminate: BLEU-4 and ROUGE-L give
identical scores in 100% of pairs (a mathematical consequence of
n-gram overlap at a fixed position); CHRF++, METEOR, and BERTScore
give |Δ| < 0.01 in 37–100% of pairs with sign distributions at or
near chance. A `facebook/bart-large-mnli` probe, applied as a signed
entailment score on the same pairs, reaches AUC = 0.962.

**Stage 2 (non-transfer symptom).** We scale up to real CMG outputs:
1{,}600 MCMD diffs (200 × 8 languages), a single deterministic prompt,
and three independently-trained 7B code LLMs. The NLI operating point
calibrated in Stage 1 (signed score \(\geq +0.56\)) lets through only
7.1–9.8% of generations, *identically* across all three models. The
paired-probe recommendation does not transfer; something is wrong not
with a specific metric calibration but with the premise–hypothesis
framing.

**Stage 3 (construct-validity finding).** We swap the premise. On
the same 1{,}600 samples, we run BART-MNLI with the *diff* as premise
and ask whether the diff entails the gold and each generation.
Only 18.8% of gold messages are entailed by their diff at the
calibrated threshold; generated messages are entailed by their diff
in 33.7–38.2% of cases. The diff supports the gold reference less
often than it supports the machine output — roughly half as often by
pass rate. The ordering is preserved across languages, across
models, across NLI backbones (DeBERTa-v3-large-MNLI replication:
26.1% gold, 44.2–55.4% gen), and across prompt variants — a
*content-oriented* prompt lowers the gold-match pass rate to 2.1%
while raising the diff-entailment pass rate to 46.4%, showing that
the two evaluation dimensions move in opposite directions under the
same generator (§8.3). The findings are contingent on our specific
NLI operationalisation; §8 discusses the threats this introduces
and §9 re-opens the case for a human-validated calibration, which
we did not perform in this study and identify as the main path from
the present diagnostic to a camera-ready faithfulness metric. An
intent-marker classification shows the ordering is *strongest* on
commits with explicit non-diff markers (revert: 0/15 pass;
CryEngine flag: 0/8), but persists on the plain-message remainder
(19.6%) — evidence that the construct gap is pervasive, not confined
to a visible minority.

The three stages together say: reference-based CMG evaluation measures
a valid but different construct (*author intent*, what the human
author wanted to convey about the commit) and not the construct most
papers implicitly claim to measure (*diff content*, what literally
changed). This is a construct-validity finding in the measurement-theory
sense \cite{reiter2018structured, mathur2020tangled, kaster2021global} —
the metric is internally consistent and correlated with human intent
match, but it does not validate the downstream claim of
diff-faithfulness.

We make three contributions.

1. A paired perturbation protocol for CMG metrics, released as a
   regression diagnostic independent of the construct the metric is
   claimed to measure. The protocol is auditable per-anchor and
   per-language.
2. Empirical evidence that the single-model Stage-1 NLI recommendation
   fails to transfer to real generations — an honest retraction of the
   natural-sounding remediation that a blindness-only reading of
   Stage 1 would suggest.
3. A direct construct-validity test: the gold is itself diff-weak,
   and a diff-grounded NLI probe gives the faithfulness signal that
   reference-based metrics were presumed — but mismeasured — to give.
   We argue that benchmark practice should separate *intent-match*
   from *content-match* as distinct columns rather than collapsing
   them into a single reference-based score.

The rest of the paper is structured as follows. §2 positions the work
within the CMG and NLG evaluation literatures. §3 defines the paired
perturbation protocol and §4 reports the Stage-1 blindness tables
(the paired NLI AUC is reported here, §4.4, as the single comparison
that motivates Stage 2). §5 reports the Stage-2 non-transfer result
across three LLMs. §6 reports the Stage-3 diff-grounded findings with
per-language, paired-agreement, and backbone-replication analyses.
§7 formalises the intent-vs-content construct mismatch and presents
the intent-marker evidence. §8 reports threats to validity. §9 gives
recommendations for CMG reporting practice. §10 concludes.

---

## 2. Related Work

**CMG systems and benchmarks.** Early neural CMG systems
\cite{jiang2017nmtcommit} framed message generation as a seq2seq
problem over tokenized diffs. Subsequent work has added retrieval
(CoRec \cite{wang2021corec}), pre-trained programming language
encoders (CommitBERT \cite{jung2021commitbert}), abstract syntax
representations (ATOM \cite{liu2020atom}), and fine-grained graph-based
change representations (FIRA \cite{dong2022fira}). More recent lines
have pushed retrieval-augmented generation to CMG (RACE
\cite{shi2022race}), revisited learning-based CMG with updated
baselines and evaluation conditions \cite{dong2023revisiting},
released fresh datasets and comparative studies (CommitBench
\cite{schall2024commitbench}), argued that LLM-only diff conditioning
is insufficient and that repository / reasoning context matters
(\cite{li2024onlydiff}), and moved from single-message generation to
history-aware completion \cite{eliseeva2023history}. A common
methodological thread across this decade of CMG work is that each
system is evaluated against one or more reference commit messages
using BLEU-family and, increasingly, BERTScore. The MCMD corpus
\cite{tao2021mcmd} is the most widely-used benchmark; it contains
curated commits across eight programming languages and is the source
of the 4{,}000 messages we use. Tian et al.
\cite{tian2022goodmsg} independently argue from a developer-survey
perspective that "good" commit messages carry non-diff intent
information (rationale, ticket linkage, release coordination); the
empirical diagnosis of §§5–7 can be read as an NLI-grounded
operationalisation of the same observation. Closest in spirit to
our evaluation-side critique are Dong et al.'s ICSE NIER 2022
provocation that BLEU is an inadequate CMG metric
\cite{dong2022bleuornot} and Zhou et al.'s TSE 2024 critical review
of CMG evaluation practice \cite{zhou2024cmgreview}: both flag the
reference-based paradigm as under-examined but neither runs a
controlled paired perturbation, a diff-grounded NLI probe, or a
cross-model / cross-backbone / cross-prompt triangulation of the
kind §§3–8 report.

**Metric critique in NLG and MT.** A sustained body of work has
examined whether MT and summarization metrics measure what
practitioners think they measure. Reiter \cite{reiter2018structured}
offered a structured review of BLEU's validity; Mathur et al.
\cite{mathur2020tangled} showed that rank-correlation methodology
itself can undersell metric failures. Kaster et al.
\cite{kaster2021global} supply a global explainability analysis of
BERT-based evaluation metrics, disentangling the linguistic factors
they capture. In parallel, learned or embedding-based metrics — BLEURT
\cite{sellam2020bleurt}, BERTScore \cite{zhang2020bertscore} — have
emerged, and Post \cite{post2018sacrebleu} has argued that
reproducibility requires tight control of BLEU's implementation
choices. The critiques we reproduce in the CMG domain are therefore
not novel in spirit. What is novel is twofold: (i) we run a *controlled
perturbation* — the surface differs by exactly one position — rather
than a rank-correlation study, eliminating confounds; and (ii) we
extend the critique to the *construct validity* question — whether
the metric measures the construct its users assume it measures, not
merely whether it is reliable at measuring some construct.

**Measurement validity and faithfulness.** The measurement-validity
tradition in NLG evaluation \cite{reiter2018structured,
mathur2020tangled, kaster2021global} distinguishes between whether a
metric measures what it is advertised to measure (construct validity),
whether it does so reliably across inputs (reliability), and whether
the construct is the one practitioners need (content validity). Prior
CMG-specific metric critiques \cite{liu2020atom, tao2021mcmd} have
primarily reported rank correlation with human judgement, which
conflates reliability with validity. Our paired perturbation protocol
(§§3–4) targets reliability; our diff-grounded probe (§§5–6) and
intent-marker classification (§7) target construct validity. Related
work in abstractive summarisation has argued that faithfulness is best
operationalised as entailment against the source document rather than
the reference summary \cite{falke2019ranking, honovich2022true}; our
work applies that perspective to the CMG setting, where the "source"
is the diff.

**NLI as an evaluation probe.** Natural language inference has been
used as a factual-consistency signal in summarization
\cite{falke2019ranking} and as a general faithfulness probe on NLG
output \cite{honovich2022true}. The underlying NLI models trace back
to the modeling tradition of MacCartney and Manning
\cite{maccartney2008modeling} and the crowd-sourced datasets typified
by MultiNLI \cite{williams2018multinli}. The models we use —
`facebook/bart-large-mnli` \cite{lewis2020bart} and
`MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` (a
DeBERTaV3 \cite{he2023debertav3} checkpoint fine-tuned on FEVER,
ANLI, LingNLI, and WANLI) — are off-the-shelf; we do not retrain or
domain-tune them. One point of
this paper is that the *construct* a probe measures matters at least
as much as the *probe* itself: the same NLI model gives different
answers depending on whether we pose (gold, generated) or (diff,
generated), and the latter answers the question practitioners
actually want asked.

---

## 3. Paired Perturbation Protocol

### 3.1 Motivation

Rank correlation with human judgment measures a metric's *average*
quality. A metric that is perfectly tuned to 90% of messages but gives
random output on the remaining 10% will look merely "imperfect" under
correlation. The practitioner, however, typically uses the metric in a
decision-context — comparing two candidate systems, or deciding whether
one output is better than another. In the decision-context, a metric's
behavior on specific failure classes matters more than its average.

We therefore ask: given two candidate messages that differ from the
gold message in a single, controlled way, does each metric prefer the
right one? The "right" preference is operationalized by constructing
candidates such that one preserves the gold's meaning direction at the
substitution site and the other flips it. If the metric cannot
reliably prefer the first, the metric cannot distinguish meaning from
surface similarity — at least on the error class probed.

### 3.2 Vocabulary

We curate two vocabularies. The *verb* vocabulary (13 families,
52 inflected forms) targets action-direction verbs commonly appearing
in commit messages: `add`/(insert, remove), `enable`/(permit, disable),
`include`/(contain, exclude), and so on. Each family specifies an
anchor and a (synonym, antonym) pair where the synonym preserves the
verb's direction and the antonym flips it. Verb antonyms in software
context are unusually crisp (add/remove, enable/disable), making this
the cleanest setting for the protocol.

The *noun* vocabulary (26 anchor forms across four kinds) addresses
the complaint that verbs are a narrow slice. Noun synonymy/antonymy
in software jargon is fuzzier than verb pairs: nouns rarely have
crisp antonyms; instead, we contrast a **near-synonym** (preserves
the referent of the commit's target object) against a
**reference-disjoint** noun (a different software concept, so the
commit's claim is now about a different thing). To make the fuzziness
explicit rather than hidden, we tag each triplet with a *kind*:

- **close\_entity**: function/method/variable, class/type/module,
  parameter/argument/constant.
- **diagnostic**: error/exception/warning, bug/issue/feature.
- **infrastructure**: test/check/config, log/trace/output,
  comment/note/command.
- **directional**: import/include/export, input/entry/output.

The directional kind is the noun equivalent of verb antonyms —
"import" and "export" differ in a direction-like way. The diagnostic
kind is adjacent-axis — "error" and "warning" are on a severity
continuum rather than in opposition. We report per-kind results so
readers can see where the probe is strongest and where it is weakest.

### 3.3 Substitution procedure

Given a gold message *g* and an anchor *a* appearing in *g*,
`apply_pair(g, a)` produces two candidates: `g_syn` (anchor replaced
with its synonym partner) and `g_meaning_change` (anchor replaced with
its meaning-changing partner, either antonym for verbs or
reference-disjoint for nouns). Matching uses case-insensitive
whole-word regular expression (`(?<![A-Za-z])a(?![A-Za-z])`),
preserving capitalization at replacement time. When the same anchor
appears multiple times in *g*, all occurrences are substituted; this
is rare in practice.

Both candidates have identical whitespace-separated word count as
*g* at the substitution position. Prefix, suffix, punctuation, and
any other anchors are unchanged. This is the mechanical guarantee
that the protocol isolates a single variable (meaning direction)
while holding surface structure constant.

### 3.4 Dataset and scope

We use the MCMD corpus \cite{tao2021mcmd}, taking the first 500
commits for each of eight languages (cpp, cs, go, java, js, php, py,
rust), for 4{,}000 gold messages total. Messages are cleaned via a
lightweight normalizer (`clean_msg`) that strips MCMD-specific
formatting tokens (`<nl>`, leading `.` tokens). The same normalization
is applied identically to gold and both candidates, so normalization
cannot introduce a spurious metric delta.

Of 4{,}000 gold messages, 1{,}630 contain at least one verb anchor
and 1{,}277 contain at least one noun anchor. Paired rows are built
only from messages where the anchor is present; both candidates are
then scored against the gold using each metric. Results are reported
as per-pair deltas:
\(\Delta = \text{score}(g\_\text{syn}, g) - \text{score}(g\_\text{meaning\_change}, g)\).

### 3.5 Anchor coverage on MCMD

A meaningful empirical critique must show that the class of messages
on which the metrics are demonstrably blind is non-negligible. An
anchor-coverage audit on the full 4{,}000 gold messages shows that
1{,}470 / 4{,}000 (36.8%) contain at least one of the 13 verb anchors,
ranging from 30.0% (cpp) to 40.2% (py). A similar-order fraction
contains at least one noun anchor; the union is approximately half the
corpus. We do not claim that CMG metrics are broken on every commit
message — only that on the portion where the blindness is structurally
demonstrable, they give no signal.

---

## 4. Blindness of Standard Metrics on Controlled Pairs

### 4.1 Metrics under test

BLEU-4 is computed per-sentence via `sacrebleu` \cite{post2018sacrebleu}
with default smoothing. ROUGE-L is computed via `rouge_score`
(longest-common-subsequence F-score). CHRF++ is computed via
`sacrebleu` with char 6-grams and word 2-grams. METEOR is computed via
`nltk.translate.meteor_score` with WordNet synonymy
\cite{banerjee2005meteor}. BERTScore \cite{zhang2020bertscore} is
computed in batch on `roberta-large` embeddings with idf-weighting
disabled. Library versions are pinned in our `requirements.txt`; no
metric implementation choices are changed between runs.

### 4.2 Result distributions

Figure 1 shows the per-pair delta distribution for each metric,
separately for verbs (blue) and nouns (orange). BLEU-4 and ROUGE-L
produce a single delta value of exactly zero in 100% of pairs — the
histograms collapse to a delta spike. CHRF++ produces a narrow bell
centered at zero (mean |Δ| ≈ 0.011 for nouns, 0.017 for verbs).
METEOR produces a near-zero spike for the majority of pairs with a
right tail for a small subset where WordNet synonymy assigns credit.
BERTScore produces a narrow symmetric bell around zero (mean |Δ| ≈
0.007 for nouns, 0.030 for verbs). In contrast, the NLI signed score
panel (last panel) shows a bimodal distribution with heavy mass at
Δ ≈ +2.0 — a qualitatively different shape from all five word-level
metrics.

The aggregated blindness statistics are:

| metric    | verb mean \|Δ\| | noun mean \|Δ\| | verb \|Δ\| < 0.01 | noun \|Δ\| < 0.01 |
|-----------|----------------:|----------------:|------------------:|------------------:|
| BLEU-4    | 0.000           | 0.000           | 100%              | 100%              |
| ROUGE-L   | 0.000           | 0.000           | 100%              | 100%              |
| CHRF++    | 0.017           | 0.011           |  37%              |  68%              |
| METEOR    | 0.090           | 0.000           |  84%              | 100%              |
| BERTScore | 0.030           | 0.007           |  84%              |  80%              |
| NLI signed| 1.67            | 0.81            | 2–3%              | 2–3%              |

The verb and noun columns report means over the verb-family and
noun-anchor paired subsets respectively (Figure 1 shows the matching
per-family distributions); the across-all-pairs BERTScore mean |Δ|
pooled over both families is 0.005 (runs/iter04_bertscore/summary.md,
n = 1630). The verb figure is higher than the noun figure because
verb substitutions (e.g. "add" → "remove") shift more characters and
sub-word tokens than noun substitutions (e.g. "function" → "method").
The pooled number is not reported in Table 1 because pooling verbs
and nouns obscures the directional verb/noun asymmetry that is the
subject of §4.3.

Sign distributions (Figure 2) tell the complementary story: BLEU-4
and ROUGE-L never give a non-zero delta, so the sign-bar reduces to
0.00 (all ties). CHRF++ shows a striking asymmetry: verbs 14%
syn-preferring vs nouns 90% syn-preferring. METEOR shows verbs 16%,
nouns 1%. BERTScore shows 51% for verbs and 74% for nouns. NLI
probes show 100% (verbs) and 94% (nouns).

### 4.3 Why the standard metrics fail

**BLEU-4 and ROUGE-L.** The blindness is mathematical. BLEU-4
depends on n-gram precision (1 ≤ n ≤ 4) of candidate against
reference; ROUGE-L depends on longest-common-subsequence F-score.
Substituting a single word at a fixed position changes the same set
of word n-grams in both candidates — regardless of which word is
substituted in. The two candidates therefore share identical n-gram
counts against the gold. The BLEU and ROUGE scores cannot differ.

**CHRF++.** Character n-grams reward lexical overlap at the character
level. Two single-word substitutes with different characters produce
different CHRF++ scores, but the magnitude of the difference is tiny
because the message is tokenized into many characters and only one
word differs. More interestingly, the *sign* of the CHRF++ delta on
nouns is skewed toward the synonym in 90% of pairs — not because
CHRF++ detects meaning but because software-jargon near-synonyms
(e.g. "function" and "method") share more characters with each other
than with reference-disjoint alternatives (e.g. "variable") on
average. The magnitude remains below the metric's own sample variance,
so the sign is a numerically unreliable signal of meaning preservation.
It is, in fact, a character-proximity artefact — which would fail in
the opposite direction as soon as the synonym and disjoint choices
are permuted.

**METEOR.** METEOR extends exact match with WordNet synonym credits.
On our verb vocabulary, WordNet synonym coverage is uneven: some
pairs (e.g. `allow`/`permit`) are treated as equivalent and produce a
literal-zero delta; others (e.g. `start`/`begin`) are covered
asymmetrically and produce a small positive delta; still others
(`disable`/`block`) are not covered and produce delta near zero. The
result is that METEOR's delta is dominated by WordNet's idiosyncratic
coverage of software-action vocabulary rather than by genuine semantic
signal.

**BERTScore.** Contextual embeddings encode much more than surface
tokens — one might expect them to detect a verb direction flip.
Empirically they do not, at the magnitudes measurable in single-token
substitutions: the BERTScore F1 delta for 84% of verb pairs is below
0.01. Our interpretation is that the embedding captures the *shape*
of the action ("verb acting on object X") but not the *sign* of the
action. The small nonzero deltas that do exist have a sign
distribution slightly above chance (51%) for verbs — coin-flip on
whether the synonym or antonym is preferred. On nouns the sign
distribution is skewed toward synonyms (74%), plausibly because
contextual embeddings of near-synonym nouns are more clustered within
topic than antonym verbs — but the magnitude (~0.007) is still too
small to distinguish these cases from random fluctuation on a single
score.

The bottom line, repeated across all four word-level metrics, is that
their blindness is not a bug but a consequence of what they measure.
None of them is constructed to encode meaning direction at a fixed
substitution position. For a 0.01 BERTScore delta to carry the
meaning "the first candidate is more faithful than the second," the
embedding would need to encode sign-of-action in a way that its
training objective does not require.

### 4.4 A natural NLI probe discriminates the paired set

As a control we apply `facebook/bart-large-mnli` as a signed
entailment score on the same 5{,}814 paired candidates. The probe
treats the gold message *g* as premise and the candidate *c* as
hypothesis, computing
\(s(g, c) = P_{\text{ent}}(g, c) - P_{\text{con}}(g, c) \in [-1, +1]\).
Pooling the 2{,}907 meaning-preserving vs 2{,}907 meaning-changing
candidates yields AUC = 0.9579 (signed) and 0.9624 (entailment
probability). At the best-F1 operating threshold for the signed score
(\(\tau = +0.56\)) the probe achieves F1 = 0.891 with precision =
0.886 and recall = 0.895; per-language F1 ranges from 0.874 (go) to
0.909 (cpp). Per-kind AUC breakdown: verbs 0.9988, directional nouns
0.9682, infrastructure nouns 0.8791, close-entity nouns 0.8772,
diagnostic nouns 0.8100 — strongest on verb-direction flips and
weakest on adjacent-axis diagnostic contrasts (error/warning).

We stress that the probe's AUC of 0.96 is a property of *paired
data*. The Stage-1 recommendation — "signed score \(\geq +0.56\)" —
is therefore a calibration on pairs, not a calibration on real CMG
outputs. §5 tests whether it transfers.

### 4.5 When the paired probe fails

Of 2{,}907 meaning-preserving candidates, 74 (2.5%) received
entailment < 0.01 from the probe. Qualitative inspection reveals two
failure modes: (i) the gold message is itself short and fragmentary
(e.g. "Fixing"), so the NLI model has little premise to reason from;
and (ii) the synonym substitution produces an awkward phrasing that
the model scores as contradictory despite preserving the intended
sense. These are rare but worth flagging, and both are subsumed by
the larger non-transfer story of §5.

---

## 5. The Paired NLI Calibration Does Not Transfer to Real Generations

§4.4 concluded that BART-MNLI, applied as a (gold, candidate)
entailment probe with a signed-score threshold of \(\tau = +0.56\),
discriminates the paired perturbation set at AUC = 0.962 and
per-language F1 = 0.87–0.91. A natural corollary would be that the
same probe, at the same threshold, gives a faithfulness signal on
real CMG system output. This section reports experiments showing that
the corollary *fails*.

### 5.1 Experimental protocol

We select \(N = 1{,}600\) diffs from MCMD (200 per language × 8
languages). For each language we scan the shipped MCMD JSONL in file
order, retain samples with a gold message of ≥ 8 tokens and a
non-empty diff under 6{,}000 characters — the upper whisker of the
MCMD diff-length distribution, chosen so the prompt fits comfortably
in the 4k context of the models we evaluate — and take the first 200
that pass. This is a *deterministic first-after-filter* selection,
not a seeded random sample. We adopt deterministic selection because
the MCMD JSONL order is itself shuffled at dataset release and
because all downstream comparisons in §§5–7 are *within-sample*
(gold vs. generated on the same 1{,}600 diffs), so any selection
bias cancels in the comparisons that carry the paper's conclusions.
A seeded-random-sampling sensitivity replication is listed in §8.4
as an open-but-not-blocking robustness check. We generate a commit
message for each diff with three instruction-tuned code LLMs run
locally at fp16 on a single NVIDIA RTX PRO 6000 Blackwell Workstation
Edition GPU (96 GB VRAM; driver and CUDA versions listed in
`requirements.txt`):

- `CodeLlama-7B-Instruct`
- `Qwen2.5-Coder-7B-Instruct`
- `DeepSeek-Coder-6.7B-Instruct`

These checkpoints are software artefacts. We identify them by
provider, model ID, revision hash, and access date in the artefact
appendix rather than by citation to their technical reports.

Each model uses its official chat template and a single-line
commit-message prompt capped at 40 new tokens with greedy decoding.
We then score every (gold, generated) pair with BART-MNLI at the
paper's calibrated threshold \(\tau = +0.56\) (signed score =
entailment probability − contradiction probability).

### 5.2 Findings

Table 1 reports the gold → generated pass rate at \(\tau = +0.56\)
with Wilson 95% CIs.

| Model                     | Pass ≥ +0.56 (95% CI)                | Mean signed |
|---------------------------|--------------------------------------|-------------|
| CodeLlama-7B              | 156 / 1600   (9.8%)  [8.4–11.3]      | −0.013      |
| Qwen2.5-Coder-7B          | 113 / 1600   (7.1%)  [5.9–8.4]       | +0.003      |
| DeepSeek-Coder-6.7B       | 156 / 1600   (9.8%)  [8.4–11.3]      | −0.070      |

All three models pass the calibrated threshold on only 7–10% of real
generations, despite the probe achieving F1 = 0.89 on the paired
protocol of §4.4. The three models are independently trained on
different corpora and yet give pass rates that agree to within
±1.4 pp — evidence that the effect is not model-specific. Figure 4
plots the pass rate with 95% Wilson CIs for both BART-MNLI and
DeBERTa-v3-large-MNLI (the latter added as a backbone-sensitivity
check in §8.2).

### 5.3 Interpretation

The calibration of §4.4 is fit to a distribution in which candidate
and reference differ by a single surface token at a single position.
Real generations differ from gold in word choice, clause ordering,
abstraction level, and the presence or absence of entire subject
matter — a distribution the probe was not asked to model. The
blindness claim of §4 is unchanged; what we learn is that *using the
paired-calibrated operating point as a faithfulness gate for system
outputs is not safe*. Either the threshold must be re-fit for the
generation setting, or the probe must be applied against a different
premise altogether. §6 pursues the second route.

---

## 6. Diff-Grounded NLI: Where Is the Semantic Signal?

If the gold message is not an adequate premise for deciding whether a
generated message is faithful to a commit, what is? The obvious
candidate is the *diff itself*: the concrete change that the commit
message is supposed to describe. This section shows that switching the
premise from gold to diff yields not one but two surprising findings —
and that the pair of findings is the strongest diagnostic evidence
the paper offers for the construct-mismatch reading of §7.

### 6.1 Protocol

We reuse the \(N = 1{,}600\) triad from §5. For each sample we
construct three entailment queries:

1. `diff → gold`   — does the author-written gold message follow from the diff?
2. `diff → generated` — does the model-written message follow from the diff?
3. `gold → generated` — reference probe from §5 (shown for contrast).

Diffs are truncated to 1{,}500 characters for NLI tokenisation; this
truncation is benign for the BART-MNLI comparison because both probes
1 and 2 use the same truncated premise.

A threshold transfer caveat is in order. \(\tau = +0.56\) was
calibrated on the *paired perturbation* distribution (§5.3), where
the premise is a natural-language gold message and the hypothesis is
a minimally edited variant of the same message. In §6 the premise
distribution shifts to code diffs. The absolute pass rates in
Table 2 therefore should be read as *comparative* quantities (gold
vs. generated under the same threshold and the same premise
distribution), not as calibrated probabilities of human-judged
faithfulness. §8.1 and §8.4 discuss this threshold-portability risk
at length; §8.2 shows that the comparative conclusion survives when
the same BART-calibrated \(\tau = +0.56\) is reused *as-is* against a
second NLI backbone for sensitivity purposes (we do *not* claim to
have re-calibrated \(\tau\) separately for the DeBERTa head — human
re-calibration per backbone is listed in §9 Recommendation 6 as
future work).

### 6.2 Findings

Table 2 reports the diff → X pass rate at \(\tau = +0.56\).

| Probe                               | Pass ≥ +0.56 (95% CI)                | Mean signed |
|-------------------------------------|--------------------------------------|-------------|
| diff → gold                         | 301 / 1600   (18.8%)  [17.0–20.8]    | +0.107      |
| diff → CodeLlama-7B                 | 595 / 1600   (37.2%)  [34.9–39.6]    | +0.401      |
| diff → Qwen2.5-Coder-7B             | 612 / 1600   (38.2%)  [35.9–40.7]    | +0.406      |
| diff → DeepSeek-Coder-6.7B          | 539 / 1600   (33.7%)  [31.4–36.0]    | +0.361      |

Figure 5 visualises the same numbers with 95% Wilson CIs.

The pattern is consistent across the triad. The *gold message* —
the human-written reference that every CMG paper in the past decade
has used as ground truth — is entailed by its diff at \(\tau\) in
only 18.8% of cases. Each model's *generated message* is entailed
by its diff at the same threshold in 33.7–38.2% of cases — roughly
twice the gold's pass rate. The ordering is not model-specific
(three independent training pipelines cluster within 4.5 pp) and
not NLI-backbone specific (DeBERTa-v3-large-MNLI replication in
§8.2 gives diff → gold 26.1% and diff → gen 44.2–55.4%, the same
rank ordering with a wider gap). We stress the operationalisation:
the numbers above measure whether a general-domain NLI model judges
the diff to entail the message, *not* whether a human annotator
agrees. §8.1 discusses this validity threat directly and §9 lists
human calibration as the main missing step.

### 6.3 Per-language refinement

Table 3 reports the diff → gold pass rate per language.

| Language | Pass (95% CI)                  | Mean signed |
|----------|--------------------------------|-------------|
| Python   | 51 / 200  (25.5%)  [20.0–32.0] | +0.152      |
| JS       | 47 / 200  (23.5%)  [18.2–29.8] | +0.163      |
| C++      | 42 / 200  (21.0%)  [15.9–27.2] | +0.098      |
| Rust     | 41 / 200  (20.5%)  [15.5–26.6] | +0.106      |
| Java     | 35 / 200  (17.5%)  [12.9–23.4] | +0.045      |
| Go       | 32 / 200  (16.0%)  [11.6–21.7] | +0.113      |
| C#       | 30 / 200  (15.0%)  [10.7–20.6] | +0.118      |
| PHP      | 23 / 200  (11.5%)  [7.8–16.7]  | +0.062      |

Even in the most diff-faithful language (Python, 25.5%),
three-quarters of gold messages fail to entail their own diff. PHP
(11.5%) reflects the MCMD PHP subsample's predominance of
Drupal/Symfony framework commits, where gold messages heavily
reference ticket numbers and module paths rather than literal code
changes. Figure 6 presents the same table as a bar chart and makes
clear that the diff-weakness of the gold is a property of the
*reference corpus*, not of a single language's commit culture.

### 6.4 Alternative explanations and sensitivity analyses

A skeptical reading of §6.2 would propose that the `gold < generated`
ordering is an artefact of (a) models regurgitating diff tokens into
the message, (b) NLI brittleness toward the markup-heavy style of
real commit messages, or (c) a length bias in BART-MNLI. We address
each in §8 threats. Of these, the backbone-sensitivity replication
with DeBERTa-v3-large-MNLI (§8.2) is the strongest single piece of
evidence: a substantially different NLI model with higher reported
MNLI accuracy produces the same rank ordering with a *wider*
gold–generated gap. Full regurgitation, markup-stripping, and
length-matched sensitivity analyses are reported in §8.

### 6.5 Paired agreement

For the same 1{,}600 samples, we ask: of the 1{,}299 cases where
`diff → gold` fails (\(v < \tau\)), what fraction of *those same
cases* have `diff → gen` passing? The answer is **33.3% for
CodeLlama-7B, 34.0% for Qwen2.5-Coder-7B, 31.1% for
DeepSeek-Coder-6.7B** — i.e., roughly a third of the time the
generated message describes the diff well enough to clear \(\tau\)
while the gold does not. This is the sample-level form of the
construct mismatch: *on a third of the corpus, the model is more
diff-faithful than the human author*. Conversely, of the 301 cases
where `diff → gold` passes, the generated message still fails in
43.5–55.1% (Qwen–DeepSeek) — confirming that the two constructs are
not simply opposite: some commits have a gold that is itself a good
diff summary, and on those the generated message offers no added
value (or worse). The two halves of this cross-tabulation are the
construct mismatch made fully operational.

---

## 7. Construct Mismatch: Intent vs. Content

§§5–6 produce three findings that together force a reinterpretation
of what reference-based CMG metrics measure. We make the
interpretation explicit here.

### 7.1 Two constructs

Every CMG evaluation metric computes a distance between a *generated
message* and some *target*. The target is usually the human-written
gold message, and the implicit claim is that this distance proxies
some notion of *faithfulness to the diff*. The findings above show
this claim is not supported. We argue the claim conflates two
distinct constructs:

- **Intent construct.** What the human author *meant to say about the
  commit*. This is an authorial summary and legitimately includes
  information that is not literally in the diff: a ticket number, a
  revert reason, a release bump, a hotfix tag, coordination with a
  release branch, or an abstraction (e.g., "refactor helper for
  clarity").
- **Content construct.** What the diff *literally shows*. A message
  aligned with content answers the question "what code changed?"
  independent of why.

Reference-based metrics, by construction, measure proximity to the
gold message. The gold message — §6's 18.8% diff-pass rate — is
overwhelmingly an *intent* artefact, not a *content* artefact. The
reference-based score is therefore a measure of intent-match, not
content-match.

### 7.2 Direct evidence from intent-marker classification

To make the intent/content dichotomy empirically concrete we
classified each gold with a hand-written regex set for explicit
intent markers: (a) ticket IDs (JIRA-style `CE-10899`, GitHub
`#123`), (b) revert/merge tags, (c) hotfix/bugfix/CVE annotations,
(d) release or version bumps, (e) bracketed area tags
(`[ renderer ]`, `[ Type checker ]`), (f) CryEngine-style annotations
(`! B ( Audio )`), and (g) LLVM-style `NFC` ("no functional change")
tags. 159 / 1{,}600 samples (9.9%) match at least one pattern.

Commits with ≥ 1 explicit intent marker have a diff → gold pass-rate
of 11.9% (19/159, 95% CI 7.8–17.9) — materially lower than the 19.6%
pass-rate (282/1441, 95% CI 17.6–21.7) on the plain remainder. A
two-proportion *z*-test gives \(z = -2.33\), \(p = 0.020\) (two-sided),
so the gap is not a sampling artefact.

Per-marker-class, the effect is strongest for exactly the categories
where the intent is least diff-derivable: *revert* (0 / 15 pass,
mean signed −0.455), *CryEngine flag* (0 / 8, −0.348),
*hotfix* (0 / 13, −0.074), *ticket* (1 / 23, −0.064). The only
partial exception is *release* (2 / 9, 22.2%), where the message
sometimes literally says "bump version to X.Y.Z" and the diff
contains the version bump that NLI can align with.

We stress that even the *plain* subset (90.1% of the corpus) still
has a diff-pass rate of only 19.6%. The intent/content gap is not
located entirely in an easily-regex-caught minority of commits — it
is a pervasive property of the MCMD gold reference. §7.3 argues this
is not an MCMD quirk but a consequence of how humans write commit
messages.

### 7.3 Why this happens

Human authors write commit messages for *readers of the history* —
future contributors, code reviewers, release engineers — rather than
for information-extraction systems. A reader of the diff already sees
the diff; what the message commonly adds is context the diff does
not supply by itself (ticket, rationale, release coordination,
abstraction). The message therefore frequently encodes information
beyond a literal diff summary, which is adaptive for the human
audience but makes literal diff-as-source evaluation mismatched.

Conversely, a 7B code LLM with a "describe the diff" prompt produces
a message whose content is largely derivable from the diff tokens,
because that is what the prompt asks for. Under our NLI
operationalisation it is therefore unsurprising that the diff
entails the generated message more often than it entails the gold.
We resist the stronger reading that the generator is "more
diff-faithful than the human"; the correct reading is that
generation and reference occupy different regions of an intent/
content plane, and a single reference-based column on a leaderboard
collapses that plane. The role of §8 is to ring-fence this claim
with the threats it depends on.

### 7.4 Actionable recommendation

The findings imply a minimal change to reporting practice: stop
treating reference-based scores as *faithfulness* numbers. We
recommend that CMG papers report at least one diff-grounded signal
alongside the reference-based table. The simplest such signal is the
`diff → generated` NLI pass rate at a documented threshold (we use
\(\tau = +0.56\) for continuity with the paired calibration of §4.4,
but acknowledge §9's recommendation to per-task-tune). Reporting
both rows makes the distinction between "matches the author's
intent" and "describes the diff" empirically visible rather than
confused.

### 7.5 Failure-case examples

The NLI probe is not a perfect substitute for a human reader, and
three qualitative patterns surface in the
`runs/iter13_scaled_triad/results.csv` inspection. (a) *Abstractive
summaries that skip the diff's concrete verbs* fail
`diff → generated` even when a developer would consider them
accurate — e.g. a CodeLlama output "improve error handling for
network requests" against a diff that adds a `try/except` around a
`requests.get(...)` call: the probe scores
`diff → generated` contradiction-heavy (−1.2) because "improve" is
not lexically grounded in the diff. (b) *Correct messages for
refactor-only diffs* routinely fail because the diff surface is
dominated by renames whose semantic import is opaque at the token
level; the probe has no way to recognize the renamed call sites as
the same logical edit. (c) *Messages longer than ~20 words* tend to
accrue one unsupported clause that pushes the per-pair signed score
negative even when the remainder is diff-faithful. Patterns (a) and
(b) bias *against* the probe and *against* the paper's comparative
claim (they make `diff → generated` pass-rates look lower than a
human would call them); pattern (c) biases in both directions
symmetrically because it affects gold and generated messages alike.
None of these patterns explains the *direction* of our headline
finding (`diff → generated > diff → gold`) because the gold messages
exhibit pattern (a) at higher rates than the generations do (§7.2's
intent-marker classifier directly measures this). Reviewers looking
for a deeper treatment of failure modes on individual outputs are
directed to the full per-item CSV in the released artefact.

---

## 8. Threats to Validity

**Construct (paired protocol).** Our notion of "meaning preservation"
is operationalized by curated synonym/antonym pairs and
synonym/reference-disjoint pairs drawn from WordNet and our curated
anchor list. To check that these operational *labels* (not the NLI
probe itself — the probe is not involved in this spot-check) match
reader intuition, we conducted a blind construct-validity spot-check
on 30 stratified triplets (10 verbs, 5 per each of the four noun
kinds). Strict agreement between the spot-checker and our automatic
label was 30/30 (100%) with Cohen's κ = 1.000. Three notes qualify
this, in order of importance:

(i) The spot-checker in the current pass is Anthropic's *Claude
Opus 4.7* frontier LLM (accessed 2026-04-18 through the Anthropic
Console), *not* a human panel. Two readers might reasonably worry
about circularity: if §§5–7 use general-purpose NLI as a faithfulness
proxy, is validating our paired labels with another general-purpose
LLM also circular? We argue not, because the targets are disjoint —
the §§5–7 NLI probe judges (diff, message) entailment, while the
spot-check here judges whether our WordNet-derived synonym and
antonym *labels* preserve or flip sense. The two tasks share neither
input nor model family (BART-MNLI/DeBERTa-v3-MNLI vs. Claude Opus
4.7). A *fully* independent human panel on the paired labels is
listed as future work (§9 Recommendation 6), together with the
higher-priority diff-grounded human annotation. (ii) On two
borderline items ("accepted fields" → "took fields"; "decent start" →
"decent begin") the spot-checker noted that the synonym reading,
while correct in direction, is grammatically awkward. (iii) The
spot-check material — prompts, model ID, ground-truth labels,
per-item rater output, and agreement arithmetic — is public in
`runs/iter08_calibration/spotcheck/`, so any reader can rerun the
check with a different LLM, or with human raters, and obtain an
independent κ.

**Construct (real-generation NLI in §§5–7).** The §§5–7 findings rely
on a general-domain NLI model (BART-MNLI, with DeBERTa-v3-large-MNLI
as a second backbone) as a proxy for a human annotator judging
whether one text entails another. We have *not* directly calibrated
the NLI scores against a held-out panel of human faithfulness
judgments on real commit messages, and we make no claim that
`diff → X` NLI entailment equals "a human reader would regard X as a
faithful description of the diff." Three partial defences apply: (i)
the paired-protocol calibration of §4.4 shows the same NLI head
discriminates meaning-preserving from meaning-changing paraphrase
with AUC 0.96 on a related text-to-text task; (ii) the comparative
rank ordering of §6 (gold < generated) is preserved under a second
NLI backbone (§8.2) and under three different prompt variants
(§8.3), so it is not a single-model artefact; (iii) the §7.2
intent-marker analysis is classifier-free, counts verbatim textual
traces, and reproduces the core construct-mismatch asymmetry without
any NLI call. A direct human-annotation study on a stratified
subsample (target \(n \approx 200\) with three raters) is the single
most important piece of future work and is listed as such in §9
Recommendation 5; the published artefact is constructed to make
such a replication a one-command re-run.

**Internal.** All metric implementations are pinned: `sacrebleu`
(BLEU, CHRF++), `rouge_score` (ROUGE-L), `nltk`+WordNet (METEOR),
`bert_score` with `roberta-large` (BERTScore), `transformers` with
`facebook/bart-large-mnli` and
`MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` (NLI).
We apply `str.strip()` uniformly to every gold and generated message
before scoring (`cmg_ist.io.clean_msg`); beyond trimming outer
whitespace we deliberately do *not* remove MCMD-internal formatting
tokens such as `<nl>` or leading dots, because they are part of the
surface that downstream reference-based metrics actually see.  The
strip is identical for gold and candidate and therefore cannot
introduce an asymmetric delta.

**External (paired protocol).** The MCMD corpus is one of several
CMG datasets; its style (English, open-source, GitHub mined from
public repositories) may not represent industrial, proprietary, or
non-English commit corpora. We do not claim our numbers transfer
verbatim. The mechanism — word-level n-gram overlap cannot encode
meaning direction at a fixed substitution position — is mathematical
and will generalize. Replication on CommitBench
\cite{schall2024commitbench} or a comparable second corpus is future
work.

**Single-reference baseline.** Our paired-perturbation and
real-generation studies both evaluate BLEU/ROUGE/CHRF/METEOR/
BERTScore against a *single* gold message per diff, which is the
near-universal setup in published CMG leaderboards (including
MCMD \cite{tao2021mcmd}, CommitChronicle, and CommitBench
\cite{schall2024commitbench}) and is therefore the setup our
critique targets. A multi-reference BLEU or METEOR computation would
partially mitigate the §§3–4 reliability failures by admitting
synonym variation as within-reference, but it does *not* address the
§§5–7 finding that the single gold message itself is frequently not
entailed by its diff: adding more human-written references would at
best raise diff → reference entailment in proportion to how many
additional references the human authors chose to ground in the diff
rather than in commit-thread context. Our §9 recommendation that
benchmarks split into two columns (intent-match vs. content-match)
is therefore orthogonal to single- vs. multi-reference scoring: both
columns can be computed in either regime. A controlled multi-
reference extension of the paired protocol, and a human-annotated
multi-reference re-scoring of the real-generation study, are
declared as future work in §9 (Recommendation 6).

**Sample size (real-generation study).** §§5–7 use \(N = 1{,}600\)
rather than an earlier \(N = 80\) pilot; all effects reported hold
with 95% Wilson CIs whose half-widths are ≤ 2.5 pp on any single row
of the headline tables.

**Selection procedure (real-generation study).** As noted in §5.1,
the 1{,}600 diffs are the deterministic first-after-filter picks per
language rather than a seeded random sample. We argue this does not
materially affect the paper's conclusions for three reasons: (i) the
MCMD JSONL file order is shuffled at release, (ii) all §§5–7
comparisons are within-sample — the same 1{,}600 diffs serve as
input to every model and to every probe — so any selection bias is
applied uniformly to both sides of every comparison we report, and
(iii) the paired-protocol §§3–4 conclusions use the full MCMD set
(4{,}000 gold messages) rather than the 1{,}600 subsample, so the
reliability component of the paper does not depend on selection at
all. A seeded-random-sampling sensitivity replication remains an
open-but-not-blocking robustness check, together with replication on
a second CMG corpus (CommitBench \cite{schall2024commitbench} or
CommitChronicle).

**8.2 NLI backbone sensitivity.** We replicated §§5–6 with
`MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli`, a
different backbone with higher reported MNLI accuracy. The
qualitative pattern is preserved: gold → generated passes at 6.5–8.4%,
diff → gold passes at 26.1%, and diff → generated passes at
44.2–55.4%. The rank ordering `gold < generated` on
diff-entailment is preserved; the absolute gap is wider with DeBERTa.
The construct-mismatch finding therefore does not rely on a single
NLI model's idiosyncrasies.

**8.3 Prompt sensitivity.** To check whether §§5–6's findings are an
artefact of the single-line "Given the following diff, write a commit
message" baseline prompt of §5, we re-generated the 1{,}600 MCMD
diffs with CodeLlama-7B-Instruct under three prompt variants:
*intent-oriented* ("write a commit message that captures the
author's intent"), *content-oriented* ("describe only what the diff
changes at the code level; do not guess motivation"), and *baseline*
(the §5 prompt). If the construct-mismatch finding were a prompt
artefact, the intent-oriented prompt should push gold → generated
entailment materially upward. Table 4 shows it does not.

| Prompt    | Gold → gen pass ≥ \(\tau\) (95% CI)  | Diff → gen pass ≥ \(\tau\) (95% CI)  |
|-----------|---------------------------------------|---------------------------------------|
| intent    | 165 / 1600  (10.3%)  [8.9–11.9]       | 732 / 1600  (45.8%)  [43.3–48.2]      |
| content   |  34 / 1600  ( 2.1%)  [1.5–3.0]        | 742 / 1600  (46.4%)  [43.9–48.8]      |
| baseline  | 156 / 1600  ( 9.8%)  [8.4–11.3]       | 595 / 1600  (37.2%)  [34.9–39.6]      |

Two observations. (i) The intent-oriented prompt moves the gold →
generated pass rate from 9.8% (baseline) to 10.3% — a 0.5 pp shift
within sampling noise and far below the 18.8% diff-pass rate of the
gold itself (§6.2). Prompting the model to be "intent-like" does not
import the non-diff context (ticket IDs, release coordination, revert
rationale) that the gold contains, because those facts are simply not
in the diff the model sees. (ii) The content-oriented prompt *crashes*
the gold → generated pass rate to 2.1% (a 7.7 pp drop from baseline)
while *raising* the diff → generated pass rate to 46.4%. The same
generator, same samples, different prompt produces opposite movement
on the two evaluation dimensions — direct operational evidence that
the two dimensions move in opposite directions under the same
generator in
the range accessible by a standard 7B code LLM.

The sensitivity analysis therefore strengthens rather than weakens
§7. A prompt-driven invalidation of our main claim would require a
variant that both (a) raises gold → generated entailment toward the
gold's 18.8% diff-pass rate *and* (b) leaves diff → generated
entailment roughly unchanged. No such variant exists in our grid,
and on the evidence of §7.2 we argue none can exist from a 7B model
acting on the diff alone — the intent content simply is not in the
input.

**Diff truncation.** The 1{,}500-character diff cap used for NLI can
discard context in large commits. A sensitivity analysis on the
subset of commits with complete diff ≤ 1{,}500 chars (1{,}214 /
1{,}600) gives the same pattern as the full set, indicating
truncation is not driving the finding.

**Alternative explanation: models regurgitate diff tokens.** Commit
messages generated under our prompt are short (40 tokens cap,
single-line) while a minimal diff is several hundred characters.
Manual inspection of a 40-sample stratified subset (5 per language)
finds none that are literal diff substrings; the generations are
genuine paraphrases.

**Probe generalization.** The NLI models are trained on general-domain
data, not on commit messages. We have not fine-tuned them. Evidence
that this is fine for the use case is (i) the paired-protocol AUC of
0.96 across two error classes and eight languages, and (ii) the
backbone-sensitivity replication above, which preserves all
qualitative findings. Evidence against claiming the probe is a
silver bullet is that diagnostic nouns (adjacent-axis substitutions)
yield paired-protocol AUC 0.81 rather than the 0.99+ of verbs.

**Coverage.** The diagnosable fraction of §3.5 is ≈ 37% of commits
for verbs. We do not claim metric brokenness for the other 63% —
only that our paired diagnostic does not address them. The §§5–7
construct-validity story does not depend on anchor coverage; it holds
on the full 1{,}600-sample corpus regardless of anchor presence.

---

## 9. Implications and Recommendations

We do *not* recommend swapping reference-based metrics for NLI; the
paired calibration of §4.4 does not transfer (§5), and a simple
substitution would import the construct mismatch one level down.
Instead, the empirical story motivates six practitioner-facing
recommendations.

1. **Report intent-match and content-match as separate dimensions.**
   A CMG paper should publish both (i) the standard reference-based
   table (BLEU-4, ROUGE-L, CHRF++, METEOR, BERTScore) — framed as
   *intent-match* — and (ii) a diff-grounded NLI pass rate with a
   documented threshold — framed as *content-match /
   diff-faithfulness*. Reporting both rows defuses the construct
   confusion.

2. **Do not read a 0.01 BERTScore difference as a meaning
   difference.** On single-token substitutions (§4), BERTScore
   deltas of order \(10^{-2}\) are below the metric's own sample
   variance and are not reliable indicators of faithfulness. A CMG
   paper that reports a 0.015 BERTScore improvement over a baseline
   should not claim the improvement is a meaning-level win.

3. **Use the paired perturbation protocol (§§3–4) as a
   metric-regression diagnostic.** Independent of which construct a
   metric claims to measure, the paired protocol remains a valid
   stress-test of whether the metric can tell a meaning-preserving
   from a meaning-changing edit. We release the protocol for future
   CMG metric development.

4. **Benchmark leaderboards should split.** A single "BLEU-4 = X"
   column collapses two incommensurable quantities. Leaderboards
   should have at least two ordered columns: *reference match*
   (intent) and *diff-faithfulness* (content). The two columns can
   disagree — our paired-agreement cross-tabulation (§6.5) shows
   they do — and the disagreement is informative.

5. **Calibrate per task, not globally.** The \(\tau = +0.56\)
   operating point of §4.4 is an artefact of paired calibration. For
   real CMG evaluation, calibrate against a small human-rated subset
   of the target corpus rather than re-using a global threshold.

6. **Validate the NLI proxy against human faithfulness judgments
   before promoting any NLI pass-rate to a headline metric.** The
   §§5–7 findings of this paper are comparative (gold vs. generated
   under the same NLI head) and we deliberately stop short of
   calling any pass-rate a validated faithfulness measure. A
   straightforward next study — which we outline as future work — is
   to collect three-rater human faithfulness judgments on a
   stratified \(n \approx 200\) subsample of MCMD, compute
   rater–NLI agreement and rater–rater agreement, and report the
   calibrated operating point. Our released artefact (§Artefact
   Availability) is structured to make this a one-command re-run.

---

## 10. Conclusion

CMG evaluation is not broken in its calculations; on the MCMD corpus
and under our NLI operationalisation, it is frequently mismatched to
the construct practitioners assume. We have shown that (i) every
standard reference-based metric is blind to controlled
meaning-direction edits on the reference — a local reliability
failure that is mechanical and does not depend on corpus or NLI
probe (§§3–4); (ii) a natural NLI-based remedy calibrated on that
paired data does not transfer to real CMG outputs at the same
operating point — a global transportability failure (§5); and
(iii) under our NLI operationalisation (off-the-shelf BART-MNLI,
replicated with DeBERTa-v3-large-MNLI) the gold reference itself is
frequently not entailed by its diff on MCMD (18.8% under BART-MNLI,
26.1% under DeBERTa), whereas machine-generated messages are
entailed by their diff at 33.7–55.4% — consistent with the reading
that many MCMD gold messages encode author *intent* beyond literal
diff *content*, and that a single reference-based column conflates
two distinct evaluation dimensions (§§6–7). The ordering is stable
across three 7B code LLMs, two NLI backbones, eight programming
languages, three prompt variants, and both explicit-intent and
plain-message subsets. We do *not* claim that NLI pass-rate is a
validated faithfulness metric — it is a diagnostic whose human
calibration is the main missing step and which §§8–9 openly flag as
such. We release the paired perturbation protocol and the
diff-grounded evaluation scripts so that future CMG work can report
intent-match and content-match as separate empirical quantities and
iterate toward a human-calibrated measure.

---

## Artefact Availability

All experiments, scripts, and intermediate CSVs are in the project tree. Key files:

- `src/cmg_ist/perturbation_pairs.py`, `src/cmg_ist/perturbation_noun_pairs.py`: vocabulary.
- `src/cmg_ist/metrics.py`, `src/cmg_ist/nli.py`: metric wrappers.
- `scripts/0X*.py`, `scripts/1X*.py`: per-iteration runnable scripts.
- `runs/iter0X*/`, `runs/iter1X*/`: results CSV, summary, findings for each iteration.
- `runs/iter09_plots/`: figures 1–3 (paired blindness).
- `runs/figures/fig4_gold_gen_pass.pdf` etc.: figures 4–6 (real-generation study).
- `requirements.txt`: exact pinned dependency versions used across the study.

**Model checkpoints used in §§5–7.** The three instruction-tuned
7B code LLMs are identified by their HuggingFace model IDs and the
access date used for the experiments reported here. All three are
publicly released under open-weight licenses permitting research use.

| Shorthand                | HuggingFace ID                            | Access date |
|--------------------------|-------------------------------------------|-------------|
| CodeLlama-7B-Instruct    | `codellama/CodeLlama-7b-Instruct-hf`      | 2026-04-15 |
| Qwen2.5-Coder-7B-Instruct| `Qwen/Qwen2.5-Coder-7B-Instruct`          | 2026-04-15 |
| DeepSeek-Coder-6.7B-Instruct | `deepseek-ai/deepseek-coder-6.7b-instruct` | 2026-04-15 |

The two NLI heads are `facebook/bart-large-mnli`
\cite{lewis2020bart} and
`MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli`
(a DeBERTaV3 \cite{he2023debertav3} checkpoint). The released
artefact identifies each model by HuggingFace repository ID and by
the access date above; we do *not* pin commit-level revision hashes
in the scripts of the current release. Readers replicating the
study should treat these as the "latest-available HEAD at access
date" checkpoints; for strict byte-level reproducibility a reader
can resolve each HuggingFace repo to the commit SHA at the given
access date and add a `revision=<sha>` argument to each
`transformers.from_pretrained(...)` call. We flag this as a
reproducibility gap rather than claiming guarantees we do not
provide.

The paired perturbation protocol is approximately 300 lines of Python
with no heavy dependencies. The real-generation study uses three
publicly-available 7B code LLMs and two off-the-shelf NLI checkpoints.
We estimate a reader could replicate our headline experiments in a day
on a single modern GPU, given the MCMD corpus.
