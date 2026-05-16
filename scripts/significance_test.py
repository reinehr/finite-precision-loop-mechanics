#!/usr/bin/env python3
"""
Signifikanztest: Wie selten sind simultane Treffer für π/e UND μ/e?

Drei Tests:
1. Nullhypothese: Zufällige Systeme (alle Primzahlen, alle k, alle Topologien)
2. Split-Primes (4k+1): Systematischer Vergleich
3. Gewichtvariation: Andere komplexe Kopplungen

Parallelisiert über multiprocessing (14 Kerne M4).
"""

import random
import math
import sys
import os
import time
from multiprocessing import Pool, cpu_count
from typing import List, Tuple, Dict, Optional

sys.path.insert(0, os.path.dirname(__file__))
from gaussian_loop import GaussInt, GaussianLoopSim

PI_E_TARGET = 273.19
MU_E_TARGET = 206.77
THRESHOLD = 0.01  # 1% Fehler = "Treffer"
THRESHOLD_LOOSE = 0.05  # 5% = "naher Treffer"

ALL_PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
              53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
SPLIT_PRIMES = [p for p in ALL_PRIMES if p % 4 == 1]  # 5,13,17,29,37,41,53,61,73,89,97
INERT_PRIMES = [p for p in ALL_PRIMES if p % 4 == 3]  # 3,7,11,19,23,31,43,47,59,67,71,79,83

WEIGHT_SPECS = [
    ("1,i", (1, 0), (0, 1)),
    ("1,1", (1, 0), (1, 0)),
    ("1,1+i", (1, 0), (1, 1)),
    ("1+i,i", (1, 1), (0, 1)),
    ("2,i", (2, 0), (0, 1)),
    ("1,2i", (1, 0), (0, 2)),
    ("1+i,1-i", (1, 1), (1, -1)),
    ("2+i,1", (2, 1), (1, 0)),
]


def make_weights(spec, mod):
    name, (lr, li), (rr, ri) = spec
    return GaussInt(lr % mod, li % mod, mod), GaussInt(rr % mod, ri % mod, mod)


def make_sim_with_weights(n_nodes, mod, w_left, w_right):
    """Erzeuge Sim mit benutzerdefinierten Gewichten."""
    sim = GaussianLoopSim(n_nodes, mod, "ring_symmetric")
    for j in range(n_nodes):
        sim.weights[j][(j - 1) % n_nodes] = w_left
        sim.weights[j][(j + 1) % n_nodes] = w_right
    return sim


def find_periods(n_nodes, mod, n_trials=100, max_steps=5000,
                 w_left=None, w_right=None, seed=None):
    """Finde alle Perioden für gegebene Konfiguration."""
    if seed is not None:
        random.seed(seed)
    periods = set()
    for _ in range(n_trials):
        if w_left is not None and w_right is not None:
            sim = make_sim_with_weights(n_nodes, mod, w_left, w_right)
        else:
            sim = GaussianLoopSim(n_nodes, mod, "ring")
        init = [GaussInt.random(mod) for _ in range(n_nodes)]
        att, period, _ = sim.find_attractor(max_steps=max_steps, init=init)
        if att is not None and period > 0:
            periods.add(period)
    return sorted(periods)


def check_ratios(periods: List[int]) -> Dict:
    """Prüfe ob Perioden-Verhältnisse π/e und μ/e treffen."""
    if len(periods) < 2:
        return {"pi_hit": False, "mu_hit": False, "pi_best": None, "mu_best": None,
                "pi_err": float('inf'), "mu_err": float('inf')}

    all_ratios = set()
    for i, p1 in enumerate(periods):
        for p2 in periods:
            if p2 > p1:
                all_ratios.add(p2 / p1)

    pi_best = min(all_ratios, key=lambda r: abs(r - PI_E_TARGET) / PI_E_TARGET) if all_ratios else 0
    mu_best = min(all_ratios, key=lambda r: abs(r - MU_E_TARGET) / MU_E_TARGET) if all_ratios else 0

    pi_err = abs(pi_best - PI_E_TARGET) / PI_E_TARGET if pi_best > 0 else float('inf')
    mu_err = abs(mu_best - MU_E_TARGET) / MU_E_TARGET if mu_best > 0 else float('inf')

    return {
        "pi_hit": pi_err < THRESHOLD,
        "mu_hit": mu_err < THRESHOLD,
        "pi_loose": pi_err < THRESHOLD_LOOSE,
        "mu_loose": mu_err < THRESHOLD_LOOSE,
        "pi_best": pi_best,
        "mu_best": mu_best,
        "pi_err": pi_err,
        "mu_err": mu_err,
        "n_periods": len(periods),
        "n_ratios": len(all_ratios),
        "max_ratio": max(all_ratios) if all_ratios else 0,
    }


