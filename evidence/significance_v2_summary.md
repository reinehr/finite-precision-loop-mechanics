# Significance v2 (Final)

**Stand:** 2026-02-25  
**Nullmodell-Samples:** 2000  
**Matching:** direct + ratio + compound (compound_limit=40)  
**Toleranz:** 5.0%

## Test-Accounting

- Kataloge pro Nullsample: 126 (aus Repro: 3 Repeats x 42 Konfigurationen)
- Targets: 16
- Nullkataloge behalten `#periods` und `max_period` pro Konfiguration bei; Periodenwerte werden zufällig gezogen.

## Per-Target p-Werte

| Target | Obs Type | p(robust>=2/3) | Bonf | BH | p(best<=obs) any-type | Bonf | BH | p(best<=obs) same-type | Bonf | BH |
|--------|----------|----------------|------|----|------------------------|------|----|-------------------------|------|----|
| c-quark | direct | 1.000000 | 1.000000 | 1.000000 | 0.001000 | 0.016000 | 0.016000 | 0.000000 | 0.000000 | 0.000000 |
| Lambda | direct | 1.000000 | 1.000000 | 1.000000 | 0.113500 | 1.000000 | 0.908000 | 0.112000 | 1.000000 | 0.224000 |
| pi+- | direct | 0.958500 | 1.000000 | 1.000000 | 0.183000 | 1.000000 | 0.942000 | 0.155000 | 1.000000 | 0.275556 |
| Omega- | direct | 1.000000 | 1.000000 | 1.000000 | 0.495000 | 1.000000 | 0.998000 | 0.493500 | 1.000000 | 0.789600 |
| mu | ratio | 0.947000 | 1.000000 | 1.000000 | 0.235500 | 1.000000 | 0.942000 | 0.041000 | 0.656000 | 0.093714 |
| tau | compound | 1.000000 | 1.000000 | 1.000000 | 0.676000 | 1.000000 | 0.998000 | 0.000500 | 0.008000 | 0.004000 |
| K+- (kaon) | compound | 1.000000 | 1.000000 | 1.000000 | 0.837500 | 1.000000 | 0.998000 | 0.005500 | 0.088000 | 0.022000 |
| Sigma+ | direct | 1.000000 | 1.000000 | 1.000000 | 0.950500 | 1.000000 | 0.998000 | 0.948500 | 1.000000 | 0.997500 |
| p (proton) | direct | 1.000000 | 1.000000 | 1.000000 | 0.955500 | 1.000000 | 0.998000 | 0.953500 | 1.000000 | 0.997500 |
| Xi- | ratio | 1.000000 | 1.000000 | 1.000000 | 0.983000 | 1.000000 | 0.998000 | 0.002000 | 0.032000 | 0.010667 |
| eta'(958) | direct | 1.000000 | 1.000000 | 1.000000 | 0.972500 | 1.000000 | 0.998000 | 0.969500 | 1.000000 | 0.997500 |
| n (neutron) | direct | 1.000000 | 1.000000 | 1.000000 | 0.980000 | 1.000000 | 0.998000 | 0.979000 | 1.000000 | 0.997500 |
| omega(782) | direct | 1.000000 | 1.000000 | 1.000000 | 0.988500 | 1.000000 | 0.998000 | 0.986500 | 1.000000 | 0.997500 |
| K0 | compound | 1.000000 | 1.000000 | 1.000000 | 0.983000 | 1.000000 | 0.998000 | 0.010500 | 0.168000 | 0.029333 |
| rho(770) | compound | 1.000000 | 1.000000 | 1.000000 | 0.998000 | 1.000000 | 0.998000 | 0.011000 | 0.176000 | 0.029333 |
| eta | direct | 1.000000 | 1.000000 | 1.000000 | 0.998000 | 1.000000 | 0.998000 | 0.997500 | 1.000000 | 0.997500 |

## Global p-Werte

- p(all 16 robust>=2/3): 0.908500
- p(all 16 with best_err <= observed best): 0.000000
- Upper bound for p(all16 best) with 2000 samples: < 0.000500

## Interpretation

- `direct`-dominierte Targets sind erwartungsgemäß am robustesten.
- `ratio/compound` erhöhen den Suchraum stark; daher sind same-type p-Werte relevanter als any-type p-Werte.
- Entscheidend für Veröffentlichungsargument: globales Nullmodell-Ergebnis für das 16/16-Repro-Kriterium.
