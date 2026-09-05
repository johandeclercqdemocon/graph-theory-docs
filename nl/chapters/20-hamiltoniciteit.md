# Hoofdstuk 20 — Hamiltoniciteit

Een **Hamiltoniaanse cykel** bezoekt elke knoop precies één keer en keert terug naar zijn start.
Vergelijk met een Euler-circuit, dat elke *kant* precies één keer gebruikt — en dat een perfecte
karakterisering in één regel heeft: een samenhangende graaf heeft er een precies wanneer elke graad
even is.

Voor Hamiltoniciteit is niets van dien aard bekend, en dit hoofdstuk gaat over wat je in plaats
daarvan krijgt.

## Waarom de analogie faalt

De voorwaarde van Euler is **lokaal**: controleer de graad van elke knoop afzonderlijk.
Hamiltoniciteit is onherleidbaar **globaal** — of er een cykel bestaat hangt af van hoe de hele
graaf in elkaar past, en geen enkele hoeveelheid lokale inspectie beslist het.

Dat is niet slechts een gebrek aan verbeelding. De Hamiltoniaanse cykel is `NP`-volledig
(hoofdstuk 22), dus een lokaal controleerbare karakterisering zou `P = NP` geven. De afwezigheid van
een Hamiltoniaanse tegenhanger van de stelling van Euler is een stellingvormig gat met een
complexiteitstheoretische verklaring.

Het vak biedt dus **voldoende** voorwaarden: hypothesen sterk genoeg om een cykel af te dwingen.
Ze zeggen allemaal een variant van "genoeg kanten, gelijkmatig verspreid".

## Dirac en Ore

> **Stelling (Dirac, 1952).** Is `n ≥ 3` en heeft elke knoop graad minstens `n/2`, dan is `G`
> Hamiltoniaans.

> **Stelling (Ore, 1960).** Is `n ≥ 3` en geldt `deg(u) + deg(v) ≥ n` voor elk niet-aangrenzend paar
> `u, v`, dan is `G` Hamiltoniaans.

Ore impliceert Dirac — is elke graad minstens `n/2`, dan sommeert elk paar tot minstens `n` — dus Ore
is de sterkere stelling en geldt voor strikt meer grafen.

*Bewijs van Ore.* Stel van niet, en zij `G` een tegenvoorbeeld met de meeste kanten: het voldoet aan
de voorwaarde van Ore, is niet Hamiltoniaans, en elke kant toevoegen maakt het Hamiltoniaans.

Neem niet-aangrenzende `u`, `v`. `uv` toevoegen creëert een Hamiltoniaanse cykel, die `uv` moet
gebruiken, dus `G` heeft een Hamiltoniaans **pad** `u = x₁, x₂, …, xₙ = v`.

Beschouw nu de verzamelingen `S = {i : u grenst aan x_{i+1}}` en `T = {i : v grenst aan xᵢ}`, beide
deelverzamelingen van `{1, …, n−1}`. Er geldt `|S| + |T| = deg(u) + deg(v) ≥ n`, en beide liggen in
een verzameling van grootte `n − 1`, dus per duivenhokprincipe delen ze een index `i`.

Maar dan zijn `u x_{i+1}` en `xᵢ v` allebei kanten, en de cykel
`u, x₂, …, xᵢ, v, x_{n−1}, …, x_{i+1}, u` — het pad vooruit tot `xᵢ`, spring naar `v`, dan achteruit
tot `x_{i+1}`, dan terug naar `u` — is Hamiltoniaans. Tegenspraak. ∎

De opzet met een **extremaal tegenvoorbeeld** (neem degene met de meeste kanten) is dezelfde zet als
in het opspannendeboombewijs van hoofdstuk 7, en de duivenhokstap is dezelfde als in hoofdstuk 3.

## Voldoende is heel ver van noodzakelijk

De voorwaarden zijn veeleisend, en de meeste Hamiltoniaanse grafen falen er ruimschoots aan:

```
  C5        ham=True   dirac=False  ore=False  mindeg=2  n/2=2.5
  K4        ham=True   dirac=True   ore=True   mindeg=3  n/2=2.0
  petersen  ham=False  dirac=False  ore=False  mindeg=3  n/2=5.0
  K33       ham=True   dirac=True   ore=True   mindeg=3  n/2=3.0
  K23       ham=False  dirac=False  ore=False  mindeg=2  n/2=2.5
```

`C₅` is per constructie Hamiltoniaans en faalt aan Dirac — minimale graad 2 tegen een drempel van
2,5. De verificatie registreert het omgekeerde als een stelling waarvan verwacht wordt dat ze
weerlegd wordt:

```
  refuted   ch20  Every Hamiltonian graph satisfies Dirac's condition  (5 graphs)
```

Vergelijk de laatste twee rijen. `K₃,₃` en `K₂,₃` zien er allebei niet bijzonder uit, en de ene is
Hamiltoniaans en de andere niet — om een reden die Dirac niet kan zien. `K_{a,b}` is Hamiltoniaans
precies wanneer `a = b`, want een cykel in een bipartiete graaf moet tussen de zijden afwisselen.

