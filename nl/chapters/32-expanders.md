# Hoofdstuk 32 — Expanders, en waar je hierna heen gaat

Het laatste idee in dit boek is een graaf die ijl is en toch buitengewoon goed samenhangt. Die twee
eisen klinken tegenstrijdig, en dat ze het niet zijn, is een van de nuttigste ontdekkingen in de moderne
wiskunde.

## De definitie

Een **expander** is een familie `d`-reguliere grafen op groeiende `n` waarvan de Cheeger-constante
`h(G)` van onderen begrensd blijft door een constante. Elke verzameling van hoogstens de helft van de
knopen heeft een rand evenredig met haar grootte, uniform, voor willekeurig grote grafen — met slechts
`dn/2` kanten om mee te werken.

De ongelijkheid van Cheeger uit hoofdstuk 30 maakt hiervan een spectrale voorwaarde. Goede expansie is
equivalent met een **grote spectrale kloof** `d − λ`, waarbij `λ` de grootste niet-triviale eigenwaarde
in absolute waarde is. Expanders construeren wordt dus een eigenwaardeprobleem.

## Twee lambda's, en ze verwarren

Er zit hier een subtiliteit die dit boek bij de eerste poging fout had, en die de alinea waard is.

Voor een `d`-reguliere graaf is `d` altijd een eigenwaarde (de al-enen-eigenvector). Is de graaf
**bipartiet**, dan is `−d` het ook. Er zijn twee grootheden in omloop:

- **`spectral_expansion`** — sluit zowel `d` als `−d` uit. Dit is de `λ` van de Ramanujan-voorwaarde.
  Een bipartiete graaf heeft `−d` juist *omdát* hij bipartiet is, en die behouden zou elke bipartiete
  graaf brandmerken als slechte expander om een reden die niets met samenhang te maken heeft.
- **`mixing_lambda`** — sluit alleen `d` uit. Dit is de `λ` van het mengingslemma hieronder, en `−d`
  moet behouden blijven.

Eén functie voor beide gebruiken liet het mengingslemma onmiddellijk falen op `K₃,₃`. Neem `S = {0}` en
`T = {1}`, beide aan dezelfde zijde: `e(S,T) = 0` terwijl `d|S||T|/n = 0,5`, dus het verschil is `0,5`.
Met `−3` uitgesloten is de grens `0`, en het lemma is geschonden. De eigenwaarde `−3` is precies wat dat
verschil verantwoordt — het is geen ruis.

Hetzelfde symbool, twee definities, en telkens is er maar één juist.

## Het mengingslemma

> **Stelling (mengingslemma voor expanders).** Voor een `d`-reguliere graaf met
> `λ = mixing_lambda(G)` en willekeurige knopenverzamelingen `S`, `T`:
>
> `| e(S,T) − d|S||T|/n | ≤ λ √(|S||T|)`.

De middelste term is wat je zou verwachten als de kanten willekeurig geplaatst waren. Het lemma zegt dus
dat een graaf met kleine `λ` een kantverdeling heeft die **niet te onderscheiden is van toeval** op de
resolutie van verzamelingsgroottes. Dat is wat "pseudotoevallig" precies betekent, en het is waarom
expanders op zoveel plaatsen toeval vervangen.

```
  held      ch32  Expander mixing lemma: |e(S,T) - d|S||T|/n| <= lambda sqrt(|S||T|)  (11 graphs)
```

Gecontroleerd over **elk** paar deelverzamelingen, tegen een spectrum uit de Jacobi-oplosser van
hoofdstuk 29 — combinatoriek aan de ene kant, lineaire algebra aan de andere.

## Hoe goed kan expansie worden?

> **Stelling (Alon–Boppana).** Voor `d`-reguliere grafen geldt `λ ≥ 2√(d−1) − o(1)` als `n → ∞`.

Er is een bodem. Geen oneindige familie `d`-reguliere grafen kan `λ` onder `2√(d−1)` hebben.

