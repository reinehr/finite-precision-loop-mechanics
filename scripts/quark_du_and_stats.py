#!/usr/bin/env python3
"""
Zwei Ziele in einem Script:

Teil A: d/u-Vertiefung
  - mod=13 coup=(3+2i)/(3-2i): 2000 Trials, alle Sub-Period-Ratios sammeln
  - mod=17 coup=(4+1i)/(4-1i): 2000 Trials, d/u=2.1667 reproduzieren?
  - Auch k=4+k=4 testen (statt nur k=3+k=3)

Teil B: Look-Elsewhere-Statistik
  - Wie viele Compound-Treffer erwarten wir ZUFÄLLIG?
  - Monte-Carlo: N zufällige Ratios ziehen, Compound-Hits zählen, 10000x wiederholen
  - Vergleich mit beobachteten 185 Compound-Hits bei 57 Ratios

Runtime: ≤15 min
Output: evidence/quark_du_stats_summary.md
"""

import random
import sys
import time
from collections import defaultdict
from multiprocessing import Pool, cpu_count
from pathlib import Path

from gaussian_loop import GaussInt

ROOT = Path(__file__).resolve().parents[1]
MAX_STEPS = 5000
OUT = str(ROOT / "evidence" / "quark_du_stats_summary.md")

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


def measure_subperiods(traj1, traj2, period):
    p1 = period
    for p in range(1, period + 1):
        if period % p != 0:
            continue
        if all(traj1[t] == traj1[t % p] for t in range(period)):
            p1 = p
            break
    p2 = period
    for p in range(1, period + 1):
        if period % p != 0:
            continue
        if all(traj2[t] == traj2[t % p] for t in range(period)):
            p2 = p
            break
    return p1, p2


def run_composite(k1, k2, mod, cab, cba, init1, init2):
    wl = GaussInt(1, 0, mod)
    wr = GaussInt(0, 1, mod)
    cabg = GaussInt(cab[0], cab[1], mod)
    cbag = GaussInt(cba[0], cba[1], mod)

    state1 = list(init1)
    state2 = list(init2)

    def step():
        nonlocal state1, state2
        new1 = []
        for j in range(k1):
            v = state1[(j-1)%k1]*wl + state1[(j+1)%k1]*wr
            if j == 0:
                v = v + state2[0]*cbag
            v = state1[j]*state1[j] + v
            new1.append(v)
        new2 = []
        for j in range(k2):
            v = state2[(j-1)%k2]*wl + state2[(j+1)%k2]*wr
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


def match_targets(ratio):
    hits = []
    if ratio is None or ratio <= 1.001:
        return hits
    for name, tgt in TARGETS.items():
        err = abs(ratio - tgt) / tgt
        if err < TOL:
            hits.append((name, tgt, ratio, err))
    return hits


# ── Teil A: d/u-Vertiefung ────────────────────────────────────

_g_cfg = None

def _init_a(cfg):
    global _g_cfg
    _g_cfg = cfg

def worker_a(seed):
    mod, k, cab, cba = _g_cfg
    random.seed(seed)
    init1 = [GaussInt.random(mod) for _ in range(k)]
    init2 = [GaussInt.random(mod) for _ in range(k)]
    pf, p1, p2 = run_composite(k, k, mod, cab, cba, init1, init2)
    ratio = None
    if p1 and p2 and min(p1, p2) > 0:
        ratio = max(p1, p2) / min(p1, p2)
    return pf, p1, p2, ratio


