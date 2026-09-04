# Hoofdstuk 14 — Koppeling

Een **koppeling** is een verzameling kanten waarvan er geen twee een knoop delen. Een grootste
vinden is een van de weinige werkelijk moeilijk ogende combinatorische problemen die toch in
polynomiale tijd oplosbaar blijken — en op bipartiete grafen is het hoofdstuk 13 met een hoed op.

## Vermeerderende paden

Zij `M` een koppeling. Een knoop is **bedekt** wanneer een kant van `M` hem raakt, en **vrij**
anders. Een **alternerend pad** wisselt af tussen kanten buiten `M` en kanten binnen `M`. Een
**vermeerderend pad** is een alternerend pad waarvan beide eindpunten vrij zijn.

Keer een vermeerderend pad om — neem zijn niet-koppelingskanten op in `M` en verwijder zijn
koppelingskanten — en je krijgt een koppeling met precies één kant meer, want het pad heeft één
niet-koppelingskant meer dan koppelingskanten.

> **Stelling (Berge, 1957).** `M` is maximaal dan en slechts dan als er geen `M`-vermeerderend pad
> bestaat.

*Bewijs.* Bestaat er een vermeerderend pad, dan geeft omkeren een grotere koppeling, dus `M` is niet
maximaal.

Omgekeerd, stel dat `M` niet maximaal is en zij `N` groter. Beschouw het symmetrisch verschil
`M △ N` en bekijk de graaf die het vormt. Elke knoop heeft er graad hoogstens 2 — hoogstens één kant
uit elke koppeling — dus elke component is een pad of een even cykel, met kanten die afwisselen
tussen `M` en `N`. Cykels gebruiken er evenveel van elk. Omdat `|N| > |M|` moet een component meer
`N`-kanten dan `M`-kanten hebben, en zo'n component kan alleen een pad zijn dat met `N`-kanten begint
en eindigt. Zijn eindpunten zijn vrij in `M`, dus het is een `M`-vermeerderend pad. ∎

**Het symmetrisch-verschilargument is de techniek om te bewaren.** Je object vergelijken met een
hypothetisch beter object en kijken waar ze verschillen, is hoe vrijwel elk koppelingsresultaat
bewezen wordt, en de waarneming dat `M △ N` maximale graad 2 heeft is wat de componenten hanteerbaar
maakt.

De stelling van Berge verandert het vinden van een maximale koppeling in: zoek een vermeerderend
pad, keer het om, herhaal. Hoogstens `n/2` iteraties.

## Het bipartiete geval, en wat erin verborgen zit

Op een bipartiete graaf is het zoeken naar een vermeerderend pad een rechttoe rechtaan alternerende
zoektocht vanaf elke vrije linkerknoop:

```python
def try_augment(v, visited):
    for w in sorted(g.neighbours(v)):
        if w in visited:
            continue
        visited.add(w)
        if w not in match or try_augment(match[w], visited):
            match[w] = v
            match[v] = w
            return True
    return False
```

`O(nm)` in totaal. Hopcroft–Karp verbetert dit tot `O(m √n)` door per fase een maximale *verzameling*
kortste vermeerderende paden te vinden.

Die zoektocht is correct op bipartiete grafen en **fout in het algemeen**, en de reden is het bekijken
waard. In een graaf met een oneven cykel kan een alternerende wandeling terugkeren naar een knoop met
de tegenovergestelde pariteit, en de zoektocht kan niet zien of ze een vermeerderend pad heeft
gevonden of rondgelopen is. Edmonds' bloesemalgoritme uit 1965 lost dit op door oneven cykels —
"bloesems" — samen te trekken, en het is het artikel dat het idee introduceerde van polynomiale tijd
als de definitie van hanteerbaar.

De verificatie registreert de beperking als een stelling waarvan verwacht wordt dat ze weerlegd wordt:

```
  refuted   ch14  Augmenting paths find a maximum matching in any graph  (1 graphs)
```

Het getuigenis is `C₇` met de linkerzijde opgegeven als `{0,1,2,6}`: de routine geeft een koppeling
van grootte 2 terug waar er 3 bestaat. Het is de moeite waard op te merken hoe *smal* dat getuigenis
is. Op `C₃` en `C₅` geeft dezelfde routine voor **elke** keuze van linkerzijde het juiste antwoord,
dus een test op kleine oneven cykels zou niets vinden en concluderen dat de code in orde is.

