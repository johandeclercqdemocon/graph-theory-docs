# Hoofdstuk 12 — Samenhang en de stelling van Menger

Hoe moeilijk is het om een graaf uiteen te laten vallen? Er zijn twee antwoorden — tel de knopen
die je moet verwijderen, of tel de disjuncte paden die je moet vernietigen — en de stelling van
Menger zegt dat het hetzelfde getal is. Het is de eerste **min-max-stelling** in dit boek, en het
patroon dat ze vestigt loopt door de volgende twee hoofdstukken en door het grootste deel van de
combinatorische optimalisatie.

## Twee maten

Een verzameling `S ⊆ V ∖ {s,t}` is een **`s`–`t`-knopensnede** wanneer haar verwijdering geen
`s`–`t`-pad overlaat. Een verzameling kanten is een **`s`–`t`-kantensnede** wanneer haar
verwijdering hetzelfde doet.

Twee paden zijn **inwendig disjunct** wanneer ze geen knoop delen behalve `s` en `t`, en
**kantdisjunct** wanneer ze geen kant delen.

Eén richting is gratis, en het loont te zien waarom ze gratis is:

> **Lemma (zwakke dualiteit).** Het aantal paarsgewijs inwendig disjuncte `s`–`t`-paden is
> hoogstens de grootte van elke `s`–`t`-knopensnede.

*Bewijs.* Elk `s`–`t`-pad moet een knoop van de snede bevatten, anders zou het de verwijdering
overleven. Inwendig disjuncte paden kunnen zo'n knoop niet delen. Dus de snede heeft minstens één
knoop per pad. ∎

Dat argument geeft `max ≤ min` gratis en vertelt je niets over de vraag of de grens scherp is.
**De inhoud van elke min-max-stelling is de andere richting** — en er is geen algemene reden ze
te verwachten. Er zijn genoeg natuurlijke paren grootheden die aan zwakke dualiteit voldoen met
een echte kloof; `ω(G) ≤ χ(G)` uit hoofdstuk 15 is er een, en hoofdstuk 19 gaat over de grafen
waar ze sluit.

## De stelling

> **Stelling (Menger, 1927).** Voor niet-aangrenzende `s` en `t` is het maximale aantal
> paarsgewijs inwendig disjuncte `s`–`t`-paden gelijk aan de minimale grootte van een
> `s`–`t`-knopensnede.
>
> De kantversie geldt voor alle `s ≠ t`: het maximale aantal kantdisjuncte `s`–`t`-paden is gelijk
> aan de minimale grootte van een `s`–`t`-kantensnede.

De voorwaarde **niet-aangrenzend** in de knopenversie is geen muggenzifterij. Zijn `s` en `t`
aangrenzend, dan scheidt geen verzameling *andere* knopen ze, dus de minimale snede bestaat niet —
de grootheid rechts is ongedefinieerd in plaats van groot. De `vertex_connectivity` van dit boek
geeft in dat geval oneindig terug, wat een uitspraak over de definitie is en niet een rekenkundig
gemak.

*Bewijs (kantversie), per inductie naar het aantal kanten.* Zij `k` de minimale kantensnedegrootte.
Zwakke dualiteit geeft hoogstens `k` disjuncte paden, dus we hebben er `k` nodig.

Kies een minimale snede `F` met `|F| = k` en neem een kant `e ∈ F`. In `G − e` heeft de minimale
`s`–`t`-snede grootte `k − 1`: hoogstens dat, want `F − e` werkt, en minstens dat, want `e` aan een
kleinere snede toevoegen zou `F` verslaan. Per inductie heeft `G − e` `k − 1` kantdisjuncte paden,
en die vermijden `e`. `e` weer toevoegen vraagt om nog één pad dat ze alle vermijdt — dat bestaat
precies omdat `e` in elke minimale snede zat. Het volledige argument vergt zorg voor het geval
waarin samentrekken in plaats van verwijderen nodig is, en de nette moderne route is die hieronder. ∎

## De nette route: het is een stroomprobleem

In plaats van die inductie af te maken, merk op dat Menger **max-stroom min-snede is met elke
capaciteit op 1**, en hoofdstuk 13 bewijst dat. Dit is geen ontwijking; het is de juiste indeling,
want één algoritme levert dan drie stellingen.

Voor de **kantversie** vervang je elke kant door twee bogen met eenheidscapaciteit:

```python
def edge_connectivity(g, s, t):
    net = FlowNetwork(g.n)
    for u, v in g.edges():
        net.add_arc(u, v, 1.0)
        net.add_arc(v, u, 1.0)
    return net.max_flow(s, t)[0]
```

Een stroom van waarde `k` valt uiteen in `k` eenheidspaden, en eenheidscapaciteit dwingt ze
kantdisjunct te zijn. Een snede van capaciteit `k` is een verzameling van `k` kanten.

Voor de **knopenversie** is de truc **knoopsplitsing**: vervang elke knoop `v` door
`v_in → v_out` met capaciteit 1, en leid elke kant naar `v_in` en uit `v_out`.

```python
def vertex_connectivity(g, s, t):
    net = FlowNetwork(2 * g.n)
    for v in g.vertices():
        net.add_arc(2*v, 2*v + 1, INF if v in (s, t) else 1.0)
    for u, v in g.edges():
        net.add_arc(2*u + 1, 2*v, INF)
        net.add_arc(2*v + 1, 2*u, INF)
    return net.max_flow(2*s + 1, 2*t)[0]
```

