#!/usr/bin/env python3
"""
Loop-Fallen auf Gaußschen Ganzzahlen Z[i]/(n).

Kernidee: Komplexe Phase entsteht natürlich aus Rundung auf Z[i].
- Multiplikation mit i = 90°-Rotation
- Loop mit komplexen Gewichten → Phase rotiert bei jedem Takt
- Periode der Rotation = Frequenz = E/h
- Spin = Orientierung (cw vs ccw)

Ref: concepts/06-i-als-potenzial-und-schoepfungsakt.md, theory/axioms.md
"""

import random
import math
from typing import List, Tuple, Optional, Dict


class GaussInt:
    """Gaußsche Ganzzahl a + bi, mod n."""

    __slots__ = ('re', 'im', 'n')

    def __init__(self, re: int, im: int, n: int):
        self.re = re % n
        self.im = im % n
        self.n = n

    def __add__(self, other):
        return GaussInt((self.re + other.re) % self.n,
                        (self.im + other.im) % self.n, self.n)

    def __sub__(self, other):
        return GaussInt((self.re - other.re) % self.n,
                        (self.im - other.im) % self.n, self.n)

    def __mul__(self, other):
        if isinstance(other, int):
            return GaussInt((self.re * other) % self.n,
                            (self.im * other) % self.n, self.n)
        # (a+bi)(c+di) = (ac-bd) + (ad+bc)i
        re = (self.re * other.re - self.im * other.im) % self.n
        im = (self.re * other.im + self.im * other.re) % self.n
        return GaussInt(re, im, self.n)

    def __eq__(self, other):
        return self.re == other.re and self.im == other.im and self.n == other.n

    def __hash__(self):
        return hash((self.re, self.im, self.n))

    def __repr__(self):
        if self.im == 0:
            return f"{self.re}"
        if self.re == 0:
            return f"{self.im}i"
        return f"{self.re}+{self.im}i"

    def norm_sq(self) -> int:
        return (self.re * self.re + self.im * self.im) % self.n

    def conj(self):
        return GaussInt(self.re, (-self.im) % self.n, self.n)

    @staticmethod
    def zero(n: int):
        return GaussInt(0, 0, n)

    @staticmethod
    def one(n: int):
        return GaussInt(1, 0, n)

    @staticmethod
    def i_unit(n: int):
        return GaussInt(0, 1, n)

    @staticmethod
    def random(n: int):
        return GaussInt(random.randint(0, n - 1), random.randint(0, n - 1), n)


