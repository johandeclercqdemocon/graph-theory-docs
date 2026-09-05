# Hoofdstuk 24 — De probabilistische methode

Dit is het scharnier van het boek. Elk bewijs tot hier was constructief: het bouwde het object, of gaf
een algoritme dat het zou bouwen. Vanaf hier houden de argumenten daarmee op.

De methode, van Erdős, is één zin: **om te bewijzen dat een object bestaat, leg je een
kansverdeling op een ruimte die het bevat en toon je dat de kans op een geschikt object positief
is.** Je toont er nooit een. Je toont dat er een moet zijn.

## Het kleinst mogelijke voorbeeld

> **Stelling.** Elke graaf heeft een bipartiete deelgraaf met minstens `m/2` kanten.

*Bewijs.* Kleur elke knoop onafhankelijk rood of blauw met kans `1/2`. Een kant steekt over wanneer
haar eindpunten verschillen, wat met kans `1/2` gebeurt. Per lineariteit van de verwachting is het
verwachte aantal overstekende kanten `m/2`.

Een stochastische variabele is met positieve kans minstens haar verwachting. Er is dus een kleuring
die minstens `m/2` overstekende kanten haalt, en de overstekende kanten vormen een bipartiete
deelgraaf. ∎

Lees dat nog eens over voor wat het níet doet. Het vertelt je niet welke kleuring. Het geeft geen
algoritme. Het beweert dat er onder `2ⁿ` kleuringen minstens één goede zit, op grond van het feit dat
het gemiddelde goed is.

**Lineariteit van de verwachting** doet al het werk, en het is het meest gebruikte instrument van de
methode juist omdat het geen onafhankelijkheid nodig heeft. De kanten hier zijn *niet* onafhankelijk
— twee kanten die een knoop delen zijn gecorreleerd — en dat maakt niets uit.

```
  held      ch24  Every graph has a bipartite subgraph with at least m/2 edges  (52 graphs)
```

## Ontrandomiseren

Het bewijs is niet-constructief, maar dit bepaalde bewijs valt te repareren. Loop de knopen in
volgorde af, en plaats elke knoop aan de zijde die tot dan toe de meeste overstekende kanten geeft:

```python
def greedy_cut(g):
    side = {}
    for v in g.vertices():
        zero = sum(1 for w in g.neighbours(v) if side.get(w) == 0)
        one = sum(1 for w in g.neighbours(v) if side.get(w) == 1)
        side[v] = 1 if zero >= one else 0
    return sum(1 for u, v in g.edges() if side[u] != side[v])
```

Dit is de **methode van de voorwaardelijke verwachtingen**: kies bij elke stap de optie waarvan de
voorwaardelijke verwachting minstens de huidige verwachting is. Omdat de verwachting bij `m/2` begint
en nooit daalt, is het uiteindelijke deterministische antwoord minstens `m/2`.

Niet elk probabilistisch bewijs laat zich zo netjes ontrandomiseren, en die welke dat niet doen zijn
de interessante.

## Ondergrenzen voor Ramsey

De klassieke toepassing, en degene die de werkelijke kracht van de methode toont.

> **Stelling (Erdős, 1947).** Geldt `C(n,k) · 2^{1−C(k,2)} < 1`, dan bestaat er een 2-kleuring van
> `K_n` zonder monochromatische `K_k`. Dus `R(k,k) > 2^{k/2}` voor `k ≥ 3`.

*Bewijs.* Kleur elke kant onafhankelijk willekeurig rood of blauw. Voor een vaste verzameling van `k`
knopen is de kans dat ze monochromatisch is `2 · 2^{−C(k,2)}`. Er zijn `C(n,k)` zulke verzamelingen,
dus per uniegrens is de kans dat *een of andere* verzameling monochromatisch is hoogstens
`C(n,k) · 2^{1−C(k,2)}`.

Is dat kleiner dan 1, dan is de kans op geen monochromatische verzameling positief, dus zo'n kleuring
bestaat. ∎

Hier verdient de methode haar reputatie. De grens `R(k,k) > 2^{k/2}` was in 1947 een dramatische
verbetering op alles wat bekend was — en **niemand heeft ooit een kleuring geconstrueerd** die er ook
maar in de buurt komt. Zestig jaar inspanning heeft expliciete constructies opgeleverd die veel
zwakker zijn dan wat een alinea middelen geeft. De kloof tussen wat we kunnen bewijzen te bestaan en
wat we kunnen bouwen is bij dit probleem enorm en ziet er permanent uit.

Hoofdstuk 28 geeft de bovengrens en de daaruit volgende staat van onwetendheid over `R(5,5)`.

## De drie instrumenten

Vrijwel elk argument in deze stijl gebruikt een van drie ideeën.

**Lineariteit van de verwachting.** `E[X + Y] = E[X] + E[Y]`, altijd, zonder enige
onafhankelijkheidsaanname. Hierboven gebruikt voor de snede.

**De uniegrens.** `P(∪Aᵢ) ≤ Σ P(Aᵢ)`, altijd. Hierboven gebruikt voor Ramsey. Grof, en meestal
voldoende.

