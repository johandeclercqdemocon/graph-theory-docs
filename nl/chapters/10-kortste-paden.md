# Hoofdstuk 10 — Kortste paden

Geef de kanten gewichten en breedte-eerst zoeken houdt op te werken. Dit hoofdstuk gaat over
waarom, wat ervoor in de plaats komt, en wat een negatief gewicht met de hele vraag doet.

## Richtingen, en waarom ze nu pas komen

Alles tot hier was ongericht. Vanaf nu heeft het boek **bogen** nodig, en de reden is
specifiek: een negatief gewicht op een ongerichte kant is betekenisloos. Je zou hem kunnen
oversteken, terugsteken, en opnieuw oversteken, en het totaal onbegrensd laten dalen. Negatieve
gewichten hebben alleen zin wanneer de kant één kant op gaat, dus zodra dit hoofdstuk ze
toelaat, moet het richting toelaten.

```python
from graphs.digraph import Digraph

d = Digraph(5, [(0,1,4), (0,2,1), (2,1,2), (1,3,1), (2,3,5), (3,4,3)])
```

Een ongerichte gewogen graaf is het bijzondere geval waarin elke boog een tweelingboog heeft.
`Digraph.of(g)` bouwt hem, en elk resultaat hieronder geldt dan onveranderd.

## Dijkstra

Houd een verzameling **afgehandelde** knopen bij waarvan de afstand definitief is. Neem
herhaaldelijk de niet-afgehandelde knoop met de kleinste voorlopige afstand, handel hem af, en
relaxeer zijn uitgaande bogen.

```python
def dijkstra(d, source):
    dist = {source: 0.0}
    heap = [(0.0, source)]
    settled = set()
    while heap:
        du, u = heapq.heappop(heap)
        if u in settled:
            continue
        settled.add(u)
        for v in d.successors(u):
            alt = du + d.weight(u, v)
            if alt < dist.get(v, INF):
                dist[v] = alt
                heapq.heappush(heap, (alt, v))
    return dist
```

```python
print(dijkstra(d, 0))    # {0: 0.0, 1: 3.0, 2: 1.0, 3: 4.0, 4: 7.0}
```

De route naar `1` kost 3 en niet de 4 van de rechtstreekse boog, want via `2` kost het `1 + 2`.

> **Stelling.** Met niet-negatieve gewichten handelt Dijkstra elke bereikbare knoop af met zijn
> werkelijke kortste afstand.

*Bewijs.* Per inductie naar de volgorde van afhandelen. Stel dat elke eerder afgehandelde knoop
zijn werkelijke afstand heeft, en zij `u` de knoop die nu afgehandeld wordt met voorlopige
waarde `du`. Elk pad van `s` naar `u` moet op enig moment de afgehandelde verzameling verlaten:
zij `xy` de eerste boog die dat doet, met `x` afgehandeld. Dat pad kost dan minstens
`dist[x] + w(x,y)`, wat minstens de voorlopige waarde van `y` is, wat minstens `du` is omdat `u`
als kleinste gekozen werd. **De laatste ongelijkheid vereist dat elk resterend booggewicht
niet-negatief is** — de rest van het pad van `y` naar `u` kan er alleen bij optellen. Dus geen
pad verslaat `du`. ∎

De voorwaarde wordt op precies één plaats gebruikt, en dat is de plaats waar ze faalt.

## Wat een negatieve boog werkelijk doet

De gebruikelijke formulering is "Dijkstra faalt op negatieve gewichten", wat waar is maar niet
informatief — en de naïeve verklaring, "zodra een knoop is afgehandeld wordt hij nooit meer
verbeterd", is niet helemaal wat er in deze implementatie gebeurt. Kijk:

```python
d = Digraph(4, [(0,1,-1), (0,2,-1), (1,3,-1), (2,1,-1)])
print(dijkstra(d, 0))          # {0: 0.0, 1: -2.0, 2: -1.0, 3: -2.0}
print(bellman_ford(d, 0)[0])   # {0: 0.0, 1: -2.0, 2: -1.0, 3: -3.0}
```

