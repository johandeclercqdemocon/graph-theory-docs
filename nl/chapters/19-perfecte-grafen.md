# Hoofdstuk 19 — Perfecte en koordale grafen

Hoofdstuk 15 bewees `ω(G) ≤ χ(G)` in één regel en liet de kloof onverklaard. Dit hoofdstuk gaat over
de grafen waar er geen kloof is — een klasse groot genoeg om de meeste eenvoudige gevallen in het
boek te bevatten, en gekarakteriseerd door een stelling die veertig jaar kostte.

## De definitie, en waarom ze over deelgrafen kwantificeert

`G` is **perfect** wanneer `χ(H) = ω(H)` voor elke **geïnduceerde** deelgraaf `H`.

De kwantor is essentieel en is de hele reden dat de definitie werkt. Alleen `χ(G) = ω(G)` eisen geeft
een klasse zonder bruikbare structuur — `C₅` plus een disjuncte `K₃` heeft `χ = ω = 3` terwijl hij
`C₅` bevat, de canonieke imperfecte graaf. Het van elke geïnduceerde deelgraaf eisen maakt de
eigenschap **erfelijk**, en dat is wat inductie toelaat; erfelijke klassen zijn precies die welke
door verboden geïnduceerde deelgrafen gedefinieerd kunnen worden.

`C₅` is de kleinste imperfecte graaf: `ω = 2` (geen driehoek) maar `χ = 3` (oneven cykel).

```
  C4   chordal=False  perfect=True   chi=2 omega=2 odd_hole=False
  C5   chordal=False  perfect=False  chi=3 omega=2 odd_hole=True
  K4   chordal=True   perfect=True   chi=4 omega=4 odd_hole=False
  P4   chordal=True   perfect=True   chi=2 omega=2 odd_hole=False
```

## Koordale grafen

Een graaf is **koordaal** wanneer elke cykel van lengte minstens 4 een koorde heeft — equivalent:
hij heeft geen geïnduceerde cykel langer dan een driehoek.

> **Stelling.** Elke koordale graaf is perfect.

Het bewijs draait om een structureel feit dat apart vermelding verdient.

> **Lemma (Dirac).** Elke koordale graaf heeft een **simpliciale** knoop: een knoop wiens buren een
> kliek vormen.

Daarmee is de stelling een eenvoudige inductie: neem een simpliciale knoop `v`, kleur `G − v` met
`ω(G − v)` kleuren, en zet `v` terug. Zijn buurverzameling is een kliek van grootte `deg(v)`, dus
samen met `v` een kliek van grootte `deg(v) + 1 ≤ ω(G)`. Dus op zijn buren verschijnen hoogstens
`ω(G) − 1` kleuren, en er is er één vrij. ∎

Herhaald simpliciale knopen verwijderen geeft een **perfecte eliminatievolgorde**, en een graaf is
koordaal precies wanneer hij er een heeft. Dat levert een werkelijk lineaire test op — ongebruikelijk
voor dit boek, want er is geen exponentiële terugval:

```python
def is_chordal(g):
    order = maximum_cardinality_order(g)
    position = {v: i for i, v in enumerate(order)}
    for v in order:
        earlier = [w for w in g.neighbours(v) if position[w] < position[v]]
        if not earlier:
            continue
        parent = max(earlier, key=lambda w: position[w])
        for w in earlier:
            if w != parent and not g.has_edge(parent, w):
                return False
    return True
```

Het controleren vergde een orakel dat het idee niet deelt. De verificatie zoekt rechtstreeks naar een
geïnduceerde cykel van lengte ≥ 4:

```
  held      ch19  Chordality test agrees with searching for a chordless long cycle  (52 graphs)
  held      ch19  Every chordal graph is perfect  (44 graphs)
```

Op koordale grafen zijn kleuring, maximale kliek, grootste onafhankelijke verzameling en minimale
kliekoverdekking allemaal lineair of bijna lineair — stuk voor stuk `NP`-moeilijk in het algemeen.
Koordale grafen zijn ook precies de doorsnedegrafen van deelbomen van een boom, en daarom duiken ze
op bij ijle-matrixeliminatie en bij probabilistische grafische modellen.

## De twee grote stellingen

> **Stelling (Lovász, 1972 — de zwakke perfecte-grafenstelling).** `G` is perfect dan en slechts dan
> als zijn complement perfect is.

Een verrassende uitspraak: perfectie gaat over klieken en kleuringen, en complementeren verwisselt
klieken met onafhankelijke verzamelingen, dus er is geen voor de hand liggende reden waarom de
eigenschap zou overleven. Ze doet het, en de stelling verdubbelt onmiddellijk elk resultaat over
perfecte grafen.

> **Stelling (Chudnovsky, Robertson, Seymour, Thomas, 2006 — de sterke
> perfecte-grafenstelling).** `G` is perfect dan en slechts dan als noch `G` noch zijn complement een
> geïnduceerde oneven cykel van lengte minstens 5 bevat.

