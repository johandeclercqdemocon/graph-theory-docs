# Hoofdstuk 31 — Minoren en boombreedte

Hoofdstuk 17 karakteriseerde vlakheid met twee verboden minoren. Dit hoofdstuk gaat over hoe ver dat
idee reikt, en het reikt opmerkelijk ver — tot een stelling die oneindig veel vragen tegelijk beslecht
en je het antwoord op geen enkele ervan vertelt.

## Minoren

`H` is een **minor** van `G` wanneer hij verkregen kan worden door knopen te verwijderen, kanten te
verwijderen, en kanten samen te trekken. Een klasse grafen is **minor-gesloten** wanneer ze onder die
operaties gesloten is: vlakke grafen, bossen, grafen inbedbaar op een vast oppervlak, grafen van
boombreedte hoogstens `k`.

Kuratowski en Wagner gaven vlakheid twee verboden minoren. De voor de hand liggende vraag is of elke
minor-gesloten klasse een eindige belemmeringsverzameling heeft. Dat is zo.

> **Stelling (Robertson–Seymour, 1983–2004).** Elke minor-gesloten klasse grafen wordt gekarakteriseerd
> door een **eindige** verzameling verboden minoren.

Twintig artikelen over twintig jaar, en het is een van de diepste resultaten in de combinatoriek. Het
heeft een onmiddellijk algoritmisch gevolg, want testen op een vaste minor `H` kost `O(n³)`:

> **Gevolg.** Lidmaatschap van elke minor-gesloten klasse is beslisbaar in `O(n³)`.

En hier komt het vreemdste. De stelling vertelt je niet wat de verboden minoren *zijn*. Ze bewijst dat
de verzameling eindig is zonder haar te identificeren — dus voor een gegeven minor-gesloten klasse weet
je dat er een kubisch algoritme bestaat en heb je mogelijk geen enkele manier om het op te schrijven.
Voor grafen inbedbaar op de torus zijn meer dan 17.000 verboden minoren bekend en de volledige lijst is
nog steeds onbekend.

**Dit is niet-constructiviteit van een andere orde dan die van hoofdstuk 24.** De probabilistische
methode bewijst dat een object bestaat zonder het te produceren; Robertson–Seymour bewijst dat een
*algoritme* bestaat zonder het te produceren. Weten dat je probleem in kubische tijd beslisbaar is
terwijl je geen middel hebt om het te beslissen, is een ongewone positie.

## Boombreedte

De andere helft van de theorie is een parameter die meet hoe boomachtig een graaf is.

Een **boomdecompositie** kent elke knoop van een boom een **zak** knopen toe zodat:

1. elke knoop in een zak zit;
2. elke kant beide eindpunten in een zak heeft;
3. voor elke knoop de zakken die hem bevatten een samenhangende deelboom vormen.

De **breedte** is de grootste zakgrootte min één; de **boombreedte** is de minimale breedte over alle
decomposities. De min één is een conventie zó gekozen dat bomen boombreedte 1 hebben in plaats van 2.

Voorwaarde 3 draagt de inhoud. Zonder haar kon je elke knoop in één zak stoppen en was de definitie
leeg.

Boombreedte berekenen gaat eenvoudiger via **eliminatievolgordes**:

```python
def eliminate(g, order):
    adjacency = {v: set(g.neighbours(v)) for v in g.vertices()}
    remaining, width = set(g.vertices()), 0
    for v in order:
        nbrs = adjacency[v] & remaining - {v}
        width = max(width, len(nbrs))
        for a, b in itertools.combinations(nbrs, 2):   # the fill edges
            adjacency[a].add(b); adjacency[b].add(a)
        remaining.discard(v)
    return width
```

`treewidth(G)` is het minimum hiervan over alle `n!` volgordes. Dat is exact en hopeloos voorbij
`n = 8`, wat passend is — boombreedte berekenen is `NP`-moeilijk, al is het vast-parameter hanteerbaar
in de breedte zelf (Bodlaender).

```
  P5        n=5   treewidth=1
  tree      n=7   treewidth=1
  C5        n=5   treewidth=2
  K4        n=4   treewidth=3
  K5        n=5   treewidth=4
  K33       n=6   treewidth=3
  grid2x3   n=6   treewidth=2
  grid3x3   n=9   treewidth=3
```

Bossen hebben boombreedte 1, cykels 2, `K_n` precies `n − 1`. Het `r × c`-rooster heeft boombreedte
`min(r, c)` — dus **vlakke grafen hebben onbegrensde boombreedte**, en vlakheid en begrensde
boombreedte zijn werkelijk verschillende beperkingen.

```
  held      ch31  Treewidth is 1 exactly for forests with at least one edge  (51 graphs)
  held      ch31  Treewidth of K_n is n-1, and of a cycle is 2  (7 graphs)
  held      ch31  Treewidth never increases when passing to a subgraph  (51 graphs)
  held      ch31  Chordal graphs have treewidth = max clique size - 1  (44 graphs)
```

De laatste regel verbindt met hoofdstuk 19. Koordale grafen zijn precies de grafen waarvan de eliminatie
geen opvulkanten produceert, dus hun boombreedte is rechtstreeks van hun grootste kliek af te lezen —
en daarom komen koordaliteit en boombreedte steeds in dezelfde zinnen voor.

## De stelling van Courcelle

Begrensde boombreedte is de moeite waard vanwege wat je ermee kunt.

