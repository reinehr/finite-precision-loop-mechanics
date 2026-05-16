# Reproduzierbarkeit: Preprint-Zahlen

**Stand:** 2026-02-26  
**Ziel:** Jede Zahl im Preprint (`latex/preprint.tex`) auf Skript + Summary-Datei zurückführen.

---

## Voraussetzung

- Python 3.x (Standardbibliothek reicht für den schnellen Kernbefehl)
- Ausführung aus `scripts/` (wegen gegenseitiger Imports)

```bash
cd scripts
```

---

## Schnellster Publikationskern

Die eng gefassten Publikationstabellen werden mit einem Befehl aus dem Repository-Root erzeugt:

```bash
python3 scripts/reproduce_publication_core.py
```

Output:

```text
evidence/publication_core_tables.md
```

Optionaler schwerer Pfad mit vorgelagerter Neuberechnung ausgewählter Kernskripte:

```bash
python3 scripts/reproduce_publication_core.py --recompute
```

Dieser Pfad ruft `significance_test.py`, `quark_masses.py --mod 13` und `entropy_degree_scan.py` auf und kann mehrere Minuten dauern. Für eine vollständige Preprint-Reproduktion bleiben die unten aufgeführten Spezialskripte relevant.

---

## §2 Setup

| Behauptung | Quelle | Hinweis |
|------------|--------|---------|
| Update-Regel z→z² + Kopplung | `gaussian_loop.py` | Kernlogik |
| Split/Inert Algebra | `theory/split_inert_theorem.md` | Theoretisch |

---

## §3 Lepton results

| Tabelle / Zahl | Skript | Output | Laufzeit |
|----------------|--------|--------|----------|
| π/e 273.00 (0.07%), μ/e 207.00 (0.11%), τ/e 3475.3 compound (0.06%) | `composite_k_repro.py` | `theory/composite_k_repro_summary.md` | ~30 min |
| τ/e als Produkt μ/e × τ/μ | `theory/tau-third-generation-ideen.md` | Konzept |
| Koide Q ≈ 2/3 (0.02%) | `theory/koide_connection.md` | Berechnung |

**Schneller Check (Lepton-Kern):**
```bash
python significance_test.py   # Split/Inert, π/e+μ/e Doppeltreffer
```

---

## §4 Quark results

| Tabelle / Zahl | Skript | Output | Laufzeit |
|----------------|--------|--------|----------|
| d/u 15/7, c/s 41/3, t/b 41.0, b/c 23/7 | `quark_masses.py --mod 13` | `theory/quark_masses_summary_mod13.md` | ~1 min |
| s/d 1.01% (mod=17) | `quark_masses.py --mod 17` | `theory/quark_masses_summary_mod17.md` | ~25 s |
| Gaussian Faktorisierung (3+2i)/(3-2i) | `theory/quark_masses_summary*.md` | Konfiguration coup=(3+2i)/(3-2i) |

```bash
python quark_masses.py --mod 13
python quark_masses.py --mod 17
```

---

## §5 Split/Inert theorem

| Tabelle / Zahl | Skript | Output | Laufzeit |
|----------------|--------|--------|----------|
| Mean # periods 6.1 vs 3.1, 0% vs 13% π/e | `significance_test.py` | `theory/significance-results.md` | ~5 min |
| p < 0.0001 Look-Elsewhere (Quarks) | `theory/quark_du_stats_summary.md` | Monte Carlo 10000 |

```bash
python significance_test.py
```

---

## §6 Statistical validation

| Behauptung | Skript / Datei | Output |
|------------|----------------|--------|
| 10 direct, 4 sub-0.1%, p(same-type) < 0.001 c-quark | `significance_v2.py` | `theory/significance_v2_summary.md` |
| Nullmodell 2000 Samples, type-conditional | `theory/direct_sector_statistics.md` | Kernaussagen |
| p(all 16 best) < 0.0005 | `theory/significance_v2_summary.md` | Global bound |
| Basin stability +0.65 (Spearman) | `theory/basin_stability_summary.md` | Korrelation |
| Selection scoring v0.4b, S = A·L·F·C·G_full | `selection_score_v04b.py` | `theory/selection_mechanism_score_v04b.md` |
| 3 Repeats, 126 Kataloge, 16 Targets <5% | `composite_k_repro.py` | `theory/composite_k_repro_summary.md` |
| Ratio/compound BH-evidenz | `theory/ratio_compound_theoretical_embedding.md`, `theory/compound_sector_statistics.md` | Theoretische Einbettung |

```bash
python significance_v2.py          # Nullmodell, p-Werte
python composite_k_repro.py         # 3 Repeats (laufzeitintensiv)
python selection_score_v04b.py     # ~41 min
```

---

## §7 Entropy selection (Why d=2?)

| Tabelle | Skript | Output | Laufzeit |
|---------|--------|--------|----------|
| d=2: 33 Perioden, 3.72 Entropie, π/e+μ/e <0.15% | `entropy_degree_scan.py` | `theory/entropy_degree_summary.md` | ~4 min |

```bash
python entropy_degree_scan.py
```

---

## Preprint-Kernzahlen: minimale Reproduktion

Für einen schnellen Nachvollzug der zentralen Ergebnisse (ohne composite_k_repro und selection_v04b):

| # | Befehl | Zweck |
|---|--------|-------|
| 1 | `python significance_test.py` | Split vs. Inert, Lepton-Doppeltreffer |
| 2 | `python quark_masses.py --mod 13` | Quark-Kern (d/u, c/s, t/b, b/c) |
| 3 | `python quark_masses.py --mod 17` | s/d 1.01% |
| 4 | `python entropy_degree_scan.py` | d=2 Entropie-Optimalität |
| 5 | `python significance_v2.py` | Nullmodell, p-Werte |

**Gesamtlaufzeit:** ~15 min

---

## Vollständige Reproduktion (Preprint-Freeze)

Zusätzlich zu oben:

| Skript | Output | Laufzeit |
|--------|--------|----------|
| `composite_k_repro.py` | 3 Repeats, 16 Targets, direct/ratio/compound | ~30 min |
| `selection_score_v04b.py` | S4b-Tabelle, G_full | ~41 min |
| `compound_sector_statistics.py` | ratio/compound BH | abhängig von significance_v2 |

---

## Appendix A: P_min = 2

| Behauptung / Tabelle | Skript | Output | Laufzeit |
|----------------------|--------|--------|----------|
| Vermutung 4.1 (a,b,c), Basin P=1/P=2 | `p_min_check.py` | `theory/p_min_empirical_summary.md` | ~90 s |

```bash
python p_min_check.py
```

---

## Datei↔Preprint Mapping

| Preprint § | Theorie-Datei(en) |
|------------|-------------------|
| Abstract | `composite_k_repro_summary.md`, `direct_sector_statistics.md` |
| §3 Leptonen | `composite_k_repro_summary.md`, `spectrum_core_table.md` |
| §4 Quarks | `quark_masses_summary_mod13.md`, `quark_masses_summary_mod17.md` |
| §5 Split/Inert | `split_inert_theorem.md`, `significance-results.md` |
| §6 Statistik | `significance_v2_summary.md`, `direct_sector_statistics.md`, `selection_mechanism_score_v04b.md`, `ratio_compound_theoretical_embedding.md` |
| §7 Entropie | `entropy_degree_summary.md` |
| **Appendix A** P_min | `p_min_two_argument.md`, `p_min_empirical_summary.md` |