Kijk naar knoop `1`. Dijkstra meldt `-2`, en dat is **correct** — de verbetering via `2` werd
gevonden en vastgelegd. Het is knoop `3` die fout is: `-2` in plaats van `-3`.

Dat is de werkelijke faalwijze. Knoop `1` werd afgehandeld bij `-1`, en zijn bogen werden toen
gerelaxeerd. Toen de betere waarde `-2` later arriveerde, werd `dist[1]` bijgewerkt, maar `1`
zat al in `settled`, dus hem opnieuw uit de heap halen deed niets en **de verbetering plantte
zich nooit voort naar `3`**. De fout is niet dat afgehandelde knopen niet kunnen verbeteren; het
is dat hun verbetering niet kan reizen.

Dit is de kleinste graaf waarop het gebeurt — vier knopen en vier bogen, alle van gewicht `-1`,
gevonden door uitputtend zoeken en niet door constructie. De verificatie registreert het als een
stelling waarvan verwacht wordt dat ze weerlegd wordt:

```
  held      ch10  Dijkstra is correct when weights are non-negative  (120 graphs)
  refuted   ch10  Dijkstra is correct when weights may be negative  (3 graphs)
```

Merk op dat grafen die een negatieve cykel *bevatten* uit die tweede familie zijn uitgesloten.
De bewering wordt weerlegd op grafen waar een correct antwoord bestaat en Dijkstra het niet
vindt, wat een scherpere uitspraak is dan "het gaat stuk wanneer het probleem slecht gesteld is".

## Bellman–Ford

Geef het afhandelen helemaal op. Relaxeer gewoon elke boog, `n − 1` keer.

```python
def bellman_ford(d, source):
    dist = {v: INF for v in d.vertices()}
    dist[source] = 0.0
    for _ in range(d.n - 1):
        for u, v, w in d.arcs():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    for u, v, w in d.arcs():
        if dist[u] + w < dist[v]:
            return dist, True          # a negative cycle is reachable
    return dist, False
```

*Correctheid.* Na `k` ronden is `dist[v]` hoogstens het gewicht van het lichtste pad van `s` naar
`v` dat hoogstens `k` bogen gebruikt. Dat volgt meteen per inductie: ronde `k` relaxeert de
laatste boog van zo'n pad, waarvan het beginstuk door ronde `k−1` is afgehandeld. Een kortste
pad zonder negatieve cykel is enkelvoudig, gebruikt dus hoogstens `n − 1` bogen, en `n − 1`
ronden volstaan. ∎

`O(nm)`, wat veel slechter is dan Dijkstra's `O(m log n)` — de prijs voor het aankunnen van
negatieve bogen.

## Negatieve cykels

Is een negatieve cykel bereikbaar, dan bestaat er geen kortste pad: ga nog eens rond en het
totaal daalt. De vraag wordt slecht gesteld, niet slechts moeilijk.

De laatste lus van Bellman–Ford is precies de test. Na `n − 1` ronden is geen verdere verbetering
mogelijk tenzij een pad meer dan `n − 1` bogen met winst kan gebruiken, en dat vereist een
negatieve cykel.

```python
neg = Digraph(3, [(0,1,1), (1,2,-3), (2,0,1)])
print(bellman_ford(neg, 0)[1])    # True
```

De verificatie controleert dit tegen een onafhankelijke opsomming van elke enkelvoudige cykel, en
niet tegen Floyd–Warshall, dat de rekenkunde van dit boek deelt:

```
  held      ch10  Bellman-Ford flags exactly the reachable negative cycles  (300 graphs)
```

**Bereikbaar** hoort bij de uitspraak. Een negatieve cykel in een verre hoek van de graaf maakt
de afstanden vanuit `s` niet slecht gedefinieerd, en Bellman–Ford vanuit `s` negeert hem terecht.
Floyd–Warshall in hoofdstuk 11 ziet de hele graaf en beantwoordt dus een net andere vraag.

