# Provenance

## Timeline (UTC)
- 2026-02-10 — He & Tang, arXiv:2602.09803 (v2 2026-03-21): n₀(2)=3, n₀(3)=8, 2r+2 ≤ n₀(r) ≤ 2r+2log₂r+O(log log r).
- 2026-07-17 — M. Thiim, Erdős-problems proof claim #78: n₀(r)=2r+4 (4≤r≤10), 2r+5 (r≥11), Lean-formalized, tag v0.4.1-proof-claim.
- 2026-09-04/05 — Dan Smith (Kairos Signal) with GPT-6: cascade Kruskal–Katona profile argument for r = 5, 6, 11, explicit constructions, integer certificates. The GPT-6 note checked only the catalogue README status ("open"), not the proof-claims tab.
- 2026-09-05 ~15:50Z — Claude (Fable 5.1) re-derives every number independently (`profile_check.py`), reads He–Tang's PDF, finds proof claims #78 and #101.
- 2026-09-05 ~16:00–16:40Z — Thiim's package cloned at the tag, built (1,064 targets, exit 0, 11m44s), axiom audit reproduced; `KairosCases.lean` written and compiled (3.4 s, no sorry).
- 2026-09-05 — this repository assembled; MANIFEST.sha256 stamped with OpenTimestamps (Bitcoin anchoring completes when the calendar attestation confirms; run `ots upgrade`/`ots verify`).

## Who did what
- Mathematics of the three cases: Dan Smith with GPT-6 (derivation), by the classical Kruskal–Katona profile method. Same method as Thiim (July) — arrived at independently, later.
- Independent verification, literature check, Lean build and `KairosCases.lean`: Claude (Fable 5.1), operated by Dan Smith. Transcripts retained privately.
- Theorem for all r ≥ 4 and its Lean formalization: M. Thiim's package (provers named there: ChatGPT 5.6 Pro, Claude Fable 5, Codex). Not our work.
- Bounds and r = 2, 3: He & Tang.

## Independence statement
The derivation was completed before any of us had read claim #78 or Thiim's repository. The later discovery is recorded in `VERIFICATION_NOTES.md` §2 with the exact evidence (forum entries, paper lines). We make no priority claim.

## Integrity
`MANIFEST.sha256` lists SHA-256 of every file in this repository at release; `MANIFEST.sha256.ots` is its OpenTimestamps proof. Verify with `sha256sum -c MANIFEST.sha256` and `ots verify MANIFEST.sha256.ots`.
