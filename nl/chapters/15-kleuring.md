# Hoofdstuk 15 — Kleuring

Een **geldige kleuring** geeft elke knoop een kleur zó dat aangrenzende knopen verschillen. Het
**chromatisch getal** `χ(G)` is het kleinste aantal kleuren dat volstaat. Het berekenen is
`NP`-moeilijk (hoofdstuk 22), dus het grootste deel van het vak bestaat uit grenzen — en in de
grenzen zitten de ideeën.

## De voor de hand liggende grenzen

> **Lemma.** `ω(G) ≤ χ(G) ≤ Δ(G) + 1`.

De ondergrens is onmiddellijk: een kliek van grootte `ω` heeft `ω` verschillende kleuren nodig. De
bovengrens komt van het gulzige algoritme hieronder.

Beide kunnen ver van de waarheid liggen. De kloof aan de linkerkant is het onderwerp van hoofdstuk
19. Die aan de rechterkant is enorm voor een ster: `K_{1,7}` heeft `Δ = 7` en `χ = 2`.

## Gulzig, en de volgorde waarvan het afhangt

Neem de knopen in een of andere volgorde; geef elke knoop de kleinste kleur die geen al gekleurde
buur gebruikt.

```python
def greedy_colouring(g, order=None):
    colour = {}
    for v in order if order is not None else g.vertices():
        used = {colour[w] for w in g.neighbours(v) if w in colour}
        c = 0
        while c in used:
            c += 1
        colour[v] = c
    return colour
```

Het gebruikt nooit meer dan `Δ + 1` kleuren, want een knoop heeft hoogstens `Δ` gekleurde buren en
`Δ + 1` kleuren laten er altijd één vrij. Dat bewijst de bovengrens hierboven.

**Het resultaat hangt volledig van de volgorde af, en die afhankelijkheid is niet mild.** Het
standaardgetuigenis is de **kroongraaf**: `K_{n,n}` met een perfecte koppeling verwijderd. Hij is
bipartiet, dus `χ = 2`. Orden de knopen door tussen de zijden af te wisselen en gulzig gebruikt `n`
kleuren:

```
  crown n=3: chi=2 greedy(natural)=2 greedy(interleaved)=3 degeneracy=2
  crown n=4: chi=2 greedy(natural)=2 greedy(interleaved)=4 degeneracy=3
  crown n=5: chi=2 greedy(natural)=2 greedy(interleaved)=5 degeneracy=4
```

Gulzig dat op een tweekleurbare graaf vijf kleuren gebruikt is zo slecht als een benadering
plausibel kan worden, en het is geen gekunstelde pathologie — het is wat er gebeurt wanneer je de
knopen toevallig in de verkeerde volgorde verwerkt.

Merk op dat de natuurlijke volgorde het elke keer goed doet. Test je gulzig op kroongrafen zonder
over de ordening na te denken, dan concludeer je dat het goed werkt.

## Degeneratie: de grens die de moeite waard is

`Δ + 1` is zwak omdat ze door de ene slechtste knoop bepaald wordt. De oplossing is vragen wat er
gebeurt terwijl je de graaf afpelt.

De **degeneratie** `d(G)` is de grootste `k` zodat elke deelgraaf een knoop van graad hoogstens `k`
heeft. Equivalent: verwijder herhaaldelijk een knoop van minimale graad, en `d(G)` is de grootste
graad die je ooit verwijdert.

> **Stelling.** `χ(G) ≤ d(G) + 1`, en `d(G) ≤ Δ(G)`.

*Bewijs.* Verwijder knopen van minimale graad één voor één en noteer de volgorde; kleur dan gulzig
in de **omgekeerde** volgorde. Wanneer elke knoop gekleurd wordt, zijn zijn al gekleurde buren
precies die welke er nog waren toen hij verwijderd werd — hoogstens `d(G)` ervan. Dus `d(G) + 1`
kleuren volstaan. ∎

Dit is strikt beter dan `Δ + 1` en nooit slechter:

```
  star K_1,7: Delta = 7  degeneracy = 1  chi = 2
  a tree:     Delta = 3  degeneracy = 1  chi = 2
```

Elk bos heeft degeneratie 1, wat `χ ≤ 2` geeft — het resultaat van hoofdstuk 6, teruggevonden als
bijzonder geval. Elke vlakke graaf heeft degeneratie hoogstens 5 (hoofdstuk 17), wat de
zeskleurenstelling gratis oplevert.

```
  held      ch15  Greedy colouring uses at most degeneracy + 1 colours  (52 graphs)
  held      ch15  chi <= degeneracy + 1, which is never worse than Delta + 1  (52 graphs)
```

## De stelling van Brooks

