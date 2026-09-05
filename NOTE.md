---
title: "Erdős Problem #776: an independent replication of three threshold cases and an external build of Thiim's Lean formalization"
author: "Dan Smith (Kairos Signal), with Claude (Fable 5.1) and GPT-6"
date: 2026-09-05
---

## Summary

For the Erdős–Trotter threshold $n_0(r)$ of problem #776 we derived $n_0(5)=14$, $n_0(6)=16$, $n_0(11)=27$ and the boundary values $g(14,5)=10$, $g(16,6)=12$, $g(27,11)=23$ by the cascade Kruskal–Katona profile criterion, explicit colex constructions up to He–Tang's integer cutoffs $B_5=33$, $B_6=35$, $B_{11}=47$, and He–Tang's Proposition 4.1 for all larger ground sets. These values are special cases of M. Thiim's proof claim #78 (17 July 2026), which determines $n_0(r)$ for every $r\ge4$ with a Lean 4 formalization, by the same method; we became aware of that claim only after the derivation. This note records the replication, an external build of the formalization, and a Lean file deriving our three cases from its endpoint theorem. No priority is claimed.

## The criterion

Let $\mathrm{sh}_k(q)=\sum_i\binom{b_i}{i-1}$ for the canonical expansion $q=\sum_i\binom{b_i}{i}$. For a prescribed profile $(a_k)$ set $D_n=a_n$ and $D_k=a_k+\mathrm{sh}_{k+1}(D_{k+1})$. If $\mathcal C_k$ denotes the $k$-sets below some member of size $\ge k$ of an antichain $\mathcal F$, then $\mathcal C_k=\mathcal F_k\sqcup\partial\mathcal C_{k+1}$, so Kruskal–Katona and monotonicity of $\mathrm{sh}$ give $|\mathcal C_k|\ge D_k$; hence $D_k\le\binom nk$ for all $k$ is necessary. Choosing colex ranks $\mathrm{sh}_{k+1}(D_{k+1}),\dots,D_k-1$ at each level shows it is sufficient. An $r$-multiplicity antichain with $n-3$ occupied sizes must occupy exactly $2,\dots,n-2$ (He–Tang, Lemma 2.5), so the full profile $a_k=r$ on $2\le k\le n-2$ decides $g(n,r)=n-3$.

## The three obstructions

| $r$ | $n$ | $D_3$ | $\mathrm{sh}_3(D_3)$ | $D_2$ | $\binom n2$ |
|---|---|---|---|---|---|
| 5 | 14 | 319 | 87 | 92 | 91 |
| 6 | 16 | 497 | 115 | 121 | 120 |
| 11 | 27 | 2709 | 341 | 352 | 351 |

Each fails by exactly one pair. Constructions exist for every $n$ in $15..33$, $17..35$, $28..47$ (61 explicit families, 1,813,031 pairwise containment checks, `verify_certificate.py`), and Proposition 4.1 covers $n\ge B_r$. The $(n-4)$-size families at the three obstruction points give the boundary values. For $n\le5$ the criterion's feasible profiles coincide with those of all $3, 6, 20, 168, 7581$ antichains.

## Relation to prior work

He and Tang (arXiv:2602.09803) proved $n_0(2)=3$, $n_0(3)=8$ and $2r+2\le n_0(r)\le 2r+2\log_2 r+O(\log\log r)$; they report finding no construction at $n=2r+5$ for $r=11$ in 24 hours, which the criterion explains: none exists. Thiim's package proves $n_0(r)=2r+4$ for $4\le r\le10$ and $2r+5$ for $r\ge11$; its paper contains the $(27,11)$ trace above. The criterion alone reproduces that formula for $r=4,\dots,14$ given the He–Tang tail.

## Machine checking

Thiim's package (tag `v0.4.1-proof-claim`) was built from source on Lean 4.30.0 with Mathlib v4.30.0: 1,064 targets, exit 0. Its `lean/AxiomAudit.lean` reproduces the documented allowlist: the symbolic endpoints depend on `propext`, `Classical.choice`, `Quot.sound`; `erdos776_threshold` additionally on three `native_decide` certificate axioms; no `sorry`. Our `KairosCases.lean` states `ProblemThreshold 5 14`, `ProblemThreshold 6 16`, `ProblemThreshold 11 27` in the package's published formulation as corollaries, and proves the boundary values from the package's occupied-level bound, the failure half, and explicit witnesses whose antichain property is decided by an executable list checker with a proved soundness lemma. It compiles in 3.4 s without `sorry`.

## Availability

https://github.com/OV3RK177/erdos776-three-cases — derivation, certificate and verifier, Lean file, build and audit logs, and a manifest of SHA-256 hashes stamped with OpenTimestamps.
