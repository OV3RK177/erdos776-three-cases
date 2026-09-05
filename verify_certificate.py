#!/usr/bin/env python3
"""Independent verifier: re-checks every family in certificates/certificate.json by direct containment
tests and level counts, and re-derives every obstruction trace with its own cascade code. Stdlib only."""
import json, sys
from math import comb
from itertools import combinations
def cascade(q, k):
    out=[]; i=k
    while q>0 and i>=1:
        b=i
        while comb(b+1,i)<=q: b+=1
        out.append((b,i)); q-=comb(b,i); i-=1
    assert q==0; return out
def sh(q,k): return 0 if q==0 else sum(comb(b,i-1) for b,i in cascade(q,k))
c=json.load(open(sys.argv[1] if len(sys.argv)>1 else "certificates/certificate.json"))
bad=0; pairs=0
for key,o in c["obstructions"].items():
    r=int(key.split("_")[0][1:]); n=int(key.split("_")[1][1:]); D={n:0}
    for k in range(n-1,-1,-1): D[k]=(r if 2<=k<=n-2 else 0)+sh(D[k+1],k+1)
    ok = all(D[k]==o["D"][str(k)] for k in range(n,1,-1)) and D[2]>comb(n,2)
    print(f"obstruction {key}: trace matches={ok} D2={D[2]} > C({n},2)={comb(n,2)}"); bad+= not ok
for key,fam in c["constructions"].items():
    r=int(key.split("_")[0][1:]); n=int(key.split("_")[1][1:]); F=[frozenset(A) for A in fam]
    assert len(set(F))==len(F) and all(A<=set(range(1,n+1)) for A in F)
    sizes={}
    for A in F: sizes[len(A)]=sizes.get(len(A),0)+1
    anti=all(not(A<B) and not(B<A) for A,B in combinations(F,2)); pairs+=len(F)*(len(F)-1)//2
    expect = n-4 if "boundary" in key else n-3
    ok = anti and all(v==r for v in sizes.values()) and len(sizes)==expect
    bad+= not ok
    if not ok or "boundary" in key or n in (15,33,17,35,28,47): print(f"construction {key}: {len(F)} sets, {len(sizes)} sizes, r={r} each, antichain={anti}, ok={ok}")
print(f"pairs compared: {pairs}; failures: {bad}"); sys.exit(1 if bad else 0)
