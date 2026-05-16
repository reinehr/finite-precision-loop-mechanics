# Residue, Radiation, And Decay

Finite precision creates a question that ordinary modular simulations often hide:

> what happens to the part of the update that does not fit into the finite register?

In a toy model, this part is simply discarded by `mod p`. In a physical mechanism, it may correspond to radiation, decay products, vacuum fluctuation, or changing coupling structure.

---

## The Residue

For a loop node:

```text
S_j = z_j(t)^2 + sum_k w[j,k] z_k(t)
z_j(t+1) = S_j mod p
```

The residue is:

```text
R_j = S_j - (S_j mod p)
```

In the simplest simulation, only `z_j(t+1)` remains. But if process potential is conserved or approximately conserved, `R_j` must go somewhere.

---

## Stable Loops Do Not Radiate

A stable loop should not emit net radiation in its unperturbed state.

That suggests:

```text
sum of residues over a full attractor period = 0
```

or at least:

```text
net residue is internally reabsorbed over the cycle
```

This is a natural explanation of why a stationary matter-like loop can be internally active without continuously radiating away.

---

## Perturbed Loops Radiate

If an external perturbation changes the intermediate sums, then the residue pattern may no longer cancel over one period.

Then:

```text
non-canceling residue -> emitted linear process
```

This gives a candidate mechanism for radiation:

- accelerated or disturbed loops change their residue balance;
- the unbalanced part leaves as a linear light-like process;
- the loop may settle into a new attractor or decay completely.

---

## Decay

The same rounding that stabilizes a loop can destabilize it near thresholds.

If a fluctuation pushes the state across a basin boundary:

```text
loop attractor -> transition state -> different attractor or linear outputs
```

This is a qualitative model of decay:

- stable loops have deep basins;
- metastable loops have accessible escape channels;
- decay probability is basin-boundary statistics plus perturbation/noise structure.

---

## Vacuum-Like Noise

Even if net residue cancels over a full period, short-lived residue imbalances may exist inside the cycle.

Those imbalances are candidates for vacuum-like fluctuations:

```text
temporary residue -> local fluctuation -> reabsorbed
```

This connects the loop mechanism to the idea that "empty" space may contain unresolved process activity rather than literal nothingness.

---

## Testable Direction

The next tests should compute residues explicitly:

1. For stable attractors, measure total residue over a full period.
2. Perturb the attractor and measure non-canceling residue.
3. Check whether residue emission correlates with escape probability.
4. Check whether residue channels map to observed transition hierarchies.

If residue conservation or residue emission patterns appear, the mechanism gains a real physical handle.

