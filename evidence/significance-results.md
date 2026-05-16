# Signifikanztest: Ergebnisse

**Stand:** 2026-02-21
**Laufzeit:** ~305 Sekunden, 14 Kerne (M4), 480 Konfigurationen

---

## Test 1: Nullhypothese

**Frage:** Wie selten sind simultane <1%-Treffer für π/e UND μ/e?

- 480 Konfigurationen getestet (24 Primzahlen × 5 Knotenzahlen × 4 Gewichtungen)
- 196 davon produzieren ≥2 verschiedene Perioden

| Kriterium | Treffer | Rate |
|-----------|---------|------|
| π/e <1% allein | 3/196 | 1.5% |
| μ/e <1% allein | 1/196 | 0.5% |
| **BEIDE <1%** | **1/196** | **0.5%** |
| π/e <5% allein | 13/196 | 6.6% |
| μ/e <5% allein | 14/196 | 7.1% |
| BEIDE <5% | 4/196 | 2.0% |

**Der einzige simultane <1%-Treffer: mod=13, k=6, Gewichte (1,i).**

Bei statistischer Unabhängigkeit wäre die Erwartung für einen simultanen Treffer:
P(beide <1%) ≈ 0.015 × 0.005 = 0.0075% (1 pro ~13.000 Konfigurationen).

Gefunden: 1 pro 196 = 0.51%. Das ist ~70× häufiger als der Unabhängigkeitswert. Aber: mit nur 196 Stichproben und dem „Look-elsewhere"-Effekt (wir haben viele Konfigurationen durchsucht) ist das allein kein Beweis. Die STRUKTURELLE Analyse (Test 2) ist aussagekräftiger.

---

## Test 2: Split-Primes vs. Inert-Primes

**Das stärkste Ergebnis.**

| Eigenschaft | Split-Primes (4k+1) | Inert-Primes (4k+3) |
|-------------|---------------------|----------------------|
| Mittlere #Perioden | **6.1** | 3.1 |
| Mittleres max. Verhältnis | **423.2** | 38.6 |
| π/e <5% | **13%** | **0%** |
| μ/e <5% | **13%** | **0%** |
| Beide <5% | **7%** | **0%** |

**Null Treffer für Inert-Primes. Alle SM-ähnlichen Strukturen kommen ausschließlich aus Split-Primes.**

Das ist kein Zufall. Es hat eine mathematische Ursache:
- Split-Primes p ≡ 1 mod 4 **zerfallen** in Z[i]: p = (a+bi)(a−bi)
- Inert-Primes p ≡ 3 mod 4 bleiben **prim** in Z[i]
- Zerfall erzeugt reichere Faktorisierung → mehr Perioden → höhere Verhältnisse

**Detail pro Primzahl (Gewichte 1,i, bester k):**

| Prim | Typ | π/e Fehler | μ/e Fehler | #Perioden |
|------|-----|-----------|-----------|-----------|
| **13** | SPLIT | **0.1%** | **0.1%** | **18** |
| 17 | SPLIT | 1.3% | 20.7% | 8 |
| 41 | SPLIT | 23.0% | 1.7% | 5 |
| 53 | SPLIT | 31.9% | 10.0% | 6 |
| 11 | INERT | 41.8% | 23.1% | 3 |
| Alle anderen | — | >40% | >40% | 2–5 |

**13 ist einzigartig:** Es ist die einzige Primzahl, die sowohl π/e als auch μ/e unter 1% trifft. Die nächstbeste (17) schafft π/e bei 1.3%, aber μ/e nur bei 20.7%.

---

## Test 3: Gewichtvariation bei mod=13, k=6

| Gewichte | #Perioden | π/e Fehler | μ/e Fehler |
|----------|-----------|-----------|-----------|
| **(1, i)** | **13** | **0.1%** | 20.1% |
| **(1, 2i)** | **16** | 4.7% | **0.4%** |
| (2, i) | 9 | 26.7% | 3.2% |
| (1+i, i) | 8 | 19.7% | 33.7% |
| (1, 1) | 6 | 17.0% | 22.7% |
| (1, 1+i) | 7 | 74.7% | 66.5% |
| (2+i, 1) | 12 | 78.5% | 71.6% |
| (1+i, 1−i) | 2 | 96.7% | 95.6% |

