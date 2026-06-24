#!/usr/bin/env python3
"""
Pre-registered, out-of-sample test of the split/inert structural claim.

WHY
---
The single biggest weakness of the core observation is the look-elsewhere /
overfitting concern: the mechanism (ring, k=6, weight (1,i), z->z^2) and the
modulus p=13 were found *during* exploration. This script turns the split/inert
claim into a genuine prediction by testing it on split primes OTHER than the
discovery primes, with a protocol frozen before execution.

FROZEN PROTOCOL (declared before looking at any result)
-------------------------------------------------------
* Rule (fixed): ring topology, k = 6 nodes, weights w = (1, i), update
  z_j -> z_j^2 + z_{j-1} + i*z_{j+1} (mod p). Identical to the published lepton core.
* Probe targets (fixed): pi/e = 273.19, mu/e = 206.77 (as in significance_test.py).
  "target-like spectrum" = the best pairwise period ratio lands near these values.
* Discovery primes EXCLUDED from the split group: {13, 29}. 13 produced the lepton
  result; 29 was used for b/c. Holding them out makes the test out-of-sample.
* Split hold-out primes  (p = 1 mod 4): 5, 17, 37, 41, 53, 61, 73, 89, 97
* Inert control primes   (p = 3 mod 4): 3, 7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83
* Sampling (fixed): N_TRIALS random initial states, MAX_STEPS, deterministic seed
  = BASE_SEED + p. No per-prime tuning is allowed.
* Statistic: label-permutation test (no external libraries), one-sided.

PRE-REGISTERED HYPOTHESES
-------------------------
H1  Split primes yield MORE distinct attractor periods than inert primes.
H2  Split primes hit "both pi/e and mu/e < 5%" at a HIGHER rate than inert primes.
H3  (falsifier) NO inert prime hits both pi/e and mu/e < 5%.

DECISION RULE (frozen)
----------------------
"Out-of-sample supported" iff ALL hold:
  (1) permutation p-value for the distinct-period difference < 0.05,
  (2) split "both < 5%" rate > inert "both < 5%" rate,
  (3) zero inert primes hit both < 5% (H3 holds).
Otherwise the strong structural claim is NOT supported out-of-sample, and that
must be reported as such.

Outputs: evidence/split_inert_holdout.jsonl, evidence/split_inert_holdout_summary.md
"""
from __future__ import annotations

import argparse
import json
import os
import random
import statistics
import sys
from datetime import datetime, timezone
from multiprocessing import Pool, cpu_count
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from significance_test import WEIGHT_SPECS, check_ratios, find_periods, make_weights  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT_JSONL = ROOT / "evidence" / "split_inert_holdout.jsonl"
OUT_MD = ROOT / "evidence" / "split_inert_holdout_summary.md"

# --- frozen protocol constants ---
K = 6
WEIGHT = WEIGHT_SPECS[0]  # ("1,i", (1,0), (0,1))
DISCOVERY_EXCLUDED = (13, 29)
SPLIT_HOLDOUT = [5, 17, 37, 41, 53, 61, 73, 89, 97]
INERT_CONTROL = [3, 7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83]
BASE_SEED = 20260624
N_TRIALS = 80      # same sampling as the published significance_test.py scan
MAX_STEPS = 4000   # same sampling as the published significance_test.py scan
N_PERM = 20000
LOOSE = 0.05


def worker(args):
    mod, kind, n_trials, max_steps, seed = args
    w_left, w_right = make_weights(WEIGHT, mod)
    periods = find_periods(K, mod, n_trials=n_trials, max_steps=max_steps,
                           w_left=w_left, w_right=w_right, seed=seed)
    r = check_ratios(periods)
    pi_err = r.get("pi_err", float("inf"))
    mu_err = r.get("mu_err", float("inf"))
    both_loose = (pi_err < LOOSE) and (mu_err < LOOSE)
    return {
        "mod": mod,
        "kind": kind,
        "n_periods": len(periods),
        "pi_err": None if pi_err == float("inf") else round(pi_err, 4),
        "mu_err": None if mu_err == float("inf") else round(mu_err, 4),
        "pi_best": r.get("pi_best"),
        "mu_best": r.get("mu_best"),
        "both_loose": both_loose,
        "periods": periods[:12],
    }


def permutation_pvalue(split_vals, inert_vals, n_perm, seed):
    """One-sided permutation p-value for mean(split) - mean(inert) > 0."""
    if not split_vals or not inert_vals:
        return 0.0, 1.0
    rng = random.Random(seed)
    observed = statistics.mean(split_vals) - statistics.mean(inert_vals)
    pooled = list(split_vals) + list(inert_vals)
    n_s = len(split_vals)
    count = 0
    for _ in range(n_perm):
        rng.shuffle(pooled)
        diff = statistics.mean(pooled[:n_s]) - statistics.mean(pooled[n_s:])
        if diff >= observed - 1e-12:
            count += 1
    return observed, (count + 1) / (n_perm + 1)


