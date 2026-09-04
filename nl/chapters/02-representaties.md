# Hoofdstuk 2 — Representaties

Een graaf is een abstract object. Een graaf in het geheugen is een concreet object, en het
gat daartussen is waar elk algoritme in dit boek zijn looptijd vandaan haalt.

Er zijn drie standaardmanieren om een graaf op te slaan, en de schoolboekvergelijking ertussen
is een tabel met asymptotiek. Dit hoofdstuk geeft je die tabel, meet haar vervolgens, en de
meting spreekt de tabel op drie plaatsen tegen. Alle drie de tegenspraken zijn eerlijk — de
asymptotiek klopt, en ze is óók niet wat er gebeurt bij de omvang waarop je werkelijk draait.

## De drie representaties

**Kantenlijst.** Sla de paren op en verder niets. `O(m)` ruimte, en elke vraag behalve "hoeveel
kanten" vereist een scan. Het is de juiste keuze voor invoer, uitvoer, en niets anders. Het
algoritme van Kruskal in hoofdstuk 9 is de enige plaats in dit boek waar het echt de
natuurlijke structuur is, omdat dat algoritme als eerste daad de kanten toch al sorteert.

**Adjacentielijst.** Voor elke knoop de verzameling van zijn buren. `O(n + m)` ruimte. Eén
knoops buren aflopen kost `O(deg(v))` — optimaal, want dat is de grootte van het antwoord.
Vragen of een specifieke kant bestaat kost `O(deg(v))` in een gelinkte lijst, of `O(1)`
verwacht in een hashverzameling, en dat laatste gebruikt `graphs.core.Graph`.

**Adjacentiematrix.** Een `n × n` array van bits, symmetrisch voor een ongerichte graaf.
`O(n²)` ruimte, ongeacht hoe weinig kanten er zijn. Kantvragen zijn één array-index. Eén
knoops buren aflopen kost `O(n)`, want je moet elke plaats in de rij bekijken, ook de nullen.

```python
from graphs.core import Graph
from graphs.matrix import MatrixGraph

g = Graph(4, [(0, 1), (1, 2), (2, 3)])
mg = MatrixGraph.of(g)
print(g.has_edge(0, 1), mg.has_edge(0, 1))     # True True
print(sorted(g.neighbours(1)), sorted(mg.neighbours(1)))   # [0, 2] [0, 2]
```

`MatrixGraph` slaat elke rij op als één Python-geheel getal dat als bitmasker dienstdoet. Die
keuze maakt de metingen hieronder interessant, en wordt aan het eind eerlijk besproken.

De tabel die iedereen opschrijft:

| | kantenlijst | adjacentielijst | adjacentiematrix |
|---|---|---|---|
| ruimte | `O(m)` | `O(n + m)` | `O(n²)` |
| `has_edge(u, v)` | `O(m)` | `O(1)` verwacht | `O(1)` |
| `N(v)` aflopen | `O(m)` | `O(deg v)` | `O(n)` |
| kant toevoegen | `O(1)` | `O(1)` | `O(1)` |

Meet het nu.

## Wat er werkelijk gebeurt

```bash
python scripts/bench_representations.py
```

```
n = 600, times in microseconds per operation, best of 3

   density        m         edge query        scan neighbours    count triangles
                        list   matrix        list    matrix     list  matrix
      0.01     1800     0.088    0.180         0.2      54.6        6      56
      0.05     8958     0.089    0.189         0.5      57.1       55      65
      0.20    35872     0.095    0.202         1.3      62.7      796      89
      0.50    89755     0.104    0.202         2.7      69.3     6619     138
```

Absolute tijden horen bij deze machine en verschuiven enkele procenten tussen runs; de
verhoudingen zijn stabiel. Drie dingen hier zijn niet wat de tabel voorspelt.

**De adjacentielijst wint de kantvraag, bij elke dichtheid.** De tabel zegt dat beide `O(1)`
zijn; de meting zegt dat de lijst ongeveer twee keer zo snel is. Een gehashte
lidmaatschapstest is werkelijk één hash en één probe. De `rows[u] >> v & 1` van de matrix is
geen enkele machine-instructie, want `rows[u]` is een Python-geheel getal van willekeurige
precisie, en het naar rechts schuiven ervan met `v` raakt elk 30-bits cijfer onder `v`. De
kantvraag van de matrix is `O(n)` in vermomming.