Vermoed door Berge in 1961, 45 jaar later bewezen in een artikel van 150 bladzijden. De verboden
structuren zijn de **oneven gaten** (geïnduceerde oneven cykels van lengte ≥ 5) en **oneven
antigaten** (hun complementen). De hele klasse wordt gedefinieerd door twee oneindige families uit te
sluiten, wat dezelfde vorm van antwoord is als die van Kuratowski in hoofdstuk 17 — en het is de reden
dat perfecte grafen in polynomiale tijd herkenbaar zijn.

De verificatie controleert de equivalentie, en voor grafen tot vijf knopen is dat een echte controle
van de *uitspraak*, ook al is het geen bewijsmateriaal voor de stelling:

```
  held      ch19  Berge: perfect iff no odd hole and no odd antihole  (52 graphs)
```

Merk op dat `C₅` zijn eigen complement is, dus hij is tegelijk een oneven gat en een oneven antigat —
de minimale belemmering in beide richtingen tegelijk.

## Waar perfectie al eerder opdook

Dit hoofdstuk geeft een naam aan een patroon dat deel III steeds gebruikte zonder het te benoemen:

| Klasse | Perfect? | Welke stelling eenvoudig werd |
|---|---|---|
| Bipartiet | ja | König (h. 14): `χ = ω = 2`, koppeling = overdekking |
| Bossen | ja | triviaal 2-kleurbaar (h. 6) |
| Koordaal | ja | gulzige kleuring is optimaal |
| Intervalgrafen | ja | plannen op vroegste eindtijd |
| Complementen van bipartiete | ja | via de stelling van Lovász |
| Oneven cykels `C₅`, `C₇`, … | **nee** | `χ = 3`, `ω = 2` |

De stelling van König in hoofdstuk 14 is het bipartiete geval van een veel algemener verschijnsel.
Kom je een grafenprobleem tegen dat op een klasse onverwacht eenvoudig is, dan is perfectie het eerste
om te controleren.

## Probeer het

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import cycle, complete, path
from graphs.algorithms import chromatic_number, max_clique_size
from graphs.perfect import is_chordal, is_perfect, has_odd_hole, has_odd_antihole
for name, g in [('C4', cycle(4)), ('C5', cycle(5)), ('K4', complete(4)), ('P4', path(4))]:
    print(f'{name:<4} chordal={is_chordal(g)!s:<6} perfect={is_perfect(g)!s:<6} '
          f'chi={chromatic_number(g)} omega={max_clique_size(g)} '
          f'odd_hole={has_odd_hole(g)!s:<6} odd_antihole={has_odd_antihole(g)}')
"
```

```
C4   chordal=False  perfect=True   chi=2 omega=2 odd_hole=False  odd_antihole=False
C5   chordal=False  perfect=False  chi=3 omega=2 odd_hole=True   odd_antihole=True
K4   chordal=True   perfect=True   chi=4 omega=4 odd_hole=False  odd_antihole=False
P4   chordal=True   perfect=True   chi=2 omega=2 odd_hole=False  odd_antihole=False
```

`C₄` is perfect maar **niet** koordaal — het is een geïnduceerde vierhoek zonder koorde. Koordaliteit
is voldoende voor perfectie en niet noodzakelijk, en `C₄` is het kleinste ding dat dat aantoont.

## Oefeningen

1. Ga met de hand na dat `C₅` `ω = 2` en `χ = 3` heeft.
2. Toon aan dat elke intervalgraaf koordaal is.
3. Waarom kwantificeert de definitie van perfect over geïnduceerde deelgrafen en niet over alle
   deelgrafen? Geef een graaf die het alternatief zou breken.
4. `C₅` is zelfcomplementair. Vind een andere zelfcomplementaire graaf, en zeg of hij perfect is.

Oplossingen in Bijlage E.

## Kernpunten

- Perfect betekent `χ = ω` op **elke geïnduceerde deelgraaf**. De kwantor maakt de klasse erfelijk,
  en dat is wat haar bruikbaar maakt.
- `C₅` is de kleinste imperfecte graaf, en hij is zijn eigen complement — tegelijk een oneven gat en
  een oneven antigat.
- Koordale grafen zijn perfect, via simpliciale knopen en perfecte eliminatievolgordes, en
  koordaliteit is in lineaire tijd testbaar.
- Koordaal is voldoende voor perfect, niet noodzakelijk: `C₄` is perfect en niet koordaal.
- Lovász: perfectie overleeft complementeren. Chudnovsky–Robertson–Seymour–Thomas: perfectie is
  precies de afwezigheid van oneven gaten en oneven antigaten.
- Bipartiete grafen zijn het perfecte geval dat je al ontmoette. König is een gevolg van een veel
  groter verhaal.
