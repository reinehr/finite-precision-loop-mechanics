#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entropie-Scan: Vergleiche z -> z^d fuer verschiedene Grade d auf Z[i]/(n).

Frage: Ist d=2 (Quadrierung) optimal fuer die Attraktor-Reichhaltigkeit?
Messe: Anzahl Orbits, Periodenspektrum, Entropie der Basin-Verteilung
fuer d = 1, 2, 3, 4, 5 auf Z[i]/(13) mit k=6, ring, w=(1,i).

14 Kerne M4. Laufzeit: ~3 min.
"""

import math
import random
import time
from collections import defaultdict
from multiprocessing import Pool, cpu_count
from pathlib import Path

from gaussian_loop import GaussInt, GaussianLoopSim

ROOT = Path(__file__).resolve().parents[1]
MOD = 13
K = 6
WORKERS = min(cpu_count(), 14)
MAX_STEPS = 6000
N_SAMPLES = 3000
OUT = str(ROOT / "evidence" / "entropy_degree_summary.md")


class DegreeSim(GaussianLoopSim):
    """Erweiterte Simulation mit variablem Polynomgrad."""

    def __init__(self, n_nodes, modulus, degree=2, topology="ring"):
        super().__init__(n_nodes, modulus, topology)
        self.degree = degree

    def step(self, nonlinear=True):
        new_state = []
        for j in range(self.n_nodes):
            s = GaussInt.zero(self.mod)
            for k_idx in range(self.n_nodes):
                s = s + self.weights[j][k_idx] * self.state[k_idx]
            if nonlinear:
                z = self.state[j]
                zd = z
                for _ in range(self.degree - 1):
                    zd = zd * z
                s = zd + s
            new_state.append(s)
        self.state = new_state


def _worker(args):
    degree, seed = args
    random.seed(seed)
    sim = DegreeSim(K, MOD, degree=degree, topology="ring")
    init = [GaussInt.random(MOD) for _ in range(K)]
    sim.state = init

    seen = {}
    traj = []
    for t in range(MAX_STEPS):
        key = sim.state_key()
        if key in seen:
            period = t - seen[key]
            return {"degree": degree, "period": period, "converged": True}
        seen[key] = t
        traj.append(key)
        sim.step()
    return {"degree": degree, "period": 0, "converged": False}


def shannon_entropy(counts):
    total = sum(counts.values())
    if total == 0:
        return 0
    h = 0
    for c in counts.values():
        if c > 0:
            p = c / total
            h -= p * math.log2(p)
    return h


def main():
    t0 = time.time()
    degrees = [1, 2, 3, 4, 5]
    print("Entropie-Scan: z -> z^d auf Z[i]/({}), k={}, ring".format(MOD, K))
    print("Grade: {}".format(degrees))
    print()

    results_by_degree = defaultdict(list)
    configs = []
    for d in degrees:
        for i in range(N_SAMPLES):
            configs.append((d, 900000 + d * 100000 + i))

    with Pool(WORKERS) as pool:
        for r in pool.imap_unordered(_worker, configs, chunksize=50):
            results_by_degree[r["degree"]].append(r)

    lines = []
    lines.append("# Entropie-Scan: Polynomgrad und Attraktor-Reichhaltigkeit")
    lines.append("")
    lines.append("**Stand:** 2026-02-22")
    lines.append("**Frage:** Ist d=2 (z -> z^2) optimal fuer die Attraktorlandschaft?")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append("- Z[i]/({}), k={}, ring, w=(1,i)".format(MOD, K))
    lines.append("- {} Samples pro Grad".format(N_SAMPLES))
    lines.append("- Grade d = {}".format(degrees))
    lines.append("")
    lines.append("## Ergebnisse")
    lines.append("")
    lines.append("| Grad d | Konvergiert | Versch. Perioden | Max Periode | "
                 "Shannon-Entropie | SM-Treffer pi/e | SM-Treffer mu/e |")
    lines.append("|--------|-------------|------------------|-------------|"
                 "------------------|-----------------|-----------------|")

    summary = {}
    for d in degrees:
        rs = results_by_degree[d]
        converged = [r for r in rs if r["converged"]]
        period_counts = defaultdict(int)
        for r in converged:
            period_counts[r["period"]] += 1

        n_conv = len(converged)
        n_periods = len(period_counts)
        max_period = max(period_counts.keys()) if period_counts else 0
        entropy = shannon_entropy(period_counts)

        sm_pi_e = 273.19
        sm_mu_e = 206.77
        pi_hit = "---"
        mu_hit = "---"
        if n_periods >= 2:
            periods = sorted(period_counts.keys())
            ratios = set()
            for i, p1 in enumerate(periods):
                for p2 in periods[i+1:]:
                    if p1 > 0:
                        ratios.add(p2 / p1)
                    if p2 > 0:
                        ratios.add(p1 / p2)
            best_pi = min(ratios, key=lambda r: abs(r - sm_pi_e)) if ratios else 0
            best_mu = min(ratios, key=lambda r: abs(r - sm_mu_e)) if ratios else 0
            pi_err = abs(best_pi - sm_pi_e) / sm_pi_e * 100 if best_pi > 0 else 999
            mu_err = abs(best_mu - sm_mu_e) / sm_mu_e * 100 if best_mu > 0 else 999
            pi_hit = "{:.2f}%".format(pi_err) if pi_err < 50 else ">50%"
            mu_hit = "{:.2f}%".format(mu_err) if mu_err < 50 else ">50%"

        lines.append("| **d={}** | {}/{} | {} | {} | {:.2f} | {} | {} |".format(
            d, n_conv, len(rs), n_periods, max_period, entropy, pi_hit, mu_hit))
        summary[d] = {
            "n_conv": n_conv, "n_periods": n_periods, "max_period": max_period,
            "entropy": entropy,
        }

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")

    if summary.get(2, {}).get("entropy", 0) >= max(
            summary.get(d, {}).get("entropy", 0) for d in degrees if d != 2):
        lines.append("**d=2 hat die hoechste Shannon-Entropie** unter allen getesteten Graden.")
        lines.append("Das stuetzt das Argument: z -> z^2 maximiert die Attraktor-Vielfalt")
        lines.append("bei minimalem Polynomgrad.")
    else:
        best_d = max(degrees, key=lambda d: summary.get(d, {}).get("entropy", 0))
        lines.append("**d={} hat die hoechste Shannon-Entropie.** ".format(best_d))
        if best_d > 2:
            lines.append("d=2 ist NICHT optimal — hoehere Grade erzeugen reichere Spektren.")
            lines.append("Das schwaechtdas Entropie-Argument fuer z -> z^2.")
        elif best_d == 1:
            lines.append("d=1 (linear) dominiert — unerwartetes Ergebnis.")

    lines.append("")
    lines.append("## Perioden-Spektren (Top-10 pro Grad)")
    lines.append("")
    for d in degrees:
        rs = results_by_degree[d]
        converged = [r for r in rs if r["converged"]]
        period_counts = defaultdict(int)
        for r in converged:
            period_counts[r["period"]] += 1
        top = sorted(period_counts.items(), key=lambda x: -x[1])[:10]
        lines.append("### d={}".format(d))
        lines.append("")
        lines.append("| Periode | Count |")
        lines.append("|---------|-------|")
        for p, c in top:
            lines.append("| {} | {} |".format(p, c))
        lines.append("")

    elapsed = time.time() - t0
    lines.append("---")
    lines.append("Laufzeit: {:.1f}s".format(elapsed))
    lines.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("Summary: {}".format(OUT))
    print("Laufzeit: {:.1f}s".format(elapsed))


if __name__ == "__main__":
    main()
