# Hoofdstuk 11 — Afstand tussen alle paren

Dijkstra vanuit elke knoop draaien kost `O(nm log n)`. Op een dichte graaf bestaat er iets
eenvoudigers en, opmerkelijk genoeg, snellers — en het is vier regels.

## Floyd–Warshall

Het idee is een andere inductie dan elk algoritme tot nu toe. In plaats van naar buiten te
groeien vanuit een bron, beperk je welke knopen een pad **doorheen** mag gaan.

Zij `d_k(u,v)` de lengte van het kortste `u`–`v`-pad waarvan alle inwendige knopen in
`{0, …, k−1}` liggen. Dan is `d_0` gewoon het booggewicht, en

```
d_{k+1}(u,v) = min( d_k(u,v),  d_k(u,k) + d_k(k,v) )
```

want een pad dat `k` mag gebruiken doet dat ofwel niet — de eerste term — ofwel wel, en dan gaat
het precies één keer door `k` en valt het uiteen in twee paden die dat niet doen.

Dat "precies één keer" vraagt om rechtvaardiging: een kortste pad bezoekt geen knoop twee keer,
mits er geen negatieve cykel is. De recursie is dus geldig onder dezelfde voorwaarde die
Bellman–Ford nodig heeft, en faalt zonder haar op dezelfde manier.

```python
def floyd_warshall(d):
    n = d.n
    dist = [[INF] * n for _ in range(n)]
    for v in range(n):
        dist[v][v] = 0.0
    for u, v, w in d.arcs():
        dist[u][v] = min(dist[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
```

`O(n³)`, drie geneste lussen, geen prioriteitswachtrij en helemaal geen datastructuur. **De
`k`-lus moet de buitenste zijn.** Dat is het enige wat je goed moet krijgen: `k` indexeert de
inductie, en `i` en `j` doorlopen binnen een vaste fase. Verwissel de lussen en je krijgt een
algoritme dat soms correcte antwoorden geeft, en dat is de ergste soort fout.

```python
d = Digraph(5, [(0,1,4), (0,2,1), (2,1,2), (1,3,1), (2,3,5), (3,4,3)])
for row in floyd_warshall(d):
    print(row)
```

```
  0 [0, 3, 1, 4, 7]
  1 [inf, 0, inf, 1, 4]
  2 [inf, 2, 0, 3, 6]
  3 [inf, inf, inf, 0, 3]
  4 [inf, inf, inf, inf, 0]
```

Rij 0 komt exact overeen met de Dijkstra-uitvoer van hoofdstuk 10. De oneindigheden zijn
eerlijk: deze digraaf heeft geen bogen terug naar 0, dus niets bereikt hem.

## Negatieve gewichten, en een andere vraag

Floyd–Warshall hanteert negatieve bogen zonder aanpassing, wat Dijkstra niet kan. En het
detecteert negatieve cykels anders dan Bellman–Ford, op een manier die precisie verdient:

```python
neg = Digraph(3, [(0,1,1), (1,2,-3), (2,0,1)])
print([floyd_warshall(neg)[v][v] for v in range(3)])   # [-1, -1, -2]
```

Een **negatieve plaats op de diagonaal** betekent dat `v` op een negatieve cykel ligt.
Bellman–Ford vanuit een bron `s` meldt of een negatieve cykel *bereikbaar is vanuit `s`*;
Floyd–Warshall meldt welke knopen er *op* liggen. Dat zijn verschillende vragen, en beide zijn
nuttig:

- De versie van Bellman–Ford vertelt je dat je afstanden vanuit `s` betekenisloos zijn.
- Die van Floyd–Warshall vertelt je welk deel van de graaf het probleem is.

De `-2` bij knoop 2 is geen afstand. Zodra er een negatieve cykel bestaat, zijn de getallen in de
matrix wat het vaste aantal relaxatieronden toevallig opleverde, en alleen hun teken is
betekenisvol.

## De metriek

Voor een ongerichte graaf met niet-negatieve gewichten is `d` een echte **metriek**:
niet-negatief, nul precies op de diagonaal, symmetrisch, en voldoend aan de
driehoeksongelijkheid. De verificatie controleert die laatste rechtstreeks:

```
  held      ch11  Graph distance satisfies the triangle inequality  (120 graphs)
  held      ch11  Floyd-Warshall agrees with enumerating every simple path  (120 graphs)
```

Symmetrie is degene die faalt voor digrafen, en ze faalt grondig — `d(u,v)` kan eindig zijn
terwijl `d(v,u)` oneindig is, zoals rij 1 van de matrix hierboven laat zien. Een gerichte graaf
geeft een **quasimetriek**, en elke meetkundige intuïtie die je uit metrische ruimten meeneemt,
moet daaraan getoetst worden.

Uit de alle-parenmatrix volgen drie standaardgrootheden:

- de **excentriciteit** van `v` is `max_u d(v,u)`;
- de **diameter** is de grootste excentriciteit;
- de **straal** is de kleinste excentriciteit, en een knoop die haar bereikt is een **centrum**.

`straal ≤ diameter ≤ 2 · straal`. De rechterongelijkheid is de driehoeksongelijkheid toegepast
via een centrum `c`: `d(u,v) ≤ d(u,c) + d(c,v) ≤ 2 · straal`. Beide grenzen worden bereikt — door
respectievelijk een cykel en een pad — dus geen van beide kan verbeterd worden.

## Welk algoritme

