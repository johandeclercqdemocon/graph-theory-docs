# Hoofdstuk 23 — Leven met hardheid

`NP`-moeilijk is niet het einde van het gesprek. Er zijn drie eerlijke antwoorden — een benaderend
antwoord aanvaarden met een *bewezen* factor, exponentiële tijd aanvaarden in een parameter die klein
blijft, of je beperken tot een grafenklasse waar het probleem eenvoudig is — en dit hoofdstuk gaat
over de keuze ertussen.

## Benaderen met garantie

Een algoritme is een **`ρ`-benadering** voor een minimalisatieprobleem wanneer het altijd een
oplossing teruggeeft met kosten hoogstens `ρ · OPT`. Het woord dat telt is *altijd*: een factor is een
bewezen grens voor het slechtste geval, geen waargenomen gemiddelde.

Het standaardvoorbeeld is prachtig grof.

> **Stelling.** Beide eindpunten nemen van elke kant van een **maximale** koppeling geeft een
> knopenoverdekking van grootte hoogstens `2 · OPT`.

```python
def vertex_cover_2approx(g):
    cover = set()
    for u, v in g.edges():
        if u not in cover and v not in cover:
            cover.add(u); cover.add(v)
    return cover
```

*Bewijs.* Zij `M` de gebouwde koppeling. Haar kanten zijn paarsgewijs disjunct, dus elke
knopenoverdekking heeft minstens één knoop uit elk nodig: `OPT ≥ |M|`. Het algoritme geeft `2|M|`
terug. Bovendien is `M` *maximaal* — er kan geen kant bij — dus elke kant van `G` raakt een gekoppelde
knoop, en het resultaat is werkelijk een overdekking. ∎

Twee dingen over dit bewijs. Het berekent `OPT` nooit, het begrenst het alleen van onderaf; zo werkt
elk benaderingsbewijs. En het heeft alleen een **maximale** koppeling nodig, geen **maximum**
koppeling — gulzig volstaat, dus het algoritme is van lineaire tijd.

```
  held      ch23  The matching heuristic returns a cover at most twice optimal  (47 graphs)
```

## De heuristiek die er beter uitziet en slechter is

De voor de hand liggende verbetering is gulzig zijn over graad: neem herhaaldelijk de knoop die de
meeste resterende kanten overdekt. Het is meer werk, het gebruikt meer informatie, en het is
intuïtief slimmer.

**Het heeft helemaal geen constante benaderingsfactor.** Het is `Θ(log n)` in het slechtste geval.

Dit zien vergt een echt geval. Neem een linkerzijde `L` van grootte `k`, en voeg voor elke
`i = 2..k` `⌊k/i⌋` rechterknopen toe die elk met `i` verschillende linkerknopen verbonden zijn. `L` is
een overdekking, dus `OPT ≤ k`. Gulzig neemt eerst de rechterknopen van hoge graad en verbruikt
uiteindelijk de hele rechterzijde, ongeveer `k ln k` knopen.

```
  k=8   n=20   m=48    OPT<=8   greedy=12   ratio>=1.50   matching=16   ratio<=2.00
  k=12  n=35   m=115   OPT<=12  greedy=23   ratio>=1.92   matching=24   ratio<=2.00
  k=16  n=50   m=204   OPT<=16  greedy=34   ratio>=2.12   matching=32   ratio<=2.00
  k=20  n=66   m=319   OPT<=20  greedy=46   ratio>=2.30   matching=40   ratio<=2.00
```

Lees de rij `k=16` twee keer. Gulzig geeft **34**; de grove koppelingsheuristiek geeft **32**. Het
algoritme dat meer informatie gebruikt doet het slechter, op een geval dat gebouwd is om precies dat
bloot te leggen, en het wordt slechter naarmate `k` groeit.

