# Mixing-Angle Program (the "bigger swing")

**Status:** design + first exploratory probe (2026-06)
**Goal:** extend the mass-ratio observation to flavor MIXING (CKM / PMNS angles),
without repeating the look-elsewhere mistake exposed by the split/inert hold-out test.

This document is the roadmap. The first numbers live in
[`../scripts/mixing_angle_explore.py`](../scripts/mixing_angle_explore.py) and
[`mixing_angles_explore_summary.md`](mixing_angles_explore_summary.md).

---

## 1. Why this is the right next target

The core result reproduces mass *ratios*. The obvious next structure in the Standard
Model is the **mixing** between flavor and mass eigenstates: the CKM matrix (quarks)
and the PMNS matrix (neutrinos). If the `Z[i]/(p)` picture is more than numerology, a
mixing structure should be *derivable from the same algebra*, not added by hand.

Crucially, the split decomposition already gives a two-sector structure:

```
For p = 1 mod 4:  Z[i]/(p)  ~  F_p x F_p ,   z = a+bi  ->  (a+rb, a-rb),  r^2 = -1.
```

Mixing is, generically, a **rotation between two sectors**. We now *have* two sectors.

## 2. Targets (measured, degrees)

| Matrix | theta12 | theta23 | theta13 |
|--------|---------|---------|---------|
| CKM    | 13.04 (Cabibbo) | 2.38 | 0.20 |
| PMNS   | 33.41 (solar)   | 49.0 (atm) | 8.54 (reactor) |

## 3. Three candidate routes

### Route A — Gatto bridge (masses -> Cabibbo)
The Gatto-Sartori-Tonin relation `sin(theta_C) ~ sqrt(m_d/m_s)` is a celebrated,
model-independent-ish flavor relation. The model already targets the down sector, so
this is a **consistency bridge**: if the model yields `m_s/m_d ~ 20`, then
`asin(sqrt(1/20)) = 12.9 deg`, i.e. the Cabibbo angle, *by construction*.
- Strength: links the EXISTING mass result to mixing.
- Weakness: not an independent prediction; re-expresses a mass ratio as an angle.

### Route B — Gaussian-factor arguments (geometry)
Each split prime `p = a^2 + b^2` carries an intrinsic angle `arg(a+bi) = atan2(b,a)`.
The up/down symmetry is already broken by `(a+bi)/(a-bi)`; its argument is a natural
candidate mixing angle.
- First-probe coincidences (NOT yet evidence): `arg(3+2i) = 33.69 deg` vs PMNS solar
  `33.41 deg`; `arg(4+i) = 14.04 deg` vs Cabibbo `13.04 deg`.
- Weakness: many primes x many transforms = large search space (see Section 5).

### Route C — Krein two-sector decomposition (IMPLEMENTED)
Implemented and verified in [`../scripts/route_c_two_sector.py`](../scripts/route_c_two_sector.py),
summary [`route_c_two_sector_summary.md`](route_c_two_sector_summary.md).

**Verified structural theorem (exact, parameter-free, p = 13, 17, 29):** under
`phi(a+bi) = (a + r b, a - r b)` with `r^2 = -1`, the `(1,i)` rule decomposes EXACTLY
into two independent real `F_p` systems with neighbor weights `+r` and `-r`; complex
conjugation `(1,i) -> (1,-i)` swaps the two sectors. So the lepton rule's "imaginary
coupling" (chirality) IS exactly the `+r` vs `-r` asymmetry between the two Krein
sectors. The two sectors have DIFFERENT period spectra (verified), confirming the
chirality is dynamically substantive, not a relabeling.

**Mixing-angle verdict (honest):** a *parameter-free* mixing angle is NOT well defined
from this decomposition. `r` is a residue mod `p`, not a length, so an angle built from
`r` is a category error (and the eigenvector equation for multiplication-by-`i` is
degenerate over `F_p`). Route C therefore yields a clean structural theorem but **no**
forced Cabibbo angle. It redirects the program to Route A.

## 4. First exploratory result (honest)

20 declared candidates (routes A + B), 2% relative threshold:

- sub-threshold matches: **2** (`arg(3+2i)`->PMNS solar; Gatto->Cabibbo)
- chance-expected (uniform-angle null): **0.95**
- Poisson look-elsewhere p-value `P(X>=2) = 0.24`  =>  **consistent with chance.**

Conclusion: the *arena* is plausible and there are tantalizing individual coincidences,
but there is **no significant signal yet**. The coincidences only define the candidate
set for a registered test.

## 5. The discipline (lesson carried from the hold-out test)

The split/inert hold-out test
([`split_inert_holdout_summary.md`](split_inert_holdout_summary.md)) showed that an
in-sample coincidence (the lepton match at p=13) did **not** generalize. The same trap
applies here even more strongly, because angles are dense in `[0,90]`. Therefore:

1. **Fix the candidate generator and the target list in advance.** No adding primes,
   transforms, or targets after seeing errors.
2. **Report the search-space size and the chance expectation every time** (the script
   does this automatically).
3. **Prefer an independent prediction (Route C) over a re-expression (Route A).**

## 6. Pre-registration sketch for the registered test

- **Primary endpoint:** Route C. Predict one angle (relating the two-sector phase
  windings of the canonical `p=13`, `k=6` system) with NO free parameter, then compare
  to the Cabibbo angle. Pass iff within a pre-declared 5% and the chance expectation for
  the single declared observable is < 0.1.
- **Secondary:** Route B restricted to the *one* prime already used for the sector it
  describes (p=13 for the lepton/solar sector; p=17 for the s/d Cabibbo sector), to keep
  the search space at O(1) rather than O(primes x transforms).
- **Falsifier:** if the Route C two-sector phase does not produce a stable angle, or the
  angle is far from any CKM/PMNS value, Route C is rejected and only the (weak) Gatto
  consistency remains.

## 7. Status and next concrete step

**Done:** Route C is implemented (the exact two-sector decomposition theorem). It shows
the program cannot get a mixing angle from `r`-geometry; the geometric coincidences of
Route B are chance-consistent.

**Therefore the live route is A (Gatto), and its blocker is concrete:** `sin theta_C ~
sqrt(m_d/m_s)` needs the model's `s/d` ratio, which is the project's weakest quark
result (`>3%` or compound; the `mod=17`, `(4+i)` route improved it toward `~1%`). The
actionable next step is to FIX `s/d` first (a dedicated `mod=17` sub-loop scan), then
apply Gatto and check whether the Cabibbo angle follows with the look-elsewhere budget
of a single declared observable. Mixing should be pursued through masses, not geometry.