> **Stelling (Courcelle, 1990).** Elke grafeneigenschap uitdrukbaar in monadische tweede-orde logica is
> in lineaire tijd beslisbaar op grafen van begrensde boombreedte.

Dat omvat 3-kleurbaarheid, Hamiltoniciteit, onafhankelijke verzameling, dominerende verzameling, en in
wezen elk probleem in deel V. Alle `NP`-moeilijk in het algemeen; alle lineaire tijd zodra de
boombreedte begrensd is.

Het mechanisme is dynamisch programmeren over de decompositieboom: verwerk de zakken van de bladeren
omhoog en houd voor elke zak een tabel van deeloplossingen bij, geïndexeerd op de inwendige configuratie
van de zak. De tabel heeft grootte exponentieel in de **breedte** en het aantal zakken is lineair in
`n`, wat `f(k) · n` geeft.

**Dit boek implementeert dat dynamisch programmeren niet.** Het correct doen betekent de
decompositieboom bouwen en introduceer-, vergeet- en samenvoegknopen behandelen, en een fout erin zou
onzichtbaar zijn tegen de bruteforce-antwoorden die de verificatie overal elders gebruikt. Dezelfde
keuze werd gemaakt voor Hopcroft–Tarjan-vlakheid in hoofdstuk 17 en voor de vierkleurenstelling in
hoofdstuk 18: waar de eerlijke opties een lange correcte implementatie of een korte foute zijn,
beschrijft dit boek en zegt het dat het beschrijft.

Het praktische voorbehoud is dat `f(k)` vaak wreed is — voor de stelling van Courcelle in volle
algemeenheid is het een toren van exponenten in de formulegrootte. "Lineaire tijd" verbergt een
constante die de leeftijd van het heelal kan overtreffen. Met de hand geschreven DP's voor specifieke
problemen doen het veel beter, en dat is wat men in de praktijk gebruikt.

## De structuurstelling voor grafenminoren

Onder Robertson–Seymour ligt een structurele beschrijving waarvan het bestaan het weten waard is.

> Ruwweg: voor elke vaste `H` kan elke `H`-minorvrije graaf opgebouwd worden door grafen aan elkaar te
> lijmen die "bijna inbedbaar" zijn op oppervlakken van begrensd geslacht.

Een minor uitsluiten dwingt dus bijna-topologische structuur af. Dit is de motor achter zowel de
welgeordendheidsstelling als de algoritmische resultaten, en de volledige formulering beslaat een
bladzijde. Het is de reden dat "uitgesloten minor" en "begrensde boombreedte" de twee ordenende ideeën
van de structurele grafentheorie zijn.

## Probeer het

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import Graph, complete, cycle, path, complete_bipartite
from graphs.treewidth import treewidth, tree_decomposition, is_tree_decomposition, grid

for name, g in [('P5', path(5)), ('C5', cycle(5)), ('K4', complete(4)),
                ('K3,3', complete_bipartite(3,3)), ('2x3 grid', grid(2,3))]:
    print(f'{name:<9} treewidth = {treewidth(g)}')
print()
g = cycle(5)
bags = tree_decomposition(g, list(g.vertices()))
print('C5 bags from the natural elimination order:', [sorted(b) for b in bags])
print('is a valid tree decomposition:', is_tree_decomposition(g, bags))
print('width of THIS ordering:', max(len(b) for b in bags) - 1, ' optimal:', treewidth(g))
"
```

```
P5        treewidth = 1
C5        treewidth = 2
K4        treewidth = 3
K3,3      treewidth = 3
2x3 grid  treewidth = 2

C5 bags from the natural elimination order: [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 4], [4]]
is a valid tree decomposition: True
width of THIS ordering: 2  optimal: 2
```

De zakken krimpen naarmate de eliminatie vordert, en de grootste heeft drie knopen — breedte 2, wat
optimaal is voor een cykel. Let op de opvulkant: knoop 0 elimineren verbindt zijn buren 1 en 4, die in
`C₅` niet aangrenzend waren.

## Oefeningen

1. Geef een boomdecompositie van `K₄` van breedte 3, en beargumenteer dat er geen betere bestaat.
2. Waarom trekt de definitie van breedte er één af?
3. Toon aan dat het `2 × n`-rooster boombreedte 2 heeft voor elke `n`.
4. Vlakke grafen hebben onbegrensde boombreedte. Welke familie toont dat, en waarom doet het ertoe voor
   algoritmen?

Oplossingen in Bijlage E.

## Kernpunten

- Minor-gesloten klassen hebben eindige karakteriseringen met verboden minoren (Robertson–Seymour), dus
  lidmaatschap is beslisbaar in `O(n³)` — zonder dat de stelling je vertelt welke minoren, en dus ook
  niet hoe.
- Dat is niet-constructiviteit één niveau boven hoofdstuk 24: een *algoritme* waarvan bewezen is dat het
  bestaat en dat niet geproduceerd wordt.
- Boombreedte meet boomachtigheid: 1 voor bossen, 2 voor cykels, `n − 1` voor `K_n`, `min(r,c)` voor het
  `r × c`-rooster.
- Vlakke grafen hebben onbegrensde boombreedte, dus de twee beperkingen zijn onafhankelijk.
- Courcelle: begrensde boombreedte maakt elke MSO-uitdrukbare eigenschap lineaire tijd. De verborgen
  constante kan een toren van exponenten zijn, en dit boek beschrijft het DP in plaats van het te
  implementeren.