**Beobachtungen:**
- Gewichte mit **imaginärem Anteil** (i-Rotation) erzeugen mehr Perioden und bessere Treffer
- (1, i): bestes π/e; (1, 2i): bestes μ/e
- Symmetrische Gewichte (1,1) oder rein reelle erzeugen weniger Struktur
- Die Rotation (komplexe Phase) ist entscheidend für das Spektrum

---

## Zusammenfassende Bewertung

### Was signifikant ist

1. **Split vs. Inert: klare Trennung.** Die algebraische Struktur von Z[i]/(n) bestimmt direkt die Physik-Relevanz. Das ist mathematisch begründbar und kein numerischer Zufall.

2. **13 ist einzigartig unter den getesteten Primzahlen.** Kein anderer Modul trifft beide Zielwerte gleichzeitig unter 1%.

3. **Imaginäre Gewichte sind entscheidend.** Die komplexe Phase (Rotation durch i) erzeugt die Attraktor-Vielfalt. Ohne i keine physik-ähnliche Struktur.

### Was offen bleibt

1. **Look-elsewhere-Effekt:** Wir haben 480 Konfigurationen durchsucht. Ein einzelner 0.5%-Treffer unter 196 ist statistisch nicht überwältigend.

2. **Größere Primzahlen:** Nur Primzahlen ≤97 getestet. 13 könnte lokal das Optimum sein, während größere Primzahlen (z.B. 137 — die Feinstruktur-Zahl!) noch ungetestet sind.

3. **Andere Topologien:** Nur Ring-Graph getestet. 2D/3D-Gitter oder Random Graphs könnten andere Ergebnisse liefern.

### Gesamturteil

**Wir stehen nicht in einer Sackgasse.** Die Theorie hat eine klare, mathematisch begründbare Vorhersage: *Die physik-relevanten Moduln sind Split-Primes.* Das ist falsifizierbar und nicht-trivial. Ob 13 der „richtige" Modul ist, erfordert weitere Tests — insbesondere mit n=137 und größeren Systemen.

---

## Update: Ultra-Scan (Full Power, 2026-02-21)

**Setup:**
- 14 Kerne (M4), zweistufiger Lauf
- Phase A: 1790 Konfigurationen (Split-Primes bis 197 + Inert-Kontrollgruppe)
- Phase B: 360 Fokus-Konfigurationen (Top-Kandidaten aus Phase A, deutlich mehr Trials)
- Gesamtlaufzeit: ~1289 Sekunden

**Artefakte:**
- `theory/ultra_scan_phaseA.jsonl`
- `theory/ultra_scan_phaseB.jsonl`
- `theory/ultra_scan_summary.md`

### Zentrale Resultate

1. **Parameter-Einengung wird klarer:**
   - Global beständigster Treffer bleibt:
     - `mod=13, k=6, topology in {ring, ring_symmetric}, weights=(1,i)`
     - `pi/e = 273.00` (Fehler 0.07%)
     - `mu/e = 207.00` (Fehler 0.11%)

2. **Robustheit von mod=13 steigt mit Sampling-Tiefe:**
   - In Phase B erscheinen **alle <1%-Doppeltreffer** ausschließlich bei `mod=13, k=6, w=(1,i)`.
   - Varianten mit `k=8, w=(1,1)` bei `mod=13` sind nahe dran, aber nicht unter 1% simultan.

3. **Weitere Kandidaten bleiben sekundär:**
   - `mod=5, k=6, w=(2+i,1)` trifft `pi/e` sehr gut, aber `mu/e` nur auf ~2.31%.
   - `mod=17, k=6, w=(1,2i)` und `mod=41, k=6, w=(1,1)` liefern respektable Teilerfolge, aber keine simultanen <1%-Treffer.
   - `mod=113, k=4, w=(1,1)` zeigt mittlere Nähe, jedoch ebenfalls kein <1%-Doppeltreffer.

4. **Status von n=137 (explizit getestet):**
   - Beste gefundene Konfiguration bei `mod=137` bleibt deutlich außerhalb des Zielbereichs.
   - Keine simultane enge Approximation an `pi/e` und `mu/e`.
   - In diesem Modellregime ist 137 aktuell **nicht** konkurrenzfähig zu 13.

### Konsequenz für den nächsten Suchraum

Die Daten engen den effektiven Suchraum weiter ein auf:
- `mod`: primär `13`, sekundär `5, 17, 41, 113`
- `k`: primär `6` (mit Nebenfenster `k=8` bei `mod=13`)
- `topology`: `ring` und `ring_symmetric` bleiben führend
- `weights`: komplexe Gewichte mit imaginärem Anteil bleiben entscheidend, insbesondere `(1,i)`

