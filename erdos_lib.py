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
