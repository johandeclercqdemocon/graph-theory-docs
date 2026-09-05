# Hoofdstuk 27 — Extremale grafentheorie

Eén vraag, keer op keer gesteld: **hoeveel kanten kan een graaf hebben voordat een of andere structuur
gedwongen wordt te verschijnen?** Hoofdstuk 16 toonde dat driehoekvrij niet bipartiet impliceert; dit
hoofdstuk vraagt hoeveel kanten driehoekvrijheid je kost.

## Mantel

> **Stelling (Mantel, 1907).** Een driehoekvrije graaf op `n` knopen heeft hoogstens `n²/4` kanten, en
> de volledig bipartiete graaf `K_{⌈n/2⌉,⌊n/2⌋}` is het unieke extremale voorbeeld.

*Bewijs.* Zij `uv` een kant. Omdat `G` driehoekvrij is, hebben `u` en `v` geen gemeenschappelijke
buur, dus `deg(u) + deg(v) ≤ n`. Sommeren over alle kanten geeft

`Σ_{uv ∈ E} (deg(u) + deg(v)) ≤ mn`.

De linkerkant telt elke knoop `v` één keer per kant eraan, wat `deg(v)²` bijdraagt. Dus
`Σ_v deg(v)² ≤ mn`. Per Cauchy–Schwarz geldt `Σ deg(v)² ≥ (Σ deg(v))²/n = 4m²/n`. Samengevoegd:
`4m²/n ≤ mn`, dus `m ≤ n²/4`. ∎

Twee technieken in vijf regels: **dubbeltelling** (hoofdstuk 3, vierde optreden) en
**Cauchy–Schwarz**, de standaardmanier om een som van kwadraten in een grens om te zetten. Beide keren
in dit deel van het boek terug.

```
  held      ch27  Mantel: a triangle-free graph has m <= n^2/4  (27 graphs)
```

## Turán

De veralgemening vervangt de driehoek door `K_{r+1}`.

> **Stelling (Turán, 1941).** Een graaf zonder `K_{r+1}` heeft hoogstens `(1 − 1/r) n²/2` kanten, en
> de unieke extremale graaf is de **Turán-graaf** `T(n,r)`: de volledig `r`-delige graaf met zo gelijk
> mogelijke delen.

Mantel is het geval `r = 2`.

Het extremale voorbeeld is het bekijken waard. Om `K_{r+1}` te vermijden met zoveel mogelijk kanten,
splits je de knopen in `r` groepen en verbind je alles *tussen* de groepen. Elke kliek kiest hoogstens
één knoop per groep, dus klieken hebben grootte hoogstens `r`. De delen gelijk maken maximaliseert het
aantal kanten — een toepassing van dezelfde convexiteit die Cauchy–Schwarz codeert.

De verificatie controleert dit door **elke** graaf op `n` knopen op te sommen en het werkelijke maximum
te vinden, in plaats van de formule te vertrouwen:

```python
def max_edges_without_clique(n, k):
    pairs = list(itertools.combinations(range(n), 2))
    best = 0
    for mask in range(1 << len(pairs)):
        chosen = [p for i, p in enumerate(pairs) if mask >> i & 1]
        if len(chosen) > best and not has_clique(Graph(n, chosen), k):
            best = len(chosen)
    return best
```

```
  held      ch27  Turan: the K_{r+1}-free maximum is exactly the Turan graph's edge count  (8 graphs)
```

`2^C(n,2)` grafen, dus dit stopt bij `n = 5`. Het volstaat om een verkeerd opgeschreven formule te
vangen, en daarvoor dient het.

## Erdős–Stone: het algemene antwoord

Turán behandelt volledige grafen. En als je een willekeurige `H` verbiedt?

> **Stelling (Erdős–Stone, 1946).** Voor elke graaf `H` met chromatisch getal `χ(H) = r + 1` is het
> maximale aantal kanten in een `H`-vrije graaf op `n` knopen
>
> `(1 − 1/r) n²/2 + o(n²)`.

Dit wordt soms de hoofdstelling van de extremale grafentheorie genoemd, en de reden is haar reikwijdte:
**het antwoord hangt van `H` alleen af via zijn chromatisch getal.** Een driehoek verbieden en de
Petersen-graaf verbieden geven dezelfde hoofdterm, want beide hebben `χ = 3`. Elk detail van de
structuur van `H` is bij deze resolutie onzichtbaar.

