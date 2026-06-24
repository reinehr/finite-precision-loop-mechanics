# Route C: Two-Sector (Krein) Decomposition

Generated: 2026-06-24 13:05 UTC  ·  rule (1, i), k=6

## Verified structural result (parameter-free, exact)

For each tested split prime, the (1, i) rule decomposes EXACTLY under
phi(a+bi) = (a + r b, a - r b) into two independent real F_p systems with
neighbor weights +r and -r; conjugation swaps them.

| p | r (sqrt -1) | decomposition exact | conjugation = swap | +r / -r sector spectra equal? |
|---|-------------|---------------------|--------------------|-------------------------------|
| 13 | 5 | YES | YES | NO (chiral) |
| 17 | 4 | YES | YES | NO (chiral) |
| 29 | 12 | YES | YES | NO (chiral) |

## Interpretation

- The 'imaginary coupling' (chirality) of the published lepton rule IS, exactly,
  the +r vs -r asymmetry between the two Krein sectors. This ties together the
  chirality decomposition, the indefinite/Krein norm
  (krein_born_summary.md), and the split-prime requirement: only split p has r.
- The two sectors are CHIRAL PARTNERS (weights +r and -r) and have DIFFERENT
  period spectra (verified above: not equal). So the +r/-r chirality is
  dynamically substantive, NOT a mere relabeling -- independent confirmation that
  chirality matters (cf. the kappa=1 vs kappa=0 chirality result).
  A full z-attractor is a pair (u-attractor, v-attractor) with period lcm(P_u, P_v).

## Mixing angle: honest verdict

- A *parameter-free* mixing angle is NOT well defined from this decomposition:
  r is a residue mod p, not a length, so any 'angle' built from r mixes F_p
  residues with real geometry (a category error). The eigenvector equation for
  multiplication-by-i over F_p is degenerate (2r-type relations vanish mod p).
- The only geometrically meaningful angles remain the Gaussian-prime arguments of
  Route B (arg(3+2i) etc.), which the look-elsewhere probe found consistent with
  chance (evidence/mixing_angles_explore_summary.md).
- Therefore the honest mixing route is Route A (Gatto: sin theta_C ~ sqrt(md/ms)).
  Its blocker is concrete and actionable: the model's s/d ratio is its weakest
  quark result. Mixing should be attacked by FIRST fixing s/d (the mod=17, (4+i)
  route improved it toward ~1%), then applying Gatto -- not by geometry of r.

## Status

Route C delivers a clean STRUCTURAL theorem (exact two-sector decomposition =
chirality), but NOT a parameter-free CKM/PMNS angle. The big swing succeeds as
method (rigorous decomposition + a falsifiable, look-elsewhere-controlled test),
and it redirects the mixing program to the Gatto/s-d route.
