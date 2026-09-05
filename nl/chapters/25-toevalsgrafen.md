# Hoofdstuk 25 — Toevalsgrafen

`G(n, p)` is de graaf op `n` knopen waarin elk van de `C(n,2)` mogelijke kanten onafhankelijk met
kans `p` verschijnt. Het inzicht van Erdős en Rényi was dat dit niet slechts een bron van
testgevallen is — er zit een rijke theorie in, en vrijwel elke eigenschap verschijnt *plotseling*
naarmate `p` groeit.

## Drempels

Een eigenschap is **monotoon stijgend** wanneer kanten toevoegen haar niet kan vernietigen:
samenhang, een driehoek hebben, een Hamiltoniaanse cykel bevatten.

> **Stelling (Bollobás–Thomason, 1987).** Elke monotoon stijgende eigenschap heeft een
> drempelfunctie `p*(n)`: is `p ≪ p*` dan geldt de eigenschap met kans naar 0, en is `p ≫ p*` dan met
> kans naar 1.

Elke monotone eigenschap heeft er een. De vraag is altijd *waar*, nooit *of*.

| Eigenschap | Drempel |
|---|---|
| Bevat een driehoek | `1/n` |
| Bevat een vaste `H` (gebalanceerd) | `n^{−v(H)/e(H)}` |
| Reuzencomponent verschijnt | `1/n` (hoofdstuk 26) |
| Geen geïsoleerde knopen | `ln n / n` |
| Samenhangend | `ln n / n` |
| Hamiltoniaans | `ln n / n` |

Dat de laatste drie een drempel delen is geen toeval, en het is de leerzaamste rij in de tabel. Onder
`ln n / n` heeft een toevalsgraaf geïsoleerde knopen; dat alleen al maakt hem onsamenhangend en
niet-Hamiltoniaans. Erboven verdwijnen de geïsoleerde knopen — en het blijkt dat *niets anders* ooit
de belemmering was. **Het moment waarop de laatste geïsoleerde knoop verdwijnt is in wezen het moment
waarop de graaf Hamiltoniaans wordt**, en dat is een veel sterkere uitspraak dan samenhang en komt er
gratis bij.

## De eerstemomentmethode

Het verwachte aantal driehoeken in `G(n,p)` is `C(n,3) p³ ≈ n³p³/6`.

Is `p ≪ 1/n`, dan gaat dit naar 0, en omdat het aantal driehoeken een niet-negatief geheel getal is,
geeft de ongelijkheid van Markov `P(minstens één driehoek) ≤ E[aantal] → 0`. Dat is de
**eerstemomentmethode**: een verwachting die naar nul gaat bewijst dat het object er meestal niet is.

Het omgekeerde vergt meer. Een verwachting die naar *oneindig* gaat bewijst geen bestaan — een
variabele kan een enorm gemiddelde hebben en toch bijna altijd nul zijn, als ze af en toe reusachtig
is. Dat uitsluiten vergt de variantie, en dat is de **tweedemomentmethode**, die hoofdstuk 26
gebruikt.

Die asymmetrie is het eigen maken waard: **eerste moment voor niet-bestaan, tweede moment voor
bestaan.** Ze omdraaien is de standaardfout in dit vak.

## Scherpte meten

Een drempel is een asymptotische uitspraak, dus geen enkel eindig experiment kan haar bevestigen. Wat
een experiment *wel* kan tonen, is dat de overgang smal is — een feit over `n = 400` in plaats van
over de limiet.

```bash
python scripts/random_graph_experiments.py
```

```
Connectivity, n = 400, p = c ln(n)/n, 40 trials per row

       c  connected fraction
     0.4                0.00
     0.6                0.00
     0.8                0.03
     1.0                0.47
     1.2                0.65
     1.5                0.93
     2.0                1.00
```

Bij `c = 0,6` is in wezen niets samenhangend; bij `c = 2,0` alles. De hele overgang vindt plaats
binnen een factor van ongeveer drie in `p`, en bij `c = 1` — precies de voorspelde drempel — is het
bijna kop of munt.

**Dit is geen bewijsmateriaal dat de drempel `ln n / n` is.** Het is ermee verenigbaar, bij één waarde
van `n`. De stelling gaat over `n → ∞`, en één `n` kan `ln n / n` niet onderscheiden van elke functie
die er bij 400 toevallig dicht bij ligt. Wat de tabel eerlijk toont is scherpte, en scherpte is het
verrassende deel — een eigenschap die van nooit naar altijd gaat over een smalle band is niet wat de
naïeve intuïtie voorspelt.