Dat is een bewering over schaalgedrag, dus die vraagt om een schaalmeting in plaats van een
bewering:

```
  edge query as n grows, p = 0.05 fixed:

      n  bits/row     list   matrix  ratio
     64        64    0.084    0.144  1.72x
    256       256    0.093    0.163  1.76x
   1024      1024    0.098    0.199  2.02x
   4096      4096    0.106    0.267  2.52x
  16384     16384    0.118    0.674  5.70x
```

De kosten van de lijst zijn vlak — `0,084` tot `0,118` microseconde over een 256-voudige
toename van `n`. Die van de matrix groeien gestaag, en bij `n = 16384` is de structuur met
"constante tijd" **ongeveer 6 keer trager dan die met "lineaire tijd"** bij precies de operatie
die ze had moeten winnen.

Houd de dichtheid vast wanneer je dit probeert. De eerste versie van deze meting liet `p` per
ongeluk met `n` meevariëren, waardoor de grote grafen bijna leeg waren; de rijen waren toen
kleine gehele getallen, de schuifoperatie was goedkoop, en de tijden kwamen er vlak uit. Het
effect verdween volledig en de verkeerde conclusie leek goed onderbouwd. Wat de rijen duur
maakt is de positie van het *hoogste* gezette bit, niet hoeveel bits gezet zijn.

**De matrix wint het tellen van driehoeken met een factor 48, en met meer naarmate de
dichtheid stijgt.** Dit is de operatie waarvoor een matrix bestaat. Driehoeken door een knoop
tellen betekent buurverzamelingen snijden, en twee bitmaskers snijden is `&` — 64 knopen per
machinewoord, zonder enige interpreteroverhead per element:

```python
def common_neighbours(self, u: int, v: int) -> int:
    return (self.rows[u] & self.rows[v]).bit_count()
```

Bij `p = 0,5` is dat 138 microseconden tegen 6619 voor de lijst. Het geheel getal van
willekeurige precisie dat kantvragen traag maakte, is precies wat dit snel maakt: het werk
gebeurt binnen één C-operatie in plaats van binnen een Python-lus. Hoofdstuk 21 gebruikt dit,
en het is het verschil tussen een kliekzoektocht die eindigt en een die dat niet doet.

**De matrix gebruikt 22 keer minder geheugen dan de lijst, op een ijle graaf.**

```
  memory, n = 600, p = 0.05:
    adjacency list  1,344,576 bytes
    bitset matrix      61,704 bytes
```

`O(n²)` dat `O(n + m)` met een factor twintig verslaat lijkt onmogelijk, en de asymptotiek is
niet fout — ze is bij `n = 600` alleen niet de baas. Een Python-`set` draagt ruwweg twee
kilobyte overhead voordat hij iets bevat, en er zijn er 600. Een geheel getal van 600 bits is
ongeveer 100 byte. Het omslagpunt waar `O(n²)` werkelijk verliest ligt ver rechts van de
meeste grafen die je tegenkomt, en heb je ooit een adjacentielijst gekozen "om geheugen te
besparen" op een graaf van een paar duizend knopen, dan is het de moeite waard te meten wat
je bespaarde.

## De tegenspraak juist lezen

Niets hiervan maakt de asymptotische tabel onjuist. Het maakt haar onvolledig op een
specifieke manier, en de specifieke punten doen ertoe:

- De trage kantvraag van de matrix is een feit over **een rij coderen als één groot geheel
  getal**. Een echte bitset — numpy, C, of `bitarray` — indexeert direct het bevattende woord
  en is werkelijk `O(1)`. Neem je één implementatieles mee uit dit hoofdstuk, dan deze: "bitset"
  en "Python-geheel-getal-als-bitset" hebben verschillende complexiteit, en maar één van beide
  komt overeen met het schoolboek.
- De geheugenkosten van de lijst zijn een feit over **de overhead van Python-verzamelingen**,
  niet over adjacentielijsten. In C zou een adjacentielijst bij `p = 0,05` werkelijk kleiner
  zijn.
- De winst van de matrix bij driehoeken tellen is **geen** artefact. Het is het echte
  asymptotische voordeel — `n/64` woorden in plaats van `deg(v)` geïnterpreteerde operaties —
  en het blijft in elke taal overeind.