def run_du_scan(mod, k, cab, cba, label, n_trials, workers):
    seeds = list(range(700000, 700000 + n_trials))
    ratios = []
    hits = []
    n_conv = 0
    periods = defaultdict(int)

    with Pool(workers, initializer=_init_a, initargs=((mod, k, cab, cba),)) as pool:
        for r in pool.imap_unordered(worker_a, seeds, chunksize=40):
            pf, p1, p2, ratio = r
            if pf > 0:
                n_conv += 1
                periods[pf] += 1
            if ratio is not None and ratio > 1.001:
                ratios.append(ratio)
                mh = match_targets(ratio)
                if mh:
                    hits.append((pf, p1, p2, ratio, mh))

    unique_ratios = sorted(set(round(r, 4) for r in ratios))

    du_hits = [h for h in hits if any(n == "d/u" for n, *_ in h[4])]
    du_best = None
    if du_hits:
        du_best = min(du_hits, key=lambda h: min(e for n, t, r, e in h[4] if n == "d/u"))

    return {
        "label": label,
        "mod": mod,
        "k": k,
        "n_trials": n_trials,
        "n_conv": n_conv,
        "n_unique_ratios": len(unique_ratios),
        "unique_ratios": unique_ratios,
        "all_ratios": ratios,
        "n_hits": len(hits),
        "hits": hits,
        "du_hits": len(du_hits),
        "du_best": du_best,
        "top_periods": sorted(periods.items(), key=lambda x: -x[1])[:10],
    }


# ── Teil B: Look-Elsewhere-Statistik ──────────────────────────

def count_compound_hits(ratios_list, targets, tol):
    """Given a list of observed ratios, count compound hits."""
    uniq = sorted(set(round(r, 4) for r in ratios_list if r > 1.001))
    n_hits = 0
    for i, r1 in enumerate(uniq):
        for r2 in uniq[i:]:
            prod = r1 * r2
            if any(abs(prod - t) / t < tol for t in targets.values()):
                n_hits += 1
            if r1 > 1:
                quot = r2 / r1
                if any(abs(quot - t) / t < tol for t in targets.values()):
                    n_hits += 1
    return n_hits


def count_direct_hits(ratios_list, targets, tol):
    n = 0
    for r in ratios_list:
        if r is None or r <= 1.001:
            continue
        if any(abs(r - t) / t < tol for t in targets.values()):
            n += 1
    return n


def look_elsewhere_mc(n_ratios, ratio_range, n_mc, targets, tol):
    """Monte Carlo: draw n_ratios random ratios from ratio_range,
    count direct and compound hits. Repeat n_mc times."""
    direct_counts = []
    compound_counts = []

    for i in range(n_mc):
        random.seed(900000 + i)
        fake_ratios = [random.uniform(ratio_range[0], ratio_range[1])
                       for _ in range(n_ratios)]
        d = count_direct_hits(fake_ratios, targets, tol)
        c = count_compound_hits(fake_ratios, targets, tol)
        direct_counts.append(d)
        compound_counts.append(c)

    return direct_counts, compound_counts


# ── main ───────────────────────────────────────────────────────