Eén gevolg is het vermelden waard, want het verklaart waarom mensen erom geven: met negatieve
bogen toegestaan is het vinden van het *kortste enkelvoudige pad* `NP`-moeilijk — een
Hamiltoniaans pad is een kortste enkelvoudig pad bij de juiste gewichten (hoofdstuk 20).
Bellman–Ford lost dat niet op. Het lost de kortste *wandeling* op, en die valt samen met het
kortste enkelvoudige pad precies wanneer geen negatieve cykel bereikbaar is.

## Kiezen

| Situatie | Gebruik | Kosten |
|---|---|---|
| Ongewogen | BFS | `O(n + m)` |
| Niet-negatieve gewichten | Dijkstra | `O(m log n)` |
| Willekeurige gewichten, één bron | Bellman–Ford | `O(nm)` |
| Willekeurige gewichten, alle paren | Floyd–Warshall (h. 11) | `O(n³)` |
| Negatieve cykel bereikbaar | geen — de vraag is slecht gesteld | — |

BFS is Dijkstra met alle gewichten gelijk aan 1, en de prioriteitswachtrij valt terug op een
gewone wachtrij omdat de invariant uit hoofdstuk 8 — hoogstens twee opeenvolgende
afstandswaarden onderweg — weer geldt.

## Probeer het

Kijk hoe de verbetering zich niet voortplant, knoop voor knoop:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.digraph import Digraph
from graphs.paths import dijkstra, bellman_ford, brute_force_shortest
d = Digraph(4, [(0,1,-1), (0,2,-1), (1,3,-1), (2,1,-1)])
dj = dijkstra(d, 0)
bf = bellman_ford(d, 0)[0]
for t in range(4):
    print(f'  to {t}: dijkstra={dj[t]:>5}  bellman={bf[t]:>5}  true={brute_force_shortest(d,0,t):>5}')
"
```

```
  to 0: dijkstra=  0.0  bellman=  0.0  true=  0.0
  to 1: dijkstra= -2.0  bellman= -2.0  true=   -2
  to 2: dijkstra= -1.0  bellman= -1.0  true=   -1
  to 3: dijkstra= -2.0  bellman= -3.0  true=   -3
```

Drie van de vier zijn juist. Alleen de knoop *stroomafwaarts* van de late verbetering is fout, en
daarom is deze fout makkelijk te missen op een graaf die je niet uitputtend hebt gecontroleerd.

## Oefeningen

1. Dijkstra's bewijs gebruikt niet-negativiteit in precies één ongelijkheid. Welke?
2. Wat is de looptijd van Bellman–Ford, en waarom is die slechter dan die van Dijkstra?
3. Wat detecteert de `n`-de relaxatieronde van Bellman–Ford?
4. Een negatieve cykel is bereikbaar vanuit `s`. Wat is de kortste wandeling van `s` naar een
   knoop op die cykel?

Oplossingen in Bijlage E.

## Kernpunten

- Negatieve gewichten dwingen richting af, en daarom stapt het boek hier over op gerichte grafen.
- Dijkstra's bewijs gebruikt niet-negativiteit in precies één ongelijkheid, en dat is precies waar
  het breekt.
- Dijkstra's werkelijke falen is niet dat afgehandelde knopen nooit verbeteren — dat kunnen ze —
  maar dat de verbetering zich niet voorbij hen kan voortplanten. Het kleinste getuigenis heeft
  vier knopen.
- Bellman–Ford relaxeert alles `n − 1` keer, hanteert negatieve bogen in `O(nm)`, en zijn `n`-de
  ronde is precies een test op een bereikbare negatieve cykel.
- Met een bereikbare negatieve cykel bestaat er geen kortste wandeling. Kortste *enkelvoudige*
  paden met negatieve gewichten is `NP`-moeilijk, en geen algoritme hier probeert het.
