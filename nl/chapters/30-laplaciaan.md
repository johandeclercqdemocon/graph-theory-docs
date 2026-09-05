# Hoofdstuk 30 — De Laplaciaan

De adjacentiematrix is de voor de hand liggende matrix om aan een graaf te hangen. De **Laplaciaan**
`L = D − A`, met `D` de diagonale graadmatrix, is de bruikbare — en dit hoofdstuk gaat over waarom die
wissel alles verandert.

## De kwadratische vorm

De reden dat `L` beter is, is één identiteit:

> **Lemma.** Voor elke vector `x` geldt `xᵀLx = Σ_{uv ∈ E} (x_u − x_v)²`.

*Bewijs.* Uitwerken: `xᵀDx = Σ_v deg(v)x_v²` en `xᵀAx = 2Σ_{uv} x_u x_v`. Aftrekken geeft
`xᵀLx = Σ_v deg(v)x_v² − 2Σ_{uv} x_u x_v = Σ_{uv} (x_u² + x_v² − 2x_u x_v)`, want elke knoop komt in
`deg(v)` kanttermen voor. ∎

Alles volgt hieruit. `xᵀLx ≥ 0` altijd, dus `L` is positief semidefiniet en alle eigenwaarden zijn
`≥ 0`. De vorm is nul precies wanneer `x` constant is op elke samenhangscomponent. Dus:

> **Stelling.** De multipliciteit van eigenwaarde 0 in `L` is gelijk aan het aantal
> samenhangscomponenten.

```
K4        L-spectrum [0.0, 4.0, 4.0, 4.0]
C5        L-spectrum [0.0, 1.382, 1.382, 3.618, 3.618]
petersen  L-spectrum [0.0, 2.0, 2.0, 2.0, 2.0, 2.0, 5.0, 5.0, 5.0, 5.0]
P4        L-spectrum [0.0, 0.5858, 2.0, 3.4142]
two triangles  L-spectrum [0.0, 0.0, 3.0, 3.0, 3.0, 3.0]
```

De laatste rij heeft twee keer 0, en de graaf heeft twee componenten. Samenhang — een combinatorische
eigenschap — wordt van een eigenwaardemultipliciteit afgelezen.

```
  held      ch30  The multiplicity of Laplacian eigenvalue 0 is the number of components  (52 graphs)
```

## De matrix-boomstelling

Hoofdstuk 7 beloofde dit en kon het niet waarmaken.

> **Stelling (Kirchhoff, 1847).** Het aantal opspannende bomen van `G` is gelijk aan elke cofactor van
> `L` — schrap een willekeurige rij en de bijbehorende kolom, en neem de determinant.

```python
def spanning_tree_count(g):
    lap = laplacian_matrix(g)
    minor = [row[1:] for row in lap[1:]]
    return round(determinant(minor))
```

`O(n³)`, tegen de opsomming van `C(m, n−1)` uit hoofdstuk 7. De verificatie controleert de een tegen de
ander, en dat is een determinant tegen een uitputtende zoektocht — zo onafhankelijk als twee berekeningen
maar kunnen zijn:

```
  held      ch30  Matrix-tree: a Laplacian cofactor counts spanning trees  (52 graphs)
```

En de belofte is nu ingelost. Hoofdstuk 7 kon de formule van Cayley alleen tot `K₆` verifiëren:

```
  K10 spanning trees: 100000000    10^8 = 100000000
```

`K₁₀` heeft `10⁸` opspannende bomen, ogenblikkelijk bevestigd uit een 9×9-determinant. De Petersen-graaf
heeft er 2000.

## Algebraïsche samenhang

De op één na kleinste eigenwaarde `λ₂` is de **algebraïsche samenhang**, of Fiedler-waarde. Ze is nul
precies wanneer de graaf onsamenhangend is, en groter naarmate de graaf moeilijker te splitsen is.

```
  held      ch30  Algebraic connectivity is positive exactly when the graph is connected  (51 graphs)
```

Vergelijk `P₄` bij `0,586` met `K₄` bij `4,0`. Beide zijn samenhangend; de ene is een pad dat één
verwijderde kant breekt, de andere is zo robuust samenhangend als vier knopen toelaten. De
Fiedler-waarde meet dat verschil op een continue schaal, waar `κ(G)` en `λ(G)` uit hoofdstuk 12 gehele
getallen geven.

## De ongelijkheid van Cheeger

Het precieze verband tussen het spectrum en het doorknippen van de graaf is het diepste resultaat in dit
boek met een korte formulering.

Definieer de **Cheeger-constante** — het isoperimetrisch getal:

`h(G) = min over S met |S| ≤ n/2 van |kanten die S verlaten| / |S|`

Haar berekenen betekent elke deelverzameling nagaan, dus ze is per definitie exponentieel. En toch:

> **Stelling (Cheeger; Alon–Milman).** `λ₂/2 ≤ h(G) ≤ √(2 · Δ · λ₂)`.

Een tweezijdige grens op een exponentieel moeilijke grootheid, uit één eigenwaarde die in `O(n³)`
berekenbaar is. Dat is de volledige theoretische grondslag van spectraal clusteren.

```
  held      ch30  Cheeger: a(G)/2 <= h(G) <= sqrt(2 * Delta * a(G))  (30 graphs)
```