Er is één enorme uitzondering, en daar liggen de moeilijke open problemen van het vak. Is `χ(H) = 2` —
dat wil zeggen, is `H` **bipartiet** — dan geeft de stelling `o(n²)` en zegt ze verder niets. De
werkelijke orde bepalen voor bipartiete `H` is het **probleem van Zarankiewicz**, en dat is in het
algemeen open. Zelfs `H = C₈` is niet volledig opgelost. De bekende gevallen:

- `H = C₄`: het antwoord is `½ n^{3/2}(1 + o(1))`, en de extremale grafen komen uit de eindige
  meetkunde.
- `H = K_{3,3}`: `Θ(n^{5/3})`, met boven- en ondergrenzen die alleen op constanten na overeenkomen.

Extremale grafentheorie is dus in wezen opgelost voor niet-bipartiete `H` en in wezen open voor
bipartiete `H`. Dat is een ongebruikelijke vorm voor een vakgebied, en het is goed te weten voordat je
op zoek gaat naar open problemen.

## Probeer het

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.extremal import max_edges_without_clique, turan_bound, turan_graph
print(f\"  {'n':>3} {'r':>3} {'exhaustive max':>15} {'Turan bound':>12} {'(1-1/r)n^2/2':>14}\")
for n in range(3, 6):
    for r in (2, 3):
        exact = max_edges_without_clique(n, r + 1)
        print(f'  {n:>3} {r:>3} {exact:>15} {turan_bound(n, r):>12} {(1 - 1/r) * n * n / 2:>14.2f}')
"
```

```
    n   r  exhaustive max  Turan bound   (1-1/r)n^2/2
    3   2               2            2           2.25
    3   3               3            3           3.00
    4   2               4            4           4.00
    4   3               5            5           5.33
    5   2               6            6           6.25
    5   3               8            8           8.33
```

Het uitputtende maximum komt elke keer exact overeen met het aantal kanten van de Turán-graaf. De
laatste kolom — de nette formule `(1 − 1/r)n²/2` — is een *bovengrens*, alleen scherp wanneer `r` een
deler van `n` is. Bij `n = 4, r = 2` is ze exact op 4; bij `n = 5, r = 2` zegt ze 6,25 tegen een echte
6, en bij `n = 5, r = 3` zegt ze 8,33 tegen een echte 8.

De verschillen zijn hier klein, en ze zijn de reden dat extremale resultaten geformuleerd worden in
termen van het extremale *object* en niet van de afgeronde formule. Het aantal kanten van de
Turán-graaf is de stelling; `(1 − 1/r)n²/2` is een handige asymptotiek die nooit kleiner en zelden
gelijk is.

## Oefeningen

1. Verifieer de grens van Mantel voor `n = 5` door een driehoekvrije graaf met 6 kanten te vinden.
2. Waarom maximaliseert het gelijk maken van de delen van de Turán-graaf het aantal kanten? Gebruik
   convexiteit.
3. Erdős–Stone zegt dat het antwoord van `H` alleen afhangt via `χ(H)`. Bepaal de chromatische getallen
   van `K₃`, `K₄` en de Petersen-graaf, en zeg welke twee van de drie dezelfde hoofdterm geven.
4. Waarom zegt Erdős–Stone niets bruikbaars wanneer `H` bipartiet is?

Oplossingen in Bijlage E.

## Kernpunten

- Mantel: driehoekvrij impliceert `m ≤ n²/4`, extremaal bij de gebalanceerde volledig bipartiete
  graaf. Bewezen met dubbeltelling plus Cauchy–Schwarz.
- Turán: geen `K_{r+1}` impliceert `m ≤ (1 − 1/r)n²/2`, extremaal bij de gebalanceerde volledig
  `r`-delige graaf.
- De nette formule is een bovengrens; het exacte antwoord is het aantal kanten van de Turán-graaf, en
  de twee verschillen wanneer `r` geen deler van `n` is.
- Erdős–Stone: voor elke `H` hangt het antwoord alleen af van `χ(H)`. Alle structuur voorbij het
  chromatisch getal is onzichtbaar.
- Is `χ(H) = 2`, dan zwijgt de stelling, en dat zwijgen is het probleem van Zarankiewicz — waar de open
  vragen van het vak liggen.
