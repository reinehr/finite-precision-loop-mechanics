# Inertia From Rounding

Inertia is usually treated as a primitive property of mass. In this mechanism, inertia is reinterpreted as a consequence of loop stability under finite precision.

The key claim:

> inertia is the resistance of a stable loop trap against being forced into a different attractor continuation.

---

## Not Just "Many Internal Operations"

It is tempting to say that matter has inertia because many operations happen inside the loop. That is only part of the story.

The deeper point is:

```text
the loop has a self-closure condition
```

Each tick is not arbitrary. It must continue the cycle in a way that returns to itself. A perturbation is therefore not merely added to a passive object. It tries to redirect a self-maintaining process.

---

## Threshold Mechanism

Finite precision creates a basin around an attractor.

If a perturbation is smaller than the relevant rounding threshold:

```text
state + perturbation -> same rounded successor
```

Then the loop continues as before. From outside, this looks like resistance:

```text
input applied, no state change observed
```

Only when the perturbation is large enough to alter the effective successor state does the loop respond.

This naturally resembles:

- reaction thresholds,
- stability basins,
- activation energies,
- resistance to acceleration.

---

## Internal Dominance

A loop trap is not a single stored value. It is a dense internal process.

Each update combines:

- local self-processing,
- neighboring inputs,
- self-coupling,
- finite rounding.

An external input is only one more contribution to a process already dominated by internal terms. Unless it changes the rounded successor, it is absorbed.

Thus inertia has two sides:

```text
basin threshold + internal self-closure
```

---

## Mass As Stability Scale

This suggests a possible mass proxy:

```text
mass-like behavior ~ difficulty of redirecting the loop
```

Candidate measures:

- basin size,
- return probability after perturbation,
- minimum perturbation needed to change attractor,
- internal operation density,
- period/frequency structure.

The numerical mass-ratio work currently uses periods and period ratios. A stronger theory would connect those ratios to perturbation resistance and basin geometry.

---

## Testable Direction

A future test should compare, for the same attractor family:

```text
period ratio
basin size
return rate after perturbation
minimum escape threshold
```

If these quantities correlate in the right way, inertia becomes more than interpretation. It becomes measurable inside the finite dynamics.

