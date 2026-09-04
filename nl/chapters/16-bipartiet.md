# Hoofdstuk 16 — Bipartiete grafen

Een graaf is **bipartiet** wanneer zijn knopen uiteenvallen in twee verzamelingen waarbij elke kant
tussen beide oversteekt. Equivalent: `χ(G) ≤ 2`. Dit is de netste karakterisering in het boek, en de
enige plaats waar een structurele eigenschap een werkelijk eenvoudige test heeft.

## De stelling

> **Stelling (König, 1916).** `G` is bipartiet dan en slechts dan als hij geen oneven cykel bevat.

*Bewijs.* Is `G` bipartiet met delen `A` en `B`, dan wisselt elke cykel ertussen af, dus terugkeren
naar het startpunt vergt een even aantal stappen.

Omgekeerd, stel dat `G` geen oneven cykel heeft. Behandel elke component apart. Kies een wortel `r`
en kleur elke knoop naar de pariteit van `d(r, v)`. Stel dat een kant `uv` twee knopen van gelijke
pariteit verbond. Neem kortste paden van `r` naar `u` en naar `v`, en zij `x` hun laatste
gemeenschappelijke knoop. De twee padstukken vanaf `x`, plus de kant `uv`, vormen een cykel van
lengte `(d(r,u) − d(r,x)) + (d(r,v) − d(r,x)) + 1`, en die is oneven omdat `d(r,u)` en `d(r,v)`
dezelfde pariteit hebben. Tegenspraak. ∎

Het bewijs is een algoritme: BFS, kleur naar de pariteit van het niveau, en elke kant *binnen* een
niveau benoemt een oneven cykel. Dat is de waarneming over BFS-niveaus uit hoofdstuk 8, nu aan het
werk.

```python
def two_colouring(g):
    colour = {}
    for source in g.vertices():
        if source in colour:
            continue
        colour[source] = 0
        queue = deque([source])
        while queue:
            v = queue.popleft()
            for w in g.neighbours(v):
                if w not in colour:
                    colour[w] = 1 - colour[v]
                    queue.append(w)
                elif colour[w] == colour[v]:
                    return None          # an edge inside a level: odd cycle
    return colour
```

`O(n + m)`. Vergelijk dat met `χ(G) ≤ 3`, wat `NP`-volledig is. De sprong in moeilijkheid tussen
twee kleuren en drie is de scherpste complexiteitsgrens in de grafentheorie, en hij gebeurt hier.

## De controle die circulair zou zijn geweest

"Bipartiet dan en slechts dan als geen oneven cykel" verifiëren is een valstrik. De voor de hand
liggende test — `is_bipartite` vergelijken met `has_odd_cycle` — is waardeloos wanneer
`has_odd_cycle` geïmplementeerd is als `not is_bipartite`, en zo implementeert een verstandige
bibliotheek het nu eenmaal.

Daarom somt de verificatie cykels rechtstreeks op:

```python
def _has_odd_cycle_bruteforce(g):
    for size in range(3, g.n + 1, 2):
        for subset in itertools.combinations(g.vertices(), size):
            first, *rest = subset
            for tail in itertools.permutations(rest):
                walk = (first,) + tail
                if all(g.has_edge(walk[i], walk[(i+1) % size]) for i in range(size)):
                    return True
    return False
```

Exponentieel, en de enige eerlijke manier om precies deze stelling te controleren:

```
  held      ch16  Konig: G is bipartite iff it has no odd cycle  (52 graphs)
```

## Noodzakelijk is niet voldoende

Bipartiete grafen zijn driehoekvrij. Het omgekeerde faalt, en de verificatie registreert het als een
stelling waarvan verwacht wordt dat ze weerlegd wordt:

```
  refuted   ch16  Triangle-free does not imply bipartite  (27 graphs)
```

Het getuigenis is `C₅`: geen driehoek, maar wel een oneven cykel, dus `χ = 3`. Dit doet er meer toe
dan het lijkt. "Driehoekvrij" is een *lokale* voorwaarde — controleer elk drietal knopen — terwijl
bipartietheid *globaal* is. Geen enkele hoeveelheid lokaal controleren stelt haar vast, en hoofdstuk
27 gaat over hoever driehoekvrijheid alleen een graaf beperkt.

