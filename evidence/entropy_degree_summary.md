# Entropie-Scan: Polynomgrad und Attraktor-Reichhaltigkeit

**Stand:** 2026-02-22
**Frage:** Ist d=2 (z -> z^2) optimal fuer die Attraktorlandschaft?

## Setup

- Z[i]/(13), k=6, ring, w=(1,i)
- 3000 Samples pro Grad
- Grade d = [1, 2, 3, 4, 5]

## Ergebnisse

| Grad d | Konvergiert | Versch. Perioden | Max Periode | Shannon-Entropie | SM-Treffer pi/e | SM-Treffer mu/e |
|--------|-------------|------------------|-------------|------------------|-----------------|-----------------|
| **d=1** | 3000/3000 | 1 | 12 | 0.00 | --- | --- |
| **d=2** | 2764/3000 | 33 | 3780 | 3.72 | 0.07% | 0.11% |
| **d=3** | 1918/3000 | 27 | 5112 | 3.17 | 1.03% | 3.01% |
| **d=4** | 568/3000 | 18 | 3276 | 2.47 | 11.28% | 2.31% |
| **d=5** | 2943/3000 | 13 | 5460 | 2.02 | 0.07% | 10.03% |

## Interpretation

**d=2 hat die hoechste Shannon-Entropie** unter allen getesteten Graden.
Das stuetzt das Argument: z -> z^2 maximiert die Attraktor-Vielfalt
bei minimalem Polynomgrad.

## Perioden-Spektren (Top-10 pro Grad)

### d=1

| Periode | Count |
|---------|-------|
| 12 | 3000 |

### d=2

| Periode | Count |
|---------|-------|
| 828 | 565 |
| 2 | 313 |
| 2484 | 294 |
| 36 | 276 |
| 10 | 225 |
| 54 | 210 |
| 108 | 153 |
| 270 | 148 |
| 2730 | 130 |
| 3276 | 102 |

### d=3

| Periode | Count |
|---------|-------|
| 1704 | 584 |
| 30 | 252 |
| 960 | 212 |
| 12 | 197 |
| 4572 | 189 |
| 192 | 184 |
| 1380 | 74 |
| 276 | 67 |
| 60 | 42 |
| 828 | 30 |

### d=4

| Periode | Count |
|---------|-------|
| 1692 | 205 |
| 1818 | 189 |
| 1602 | 49 |
| 564 | 45 |
| 9 | 29 |
| 2736 | 13 |
| 18 | 8 |
| 606 | 8 |
| 522 | 6 |
| 534 | 4 |

### d=5

| Periode | Count |
|---------|-------|
| 1092 | 1415 |
| 12 | 712 |
| 4 | 510 |
| 24 | 111 |
| 5460 | 71 |
| 20 | 48 |
| 120 | 47 |
| 576 | 20 |
| 2184 | 3 |
| 60 | 2 |

---
Laufzeit: 228.2s