Lees nu de eerste twee rijen. Bij `k = 8` en `k = 12` wint gulzig. **Je hebt een geval van vijftig
knopen nodig voordat het verschil überhaupt verschijnt**, en niets kleiners geeft er een hint van. Wie
deze twee heuristieken op kleine grafen vergelijkt, concludeert dat gulzig beter is en levert het op.

```
  refuted   ch23  The max-degree heuristic is at most twice optimal  (3 graphs)
```

Daarom telt de garantie zwaarder dan de metingen. De 2 van de koppelingsheuristiek is een stelling;
de schijnbare superioriteit van gulzig was een steekproefartefact.

Let ook op hoe de factor wordt vastgesteld. `OPT` berekenen op een graaf van vijftig knopen is
onhaalbaar, maar `L` is per constructie een overdekking van grootte `k`, dus `OPT ≤ k` en
`|gulzig| / k` is een strikte **ondergrens** voor de werkelijke factor. Een toelaatbare oplossing
aanwijzen om het optimum te begrenzen is de standaardzet, en het is dezelfde die het 2-benaderingsbewijs
in de andere richting maakt.

## Parameterhardheid

Het tweede antwoord: houd exactheid vast, en beperk het exponentiële tot een parameter.

**Knopenoverdekking van grootte hoogstens `k`** is oplosbaar in `O(2^k · (n + m))`. Kies een
onoverdekte kant; een van haar eindpunten moet in de overdekking zitten, dus vertak op de twee keuzes
met `k − 1`. De recursiediepte is `k`, dus de boom heeft `2^k` bladeren — onafhankelijk van `n`.

```python
def vertex_cover_at_most_k(g, k):
    uncovered = next(((u, v) for u, v in g.edges()), None)
    if uncovered is None:
        return set()
    if k <= 0:
        return None
    u, v = uncovered
    for choice in (u, v):
        smaller = Graph(g.n, [e for e in g.edges() if choice not in e])
        rest = vertex_cover_at_most_k(smaller, k - 1)
        if rest is not None:
            return {choice} | rest
    return None
```

Vergelijk met brute kracht over `C(n, k)` deelverzamelingen. Voor `n = 10⁶` en `k = 10` is dat `10⁶⁰`
tegen `1024`. Een probleem dat zo'n algoritme toelaat is **vast-parameter hanteerbaar** (FPT), en het
onderscheid tussen `f(k) · poly(n)` en `n^{f(k)}` is het hele vakgebied.

```
  held      ch23  Bounded search finds a cover of size <= k exactly when one exists  (52 graphs)
```

Niet elk probleem werkt mee. Onafhankelijke verzameling geparametriseerd naar oplossingsgrootte is
`W[1]`-moeilijk, de geparametriseerde tegenhanger van `NP`-moeilijk — dus de equivalentie van
hoofdstuk 21 breekt ook hier. Knopenoverdekking is FPT; zijn exacte tweelingbroer onder complementeren
niet.

## De invoer beperken

Het derde antwoord, en vaak het beste: merk op dat jouw grafen niet willekeurig zijn.

| Beperking | Wat eenvoudig wordt |
|---|---|
| Bipartiet | knopenoverdekking, onafhankelijke verzameling, koppeling (h. 14, 16) |
| Koordaal / perfect | kleuring, kliek, onafhankelijke verzameling (h. 19) |
| Vlak | 4-kleuring gratis; PTAS voor veel problemen (h. 17) |
| Begrensde boombreedte | vrijwel alles, via dynamisch programmeren (h. 31) |
| Begrensde graad | benaderingsfactoren verbeteren |

Daarom besteedde deel IV vijf hoofdstukken aan structuur. Het praktische antwoord op "dit probleem is
`NP`-moeilijk" is heel vaak "ja, maar mijn grafen zijn vlak", en de klassen kennen is wat je dat laat
opmerken.

## Wat niet kan

Eerlijkheid vergt ook de negatieve resultaten:

