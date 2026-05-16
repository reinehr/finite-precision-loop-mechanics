# Finite Precision Loop Mechanics

This repository presents a mechanism-first idea:

> If physical processes have finite precision, then rounding is not merely an error. It can become a physical mechanism: it creates thresholds, residues, attractor basins, loop traps, inertia-like resistance, radiation-like leakage, interaction modes, and eventually an emergent relational space.

The numerical mass-ratio results are important, but they are not the starting point. They are evidence that this finite-precision mechanics may generate nontrivial particle-like structure in a concrete model.

---

## Core Intuition

The project begins with a conservative physical suspicion:

```text
No actual physical system can carry infinite precision.
```

If this is true, then physical evolution cannot be a perfectly continuous computation over infinitely resolved real numbers. It must contain some form of finite state, finite distinguishability, or effective rounding.

In a finite deterministic state space, processes eventually repeat. Most repetitions are uninteresting. Some, however, can become stable attractor cycles. This repository calls those cycles **loop traps**.

The central hypothesis is:

```text
matter-like behavior = stable loop-trapped process
light-like behavior  = linear untrapped process
```

---

## Mechanism Before Numerics

The intended order of ideas is:

1. **Finite precision:** why exact real-valued physical states are suspect.
2. **Linear process:** why light is modeled as an untrapped one-input/one-output process.
3. **Loop trap:** how finite precision and self-reference can close a process into an attractor.
4. **Schmalznudel mechanism:** how a small self-coupled loop can behave like trapped light.
5. **Inertia:** why rounding thresholds make a stable loop resist perturbation.
6. **Residues:** why discarded/overflowing potential suggests radiation, decay, or vacuum noise.
7. **Interactions:** how loop asymmetries and coupled sub-loops suggest force-like modes.
8. **Emergent space:** why relations between loops, not a background container, may become space.
9. **Numerical evidence:** why the `Z[i]/(p)` calculations are worth taking seriously.

The calculations are therefore a test bed for the mechanism, not the whole point.

---

## Repository Map

```text
theory/
  00_core_thesis.md
  01_finite_precision.md
  02_light_as_linear_process.md
  03_loop_traps.md
  04_schmalznudel_mechanism.md
  05_inertia_from_rounding.md
  06_residue_radiation_decay.md
  07_interactions.md
  08_emergent_3d_space.md
  09_predictions_and_tests.md

evidence/
  PUBLICATION_CORE.md
  SEARCH_AUDIT.md
  SKEPTIC_REVIEW_PACKAGE.md
  publication_core_tables.md
  REPRODUCIBILITY.md
  supporting scan summaries

scripts/
  reproduce_publication_core.py
  gaussian_loop.py
  significance_test.py
  quark_masses.py
  quark_du_and_stats.py
  entropy_degree_scan.py

latex/
  preprint.tex
```

---

## One-Command Evidence Check

From the repository root:

```bash
python3 scripts/reproduce_publication_core.py
```

This writes:

```text
evidence/publication_core_tables.md
```

For a heavier recomputation of selected upstream evidence:

```bash
python3 scripts/reproduce_publication_core.py --recompute
```

---

## What The Model Claims

The mechanism claims, cautiously:

- finite precision can create attractor basins;
- attractor basins can stabilize loop-like processes;
- stable loop traps can resist small perturbations;
- this resistance is a candidate mechanism for inertia;
- rounding residues are candidate mechanisms for radiation, decay, and vacuum-like fluctuations;
- asymmetric loops and coupled sub-loops are candidate mechanisms for interaction modes;
- spatial structure may emerge from stable relations and potential pressure between loops;
- concrete finite systems on `Z[i]/(p)` produce nontrivial period spectra and mass-ratio coincidences.

---

## What It Does Not Claim

This repository does not claim to have derived:

- the full Standard Model,
- gauge symmetry in its established mathematical form,
- Lorentz invariance,
- scattering amplitudes,
- quantum field theory,
- gravity,
- the fine-structure constant,
- consciousness,
- a completed Theory of Everything.

The broad speculative ontology is intentionally kept out of this public core.

---

## Recommended Reading Order

Start with the mechanism:

1. `theory/00_core_thesis.md`
2. `theory/01_finite_precision.md`
3. `theory/02_light_as_linear_process.md`
4. `theory/03_loop_traps.md`
5. `theory/04_schmalznudel_mechanism.md`

Then read the physical consequences:

6. `theory/05_inertia_from_rounding.md`
7. `theory/06_residue_radiation_decay.md`
8. `theory/07_interactions.md`
9. `theory/08_emergent_3d_space.md`
10. `theory/09_predictions_and_tests.md`

Then inspect the evidence:

11. `evidence/PUBLICATION_CORE.md`
12. `evidence/SEARCH_AUDIT.md`
13. `evidence/publication_core_tables.md`
14. `latex/preprint.tex`

---

## Status

This is a speculative research program with a reproducible numerical core. The goal is not to present a finished theory, but to make the mechanism clear enough that it can be criticized, falsified, or improved.

