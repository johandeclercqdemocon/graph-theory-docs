# Hoofdstuk 21 — Klieken, onafhankelijke verzamelingen, overdekkingen

Drie beroemde `NP`-moeilijke problemen. Het zijn hetzelfde probleem, en dat helder inzien is meer
waard dan welk afzonderlijk algoritme ervoor ook.

## Drie definities

- Een **kliek** is een verzameling paarsgewijs aangrenzende knopen. `ω(G)` is de grootste.
- Een **onafhankelijke verzameling** is een verzameling paarsgewijs niet-aangrenzende knopen. `α(G)`
  is de grootste.
- Een **knopenoverdekking** is een verzameling die elke kant raakt. `τ(G)` is de kleinste.

## Ze zijn één probleem

> **Propositie.** `S` is een kliek in `G` dan en slechts dan als `S` een onafhankelijke verzameling
> is in `Ḡ`. Dus `ω(G) = α(Ḡ)`.

*Bewijs.* "Elk paar aangrenzend in `G`" en "geen paar aangrenzend in `Ḡ`" zijn dezelfde uitspraak,
want `Ḡ` heeft precies de niet-kanten van `G`. ∎

> **Stelling (Gallai, 1959).** `α(G) + τ(G) = n`.

*Bewijs.* `S` is onafhankelijk dan en slechts dan als `V ∖ S` een knopenoverdekking is: geen kant
heeft beide eindpunten in `S` precies wanneer elke kant een eindpunt erbuiten heeft. Dat is een
bijectie tussen onafhankelijke verzamelingen en knopenoverdekkingen die de grootte omkeert. De
grootste van de ene komt dus overeen met de kleinste van de andere. ∎

Beide worden gecontroleerd tegen onafhankelijke uitputtende zoektochten en niet tegen elkaar:

```
  held      ch21  Gallai: alpha(G) + tau(G) = n  (52 graphs)
  held      ch21  A clique in G is an independent set in the complement  (52 graphs)
```

```
  C5        n=5   alpha=2 tau=3 alpha+tau=5   omega=2 omega(comp)=2
  petersen  n=10  alpha=4 tau=6 alpha+tau=10  omega=2 omega(comp)=4
  K4        n=4   alpha=1 tau=3 alpha+tau=4   omega=4 omega(comp)=1
```

Lees de Petersen-rij: `α = 4`, en de grootste kliek van het complement is ook 4. De identiteit is
geen toeval van kleine gevallen; het is dezelfde verzameling knopen, twee keer bekeken.

Het gevolg is praktisch. **Los er één op, en je hebt alle drie opgelost** — een exact algoritme, een
benadering, of een hardheidsbewijs voor één ervan draagt onmiddellijk over. Het betekent ook dat je
niet kunt hopen er één eenvoudig te vinden: had de onafhankelijke verzameling een polynomiaal
algoritme, dan hadden kliek en knopenoverdekking dat ook.

## Waarom complementeren niet gratis is

Er zit een addertje onder het gras, en het is het soort dat asymptotiek verbergt.

De reductie van kliek naar onafhankelijke verzameling complementeert de graaf. Een ijle graaf met
`m = O(n)` heeft een complement met `Θ(n²)` kanten. Een algoritme waarvan de looptijd van `m`
afhangt, wordt na de reductie dus veel trager, ook al is de reductie "lineaire tijd" in de zin die
voor de complexiteitstheorie telt.

Hier verdient de bitsetrepresentatie van hoofdstuk 2 haar plaats. Een bitmaskerrij complementeren is
één `~` en een masker; buurverzamelingen snijden is één `&`. Kliekzoektocht op een dichte graaf in een
adjacentielijstrepresentatie is precies het slechtste geval dat de metingen van hoofdstuk 2
aanwezen.

```python
def common_neighbours(self, u, v):
    return (self.rows[u] & self.rows[v]).bit_count()
```

Elke serieuze implementatie van maximale kliek is op die operatie gebouwd.

## De natuurlijke gulzige grens

De drie problemen laten alle drie een voor de hand liggende gulzige heuristiek toe, en het is nuttig
te weten hoe slecht elk zich gedraagt voordat hoofdstuk 23 het echt behandelt:

- **Knopenoverdekking** heeft een 2-benadering (hoofdstuk 23), en onder het unieke-spellenvermoeden is
  niets beters mogelijk.
- **Onafhankelijke verzameling** en **kliek** hebben *geen* benadering met constante factor, en zijn
  zelfs niet binnen `n^{1−ε}` te benaderen tenzij `P = NP`. Dat is een van de sterkste bekende
  onbenaderbaarheidsresultaten.

Die asymmetrie is verbluffend, gegeven dat de problemen equivalent zijn. De oplossing is dat de
equivalentie *exacte* antwoorden behoudt maar geen *verhoudingen*: een overdekking van grootte
`τ + 1` is een 1,01-benadering wanneer `τ = 100`, terwijl de bijbehorende onafhankelijke verzameling
van grootte `α − 1` een 2-benadering kan zijn wanneer `α = 2`. Complementeren beeldt "iets te groot"
af op "verhoudingsgewijs veel te klein".

**Equivalente problemen hoeven geen equivalent benaderingsgedrag te hebben**, en dit is daarvan het
netste voorbeeld in het boek.

## Probeer het

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import petersen, cycle, complete
from graphs.approx import max_independent_set, min_vertex_cover, max_clique
for name, g in [('C5', cycle(5)), ('K4', complete(4)), ('petersen', petersen())]:
    a = max_independent_set(g); t = min_vertex_cover(g); w = max_clique(g)
    print(f'{name:<9} alpha={len(a)} tau={len(t)} sum={len(a)+len(t)} n={g.n} '
          f'omega={len(w)} omega(complement)={len(max_clique(g.complement()))}')
"
```

```
C5        alpha=2 tau=3 sum=5 n=5 omega=2 omega(complement)=2
K4        alpha=1 tau=3 sum=4 n=4 omega=4 omega(complement)=1
petersen  alpha=4 tau=6 sum=10 n=10 omega=2 omega(complement)=4
```

Elke rij heeft `α + τ = n`, en elke `ω(Ḡ)` komt overeen met de `α` van dezelfde graaf.

## Oefeningen

1. Bereken `α`, `τ` en `ω` voor `C₆` en controleer de identiteit van Gallai.
2. Toon aan dat `ω(G) · α(G) ≥ n` in het algemeen onwaar is, en vind het kleinste tegenvoorbeeld.
3. Is `G` bipartiet, wat is `τ(G)` dan uitgedrukt in zijn maximale koppeling? (Hoofdstuk 14.)
4. Leg uit waarom een ijle graaf complementeren een kliekalgoritme trager maakt, ook al is de reductie
   van lineaire tijd.

Oplossingen in Bijlage E.

## Kernpunten

- Kliek, onafhankelijke verzameling en knopenoverdekking zijn één probleem in drie notaties:
  `ω(G) = α(Ḡ)` en `α(G) + τ(G) = n`.
- Los er één op en je hebt alle drie exact opgelost. Dat snijdt aan twee kanten — geen van drieën kan
  eenvoudig zijn.
- De reductie is van lineaire tijd maar niet gratis: een ijle graaf complementeren geeft een dichte,
  en algoritmen waarvan de kosten van `m` afhangen lijden eronder. Bitsetrepresentaties (hoofdstuk 2)
  zijn het standaardantwoord.
- Equivalentie van exacte problemen draagt **niet** over op benadering. Knopenoverdekking heeft een
  2-benadering; onafhankelijke verzameling in wezen geen.