def test_config(args):
    """Worker: teste eine (n, k, weight)-Konfiguration."""
    mod, k, w_spec, trial_seed = args
    w_name = w_spec[0] if w_spec else "default"
    try:
        if w_spec:
            w_left, w_right = make_weights(w_spec, mod)
            periods = find_periods(k, mod, n_trials=80, max_steps=4000,
                                   w_left=w_left, w_right=w_right, seed=trial_seed)
        else:
            periods = find_periods(k, mod, n_trials=80, max_steps=4000, seed=trial_seed)
        result = check_ratios(periods)
        result["mod"] = mod
        result["k"] = k
        result["weights"] = w_name
        result["periods"] = periods[:20]
        return result
    except Exception as e:
        return {"mod": mod, "k": k, "weights": w_name, "error": str(e)}


def test1_null_hypothesis():
    """Test 1: Wie oft treffen zufällige Konfigurationen π/e UND μ/e?"""
    print("=" * 80)
    print("TEST 1: NULLHYPOTHESE — Wie selten sind simultane Treffer?")
    print("=" * 80)

    configs = []
    for mod in ALL_PRIMES:
        for k in range(3, 8):
            for w_spec in WEIGHT_SPECS[:4]:
                configs.append((mod, k, w_spec, 42 + mod * 100 + k))

    print(f"Teste {len(configs)} Konfigurationen auf {cpu_count()} Kernen...")
    t0 = time.time()

    with Pool(min(cpu_count(), 14)) as pool:
        results = pool.map(test_config, configs)

    elapsed = time.time() - t0
    print(f"Fertig in {elapsed:.1f}s")

    valid = [r for r in results if "error" not in r and r.get("n_periods", 0) >= 2]
    pi_hits = [r for r in valid if r.get("pi_hit")]
    mu_hits = [r for r in valid if r.get("mu_hit")]
    both_hits = [r for r in valid if r.get("pi_hit") and r.get("mu_hit")]
    pi_loose = [r for r in valid if r.get("pi_loose")]
    mu_loose = [r for r in valid if r.get("mu_loose")]
    both_loose = [r for r in valid if r.get("pi_loose") and r.get("mu_loose")]

    n = len(valid)
    print(f"\nGültige Konfigurationen: {n}")
    print(f"\nTreffer (<1% Fehler):")
    print(f"  π/e allein: {len(pi_hits)}/{n} = {len(pi_hits)/n*100:.1f}%")
    print(f"  μ/e allein: {len(mu_hits)}/{n} = {len(mu_hits)/n*100:.1f}%")
    print(f"  BEIDE:      {len(both_hits)}/{n} = {len(both_hits)/n*100:.1f}%")
    print(f"\nNahe Treffer (<5% Fehler):")
    print(f"  π/e allein: {len(pi_loose)}/{n} = {len(pi_loose)/n*100:.1f}%")
    print(f"  μ/e allein: {len(mu_loose)}/{n} = {len(mu_loose)/n*100:.1f}%")
    print(f"  BEIDE:      {len(both_loose)}/{n} = {len(both_loose)/n*100:.1f}%")

    if both_hits:
        print(f"\n--- Simultane <1%-Treffer: ---")
        for r in sorted(both_hits, key=lambda x: x["pi_err"] + x["mu_err"]):
            print(f"  mod={r['mod']}, k={r['k']}, w={r['weights']}: "
                  f"π/e={r['pi_best']:.2f} ({r['pi_err']*100:.2f}%), "
                  f"μ/e={r['mu_best']:.2f} ({r['mu_err']*100:.2f}%), "
                  f"{r['n_periods']} Perioden")

    return valid, both_hits


