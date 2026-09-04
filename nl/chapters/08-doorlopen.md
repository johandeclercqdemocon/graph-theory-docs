# Hoofdstuk 8 — Doorlopen

Breedte-eerst en diepte-eerst zoeken bezoeken dezelfde knopen in `O(n + m)` tijd. Ze verschillen
alleen in welke knoop ze als volgende nemen — een wachtrij tegenover een stapel — en dat ene
verschil geeft ze volstrekt verschillende toepassingen.

## De twee volgordes

```python
from graphs.core import Graph
from graphs.algorithms import bfs_order, dfs_order, distances

g = Graph(6, [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (4, 5)])
print(bfs_order(g, 0))    # [0, 1, 2, 3, 4, 5]
print(dfs_order(g, 0))    # [0, 1, 3, 2, 4, 5]
print(distances(g, 0))    # {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 4}
```

Breedte-eerst bezoekt `2` vóór `3`, omdat `2` dichter bij de bron ligt. Diepte-eerst bezoekt `3`
vóór `2`, omdat het het eerste pad zo ver mogelijk volgt voordat het terugkeert. Beide kosten
`O(n + m)`: elke knoop komt één keer in de houder, en elke kant wordt twee keer bekeken — één
keer vanaf elk eindpunt.

Het enige structurele verschil in de code is de houder:

```python
queue.popleft()   # BFS: first in, first out
stack.pop()       # DFS: last in, first out
```

Merk op dat `dfs_order` hier **iteratief** is. De recursieve versie is korter en is wat de
meeste teksten afdrukken, maar de standaardrecursielimiet van Python is 1000, dus een padgraaf
op tienduizend knopen laat haar crashen. De iteratieve versie kent die grens niet, en dit boek
gebruikt haar overal.

## Waarom breedte-eerst kortste paden vindt

De correctheid van BFS is het enige in dit hoofdstuk dat werkelijk bewijs vergt.

> **Stelling.** BFS vanuit `s` kent elke bereikbare `v` de waarde `d(s, v)` toe, de lengte van
> een kortste pad.

*Bewijs.* Zij `dist[v]` de waarde die BFS toekent. We tonen `dist[v] = d(s,v)` per inductie naar
`d(s,v)`.

Ten eerste geldt altijd `dist[v] ≥ d(s,v)`, want BFS zet `dist[w] = dist[v] + 1` alleen wanneer
`vw` een kant is, dus de toegekende waarden tekenen een werkelijke wandeling vanaf `s` uit.

Voor de andere richting: stel `d(s,v) = k` en dat elke knoop op werkelijke afstand `< k` correct
gelabeld is. Neem een kortste `s`–`v`-pad en zij `u` de knoop ervoor op dat pad, dus
`d(s,u) = k−1` en per inductie `dist[u] = k−1`. De wachtrij wordt in niet-dalende volgorde van
`dist` verwerkt — dat is de invariant die BFS laat werken, en ze geldt omdat we alleen waarden
toevoegen die één groter zijn dan de waarde die verwerkt wordt. Dus `u` verlaat de rij voordat
enige knoop van afstand `k` of meer verwerkt wordt, en op dat moment is `v` ofwel al gelabeld met
iets `≤ k`, ofwel krijgt hij `k`. Hoe dan ook `dist[v] ≤ k`. ∎

De invariant — **de wachtrij bevat op elk moment hoogstens twee verschillende afstandswaarden,
en die zijn opeenvolgend** — is het ding om te onthouden. Ze faalt zodra kanten verschillende
gewichten hebben, en dat is precies waarom hoofdstuk 10 Dijkstra en een prioriteitswachtrij
nodig heeft in plaats van een gewone rij.

De verificatie controleert de stelling tegen uitputtend opgesomde paden en niet tegen een tweede
kortstepadroutine:

```
  held      ch 8  BFS distances equal true shortest-path lengths  (52 graphs)
  held      ch 8  DFS and BFS reach exactly the same vertices  (52 graphs)
```

## Zoekbomen, en de kanten die ze achterlaten

Beide zoekmethoden bouwen een **zoekboom**: onthoud voor elke knoop behalve de bron de kant
waarlangs hij het eerst ontdekt werd. Omdat elke knoop precies één keer ontdekt wordt, zijn dat
`n − 1` kanten op een samenhangende graaf, en hij is samenhangend, dus het is een opspannende
boom — de bestaansstelling van hoofdstuk 7, nu constructief gemaakt.

Elke kant van de graaf is vervolgens ofwel een **boomkant** ofwel niet. De kanten die het niet
zijn classificeren is waar de twee zoekmethoden het scherpst uiteenlopen, en het is de grondslag
van hoofdstuk 12.

Voor **diepte-eerst op een ongerichte graaf** is elke niet-boomkant een **terugkant**: ze
verbindt een knoop met een van zijn eigen voorouders in de boom.

