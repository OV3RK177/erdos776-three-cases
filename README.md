# Erdős Problem #776 — three parameter cases, independently derived, machine-checked

**n₀(5) = 14, n₀(6) = 16, n₀(11) = 27**, with the exact boundary values **g(14,5) = 10, g(16,6) = 12, g(27,11) = 23**.

## Status — read this first

These results are **correct and not new**. They are special cases of the complete determination
n₀(r) = 2r+4 for 4 ≤ r ≤ 10 and n₀(r) = 2r+5 for r ≥ 11, posted as
[proof claim #78](https://www.erdosproblems.com/forum/thread/776/proof-claims) by M. Thiim on
**17 July 2026** with a full Lean 4 formalization
([mthiim/erdos_776](https://github.com/mthiim/erdos_776), tag `v0.4.1-proof-claim`), building on
He and Tang ([arXiv:2602.09803](https://arxiv.org/abs/2602.09803)), who determined r = 2, 3 and the
bounds 2r+2 ≤ n₀(r) ≤ 2r + 2log₂r + O(log log r). Claim #101 (G. Ronen) covers n₀(4) = 12.

We arrived at the three values on **5 September 2026** by the same method (cascade Kruskal–Katona
profile criterion, colex constructions, He–Tang Proposition 4.1 for the infinite tail), without
knowledge of claim #78, and discovered the prior claim during the literature check *after* the
derivation. We publish this package because:

1. it is an **independent replication** of the part of claim #78 covering r = 5, 6, 11 — the
   same obstruction traces and the same 253-set family on 27 points appear in Thiim's paper;
2. we **built Thiim's Lean package from source** on our machine (1,064 targets, exit 0) and
   reproduced its axiom audit. This is not the first external build: `coffeewithcolin` reported the
   same result on the claim #78 comment thread on 21 July 2026 — same tag, same commit, 1,064 jobs,
   no `sorry`, and the same axiom allowlist. Ours is an independent second confirmation on
   different hardware, seven weeks later;
3. our three cases are **compiled in Lean 4 as corollaries** of its endpoint theorem, with the
   exact boundary values added via explicit witnesses and a proved soundness lemma.

No priority is claimed. Credit for the theorem belongs to Thiim's package; for the bounds and the
r = 2, 3 cases to He and Tang.

## What is here

| Path | What | Checked how |
|---|---|---|
| `profile_check.py` | Our derivation: cascade shadow function, downward recurrence, obstruction traces, feasibility for r = 2..14, colex constructions, brute-force antichain checks, exhaustive n ≤ 5 comparison | run it |
| `certificates/certificate.json` | 3 obstruction traces + 61 explicit antichains (every n in 15..33 / 17..35 / 28..47, plus the three (n−4)-size boundary families) | `verify_certificate.py` (stdlib only; 1,813,031 pairwise containment tests, 0 failures) |
| `lean/KairosCases.lean` | n₀(5)=14, n₀(6)=16, n₀(11)=27 in the published formulation, plus g(14,5)=10, g(16,6)=12, g(27,11)=23 | compiles against Thiim's package at the tag, 3.4 s, no `sorry`; `#print axioms` in `logs/` |
| `logs/thiim_package_build.log`, `logs/thiim_axiom_audit.log` | Our build of mthiim/erdos_776 @ v0.4.1-proof-claim, Lean 4.30.0 + Mathlib v4.30.0 | exit 0; audit allowlist reproduced |
| `VERIFICATION_NOTES.md` | Working notes, including the priority finding | — |
| `PROVENANCE.md`, `MANIFEST.sha256` (+ `.ots`), `MANIFEST.release1.sha256` (+ `.ots`) | Timeline, attribution, hashes and OpenTimestamps proofs: release1 = the first push (17:10Z), the current manifest adds NOTE.md | `ots verify -f MANIFEST.release1.sha256 MANIFEST.release1.sha256.ots`; `ots verify MANIFEST.sha256.ots` |

## The argument in one paragraph

An r-multiplicity antichain with n−3 occupied sizes must occupy exactly sizes 2..n−2 (He–Tang
Lemma 2.5 / our Section 1). Let C_k be the k-sets lying under some member of size ≥ k; then
C_k = F_k ⊔ ∂C_{k+1}, so with the cascade shadow function sh_k the recurrence
D_k = a_k + sh_{k+1}(D_{k+1}) is a lower bound for |C_k| (Kruskal–Katona + monotonicity), and
D_k > C(n,k) at any rank is a contradiction. For (r,n) = (5,14), (6,16), (11,27) the rank-2
requirement exceeds the pair capacity by exactly one (92 > 91, 121 > 120, 352 > 351). Conversely,
when every capacity holds, choosing colex ranks sh_{k+1}(D_{k+1}) .. D_k−1 at each level gives an
antichain with the requested profile; these families cover every n up to He–Tang's integer cutoffs
B₅=33, B₆=35, B₁₁=47, and Proposition 4.1 covers the rest.

## Reproduce

```bash
python3 profile_check.py                       # derivation + brute-force checks (~1 min)
python3 verify_certificate.py                  # independent verifier of certificate.json
git clone --branch v0.4.1-proof-claim https://github.com/mthiim/erdos_776 && cd erdos_776
lake exe cache get && lake build               # Thiim's package (≈12 min after cache)
cp ../lean/KairosCases.lean . && lake env lean KairosCases.lean
lake env lean lean/AxiomAudit.lean
```

## Trust boundary

The three threshold theorems depend on Lean's standard axioms plus the three `native_decide`
certificate axioms of Thiim's package (documented in its audit). Our exact-value theorems add three
`native_decide` evaluations of our own executable checker (`pairwiseOK`, soundness proved in the
file). Nothing here is peer-reviewed. Claim #78 itself has, as of 5 September 2026, no published
independent review other than this build.

— Kairos Signal, https://kairossignal.com/proofs — Dan Smith with Claude (Fable 5.1) and GPT-6.
