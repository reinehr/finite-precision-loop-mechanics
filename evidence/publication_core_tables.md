# Publication Core Tables

Generated: 2026-05-16 02:38 UTC

This file is the one-command reproduction target for the first, narrow publication core.
It intentionally separates direct/core observations from compound or exploratory claims.

Command:

```bash
python3 scripts/reproduce_publication_core.py
```

For heavier recomputation before table generation:

```bash
python3 scripts/reproduce_publication_core.py --recompute
```

## Lepton Core

| Target | Experimental ratio | Model value | Error | Match type | Scope |
|---|---|---|---|---|---|
| pi/e | 273.19 | 273.00 | 0.07% | direct period | p=13, k=6, w=(1,i)/(i,1) |
| mu/e | 206.77 | 207.00 | 0.11% | period ratio | p=13, k=6, w=(1,i)/(i,1) |
| tau/e | 3477.23 | 3475.3 | 0.06% | compound | larger search space |

## Quark Core

| Target | Experimental ratio | Model value | Error | Match type | Scope |
|---|---|---|---|---|---|
| d/u | 2.14 | 15/7 = 2.1429 | 0.13% | focused direct statistic | p=13 |
| c/s | 13.7 | 41/3 = 13.6667 | 0.24% | sub-loop ratio | (3+2i)/(3-2i), p=13 |
| t/b | 41.4 | 41.0 | 0.97% | sub-loop ratio | (3+2i)/(3-2i), p=13 |
| b/c | 3.28 | 23/7 = 3.2857 | 0.17% | secondary modulus | p=29 |

## Split/Inert Control

Lepton control from the symmetric `Z[i]/p` scan. The claim is limited to tested symmetric setups unless a formal proof is supplied.

| Metric | Split primes | Inert primes |
|---|---|---|
| mean number of periods | 6.1 | 3.1 |
| pi/e <5% | 13% | 0% |
| mu/e <5% | 13% | 0% |
| both <5% | 7% | 0% |

## Entropy Scan For Polynomial Degree

| Degree d | Converged | Distinct periods | Shannon entropy | pi/e error | mu/e error |
|---|---|---|---|---|---|
| 1 | 3000/3000 | 1 | 0.00 | --- | --- |
| 2 | 2764/3000 | 33 | 3.72 | 0.07% | 0.11% |
| 3 | 1918/3000 | 27 | 3.17 | 1.03% | 3.01% |
| 4 | 568/3000 | 18 | 2.47 | 11.28% | 2.31% |
| 5 | 2943/3000 | 13 | 2.02 | 0.07% | 10.03% |

## Null Model References

- `scripts/significance_test.py`: configuration-level lepton search and split/inert control.
- `scripts/significance_v2.py`: type-conditional random-period null model.
- `scripts/quark_du_and_stats.py`: quark direct-hit look-elsewhere Monte Carlo.
- `scripts/quark_masses.py`: coupled sub-loop quark-ratio scan.
- `scripts/entropy_degree_scan.py`: degree scan for `z -> z^d`.

## Explicit Limitations

- The historical exploratory search space is larger than any single script.
- Ratio and compound matches carry larger effective search spaces than direct period matches.
- `alpha`, gauge symmetries, Lorentz invariance, and scattering amplitudes are not derived.
- The update rule is entropy-supported but not proven from a first-principles action.
