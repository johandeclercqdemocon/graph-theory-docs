# Hoofdstuk 7 — Opspannende bomen en de formule van Cayley

Een **opspannende boom** van `G` is een deelgraaf die een boom is en elke knoop bevat. Het is de
goedkoopste manier om een graaf samenhangend te houden, en tellen hoeveel een graaf er heeft
blijkt een veel rijkere vraag dan het lijkt.

## Bestaan

![Opspannende boom van C6](../../figures/spanning-tree.svg)

Een opspannende boom van `C₆`: verwijder een willekeurige kant van de cykel en wat overblijft is
een boom op alle zes de knopen. `C₆` heeft precies zes opspannende bomen, één per verwijderde
kant.

> **Stelling.** Elke samenhangende graaf heeft een opspannende boom.

*Bewijs.* Neem onder alle samenhangende opspannende deelgrafen van `G` er een met de minste
kanten; noem hem `T`. Bevatte `T` een cykel, dan zou een kant van die cykel verwijderen hem
samenhangend laten (hoofdstuk 6) en minder kanten gebruiken, in tegenspraak met minimaliteit.
Dus `T` is samenhangend en cykelvrij: een boom. ∎

Dat is het **extremale argument**, en het is na de langste-padtruc de tweede algemene zet die
een naam verdient. Neem het extreme object, en toon dan dat elk mankement je verder zou laten
gaan. De hoofdstukken 13 en 27 gebruiken het opnieuw.

Het bewijs is geen algoritme — "neem een minimale" is geen procedure — maar er volgen meteen
twee algoritmen uit, en hoofdstuk 8 geeft beide: de breedte-eerstboom en de diepte-eerstboom van
een samenhangende graaf zijn opspannende bomen, elk berekend in `O(n + m)`.

## Ze tellen

Hoeveel opspannende bomen heeft een graaf? Voor `K₅` zegt brute kracht 125. Voor `K₆`, 1296.
Dat zijn `5³` en `6⁴`.

> **Stelling (Cayley, 1889).** De volledige graaf `K_n` heeft precies `n^(n−2)` gelabelde
> opspannende bomen — equivalent: er zijn `n^(n−2)` verschillende bomen op een vaste
> knopenverzameling van grootte `n`.

De uitputtende telling is het ermee eens, en dat is de moeite waard voordat je enig bewijs
vertrouwt:

```
  K_2: cayley n^(n-2) =      1   enumerated = 1
  K_3: cayley n^(n-2) =      3   enumerated = 3
  K_4: cayley n^(n-2) =     16   enumerated = 16
  K_5: cayley n^(n-2) =    125   enumerated = 125
  K_6: cayley n^(n-2) =   1296   enumerated = 1296
```

Het woord **gelabeld** doet cruciaal werk. Op isomorfie na zijn er maar 6 bomen op 6 knopen; er
zijn 1296 bomen *op de knopenverzameling* `{0,…,5}`. Het onderscheid uit hoofdstuk 5 tussen
gelijkheid en isomorfie is precies het verschil, en de twee door elkaar halen laat de formule
van Cayley absurd lijken.

## De Prüfer-bijectie

Er zijn verschillende bewijzen. Dit is het beste, want het telt de bomen niet alleen — het
*benoemt* ze.

> **Stelling (Prüfer).** Voor `n ≥ 2` bestaat er een bijectie tussen gelabelde bomen op
> `{0, …, n−1}` en rijen van lengte `n − 2` over `{0, …, n−1}`.

Omdat er `n^(n−2)` zulke rijen zijn, volgt de formule van Cayley onmiddellijk.

**Coderen.** Zolang er meer dan twee knopen over zijn, zoek het blad met het kleinste label,
noteer zijn unieke buur, en verwijder het blad. Stop wanneer er twee knopen resten.

```python
def to_prufer(t):
    degree = [t.degree(v) for v in t.vertices()]
    neighbours = [set(t.neighbours(v)) for v in t.vertices()]
    seq = []
    for _ in range(t.n - 2):
        leaf = min(v for v in t.vertices() if degree[v] == 1)
        parent = next(iter(neighbours[leaf]))
        seq.append(parent)
        degree[leaf] = 0
        neighbours[parent].discard(leaf)
        degree[parent] -= 1
    return seq
```

**Decoderen.** Gegeven een rij, bereken de graad van elke knoop als één plus het aantal keren
dat hij voorkomt. Neem dan herhaaldelijk de knoop met het kleinste label van graad 1 die nog
niet gebruikt is, verbind hem met de volgende plaats in de rij, en verlaag beide graden. Verbind
ten slotte de twee overgebleven knopen van graad 1.

