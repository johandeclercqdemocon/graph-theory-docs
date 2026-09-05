# Hoofdstuk 29 — Spectrale grafentheorie

Hoofdstuk 4 merkte op dat `A^k` wandelingen telt en liet de matrix daar liggen. Dit hoofdstuk neemt de
matrix serieus: de adjacentiematrix van een graaf is reëel en symmetrisch, dus ze heeft `n` reële
eigenwaarden, en die getallen coderen een verrassende hoeveelheid structuur.

## Veertig regels eigenwaarde-oplosser

Dit boek heeft geen dependencies, dus het heeft zijn eigen oplosser nodig. Voor reële symmetrische
matrices is de **Jacobi-rotatiemethode** kort, onvoorwaardelijk convergent, en leesbaar.

Het idee: zoek de grootste plaats buiten de diagonaal en roteer in dat vlak om haar op nul te zetten.
Elke rotatie verkleint de som van de kwadraten van de niet-diagonale plaatsen, dus de matrix convergeert
naar een diagonale matrix, waarvan de plaatsen de eigenwaarden zijn.

```python
for _ in range(max_sweeps):
    off, p, q = 0.0, 0, 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(a[i][j]) > off:
                off, p, q = abs(a[i][j]), i, j
    if off < tolerance:
        break
    theta = (math.pi / 4 if a[p][p] == a[q][q]
             else 0.5 * math.atan2(2 * a[p][q], a[p][p] - a[q][q]))
    c, s = math.cos(theta), math.sin(theta)
    # rotate rows p, q and then columns p, q
```

Trager dan wat een bibliotheek gebruikt — `O(n³)` per veegbeurt — en het is degene die je kunt lezen.
Ze is bovendien alleen geldig voor symmetrische invoer; er iets anders in stoppen levert onzin op in
plaats van een fout, en de moduledocumentatie zegt dat expliciet.

Een eigenwaarde-oplosser verifiëren vergt zorg: haar vergelijken met een andere oplosser die je ook zelf
schreef bewijst niets. De verificatie gebruikt in plaats daarvan **spooridentiteiten**, die feiten over
de graaf zijn en niet over de lineaire algebra:

- `Σ λᵢ = spoor(A) = 0`, want de diagonaal is helemaal nul;
- `Σ λᵢ² = spoor(A²) = 2m`, want `(A²)_{vv}` is het aantal gesloten wandelingen van lengte 2, en dat is
  `deg(v)`;
- `Σ λᵢ³ = spoor(A³) = 6 · (aantal driehoeken)`, want een gesloten wandeling van lengte 3 is een
  driehoek doorlopen vanaf een van 3 startpunten in een van 2 richtingen.

```
  held      ch29  The adjacency spectrum sums to 0 and its squares sum to 2m  (52 graphs)
  held      ch29  The cube of the spectrum sums to six times the triangle count  (52 graphs)
```

De derde identiteit is de goede: het aantal driehoeken rechts wordt door directe opsomming berekend, dus
een spectrum dat eraan voldoet wordt tegen combinatoriek gecontroleerd en niet tegen nog meer lineaire
algebra.

## Wat het spectrum weet

```
K4        spectrum [-1.0, -1.0, -1.0, 3.0]
C4        spectrum [-2.0, -0.0, 0.0, 2.0]
C5        spectrum [-1.618, -1.618, 0.618, 0.618, 2.0]
petersen  spectrum [-2.0, -2.0, -2.0, -2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 3.0]
K33       spectrum [-3.0, -0.0, 0.0, 0.0, 0.0, 3.0]
```

Lees de Petersen-rij: `3` één keer, `1` vijf keer, `−2` vier keer. Een graaf op 10 knopen met slechts
drie verschillende eigenwaarden, wat uiterst ongewoon is en een van de redenen is dat deze graaf
bijzonder is — grafen met drie verschillende adjacentie-eigenwaarden zijn **sterk regulier**, en de
Petersen-graaf is de kleinste interessante.

Verschillende structurele feiten lees je rechtstreeks van het spectrum af:

- **`λ_max` ligt tussen de gemiddelde en de maximale graad**: `2m/n ≤ λ_max ≤ Δ`. Voor een
  `d`-reguliere graaf vallen beide grenzen samen, dus `λ_max = d` precies, met de al-enen-eigenvector.
- **De graaf is bipartiet dan en slechts dan als het spectrum symmetrisch is om 0.** `C₄` geeft
  `{−2, 0, 0, 2}` en `K₃,₃` geeft `{−3, 0, 0, 0, 0, 3}`; `C₅` geeft een asymmetrisch spectrum en is
  niet bipartiet.
- **Het aantal samenhangscomponenten** is de multipliciteit van `λ_max` voor een reguliere graaf.

```
  held      ch29  A d-regular graph has spectral radius exactly d  (12 graphs)
  held      ch29  The spectral radius lies between the average and maximum degree  (52 graphs)
```

## Wat het spectrum niet weet

Het spectrum is een invariant, dus het kan bewijzen dat twee grafen niet isomorf zijn. Zoals elke
invariant in hoofdstuk 5 kan het niet bewijzen dat ze het wel zijn.

Twee grafen met hetzelfde spectrum heten **cospectraal**. Het kleinste cospectrale paar is `K₁,₄` en
`C₄ + K₁` — een ster en een vierhoek-plus-losse-knoop, beide met spectrum `{−2, 0, 0, 0, 2}`. Ze zijn
duidelijk niet isomorf; de ene is samenhangend.