def main():
    t0 = time.time()
    workers = min(cpu_count(), 14)
    N_DU = 2000

    print("=" * 60)
    print("  TEIL A: d/u-VERTIEFUNG + TEIL B: LOOK-ELSEWHERE")
    print("=" * 60)
    sys.stdout.flush()

    # ── Teil A ─────────────────────────────────────────────────
    configs = [
        (13, 3, (3, 2), (3, 11), "mod13_k3_(3+2i)/(3-2i)"),
        (17, 3, (4, 1), (4, 16), "mod17_k3_(4+i)/(4-i)"),
        (13, 4, (3, 2), (3, 11), "mod13_k4_(3+2i)/(3-2i)"),
        (17, 4, (4, 1), (4, 16), "mod17_k4_(4+i)/(4-i)"),
        (29, 3, (5, 2), (5, 27), "mod29_k3_(5+2i)/(5-2i)"),
    ]

    scan_results = []
    for mod, k, cab, cba, label in configs:
        t1 = time.time()
        print(f"\nScan: {label} (N={N_DU}) ...")
        sys.stdout.flush()
        res = run_du_scan(mod, k, cab, cba, label, N_DU, workers)
        el = time.time() - t1
        print(f"  {el:.0f}s | conv={res['n_conv']} | ratios={res['n_unique_ratios']} | "
              f"d/u hits={res['du_hits']} | total hits={res['n_hits']}")
        if res["du_best"]:
            pf, p1, p2, ratio, mh = res["du_best"]
            err = min(e for n, t, r, e in mh if n == "d/u")
            print(f"  Best d/u: {ratio:.4f} (err={err*100:.2f}%) from P={pf}, sub={p1}/{p2}")
        sys.stdout.flush()
        scan_results.append(res)

    el_a = time.time() - t0
    print(f"\nTeil A fertig: {el_a:.0f}s")

    # ── Teil B ─────────────────────────────────────────────────
    print("\nTeil B: Look-Elsewhere Monte Carlo ...")
    sys.stdout.flush()

    observed_n_ratios = 57
    observed_ratio_range = (1.08, 420.0)
    observed_direct = 23
    observed_compound = 185
    n_mc = 10000

    direct_mc, compound_mc = look_elsewhere_mc(
        observed_n_ratios, observed_ratio_range, n_mc, TARGETS, TOL
    )

    mean_d = sum(direct_mc) / len(direct_mc)
    mean_c = sum(compound_mc) / len(compound_mc)
    p_direct = sum(1 for d in direct_mc if d >= observed_direct) / n_mc
    p_compound = sum(1 for c in compound_mc if c >= observed_compound) / n_mc
    max_d = max(direct_mc)
    max_c = max(compound_mc)

    el_b = time.time() - t0 - el_a
    print(f"  {el_b:.0f}s | E[direct]={mean_d:.1f} | E[compound]={mean_c:.1f}")
    print(f"  P(direct≥{observed_direct})={p_direct:.4f}")
    print(f"  P(compound≥{observed_compound})={p_compound:.4f}")

    # Also test with ratio range matching inert primes (narrower)
    print("\nKontrolle: Look-Elsewhere mit mod=7 Ratio-Range (1,103) ...")
    inert_n = 18
    inert_range = (2.0, 103.0)
    inert_observed_direct = 6
    inert_observed_compound = 30

    d_mc2, c_mc2 = look_elsewhere_mc(inert_n, inert_range, n_mc, TARGETS, TOL)
    mean_d2 = sum(d_mc2) / len(d_mc2)
    mean_c2 = sum(c_mc2) / len(c_mc2)
    p_d2 = sum(1 for d in d_mc2 if d >= inert_observed_direct) / n_mc
    p_c2 = sum(1 for c in c_mc2 if c >= inert_observed_compound) / n_mc

    print(f"  E[direct]={mean_d2:.1f}, P(≥{inert_observed_direct})={p_d2:.4f}")
    print(f"  E[compound]={mean_c2:.1f}, P(≥{inert_observed_compound})={p_c2:.4f}")

    total = time.time() - t0
    print(f"\nGesamtlaufzeit: {total:.0f}s")

    # ── write summary ─────────────────────────────────────────
    L = []
    L.append("# d/u-Vertiefung und Look-Elsewhere-Statistik")
    L.append("")
    L.append(f"- Laufzeit: {total:.0f}s")
    L.append("")

    L.append("## Teil A: d/u aus Gaußscher Faktor-Kopplung")
    L.append("")
    L.append("| Konfiguration | Konverg. | Versch. Ratios | d/u Hits | Alle Hits | Bestes d/u | Fehler |")
    L.append("|---------------|----------|----------------|----------|-----------|------------|--------|")
    for res in scan_results:
        du_str = "-"
        err_str = "-"
        if res["du_best"]:
            _, _, _, ratio, mh = res["du_best"]
            err = min(e for n, t, r, e in mh if n == "d/u")
            du_str = f"{ratio:.4f}"
            err_str = f"{err*100:.2f}%"
        L.append(f"| {res['label']} | {res['n_conv']} | {res['n_unique_ratios']} | "
                 f"{res['du_hits']} | {res['n_hits']} | {du_str} | {err_str} |")
    L.append("")

    for res in scan_results:
        if res["hits"]:
            L.append(f"### Treffer: {res['label']}")
            L.append("")
            L.append("| P_full | P_sub1 | P_sub2 | Ratio | Target | Fehler |")
            L.append("|--------|--------|--------|-------|--------|--------|")
            seen_rows = set()
            for pf, p1, p2, ratio, mh in sorted(res["hits"], key=lambda x: x[3]):
                for name, tgt, rat, err in mh:
                    row = f"| {pf} | {p1} | {p2} | {rat:.4f} | {name}={tgt} | {err*100:.2f}% |"
                    if row not in seen_rows:
                        L.append(row)
                        seen_rows.add(row)
            L.append("")

    # Ratio catalogs
    L.append("### Ratio-Kataloge")
    L.append("")
    for res in scan_results:
        rats = res["unique_ratios"][:50]
        L.append(f"**{res['label']}:** {rats}")
    L.append("")

    L.append("### Top-Perioden")
    L.append("")
    for res in scan_results:
        L.append(f"**{res['label']}:** {dict(res['top_periods'])}")
    L.append("")

    # Teil B
    L.append("## Teil B: Look-Elsewhere-Statistik")
    L.append("")
    L.append("### Frage: Wie viele Treffer erwarten wir rein zufällig?")
    L.append("")
    L.append(f"Setup: {n_mc} Monte-Carlo-Durchläufe, je {observed_n_ratios} zufällige Ratios "
             f"aus [{observed_ratio_range[0]}, {observed_ratio_range[1]}], "
             f"{len(TARGETS)} Targets, {TOL*100:.0f}% Toleranz")
    L.append("")
    L.append("| Metrik | Beobachtet (mod=13) | Erwartung (Zufall) | p-Wert |")
    L.append("|--------|---------------------|--------------------|--------|")
    L.append(f"| Direkte Treffer | {observed_direct} | {mean_d:.1f} (max {max_d}) | {p_direct:.4f} |")
    L.append(f"| Compound Treffer | {observed_compound} | {mean_c:.1f} (max {max_c}) | {p_compound:.4f} |")
    L.append("")

    if p_direct < 0.01:
        L.append(f"**Die direkten Treffer sind hochsignifikant (p={p_direct:.4f}).** "
                 "Zufällige Ratios erreichen fast nie so viele direkte Übereinstimmungen.")
    elif p_direct < 0.05:
        L.append(f"**Die direkten Treffer sind signifikant (p={p_direct:.4f}).**")
    else:
        L.append(f"**Die direkten Treffer sind NICHT signifikant (p={p_direct:.4f}).** "
                 "Zufällige Ratios produzieren ähnlich viele Treffer.")
    L.append("")

    if p_compound < 0.01:
        L.append(f"**Die Compound-Treffer sind hochsignifikant (p={p_compound:.4f}).**")
    elif p_compound < 0.05:
        L.append(f"**Die Compound-Treffer sind signifikant (p={p_compound:.4f}).**")
    else:
        L.append(f"**Die Compound-Treffer sind NICHT signifikant (p={p_compound:.4f}).** "
                 "Bei {observed_n_ratios} verschiedenen Ratios sind viele Compound-Hits "
                 "statistisch erwartbar.")
    L.append("")

    L.append("### Kontrolle: mod=7 (inert)")
    L.append("")
    L.append(f"Setup: {inert_n} Ratios aus [{inert_range[0]}, {inert_range[1]}]")
    L.append("")
    L.append("| Metrik | Beobachtet (mod=7) | Erwartung (Zufall) | p-Wert |")
    L.append("|--------|--------------------|--------------------|--------|")
    L.append(f"| Direkte | {inert_observed_direct} | {mean_d2:.1f} | {p_d2:.4f} |")
    L.append(f"| Compound | {inert_observed_compound} | {mean_c2:.1f} | {p_c2:.4f} |")
    L.append("")

    L.append("## Gesamtfazit")
    L.append("")
    L.append("*(wird manuell ergänzt nach Analyse der Ergebnisse)*")
    L.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"\nSummary: {OUT}")


if __name__ == "__main__":
    main()
