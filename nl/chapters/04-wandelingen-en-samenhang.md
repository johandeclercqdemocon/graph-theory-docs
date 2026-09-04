# Hoofdstuk 4 — Wandelingen, paden, samenhang

Dit hoofdstuk is woordenschat, en het loont de moeite er precies in te zijn, want drie
woorden die beginners door elkaar gebruiken zijn niet onderling verwisselbaar, en de helft
van de verwarring in latere bewijzen komt voort uit het vervagen ervan.

## Drie woorden

Een **wandeling** is een rij knopen `v₀, v₁, …, v_k` waarbij opeenvolgende knopen aangrenzend
zijn. Herhalingen zijn toegestaan, zowel van knopen als van kanten. De **lengte** is `k`, het
aantal doorlopen kanten — niet het aantal knopen, dat `k + 1` is.

Een **pad** is een wandeling zonder herhaalde knoop.

Een **cykel** is een wandeling van lengte minstens 3 die begint en eindigt in dezelfde knoop,
zonder andere herhalingen.

Het verband tussen de eerste twee is het lemma waarop al het overige rust:

> **Lemma.** Bestaat er een wandeling van `u` naar `v`, dan bestaat er een pad van `u` naar
> `v`.

*Bewijs.* Neem een wandeling van `u` naar `v` van minimale lengte. Zou ze een knoop `w`
herhalen, dan kon het stuk tussen de twee bezoeken aan `w` geschrapt worden, wat een kortere
wandeling van `u` naar `v` oplevert — in tegenspraak met de minimaliteit. Dus ze herhaalt geen
knoop, en is een pad. ∎

Daarom mag je altijd "pad" aannemen wanneer een argument je een "wandeling" aanreikt, en vanaf
hoofdstuk 9 gebeurt dat zonder commentaar. Het is ook de reden dat de twee begrippen werkelijk
verschillen: wandelingen zijn eenvoudig te tellen en paden niet, wat het onderwerp is van de
volgende paragraaf.

## Wandelingen tellen

Wandelingen hebben een nette algebraïsche beschrijving die paden opvallend ontberen.

> **Stelling.** Zij `A` de adjacentiematrix van `G`. De `(u, v)`-plaats van `A^k` is het aantal
> wandelingen van lengte precies `k` van `u` naar `v`.

*Bewijs.* Inductie naar `k`. Voor `k = 1` is de bewering de definitie van `A`. Stel dat ze
geldt voor `k`. Een wandeling van lengte `k+1` van `u` naar `v` is een wandeling van lengte `k`
van `u` naar een `t`, gevolgd door een kant `tv`. Sommeren over `t` geeft
`(A^{k+1})_{uv} = Σ_t (A^k)_{ut} · A_{tv}`, en dat is precies de definitie van
matrixvermenigvuldiging. ∎

```python
from graphs.core import cycle, complete
from graphs.algorithms import walk_counts

for row in walk_counts(cycle(4), 2):
    print(row)
```

```
[2, 0, 2, 0]
[0, 2, 0, 2]
[2, 0, 2, 0]
[0, 2, 0, 2]
```

Lees het. Vanuit knoop 0 zijn er twee wandelingen van lengte 2 terug naar knoop 0 (naar een van
beide buren en terug), twee naar knoop 2 (langs beide kanten rond), en geen naar de knopen 1
en 3 — want `C₄` is bipartiet, en een wandeling van even lengte kan niet tussen de twee zijden
oversteken. De nullen in die matrix zijn de stelling van hoofdstuk 16, drie hoofdstukken te
vroeg zichtbaar.

Probeer nu dezelfde stelling voor paden op te schrijven. Dat lukt niet: er is geen
matrixoperatie die paden telt, en ze tellen is `#P`-volledig. De kloof tussen "wandelingen zijn
lineaire algebra" en "paden zijn onhandelbaar" is een van de scherpste scheidslijnen in het
vak, en hoofdstuk 29 is wat er gebeurt als je de kant van de lineaire algebra serieus neemt.

## Samenhang

`u` en `v` zijn **verbonden** wanneer een pad ze samenvoegt. Die relatie is reflexief (de
wandeling van lengte nul), symmetrisch (draai het pad om) en transitief (plak twee wandelingen
aan elkaar en pas dan het bovenstaande lemma toe om een pad te krijgen) — ze is dus een
equivalentierelatie, en haar klassen zijn de **samenhangscomponenten**.

Dat "dus" is de hele reden dat het lemma bewezen moest worden. Twee paden aan elkaar plakken
geeft geen pad; het geeft een wandeling. Zonder het wandeling-naar-padlemma faalt transitiviteit
en zijn componenten niet welgedefinieerd.

```python
from graphs.core import Graph
from graphs.algorithms import components, is_connected

g = Graph(7, [(0, 1), (1, 2), (2, 0), (3, 4), (5, 6)])
print(components(g))     # [{0, 1, 2}, {3, 4}, {5, 6}]
print(is_connected(g))   # False
```

Een graaf is **samenhangend** wanneer hij precies één component heeft. Twee conventies moeten
uitgesproken worden in plaats van aangenomen, want teksten verschillen erin en bewijzen hangen
er stilzwijgend van af:

