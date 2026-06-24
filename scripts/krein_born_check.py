#!/usr/bin/env python3
"""
Indefinite (Krein-type) structure and Born-rule re-check on the lepton core.

MOTIVATION
----------
An earlier positive-definite Born check found NO clean structure when basin sizes
were compared to a *positive-definite* amplitude. But on a split prime, the natural
quadratic form on Z[i]/(p) is INDEFINITE, not positive-definite:

  For p = 1 mod 4, pick r with r^2 = -1 (mod p). Then
      phi(a+bi) = (a + r b,  a - r b)  =  (u, v)
  is a ring isomorphism  Z[i]/(p)  ->  F_p x F_p, and
      N(z) = a^2 + b^2 = u * v   (mod p).
  So the "norm" is the HYPERBOLIC product u*v, with signature (+,-) in the
  x = (u+v)/2, y = (u-v)/2 basis:  u*v = x^2 - y^2.

This is the finite analogue of an INDEFINITE / Krein inner product -- exactly the
object Turok & Bateman use in the 2026 quadratic-gravity revival to host
negative-norm ("ghost") states without negative probabilities. Conjugation
z -> conj(z) swaps (u, v), i.e. it is the natural parity/spin flip.

This script:
  1. Verifies the algebra numerically (homomorphism, conjugation swap, N = u*v).
  2. Classifies the canonical lepton attractors (p=13, k=6, ring, (1,i)) by the
     quadratic-residue SIGNATURE chi(N) in {+1 positive, -1 negative, 0 null}.
  3. Re-runs the Born-style correlation (basin size vs signature / norm) and
     checks whether any cycle-summed norm is conserved along an attractor.

It is an honest probe, not a derivation. Null results are reported as such.

Outputs: evidence/krein_born_check.jsonl, evidence/krein_born_summary.md
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gaussian_loop import GaussianLoopSim, GaussInt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT_JSONL = ROOT / "evidence" / "krein_born_check.jsonl"
OUT_MD = ROOT / "evidence" / "krein_born_summary.md"

P = 13
K = 6
N_INIT = 4000
MAX_STEPS = 3000
SEED = 20260624


def sqrt_minus_one(p: int):
    for r in range(1, p):
        if (r * r) % p == (p - 1) % p:
            return r
    return None


def legendre(x: int, p: int) -> int:
    x %= p
    if x == 0:
        return 0
    return 1 if pow(x, (p - 1) // 2, p) == 1 else -1


def verify_algebra(p: int, n_samples: int, rng: random.Random) -> dict:
    r = sqrt_minus_one(p)
    if r is None:
        return {"split": False, "r": None}

    def phi(a, b):
        return ((a + r * b) % p, (a - r * b) % p)

    hom_ok = sq_ok = conj_ok = norm_ok = True
    for _ in range(n_samples):
        a, b = rng.randrange(p), rng.randrange(p)
        c, d = rng.randrange(p), rng.randrange(p)
        # multiplication (a+bi)(c+di) = (ac-bd) + (ad+bc)i
        mre, mim = (a * c - b * d) % p, (a * d + b * c) % p
        u1, v1 = phi(a, b)
        u2, v2 = phi(c, d)
        if phi(mre, mim) != ((u1 * u2) % p, (v1 * v2) % p):
            hom_ok = False
        # squaring
        sre, sim = (a * a - b * b) % p, (2 * a * b) % p
        if phi(sre, sim) != ((u1 * u1) % p, (v1 * v1) % p):
            sq_ok = False
        # conjugation swaps coordinates
        if phi(a, (-b) % p) != (v1, u1):
            conj_ok = False
        # norm = u*v
        if (a * a + b * b) % p != (u1 * v1) % p:
            norm_ok = False
    return {"split": True, "r": r, "hom_ok": hom_ok, "sq_ok": sq_ok,
            "conj_ok": conj_ok, "norm_ok": norm_ok, "samples": n_samples}


def collect_attractors(p: int, k: int, n_init: int, max_steps: int, rng: random.Random):
    """Return dict: attractor_key -> record with period, basin, signature profile."""
    attractors = {}
    for _ in range(n_init):
        sim = GaussianLoopSim(k, p, "ring")
        init = [GaussInt(rng.randrange(p), rng.randrange(p), p) for _ in range(k)]
        cycle, period, _ = sim.find_attractor(max_steps=max_steps, init=init)
        if cycle is None or period <= 0:
            continue
        key = frozenset(tuple((z.re, z.im) for z in state) for state in cycle)
        rec = attractors.get(key)
        if rec is None:
            sectors = Counter()
            norms = []
            for state in cycle:
                for z in state:
                    nrm = (z.re * z.re + z.im * z.im) % p
                    norms.append(nrm)
                    sectors[legendre(nrm, p)] += 1
            total = sum(sectors.values())
            attractors[key] = {
                "period": period,
                "basin": 1,
                "n_pos": sectors.get(1, 0),
                "n_neg": sectors.get(-1, 0),
                "n_null": sectors.get(0, 0),
                "frac_pos": sectors.get(1, 0) / total,
                "frac_neg": sectors.get(-1, 0) / total,
                "frac_null": sectors.get(0, 0) / total,
                "mean_norm": sum(norms) / len(norms),
                "norm_sum_per_state": [sum((z.re * z.re + z.im * z.im) % p for z in state)
                                       for state in cycle],
            }
        else:
            rec["basin"] += 1
    return attractors


def spearman(xs, ys) -> float:
    n = len(xs)
    if n < 3:
        return float("nan")

    def ranks(v):
        order = sorted(range(n), key=lambda i: v[i])
        rk = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for t in range(i, j + 1):
                rk[order[t]] = avg
            i = j + 1
        return rk

    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = math.sqrt(sum((rx[i] - mx) ** 2 for i in range(n)))
    dy = math.sqrt(sum((ry[i] - my) ** 2 for i in range(n)))
    return num / (dx * dy) if dx > 0 and dy > 0 else float("nan")


def conjugate_pairs(attractors: dict, p: int) -> tuple[int, int]:
    """Count attractors whose conjugate is also present and shares the signature."""
    keys = set(attractors.keys())
    matched = same_sig = 0
    for key, rec in attractors.items():
        conj_key = frozenset(tuple((re, (-im) % p) for (re, im) in state) for state in key)
        if conj_key in keys:
            matched += 1
            c = attractors[conj_key]
            if (c["n_pos"], c["n_neg"], c["n_null"]) == (rec["n_pos"], rec["n_neg"], rec["n_null"]):
                same_sig += 1
    return matched, same_sig


def run(p, k, n_init, max_steps):
    rng = random.Random(SEED)
    algebra = verify_algebra(p, 500, rng)
    attractors = collect_attractors(p, k, n_init, max_steps, rng)
    recs = list(attractors.values())

    basins = [r["basin"] for r in recs]
    frac_null = [r["frac_null"] for r in recs]
    frac_pos = [r["frac_pos"] for r in recs]
    mean_norm = [r["mean_norm"] for r in recs]

    corr_null = spearman(basins, frac_null)
    corr_pos = spearman(basins, frac_pos)
    corr_norm = spearman(basins, mean_norm)

    # global signature distribution, basin-weighted
    tot_pos = sum(r["n_pos"] * r["basin"] for r in recs)
    tot_neg = sum(r["n_neg"] * r["basin"] for r in recs)
    tot_null = sum(r["n_null"] * r["basin"] for r in recs)
    tot = tot_pos + tot_neg + tot_null or 1

    matched, same_sig = conjugate_pairs(attractors, p)

    # conserved-norm check on the longest-period attractor
    cons_unsigned = None
    if recs:
        longest = max(recs, key=lambda r: r["period"])
        sums = longest["norm_sum_per_state"]
        cons_unsigned = (len(set(sums)) == 1) if sums else None

    return {
        "algebra": algebra,
        "n_attractors": len(recs),
        "n_init": n_init,
        "corr_basin_fracnull": corr_null,
        "corr_basin_fracpos": corr_pos,
        "corr_basin_meannorm": corr_norm,
        "frac_pos": tot_pos / tot, "frac_neg": tot_neg / tot, "frac_null": tot_null / tot,
        "conj_matched": matched, "conj_same_sig": same_sig,
        "cons_unsigned_norm": cons_unsigned,
        "recs": recs,
    }


def write_outputs(res, p, k, selftest):
    with OUT_JSONL.open("w", encoding="utf-8") as f:
        for r in res["recs"]:
            row = {kk: vv for kk, vv in r.items() if kk != "norm_sum_per_state"}
            f.write(json.dumps(row) + "\n")

    a = res["algebra"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    L = []
    L.append("# Krein / Indefinite Born Check")
    L.append("")
    if selftest:
        L.append("> **SELF-TEST RUN** (reduced sampling).")
        L.append("")
    L.append(f"Generated: {now}  ·  system: Z[i]/({p}), k={k}, ring, weights (1, i)")
    L.append("")
    L.append("## 1. Algebraic structure (exact, verified numerically)")
    L.append("")
    if a.get("split"):
        L.append(f"- sqrt(-1) mod {p} = {a['r']}; map phi(a+bi) = (a+{a['r']}b, a-{a['r']}b).")
        L.append(f"- Ring homomorphism Z[i]/({p}) -> F_{p} x F_{p}: "
                 f"{'VERIFIED' if a['hom_ok'] else 'FAILED'} "
                 f"(mult), {'VERIFIED' if a['sq_ok'] else 'FAILED'} (square), on {a['samples']} samples.")
        L.append(f"- Conjugation swaps the two coordinates (parity/spin flip): "
                 f"{'VERIFIED' if a['conj_ok'] else 'FAILED'}.")
        L.append(f"- Norm N(z)=a^2+b^2 equals the hyperbolic product u*v: "
                 f"{'VERIFIED' if a['norm_ok'] else 'FAILED'}.")
        L.append("")
        L.append("So the natural norm is INDEFINITE (signature (+,-) via u*v = x^2 - y^2):")
        L.append("a finite analogue of a Krein inner product. chi(N) in {+1,-1,0} labels the")
        L.append("positive-norm / negative-norm / null sectors.")
    else:
        L.append(f"- p={p} is inert (no sqrt(-1)); the split Krein decomposition does not apply.")
    L.append("")
    L.append("## 2. Signature of the lepton attractors")
    L.append("")
    L.append(f"- Distinct attractors found: {res['n_attractors']} (from {res['n_init']} random inits).")
    L.append(f"- Basin-weighted state signature: positive (chi=+1) {res['frac_pos']:.1%}, "
             f"negative (chi=-1) {res['frac_neg']:.1%}, null (chi=0) {res['frac_null']:.1%}.")
    L.append(f"- Conjugate states found within the SAME (1, i) attractor set: {res['conj_matched']} "
             "(expected ~0).")
    L.append("  Reason: conjugation sends the (1, i) rule to the (1, -i) rule, so the parity/spin")
    L.append("  partner of a (1, i) attractor lives in the (1, -i) system. The proper spin-doublet")
    L.append("  test therefore compares the (1, i) and (1, -i) systems -- a clean next experiment.")
    L.append("")
    L.append("## 3. Born-style re-check (indefinite)")
    L.append("")
    L.append("Spearman correlation of basin size with:")
    L.append(f"- fraction of NULL-sector states:     {res['corr_basin_fracnull']:+.3f}")
    L.append(f"- fraction of POSITIVE-sector states: {res['corr_basin_fracpos']:+.3f}")
    L.append(f"- mean (positive-definite) norm:      {res['corr_basin_meannorm']:+.3f}")
    L.append(f"- cycle-summed unsigned norm conserved along longest attractor: "
             f"{res['cons_unsigned_norm']}")
    L.append("")
    L.append("## Honest reading")
    L.append("")
    L.append("- CONFIRMED (algebra): on the split prime the dynamics decomposes into two F_p")
    L.append("  sectors swapped by conjugation, and the natural norm is the indefinite form")
    L.append("  u*v. This is a real, exact structural fact and the right setting for a")
    L.append("  Krein/negative-norm reading (cf. Turok-Bateman quadratic gravity).")
    L.append("- The signature distribution and basin correlations above are the data; if all")
    L.append("  correlations are weak (|rho| small), an indefinite Born law is NOT yet")
    L.append("  demonstrated -- only the correct arena for it is established. State that plainly.")
    L.append("- Next: test a sign-fixed Krein functional |<psi|psi>| as the conserved quantity,")
    L.append("  and whether positive/negative sectors map to the cw/ccw spin doublet.")
    L.append("")
    OUT_MD.write_text("\n".join(L), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="Fast reduced run.")
    args = ap.parse_args()
    n_init = 200 if args.selftest else N_INIT
    max_steps = 800 if args.selftest else MAX_STEPS
    global OUT_JSONL, OUT_MD
    if args.selftest:
        OUT_JSONL = ROOT / "evidence" / "krein_born_check_selftest.jsonl"
        OUT_MD = ROOT / "evidence" / "krein_born_selftest_summary.md"

    print(f"System Z[i]/({P}), k={K}, ring, (1,i); {n_init} inits, max_steps {max_steps}")
    res = run(P, K, n_init, max_steps)
    write_outputs(res, P, K, args.selftest)
    a = res["algebra"]
    if a.get("split"):
        print(f"Algebra: hom={a['hom_ok']} square={a['sq_ok']} conj_swap={a['conj_ok']} "
              f"norm=uv={a['norm_ok']}")
    print(f"Attractors: {res['n_attractors']}  signature +/-/0 = "
          f"{res['frac_pos']:.0%}/{res['frac_neg']:.0%}/{res['frac_null']:.0%}")
    print(f"Basin Spearman: null={res['corr_basin_fracnull']:+.3f} "
          f"pos={res['corr_basin_fracpos']:+.3f} meanNorm={res['corr_basin_meannorm']:+.3f}")
    print(f"Wrote {OUT_JSONL.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