Erger nog, dit is niet zeldzaam. **Vrijwel alle bomen zijn cospectraal met een andere boom**, dus voor
bomen is het spectrum als onderscheidingsmiddel bijna nutteloos. De precieze fractie van alle grafen die
door hun spectrum bepaald wordt is een open probleem, en de numerieke aanwijzingen suggereren dat ze
dicht bij 1 ligt voor algemene grafen — wat bomen tot een ongewoon slecht geval maakt.

Dit is hetzelfde verhaal als kleurverfijning in hoofdstuk 5: een goedkope invariant, correct in één
richting, en blind voor een familie gevallen die je kunt karakteriseren.

## Verstrengeling

Het diepste elementaire instrument hier is **eigenwaardeverstrengeling**.

> **Stelling (verstrengeling van Cauchy).** Is `H` een geïnduceerde deelgraaf van `G` op `n − 1` knopen,
> met eigenwaarden `μ₁ ≤ … ≤ μ_{n−1}` en heeft `G` `λ₁ ≤ … ≤ λ_n`, dan geldt
>
> `λ₁ ≤ μ₁ ≤ λ₂ ≤ μ₂ ≤ … ≤ μ_{n−1} ≤ λ_n`.

Een knoop verwijderen kan de eigenwaarden niet langs elkaar heen laten schuiven. Dit levert grenzen die
combinatorisch moeilijk te krijgen zijn — bijvoorbeeld de **verhoudingsgrens**, dat een onafhankelijke
verzameling in een `d`-reguliere graaf grootte hoogstens `n · (−λ_min)/(d − λ_min)` heeft. Voor de
Petersen-graaf: `10 · 2/(3 + 2) = 4`, en dat is precies `α(Petersen) = 4` zoals hoofdstuk 21 berekende.

Een scherpe grens op een `NP`-moeilijke grootheid, uit vier eigenwaarden, is een eerlijke aanbeveling
voor de methode.

## Probeer het

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import complete, cycle, petersen, complete_bipartite, Graph
from graphs.spectral import adjacency_spectrum

for name, g in [('C4', cycle(4)), ('C5', cycle(5)), ('K3,3', complete_bipartite(3,3)),
                ('petersen', petersen())]:
    sp = [round(x, 3) for x in adjacency_spectrum(g)]
    symmetric = all(abs(sp[i] + sp[-1-i]) < 1e-6 for i in range(len(sp)))
    print(f'{name:<9} {sp}')
    print(f'{\"\":<9} symmetric about 0: {symmetric}  (bipartite iff this)')

print()
star = Graph(5, [(0,1),(0,2),(0,3),(0,4)])
other = Graph(5, [(0,1),(1,2),(2,3),(3,0)])
print('cospectral pair:')
print('  K_1,4        ', [round(x,3) for x in adjacency_spectrum(star)])
print('  C_4 + K_1    ', [round(x,3) for x in adjacency_spectrum(other)])
"
```

```
C4        [-2.0, -0.0, 0.0, 2.0]
          symmetric about 0: True  (bipartite iff this)
C5        [-1.618, -1.618, 0.618, 0.618, 2.0]
          symmetric about 0: False  (bipartite iff this)
K3,3      [-3.0, -0.0, 0.0, 0.0, 0.0, 3.0]
          symmetric about 0: True  (bipartite iff this)
petersen  [-2.0, -2.0, -2.0, -2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 3.0]
          symmetric about 0: False  (bipartite iff this)

cospectral pair:
  K_1,4         [-2.0, -0.0, 0.0, 0.0, 2.0]
  C_4 + K_1     [-2.0, -0.0, 0.0, 0.0, 2.0]
```

Identieke spectra; de ene graaf is samenhangend en de andere niet. Het spectrum weet heel veel en niet
alles.

## Oefeningen

1. Bereken het adjacentiespectrum van `K_n` met de hand. (Hint: `A = J − I`.)
2. Toon aan dat `Σ λᵢ² = 2m` volgt uit het tellen van gesloten wandelingen van lengte 2.
3. Verifieer de verhoudingsgrens op de Petersen-graaf en vergelijk met `α = 4`.
4. Waarom kan het spectrum bewijzen dat twee grafen niet isomorf zijn maar nooit dat ze het wel zijn?

Oplossingen in Bijlage E.

## Kernpunten

- De adjacentiematrix van een graaf is reëel symmetrisch, dus het spectrum is reëel. Veertig regels
  Jacobi-rotatie berekenen het zonder dependencies.
- Verifieer een eigenwaarde-oplosser tegen spooridentiteiten — `Σλ = 0`, `Σλ² = 2m`,
  `Σλ³ = 6·driehoeken` — en niet tegen een andere oplosser.
- `λ_max` ligt tussen de gemiddelde en de maximale graad, met gelijkheid voor reguliere grafen.
  Bipartiet precies wanneer het spectrum symmetrisch om 0 is.
- Cospectrale niet-isomorfe grafen bestaan en zijn gewoon onder bomen. Het spectrum is een eenzijdige
  invariant, zoals alles in hoofdstuk 5.
- Verstrengeling geeft grenzen op combinatorische grootheden uit eigenwaarden; de verhoudingsgrens is op
  de Petersen-graaf precies scherp.