def test2_split_vs_inert():
    """Test 2: Split-Primes (4k+1) vs. Inert-Primes (4k+3)."""
    print(f"\n{'='*80}")
    print("TEST 2: SPLIT-PRIMES vs. INERT-PRIMES")
    print(f"{'='*80}")

    configs = []
    for mod in ALL_PRIMES:
        for k in [4, 5, 6, 7]:
            configs.append((mod, k, WEIGHT_SPECS[0], 42 + mod * 100 + k))

    t0 = time.time()
    with Pool(min(cpu_count(), 14)) as pool:
        results = pool.map(test_config, configs)
    elapsed = time.time() - t0
    print(f"Fertig in {elapsed:.1f}s")

    valid = [r for r in results if "error" not in r and r.get("n_periods", 0) >= 2]

    split_results = [r for r in valid if r["mod"] in SPLIT_PRIMES]
    inert_results = [r for r in valid if r["mod"] in INERT_PRIMES]

    def stats(group, label):
        n = len(group)
        if n == 0:
            print(f"  {label}: keine Daten")
            return
        avg_periods = sum(r["n_periods"] for r in group) / n
        avg_max = sum(r["max_ratio"] for r in group) / n
        pi_hits = sum(1 for r in group if r.get("pi_loose"))
        mu_hits = sum(1 for r in group if r.get("mu_loose"))
        both = sum(1 for r in group if r.get("pi_loose") and r.get("mu_loose"))
        print(f"  {label} (n={n}):")
        print(f"    Mittlere #Perioden: {avg_periods:.1f}")
        print(f"    Mittleres max. Verhältnis: {avg_max:.1f}")
        print(f"    π/e <5%: {pi_hits} ({pi_hits/n*100:.0f}%)")
        print(f"    μ/e <5%: {mu_hits} ({mu_hits/n*100:.0f}%)")
        print(f"    Beide <5%: {both} ({both/n*100:.0f}%)")

    stats(split_results, "Split-Primes (4k+1)")
    stats(inert_results, "Inert-Primes (4k+3)")

    print(f"\n  Split-Primes: {SPLIT_PRIMES}")
    print(f"  Inert-Primes: {INERT_PRIMES}")

    # Detail: bester Treffer pro Prime
    print(f"\n  Detail pro Primzahl (Gewichte 1,i, bester k):")
    for mod in ALL_PRIMES:
        group = [r for r in valid if r["mod"] == mod]
        if not group:
            continue
        best = min(group, key=lambda r: r["pi_err"] + r["mu_err"])
        typ = "SPLIT" if mod in SPLIT_PRIMES else "INERT"
        print(f"    {mod:>3} ({typ}): k={best['k']}, "
              f"π/e={best['pi_best']:.1f} ({best['pi_err']*100:.1f}%), "
              f"μ/e={best['mu_best']:.1f} ({best['mu_err']*100:.1f}%), "
              f"{best['n_periods']} Perioden")


def test3_weight_variation():
    """Test 3: Gewichtvariation bei mod=13."""
    print(f"\n{'='*80}")
    print("TEST 3: GEWICHTVARIATION bei mod=13, k=6")
    print(f"{'='*80}")

    configs = []
    for w_spec in WEIGHT_SPECS:
        configs.append((13, 6, w_spec, 42))

    t0 = time.time()
    with Pool(min(cpu_count(), 14)) as pool:
        results = pool.map(test_config, configs)
    elapsed = time.time() - t0
    print(f"Fertig in {elapsed:.1f}s")

    print(f"\n{'Gewichte':<15} {'#Per':>4} {'MaxRatio':>10} "
          f"{'π/e':>10} {'err%':>6} {'μ/e':>10} {'err%':>6}")
    print("-" * 70)
    for r in results:
        if "error" in r:
            print(f"{r['weights']:<15} ERROR: {r['error']}")
            continue
        print(f"{r['weights']:<15} {r['n_periods']:>4} {r['max_ratio']:>10.1f} "
              f"{r.get('pi_best',0):>10.1f} {r.get('pi_err',1)*100:>5.1f}% "
              f"{r.get('mu_best',0):>10.1f} {r.get('mu_err',1)*100:>5.1f}%")


def main():
    print(f"Parallelisierung: {cpu_count()} Kerne verfügbar\n")
    test1_null_hypothesis()
    test2_split_vs_inert()
    test3_weight_variation()

    print(f"\n{'='*80}")
    print("ALLE TESTS ABGESCHLOSSEN")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