class GaussianLoopSim:
    """Netzwerk auf Z[i]/(n) mit komplexen Gewichten."""

    def __init__(self, n_nodes: int, modulus: int, topology: str = "ring"):
        self.n_nodes = n_nodes
        self.mod = modulus
        self.state: List[GaussInt] = [GaussInt.zero(modulus) for _ in range(n_nodes)]
        self.weights: List[List[GaussInt]] = []
        self._build_topology(topology)

    def _build_topology(self, topology: str):
        n, m = self.n_nodes, self.mod
        if topology == "ring":
            self.weights = [[GaussInt.zero(m) for _ in range(n)] for _ in range(n)]
            for j in range(n):
                # Nachbar links: Gewicht 1, Nachbar rechts: Gewicht i (Rotation!)
                self.weights[j][(j - 1) % n] = GaussInt.one(m)
                self.weights[j][(j + 1) % n] = GaussInt.i_unit(m)
        elif topology == "ring_symmetric":
            self.weights = [[GaussInt.zero(m) for _ in range(n)] for _ in range(n)]
            for j in range(n):
                self.weights[j][(j - 1) % n] = GaussInt.one(m)
                self.weights[j][(j + 1) % n] = GaussInt.one(m)
        elif topology == "full_random":
            self.weights = [[GaussInt.zero(m) for _ in range(n)] for _ in range(n)]
            for j in range(n):
                neighbors = random.sample(range(n), min(4, n))
                for k in neighbors:
                    if k != j:
                        self.weights[j][k] = GaussInt.random(m)
        elif topology == "grid_2x3" and n == 6:
            # 2x3 Grid: 0-1-2 / 3-4-5
            self.weights = [[GaussInt.zero(m) for _ in range(n)] for _ in range(n)]
            edges = [(0, 1), (1, 2), (0, 3), (1, 4), (2, 5), (3, 4), (4, 5)]
            one, iu = GaussInt.one(m), GaussInt.i_unit(m)
            for a, b in edges:
                self.weights[a][b] = one
                self.weights[b][a] = iu
        elif topology == "star" and n == 6:
            # Center 0, leaves 1..5
            self.weights = [[GaussInt.zero(m) for _ in range(n)] for _ in range(n)]
            one, iu = GaussInt.one(m), GaussInt.i_unit(m)
            for j in range(1, 6):
                self.weights[0][j] = one
                self.weights[j][0] = iu

    def step(self, nonlinear: bool = True):
        new_state = []
        for j in range(self.n_nodes):
            s = GaussInt.zero(self.mod)
            for k in range(self.n_nodes):
                s = s + self.weights[j][k] * self.state[k]
            if nonlinear:
                # z -> z² + coupling (Mandelbrot-artig auf Z[i]/n)
                z = self.state[j]
                sq = z * z
                s = sq + s
            new_state.append(s)
        self.state = new_state

    def state_key(self) -> Tuple:
        return tuple((z.re, z.im) for z in self.state)

    def find_attractor(self, max_steps: int = 5000,
                       init: Optional[List[GaussInt]] = None):
        if init is not None:
            self.state = list(init)
        seen: Dict[Tuple, int] = {}
        traj = []
        for t in range(max_steps):
            key = self.state_key()
            if key in seen:
                period = t - seen[key]
                cycle_start = seen[key]
                attractor = traj[cycle_start:t]
                return attractor, period, cycle_start
            seen[key] = t
            traj.append([z for z in self.state])
            self.step()
        return None, 0, max_steps

    def phase_trajectory(self, node: int, steps: int,
                         init: Optional[List[GaussInt]] = None) -> List[Tuple[int, int]]:
        """Verfolge (re, im) eines Knotens über steps Takte."""
        if init is not None:
            self.state = list(init)
        pts = []
        for _ in range(steps):
            z = self.state[node]
            pts.append((z.re, z.im))
            self.step()
        return pts


