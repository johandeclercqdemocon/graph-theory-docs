# Hoofdstuk 22 — NP-moeilijkheid

Aan verschillende problemen in dit boek is "en dit is `NP`-moeilijk" gehangen zonder verantwoording.
Dit hoofdstuk maakt de bewering precies en toont de techniek, op de grafenproblemen die we al in
handen hebben.

## Wat de bewering betekent

Een beslissingsprobleem zit in **`NP`** wanneer een *ja*-geval een certificaat heeft dat in
polynomiale tijd controleerbaar is. "Heeft `G` een onafhankelijke verzameling van grootte `k`?" zit in
`NP`: overhandig de verzameling, en controleren kost `O(k²)`.

Een probleem is **`NP`-moeilijk** wanneer elk probleem in `NP` er in polynomiale tijd toe herleid kan
worden, en **`NP`-volledig** wanneer het allebei is. Een reductie van `A` naar `B` is een
polynomiale afbeelding `f` met `x ∈ A ⟺ f(x) ∈ B`, en ze betekent dat `B` minstens zo moeilijk is
als `A`.

Twee dingen worden vaak door elkaar gehaald. `NP`-moeilijk betekent niet "niet in `P`" — dat is juist
de open vraag. En het betekent niet "moeilijk in de praktijk": SAT-oplossers verwerken routineus
gevallen met miljoenen variabelen. `NP`-moeilijkheid is een uitspraak over slechtste gevallen over
alle invoeren, wat een veel zwakkere bewering over jouw invoer is dan het klinkt.

## Het reductiepatroon

De richting die iedereen in verwarring brengt: om te tonen dat `B` moeilijk is, herleid je een
**bekend moeilijke** `A` **naar** `B`. Je toont dat `B` oplossen je `A` zou laten oplossen, dus `B`
erft de moeilijkheid van `A`. `B` naar `A` herleiden toont niets over `B`.

Elke reductie heeft drie verplichtingen, en de derde overslaan is de standaardfout:

1. `f` loopt in polynomiale tijd;
2. `x ∈ A ⟹ f(x) ∈ B`;
3. `f(x) ∈ B ⟹ x ∈ A`.

De derde is waar reducties werkelijk sneuvelen. Het is eenvoudig om een gadget te bouwen dat
oplossingen in oplossingen omzet en te vergeten oplossingen van `f(x)` uit te sluiten die nergens
vandaan kwamen.

## De reducties die we al hebben

De identiteiten van hoofdstuk 21 zijn reducties, en ongewoon eenvoudige:

```python
def clique_to_independent_set(g):
    return g.complement()                       # omega(G) = alpha(complement)

def independent_set_to_vertex_cover(g, independent):
    return set(g.vertices()) - independent      # alpha(G) + tau(G) = n
```

Beide zijn `O(n²)` en beide behouden optima in elke richting, wat verplichting 3 naar behoren
uitvoert. De verificatie controleert het:

```
  held      ch22  The complement of a maximum independent set is a minimum vertex cover  (52 graphs)
```

Let op wat die controle wel en niet vaststelt. Ze bevestigt dat de *reductie correct is* — dat de
afbeelding optima werkelijk op optima afbeeldt. Ze zegt niets over `NP`-moeilijkheid, wat niet het
soort uitspraak is dat een eindige controle kan behandelen.

## 3-SAT naar onafhankelijke verzameling

Het klassieke startpunt is `3-SAT`, dat Cook en Levin rechtstreeks `NP`-volledig bewezen. Vanaf daar
is al het overige reducties.

Gegeven een 3-CNF-formule met `k` clausules, bouw een graaf:

- voor elke clausule een **driehoek** waarvan de drie knopen haar literalen zijn;
- een kant tussen elke twee knopen met **tegenstrijdige** literalen (`x` en `¬x`).

Dan is de formule vervulbaar **dan en slechts dan als** de graaf een onafhankelijke verzameling van
grootte `k` heeft.

*Bewijs.* (⟹) Gegeven een vervullende toekenning, kies per clausule één ware literaal. Geen twee zijn
tegenstrijdig, want ze zijn alle waar onder één toekenning, en geen twee zitten in dezelfde driehoek.
Dat is een onafhankelijke verzameling van grootte `k`.

(⟸) Gegeven een onafhankelijke verzameling van grootte `k`: de driehoeken dwingen hoogstens één knoop
per clausule af, dus precies één uit elke. Geen twee gekozen literalen zijn tegenstrijdig, dus elke
gekozen literaal waar maken is consistent, en het vervult elke clausule. Variabelen die ongezet
blijven mogen beide kanten op. ∎

