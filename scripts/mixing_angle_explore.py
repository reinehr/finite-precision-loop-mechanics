#!/usr/bin/env python3
"""
Exploratory probe: can mixing angles (CKM / PMNS) arise in the Z[i]/(p) picture?

This is the FIRST step of the "bigger swing": extending the mass-ratio observation
to flavor MIXING. It is deliberately exploratory and -- having learned the lesson
from scripts/split_inert_holdout_test.py -- it accounts for its own search space.

THREE CANDIDATE ROUTES (declared up front)
------------------------------------------
A. Gatto-Sartori-Tonin relation:  sin(theta_C) ~ sqrt(m_d / m_s).
   The model already targets down-sector mass ratios, so this is a consistency
   bridge from masses to the Cabibbo angle.
B. Gaussian-factor arguments:  each split prime p = a^2 + b^2 gives a natural angle
   arg(a + b i) = atan2(b, a) and simple transforms.  Mixing as geometry of the
   factorization that already breaks up/down symmetry.
C. (future) Krein two-sector relative phase: the relative winding of an attractor
   in the two F_p sectors of the split decomposition (needs the (1,i) vs (1,-i)
   comparison from krein_born_check.py). Not computed here; see the program doc.

HONESTY
-------
Finding ONE angle near ONE target proves nothing if many candidates were scanned.
This script reports the number of comparisons and the chance-expected number of
sub-threshold matches, so any apparent hit is judged against look-elsewhere.

Output: evidence/mixing_angles_explore_summary.md
"""
from __future__ import annotations

import math
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_MD = ROOT / "evidence" / "mixing_angles_explore_summary.md"

# Measured mixing angles in degrees (PDG / NuFIT, normal ordering).
TARGETS = {
    "CKM theta12 (Cabibbo)": 13.04,
    "CKM theta23": 2.38,
    "CKM theta13": 0.20,
    "PMNS theta12 (solar)": 33.41,
    "PMNS theta23 (atm)": 49.0,
    "PMNS theta13 (reactor)": 8.54,
}

# Split primes p = a^2 + b^2 (p = 1 mod 4) used or adjacent in the model.
SPLIT_FACTORS = {
    5: (2, 1), 13: (3, 2), 17: (4, 1), 29: (5, 2), 37: (6, 1), 41: (5, 4),
}

# Experimental down-sector mass ratio for the Gatto bridge.
MS_OVER_MD_EXP = 20.0  # PDG range ~17-22; central ~20.


def candidate_angles():
    """Return list of (label, angle_deg). Declared, bounded candidate set."""
    cands = []
    for p, (a, b) in SPLIT_FACTORS.items():
        base = math.degrees(math.atan2(b, a))
        cands.append((f"arg({a}+{b}i) [p={p}]", base))
        cands.append((f"90-arg({a}+{b}i) [p={p}]", 90.0 - base))
        cands.append((f"2*arg({a}+{b}i) [p={p}]", (2 * base) % 90.0))
    # Gatto bridge (route A), as sin(theta)=sqrt(md/ms) and tan form.
    g = math.degrees(math.asin(math.sqrt(1.0 / MS_OVER_MD_EXP)))
    cands.append((f"asin(sqrt(md/ms)), ms/md={MS_OVER_MD_EXP:g}", g))
    gt = math.degrees(math.atan(math.sqrt(1.0 / MS_OVER_MD_EXP)))
    cands.append((f"atan(sqrt(md/ms)), ms/md={MS_OVER_MD_EXP:g}", gt))
    return cands


def nearest_target(angle):
    best_name, best_err = None, float("inf")
    for name, t in TARGETS.items():
        err = abs(angle - t) / t
        if err < best_err:
            best_name, best_err = name, err
    return best_name, best_err