De inwendige boog begrenst hoeveel stroom *door* `v` gaat op 1, dus paden kunnen geen knoop delen.
De kanten krijgen oneindige capaciteit omdat de stelling knopen telt en geen kanten, en `s` en `t`
krijgen oneindige capaciteit omdat ze niet verwijderd mogen worden.

Knoopsplitsing is een algemene techniek en geen eenmalige truc: telkens wanneer een beperking op
knopen ligt in plaats van op kanten, splits je de knoop en zet je de beperking op de inwendige
boog.

Beide worden gecontroleerd tegen uitputtend verwijderen — een volstrekt andere berekening:

```
  held      ch12  Menger (edge form): max edge-disjoint s-t paths = min s-t edge cut  (49 graphs)
  held      ch12  Menger (vertex form): max internally-disjoint paths = min s-t vertex cut  (51 graphs)
```

## Globale samenhang

De **knopensamenhang** `κ(G)` is het kleinste aantal knopen waarvan verwijdering `G` onsamenhangend
maakt of tot één knoop reduceert; de **kantensamenhang** `λ(G)` is de kantentegenhanger. Een graaf
is **`k`-samenhangend** wanneer `κ(G) ≥ k`.

> **Stelling (Whitney).** `κ(G) ≤ λ(G) ≤ δ(G)`.

*Bewijs.* De rechterongelijkheid: alle kanten bij een knoop van minimale graad verwijderen isoleert
hem. De linker: neem een minimale kantensnede en kies van elke snedekant één eindpunt aan de
bronzijde. Die knopen verwijderen vernietigt elk `s`–`t`-pad, dus `κ ≤ λ`. ∎

Beide ongelijkheden kunnen strikt zijn, en de Petersen-graaf is deze keer niet het getuigenis — hij
heeft `κ = λ = δ = 3`. Neem in plaats daarvan twee driehoeken verbonden door één lang pad: `δ = 2`,
`λ = 1`, `κ = 1`.

Een bruikbare herformulering, die Menger op elk paar tegelijk toepast:

> **Gevolg.** `G` is `k`-samenhangend dan en slechts dan als elk paar knopen verbonden is door `k`
> inwendig disjuncte paden.

Dat is de vorm om te onthouden, want ze zet een uitspraak over het *vernietigen* van de graaf om in
een uitspraak over *routes erdoorheen* — en daarom is `k`-samenhang het juiste robuustheidsbegrip
voor een netwerk.

## Probeer het

Bevestig beide vormen op de Petersen-graaf, waarvan de samenhang in elke zin 3 is:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import petersen, cycle
from graphs.flow import edge_connectivity, vertex_connectivity, brute_force_edge_cut, brute_force_vertex_cut

p = petersen()
print('petersen, vertices 0 and 2 (non-adjacent):')
print('   edge-disjoint paths  ', edge_connectivity(p, 0, 2), ' exhaustive edge cut  ', brute_force_edge_cut(p, 0, 2))
print('   internally-disjoint  ', vertex_connectivity(p, 0, 2), ' exhaustive vertex cut', brute_force_vertex_cut(p, 0, 2))
c = cycle(6)
print('C_6, opposite vertices:')
print('   edge-disjoint paths  ', edge_connectivity(c, 0, 3), ' exhaustive edge cut  ', brute_force_edge_cut(c, 0, 3))
"
```

```
petersen, vertices 0 and 2 (non-adjacent):
   edge-disjoint paths   3.0  exhaustive edge cut   3.0
   internally-disjoint   3.0  exhaustive vertex cut 3.0
C_6, opposite vertices:
   edge-disjoint paths   2.0  exhaustive edge cut   2.0
```

Een cykel geeft 2 in beide richtingen, wat het kleinste interessante geval is: twee routes rond, en
je moet twee kanten doorknippen om ze te stoppen.

## Oefeningen

1. Formuleer zwakke dualiteit voor knopensneden, en leg uit waarom ze op zichzelf niets bewijst.
2. Waarom vereist de knopenversie van de stelling van Menger dat `s` en `t` niet aangrenzend zijn?
3. Geef een graaf waarin `κ(G) < λ(G) < δ(G)` — of leg uit waarom een van die ongelijkheden niet
   strikt kan zijn.
4. Waarom krijgt in de knoopsplitsingsconstructie de inwendige boog capaciteit 1 en de kantbogen
   oneindig?

Oplossingen in Bijlage E.

## Kernpunten

- Menger is een min-max-stelling: disjuncte paden tegenover snedegrootte, in zowel een knopen- als
  een kantversie.
- Zwakke dualiteit (`max ≤ min`) is gratis en bewijst niets. De stelling is de andere ongelijkheid,
  en er is geen algemene reden waarom zo'n grens scherp zou zijn.
- De knopenversie vereist dat `s` en `t` niet aangrenzend zijn, want anders bestaat er helemaal
  geen snede.
- Beide vormen zijn max-stroom min-snede met eenheidscapaciteiten. Knoopsplitsing —
  `v_in → v_out` met capaciteit 1 — is de algemene manier om een beperking van kanten naar knopen
  te verplaatsen.
- `κ(G) ≤ λ(G) ≤ δ(G)`, en `G` is `k`-samenhangend precies wanneer elk paar `k` inwendig disjuncte
  paden heeft.
