# Skeptic Review Package

**Purpose:** send-ready package for external physicists, mathematical physicists, or discrete-dynamics researchers.

This package is intentionally narrow. It asks reviewers to assess whether the finite-dynamical observation is real, nontrivial, and worth formalizing. It does **not** ask them to evaluate the broader TOE framework.

---

## Files To Send

Send these files first:

1. `latex/preprint.tex`
2. `evidence/PUBLICATION_CORE.md`
3. `evidence/SEARCH_AUDIT.md`
4. `evidence/publication_core_tables.md`
5. `scripts/reproduce_publication_core.py`
6. `theory/04_schmalznudel_mechanism.md` (optional mechanism layer; not the headline claim)

Optional supporting files:

1. `theory/significance-results.md`
2. `theory/significance_v2_summary.md`
3. `theory/quark_du_stats_summary.md`
4. `theory/quark_masses_summary.md`
5. `theory/entropy_degree_summary.md`
6. `evidence/REPRODUCIBILITY.md`

Repository command for the first check:

```bash
python3 scripts/reproduce_publication_core.py
```

---

## Reviewer Profiles

Ask for harsh feedback from 2-3 people with different biases:

1. **Mathematical physicist / dynamical systems person**
   - Can judge whether the finite-state attractor observation is mathematically interesting.
   - Best at spotting trivial period-spectrum artifacts.

2. **Particle phenomenology or lattice/gauge person**
   - Can judge whether the mass-ratio framing is physically meaningful or misleading.
   - Best at identifying missing Standard Model structure.

3. **Number theory / finite fields / algebraic dynamics person**
   - Can judge whether the split/inert control is genuinely nontrivial.
   - Best at suggesting a proof or a sharper counterexample.

Do not start with broad TOE audiences. Start with people who will try to kill the core claim.

---

## Email Template

Subject:

```text
Request for critical feedback: finite Gaussian-ring attractors and SM mass-ratio coincidences
```

Body:

```text
Dear [Name],

I am not a physicist, and I would value a critical assessment before making anything public.

I have a small numerical observation in mathematical physics: attractor periods of a finite dynamical system on Gaussian integers modulo p appear close to several Standard Model mass ratios. The strongest structural control is the split/inert prime distinction in Z[i]: within the tested symmetric setups, split primes produce target-like spectra while inert primes do not.

I am not claiming a Theory of Everything or a derivation of the Standard Model. The question is narrower:

1. Is the observation nontrivial, or is it likely ordinary numerology / overfitting?
2. Is the split/inert control mathematically meaningful in this context?
3. What is the first falsifying or sanity-check calculation you would demand?
4. Is the search-space accounting sufficient, or is the look-elsewhere problem still fatal?

The quickest reproduction command is:

python3 scripts/reproduce_publication_core.py

I would be grateful for blunt feedback, including a recommendation not to publish if that is your view.

Best,
Jakob Reinehr
```

---

## Questions For Reviewers

Ask each reviewer to answer these directly:

1. Is the narrow observation clear enough to evaluate independently?
2. Is the update rule too ad hoc, or is the entropy-degree scan a meaningful partial defense?
3. Does the split/inert distinction reduce the numerology concern?
4. Are the null models appropriate?
5. Which result should be removed from the preprint because it has too much search freedom?
6. What calculation would most quickly falsify the core claim?
7. Would you recommend posting this as an arXiv observation after revisions?

---

## What To Avoid Saying

Avoid these phrases in outreach:

- "Theory of Everything"
- "I derived matter"
- "I derived the Standard Model"
- "I explain consciousness"
- "This proves physics is discrete"

Use instead:

- "finite dynamical observation"
- "mass-ratio coincidences"
- "candidate mechanism"
- "split/inert control"
- "I need help ruling out overfitting"

---

## Decision Rule After Feedback

Post only if at least one technically strong reviewer says:

```text
The claim is not obviously trivial, the search accounting is legible, and a short observation note is reasonable.
```

Do not post if the dominant feedback is:

```text
The targets/search space are too unconstrained, the null model is not relevant, or the split/inert effect is expected/trivial.
```

If feedback is mixed, revise the preprint into an even narrower note containing only:

1. the dynamical system,
2. the split/inert comparison,
3. the lepton `pi/e` and `mu/e` result,
4. the search audit,
5. the one-command reproduction script.