De verificatie berekent `h(G)` via haar exponentiële definitie en `λ₂` uit de Laplaciaan, dus de twee
zijden komen uit ongerelateerde berekeningen. Dat is de enige eerlijke manier om een ongelijkheid tussen
beide te controleren.

De grens is niet scherp — er zit een vierkantswortel tussen de twee zijden — en die kloof is echt, geen
artefact van het bewijs. Ze is de reden dat spectraal clusteren goede partities geeft en geen optimale.

## Spectraal clusteren

Het algoritme volgt vanzelf. Om een graaf in tweeën te splitsen:

1. bereken de eigenvector bij `λ₂` — de **Fiedler-vector**;
2. sorteer de knopen op hun plaats erin;
3. knip bij de beste van de `n − 1` resulterende splitsingen.

De rechtvaardiging is opnieuw de kwadratische vorm. `xᵀLx` minimaliseren onder `x ⟂ 1` en `‖x‖ = 1` geeft
precies de Fiedler-vector, en `xᵀLx = Σ(x_u − x_v)²` is klein juist wanneer aangrenzende knopen
soortgelijke waarden krijgen. De Fiedler-vector is dus de toekenning van getallen aan knopen die
aangrenzende knopen zo dicht mogelijk bij elkaar brengt — een **relaxatie** van het 0/1-waardige
snedeprobleem, met de geheeltalligheid weggelaten.

Dat is het algemene recept om mee te nemen: **laat de geheeltalligheidseis vallen, los het continue
probleem exact op, en rond af.** De ongelijkheid van Cheeger is precies de uitspraak dat afronden niet
te veel verliest.

## Probeer het

```bash
python -c "
import sys, math; sys.path.insert(0, '.')
from graphs.core import complete, cycle, path, petersen, Graph
from graphs.spectral import (algebraic_connectivity, cheeger_constant,
                             laplacian_spectrum, spanning_tree_count)
print(f\"  {'graph':<10} {'lambda2':>9} {'h(G)':>7} {'lambda2/2':>10} {'sqrt(2*D*l2)':>13} {'trees':>7}\")
for name, g in [('P4', path(4)), ('C5', cycle(5)), ('K4', complete(4)), ('petersen', petersen())]:
    l2 = algebraic_connectivity(g); h = cheeger_constant(g)
    D = max(g.degree(v) for v in g.vertices())
    print(f'  {name:<10} {l2:>9.4f} {h:>7.4f} {l2/2:>10.4f} {math.sqrt(2*D*l2):>13.4f} {spanning_tree_count(g):>7}')
print()
two = Graph(6, [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3)])
print('  disconnected graph, lambda2 =', round(algebraic_connectivity(two), 10))
"
```

```
  graph        lambda2    h(G)  lambda2/2  sqrt(2*D*l2)   trees
  P4            0.5858  0.5000     0.2929        1.5307       1
  C5            1.3820  1.0000     0.6910        2.3511       5
  K4            4.0000  2.0000     2.0000        4.8990      16
  petersen      2.0000  1.0000     1.0000        3.4641    2000

  disconnected graph, lambda2 = 0.0
```

Elke rij voldoet aan `λ₂/2 ≤ h(G) ≤ √(2Δλ₂)`, en de twee grenzen liggen ver uiteen — voor `P₄` omsluiten
`0,29` en `1,53` een werkelijke waarde van `0,50`. Dat venster met factor vijf is wat "spectraal
clusteren werkt maar is niet optimaal" kwantitatief betekent.

Merk op dat `K₄` het scherpe geval aan de linkerkant is: `λ₂/2 = 2,0 = h(G)`.

## Oefeningen

1. Bewijs `xᵀLx = Σ_{uv∈E}(x_u − x_v)²` door uit te werken, en leid af dat `L` positief semidefiniet is.
2. Bereken het Laplace-spectrum van `K₃` met de hand en controleer dat de matrix-boomstelling 3 geeft.
3. Waarom is de al-enen-vector altijd een eigenvector van `L` met eigenwaarde 0?
4. `P₄` heeft `λ₂ = 0,586` en `K₄` heeft `λ₂ = 4`. Beide zijn samenhangend — wat meet het verschil?

Oplossingen in Bijlage E.

## Kernpunten

- `L = D − A`, en `xᵀLx = Σ(x_u − x_v)²` is de identiteit waaruit alles volgt.
- De multipliciteit van eigenwaarde nul is het aantal componenten. Samenhang wordt lineaire algebra.
- Matrix-boom telt opspannende bomen met één `O(n³)`-determinant en maakt de exponentiële opsomming van
  hoofdstuk 7 overbodig: `K₁₀` heeft `10⁸` opspannende bomen, ogenblikkelijk berekend.
- `λ₂` is nul precies wanneer de graaf onsamenhangend is, en meet hoe moeilijk hij te doorknippen is.
- Cheeger omsluit een exponentieel moeilijke grootheid tussen twee functies van één eigenwaarde. De
  kloof is een echte vierkantswortel, en daarom is spectraal clusteren goed en niet optimaal.
- Het recept veralgemeent: laat de geheeltalligheid vallen, los exact op, rond af.
