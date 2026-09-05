# Hoofdstuk 26 — De reuzencomponent

Bij `p = c/n` gebeurt er iets abrupts met `G(n,p)` zodra `c` de 1 passeert. Eronder is elke component
klein. Erboven is er precies één enorme component en is al het overige nog steeds klein. Dit is de
best bestudeerde faseovergang in de combinatoriek, en het loont te begrijpen zowel wat er gebeurt als
waarom het mechanisme zo eenvoudig is.

## De stelling

> **Stelling (Erdős–Rényi, 1960).** Zij `p = c/n`.
>
> - Is `c < 1`, dan heeft de grootste component grootte `O(log n)` met hoge waarschijnlijkheid.
> - Is `c > 1`, dan is er een unieke component van grootte `≈ βn`, waarbij `β` de positieve wortel is
>   van `β = 1 − e^{−cβ}`, en elke andere component is `O(log n)`.
> - Is `c = 1`, dan heeft de grootste component grootte `Θ(n^{2/3})` — niet logaritmisch en niet
>   lineair.

Drie regimes, en het derde is het vreemdste: precies op het kritieke punt is het antwoord een
gebroken macht, en daarom wordt het kritieke venster apart en veel gedetailleerder bestudeerd dan
beide zijden.

## Waarom: het vertakkingsproces

Het mechanisme is eerst een heuristiek en pas daarna een bewijs, en de heuristiek is het deel om te
onthouden.

Verken een component met BFS vanuit een knoop. Elke knoop die je bereikt heeft ongeveer `n` mogelijke
buren, elk aanwezig met kans `c/n`, dus hij levert ongeveer **`c` nieuwe knopen** in verwachting. Vroeg
in de verkenning is er vrijwel niets bezocht, dus het proces lijkt op een **vertakkingsproces met
gemiddeld nageslacht `c`**.

De theorie van vertakkingsprocessen levert dan het antwoord, en het is een tweedeling:

- `c < 1` (subkritiek): uitsterven met kans 1, en het verwachte totale nageslacht is `1/(1−c)`, een
  constante. Componenten zijn klein.
- `c > 1` (superkritiek): overleven met kans `β > 0`, waarbij `β` voldoet aan `β = 1 − e^{−cβ}`. Een
  positieve fractie van de startknopen brengt onbegrensde groei voort, en ze belanden allemaal in
  dezelfde component.
- `c = 1` (kritiek): uitsterven met kans 1, maar de verwachte tijd tot uitsterven is oneindig. Daarom
  is het kritieke geval delicaat.

**`c = 1` is waar elke knoop zichzelf precies één keer vervangt.** Eronder sterft de verkenning uit;
erboven ontsnapt ze. Alles in dit hoofdstuk is die ene zin.

De vertakkingsbenadering is niet exact — de graaf heeft maar `n` knopen, dus het proces moet
uiteindelijk opraken — en haar tot een bewijs maken vergt de tweedemomentmethode (hoofdstuk 25) om te
tonen dat de grootte van de grote component geconcentreerd is, plus een apart argument voor
uniciteit. Uniciteit heeft ook een aardige heuristiek: twee componenten van grootte `εn` hebben `ε²n²`
mogelijke kanten ertussen, en bij `p = c/n` zouden ze met kans naar 1 verbonden zijn.

## Het meten

```bash
python scripts/random_graph_experiments.py
```

```
Giant component, n = 400, 5 trials per row

  c = pn  largest/n    2nd/n  #comps
     0.4      0.014    0.013   317.6
     0.6      0.035    0.024   280.0
     0.8      0.052    0.039   237.0
     0.9      0.096    0.070   202.4
     1.0      0.142    0.044   199.4
     1.1      0.217    0.066   176.4
     1.2      0.324    0.056   157.6
     1.5      0.581    0.023   116.4
     2.0      0.793    0.011    65.6
     3.0      0.937    0.006    24.2
```

Twee kolommen, en de tweede is degene om te lezen.

**De grootste component groeit gestaag** van 1,4% naar 94% van de graaf — maar dat is een geleidelijk
ogende kromme, en bij `n = 400` is de overgang werkelijk vervaagd. De stelling is asymptotisch;
`log n ≈ 6` en `n^{2/3} ≈ 54` en `n = 400` liggen bij deze omvang eenvoudigweg niet ver genoeg uit
elkaar om op drie regimes te lijken.

**De op één na grootste component is het scherpe signaal.** Ze stijgt tot 7% van de graaf bij
`c = 0,9`, en zakt dan weg — 4,4% bij `c = 1,0`, 2,3% bij `c = 1,5`, 1,1% bij `c = 2,0`, 0,6% bij
`c = 3,0`. Die niet-monotone piek nabij `c = 1` is de overgang die zich zichtbaar maakt: onder de
drempel zijn de twee grootste componenten vergelijkbaar, erboven loopt de grootste weg en laat al het
overige achter.