## De stelling van Hall

> **Stelling (Hall, 1935).** Een bipartiete graaf met delen `L` en `R` heeft een koppeling die elke
> knoop van `L` bedekt dan en slechts dan als `|N(S)| ≥ |S|` voor elke `S ⊆ L`.

De voorwaarde is duidelijk noodzakelijk: `S` heeft `|S|` verschillende partners nodig, allemaal
binnen `N(S)`.

*Bewijs van de voldoendheid.* Stel dat geen koppeling `L` bedekt, en neem een maximale koppeling `M`
met een vrije `u ∈ L`. Zij `Z` de verzameling knopen die vanuit `u` via alternerende paden bereikbaar
zijn. Geen knoop van `Z ∩ R` is vrij — dat zou een vermeerderend pad geven, in tegenspraak met
maximaliteit — dus elke knoop van `Z ∩ R` is gekoppeld, en wel aan `Z ∩ L`. Met `S = Z ∩ L` krijgen
we `N(S) = Z ∩ R`, en `|Z ∩ L| = |Z ∩ R| + 1` vanwege `u`. Dus `|N(S)| = |S| − 1 < |S|`, in
tegenspraak met de voorwaarde. ∎

De voorwaarde van Hall controleren vergt naar elke deelverzameling kijken, en de verificatie doet
precies dat — `2^|L|` deelverzamelingen. Iets goedkopers zou de stelling aannemen die getest wordt:

```
  held      ch14  Hall: every left vertex can be matched iff |N(S)| >= |S| for all S  (120 graphs)
```

De stelling van Hall is een vermomde min-max-stelling, en de vermomming is dun: ze zegt dat de
belemmering voor een perfecte koppeling altijd één enkele "te drukke" verzameling is.

## De stelling van König

> **Stelling (König, 1931).** In een bipartiete graaf is de grootte van een maximale koppeling gelijk
> aan de grootte van een minimale knopenoverdekking.

Zwakke dualiteit is gratis — elke kant van een koppeling heeft zijn eigen overdekkingsknoop nodig —
en opnieuw is de inhoud de andere richting. Het bewijs is een *constructie*:

```python
def konig_cover(g, left, right):
    match = bipartite_matching(g, left)
    unmatched_left = [v for v in left if v not in match]
    # Z: everything reachable from an exposed left vertex by alternating paths
    ...
    return (set(left) - reachable) | (set(right) & reachable)
```

*Bewijs dat dit een overdekking van de juiste grootte is.* Neem een kant `uv` met `u ∈ L`, `v ∈ R`.
Is `u ∉ Z`, dan zit `u` in de overdekking. Is `u ∈ Z`, dan zit `v` er ook in — ofwel is `uv` een
niet-koppelingskant, zodat het alternerende pad zich erdoorheen uitbreidt, ofwel is het een
koppelingskant en werd `u` erlangs bereikt. Hoe dan ook is `v` overdekt. Het is dus een overdekking.

Voor de grootte: elke knoop van `L ∖ Z` is gekoppeld (een vrije linkerknoop zit per definitie in
`Z`), en elke knoop van `R ∩ Z` is gekoppeld (aangetoond in het bewijs van Hall hierboven). Geen
koppelingskant heeft beide eindpunten in de overdekking — dat zou `u ∈ L∖Z` en `v ∈ R∩Z` vergen, maar
`v ∈ Z` bereikt langs zijn koppelingskant dwingt `u ∈ Z`. Dus de overdekking heeft precies één knoop
per koppelingskant. ∎

De verificatie controleert het getal en de constructie apart, want een juist antwoord uit een
verkeerde constructie is een echte faalwijze:

```
  held      ch14  Konig: in a bipartite graph, max matching = min vertex cover  (120 graphs)
  held      ch14  Konig's construction returns a cover of exactly the matching's size  (120 graphs)
```

**König faalt op niet-bipartiete grafen**, en het kleinste getuigenis is de driehoek: maximale
koppeling 1, minimale knopenoverdekking 2. Hoofdstuk 19 identificeert precies voor welke grafen de
gelijkheid geldt, en dat is een veel grotere klasse dan de bipartiete.

