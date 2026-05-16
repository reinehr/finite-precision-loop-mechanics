#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quark-Massenverhältnisse aus gekoppelten Sub-Loops.

Quarks = Sub-Loops (k=3) innerhalb eines Komposit-Systems.
Die Quarkmasse ~ 1/Teilperiode des Sub-Loops im Komposit.

Targets:
  d/u  ≈ 2.14   (1. Gen)
  c/s  ≈ 13.7   (2. Gen)
  t/b  ≈ 41.4   (3. Gen)
  s/d  ≈ 19.8
  s/u  ≈ 42.3
  c/u  ≈ 579.5
  b/c  ≈ 3.28

Approach:
  Phase 1: k=3+k=3 symmetric & asymmetric weights → sub-period ratios
  Phase 2: k=3+k=6 baryon-like composites
  Phase 3: Compound sub-period ratios (product)
  Phase 4: Gaussian factor weights (3+2i)/(3−2i)

Runtime target: ≤15 min
Output: evidence/quark_masses_summary.md
"""

import argparse
import random
import sys
import time
from collections import defaultdict
from multiprocessing import Pool, cpu_count
from pathlib import Path

from gaussian_loop import GaussInt

ROOT = Path(__file__).resolve().parents[1]
MOD = 13  # overridden by --mod
OUT_BASE = str(ROOT / "evidence" / "quark_masses_summary")
MAX_STEPS = 5000

TARGETS = {
    "d/u": 2.14,
    "c/s": 13.7,
    "t/b": 41.4,
    "s/d": 19.8,
    "s/u": 42.3,
    "c/u": 579.5,
    "b/c": 3.28,
}
TOL = 0.05


# ── weight specs (picklable tuples) ────────────────────────────
# (w_left1, w_right1, w_left2, w_right2, c_ab, c_ba, label)
# Base specs (mod-independent or mod 13)
WEIGHT_SPECS_BASE = [
    ((1,0),(0,1),(1,0),(0,1),(1,0),(1,0),  "sym_(1,i)"),
    ((1,0),(0,1),(0,1),(1,0),(1,0),(1,0),  "asym_(1,i)_(i,1)"),
    ((1,0),(0,1),(1,0),(0,12),(1,0),(1,0), "asym_(1,i)_(1,-i)"),
    ((1,0),(0,1),(1,0),(0,1),(0,1),(0,1),  "sym_coup=i"),
    ((1,0),(0,1),(1,0),(0,1),(0,1),(0,12), "asym_coup=i/-i"),
    ((1,0),(0,1),(1,0),(0,1),(2,0),(1,0),  "asym_coup=2/1"),
    ((1,0),(0,1),(1,0),(0,1),(3,2),(3,11), "coup=(3+2i)/(3-2i)"),
    ((3,2),(3,11),(3,2),(3,11),(1,0),(1,0),"w=gauss_fac_sym"),
    ((3,2),(1,0),(3,11),(1,0),(1,0),(1,0), "w=gauss_fac_asym"),
    ((1,0),(0,1),(1,0),(1,0),(1,0),(1,0),  "asym_(1,i)_(1,1)"),
    ((1,0),(0,1),(0,1),(0,1),(1,0),(1,0),  "asym_(1,i)_(i,i)"),
    ((1,0),(0,1),(1,0),(0,1),(1,0),(0,0),  "one_way_A→B"),
    ((1,0),(0,1),(1,0),(0,1),(0,0),(1,0),  "one_way_B→A"),
]

# mod=17: 17=(4+i)(4-i), Kopplung (4,1)/(4,16) für s/d≈19.8
WEIGHT_SPECS_MOD17 = [
    ((4,1),(4,16),(4,1),(4,16),(1,0),(1,0), "mod17_(4+i)/(4-i)_sym"),
    ((4,1),(4,16),(4,16),(4,1),(1,0),(1,0), "mod17_(4+i)/(4-i)_asym"),
]


def get_weight_specs(mod):
    specs = list(WEIGHT_SPECS_BASE)
    if mod == 17:
        specs.extend(WEIGHT_SPECS_MOD17)
    return specs


# Will be set in main() before Pool (workers inherit via fork)
WEIGHT_SPECS = WEIGHT_SPECS_BASE


# ── helpers ────────────────────────────────────────────────────

def measure_subperiods(traj_sub1, traj_sub2, period):
    """Find minimal sub-period that divides the composite period."""
    p1 = period
    for p in range(1, period + 1):
        if period % p != 0:
            continue
        if all(traj_sub1[t] == traj_sub1[t % p] for t in range(period)):
            p1 = p
            break

    p2 = period
    for p in range(1, period + 1):
        if period % p != 0:
            continue
        if all(traj_sub2[t] == traj_sub2[t % p] for t in range(period)):
            p2 = p
            break

    return p1, p2


def run_composite(k1, k2, mod, wl1, wr1, wl2, wr2, cab, cba, init1, init2):
    """Run a composite system and return (period, sub1_period, sub2_period)."""
    wl1g = GaussInt(wl1[0], wl1[1], mod)
    wr1g = GaussInt(wr1[0], wr1[1], mod)
    wl2g = GaussInt(wl2[0], wl2[1], mod)
    wr2g = GaussInt(wr2[0], wr2[1], mod)
    cabg = GaussInt(cab[0], cab[1], mod)
    cbag = GaussInt(cba[0], cba[1], mod)

    state1 = list(init1)
    state2 = list(init2)

    def step():
        nonlocal state1, state2
        new1 = []
        for j in range(k1):
            v = state1[(j-1)%k1]*wl1g + state1[(j+1)%k1]*wr1g
            if j == 0:
                v = v + state2[0]*cbag
            v = state1[j]*state1[j] + v
            new1.append(v)
        new2 = []
        for j in range(k2):
            v = state2[(j-1)%k2]*wl2g + state2[(j+1)%k2]*wr2g
            if j == 0:
                v = v + state1[0]*cabg
            v = state2[j]*state2[j] + v
            new2.append(v)
        state1 = new1
        state2 = new2

    def full_key():
        return (
            tuple((z.re, z.im) for z in state1),
            tuple((z.re, z.im) for z in state2),
        )

    seen = {}
    for t in range(MAX_STEPS):
        fk = full_key()
        if fk in seen:
            period = t - seen[fk]
            traj1, traj2 = [], []
            for _ in range(period):
                traj1.append(tuple((z.re, z.im) for z in state1))
                traj2.append(tuple((z.re, z.im) for z in state2))
                step()
            p1, p2 = measure_subperiods(traj1, traj2, period)
            return period, p1, p2
        seen[fk] = t
        step()

    return 0, None, None


def worker_phase1(cfg):
    ws_idx, seed, mod, weight_specs = cfg
    ws = weight_specs[ws_idx]
    wl1, wr1, wl2, wr2, cab, cba, label = ws
    random.seed(seed)
    k1 = k2 = 3
    init1 = [GaussInt.random(mod) for _ in range(k1)]
    init2 = [GaussInt.random(mod) for _ in range(k2)]
    pf, p1, p2 = run_composite(k1, k2, mod, wl1, wr1, wl2, wr2, cab, cba, init1, init2)
    ratio = None
    if p1 and p2 and min(p1, p2) > 0:
        ratio = max(p1, p2) / min(p1, p2)
    return ws_idx, label, pf, p1, p2, ratio


def worker_baryon(cfg):
    seed, mod = cfg
    random.seed(seed)
    k1, k2 = 3, 6
    init1 = [GaussInt.random(mod) for _ in range(k1)]
    init2 = [GaussInt.random(mod) for _ in range(k2)]
    pf, p1, p2 = run_composite(
        k1, k2, mod, (1,0),(0,1),(1,0),(0,1),(1,0),(1,0),
        init1, init2,
    )
    ratio = None
    if p1 and p2 and min(p1, p2) > 0:
        ratio = max(p1, p2) / min(p1, p2)
    return pf, p1, p2, ratio


def match_targets(ratio):
    hits = []
    if ratio is None or ratio <= 1.001:
        return hits
    for name, tgt in TARGETS.items():
        err = abs(ratio - tgt) / tgt
        if err < TOL:
            hits.append((name, tgt, ratio, err))
    return hits


# ── main ───────────────────────────────────────────────────────

def main():
    global MOD, WEIGHT_SPECS
    ap = argparse.ArgumentParser()
    ap.add_argument("--mod", type=int, default=13, help="Modulus (13 or 17)")
    args = ap.parse_args()
    MOD = args.mod
    WEIGHT_SPECS = get_weight_specs(MOD)
    OUT = f"{OUT_BASE}_mod{MOD}.md"

    t0 = time.time()
    N_TRIALS = 300
    workers = min(cpu_count(), 14)

    print("=" * 60)
    print("  QUARK-MASSENVERHÄLTNISSE AUS SUB-LOOP-PERIODEN")
    print("=" * 60)
    print(f"mod={MOD}  k=3+3  {len(WEIGHT_SPECS)} Gewichts-Konfigurationen")
    print(f"N_TRIALS={N_TRIALS}  workers={workers}")
    print(f"Targets: {TARGETS}\n")
    sys.stdout.flush()

    # ── Phase 1 ────────────────────────────────────────────────
    print("Phase 1: k=3+k=3 Sub-Period-Scan ...")
    cfgs = [(wi, 300000 + wi*N_TRIALS + i, MOD, WEIGHT_SPECS)
            for wi in range(len(WEIGHT_SPECS)) for i in range(N_TRIALS)]
    random.shuffle(cfgs)

    results1 = []
    ratio_cat = defaultdict(list)
    period_cat = defaultdict(lambda: defaultdict(int))
    hits1 = []
    done = 0

    with Pool(workers) as pool:
        for r in pool.imap_unordered(worker_phase1, cfgs, chunksize=20):
            ws_idx, label, pf, p1, p2, ratio = r
            results1.append(r)
            if pf > 0:
                period_cat[label][pf] += 1
            if ratio is not None and ratio > 1.001:
                ratio_cat[label].append(ratio)
            mh = match_targets(ratio)
            if mh:
                hits1.append((r, mh))
            done += 1
            if done % 500 == 0:
                el = time.time() - t0
                print(f"  {done}/{len(cfgs)}  {el:.0f}s  hits={len(hits1)}")
                sys.stdout.flush()

    el1 = time.time() - t0
    print(f"  Phase 1 fertig: {el1:.0f}s, {len(hits1)} Treffer\n")
    sys.stdout.flush()

    # ── Phase 2: k=3+k=6 baryon-like ──────────────────────────
    print("Phase 2: k=3+k=6 Komposit ...")
    baryon_cfgs = [(s, MOD) for s in range(200)]
    baryon_res = []
    hits2 = []

    with Pool(workers) as pool:
        for r in pool.imap_unordered(worker_baryon, baryon_cfgs, chunksize=10):
            baryon_res.append(r)
            pf, p1, p2, ratio = r
            mh = match_targets(ratio)
            if mh:
                hits2.append((r, mh))

    el2 = time.time() - t0
    print(f"  Phase 2 fertig: {el2-el1:.0f}s, {len(hits2)} Treffer\n")
    sys.stdout.flush()

    # ── Phase 3: compound ratios ──────────────────────────────
    print("Phase 3: Zusammengesetzte Verhältnisse ...")
    compound = []
    for label, ratios in ratio_cat.items():
        uniq = sorted(set(round(r, 4) for r in ratios))
        for i, r1 in enumerate(uniq):
            for r2 in uniq[i:]:
                prod = r1 * r2
                mh = match_targets(prod)
                if mh:
                    compound.append((label, r1, r2, prod, mh))
                if r1 > 1:
                    quot = r2 / r1
                    mh2 = match_targets(quot)
                    if mh2:
                        compound.append((label, r2, r1, quot, mh2))

    el3 = time.time() - t0
    print(f"  Phase 3 fertig: {el3-el2:.0f}s, {len(compound)} Treffer\n")
    sys.stdout.flush()

    # ── write summary ─────────────────────────────────────────
    L = []
    L.append("# Quark-Massenverhältnisse aus Sub-Loop-Perioden")
    L.append("")
    L.append(f"- Laufzeit: {el3:.0f}s")
    L.append(f"- Modulus: {MOD}, Sub-Loops: k=3+k=3 (Phase 1), k=3+k=6 (Phase 2)")
    L.append(f"- Gewichts-Konfigurationen: {len(WEIGHT_SPECS)}")
    L.append(f"- Trials/Konfiguration: {N_TRIALS}")
    L.append(f"- Toleranz: {TOL*100:.0f}%")
    L.append("")

    L.append("## Ziel-Verhältnisse (Current Quark Masses)")
    L.append("")
    L.append("| Verhältnis | Wert |")
    L.append("|------------|------|")
    for n, v in TARGETS.items():
        L.append(f"| {n} | {v} |")
    L.append("")

    # Phase 1 overview
    L.append("## Phase 1: k=3+k=3 Übersicht")
    L.append("")
    L.append("| Konfiguration | Konverg. | Versch. Ratios | Min | Max | Treffer |")
    L.append("|---------------|----------|----------------|-----|-----|---------|")
    for wi, ws in enumerate(WEIGHT_SPECS):
        label = ws[6]
        rats = ratio_cat.get(label, [])
        n_conv = sum(1 for r in results1 if r[0] == wi and r[2] > 0)
        uniq = sorted(set(round(r, 2) for r in rats))
        nh = sum(1 for r, h in hits1 if r[0] == wi)
        mn = f"{min(rats):.2f}" if rats else "-"
        mx = f"{max(rats):.2f}" if rats else "-"
        L.append(f"| {label} | {n_conv} | {len(uniq)} | {mn} | {mx} | {nh} |")
    L.append("")

    # Direct hits
    L.append("## Direkte Treffer")
    L.append("")
    if hits1:
        L.append("| Konfiguration | P_full | P_sub1 | P_sub2 | Ratio | Target | Fehler |")
        L.append("|---------------|--------|--------|--------|-------|--------|--------|")
        for r, hlist in sorted(hits1, key=lambda x: x[1][0][3]):
            wi, label, pf, p1, p2, ratio = r
            for name, tgt, rat, err in hlist:
                L.append(f"| {label} | {pf} | {p1} | {p2} | {rat:.4f} | {name}={tgt} | {err*100:.2f}% |")
    else:
        L.append("Keine direkten Treffer.")
    L.append("")

    # Phase 2
    L.append("## Phase 2: k=3+k=6")
    L.append("")
    conv_b = [r for r in baryon_res if r[0] > 0]
    rats_b = [r[3] for r in conv_b if r[3] is not None and r[3] > 1.001]
    L.append(f"- Konvergiert: {len(conv_b)}/{len(baryon_res)}")
    if rats_b:
        L.append(f"- Ratio-Bereich: {min(rats_b):.2f} — {max(rats_b):.2f}")
        uniq_b = sorted(set(round(r, 2) for r in rats_b))
        L.append(f"- Verschiedene Ratios ({len(uniq_b)}): {uniq_b[:30]}")
    if hits2:
        L.append("")
        L.append("| P_full | P_sub1 | P_sub2 | Ratio | Target | Fehler |")
        L.append("|--------|--------|--------|-------|--------|--------|")
        for r, hlist in hits2:
            pf, p1, p2, ratio = r
            for name, tgt, rat, err in hlist:
                L.append(f"| {pf} | {p1} | {p2} | {rat:.4f} | {name}={tgt} | {err*100:.2f}% |")
    else:
        L.append("- Keine Treffer.")
    L.append("")

    # Compound
    L.append("## Phase 3: Zusammengesetzte Verhältnisse (Produkte/Quotienten)")
    L.append("")
    if compound:
        L.append("| Konfiguration | R1 | R2 | Ergebnis | Target | Fehler |")
        L.append("|---------------|----|----|----------|--------|--------|")
        for label, r1, r2, prod, hlist in compound[:50]:
            for name, tgt, rat, err in hlist:
                L.append(f"| {label} | {r1:.4f} | {r2:.4f} | {prod:.4f} | {name}={tgt} | {err*100:.2f}% |")
    else:
        L.append("Keine zusammengesetzten Treffer.")
    L.append("")

    # Full ratio catalog
    L.append("## Gesamtkatalog beobachteter Sub-Period-Verhältnisse")
    L.append("")
    all_r = set()
    for rats in ratio_cat.values():
        for r in rats:
            all_r.add(round(r, 3))
    sr = sorted(all_r)
    L.append(f"Insgesamt {len(sr)} verschiedene Verhältnisse.")
    L.append("")
    L.append(f"Ratios: {sr[:60]}")
    if len(sr) > 60:
        L.append(f"... und {len(sr)-60} weitere")
    L.append("")

    # Sub-period catalog
    L.append("## Sub-Perioden-Katalog (häufigste Komposit-Perioden)")
    L.append("")
    for label in sorted(period_cat.keys()):
        top = sorted(period_cat[label].items(), key=lambda x: -x[1])[:8]
        L.append(f"**{label}**: {dict(top)}")
    L.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"Summary geschrieben: {OUT}")
    print(f"Gesamtlaufzeit: {el3:.0f}s")


if __name__ == "__main__":
    main()
