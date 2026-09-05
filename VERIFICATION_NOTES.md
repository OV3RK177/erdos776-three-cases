# Erdős problem #776 — verification record (Claude, 2026-09-05)

Dan (with GPT-6) produced a Kruskal–Katona profile argument for n₀(5)=14, n₀(6)=16, n₀(11)=27 and
g(14,5)=10, g(16,6)=12, g(27,11)=23, and asked for a Lean 4 formalization.

## 1. The mathematics is correct (checked independently, `profile_check.py`)
- Cascade shadow function, downward recurrence D_k = a_k + sh_{k+1}(D_{k+1}), capacity test: my own
  implementation reproduces every number in the note (D₃ = 319/497/2709, sh₃ = 87/115/341, D₂ = 92/121/352
  against C(n,2) = 91/120/351; the r=5,n=14 trace 5,55,255,695,1285,1721,1741,1337,769,319,92).
- Necessity proof (C_k = F_k ⊔ ∂C_{k+1}, KK + monotonicity, induction) and sufficiency (colex segments,
  shadow of an initial segment is an initial segment, select ranks sh_{k+1}(D_{k+1})..D_k−1) are sound.
- Exhaustive check: for n ≤ 5 the criterion's feasible profiles equal those realised by ALL antichains
  (3, 6, 20, 168, 7,581 antichains; 3/5/10/26/96 profiles) — matches the note's counts.
- Colex constructions built here and checked by brute-force pairwise containment: r=5 n=15,33; r=6 n=17,35;
  r=11 n=28,47; and the three (n−4)-size boundary families (50/72/253 sets) — all antichains, exact
  multiplicities. Criterion feasible for every n in 15..33 / 17..35 / 28..47.
- He–Tang Prop. 4.1 bound with integer cutoffs B₅=33, B₆=35, B₁₁=47 read from the PDF (arXiv:2602.09803v2,
  lines "n ≥ 2r + 2log₂r + log₂log₂r + 15"); Definition 1.3 is the strict-`n > n₀` convention as stated.
- The criterion alone (plus HT's tail) gives n₀(r) = 2r+4 for r = 4..10 and 2r+5 for r = 11..14 — it also
  explains why He–Tang's 24-hour search found no construction at n = 27 for r = 11: none exists.

## 2. PRIORITY: these three values were already proved and Lean-formalized in July 2026
- erdosproblems.com/776 lists two proof claims. Claim #78 (M. Thiim, 17 July 2026, "AI's operated by
  M. Thiim": ChatGPT 5.6 Pro, Claude Fable 5, Codex) claims the COMPLETE determination
  n₀(r) = 2r+4 (4 ≤ r ≤ 10), 2r+5 (r ≥ 11), with a Lean formalization (github.com/mthiim/erdos_776, tag
  v0.4.1-proof-claim). Its paper contains the identical (27, 11) trace: m₃ = 2709 = C(26,3)+C(15,2)+C(4,1),
  "no 11-multiplicity antichain on [27]", n₀(11) = 27, and certificates/r11_n27_23_levels.txt (our 253-set
  family). Same method: cascade Kruskal–Katona profile criterion + colex constructions + He–Tang's tail.
- Claim #101 (G. Ronen) proves n₀(4) = 12 separately.
- He–Tang themselves have only r = 2, 3 exact and 2r+2 ≤ n₀(r) ≤ 2r + 2log₂r + O(log log r).
- So: the three cases are CORRECT special cases of a result claimed seven weeks earlier by someone else,
  by the same method. Not new. The catalogue still says "open" because nobody has reviewed the claims.

## 3. Lean 4 — what is machine-checked on this box (research/erdos776/erdos_776)
- Thiim's package cloned at the tag; Lean 4.30.0 + Mathlib v4.30.0 (cache); `lake build` 1064 targets,
  exit 0, 11m44s. `lean/AxiomAudit.lean` reproduces the documented allowlist exactly: the symbolic
  endpoints depend on propext / Classical.choice / Quot.sound only; `erdos776_threshold` additionally on
  three generated `native_decide` certificate axioms. No sorry anywhere.
- `KairosCases.lean` (ours): n₀(5)=14, n₀(6)=16, n₀(11)=27 in the published formulation
  (`ProblemThreshold r N`, strict `n > N`), plus the failure/success halves, as corollaries of
  `erdos776_threshold` — compiled, `#print axioms` = the same set as the package endpoint.
  Exact values g(14,5)=10, g(16,6)=12, g(27,11)=23: package upper bound `card_occupiedLevels_le_middle`
  + failure half + our explicit colex witnesses (50/72/253 sets). FINAL: witnesses are `List (List (Fin n))`
  literals mapped to a Finset; the antichain property is decided by an executable list checker `pairwiseOK`
  with a proved soundness lemma `isSperner_of_pairwiseOK`; `native_decide` on the checker and on the
  level counts. Whole file compiles in 3.4 s, exit 0, no sorry (kairos_cases_v4.log). Axioms of g_*: the
  standard three + our three native checks + the package's three certificates.
  Traps hit: (a) a 253-set nested Finset literal `{{0,13},…}` blew maxRecDepth and then 16 GB of RAM in
  elaboration — write `List` literals and map; (b) `native_decide` directly on `∀ a ∈ F, ∀ b ∈ F, a ⊆ b → a = b`
  took 17 s for 50 sets and ran away for 253 (the Decidable instance over Finset/Multiset is what gets
  compiled) — decide a Bool function over lists and prove it sound instead; (c) `pkill`/`pgrep -f` matched my
  own shell twice more; the second stray compile was found only via `ps -eo comm`.
- What would make it OUR formalization rather than corollaries: re-proving the numeric Kruskal–Katona bridge
  (cascade form) — Thiim's `Combinatorics/NumericShadow.lean` etc. already does this; Mathlib has only
  `Finset.kruskal_katona` (initial-segment form) and `kruskal_katona_lovasz_form`.