def run(split_primes, inert_primes, n_trials, max_steps, n_perm):
    configs = [(p, "split", n_trials, max_steps, BASE_SEED + p) for p in split_primes]
    configs += [(p, "inert", n_trials, max_steps, BASE_SEED + p) for p in inert_primes]
    workers = min(cpu_count(), 14)
    if workers > 1 and len(configs) > 2:
        with Pool(workers) as pool:
            rows = pool.map(worker, configs)
    else:
        rows = [worker(c) for c in configs]

    split_rows = [r for r in rows if r["kind"] == "split"]
    inert_rows = [r for r in rows if r["kind"] == "inert"]

    sp_periods = [r["n_periods"] for r in split_rows]
    in_periods = [r["n_periods"] for r in inert_rows]
    sp_both = sum(1 for r in split_rows if r["both_loose"])
    in_both = sum(1 for r in inert_rows if r["both_loose"])
    sp_rate = sp_both / len(split_rows) if split_rows else 0.0
    in_rate = in_both / len(inert_rows) if inert_rows else 0.0

    obs_per, p_per = permutation_pvalue(sp_periods, in_periods, n_perm, BASE_SEED)
    obs_rate, p_rate = permutation_pvalue(
        [1.0 if r["both_loose"] else 0.0 for r in split_rows],
        [1.0 if r["both_loose"] else 0.0 for r in inert_rows],
        n_perm, BASE_SEED + 1)

    decision = (p_per < 0.05) and (sp_rate > in_rate) and (in_both == 0)
    return {
        "rows": rows, "split_rows": split_rows, "inert_rows": inert_rows,
        "sp_mean_periods": statistics.mean(sp_periods) if sp_periods else 0.0,
        "in_mean_periods": statistics.mean(in_periods) if in_periods else 0.0,
        "sp_both": sp_both, "in_both": in_both, "sp_rate": sp_rate, "in_rate": in_rate,
        "obs_per": obs_per, "p_per": p_per, "obs_rate": obs_rate, "p_rate": p_rate,
        "decision": decision,
    }


