# Loop Traps

A loop trap is a stable or metastable process cycle created by finite precision.

It is important to avoid a misunderstanding:

```text
"loop" means recurrence in process/state space,
not necessarily a literal circle in pre-existing space.
```

The topology used in a toy model can be a ring, simplex, coupled graph, or something else. The essence is the repeated return of the whole process state.

---

## Basic Mechanism

The finite update rule has the form:

```text
state(t+1) = update(state(t)) with finite precision
```

Because the state space is finite, any long enough trajectory must either fail to converge within the observation window or enter a cycle.

Once a cycle forms:

```text
A -> B -> C -> A
```

the process has a stable identity across ticks.

This is the root of particle-like persistence.

---

## Why Rounding Helps Stability

In a continuous chaotic system, almost-closed loops usually miss closure. Tiny differences matter forever.

In a finite-precision system, near misses can be mapped to the same effective state:

```text
almost A -> rounded to A
```

This creates a capture region around the cycle. The loop does not need to close with infinite precision. It only needs to close within the rounding basin.

That is why rounding is described as a "glue":

```text
finite precision turns approximate recurrence into actual recurrence
```

---

## Stability And Decay

The same rounding that stabilizes a loop can also destabilize it.

If a perturbation remains inside the basin:

```text
perturbed state -> rounded back into cycle
```

If it crosses a threshold:

```text
perturbed state -> different successor -> escape or transition
```

This gives a natural qualitative distinction between:

- stable particles,
- metastable particles,
- decay channels,
- threshold reactions.

---

## Mass-Ratio Evidence

The numerical evidence in this repository uses finite systems on:

```text
Z[i]/(p)
```

The observed period spectra contain ratios close to several Standard Model mass ratios. This does not prove the physical interpretation, but it shows that loop traps in a small finite phase-like system can generate nontrivial structured spectra.

That is why the calculations matter: they keep the loop-trap mechanism testable.