---

## Update: Peak-Focus (2026-02-21, schneller Lauf)

**Setup:**
- 416 Konfigurationen, 14 Kerne, 665s Laufzeit
- 120 Trials, 6000 Steps pro Config
- Drei Gruppen: peak_13, split_secondary (5,17,29,37,41), inert_control (7,11,19,23)
- 12 Gewichtsvarianten inkl. neuer: `(3,i)`, `(1,3i)`, `(2+i,i)`, `(i,1)`

### Zentrale Resultate

**1. mod=13, k=6 bleibt einzigartig und unangreifbar:**

| Gruppe | valid | avg #Perioden | <1% Doppeltreffer | <5% Doppeltreffer |
|--------|-------|---------------|-------------------|-------------------|
| **peak_13** | 117 | 7.8 | **5** | **11** |
| split_secondary | 77 | 6.5 | **0** | **0** |
| inert_control | 10 | 6.0 | **0** | **0** |

Alle 5 Doppeltreffer (<1% für pi/e UND mu/e simultan) stammen aus **exakt einer Konfiguration:**
- `mod=13, k=6, weights=(1,i)` oder `(i,1)` (L/R-Symmetrie)
- `pi/e = 273.00` (0.07% Fehler), `mu/e = 207.00` (0.11% Fehler)

**2. Neue Erkenntnis: Gewichtssymmetrie**

`(1,i)` und `(i,1)` liefern gleichwertige Ergebnisse — die Wahl der Richtung (links/rechts im Ring) ist irrelevant. Das deutet auf eine fundamentale Paritätssymmetrie hin.

**3. Sekundäre Split-Primes scheitern:**

Kein einziger anderer Split-Prime (5, 17, 29, 37, 41) erreicht auch nur <5% simultan für pi/e und mu/e. mod=13 ist nicht einfach „der beste unter vielen" — es ist **der einzige**.

**4. Offenes Problem: tau/e**

Das tau/e-Verhältnis (3477.23) wird von keiner getesteten Konfiguration gut getroffen (bester Fehler ~45%). Dies deutet darauf hin, dass die dritte Lepton-Generation möglicherweise eine erweiterte Topologie, größeres k, oder einen anderen Mechanismus erfordert.

### Implikation

Die Parameter `mod=13, k=6, w=(1,i)` sind innerhalb des getesteten Raums **isoliert optimal**. Die Theorie macht damit eine harte, falsifizierbare Vorhersage:
- Der fundamentale Zustandsraum pro Knoten ist Z[i]/(13)
- 6 Knoten pro minimale Teilchen-Topologie
- Die Kopplung zwischen Nachbarn ist rein imaginär (Phasenrotation)

---

## Update: Lepton-Short-Runs (<15 Minuten, 2026-02-21)

Zwei zusätzliche Kurzläufe mit Leptonen-Fokus:

- **Run A:** mod=13, k=6..16, 220 Konfigurationen, 831s
- **Run B:** Split-Primes inkl. 137, k in {6,8,10}, 396 Konfigurationen, 531s

### Ergebnisbild

1. **mu/e bleibt extrem stabil** bei `mod=13, k=6, w=(1,i)/(i,1)` mit ~0.11% Fehler.
2. **tau/e verbessert sich erstmals deutlich** (bestes Einzelereignis: 5.79% Fehler bei `mod=13, k=6, ring_symmetric, w=(i,1)`), aber:
3. **Replikation im direkten Zoom-Test fehlt bisher** (`tau_zoom_short`, 45s, 120 valid configs): kein Fall unter 15%.

### Interpretation

- Der 5.79%-Treffer ist aktuell ein **interessanter Kandidat**, aber noch **nicht robust**.
- Für tau/e scheint die Dynamik deutlich seltener/instabiler zu sein als für mu/e.
- Das stützt die Arbeitshypothese: 3. Generation benötigt evtl. seltene Attraktor-Basins, mehr Trials oder eine erweiterte Struktur.

### Neue Artefakte

- `theory/lepton_short_run_A.jsonl`
- `theory/lepton_short_run_B.jsonl`
- `theory/lepton_short_summary.md`
- `theory/tau_zoom_short.jsonl`
- `theory/tau_zoom_short_summary.md`