`Δ + 1` is scherp voor precies twee families, en dat is de hele inhoud van het resultaat.

> **Stelling (Brooks, 1941).** Is `G` samenhangend en noch een volledige graaf noch een oneven
> cykel, dan `χ(G) ≤ Δ(G)`.

De twee uitzonderingen zijn geen versiering. `K_n` heeft `Δ = n − 1` en `χ = n`. Een oneven cykel
heeft `Δ = 2` en `χ = 3`. Laat een van beide uitzonderingen weg en de stelling is onwaar bij `K₃`,
dat beide is.

De verificatie codeert de uitzonderingen als *falende voorwaarden* in plaats van als bijzondere
gevallen die slagen, precies het onderscheid waarvoor hoofdstuk 3 pleitte:

```python
if canonical(g) == canonical(complete(g.n)):
    return None                      # says nothing, rather than "held"
if g.n % 2 == 1 and canonical(g) == canonical(cycle(g.n)):
    return None
return chromatic_number(g) <= max_degree(g)
```

Het bewijs is een gevalsonderscheid naar samenhang dat dit boek niet volledig weergeeft; de
leesbare kern is dat een niet-volledige samenhangende graaf met `Δ ≥ 3` een ordening heeft waarin
gulzig bij de laatste knoop een kleur vrijlaat, verkregen door een opspannende boom in een geschikte
knoop te wortelen en naar binnen te kleuren.

## Exacte kleuring

`χ(G)` wordt hier berekend door `k = 1, 2, 3, …` te proberen met backtracking:

```python
def chromatic_number(g):
    for k in range(1, g.n + 1):
        if _colourable(g, k):
            return k
    return g.n
```

Exponentieel, en onvermijdelijk zo tenzij `P = NP`. Bruikbaar tot ongeveer twaalf knopen, wat
genoeg is voor de verificatie en voor niets anders. Hoofdstuk 23 behandelt wat je in plaats daarvan
doet wanneer je werkelijk een antwoord nodig hebt.

## Probeer het

Kijk hoe de ordening ertoe doet, op een graaf die tweekleurbaar is:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import Graph
from graphs.algorithms import chromatic_number, greedy_colouring
from graphs.planar import degeneracy_order

# crown graph: K_{4,4} minus a perfect matching
n = 4
g = Graph(2*n, [(i, n+j) for i in range(n) for j in range(n) if i != j])
interleaved = [x for i in range(n) for x in (i, n+i)]
print('chromatic number      ', chromatic_number(g))
print('greedy, natural order ', max(greedy_colouring(g).values()) + 1)
print('greedy, interleaved   ', max(greedy_colouring(g, interleaved).values()) + 1)
print('greedy, degeneracy    ', max(greedy_colouring(g, degeneracy_order(g)).values()) + 1)
"
```

```
chromatic number       2
greedy, natural order  2
greedy, interleaved    4
greedy, degeneracy     2
```

Vier kleuren voor een bipartiete graaf, enkel door een slechte volgorde. De degeneratieordening
herstelt hier het juiste antwoord, al is dat in het algemeen niet gegarandeerd — ze garandeert
alleen `d + 1`, en dat is 4 voor deze graaf.

## Oefeningen

1. Toon aan dat `χ(G) ≥ n / α(G)`, waarbij `α(G)` de grootte is van de grootste onafhankelijke
   verzameling.
2. Vind een graaf met `ω(G) = 2` en `χ(G) = 3`. Wat is de kleinste zo'n graaf?
3. Bewijs dat elke graaf met degeneratie `d` hoogstens `d · n` kanten heeft.
4. De kroongraaf hierboven heeft `χ = 2` maar gulzig kan er `n` kleuren gebruiken. Wat is zijn
   degeneratie, en waarom is dat geen tegenspraak met de grens `d + 1`?

Oplossingen in Bijlage E.

## Kernpunten

- `ω(G) ≤ χ(G) ≤ Δ(G) + 1`. Beide ongelijkheden kunnen willekeurig ruim zijn.
- Het antwoord van gulzig hangt volledig af van de knoopvolgorde. Op de kroongraaf gebruikt een
  slechte volgorde `n` kleuren waar er 2 volstaan — en de natuurlijke volgorde doet het goed, dus
  een onzorgvuldige test ziet niets verkeerds.
- Degeneratie is de grens om te gebruiken: `χ ≤ d + 1`, nooit slechter dan `Δ + 1`, en ze levert
  bossen en vlakke grafen hun grens gratis.
- Brooks: `χ ≤ Δ` tenzij de graaf volledig is of een oneven cykel. Beide uitzonderingen zijn nodig
  en `K₃` is ze allebei.
- Exacte `χ` is `NP`-moeilijk; de implementatie hier is voor verificatie en niet voor gebruik.