Een graaf die haar haalt heet **Ramanujan**: `λ ≤ 2√(d−1)`, optimale expansie. Ze bestaan —
Lubotzky–Phillips–Sarnak en Margulis construeerden in 1988 oneindige families met diepe getaltheorie, en
de naam komt van het Ramanujan-vermoeden waarop hun bewijs steunt. Marcus, Spielman en Srivastava gaven
in 2013 een heel ander bestaansbewijs voor bipartiete Ramanujan-grafen van elke graad, met
verstrengelde veeltermen.

De Petersen-graaf is Ramanujan: `d = 3`, `λ = 2`, en `2√2 ≈ 2,83`.

```
  held      ch32  The Petersen graph is Ramanujan  (1 graphs)
```

## Waarom het iemand kan schelen

Expanders zijn ijle objecten met de samenhang van dichte grafen, dus ze duiken op waar je goedkoop
robuustheid nodig hebt:

- **Ontrandomiseren.** Een toevalswandeling op een expander raakt elke grote verzameling snel, dus
  `O(log n)` toevalsbits kunnen `O(n)` vervangen in veel algoritmen.
- **Foutcorrigerende codes.** Expandercodes decoderen in lineaire tijd en benaderen de Shannon-limiet.
- **Netwerkontwerp.** Constante graad, constante diameter, en bestand tegen knoopuitval.
- **Eigenschapstesten.** Een graaf onderscheiden van een die ver van een eigenschap af ligt.
- **De PCP-stelling.** Expanders worden gebruikt in de kloofversterkingsstap, en dus in de
  onbenaderbaarheidsresultaten uit hoofdstuk 23.

Het terugkerende thema: **expliciete constructies zijn veel moeilijker dan bestaansbewijzen.** Een
willekeurige `d`-reguliere graaf is met kans naar 1 een expander — een argument van één alinea in de
stijl van hoofdstuk 24 — terwijl expliciete families tot 1988 duurden en gereedschap uit een ander
vakgebied vergden. Dat is dezelfde kloof als bij de Ramsey-ondergrenzen in hoofdstuk 28, en het is de
karakteristieke vorm van de nalatenschap van de probabilistische methode.

## Probeer het

```bash
python -c "
import sys, math; sys.path.insert(0, '.')
from graphs.core import complete, cycle, petersen, complete_bipartite
from graphs.spectral import (spectral_expansion, mixing_lambda, is_ramanujan,
                             cheeger_constant, algebraic_connectivity)
print(f\"  {'graph':<10} {'d':>2} {'expansion l':>12} {'mixing l':>9} {'2sqrt(d-1)':>11} {'ram':>5} {'h(G)':>6}\")
for name, g in [('C6', cycle(6)), ('K4', complete(4)), ('K3,3', complete_bipartite(3,3)),
                ('petersen', petersen())]:
    d = g.degree(0)
    print(f'  {name:<10} {d:>2} {spectral_expansion(g):>12.4f} {mixing_lambda(g):>9.4f} '
          f'{2*math.sqrt(d-1):>11.4f} {str(is_ramanujan(g)):>5} {cheeger_constant(g):>6.3f}')
"
```

```
  graph       d  expansion l  mixing l  2sqrt(d-1)   ram   h(G)
  C6          2       1.0000    2.0000      2.0000  True  0.667
  K4          3       1.0000    1.0000      2.8284  True  2.000
  K3,3        3       0.0000    3.0000      2.8284  True  1.667
  petersen    3       2.0000    2.0000      2.8284  True  1.000
```

Kijk naar de rij `K₃,₃`: expansie `λ = 0` en menging `λ = 3`. Dezelfde graaf, hetzelfde spectrum, en de
twee kolommen verschillen de hele graad — omdat de ene `−3` uitsluit en de andere dat niet mag. Die ene
rij is het onderscheid waarmee dit hoofdstuk opende.

Vergelijk `C₆` en de Petersen-graaf. Beide hebben menging `λ = 2` en beide heten formeel "Ramanujan",
maar een cykel is in geen enkele nuttige zin een expander — en de tabel met één graaf per rij kan dat
niet tonen. Expansie is een eigenschap van een *groeiende familie*, dus je moet haar zien groeien:

```
    C_4   h = 1.0000   (4/n = 1.0000)
    C_8   h = 0.5000   (4/n = 0.5000)
    C_12  h = 0.3333   (4/n = 0.3333)
    C_14  h = 0.2857   (4/n = 0.2857)
```

`h(Cₙ) = 4/n → 0`. Je kunt een cykel altijd met twee kanten doorknippen, hoe groot hij ook wordt, dus de
verhouding tussen rand en grootte verdwijnt. Een expanderfamilie houdt `h` van *onderen* begrensd door
een constante, en geen enkele hoeveelheid inspectie van één eindige cykel onthult dat deze dat niet doet.

Dat is de valstrik die de tabel van dit hoofdstuk zet en de reden dat de definitie over een familie
kwantificeert: **geen enkele eindige graaf is of is geen expander.** `C₆` Ramanujan noemen is technisch
juist en zegt niets over de familie waartoe hij behoort.

## Waar je hierna heen gaat

Dit boek stopt hier. De natuurlijke vervolgen:

**Structurele grafentheorie.** Diestel, *Graph Theory*, is de standaard moderne referentie en behandelt
minoren, samenhang en extremale theorie grondig.

**Extremaal en probabilistisch.** Alon en Spencer, *The Probabilistic Method*, is hét boek over het
onderwerp van hoofdstuk 24 en gaat er ver voorbij — het lokale lemma, martingalen, entropie.

**Spectraal.** Spielmans collegenotities over spectrale en algebraïsche grafentheorie, en Chung,
*Spectral Graph Theory*, voor de genormaliseerde Laplaciaan die dit boek oversloeg.

**Algoritmen.** Williamson en Shmoys over benaderen; Cygan e.a. over geparametriseerde algoritmen, de
moderne behandeling van de tweede helft van hoofdstuk 23.

**Open problemen** die je nu kunt lezen: de waarden van `R(5,5)` en `R(6,6)`; het probleem van
Zarankiewicz voor bipartiete `H` (hoofdstuk 27); of `P = NP`; het reconstructievermoeden, dat een graaf
op minstens drie knopen bepaald wordt door de multiverzameling van zijn knoop-verwijderde deelgrafen —
open sinds 1942 en gênant eenvoudig te formuleren.

## Oefeningen

1. Waarom is een cykel geen expander, ondanks dat hij samenhangend en regulier is?
2. Verifieer dat de Petersen-graaf Ramanujan is vanuit zijn spectrum `{3, 1⁵, (−2)⁴}`.
3. Leg uit waarom `−d` behouden moet blijven voor het mengingslemma maar uitgesloten voor de
   Ramanujan-voorwaarde.
4. Geef het argument van één alinea dat een willekeurige `d`-reguliere graaf waarschijnlijk een expander
   is, en zeg waarom dat er geen produceert.

Oplossingen in Bijlage E.

## Kernpunten

- Een expander is een *familie* ijle reguliere grafen met van onderen begrensde expansie. Geen enkele
  eindige graaf is een expander.
- Cheeger (hoofdstuk 30) maakt expansie tot een spectrale voorwaarde: goede expansie is een grote
  spectrale kloof.
- Er zijn twee verschillende `λ`'s in omloop. Het mengingslemma behoudt `−d`; de Ramanujan-voorwaarde
  laat haar vallen. Ze verwarren breekt het mengingslemma onmiddellijk op `K₃,₃`.
- Het mengingslemma zegt dat kleine `λ` betekent dat de kanten verdeeld zijn alsof bij toeval — de
  precieze inhoud van "pseudotoevallig".
- Alon–Boppana legt een bodem bij `2√(d−1)`; Ramanujan-grafen halen haar, en de Petersen-graaf is er een.
- Willekeurige `d`-reguliere grafen zijn vrijwel zeker expanders; expliciete constructies duurden tot
  1988 en vergden getaltheorie. Bestaan is eenvoudig, construeren is moeilijk — de vorm van dit hele
  laatste deel van het boek.