**De verwijderingsmethode.** Toon dat een willekeurig object *gemiddeld* weinig slechte delen heeft,
en verwijder dan één knoop per slecht deel. Wat overblijft is goed en nog steeds groot. Dat geeft
bijvoorbeeld dat een graaf met `n` knopen en `m` kanten een onafhankelijke verzameling van grootte
minstens `n²/(4m)` heeft — neem elke knoop met kans `p`, verwijder één eindpunt van elke overlevende
kant, en optimaliseer `p`.

Wanneer deze drie falen, wordt de machinerie veel zwaarder — het lokale lemma van Lovász,
martingaalconcentratie, de tweedemomentmethode — en hoofdstuk 26 heeft die laatste nodig.

## Wat er vanaf hier verandert

De rest van deel VI is in deze stijl geschreven, en het loont de verschuiving expliciet te maken.

De verificatie kan niet op dezelfde manier helpen als eerder. Een bewering als "er bestaat een
kleuring zonder monochromatische `K_k`" is alleen controleerbaar door alle kleuringen af te zoeken,
en dat is precies wat de methode wil vermijden. Hoofdstuk 28 controleert `R(3,3) = 6` uitputtend
omdat 32.768 kleuringen klein is; `R(5,5)` betreft meer kleuringen dan er atomen in het waarneembare
heelal zijn, en geen enkele hoeveelheid rekenkracht beslist het.

Vanaf hier zijn de beweringen van het boek dus controleerbaar bij kleine `n` terwijl de stellingen
over grote `n` gaan, en het gat daartussen is een gat dat de verificatie niet kan dichten. De
hoofdstukken 25 en 26 gaan daarmee om door *scherpte* te meten in plaats van waarheid — tonen dat de
overgang smal is, wat een eindig feit is — en door ronduit te zeggen dat een limietuitspraak niet is
wat er getest wordt.

## Probeer het

```bash
python -c "
import sys, random; sys.path.insert(0, '.')
from graphs.core import petersen, complete
from graphs.extremal import max_cut_bruteforce, greedy_cut, random_bipartition_cut
rng = random.Random(4)
for name, g in [('K5', complete(5)), ('petersen', petersen())]:
    trials = [random_bipartition_cut(g, rng) for _ in range(1000)]
    print(f'{name}: m={g.m}  m/2={g.m/2}')
    print(f'   random cut, mean over 1000 trials: {sum(trials)/1000:.2f}')
    print(f'   greedy (derandomised):             {greedy_cut(g)}')
    print(f'   true maximum:                      {max_cut_bruteforce(g)}')
"
```

```
K5: m=10  m/2=5.0
   random cut, mean over 1000 trials: 5.01
   greedy (derandomised):             6
   true maximum:                      6
petersen: m=15  m/2=7.5
   random cut, mean over 1000 trials: 7.41
   greedy (derandomised):             12
   true maximum:                      12
```

De willekeurige gemiddelden landen dicht bij `m/2` — `5,01` tegen `5,0`, en `7,41` tegen `7,5` —
precies zoals lineariteit van de verwachting voorspelt. Het ontrandomiseerde gulzige algoritme
overtreft de grens ruim en haalt hier op beide grafen het werkelijke maximum. Dat is normaal en het is
geen garantie: de stelling belooft `m/2` en niets meer, en een heuristiek die het meestal beter doet is
precies de situatie waar hoofdstuk 23 voor waarschuwde.

## Oefeningen

1. Bewijs in je eigen woorden dat elke graaf een bipartiete deelgraaf met minstens `m/2` kanten heeft,
   en zeg waar onafhankelijkheid nodig geweest zou zijn als je haar gebruikt had.
2. Een toernooi is een volledige graaf waarin elke kant gericht is. Toon aan dat een of ander toernooi
   op `n` knopen minstens `n!/2^{n−1}` Hamiltoniaanse paden heeft.
3. Gebruik de verwijderingsmethode om te tonen dat een graaf met `n` knopen en `m ≥ n/2` kanten een
   onafhankelijke verzameling van grootte minstens `n²/(4m)` heeft.
4. Waarom laat de `m/2`-snedegrens zich eenvoudig ontrandomiseren en de Ramsey-ondergrens niet?

Oplossingen in Bijlage E.

## Kernpunten

- Om bestaan te bewijzen, toon je dat een willekeurig object met positieve kans werkt. Je bouwt er
  nooit een.
- Lineariteit van de verwachting heeft geen onafhankelijkheid nodig, en daarom is ze het werkpaard.
- De uniegrens is grof en meestal voldoende; de verwijderingsmethode behandelt "grotendeels goede"
  objecten.
- `R(k,k) > 2^{k/2}` volgt uit een alinea middelen, en geen expliciete constructie is ooit in de buurt
  gekomen. Die kloof is de duidelijkste demonstratie van de methode.
- Vanaf hier zijn de stellingen asymptotisch en de verificatie eindig. Het boek meet scherpte, en doet
  niet alsof dat hetzelfde is als bewijs.