De twee gadgets doen elk precies één taak. De driehoek dwingt "hoogstens één per clausule" af; de
tegenstrijdigheidskanten dwingen consistentie af. Die scheiding van verantwoordelijkheden is hoe een
goede reductie eruitziet, en de (⟸)-richting is waar de driehoeken hun plaats verdienen.

## Wat moeilijk is en wat niet

| Probleem | Status |
|---|---|
| Kortste pad (niet-negatief) | `P` — hoofdstuk 10 |
| Maximale stroom | `P` — hoofdstuk 13 |
| Bipartiete koppeling | `P` — hoofdstuk 14 |
| Algemene koppeling | `P` — Edmonds' bloesems, hoofdstuk 14 |
| Vlakheid | `P`, zelfs `O(n)` — hoofdstuk 17 |
| 2-kleuring | `P` — hoofdstuk 16 |
| **3-kleuring** | `NP`-volledig |
| Onafhankelijke verzameling, kliek, knopenoverdekking | `NP`-volledig — hoofdstuk 21 |
| Hamiltoniaanse cykel | `NP`-volledig — hoofdstuk 20 |
| Grafenisomorfie | in `NP`, geen van beide bekend — hoofdstuk 5 |

De grens is scherp en vaak verrassend. Twee kleuren eenvoudig, drie moeilijk. Euler-circuit
eenvoudig, Hamiltoniaanse cykel moeilijk. Koppeling eenvoudig, onafhankelijke verzameling moeilijk. In
elk paar zien de twee problemen er vergelijkbaar moeilijk uit en zijn ze het niet, en daarom is "dit
ziet er moeilijk uit" nooit een argument.

## Probeer het

Kijk hoe de reductie een optimum overdraagt, in beide richtingen:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import petersen, cycle
from graphs.approx import (max_clique, max_independent_set, min_vertex_cover,
                           clique_to_independent_set, independent_set_to_vertex_cover,
                           is_vertex_cover)
for name, g in [('C5', cycle(5)), ('petersen', petersen())]:
    ind = max_independent_set(g)
    cover = independent_set_to_vertex_cover(g, ind)
    print(f'{name}: alpha={len(ind)} -> cover size {len(cover)}, valid={is_vertex_cover(g, cover)}, '
          f'optimal={len(cover) == len(min_vertex_cover(g))}')
    print(f'   omega(G)={len(max_clique(g))} equals alpha(complement)={len(max_independent_set(clique_to_independent_set(g)))}')
"
```

```
C5: alpha=2 -> cover size 3, valid=True, optimal=True
   omega(G)=2 equals alpha(complement)=2
petersen: alpha=4 -> cover size 6, valid=True, optimal=True
   omega(G)=2 equals alpha(complement)=2
```

## Oefeningen

1. Om te bewijzen dat probleem `B` `NP`-moeilijk is, herleid je `B` naar een bekend moeilijk probleem
   of andersom? Leg uit waarom de andere richting niets bewijst.
2. Wat gaat er in de 3-SAT-reductie mis als je de tegenstrijdigheidskanten weglaat?
3. Wat gaat er mis als je de driehoeken weglaat?
4. Knopenoverdekking is `NP`-volledig in het algemeen maar eenvoudig op bipartiete grafen (hoofdstuk
   14). Is dat in tegenspraak met `NP`-moeilijkheid?

Oplossingen in Bijlage E.

## Kernpunten

- Om te bewijzen dat `B` moeilijk is, herleid je een bekend moeilijke `A` **naar** `B`. De andere
  richting bewijst niets.
- Een reductie heeft drie verplichtingen; de omgekeerde implicatie is degene die in de praktijk
  sneuvelt.
- De reductie van 3-SAT naar onafhankelijke verzameling gebruikt twee gadgets met elk één taak:
  driehoeken voor "één literaal per clausule", tegenstrijdigheidskanten voor consistentie.
- Een reductie op voorbeelden controleren bevestigt dat ze optima juist afbeeldt. Ze kan
  `NP`-moeilijkheid niet bevestigen, want dat is niet dat soort uitspraak.
- De grens tussen `P` en `NP`-volledig volgt niet de schijnbare moeilijkheid: 2-kleuring eenvoudig,
  3-kleuring moeilijk; Euler eenvoudig, Hamilton moeilijk; koppeling eenvoudig, onafhankelijke
  verzameling moeilijk.
