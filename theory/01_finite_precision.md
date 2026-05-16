# Finite Precision

The starting assumption is not that the universe is a computer in any ordinary engineering sense. The starting assumption is weaker:

> what physically exists cannot require infinite actual precision.

A real physical state must be finitely instantiated. If a difference can never be physically distinguished, stored, transmitted, or acted upon, then treating that difference as actual rather than merely mathematical may be an over-idealization.

---

## Why Infinite Precision Is Suspicious

Continuous mathematics is extraordinarily successful, but it may be an effective language rather than an ontology.

Several motivations point in the same direction:

- finite regions appear to have finite information capacity;
- measurement never accesses infinite digits;
- dynamical chaos makes infinite precision physically consequential in a way no finite system can maintain;
- quantum theory already limits simultaneous distinguishability;
- gravitational/information bounds suggest that arbitrary information density is not physical.

The claim here is not that continuum mathematics is wrong. The claim is that continuum mathematics may describe the large-scale limit of a finite-precision process.

---

## Rounding Is Not Just Error

In ordinary numerical computation, rounding is an implementation flaw. In this framework, rounding is promoted to a possible physical mechanism.

Rounding means:

```text
two states closer than the resolution threshold become the same effective state
```

This creates:

- equivalence classes,
- thresholds,
- basins of attraction,
- ignored weak inputs,
- sudden transitions when thresholds are crossed.

These are exactly the ingredients needed for stability, inertia-like resistance, and effective interaction ranges.

---

## General Rounding, Not Just Truncation

The mechanism should not be imagined as universal downward truncation.

Pure truncation would bias every process in one direction and would likely drain the state space. The intended idea is more general:

```text
finite resolution maps many nearby possible values to one effective value
```

Depending on the local state, this can act like rounding up, rounding down, modular overflow, saturation, or thresholding.

The finite models in this repository use modular arithmetic because it is simple and reproducible:

```text
Z[i]/(p)
```

This is not claimed to be the final physical cut-off. It is a minimal finite test bed.

---

## Finite State Dynamics Forces Recurrence

A deterministic system with finitely many states cannot keep producing new states forever. Eventually it must revisit a previous state.

Once it revisits a state, the future repeats:

```text
x_t = x_s  ->  x_{t+1} = x_{s+1}  ->  ...
```

This creates an attractor cycle.

In this framework, recurrence is not a curiosity. It is the basic source of stable physical form.

---

## Physical Consequence

If finite precision is real, then small differences can disappear. That means small perturbations can fail to change the next effective state.

This is the seed of inertia:

```text
small perturbation -> rounded away -> loop remains itself
```

It is also the seed of effective range:

```text
weak influence -> below threshold -> no effective coupling
```

Finite precision therefore does not merely limit knowledge. It can create physical behavior.