def explore_moduli():
    """Systematische Suche: welche Moduln erzeugen reichhaltige Attraktoren?"""
    print("=== Gaußsche Loop-Fallen: Attraktor-Landschaft (nicht-linear) ===\n")
    n_nodes = 5

    results = []
    for mod in [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        attractor_keys = set()
        periods = set()
        for trial in range(50):
            sim = GaussianLoopSim(n_nodes, mod, "ring")
            init = [GaussInt.random(mod) for _ in range(n_nodes)]
            att, period, conv = sim.find_attractor(max_steps=3000, init=init)
            if att is not None and period > 0:
                periods.add(period)
                # Identifiziere Attraktor über erstes Element
                att_key = tuple((z.re, z.im) for z in att[0])
                attractor_keys.add(att_key)
        results.append((mod, len(attractor_keys), sorted(periods)))

    print(f"{'Mod':>4} | {'#Attr':>5} | Perioden")
    print("-" * 70)
    for mod, n_att, periods in results:
        p_str = str(periods[:10]) + ("..." if len(periods) > 10 else "")
        print(f"{mod:>4} | {n_att:>5} | {p_str}")

    best = max(results, key=lambda r: r[1])
    print(f"\nReichhaltigster Modul: {best[0]} mit {best[1]} verschiedenen Attraktoren")
    return best[0]


def phase_analysis(mod: int):
    """Analysiere Phasenrotation in Loops."""
    print(f"\n=== Phasen-Analyse, mod {mod} ===\n")
    n_nodes = 6
    sim = GaussianLoopSim(n_nodes, mod, "ring")
    init = [GaussInt.random(mod) for _ in range(n_nodes)]
    att, period, conv = sim.find_attractor(max_steps=3000, init=init)
    if att is None:
        print("Kein Attraktor gefunden.")
        return

    print(f"Periode: {period}, Konvergenz bei T={conv}")
    print(f"Knoten 0 im Attraktor:")
    for t, state in enumerate(att[:min(period, 20)]):
        z = state[0]
        print(f"  T={t}: {z.re}+{z.im}i")

    # Phasenwinkel-Differenz pro Takt
    if period >= 2:
        angles = []
        for t in range(min(period, 20)):
            z = att[t][0]
            angle = math.atan2(z.im, z.re) if (z.re != 0 or z.im != 0) else 0
            angles.append(angle)
        if len(angles) >= 2:
            diffs = [(angles[t + 1] - angles[t]) % (2 * math.pi) for t in range(len(angles) - 1)]
            mean_diff = sum(diffs) / len(diffs)
            print(f"  Mittlere Phasendrehung pro Takt: {mean_diff:.4f} rad ({math.degrees(mean_diff):.1f}°)")


def confinement_test(mod: int):
    """Teste: Sub-Netzwerke allein instabil, zusammen stabil?"""
    print(f"\n=== Confinement-Test, mod {mod} ===\n")

    alone_periods = []
    for _ in range(20):
        sim = GaussianLoopSim(3, mod, "ring")
        init = [GaussInt.random(mod) for _ in range(3)]
        _, period, _ = sim.find_attractor(max_steps=2000, init=init)
        alone_periods.append(period)

    pair_periods = []
    for _ in range(20):
        sim = GaussianLoopSim(6, mod, "ring")
        init = [GaussInt.random(mod) for _ in range(6)]
        _, period, _ = sim.find_attractor(max_steps=2000, init=init)
        pair_periods.append(period)

    alone_unique = len(set(alone_periods))
    pair_unique = len(set(pair_periods))
    alone_max = max(alone_periods) if alone_periods else 0
    pair_max = max(pair_periods) if pair_periods else 0

    print(f"3 Knoten allein: {alone_unique} versch. Perioden, max={alone_max}")
    print(f"6 Knoten zusammen: {pair_unique} versch. Perioden, max={pair_max}")
    if pair_max > alone_max:
        print("→ Zusammengesetzte Loops zeigen reichhaltigere Attraktorstruktur!")


def spin_test(mod: int):
    """Teste: gibt es cw/ccw-Paare (Spin-Analogon)?"""
    print(f"\n=== Spin-Test (cw/ccw), mod {mod} ===\n")
    n_nodes = 6
    found_pairs = 0
    for trial in range(30):
        sim = GaussianLoopSim(n_nodes, mod, "ring")
        init = [GaussInt.random(mod) for _ in range(n_nodes)]
        att, period, _ = sim.find_attractor(max_steps=2000, init=init)
        if att is None or period == 0:
            continue
        # Konjugierter Startwert → sollte konjugierten Attraktor geben
        conj_init = [GaussInt(z.re, (-z.im) % mod, mod) for z in init]
        sim2 = GaussianLoopSim(n_nodes, mod, "ring")
        att2, period2, _ = sim2.find_attractor(max_steps=2000, init=conj_init)
        if att2 is not None and period2 == period:
            # Prüfe ob att2 das Konjugierte von att ist
            match = True
            for t in range(min(period, 10)):
                for j in range(n_nodes):
                    z1 = att[t][j]
                    z2 = att2[t][j]
                    if z1.re != z2.re or z1.im != (mod - z2.im) % mod:
                        match = False
                        break
                if not match:
                    break
            if match:
                found_pairs += 1
    print(f"Konjugierte Attraktor-Paare (Spin cw/ccw): {found_pairs} von 30 Trials")


def main():
    random.seed(42)
    best_mod = explore_moduli()
    phase_analysis(best_mod)
    confinement_test(best_mod)
    spin_test(best_mod)


if __name__ == "__main__":
    main()
