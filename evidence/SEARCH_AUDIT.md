# Search Audit For Publication Core

**Status:** methodological audit for a skeptic-facing preprint

This document makes the search space explicit. Its purpose is to reduce ambiguity around look-elsewhere effects and to separate preprint-ready claims from exploratory material.

---

## Core Dynamical System

Lepton-sector scans use:

```text
state:      z_j in Z[i]/(p)
topology:   ring of k nodes
update:     z_j(t+1) = z_j(t)^2 + w_L z_{j-1}(t) + w_R z_{j+1}(t) mod p
observable: attractor period set and period ratios
```

Quark-sector scans use:

```text
state:      two coupled sub-loops, usually k=3 + k=3
observable: sub-loop periods inside the composite attractor
primary asymmetry: conjugate Gaussian factors of split primes
```

---

## Target Ratios

### Primary Lepton Targets

These are the strongest simple-period/period-ratio targets used in the current preprint:

| Target | Value | Status |
|--------|-------|--------|
| `pi/e` | 273.19 | direct period match in the core configuration |
| `mu/e` | 206.77 | period-ratio match in the core configuration |
| `tau/e` | 3477.23 | compound result; larger search space |
| `tau/mu` | 16.817 | supporting factor for `tau/e` compound |

### Primary Quark Targets

The current quark scan target list is:

| Target | Value |
|--------|-------|
| `d/u` | 2.14 |
| `c/s` | 13.7 |
| `t/b` | 41.4 |
| `s/d` | 19.8 |
| `s/u` | 42.3 |
| `c/u` | 579.5 |
| `b/c` | 3.28 |

For the first publication, the safest quark claims are the sub-percent direct/sub-period coincidences:

| Target | Model value | Error | Comment |
|--------|-------------|-------|---------|
| `c/s` | `41/3 = 13.6667` | 0.24% | appears under `(3+2i)/(3-2i)` coupling |
| `t/b` | `41.0` | 0.97% | appears under `(3+2i)/(3-2i)` coupling |
| `d/u` | `15/7 = 2.1429` | 0.13% | from focused `quark_du_and_stats.py` result |
| `b/c` | `23/7 = 3.2857` | 0.17% | mod 29 result, not same core modulus |

The preprint should clearly label which of these come from the same `p=13` mechanism and which require a secondary modulus or focused scan.

---

## Thresholds

Current scripts use two common thresholds:

| Threshold | Meaning | Used in |
|-----------|---------|---------|
| `<1%` | tight hit | lepton uniqueness / headline comparisons |
| `<5%` | loose hit | broader robustness, null models, quark scan inclusion |

The preprint should not mix these without labeling them. A recommended convention:

- headline table: report exact percent error, no binary label;
- tight claims: `<1%`;
- robustness tables: `<5%`, explicitly called loose.

---

## Lepton Search Accounting

`scripts/significance_test.py`:

```text
primes:      24 primes from 3 to 97
k:           3..7
weights:     first 4 weight specs for null test
configs:     480
valid:       196 with at least two periods
trials:      80 per configuration
max_steps:   4000
targets:     pi/e, mu/e
thresholds:  1% tight, 5% loose
```

Key reported result:

```text
Only one simultaneous <1% pi/e and mu/e hit:
p=13, k=6, weights=(1,i)
```

`theory/significance-results.md` further reports an ultra-scan:

```text
Phase A: 1790 configurations
Phase B: 360 focused configurations
primes: split primes up to 197 plus inert controls
result: all focused simultaneous <1% pi/e and mu/e hits remain at p=13, k=6, weights=(1,i)/(i,1)
```

The exact ultra-scan raw artifacts should remain available when making a public claim.

---

## Split/Inert Control

The split/inert distinction is the strongest structural control because it is not a continuously fitted parameter.

From `scripts/significance_test.py` and `theory/significance-results.md`:

```text
split primes: p = 1 mod 4
inert primes: p = 3 mod 4
comparison setup: k in {4,5,6,7}, weights=(1,i)
metric: period richness and pi/e, mu/e loose hits
```

Reported lepton-control table:

| Metric | Split | Inert |
|--------|-------|-------|
| mean number of periods | 6.1 | 3.1 |
| `pi/e <5%` | 13% | 0% |
| `mu/e <5%` | 13% | 0% |
| both `<5%` | 7% | 0% |

Important caveat:

```text
The strongest defensible statement is "zero in the tested symmetric setups",
not "mathematically impossible in every conceivable setup", unless a proof is supplied.
```

---

## Quark Search Accounting

`scripts/quark_masses.py`:

```text
moduli:       13 by default; 17 supported for a secondary scan
systems:      k=3+k=3 and k=3+k=6
weight specs: 13 base specs for mod 13; extra factor specs for mod 17
trials:       300 per configuration
max_steps:    5000
threshold:    5%
targets:      d/u, c/s, t/b, s/d, s/u, c/u, b/c
```

For publication, avoid presenting all 5% matches as equally strong. Prefer a tiering:

1. **Gaussian-factor direct/sub-period results** from `(3+2i)/(3-2i)`.
2. **Focused d/u statistics** from `quark_du_and_stats.py`.
3. **Secondary-modulus result** such as `b/c` at mod 29.
4. **Compound or one-way-coupling hits** as exploratory only.

---

## Null Models

### Null Model 1: Configuration Search

Used in `significance_test.py`:

```text
Compare many finite-ring configurations across primes, k, and weights.
Measure how often pi/e and mu/e are hit by period ratios.
```

This is useful but not sufficient because the project searched many ideas over time.

### Null Model 2: Type-Conditional Random Periods

Used in `significance_v2.py`:

```text
null samples: 2000
catalogs per sample: 126
targets: 16
matching: direct, ratio, compound
period counts and max period are preserved per configuration
period values are randomized
```

Reported result:

```text
p(all 16 best <= observed best) < 0.0005
```

Caveat:

```text
The robust-hit criterion alone is not discriminative; same-type error sharpness is more meaningful.
```

### Null Model 3: Quark Look-Elsewhere

Reported in `theory/quark_du_stats_summary.md`:

```text
Monte Carlo runs: 10000
direct hits observed: 23
direct hits expected: 1.2
reported p: < 0.0001
```

This should be cited with the exact script and randomization method.

---

## Known Look-Elsewhere Risks

- The project contains many exploratory scripts and summaries.
- Some targets were added after initial discoveries.
- Ratio and compound matching expand the effective search space.
- Multiple moduli, topologies, and coupling schemes have been tried.
- Some claims rely on focused follow-up scans.

Recommended preprint language:

```text
The numerical coincidences are not presented as a derivation. They are an observation that remains interesting because the same small algebraic setting recurs under several controls. The effective historical search space is larger than any single script, and this is a limitation.
```

---

## Minimum Publication-Ready Evidence Package

A skeptic should be able to run one command to regenerate:

1. core lepton table,
2. split/inert control table,
3. core quark table,
4. entropy-by-degree table,
5. list of limitations and null-model references.

This is implemented in:

```bash
python3 scripts/reproduce_publication_core.py
```

The command writes:

```text
evidence/publication_core_tables.md
```

