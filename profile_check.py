#!/usr/bin/env python3
"""Independent check of the Erdos-776 profile argument (2026-09-05). Exact integers only."""
from math import comb
from itertools import combinations
import json, sys

def cascade(q, k):
    """canonical k-binomial expansion of q>0: list of (b_i, i), b_k > b_{k-1} > ... >= i >= 1"""
    out = []; i = k
    while q > 0 and i >= 1:
        b = i
        while comb(b + 1, i) <= q: b += 1
        out.append((b, i)); q -= comb(b, i); i -= 1
    assert q == 0
    for (b1, i1), (b2, i2) in zip(out, out[1:]): assert b1 > b2 and i1 == i2 + 1 and b2 >= i2
    return out

def sh(q, k):
    if q == 0: return 0
    return sum(comb(b, i - 1) for b, i in cascade(q, k))

def trace(n, r, ranks=None):
    a = {k: (r if 2 <= k <= n - 2 else 0) for k in range(n + 1)} if ranks is None else ranks
    D = {}; D[n] = a[n]
    for k in range(n - 1, -1, -1): D[k] = a[k] + sh(D[k + 1], k + 1)
    ok = all(D[k] <= comb(n, k) for k in range(n + 1))
    return D, ok

# --- the three obstruction traces
for r, n, D3, s3, D2 in ((5, 14, 319, 87, 92), (6, 16, 497, 115, 121), (11, 27, 2709, 341, 352)):
    D, ok = trace(n, r)
    print(f"r={r} n={n}: D3={D[3]} sh3={sh(D[3],3)} D2={D[2]} C(n,2)={comb(n,2)} feasible={ok}  matches note: {(D[3],sh(D[3],3),D[2])==(D3,s3,D2)}")
    first_fail = [k for k in range(n, -1, -1) if D[k] > comb(n, k)]
    print(f"   ranks violating capacity: {first_fail}")
print("r=5 n=14 full trace:", [trace(14,5)[0][k] for k in range(12,1,-1)])

# --- feasibility of the full profile for a range of n, and the (n-4)-size boundary profile
def full_ok(n, r): return trace(n, r)[1]
def boundary_ok(n, r):
    a = {k: (r if 2 <= k <= n - 3 else 0) for k in range(n + 1)}; return trace(n, r, a)[1]
for r, lo, hi in ((5, 15, 33), (6, 17, 35), (11, 28, 47)):
    print(f"r={r}: full profile feasible for all {lo}..{hi}: {all(full_ok(n,r) for n in range(lo,hi+1))};  infeasible at n0={lo-1}: {not full_ok(lo-1,r)};  (n-4)-profile feasible at n0: {boundary_ok(lo-1,r)}")

# --- the note's own next step: where does the criterion put n0 for r=2..14 (largest failing n below 2r+40)?
print("criterion-based thresholds (largest n < 2r+40 with the full profile infeasible; needs HT for the tail):")
for r in range(2, 15):
    fails = [n for n in range(4, 2 * r + 40) if not full_ok(n, r)]
    print(f"   r={r:2d}: last infeasible n = {max(fails) if fails else None}; n0-2r = {max(fails)-2*r if fails else None}; infeasible set tail = {fails[-4:]}")

# --- explicit colex constructions + brute-force antichain check (independent of the criterion logic)
def unrank(idx, k):
    """zero-based colex rank -> k-set of positive ints"""
    s = []
    for i in range(k, 0, -1):
        b = i - 1
        while comb(b + 1, i) <= idx: b += 1
        s.append(b + 1); idx -= comb(b, i)
    return frozenset(s)
def build(n, r, top):
    a = {k: (r if 2 <= k <= top else 0) for k in range(n + 1)}
    D, ok = trace(n, r, a); assert ok
    fam = []
    for k in range(n, -1, -1):
        if a[k] == 0: continue
        s = sh(D[k + 1], k + 1) if k < n else 0
        for idx in range(s, D[k]): fam.append(unrank(idx, k))
    return fam
def is_antichain(fam, n):
    for A in fam: assert A <= set(range(1, n + 1))
    return all(not (A < B) and not (B < A) for A, B in combinations(fam, 2))
tot = 0
for r, n, top in ((5, 15, 13), (5, 33, 31), (6, 17, 15), (6, 35, 33), (11, 28, 26), (11, 47, 45), (5, 14, 11), (6, 16, 13), (11, 27, 24)):
    fam = build(n, r, top); sizes = sorted({len(A) for A in fam})
    assert len(fam) == r * (top - 1) and all(sum(1 for A in fam if len(A) == k) == r for k in range(2, top + 1))
    ok = is_antichain(fam, n); tot += len(fam) * (len(fam) - 1) // 2
    print(f"construction r={r} n={n} ranks 2..{top}: {len(fam)} sets, {len(sizes)} sizes, antichain={ok}")
print("pair comparisons done:", tot)

# --- exhaustive check of the criterion on ground sets n<=5 (all antichains)
def all_antichains(n):
    subsets = [frozenset(c) for k in range(n + 1) for c in combinations(range(1, n + 1), k)]
    N = len(subsets); res = []
    # enumerate antichains by DFS over subsets in fixed order
    def dfs(i, chosen):
        if i == N: res.append(list(chosen)); return
        dfs(i + 1, chosen)
        s = subsets[i]
        if all(not (s < t) and not (t < s) for t in chosen):
            chosen.append(s); dfs(i + 1, chosen); chosen.pop()
    dfs(0, []); return res
for n in range(1, 6):
    acs = all_antichains(n)
    feas = {tuple(sum(1 for A in F if len(A) == k) for k in range(n + 1)) for F in acs}
    allprof = [p for p in __import__('itertools').product(*[range(comb(n, k) + 1) for k in range(n + 1)])]
    crit = {p for p in allprof if trace(n, 0, dict(enumerate(p)))[1]}
    print(f"n={n}: antichains {len(acs)} (incl. empty), realizable profiles {len(feas)}, criterion-feasible {len(crit)}, equal: {feas==crit}")
