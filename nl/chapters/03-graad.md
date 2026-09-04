# Hoofdstuk 3 — Graad

De graad van een knoop is hoeveel kanten hem raken. Het is het eerste getal dat je aan een
graaf kunt hangen, het goedkoopste om te berekenen, en er volgt verrassend veel uit alleen
dat.

## Het handdruklemma

Schrijf `deg(v)` voor het aantal buren van `v`, en `Δ(G)` en `δ(G)` voor de grootste en
kleinste graad in `G`.

> **Stelling (handdruklemma).** Voor elke graaf geldt `Σ_v deg(v) = 2m`.

*Bewijs.* Tel de paren `(v, e)` waarbij `v` een knoop is, `e` een kant, en `v` een eindpunt van
`e`. Tel je per knoop, dan komt elke `v` in `deg(v)` zulke paren voor, wat `Σ_v deg(v)` geeft.
Tel je per kant, dan heeft elke kant precies twee eindpunten, wat `2m` geeft. De twee tellingen
gaan over dezelfde verzameling, dus ze zijn gelijk. ∎

Dat is een **dubbeltelling**: één verzameling, twee manieren om haar te turven. Het is de
meest herbruikbare bewijstechniek in dit boek, en ze keert terug in hoofdstuk 17 voor de
formule van Euler en in hoofdstuk 27 voor de stelling van Mantel.

```python
from graphs.core import petersen

g = petersen()
print(sum(g.degree(v) for v in g.vertices()), 2 * g.m)   # 30 30
```

De werkelijke inhoud van het lemma is een pariteitsuitspraak, en dit is de vorm die je
daadwerkelijk zult gebruiken:

> **Gevolg.** In elke graaf is het aantal knopen van oneven graad even.

*Bewijs.* Splits de som in het handdruklemma in termen van even en van oneven graad. De even
termen sommeren tot een even getal, en het totaal `2m` is even, dus de oneven termen moeten
ook tot een even getal sommeren. Een som van oneven getallen is even precies wanneer er een
even aantal van is. ∎

Daarom kun je geen feest houden waarop elk van negen mensen precies drie anderen de hand
schudt, en daarom moet een 3-reguliere graaf een even aantal knopen hebben. Beide uitspraken
klinken alsof ze werk vergen; beide zijn één regel.

## Twee knopen delen altijd een graad

> **Stelling.** Elke graaf met `n ≥ 2` heeft twee knopen van dezelfde graad.

*Bewijs.* Graden liggen in `{0, 1, …, n−1}`, wat `n` waarden zijn voor `n` knopen — nog geen
tegenspraak. Maar `0` en `n−1` kunnen niet allebei voorkomen: een knoop van graad `n−1` grenst
aan alles, dus niets heeft graad `0`. Dus de graden liggen werkelijk in een verzameling van
grootte `n−1`, en het duivenhokprincipe maakt het af. ∎

De voorwaarde `n ≥ 2` doet echt werk, en het is precies het soort dat bij het overschrijven
sneuvelt. Op één knoop is de bewering onwaar — er is maar één knoop, dus geen paar om te
vergelijken. De verificatie legt de voorwaarde expliciet vast in plaats van op de lezer te
vertrouwen:

```python
@theorem("Any graph with n >= 2 has two vertices of equal degree", chapter=3)
def two_vertices_share_a_degree(g: Graph) -> bool | None:
    if g.n < 2:
        return None          # not a pass -- the hypothesis fails, so this graph says nothing
    degrees = [g.degree(v) for v in g.vertices()]
    return len(set(degrees)) < len(degrees)
```

Dat er `None` teruggegeven wordt in plaats van `True` doet ertoe. `True` zou betekenen "de
stelling gold hier", en dat is een leugen over een graaf waarover de stelling niets zegt.

## Graadrijen

De **graadrij** is de lijst van graden, gebruikelijk niet-stijgend geordend. Het is een
invariant: knopen hernoemen kan haar niet veranderen. Ze is dus een snelle manier om te
bewijzen dat twee grafen *niet* isomorf zijn — en, zoals hoofdstuk 5 laat zien, een ernstig
onvolledige manier om te bewijzen dat ze het wel zijn.