## Bondy–Chvátal, en waarom Ore werkt

Achter de stelling van Ore zit een nettere uitspraak.

> **Stelling (Bondy–Chvátal, 1976).** Zij de **afsluiting** van `G` het resultaat van herhaaldelijk
> niet-aangrenzende `u, v` met `deg(u) + deg(v) ≥ n` te verbinden. Dan is `G` Hamiltoniaans dan en
> slechts dan als zijn afsluiting dat is.

Dit is werkelijk verrassend: kanten toevoegen kan Hamiltoniciteit uiteraard niet vernietigen, maar
dat deze bepaalde toevoegingen haar niet kunnen *creëren* is de inhoud.

De stelling van Ore is nu een gevolg. Een graaf die aan de voorwaarde van Ore voldoet heeft
afsluiting `K_n`, en die is Hamiltoniaans, dus de graaf is het.

```
  held      ch20  Bondy-Chvatal: G is Hamiltonian iff its closure is  (49 graphs)
```

## Noodzakelijke voorwaarden

De andere kant op zijn de bruikbare feiten negatief — manieren om te bewijzen dat een graaf *niet*
Hamiltoniaans is:

- Een Hamiltoniaanse graaf is **2-samenhangend**: de cykel geeft twee disjuncte paden tussen elk
  paar, dus Menger (hoofdstuk 12) is van toepassing.
- `k` knopen uit een Hamiltoniaanse graaf verwijderen laat hoogstens `k` componenten achter, want de
  cykel valt in hoogstens `k` bogen uiteen. Dit is vaak het snelste weerleggingsmiddel.
- Een Hamiltoniaanse bipartiete graaf heeft even grote delen.

De Petersen-graaf is niet Hamiltoniaans, en het standaardbewijs is een gevalsonderscheid naar hoeveel
spaken de cykel gebruikt. Hij *heeft* wel een Hamiltoniaans pad, en daarom heet hij
**hypohamiltoniaans**: niet Hamiltoniaans, maar `G − v` is Hamiltoniaans voor elke `v`. Hij is,
voorspelbaar, ook hier het tegenvoorbeeld van dit boek.

## Probeer het

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import cycle, complete_bipartite, petersen
from graphs.hamilton import hamiltonian_cycle, hamiltonian_path, dirac_condition, is_hamiltonian
print('C5  hamiltonian cycle:', hamiltonian_cycle(cycle(5)), ' dirac says:', dirac_condition(cycle(5)))
print('K2,3 hamiltonian:     ', is_hamiltonian(complete_bipartite(2,3)), '(unequal parts)')
print('K3,3 hamiltonian:     ', is_hamiltonian(complete_bipartite(3,3)), '(equal parts)')
print('petersen cycle:       ', hamiltonian_cycle(petersen()))
print('petersen path:        ', hamiltonian_path(petersen()) is not None)
"
```

```
C5  hamiltonian cycle: [0, 1, 2, 3, 4]  dirac says: False
K2,3 hamiltonian:      False (unequal parts)
K3,3 hamiltonian:      True (equal parts)
petersen cycle:        None
petersen path:         True
```

`C₅` is de netste illustratie van de kloof: een vijfcykel *is* een Hamiltoniaanse cykel, en de best
bekende voldoende voorwaarde kan dat niet zien.

## Oefeningen

1. Toon aan dat `K_{a,b}` Hamiltoniaans is dan en slechts dan als `a = b ≥ 2`.
2. Bewijs dat een Hamiltoniaanse graaf geen snijknoop heeft.
3. Ga na dat de voorwaarde van Ore die van Dirac impliceert, en geef een graaf die aan Ore voldoet
   maar niet aan Dirac.
4. `k` knopen uit een Hamiltoniaanse graaf verwijderen laat hoogstens `k` componenten achter. Gebruik
   dat om van een graaf naar keuze te tonen dat hij niet Hamiltoniaans is.

Oplossingen in Bijlage E.

## Kernpunten

- Euler-circuits hebben een lokale karakterisering; Hamiltoniaanse cykels geen, en `NP`-volledigheid
  verklaart waarom je er geen moet verwachten.
- Dirac (`δ ≥ n/2`) en Ore (`deg u + deg v ≥ n` voor niet-aangrenzende paren) zijn voldoende, niet
  noodzakelijk. `C₅` is Hamiltoniaans en faalt aan beide.
- Ore's bewijs gebruikt een extremaal tegenvoorbeeld plus duivenhok — dezelfde twee zetten als in de
  hoofdstukken 7 en 3.
- De afsluitingsstelling van Bondy–Chvátal is de eigenlijke uitspraak; Ore is haar gevolg.
- Om Hamiltoniciteit te weerleggen, gebruik de negatieve feiten: 2-samenhang, de grens van
  `k` knopen tegen `k` componenten, en gelijke delen in het bipartiete geval.