- **Knopenoverdekking** is niet beter dan `2 − ε` te benaderen onder het unieke-spellenvermoeden, en
  niet beter dan `1,36` tenzij `P = NP`. Het grove algoritme hierboven is in wezen optimaal.
- **Onafhankelijke verzameling en kliek** zijn niet binnen `n^{1−ε}` te benaderen tenzij `P = NP`.
- **Kleuring** evenmin binnen `n^{1−ε}`.
- **Metrische TSP** heeft een 3/2-benadering (Christofides); algemene TSP heeft er geen, want elke
  benadering met constante factor zou Hamiltoniciteit beslissen.

De 2-benadering voor knopenoverdekking is dus geen tussenoplossing die op verbetering wacht. Ze is,
onder standaardaannames, het eindpunt.

## Probeer het

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.approx import (greedy_lower_bound_instance, greedy_max_degree_cover,
                           vertex_cover_2approx, is_vertex_cover)
for k in (8, 12, 16, 20):
    g, known = greedy_lower_bound_instance(k)
    gr, mm = greedy_max_degree_cover(g), vertex_cover_2approx(g)
    assert is_vertex_cover(g, gr) and is_vertex_cover(g, mm)
    print(f'k={k:<3} n={g.n:<3} OPT<={k:<3} greedy={len(gr):<3} (ratio>={len(gr)/k:.2f})  '
          f'matching={len(mm):<3} (ratio<={len(mm)/k:.2f})')
"
```

```
k=8   n=20  OPT<=8   greedy=12  (ratio>=1.50)  matching=16  (ratio<=2.00)
k=12  n=35  OPT<=12  greedy=23  (ratio>=1.92)  matching=24  (ratio<=2.00)
k=16  n=50  OPT<=16  greedy=34  (ratio>=2.12)  matching=32  (ratio<=2.00)
k=20  n=66  OPT<=20  greedy=46  (ratio>=2.30)  matching=40  (ratio<=2.00)
```

De koppelingskolom komt nooit boven 2,00, want dat kan ze niet. De gulzige kolom passeert haar bij
`k = 16` en blijft klimmen.

## Oefeningen

1. Bewijs dat de koppelingsheuristiek een overdekking van grootte precies `2|M|` teruggeeft, en dat de
   maximaliteit van `M` is wat er een overdekking van maakt.
2. Geef een graaf waarop de koppelingsheuristiek precies `2 · OPT` teruggeeft.
3. Waarom verslaat `O(2^k · (n+m))` de `O(n^k)` voor grote `n` en kleine `k`? Geef getallen.
4. Knopenoverdekking is FPT maar onafhankelijke verzameling is `W[1]`-moeilijk, ook al toonde
   hoofdstuk 21 dat de problemen equivalent zijn. Leg uit hoe beide waar kunnen zijn.

Oplossingen in Bijlage E.

## Kernpunten

- Een `ρ`-benadering is een bewezen grens voor het slechtste geval. Benaderingsbewijzen berekenen
  `OPT` nooit; ze begrenzen het, doorgaans door een toelaatbare oplossing of een disjuncte structuur
  aan te wijzen.
- De knopenoverdekking uit een maximale koppeling is een 2-benadering, van lineaire tijd, en onder
  standaardaannames in wezen optimaal.
- De maximale-graadheuristiek ziet er slimmer uit en heeft geen constante factor. Ze verslaat de
  koppelingsheuristiek op grafen tot ongeveer 35 knopen en verliest vanaf 50 — dus testen op kleine
  gevallen geeft precies het verkeerde antwoord.
- Vast-parameter hanteerbaarheid beperkt het exponentiële tot `k`: `2^k (n+m)` in plaats van `n^k`.
  Knopenoverdekking is FPT; onafhankelijke verzameling is `W[1]`-moeilijk ondanks hetzelfde probleem
  te zijn.
- De invoerklasse beperken is vaak het beste van de drie antwoorden, en daarvoor diende deel IV.