De algemene les is de les die dit boek zal herhalen: een asymptotische grens vertelt je de
vórm van een kromme, niet haar positie. Twee `O(1)`-operaties kunnen zesvoudig verschillen, en
welke wint kan omkeren naarmate `n` groeit.

## Kiezen

Gebruik voor alles in deel I tot en met III de adjacentielijst. Doorlopen, kortste paden,
stromen en koppelingen zijn allemaal `O(n + m)` of erger in `m`, en ze lopen allemaal
buurverzamelingen af, wat de beste operatie van de lijst is en de slechtste van de matrix met
twee ordes van grootte.

Grijp naar een matrix wanneer je **verzamelingsoperaties op buurverzamelingen** doet —
driehoeken tellen, kliekzoektocht (hoofdstuk 21), gemeenschappelijke-buurgelijkenis — of
wanneer de graaf werkelijk dicht is, dat wil zeggen `m` een constante fractie van `n²` is en
niet slechts groot.

Grijp naar een kantenlijst wanneer de kanten het onderwerp zijn: ze sorteren (hoofdstuk 9), ze
streamen, of ze naar schijf schrijven.

## Probeer het

Kijk hoe de twee representaties het oneens zijn over wie sneller is, op dezelfde graaf, enkel
afhankelijk van de gestelde vraag:

```bash
python -c "
import sys, time, random
sys.path.insert(0, '.')
from graphs.generate import random_graph
from graphs.matrix import MatrixGraph
g = random_graph(800, 0.3, random.Random(1))
mg = MatrixGraph.of(g)

t = time.perf_counter(); sum(1 for _ in g.neighbours(5)); scan_list = time.perf_counter() - t
t = time.perf_counter(); sum(1 for _ in mg.neighbours(5)); scan_mat = time.perf_counter() - t
print(f'scan one neighbourhood: list {scan_list*1e6:.0f}us, matrix {scan_mat*1e6:.0f}us')

t = time.perf_counter(); mg.common_neighbours(5, 6); tri_mat = time.perf_counter() - t
t = time.perf_counter(); len(g.neighbours(5) & g.neighbours(6)); tri_list = time.perf_counter() - t
print(f'intersect two:          list {tri_list*1e6:.0f}us, matrix {tri_mat*1e6:.0f}us')
"
```

De eerste regel bevoordeelt de lijst met ruime marge en de tweede de matrix. Geen van beide
representaties is beter; ze beantwoorden verschillende vragen goed, en de enige manier om te
weten welke je nodig hebt, is weten welke vraag je stelt.

## Oefeningen

1. Hoeveel kanten zijn er gemiddeld bij `n = 1000` en `p = 0,01`, en hoeveel plaatsen heeft de
   adjacentiematrix?
2. Welke representatie zou je kiezen om driehoeken door een gegeven knoop te tellen, en waarom?
3. `MatrixGraph.has_edge` ziet eruit als een bittest in constante tijd. Leg uit waarom dat in
   deze implementatie niet zo is.
4. In de code van dit boek gebruikte de bitsetmatrix bij `n = 600` *minder* geheugen dan de
   adjacentielijst. Geef de reden, en zeg of dat in C ook zou gelden.

Oplossingen in Bijlage E.

## Kernpunten

- Kantenlijst voor invoer en uitvoer, adjacentielijst voor doorlopen, adjacentiematrix voor
  verzamelingsoperaties op buren en voor dichte grafen.
- `n` en `m` begrenzen alles, maar constanten bepalen echte programma's. De `O(1)`-kantvraag
  van de matrix mat ongeveer 6 keer trager dan die van de lijst bij `n = 16384`, want een
  Python-geheel getal is geen machinewoord.
- De matrix versloeg de lijst op geheugen met een factor 22 bij `n = 600`. `O(n²)` betekent
  niet "groot" bij de omvang die de meeste grafen werkelijk hebben.
- Buurverzamelingen snijden met bitmaskers is de enige echte, taalonafhankelijke asymptotische
  winst, en hoofdstuk 21 hangt ervan af.
- Spreekt een meting een grens tegen, houd dan de andere variabelen vast en meet opnieuw
  voordat je een van beide gelooft. De dichtheid met `n` laten meevariëren verborg het
  belangrijkste effect van dit hoofdstuk volledig.
