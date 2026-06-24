# Split/Inert Hold-Out Test (pre-registered)

Generated: 2026-06-24 13:04 UTC

## Frozen protocol

- Rule: ring, k=6, weights (1, i), z -> z^2 + z_(j-1) + i z_(j+1) mod p.
- Discovery primes excluded from split group: [13, 29].
- Split hold-out primes: [5, 17, 37, 41, 53, 61, 73, 89, 97]
- Inert control primes: [3, 7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83]
- Sampling: 80 random inits, max_steps 4000, seed = 20260624+p.
- Probe targets: pi/e = 273.19, mu/e = 206.77; loose threshold 5%.
- Test: label-permutation, one-sided, 20000 permutations.

## Result

- Mean distinct periods: split = 2.22, inert = 0.77 (diff +1.45, permutation p = 0.1740).
- Both pi/e and mu/e < 5%: split = 0/9 (0%), inert = 0/13 (0%) (permutation p = 1.0000).
- H3 (no inert both<5%): holds.

### Decision (against the frozen rule)

**Out-of-sample split/inert claim: NOT SUPPORTED.**

Decision rule: (1) period-count permutation p < 0.05, (2) split both<5% rate > inert, (3) zero inert both<5%.

## Per-prime detail

| p | type | #periods | best pi/e err | best mu/e err | both<5% |
|---|------|----------|---------------|---------------|---------|
| 3 | inert | 4 | 69.2% | 59.4% | no |
| 7 | inert | 5 | 72.2% | 63.2% | no |
| 11 | inert | 1 | - | - | no |
| 19 | inert | 0 | - | - | no |
| 23 | inert | 0 | - | - | no |
| 31 | inert | 0 | - | - | no |
| 43 | inert | 0 | - | - | no |
| 47 | inert | 0 | - | - | no |
| 59 | inert | 0 | - | - | no |
| 67 | inert | 0 | - | - | no |
| 71 | inert | 0 | - | - | no |
| 79 | inert | 0 | - | - | no |
| 83 | inert | 0 | - | - | no |
| 5 | split | 8 | 1.6% | 7.4% | no |
| 17 | split | 11 | 1.3% | 29.6% | no |
| 37 | split | 1 | - | - | no |
| 41 | split | 0 | - | - | no |
| 53 | split | 0 | - | - | no |
| 61 | split | 0 | - | - | no |
| 73 | split | 0 | - | - | no |
| 89 | split | 0 | - | - | no |
| 97 | split | 0 | - | - | no |

## Secondary observations (descriptive, NOT pre-registered)

These do not change the frozen decision above; they are reported for honesty and
to motivate a better-powered follow-up.

- Sampling limit: 6/9 split and 10/13 inert primes produced ZERO attractors at k=6 within max_steps. This is dominated by large primes (big state space p^2 per node) and dilutes the test regardless of split/inert.
- Among adequately sampled split primes: p=5: pi/e 1.6%, p=17: pi/e 1.3%.
- Among adequately sampled inert primes: p=3: pi/e 69.2%, p=7: pi/e 72.2%.
- Reading: where short attractors exist, small split primes land close to pi/e while
  inert primes do not -- a directional split/inert signal. But the STRONG 'both
  pi/e and mu/e < 5%' property reproduces only at p=13, so the full lepton
  coincidence is p=13-specific, not a generic split-prime property.

## Honest conclusion

1. Primary (frozen): the strong target-like-spectrum claim is NOT supported
   out-of-sample under this rule. The full lepton match is specific to p=13.
2. Secondary (descriptive): a weaker split/inert richness/closeness signal is
   visible among small, adequately sampled primes but is not significant here.
3. Motivated follow-up (to be pre-registered separately): size-matched primes and
   state-space-scaled max_steps, with 'best single-target error' as the primary
   endpoint instead of the near-impossible joint-threshold metric.
