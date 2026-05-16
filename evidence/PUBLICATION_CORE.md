# Publication Core

**Status:** working definition for a narrow first publication

This file isolates the part of the project that can be shown to external physicists or mathematical physicists without requiring them to evaluate the broader TOE, consciousness, retrocausal, or cosmological interpretation.

---

## Narrow Claim

The proposed publication claim is:

> Attractor periods of a finite dynamical system on Gaussian integers modulo `p` show unexpectedly close coincidences with several Standard Model mass ratios, and the split/inert prime distinction provides a nontrivial algebraic control.

This is deliberately weaker than:

- a derivation of the Standard Model,
- a derivation of mass from first principles,
- a Theory of Everything,
- an explanation of space, time, gravity, consciousness, or the fine-structure constant.

The correct framing is **observation plus candidate mechanism**, not completed theory.

---

## Core System

The publication core uses a finite state space:

```text
z_j(t) in Z[i]/(p)
```

with the update rule:

```text
z_j(t+1) = z_j(t)^2 + w_L z_{j-1}(t) + w_R z_{j+1}(t) mod p
```

For the lepton scan, the primary configuration is:

```text
p = 13
k = 6
topology = ring
weights = (1, i) or (i, 1)
```

For the quark scan, the primary mechanism is a coupled `k=3 + k=3` system using the Gaussian factorization:

```text
13 = (3 + 2i)(3 - 2i)
```

The physical interpretation is intentionally limited to:

```text
period ratios as candidate mass-ratio proxies
```

No claim is made that the full particle ontology has been derived.

---

## What Belongs In The First Preprint

- Definition of the finite dynamical system.
- Exact search protocol and parameter accounting.
- Lepton mass-ratio coincidences.
- Quark sub-loop ratio coincidences.
- Split-prime versus inert-prime comparison.
- Null models and look-elsewhere accounting.
- Entropy scan supporting `d=2` as a non-arbitrary update choice.
- Reproducibility commands and code availability.
- Negative results and limitations.

---

## What Must Stay Out

The first preprint should not include:

- consciousness as fundamental,
- retrocausality or two-boundary cosmology,
- the lightning/Omega hypothesis,
- theology,
- free will,
- emergent 3D space,
- gravity,
- claims that matter, time, and space have been derived,
- claims that this is a complete TOE.

Those ideas can remain in the repository as broader motivation, but they increase the chance that the narrow numerical observation is dismissed before it is evaluated.

---

## Conservative Language

Use:

- "coincides with"
- "is close to"
- "candidate mechanism"
- "finite dynamical observation"
- "structural control"
- "within the tested search space"

Avoid:

- "proves"
- "derives"
- "explains the Standard Model"
- "Theory of Everything"
- "the origin of matter"
- "fundamental law"

---

## Strongest Point

The strongest point is not any single numerical hit. It is the combination of:

1. a small finite dynamical system,
2. repeated period coincidences,
3. a split/inert algebraic distinction in `Z[i]`,
4. explicit negative controls,
5. reproducible scripts.

This combination is what may make the observation worth expert scrutiny.

---

## Weakest Points

- The target list and search space were developed during exploration, so meta-look-elsewhere risk remains.
- The update rule is motivated and entropy-supported, but not derived from a physical action principle.
- The fine-structure constant `alpha` has not been derived; several attempts failed.
- Gauge symmetry, Lorentz invariance, spin-statistics, and scattering amplitudes are not addressed.
- Some quark and compound results have larger search spaces than direct period matches.

These should be stated plainly in the preprint, not hidden.