## Vrijwel elke graaf

Resultaten over toevalsgrafen worden meestal geformuleerd als feiten over "vrijwel elke graaf", en de
vertaling is het expliciet maken waard. `G(n, 1/2)` is de uniforme verdeling over alle gelabelde
grafen op `n` knopen, want elke graaf heeft kans `2^{−C(n,2)}`. Een eigenschap die **met hoge
waarschijnlijkheid** geldt in `G(n, 1/2)` is dus een eigenschap van vrijwel elke graaf.

Verschillende zulke feiten zijn verbluffend:

- Vrijwel elke graaf heeft diameter 2.
- Vrijwel elke graaf heeft een triviale automorfismegroep — helemaal geen symmetrieën.
- Vrijwel elke graaf heeft kliekgetal ongeveer `2 log₂ n`, geconcentreerd op **twee waarden**.

Die laatste is opmerkelijk. `ω(G)` voor een toevalsgraaf ligt niet slechts in de buurt van `2 log₂ n`;
het is een van twee specifieke gehele getallen met kans naar 1. En toch is een kliek van grootte
`(1+ε) log₂ n` vinden in een toevalsgraaf een beroemd open probleem — gulzig vindt `log₂ n` en niets
doet het beter. **We weten precies hoe groot het antwoord is en kunnen het niet vinden**, wat dezelfde
kloof is die hoofdstuk 24 voor Ramsey aanwees, in een andere vermomming.

## Probeer het

```bash
python -c "
import sys, random, math; sys.path.insert(0, '.')
from graphs.generate import random_graph
from graphs.algorithms import distances
rng = random.Random(2)
n = 200
for p in (0.02, 0.05, 0.1, 0.3):
    diam = 0
    g = random_graph(n, p, rng)
    for v in g.vertices():
        d = distances(g, v)
        if len(d) == n:
            diam = max(diam, max(d.values()))
        else:
            diam = -1; break
    print(f'p={p:<5} m={g.m:<6} diameter={diam if diam > 0 else \"disconnected\"}')
"
```

```
p=0.02  m=407    diameter=disconnected
p=0.05  m=1006   diameter=4
p=0.1   m=1925   diameter=3
p=0.3   m=5970   diameter=2
```

Bij `p = 0,3` is de diameter al 2, en hij blijft daar — het resultaat "vrijwel elke graaf heeft
diameter 2" arriveert ruim vóór `p = 1/2`.

## Oefeningen

1. Bereken het verwachte aantal driehoeken in `G(n, p)` en vind de drempel waar het ophoudt naar nul
   te gaan.
2. Waarom bewijst een verwacht aantal kopieën van `H` dat naar oneindig gaat niet dat `H` verschijnt?
   Geef de vorm van een tegenvoorbeeld.
3. Toon aan dat het verwachte aantal geïsoleerde knopen in `G(n,p)` gelijk is aan `n(1−p)^{n−1}`, en
   vind waar het naar een constante gaat.
4. `G(n, 1/2)` is uniform over gelabelde grafen. Waarom maakt dat uitspraken "met hoge
   waarschijnlijkheid" tot uitspraken over vrijwel elke graaf?

Oplossingen in Bijlage E.

## Kernpunten

- Elke monotoon stijgende eigenschap heeft een drempel; de vraag is waar die ligt.
- Samenhang, geen geïsoleerde knopen, en Hamiltoniciteit delen de drempel `ln n / n`. Het verdwijnen
  van de laatste geïsoleerde knoop is in wezen het moment waarop de graaf Hamiltoniaans wordt.
- Eerste moment (verwachting → 0) bewijst niet-bestaan. Bestaan vergt het tweede moment, want een
  groot gemiddelde kan een variabele verbergen die meestal nul is.
- Een eindig experiment kan een asymptotische drempel niet bevestigen. Het kan tonen dat de overgang
  scherp is, wat een andere en nog steeds verrassende bewering is, en het boek zegt welke van beide
  het toont.
- Vrijwel elke graaf heeft diameter 2, geen symmetrieën, en een kliekgetal geconcentreerd op twee
  waarden — die we niet kunnen vinden.