De interessante vraag loopt de andere kant op. Gegeven een lijst getallen, bestaat er een
graaf met die graden? Zo'n lijst heet **grafisch**.

Sommige falen om eenvoudige redenen. `[1, 1, 1]` heeft een oneven som, dus het handdruklemma
doodt haar. `[5, 1, 1, 1]` heeft een knoop die vijf buren wil in een graaf met vier knopen.
Maar `[3, 3, 3, 1]` heeft een even som en geen te grote plaats, en is nog steeds niet grafisch
— en inzien waarom vergt een argument in plaats van een waarneming.

## Havel–Hakimi

Het algoritme is gulzig en het bewijs ís het algoritme.

> **Stelling (Havel–Hakimi).** Zij `d₁ ≥ d₂ ≥ … ≥ dₙ` met `d₁ ≥ 1`. De rij is grafisch dan en
> slechts dan als de rij die ontstaat door `d₁` te verwijderen en één af te trekken van elk van
> de volgende `d₁` plaatsen, grafisch is.

*Bewijs.* De ene richting is eenvoudig: gegeven een graaf voor de gereduceerde rij, voeg een
nieuwe knoop toe verbonden met de `d₁` knopen waarvan de graad verlaagd werd, en je hebt een
graaf voor de oorspronkelijke rij.

De andere richting is de inhoud. Stel dat `G` de oorspronkelijke rij realiseert, met `v` de
knoop van graad `d₁`. Grenst `v` aan precies de `d₁` knopen van eerstvolgend hoogste graad,
verwijder hem dan en je bent klaar. Zo niet, dan zijn er knopen `x` en `y` met
`deg(x) ≥ deg(y)`, waarbij `v` aan `y` grenst maar niet aan `x`. Omdat `deg(x) ≥ deg(y)` en
`x` meer met `v`'s niet-buren verbonden is dan `y`, moet er een knoop `z` zijn die aan `x`
grenst maar niet aan `y`. Verwijder nu de kanten `vy` en `xz`, en voeg `vx` en `yz` toe. Elke
graad blijft gelijk, en `v` grenst nu aan `x` in plaats van aan `y`. Herhaal; elke verwisseling
verhoogt strikt het aantal knopen van hoge graad dat aan `v` grenst, dus het proces eindigt in
een realisatie van de vereiste vorm. ∎

Dat **twee-verwisselingsargument** — ruil een paar kanten voor een paar dat alle graden
behoudt — is het onthouden waard. Het is dezelfde zet die de stelling over vermeerderende
paden in hoofdstuk 14 bewijst en de voorwaarde van Ore in hoofdstuk 20.

Het algoritme is de stelling, herhaald toegepast:

```python
from graphs.degree import is_graphical_havel_hakimi, realise

print(is_graphical_havel_hakimi([3, 3, 3, 1]))    # False
print(is_graphical_havel_hakimi([3, 3, 2, 2, 1, 1]))  # True
print(sorted(realise([3, 3, 2, 2, 1, 1]).edges()))
# [(0, 1), (0, 4), (0, 5), (1, 2), (1, 3), (2, 3)]
```

Omdat het bewijs constructief is, geeft `realise` je een werkelijke graaf en niet een ja.

## Erdős–Gallai

Er bestaat ook een niet-constructieve karakterisering, en die gebruik je wanneer je een
criterium wilt in plaats van een graaf.

> **Stelling (Erdős–Gallai).** Een niet-stijgende rij niet-negatieve gehele getallen met even
> som is grafisch dan en slechts dan als voor elke `k` van `1` tot `n` geldt:
>
> `Σ_{i≤k} dᵢ ≤ k(k−1) + Σ_{i>k} min(dᵢ, k)`.

