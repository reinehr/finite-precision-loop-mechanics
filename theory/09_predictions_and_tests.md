# Predictions And Tests

The mechanism should not remain only a story. It must produce tests that can fail.

This file separates near-term computational tests from longer-term physical ambitions.

---

## Test 1: Residue Balance

Claim:

```text
stable unperturbed loops should have balanced net residue over a full period
```

Test:

1. For each attractor, compute the unmodded intermediate sum `S_j`.
2. Compute residue `R_j = S_j - (S_j mod p)`.
3. Sum residues across nodes and across one full period.
4. Compare stable and unstable attractors.

Possible falsification:

```text
stable attractors show arbitrary non-canceling residue with no structure
```

---

## Test 2: Perturbed Residue Emission

Claim:

```text
perturbations should create non-canceling residue before transition or decay
```

Test:

1. Start on a known attractor.
2. Apply controlled perturbations of increasing size.
3. Measure return, transition, escape, and residue imbalance.
4. Check whether residue imbalance predicts escape.

---

## Test 3: Inertia Proxy

Claim:

```text
mass-like resistance should correlate with basin geometry and return rates
```

Test:

For each attractor, measure:

- period,
- basin size,
- return probability after perturbation,
- minimum perturbation that changes attractor,
- residue imbalance under perturbation.

The theory becomes stronger if these measures form a coherent hierarchy.

---

## Test 4: Interaction Sectors

Claim:

```text
loop asymmetries classify into interaction-like sectors
```

Test:

1. Classify attractors by chirality, phase rotation, residue pattern, and coupling asymmetry.
2. Couple pairs of attractors.
3. Measure attraction, repulsion, transition, or composite closure.
4. Check whether complementary sectors behave systematically.

---

## Test 5: Sub-Loop Confinement

Claim:

```text
some sub-loops only close as composite attractors
```

Test:

1. Compare isolated sub-loops with coupled sub-loop systems.
2. Measure period richness, convergence, and basin structure.
3. Attempt separation by weakening coupling.
4. Check whether new composites form instead of isolated sub-loops.

---

## Test 6: Emergent Dimension

Claim:

```text
potential pressure plus loop stability favors effective 3D relational geometry
```

Test:

1. Simulate many loop traps in adaptive relational graphs.
2. Allow residue or potential pressure to modify couplings.
3. Estimate effective graph dimension.
4. Check whether dimension near 3 is selected.

---

## Evidence Already Present

Current evidence is narrower:

- `Z[i]/(p)` attractor spectra are nontrivial.
- `p=13, k=6, w=(1,i)/(i,1)` gives close lepton-ratio coincidences.
- split primes and inert primes differ sharply in tested symmetric scans.
- coupled sub-loops produce quark-ratio coincidences.
- degree `d=2` maximizes attractor entropy among tested polynomial degrees.

These results do not prove the mechanism. They justify testing it.

---

## What Would Most Damage The Program?

The mechanism would be weakened if:

- residue accounting shows no conservation-like structure;
- perturbation resistance does not correlate with any mass-like proxy;
- split/inert differences vanish under cleaner replication;
- period-ratio hits disappear under stricter pre-registered target lists;
- adaptive relational simulations do not show any tendency toward stable effective dimension.

The project should welcome these tests. A mechanism that cannot be broken cannot become physics.