*Bewijs.* Beschouw een kant `uv` en stel dat `u` het eerst ontdekt wordt. DFS keert niet terug
uit `u` voordat elke knoop die via onbezochte knopen vanuit `u` bereikbaar is, afgehandeld is —
in het bijzonder wordt `v` ontdekt tijdens de verkenning van `u`, dus `v` is een afstammeling van
`u`. Dus `uv` verbindt een knoop met een voorouder. ∎

**Er zijn geen kruiskanten in ongericht DFS.** Dat is een sterke uitspraak, en ze maakt DFS het
juiste gereedschap om bruggen, snijknopen en biconnexe componenten te vinden: de enige manier om
"boven" je huidige positie te komen is een terugkant, dus bijhouden welke hoogste voorouder vanuit
elke deelboom bereikbaar is, vertelt je precies welke boomkanten bruggen zijn. Hoofdstuk 12 bouwt
dat algoritme.

Voor **breedte-eerst op een ongerichte graaf** gaat het overeenkomstige feit over niveaus: elke
kant verbindt knopen waarvan de afstanden tot de bron **hoogstens één** verschillen. Een kant naar
een knoop twee niveaus lager zou het pad hebben verkort. Elke niet-boomkant ligt dus ofwel binnen
een niveau ofwel tussen opeenvolgende niveaus — en een kant *binnen* een niveau is precies een
oneven cykel die erop wacht gevonden te worden, wat het tweekleuringsalgoritme van hoofdstuk 16
is.

## Welke je gebruikt

| Probleem | Zoekmethode | Waarom |
|---|---|---|
| Kortste paden, ongewogen | BFS | De niveau-invariant ís de afstand |
| Samenhangscomponenten | beide | Beide bereiken dezelfde verzameling |
| Bipartietheid / oneven cykel | BFS | Een kant binnen een niveau benoemt de oneven cykel |
| Bruggen, snijknopen | DFS | Geen kruiskanten, dus terugkanten vertellen alles |
| Topologische ordening (gericht) | DFS | Afhandelvolgorde, omgekeerd |
| Cykeldetectie | beide | Een terugkant in DFS; een kant binnen of terug in BFS |

Het enige geval waarin de keuze een fout is in plaats van een voorkeur, is kortste paden. DFS
vindt *een* pad, en mensen gebruiken het daar ook voor, maar het pad dat het vindt kan willekeurig
veel langer zijn dan het kortste — op een graaf met een lange omweg neemt DFS die vrolijk.

## Probeer het

Kijk hoe DFS een pad teruggeeft dat veel langer is dan het kortste, op een graaf die ontworpen is
om het te misleiden:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import Graph
from graphs.algorithms import bfs_order, dfs_order, distances
# 0 and 7 are adjacent; there is also a long way round through 1..6
g = Graph(8, [(0,7)] + [(i, i+1) for i in range(7)])
print('bfs order:', bfs_order(g, 0))
print('dfs order:', dfs_order(g, 0))
print('true distance 0 to 7:', distances(g, 0)[7])
print('position of 7 in dfs:', dfs_order(g, 0).index(7))
"
```

```
bfs order: [0, 1, 7, 2, 6, 3, 5, 4]
dfs order: [0, 1, 2, 3, 4, 5, 6, 7]
true distance 0 to 7: 1
position of 7 in dfs: 7
```

BFS bereikt knoop 7 als tweede, omdat hij één stap verwijderd is. DFS bereikt hem als laatste, na
eerst de hele omweg van zeven kanten te hebben afgelegd. Beide zijn correcte doorlopen; slechts
één ervan weet iets over afstand.

## Oefeningen

1. Je hebt kortste paden nodig in een ongewogen graaf. BFS of DFS, en waarom is de andere fout in
   plaats van slechts trager?
2. Wat is de looptijd van beide zoekmethoden, en waarom is die dezelfde?
3. In een BFS vind je een kant tussen twee knopen in hetzelfde niveau. Wat heb je gevonden?
4. Waarom schrijft dit boek DFS iteratief in plaats van recursief?

Oplossingen in Bijlage E.

## Kernpunten

- BFS en DFS verschillen alleen door wachtrij tegenover stapel, en beide lopen in `O(n + m)`.
- BFS berekent exacte kortstepadafstanden op ongewogen grafen. De invariant is dat de wachtrij
  hoogstens twee opeenvolgende afstandswaarden bevat — en dat is precies wat ongelijke
  kantgewichten kapotmaken, waarom hoofdstuk 10 bestaat.
- Beide bouwen opspannende bomen, wat de bestaansstelling van hoofdstuk 7 constructief maakt.
- Ongericht DFS heeft **geen kruiskanten**: elke niet-boomkant is een terugkant. Dat maakt het tot
  het gereedschap voor bruggen en snijknopen.
- Ongericht BFS legt elke kant binnen een niveau of tussen opeenvolgende niveaus. Een kant binnen
  een niveau is een oneven cykel.
- Schrijf DFS iteratief. De recursieve vorm sterft aan de grens van 1000 frames van Python op een
  graaf die enkel lang is.