```python
print(is_bipartite(cycle(5)), is_bipartite(cycle(6)))   # False True
print(is_bipartite(petersen()), chromatic_number(petersen()))   # False 3
```

De Petersen-graaf heeft omtrek 5 — geen driehoeken, geen vierhoeken — en is nog steeds niet
bipartiet.

## Waarom bipartiete grafen eenvoudig zijn

Een lange lijst `NP`-moeilijke problemen wordt polynomiaal op bipartiete grafen:

| Probleem | Algemeen | Bipartiet |
|---|---|---|
| Maximale koppeling | `O(n³)` (bloesems) | `O(m√n)` |
| Minimale knopenoverdekking | `NP`-moeilijk | `=` maximale koppeling (König, h. 14) |
| Grootste onafhankelijke verzameling | `NP`-moeilijk | `n −` maximale koppeling |
| 3-kleuring | `NP`-volledig | triviaal: `χ ≤ 2` |

De reden is telkens dezelfde, en het is die uit hoofdstuk 14: de beperkingsmatrix van een bipartiete
graaf is **totaal unimodulair**, dus het natuurlijke lineaire programma heeft gehele optimale
hoekpunten en LP-dualiteit geeft je de combinatorische min-max-stelling rechtstreeks. Oneven cykels
zijn precies wat die eigenschap vernietigt.

"Bevat geen oneven cykel" is dus geen curiositeit. Het is de structurele reden waarom een hele familie
problemen in moeilijkheid instort.

## Probeer het

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import cycle, petersen, complete_bipartite
from graphs.algorithms import is_bipartite, two_colouring, chromatic_number
for name, g in [('C5', cycle(5)), ('C6', cycle(6)), ('K33', complete_bipartite(3,3)), ('petersen', petersen())]:
    print(f'{name:<9} bipartite={is_bipartite(g)!s:<6} chi={chromatic_number(g)}')
print()
print('C6 two-colouring:', two_colouring(cycle(6)))
print('C5 two-colouring:', two_colouring(cycle(5)))
"
```

```
C5        bipartite=False  chi=3
C6        bipartite=True   chi=2
K33       bipartite=True   chi=2
petersen  bipartite=False  chi=3

C6 two-colouring: {0: 0, 1: 1, 5: 1, 2: 0, 4: 0, 3: 1}
C5 two-colouring: None
```

## Oefeningen

1. Toon aan dat een graaf bipartiet is dan en slechts dan als elke deelgraaf een onafhankelijke
   verzameling heeft met minstens de helft van zijn knopen.
2. Hoeveel kanten kan een bipartiete graaf op `n` knopen hebben? Welke graaf bereikt dat?
3. Geef een graaf van omtrek 5 die niet bipartiet is, anders dan `C₅` en de Petersen-graaf.
4. Leg uit waarom "driehoekvrij" in `O(n³)` gecontroleerd kan worden terwijl "bipartiet" `O(n + m)`
   nodig heeft — en waarom de goedkopere test de sterkere eigenschap is.

Oplossingen in Bijlage E.

## Kernpunten

- Bipartiet ⟺ geen oneven cykel ⟺ `χ ≤ 2`, alle drie testbaar in `O(n + m)` met de pariteit van
  BFS-niveaus.
- Een kant binnen een BFS-niveau *is* een oneven cykel. Het bewijs en het algoritme zijn hetzelfde
  object.
- Deze stelling verifiëren vergt cykels onafhankelijk opsommen; de natuurlijke implementatie van "heeft
  een oneven cykel" is "is niet bipartiet", en die twee tegen elkaar controleren bewijst niets.
- Driehoekvrij impliceert niet bipartiet. `C₅` is het kleinste getuigenis; de Petersen-graaf heeft
  omtrek 5 en faalt nog steeds.
- Bipartietheid maakt koppeling, knopenoverdekking en onafhankelijke verzameling alle polynomiaal,
  omdat ze de beperkingsmatrix totaal unimodulair maakt. Oneven cykels breken dat.