| | tijd | negatieve bogen | het best wanneer |
|---|---|---|---|
| BFS vanuit elke knoop | `O(nm)` | nee (ongewogen) | ongewogen |
| Dijkstra vanuit elke knoop | `O(nm log n)` | nee | ijl, `m ≪ n²` |
| Floyd–Warshall | `O(n³)` | ja | dicht, of negatieve bogen |
| Johnson | `O(nm log n)` | ja | ijl **én** negatieve bogen |

Het omslagpunt ligt bij `m ≈ n² / log n`. Eronder wint herhaald Dijkstra; erboven Floyd–Warshall,
dat bovendien op constanten ruim wint omdat het drie lussen over een vlakke array zijn zonder
allocatie.

Het algoritme van Johnson is het enige gat dat dit boek in kortste paden openlaat. Het herweegt de
graaf met een Bellman–Ford-potentiaal zodat alle gewichten niet-negatief worden en kortste paden
behouden blijven, en draait dan `n` keer Dijkstra. Het is het juiste antwoord voor ijle grafen met
negatieve bogen, en het is een werkelijk vernuftige truc in plaats van een routineuze combinatie —
de potentiaalfunctie is `h(v) = d(s, v)` vanuit een nieuwe knoop die met alles verbonden is op
gewicht 0, en de herwogen boog `w'(u,v) = w(u,v) + h(u) − h(v)` is niet-negatief precies omdat `h`
aan de driehoeksongelijkheid voldoet.

## Probeer het

Breek de lusvolgorde met opzet en kijk hoe vaak het zichtbaar wordt:

```bash
python -c "
import sys, random; sys.path.insert(0, '.')
from graphs.digraph import Digraph, INF, random_digraph
from graphs.paths import floyd_warshall, brute_force_shortest

def wrong(d):
    n = d.n
    dist = [[INF]*n for _ in range(n)]
    for v in range(n): dist[v][v] = 0.0
    for u, v, w in d.arcs(): dist[u][v] = min(dist[u][v], w)
    for i in range(n):          # i outermost -- the classic mistake
        for j in range(n):
            for k in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

# a plain path: the broken version gets this right
d = Digraph(4, [(0,1,1), (1,2,1), (2,3,1)])
print('path graph, 0->3:  correct', floyd_warshall(d)[0][3], ' broken', wrong(d)[0][3])

# and one where it does not
d = Digraph(4, [(0,3,2), (2,1,1), (3,0,1), (3,2,4)])
print('witness,    0->1:  correct', floyd_warshall(d)[0][1], ' broken', wrong(d)[0][1],
      ' true', brute_force_shortest(d, 0, 1))

rng = random.Random(1); bad = 0
for _ in range(4000):
    g = random_digraph(rng.randint(3, 6), 0.4, rng)
    if any(floyd_warshall(g)[i][j] != wrong(g)[i][j] for i in g.vertices() for j in g.vertices()):
        bad += 1
print(f'broken version differs on {bad}/4000 random digraphs')
"
```

```
path graph, 0->3:  correct 3  broken 3
witness,    0->1:  correct 7  broken inf
broken version differs on 942/4000 random digraphs
```

Dit is de gevaarlijke soort fout, en de getallen zeggen waarom. Op een padgraaf heeft de kapotte
versie gelijk. Op een willekeurig gekozen digraaf heeft ze ongeveer **een kwart van de tijd**
ongelijk. Een implementatie die op elke invoer faalde, zou door de eerste test die iemand schreef
gevangen worden; een die op de eenvoudige gevallen klopt en op 24% van de rest faalt, doorstaat
een met de hand gecontroleerd voorbeeld en gaat de deur uit.

Het getuigenis toont het mechanisme. De echte route `0 → 3 → 2 → 1` kost `2 + 4 + 1 = 7`. Met `i`
als buitenste lus wordt de plaats `dist[0][1]` definitief gemaakt terwijl `dist[3][1]` nog
oneindig is, omdat rij 3 nog niet verwerkt is — en niets bezoekt rij 0 ooit opnieuw. De juiste
volgorde maakt *alle* paden door knoop `k` definitief voordat ze naar `k+1` gaat, dus geen rij kan
achterblijven.

## Oefeningen

1. Wat is de looptijd van Floyd–Warshall, en welke datastructuur heeft het nodig?
2. Waarom moet de `k`-lus de buitenste zijn?
3. Wat betekent een negatieve plaats op de diagonaal van de uitvoer?
4. Geef een digraaf op twee knopen waarin `d(u,v)` eindig is en `d(v,u)` oneindig.

Oplossingen in Bijlage E.

## Kernpunten

- Floyd–Warshall induceert op *welke knopen een pad mag doorkruisen*, niet op afstand tot een
  bron. Daarom doet het alle paren tegelijk.
- `k` moet de buitenste lus zijn. Zij indexeert de inductie; `i` en `j` niet.
- `O(n³)`, negatieve bogen toegestaan, geen datastructuren. Op dichte grafen verslaat het `n`
  keer Dijkstra op zowel asymptotiek als constanten.
- Een negatieve plaats op de diagonaal betekent dat die knoop op een negatieve cykel ligt — een
  andere vraag dan Bellman–Fords "is er een bereikbaar vanuit `s`", en beide zijn het stellen
  waard.
- Ongerichte afstand is een metriek; gerichte afstand slechts een quasimetriek, en asymmetrie is
  geen randgeval.