## De min-max-familie

Drie hoofdstukken, één vorm:

| Stelling | max | min |
|---|---|---|
| Menger (h. 12) | disjuncte `s`–`t`-paden | `s`–`t`-snede |
| Max-stroom min-snede (h. 13) | stroomwaarde | snedecapaciteit |
| König (h. 14) | koppeling | knopenoverdekking |
| Hall (h. 14) | koppeling die `L` verzadigt | schendende verzameling (belemmering) |

Alle vier zijn dezelfde stelling vanuit verschillende hoeken bekeken, en alle vier zijn gevallen van
dualiteit in de lineaire programmering waarbij het polytoop toevallig gehele hoekpunten heeft. Die
laatste zin is de hele reden dat bipartiete koppeling eenvoudig is en algemene koppeling Edmonds
vergde: de bipartiete beperkingsmatrix is **totaal unimodulair**, en de algemene niet.

## Probeer het

Kijk hoe de constructie van König een overdekking oplevert van dezelfde grootte als de koppeling, op
een graaf waar geen van beide voor de hand ligt:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import Graph
from graphs.matching import bipartite_matching, bipartition, matching_size, konig_cover, min_vertex_cover_bruteforce

# left {0,1,2}, right {3,4,5}
g = Graph(6, [(0,5), (1,3), (1,4), (1,5), (2,5)])
left, right = bipartition(g)
m = bipartite_matching(g, left)
cover = konig_cover(g, left, right)
print('matching size      ', matching_size(m))
print('konig cover        ', sorted(cover), 'size', len(cover))
print('true minimum cover ', min_vertex_cover_bruteforce(g))
print('is a cover         ', all(u in cover or v in cover for u, v in g.edges()))
"
```

```
matching size       2
konig cover         [1, 5] size 2
true minimum cover  2
is a cover          True
```

Vijf kanten overdekt door twee knopen, passend bij een maximale koppeling van grootte 2. De
overdekking neemt **één knoop van elke zijde** — `1` van links en `5` van rechts — en welke zijde
elk vandaan komt, is precies wat de alternerende-bereikbaarheidsverzameling `Z` bepaalt. Het is niet
"één eindpunt van elke koppelingskant, willekeurig gekozen": hier verkeerd kiezen geeft een
verzameling die helemaal geen overdekking is.

Dit voorbeeld kiezen vergde zoeken. De voor de hand liggende kleine bipartiete grafen geven een
overdekking die simpelweg de hele linkerzijde is, wat triviaal een overdekking is en niets aantoont.

## Oefeningen

1. Definieer een vermeerderend pad, en zeg wat omkeren met de koppelingsgrootte doet.
2. Formuleer de stelling van Berge en noem de techniek die haar bewijs gebruikt.
3. De eenvoudige vermeerderingszoektocht is fout op niet-bipartiete grafen. Welke structuur verslaat
   haar?
4. De stelling van König zegt dat maximale koppeling gelijk is aan minimale knopenoverdekking.
   Bereken beide voor een driehoek en verklaar het resultaat.

Oplossingen in Bijlage E.

## Kernpunten

- Berge: een koppeling is maximaal dan en slechts dan als er geen vermeerderend pad bestaat. Bewezen
  met symmetrisch verschil, de techniek om mee te nemen.
- De eenvoudige vermeerderingszoektocht is alleen correct op bipartiete grafen. Oneven cykels
  verslaan haar, en Edmonds' bloesemalgoritme is de oplossing. Het getuigenis hier is `C₇`; `C₃` en
  `C₅` leggen de fout helemaal niet bloot.
- Hall: `L` kan verzadigd worden dan en slechts dan als geen deelverzameling van `L` te weinig buren
  heeft. Haar eerlijk controleren betekent alle `2^|L|` deelverzamelingen bekijken.
- König: bipartiete maximale koppeling is gelijk aan minimale knopenoverdekking, en het bewijs bouwt
  de overdekking uit alternerende bereikbaarheid. Het faalt op de driehoek.
- Menger, max-stroom min-snede, König en Hall zijn één stelling in vier vermommingen —
  LP-dualiteit met een geheeltallig polytoop.