- De graaf op één knoop **is** samenhangend. Daarover bestaat geen discussie.
- De lege graaf — helemaal geen knopen — geldt in dit boek als samenhangend. Hij heeft nul
  componenten, niet één, dus dit is een conventie en geen gevolg. Ze is gekozen omdat ze "elke
  graaf is de disjuncte vereniging van zijn componenten" waar maakt zonder uitzondering, en
  omdat de kantentelling van hoofdstuk 6 dan uitkomt. Sommige teksten noemen de lege graaf niet
  samenhangend; lees je er zo een, ga dan na welke stellingen er een voorwaarde bij krijgen.

## Het kantenbudget

> **Stelling.** Een samenhangende graaf op `n ≥ 1` knopen heeft `m ≥ n − 1`.

*Bewijs.* Inductie naar `n`. Voor `n = 1` volstaat `m ≥ 0`. Voor de stap: neem een
samenhangende `G` op `n` knopen. Heeft elke knoop graad minstens 2, dan is
`2m = Σ deg(v) ≥ 2n`, dus `m ≥ n > n − 1` en we zijn klaar. Anders heeft een knoop `v` graad
hoogstens 1; omdat `G` samenhangend is en `n ≥ 2`, is zijn graad precies 1. Verwijder `v` en
zijn kant. Het resultaat is samenhangend op `n − 1` knopen, heeft dus per inductie minstens
`n − 2` kanten, en `G` heeft er minstens `n − 1`. ∎

Het complementaire feit — een graaf met `m ≥ n` bevat een cykel — is dat van hoofdstuk 6, en
samen leggen ze bomen precies vast.

Een tweede klein resultaat dat voortdurend gebruikt wordt:

> **Lemma.** Eén kant verwijderen verhoogt het aantal componenten met hoogstens één.

*Bewijs.* `uv` verwijderen kan alleen knopen scheiden waarvan elk pad `uv` gebruikte. Twee
knopen die in `G − uv` nog door een pad verbonden zijn, blijven in dezelfde component. Elke
knoop bereikt in `G − uv` nog `u` of `v`, want een pad ernaartoe in `G` dat `uv` gebruikte kan
afgekapt worden bij de eerste van `u`, `v` die het tegenkomt. De component die `uv` bevat valt
dus in hoogstens twee stukken uiteen, en geen andere component verandert. ∎

Een kant waarvan verwijdering het aantal *wel* verhoogt heet een **brug**, en hoofdstuk 12
karakteriseert ze: een kant is een brug precies wanneer ze op geen enkele cykel ligt.

## Afstand

Voor `u`, `v` in dezelfde component is `d(u, v)` de lengte van een kortste pad ertussen. Het is
een metriek: niet-negatief, nul alleen op de diagonaal, symmetrisch, en voldoend aan de
driehoeksongelijkheid `d(u, w) ≤ d(u, v) + d(v, w)` — plak aan elkaar en kort in.

```python
from graphs.core import path
from graphs.algorithms import distances

print(distances(path(5), 0))   # {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
```

Breedte-eerst zoeken berekent ze alle in `O(n + m)`, en hoofdstuk 8 legt uit waarom dat klopt.
De **diameter** is de grootste eindige afstand; de **excentriciteit** van `v` is de grootste
afstand vanaf `v`; de **straal** is de kleinste excentriciteit. Hoofdstuk 11 berekent ze
allemaal, en hoofdstuk 30 verbindt de diameter met het Laplace-spectrum, wat een veel minder
voor de hand liggend verband is dan het klinkt.

## Probeer het

Bevestig de matrixmachtstelling tegen een directe telling, op een graaf die klein genoeg is om
met de hand na te gaan:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import complete
from graphs.algorithms import walk_counts
w = walk_counts(complete(4), 3)
print('closed walks of length 3 at each vertex:', [w[i][i] for i in range(4)])
"
```

```
closed walks of length 3 at each vertex: [6, 6, 6, 6]
```

Zes klopt, en je ziet waarom: een gesloten wandeling van lengte 3 vanuit `v` in `K₄` moet twee
verschillende andere knopen bezoeken, en er zijn `3 × 2 = 6` geordende manieren om die te
kiezen. Merk op dat dit elke driehoek **twee keer** telt — één keer per richting — en dat is
waarom de standaardformule voor het aantal driehoeken `trace(A³)/6` is: drie startpunten, twee
richtingen.

## Oefeningen

1. Geef in `C₅` een wandeling die geen pad is, en een pad dat geen cykel is.
2. Waaraan is `(A²)_{vv}` gelijk, en waarom?
3. Wat is het minimale aantal kanten in een samenhangende graaf op `n` knopen, en welke grafen
   bereiken het?
4. Twee paden aan elkaar plakken hoeft geen pad te geven. Leg uit waarom samenhang toch een
   equivalentierelatie is.

Oplossingen in Bijlage E.

## Kernpunten

- Wandeling, pad en cykel zijn drie verschillende dingen. Een wandeling herhaalt; een pad niet;
  een cykel sluit.
- Elke wandeling bevat een pad met dezelfde eindpunten. Dat maakt samenhang tot een
  equivalentierelatie, en het wordt na dit hoofdstuk overal stilzwijgend gebruikt.
- `(A^k)_{uv}` telt wandelingen van lengte `k`. Voor paden bestaat niets vergelijkbaars, en dat
  gat is geen gat in onze kennis — paden tellen is `#P`-volledig.
- Samenhangende grafen hebben `m ≥ n − 1`; een kant verwijderen splitst hoogstens één component
  in tweeën.
- Spreek je conventie voor de lege graaf één keer uit en houd je eraan. Dit boek noemt hem
  samenhangend.
