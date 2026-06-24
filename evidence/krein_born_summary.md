# Krein / Indefinite Born Check

Generated: 2026-06-24 13:08 UTC  ·  system: Z[i]/(13), k=6, ring, weights (1, i)

## 1. Algebraic structure (exact, verified numerically)

- sqrt(-1) mod 13 = 5; map phi(a+bi) = (a+5b, a-5b).
- Ring homomorphism Z[i]/(13) -> F_13 x F_13: VERIFIED (mult), VERIFIED (square), on 500 samples.
- Conjugation swaps the two coordinates (parity/spin flip): VERIFIED.
- Norm N(z)=a^2+b^2 equals the hyperbolic product u*v: VERIFIED.

So the natural norm is INDEFINITE (signature (+,-) via u*v = x^2 - y^2):
a finite analogue of a Krein inner product. chi(N) in {+1,-1,0} labels the
positive-norm / negative-norm / null sectors.

## 2. Signature of the lepton attractors

- Distinct attractors found: 792 (from 4000 random inits).
- Basin-weighted state signature: positive (chi=+1) 40.5%, negative (chi=-1) 40.5%, null (chi=0) 19.0%.
- Conjugate states found within the SAME (1, i) attractor set: 0 (expected ~0).
  Reason: conjugation sends the (1, i) rule to the (1, -i) rule, so the parity/spin
  partner of a (1, i) attractor lives in the (1, -i) system. The proper spin-doublet
  test therefore compares the (1, i) and (1, -i) systems -- a clean next experiment.

## 3. Born-style re-check (indefinite)

Spearman correlation of basin size with:
- fraction of NULL-sector states:     -0.050
- fraction of POSITIVE-sector states: +0.066
- mean (positive-definite) norm:      +0.005
- cycle-summed unsigned norm conserved along longest attractor: False

## Honest reading

- CONFIRMED (algebra): on the split prime the dynamics decomposes into two F_p
  sectors swapped by conjugation, and the natural norm is the indefinite form
  u*v. This is a real, exact structural fact and the right setting for a
  Krein/negative-norm reading (cf. Turok-Bateman quadratic gravity).
- The signature distribution and basin correlations above are the data; if all
  correlations are weak (|rho| small), an indefinite Born law is NOT yet
  demonstrated -- only the correct arena for it is established. State that plainly.
- Next: test a sign-fixed Krein functional |<psi|psi>| as the conserved quantity,
  and whether positive/negative sectors map to the cw/ccw spin doublet.