De ongelijkheid zegt iets dat je kunt lezen: de `k` knopen van hoogste graad moeten hun graad
kwijt kunnen, ofwel onderling — hoogstens `k(k−1)` kanteindpunten — ofwel door naar de rest te
reiken, waar elke overblijvende knoop `i` er hoogstens `min(dᵢ, k)` kan opnemen. Kunnen ze dat
niet, dan is de rij onmogelijk.

Twee stellingen, twee algoritmen, en geen reden om aan te nemen dat ze het eens zijn. Daarom
controleert de verificatie beide tegen uitputtend zoeken en niet tegen elkaar:

```
  held      ch 3  Havel-Hakimi agrees with brute-force realisability  (52 graphs)
  held      ch 3  Erdos-Gallai agrees with Havel-Hakimi  (52 graphs)
  held      ch 3  Havel-Hakimi's construction really has the requested degrees  (52 graphs)
```

De eerste regel is degene die telt. Havel–Hakimi tegen Erdős–Gallai controleren zou alleen
vaststellen dat twee implementaties van mij het eens zijn, wat ze kunnen zijn terwijl ze
allebei fout zijn. Controleren tegen "probeer elke graaf op `n` knopen en kijk" kan zo niet
falen.

## Probeer het

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.degree import is_graphical_havel_hakimi, is_graphical_erdos_gallai, is_graphical_bruteforce
for s in ([3,3,3,3], [3,3,3,1], [1,1,1], [5,1,1,1,1,1], [2,2,2]):
    hh = is_graphical_havel_hakimi(list(s))
    eg = is_graphical_erdos_gallai(list(s))
    bf = is_graphical_bruteforce(list(s))
    print(f'{str(s):<18} Havel-Hakimi={hh!s:<6} Erdos-Gallai={eg!s:<6} exhaustive={bf}')
"
```

```
[3, 3, 3, 3]       Havel-Hakimi=True   Erdos-Gallai=True   exhaustive=True
[3, 3, 3, 1]       Havel-Hakimi=False  Erdos-Gallai=False  exhaustive=False
[1, 1, 1]          Havel-Hakimi=False  Erdos-Gallai=False  exhaustive=False
[5, 1, 1, 1, 1, 1] Havel-Hakimi=True   Erdos-Gallai=True   exhaustive=True
[2, 2, 2]          Havel-Hakimi=True   Erdos-Gallai=True   exhaustive=True
```

Let op de vierde: `[5, 1, 1, 1, 1, 1]` is grafisch op **zes** knopen — het is de ster `K_{1,5}`
— ook al zou het op vijf onmogelijk zijn. Graadrijen dragen `n` met zich mee, en dat vergeten
is de meest voorkomende manier om deze paragraaf verkeerd te lezen.

## Oefeningen

1. Kunnen negen mensen elk precies drie anderen de hand schudden? Verantwoord je antwoord met
   het handdruklemma.
2. Is `[4, 3, 2, 1, 0]` grafisch? Voer Havel–Hakimi met de hand uit.
3. Wat is de som van de graden van de Petersen-graaf, en wat zegt dat over zijn aantal kanten?
4. De stelling "twee knopen delen een graad" vereist `n ≥ 2`. Geef de graaf op één knoop en leg
   precies uit welke stap van het bewijs faalt.

Oplossingen in Bijlage E.

## Kernpunten

- Het handdruklemma is een dubbeltelling, en dubbeltelling is de werkpaardtechniek van dit
  boek.
- Het aantal knopen van oneven graad is altijd even. De meeste pariteitsargumenten over grafen
  herleiden hiertoe.
- De graadrij is een invariant, dus ze kan isomorfie weerleggen maar nooit bewijzen.
- Havel–Hakimi beslist realiseerbaarheid door constructie; Erdős–Gallai beslist haar door
  ongelijkheid. Beide worden hier bewezen, en beide worden tegen uitputtend zoeken
  gecontroleerd en niet tegen elkaar.
- Heeft een stelling een voorwaarde als `n ≥ 2`, codeer die dan als "dit geval zegt niets" en
  niet als "dit geval slaagde".