def chance_expectation(n_candidates, threshold):
    """Expected number of candidates within `threshold` of ANY target,
    if candidate angles were uniform on [0, 90)."""
    # P(uniform angle within rel-threshold of target t) ~ 2*threshold*t/90, summed,
    # capped at 1 per candidate.
    p_any = min(1.0, sum(2.0 * threshold * t / 90.0 for t in TARGETS.values()))
    return n_candidates * p_any, p_any


def main():
    cands = candidate_angles()
    threshold = 0.02  # 2% relative
    rows = []
    hits = 0
    for label, ang in cands:
        name, err = nearest_target(ang)
        is_hit = err < threshold
        hits += int(is_hit)
        rows.append((label, ang, name, err, is_hit))

    exp_hits, p_any = chance_expectation(len(cands), threshold)
    # Poisson tail P(X >= hits | mean = exp_hits): honest look-elsewhere p-value.
    pois = math.exp(-exp_hits) * sum(exp_hits ** i / math.factorial(i) for i in range(hits))
    look_elsewhere_p = 1.0 - pois  # P(X >= hits)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    L = []
    L.append("# Mixing Angles: First Exploratory Probe")
    L.append("")
    L.append(f"Generated: {now}")
    L.append("")
    L.append("Targets (deg): " + ", ".join(f"{k.split(' ')[0]} {k.split('(')[-1].rstrip(')')}"
             f"={v}" for k, v in TARGETS.items()))
    L.append("")
    L.append(f"Candidates scanned: {len(cands)} · match threshold: {threshold:.0%} relative")
    L.append("")
    L.append("| candidate | angle (deg) | nearest target | rel. error | < threshold |")
    L.append("|-----------|-------------|----------------|------------|-------------|")
    for label, ang, name, err, is_hit in sorted(rows, key=lambda r: r[3]):
        L.append(f"| {label} | {ang:.2f} | {name} | {err*100:.1f}% | "
                 f"{'YES' if is_hit else ''} |")
    L.append("")
    L.append("## Look-elsewhere assessment")
    L.append("")
    L.append(f"- Sub-threshold matches observed: **{hits}**.")
    L.append(f"- Chance-expected matches (uniform-angle null): **{exp_hits:.2f}** "
             f"(per-candidate hit prob ~ {p_any:.3f}).")
    L.append(f"- Poisson look-elsewhere p-value, P(X >= {hits}): **{look_elsewhere_p:.2f}**.")
    if look_elsewhere_p > 0.05:
        L.append("- => The observed matches are **consistent with chance** (p > 0.05). No")
        L.append("  significant mixing-angle signal yet. Do NOT report individual coincidences")
        L.append("  as evidence; they only define the registered candidate set below.")
    else:
        L.append("- => Observed matches exceed chance at p < 0.05. Suggestive, but must still be")
        L.append("  confirmed by a pre-registered, narrowed protocol before any claim.")
    L.append("")
    L.append("## Notable individual coincidences (for the registered follow-up only)")
    L.append("")
    L.append("- arg(3+2i) = 33.69 deg vs PMNS solar 33.41 deg (the p=13 lepton/quark prime).")
    L.append("- arg(4+i) = 14.04 deg vs Cabibbo 13.04 deg (p=17, the s/d-improving prime).")
    L.append("- Gatto sqrt(md/ms) reproduces the Cabibbo angle by construction if the model")
    L.append("  yields ms/md ~ 20; this links the EXISTING mass result to mixing.")
    L.append("")
    L.append("These are listed as PRE-REGISTRATION candidates, not as results. The honest")
    L.append("status is: the arena is plausible; nothing here is yet established.")
    L.append("")
    OUT_MD.write_text("\n".join(L), encoding="utf-8")

    print(f"Candidates: {len(cands)}  sub-{threshold:.0%} matches: {hits}  "
          f"chance-expected: {exp_hits:.2f}")
    for label, ang, name, err, is_hit in sorted(rows, key=lambda r: r[3])[:6]:
        print(f"  {label:32s} {ang:6.2f}  -> {name:24s} {err*100:5.1f}%"
              f"{'  <hit>' if is_hit else ''}")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
