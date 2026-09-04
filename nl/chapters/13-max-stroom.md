# Hoofdstuk 13 — Max-stroom min-snede

Dit is de stelling waar het vorige hoofdstuk naar doorverwees, en die waar het volgende zich toe
herleidt. Het is het centrale algoritmische resultaat in de grafentheorie, en het bewijs is korter
dan zijn reputatie doet vermoeden.

## De opzet

Een **stroomnetwerk** is een digraaf met een niet-negatieve **capaciteit** `c(u,v)` op elke boog,
een **bron** `s`, en een **put** `t`. Een **stroom** `f` kent elke boog een waarde toe met

- **capaciteit**: `0 ≤ f(u,v) ≤ c(u,v)`;
- **behoud**: voor elke `v` behalve `s` en `t` is de instroom gelijk aan de uitstroom.

De **waarde** van een stroom is de netto hoeveelheid die `s` verlaat. Een **snede** is een
verdeling `(S, T)` met `s ∈ S` en `t ∈ T`; haar **capaciteit** is de totale capaciteit van bogen
van `S` naar `T`. Bogen die van `T` naar `S` teruglopen dragen niets bij — een punt dat makkelijk
verkeerd gaat en waarvan het bewijs hieronder afhangt.

Opnieuw zwakke dualiteit, en opnieuw gratis:

> **Lemma.** De waarde van elke stroom is hoogstens de capaciteit van elke snede.

*Bewijs.* Alle stroom die `s` verlaat moet uiteindelijk van `S` naar `T` oversteken, en de
overstekende bogen dragen hoogstens hun capaciteit. ∎

## Het restnetwerk, en waarom omkeringen ertoe doen

Het algoritme luidt: zoek een pad van `s` naar `t` met vrije capaciteit, duw er zoveel doorheen als
het aankan, herhaal. Naïef uitgevoerd loopt dit vast — een vroege gulzige keuze kan een betere
latere blokkeren.

De oplossing is het **restnetwerk**. Houd naast elke boog `(u,v)` die `f` draagt een omgekeerde
boog `(v,u)` bij met restcapaciteit `f`. Stroom langs de omgekeerde boog duwen *annuleert* stroom
op de voorwaartse.

```python
def add_arc(self, u, v, c):
    self.cap[(u, v)] = self.cap.get((u, v), 0.0) + c
    self.cap.setdefault((v, u), 0.0)      # the reverse arc, initially empty
```

Die ene regel is wat de hele methode laat werken. Zonder omgekeerde bogen kan het algoritme geen
beslissing herzien, en gulzig paden duwen is dan werkelijk fout. Mét ze leidt elk vermeerderend pad
ofwel nieuwe stroom ofwel *herleidt* het oude stroom, en de zoektocht hoeft nooit terug te keren.

Een **vermeerderend pad** is een willekeurig `s`–`t`-pad in het restnetwerk. Het algoritme — de
**methode van Ford–Fulkerson** — is: vermeerder tot er geen meer bestaat.

## Edmonds–Karp

Ford–Fulkerson zegt niet welk vermeerderend pad je moet nemen, en die keuze doet meer terzake dan
het lijkt. Neem ze willekeurig, en op een netwerk met irrationale capaciteiten kan de methode
eeuwig doorlopen en naar een waarde onder het maximum convergeren. Met gehele capaciteiten
termineert ze, maar ze kan tijd kosten evenredig met de *waarde* van de stroom, wat exponentieel is
in de invoergrootte.

**Neem kortste vermeerderende paden** — BFS, geen DFS — en het wordt Edmonds–Karp, met looptijd
`O(n m²)` ongeacht de capaciteiten. De grens volgt uit het feit dat de BFS-afstand van `s` naar `t`
in het restnetwerk nooit daalt en na elke `O(m)` vermeerderingen strikt moet stijgen.

```python
def _shortest_augmenting_path(self, residual, source, sink):
    parent = {source: source}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in self.adj[u]:
            if v not in parent and residual.get((u, v), 0.0) > 1e-12:
                parent[v] = u
                if v == sink:
                    return parent
                queue.append(v)
    return None
```

De keuze van houder is het hele verschil tussen een algoritme met een polynomiale grens en een
zonder. Het is hetzelfde onderscheid tussen `deque` en stapel als in hoofdstuk 8, en hier doet het
meer terzake.

## De stelling

> **Stelling (Ford–Fulkerson, Elias–Feinstein–Shannon, 1956).** De maximale stroomwaarde is gelijk
> aan de minimale snedecapaciteit.

*Bewijs.* Zwakke dualiteit geeft `max ≤ min`. Voor de omgekeerde richting: laat het algoritme
volledig aflopen en zij `S` de verzameling knopen die vanuit `s` bereikbaar zijn in het uiteindelijke
restnetwerk. Dan geldt `t ∉ S`, want anders zou er nog een vermeerderend pad zijn. Dus `(S, T)` is
een snede.

Elke boog van `S` naar `T` is **verzadigd** — had ze vrije restcapaciteit, dan zou haar kop in `S`
liggen. Elke boog van `T` naar `S` draagt **nul** stroom — droeg ze iets, dan zou haar omgekeerde
restboog haar staart in `S` plaatsen.

Dus de netto stroom over de snede is gelijk aan de totale capaciteit van de snede, en de waarde van
de stroom is daaraan gelijk. Deze stroomwaarde is dus gelijk aan deze snedecapaciteit, en per zwakke
dualiteit zijn beide optimaal. ∎

Het bewijs is constructief: het beweert niet slechts dat er een passende snede bestaat, het
overhandigt er een. Dat is wat `min_cut` teruggeeft, en de verificatie controleert de constructie
apart van het getal, want het zijn verschillende beweringen:

```
  held      ch13  Max-flow equals min-cut  (80 graphs)
  held      ch13  The cut the algorithm reports really has the flow's value  (80 graphs)
  held      ch13  Integer capacities give an integer maximum flow  (80 graphs)
```

De tweede regel is niet overbodig. Een correcte maximale waarde met een verkeerd uitgelezen snede is
een plausibele fout, en alleen het getal controleren zou haar missen.

## Geheeltalligheid

> **Gevolg.** Zijn alle capaciteiten geheel, dan is een maximale stroom geheel.

*Bewijs.* Elke vermeerdering duwt de flessenhals van het pad, die geheel is wanneer alle
restcapaciteiten dat zijn. Per inductie blijven ze de hele tijd geheel. ∎

Dit gevolg is de reden dat stroom überhaupt combinatorische problemen oplost. Menger in hoofdstuk 12
en koppeling in hoofdstuk 14 hebben allebei nodig dat het antwoord een *verzameling paden* of een
*verzameling kanten* is en geen fractionele toewijzing — en geheeltalligheid is wat belooft dat het
optimum als zodanig afgelezen kan worden. Een lineair programma met dezelfde beperkingen zou je
`0,5` op drie bogen geven en geen manier om af te ronden.

```python
net = FlowNetwork(6, [(0,1,16), (0,2,13), (1,2,10), (2,1,4), (1,3,12),
                      (3,2,9), (2,4,14), (4,3,7), (3,5,20), (4,5,4)])
print(net.max_flow(0, 5)[0])           # 23.0
print(sorted(net.min_cut(0, 5)[1]))    # [0, 1, 2, 4]
```

De snede `{0,1,2,4}` tegenover `{3,5}` heeft capaciteit `12 + 7 + 4 = 23`. Merk op dat de boog
`(3,2)` met capaciteit 9 *achterwaarts* over deze snede loopt en niets bijdraagt — het punt dat aan
het begin van dit hoofdstuk werd aangestipt.

## Waartoe het zich herleidt

Stroom is het werkpaard van de combinatorische optimalisatie omdat zoveel problemen het in vermomming
zijn:

| Probleem | Codering |
|---|---|
| Menger, kantvorm | eenheidscapaciteiten (h. 12) |
| Menger, knoopvorm | eenheidscapaciteiten + knoopsplitsing (h. 12) |
| Bipartiete koppeling | bron → links → rechts → put, alles eenheid (h. 14) |
| Knoopdisjuncte routering | knoopsplitsing |
| Projectselectie, beeldsegmentatie | min-snede rechtstreeks |
| Honkbaleliminatie | max-stroom-haalbaarheid |

De vaardigheid die de moeite waard is, is niet Edmonds–Karp implementeren — je gebruikt een
bibliotheek — maar herkennen dat een probleem *een* stroomprobleem is, en dat is meestal een kwestie
van vragen wat de capaciteiten zouden moeten zijn.

## Probeer het

Kijk hoe een omgekeerde boog zijn werk doet. Eerst een netwerk waarin het gulzige eerste pad een
vergissing is:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.flow import FlowNetwork
# 0->1->3 and 0->2->3, plus a crossing arc 1->2
net = FlowNetwork(4, [(0,1,1), (0,2,1), (1,2,1), (1,3,1), (2,3,1)])
v, residual = net.max_flow(0, 3)
print('max flow:', v, ' min cut:', net.brute_force_min_cut(0, 3))
print('flow on the crossing arc 1->2:', net.cap[(1,2)] - residual[(1,2)])
"
```

```
max flow: 2.0  min cut: 2.0
flow on the crossing arc 1->2: 0.0
```

Het maximum is 2 — één eenheid langs elke zijde — en de kruisende boog draagt uiteindelijk niets.
Edmonds–Karp vindt dit meteen omdat BFS eerst de paden van twee bogen neemt. Ford–Fulkerson dat
eerst het pad `0→1→2→3` van drie bogen zou nemen, zou het via de omgekeerde boog moeten *terugdraaien*
— precies de situatie waarvoor omgekeerde bogen bestaan.

## Oefeningen

1. Waarom heeft het restnetwerk omgekeerde bogen nodig? Wat gaat er zonder stuk?
2. Ford–Fulkerson bepaalt niet welk vermeerderend pad je neemt. Wat gaat er mis wanneer je slecht
   kiest?
3. Formuleer het geheeltalligheidsgevolg en leg uit waarom het stroom bruikbaar maakt voor
   combinatorische problemen.
4. Een boog loopt van de putzijde terug naar de bronzijde van een snede. Hoeveel draagt ze bij aan
   de capaciteit van de snede?

Oplossingen in Bijlage E.

## Kernpunten

- Max-stroom is gelijk aan min-snede, en het bewijs is constructief: de in het restnetwerk bereikbare
  verzameling van het verzadigde netwerk *is* een minimale snede.
- Omgekeerde restbogen zijn het mechanisme. Zonder ze kan gulzige vermeerdering een beslissing niet
  herzien en is ze eenvoudigweg fout.
- Ford–Fulkerson bepaalt niet welk vermeerderend pad. Kortste nemen (BFS) geeft Edmonds–Karp en
  `O(n m²)`; willekeurige nemen kan op irrationale capaciteiten niet termineren.
- Gehele capaciteiten geven een geheel optimum. Dat gevolg is waarom stroom combinatorische en niet
  slechts numerieke problemen oplost.
- Bogen die vanaf de putzijde terugkruisen dragen nul bij aan de capaciteit van een snede.