Vergelijk de rij `c = 0,4` — grootste 1,4%, tweede 1,3%, in wezen gelijk — met `c = 3,0` — grootste
94%, tweede 0,6%. De *verhouding* tussen de eerste en de tweede is de ordeparameter, en die verandert
van karakter, niet de grootte van de grootste alleen.

Bij `n = 400` met 5 herhalingen zijn deze getallen ruisig, en het gaat om de vorm en niet om enig
afzonderlijk cijfer. Een eindig experiment kan een asymptotische stelling niet bevestigen; wat het wel
kan, is je tonen waar te kijken.

## Waarom het buiten de grafentheorie telt

Dezelfde overgang, met hetzelfde `c = 1`-mechanisme, beheerst:

- **Percolatie**: vloeistof die zich boven een kritieke dichtheid door poreus gesteente verspreidt.
- **Epidemieën**: het basisreproductiegetal `R₀` is precies `c`, en `R₀ = 1` is precies deze drempel.
  De reuzencomponent is de uitbraak.
- **Netwerkweerbaarheid**: hoeveel knopen kunnen uitvallen voordat een netwerk versplintert.
- **Willekeurige SAT**: vervulbaarheid heeft een analoge scherpe drempel in de verhouding tussen
  clausules en variabelen.

De bewering dat een epidemie ofwel uitdooft ofwel een constante fractie van de bevolking bereikt, met
niets ertussenin, is deze stelling. De vertakkingsheuristiek — elk geval brengt `R₀` nieuwe gevallen
voort — is dezelfde, en het is waarom `R₀ = 1` het getal is waar iedereen naar kijkt.

## Probeer het

Kijk hoe de op één na grootste component piekt en terugvalt:

```bash
python -c "
import sys, random; sys.path.insert(0, '.')
from graphs.generate import random_graph
from graphs.algorithms import components
rng = random.Random(11)
n, trials = 800, 15
for c in (0.5, 0.9, 1.0, 1.1, 1.5, 2.5):
    first = second = 0
    for _ in range(trials):
        s = sorted((len(x) for x in components(random_graph(n, c/n, rng))), reverse=True)
        first += s[0]; second += s[1] if len(s) > 1 else 0
    a, b = first/trials, second/trials
    print(f'c={c:<4} largest={a:<7.1f} second={b:<6.1f} ratio={a/max(b,1):.1f}')
"
```

```
c=0.5  largest=11.2    second=8.4    ratio=1.3
c=0.9  largest=51.3    second=26.0   ratio=2.0
c=1.0  largest=106.5   second=29.9   ratio=3.6
c=1.1  largest=128.1   second=45.1   ratio=2.8
c=1.5  largest=470.1   second=11.9   ratio=39.6
c=2.5  largest=717.0   second=3.3    ratio=219.5
```

De verhouding is het verhaal: nabij 1 onder de drempel, en onbegrensd klimmend erboven.

**Dit vergt middelen over vijftien herhalingen, en dat is zelf de bevinding.** Eén run per rij levert
een niet-monotone warboel — bij één poging gaf `c = 1,1` een *lagere* verhouding dan `c = 1,0`. Dat is
geen experimentele slordigheid; nabij het kritieke punt hebben de componentgroottes werkelijk een
enorme variantie, en dat is juist waarom het geval `c = 1` zijn eigen `Θ(n^{2/3})`-stelling en zijn
eigen literatuur heeft. Zien je metingen bij een faseovergang er ruisig uit, dan kan de ruis het
verschijnsel zijn.

## Oefeningen

1. Los `β = 1 − e^{−cβ}` numeriek op voor `c = 1,5` en vergelijk met de gemeten 0,581.
2. Waarom breekt de vertakkingsheuristiek af zodra de verkende verzameling een constante fractie van
   de graaf is?
3. Geef het argument dat twee reuzencomponenten niet naast elkaar kunnen bestaan.
4. Wat betekent `c < 1` in epidemiologische termen, en waarmee komt de op één na grootste component
   overeen?

Oplossingen in Bijlage E.

## Kernpunten

- Bij `p = c/n`: alle componenten `O(log n)` voor `c < 1`; een unieke component van `βn` voor `c > 1`;
  `Θ(n^{2/3})` precies bij `c = 1`.
- Het mechanisme is een vertakkingsproces met gemiddeld nageslacht `c`. `c = 1` is waar elke knoop
  zichzelf precies één keer vervangt — die ene zin is het hele hoofdstuk.
- `β` voldoet aan `β = 1 − e^{−cβ}`, wat volgt uit de uitsterfkans van dat proces.
- Bij `n = 400` ziet de groei van de grootste component er geleidelijk uit. De **verhouding tussen de
  grootste en de op één na grootste** is het scherpe signaal, en de piek van de tweede nabij `c = 1`
  is de overgang die bij eindige omvang zichtbaar wordt.
- Dezelfde overgang is percolatie, `R₀ = 1` bij epidemieën, en de drempel bij willekeurige SAT.