*Bewijs dat deze elkaars inverse zijn.* De sleutelwaarneming is dat **een knoop precies
`deg(v) − 1` keer in de rij voorkomt**. Een blad komt er dus nooit in voor, en een inwendige
knoop minstens één keer. De decodeerder kan dus het bij elke stap verwijderde blad
identificeren — het is het kleinste label dat niet in de resterende rij voorkomt en nog niet
verbruikt is — en dat is precies het blad dat de codeerder koos. Per inductie naar `n` maakt elke
stap van de decodeerder de overeenkomstige stap van de codeerder ongedaan. Beide afbeeldingen
zijn dus welgedefinieerd en elkaars inverse, dus elk is een bijectie. ∎

Die graadwaarneming ís het hele bewijs, en het is ook de snelste manier om informatie uit een
Prüfer-rij te lezen zonder haar te decoderen:

```python
from graphs.core import Graph, path
from graphs.generate import to_prufer, from_prufer

star = Graph(5, [(0, 1), (0, 2), (0, 3), (0, 4)])
print(to_prufer(star))          # [0, 0, 0]
print(to_prufer(path(5)))       # [1, 2, 3]
print(sorted(from_prufer([0, 0, 0]).edges()))
# [(0, 1), (0, 2), (0, 3), (0, 4)]
```

Het middelpunt van de ster heeft graad 4 en komt `4 − 1 = 3` keer voor. De twee uiteinden van
het pad hebben graad 1 en komen nooit voor. Je kunt de graadrij er rechtstreeks van aflezen.

Een gevolg dat rechtstreeks bewijzen omslachtig zou zijn, valt er gratis uit: **het aantal
gelabelde bomen op `n` knopen met voorgeschreven graden `d₁, …, dₙ` is de multinomiaalcoëfficiënt
`(n−2)! / ∏(dᵢ − 1)!`** — want dat is precies hoeveel rijen elke knoop `i` precies `dᵢ − 1` keer
laten voorkomen.

## Tellen voor algemene grafen

De formule van Cayley behandelt `K_n`. Voor een willekeurige graaf is het antwoord de
**matrix-boomstelling**: het aantal opspannende bomen is gelijk aan elke cofactor van de
Laplace-matrix. Het rekent in `O(n³)` met een determinant, zonder iets op te sommen.

Die stelling heeft de Laplaciaan nodig en wacht dus tot hoofdstuk 30. Het is nu al de moeite
waard te vermelden als de grootste kloof tussen wat dit hoofdstuk kan en wat mogelijk is:
`spanning_trees` in de bibliotheek van dit boek somt `C(m, n−1)` deelverzamelingen op en test ze
elk, en daarom stopt de Cayley-controle hierboven bij `K₆`. De matrix-boomstelling haalt de 1296
van `K₆` uit een 5×5-determinant.

## Probeer het

Kijk hoe de bijectie heen en terug loopt op een willekeurige boom, en controleer de
graadwaarneming:

```bash
python -c "
import sys, random; sys.path.insert(0, '.')
from graphs.generate import random_tree, to_prufer, from_prufer
rng = random.Random(11)
t = random_tree(8, rng)
seq = to_prufer(t)
print('prufer sequence:', seq)
print('degrees:        ', [t.degree(v) for v in t.vertices()])
print('appearances+1:  ', [seq.count(v) + 1 for v in t.vertices()])
print('round trips:    ', sorted(from_prufer(seq).edges()) == sorted(t.edges()))
"
```

```
prufer sequence: [7, 7, 7, 3, 2, 7]
degrees:         [1, 1, 2, 2, 1, 1, 1, 5]
appearances+1:   [1, 1, 2, 2, 1, 1, 1, 5]
round trips:     True
```

De tweede en derde regel zijn identiek, en dat is het lemma waar het hele bewijs om draait.

## Oefeningen

1. Hoeveel gelabelde opspannende bomen heeft `K₄`? Controleer tegen de formule van Cayley.
2. Bereken met de hand de Prüfer-rij van het pad `0—1—2—3`.
3. Een knoop komt `deg(v) − 1` keer voor in een Prüfer-rij. Wat zegt dat over de labels die er
   nooit in voorkomen?
4. Er zijn 1296 gelabelde bomen op 6 knopen maar slechts 6 op isomorfie na. Verklaar het verschil
   in één zin.

Oplossingen in Bijlage E.

## Kernpunten

- Elke samenhangende graaf heeft een opspannende boom, via het extremale argument: neem een
  minimale samenhangende opspannende deelgraaf en toon dat hij geen cykel kan bevatten.
- `K_n` heeft `n^(n−2)` **gelabelde** opspannende bomen. Op isomorfie na is het aantal veel
  kleiner, en de twee door elkaar halen laat de formule fout lijken.
- De Prüfer-bijectie bewijst de formule van Cayley door elke boom van een naam te voorzien. Het
  lemma dat haar draagt: knoop `v` komt precies `deg(v) − 1` keer voor.
- Boomtellingen met voorgeschreven graden vallen zonder extra werk uit dezelfde bijectie, als een
  multinomiaalcoëfficiënt.
- Opspannende bomen van een algemene graaf tellen is de matrix-boomstelling, `O(n³)` via een
  determinant. De opsommer van dit hoofdstuk is exponentieel en stopt bij `K₆`.