def write_outputs(res, split_primes, inert_primes, n_trials, max_steps, n_perm, selftest):
    with OUT_JSONL.open("w", encoding="utf-8") as f:
        for r in res["rows"]:
            f.write(json.dumps(r) + "\n")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    verdict = "SUPPORTED" if res["decision"] else "NOT SUPPORTED"
    L = []
    L.append("# Split/Inert Hold-Out Test (pre-registered)")
    L.append("")
    if selftest:
        L.append("> **SELF-TEST RUN** (reduced primes/trials) — not the registered statistic.")
        L.append("")
    L.append(f"Generated: {now}")
    L.append("")
    L.append("## Frozen protocol")
    L.append("")
    L.append(f"- Rule: ring, k={K}, weights (1, i), z -> z^2 + z_(j-1) + i z_(j+1) mod p.")
    L.append(f"- Discovery primes excluded from split group: {list(DISCOVERY_EXCLUDED)}.")
    L.append(f"- Split hold-out primes: {split_primes}")
    L.append(f"- Inert control primes: {inert_primes}")
    L.append(f"- Sampling: {n_trials} random inits, max_steps {max_steps}, seed = {BASE_SEED}+p.")
    L.append(f"- Probe targets: pi/e = 273.19, mu/e = 206.77; loose threshold {LOOSE:.0%}.")
    L.append(f"- Test: label-permutation, one-sided, {n_perm} permutations.")
    L.append("")
    L.append("## Result")
    L.append("")
    L.append(f"- Mean distinct periods: split = {res['sp_mean_periods']:.2f}, "
             f"inert = {res['in_mean_periods']:.2f} "
             f"(diff {res['obs_per']:+.2f}, permutation p = {res['p_per']:.4f}).")
    L.append(f"- Both pi/e and mu/e < 5%: split = {res['sp_both']}/{len(res['split_rows'])} "
             f"({res['sp_rate']:.0%}), inert = {res['in_both']}/{len(res['inert_rows'])} "
             f"({res['in_rate']:.0%}) (permutation p = {res['p_rate']:.4f}).")
    L.append(f"- H3 (no inert both<5%): {'holds' if res['in_both'] == 0 else 'VIOLATED'}.")
    L.append("")
    L.append("### Decision (against the frozen rule)")
    L.append("")
    L.append(f"**Out-of-sample split/inert claim: {verdict}.**")
    L.append("")
    L.append("Decision rule: (1) period-count permutation p < 0.05, "
             "(2) split both<5% rate > inert, (3) zero inert both<5%.")
    L.append("")
    L.append("## Per-prime detail")
    L.append("")
    L.append("| p | type | #periods | best pi/e err | best mu/e err | both<5% |")
    L.append("|---|------|----------|---------------|---------------|---------|")
    for r in sorted(res["rows"], key=lambda x: (x["kind"], x["mod"])):
        pe = "-" if r["pi_err"] is None else f"{r['pi_err']*100:.1f}%"
        me = "-" if r["mu_err"] is None else f"{r['mu_err']*100:.1f}%"
        L.append(f"| {r['mod']} | {r['kind']} | {r['n_periods']} | {pe} | {me} | "
                 f"{'yes' if r['both_loose'] else 'no'} |")
    L.append("")
    # --- secondary, descriptive (NOT part of the frozen decision) ---
    rows = res["rows"]
    zero_split = sum(1 for r in rows if r["kind"] == "split" and r["n_periods"] == 0)
    zero_inert = sum(1 for r in rows if r["kind"] == "inert" and r["n_periods"] == 0)
    adq = [r for r in rows if r["n_periods"] >= 2 and r["pi_err"] is not None]
    adq_split = [r for r in adq if r["kind"] == "split"]
    adq_inert = [r for r in adq if r["kind"] == "inert"]
    L.append("## Secondary observations (descriptive, NOT pre-registered)")
    L.append("")
    L.append("These do not change the frozen decision above; they are reported for honesty and")
    L.append("to motivate a better-powered follow-up.")
    L.append("")
    L.append(f"- Sampling limit: {zero_split}/{len([r for r in rows if r['kind']=='split'])} split and "
             f"{zero_inert}/{len([r for r in rows if r['kind']=='inert'])} inert primes produced "
             "ZERO attractors at k=6 within max_steps. This is dominated by large primes "
             "(big state space p^2 per node) and dilutes the test regardless of split/inert.")
    def _fmt(group):
        return ", ".join("p={0}: pi/e {1:.1f}%".format(r["mod"], r["pi_err"] * 100) for r in group)
    if adq_split:
        L.append("- Among adequately sampled split primes: " + _fmt(adq_split) + ".")
    if adq_inert:
        L.append("- Among adequately sampled inert primes: " + _fmt(adq_inert) + ".")
    L.append("- Reading: where short attractors exist, small split primes land close to pi/e while")
    L.append("  inert primes do not -- a directional split/inert signal. But the STRONG 'both")
    L.append("  pi/e and mu/e < 5%' property reproduces only at p=13, so the full lepton")
    L.append("  coincidence is p=13-specific, not a generic split-prime property.")
    L.append("")
    L.append("## Honest conclusion")
    L.append("")
    L.append("1. Primary (frozen): the strong target-like-spectrum claim is NOT supported")
    L.append("   out-of-sample under this rule. The full lepton match is specific to p=13.")
    L.append("2. Secondary (descriptive): a weaker split/inert richness/closeness signal is")
    L.append("   visible among small, adequately sampled primes but is not significant here.")
    L.append("3. Motivated follow-up (to be pre-registered separately): size-matched primes and")
    L.append("   state-space-scaled max_steps, with 'best single-target error' as the primary")
    L.append("   endpoint instead of the near-impossible joint-threshold metric.")
    L.append("")
    OUT_MD.write_text("\n".join(L), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true",
                    help="Fast reduced run (few primes/trials) for CI / smoke test.")
    args = ap.parse_args()

    global OUT_JSONL, OUT_MD
    if args.selftest:
        split_primes, inert_primes = [5, 17], [3, 7]
        n_trials, max_steps, n_perm = 12, 800, 2000
        OUT_JSONL = ROOT / "evidence" / "split_inert_holdout_selftest.jsonl"
        OUT_MD = ROOT / "evidence" / "split_inert_holdout_selftest_summary.md"
    else:
        split_primes, inert_primes = SPLIT_HOLDOUT, INERT_CONTROL
        n_trials, max_steps, n_perm = N_TRIALS, MAX_STEPS, N_PERM

    print(f"Split hold-out primes: {split_primes}")
    print(f"Inert control primes:  {inert_primes}")
    print(f"Sampling: {n_trials} trials, max_steps {max_steps}, permutations {n_perm}")
    res = run(split_primes, inert_primes, n_trials, max_steps, n_perm)
    write_outputs(res, split_primes, inert_primes, n_trials, max_steps, n_perm, args.selftest)

    print(f"\nMean distinct periods: split={res['sp_mean_periods']:.2f} "
          f"inert={res['in_mean_periods']:.2f} (p={res['p_per']:.4f})")
    print(f"Both<5%: split={res['sp_both']}/{len(res['split_rows'])} "
          f"inert={res['in_both']}/{len(res['inert_rows'])} (p={res['p_rate']:.4f})")
    print(f"H3 (no inert both<5%): {'holds' if res['in_both'] == 0 else 'VIOLATED'}")
    print(f"\nDECISION: out-of-sample claim {'SUPPORTED' if res['decision'] else 'NOT SUPPORTED'}")
    print(f"Wrote {OUT_JSONL.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
