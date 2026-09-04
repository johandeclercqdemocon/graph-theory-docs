# Hoofdstuk 18 — De vijf- en de vierkleurenstelling

Twee stellingen over dezelfde objecten. De ene heeft een bewijs dat je in een bladzijde kunt lezen.
De andere heeft een bewijs dat je helemaal niet kunt lezen, en dit hoofdstuk gaat er deels over wat
dat betekent.

## Zes kleuren, gratis

Hoofdstuk 17 stelde vast dat elke vlakke graaf een knoop van graad hoogstens 5 heeft — anders zou
`2m = Σdeg(v) ≥ 6n` zijn, in tegenspraak met `m ≤ 3n − 6`. Vlakke grafen zijn dus 5-degeneraat, en de
grens uit hoofdstuk 15 geeft `χ ≤ 6` onmiddellijk.

```
  held      ch18  Every planar graph has a vertex of degree at most 5  (51 graphs)
```

Dat kostte twee regels. Tot vijf komen kost een bladzijde, en tot vier kwam een eeuw.

## Vijf kleuren

> **Stelling (Heawood, 1890).** Elke vlakke graaf is 5-kleurbaar.

*Bewijs.* Inductie naar `n`. Neem een knoop `v` met `deg(v) ≤ 5` en kleur `G − v` met 5 kleuren.

Gebruiken de buren van `v` hoogstens 4 kleuren, dan is er een kleur vrij — klaar.

Anders is `deg(v) = 5` en gebruiken zijn buren alle vijf. Leg een vlakke inbedding vast en label de
buren `v₁, …, v₅` in rotatievolgorde, waarbij `vᵢ` kleur `i` heeft.

Beschouw de deelgraaf voortgebracht door de kleuren 1 en 3, en zij `H` de component die `v₁` bevat.
Is `v₃ ∉ H`, verwissel dan de kleuren 1 en 3 in heel `H`. Dat blijft geldig — `H` is een volledige
component van die deelgraaf, dus geen kant verlaat haar met een kleurconflict — en nu heeft `v₁`
kleur 3, wat kleur 1 vrijmaakt voor `v`.

Is `v₃ ∈ H`, dan is er een pad van `v₁` naar `v₃` dat alleen de kleuren 1 en 3 gebruikt. Samen met
`v` omsluit dat een gebied. Beschouw nu de kleuren 2 en 4 en de component die `v₂` bevat. Elk pad van
`v₂` naar `v₄` zou dat eerste pad moeten kruisen — en in een *vlakke* inbedding kan dat niet, want
kruisingen bestaan er niet. Dus `v₄` zit niet in de component van `v₂`, en dezelfde verwisseling
maakt kleur 2 vrij. ∎

Dat is een **Kempe-ketenargument**, en de tweekleurige componentverwisseling is de techniek. Let op
waar vlakheid binnenkomt: bij de laatste stap. Een pad kan een ander pad niet kruisen. Dat is de
enige topologische invoer, en ze doet al het werk.

## Vier kleuren

> **Stelling (Appel–Haken, 1976).** Elke vlakke graaf is 4-kleurbaar.

Kempe publiceerde een bewijs in 1879. Het hield elf jaar stand tot Heawood er een fout in vond — het
ketenverwisselingsargument faalt wanneer twee verwisselingen op elkaar inwerken, en dat geval had
Kempe niet behandeld. Wat het wrak overleefde is de vijfkleurenstelling hierboven.

Het uiteindelijke bewijs heeft twee delen:

- een **onvermijdbare verzameling**: een lijst van 1936 configuraties (later teruggebracht tot 633)
  zodat elke vlakke graaf er minstens één moet bevatten;
- **reduceerbaarheid**: een aantoning dat een minimaal tegenvoorbeeld er geen van kan bevatten.

Het tweede deel is waar de computer binnenkomt. Elke configuratie vergt het controleren van een groot
aantal kleuringen, en dat met de hand doen voor 633 configuraties is niet haalbaar.

Het bewijs is sindsdien geverifieerd — Robertson, Sanders, Seymour en Thomas vereenvoudigden het in
1997, en Gonthier produceerde in 2005 een volledig machinaal gecontroleerde versie in Coq. Bij die
laatste loont het stil te staan: het bewijs is nu strenger geverifieerd dan de meeste bewijzen die
mensen schrijven, en het is nog steeds onleesbaar.

Dit boek kan het niet bewijzen. Wat het wel kan, is het controleren:

```
  held      ch18  Every planar graph is 4-colourable  (51 graphs)
```

**Die regel is geen bewijsmateriaal voor de stelling.** Ze zegt dat elke vlakke graaf op hoogstens 6
knopen 4-kleurbaar is, en daar twijfelde nooit iemand aan — het eerste mogelijke tegenvoorbeeld zou
enorm zijn. Ze staat om een andere reden in de verificatie: om te vangen dat de uitspraak verkeerd
opgeschreven wordt, en om luid te falen wanneer `is_planar` of `chromatic_number` stukgaat. "De
controle slaagt" verwarren met "de stelling wordt ondersteund" is precies de fout die de verificatie
van dit boek niet wil aanmoedigen.

## Wat de moeilijkheid betekent

De kloof tussen vijf en vier kleuren is geen kloof in inspanning. Ze is structureel:

- **Zes** volgt uit een graadgrens, die volgt uit tellen.
- **Vijf** volgt uit een lokaal verwisselingsargument dat vlakheid geldig maakt.
- **Vier** heeft geen bekend argument dat gevalsonderscheid over honderden configuraties vermijdt.

Niemand heeft een kort bewijs gevonden en er is geen reden er een te verwachten. De vierkleurenstelling
is misschien gewoon een ware uitspraak waarvan het kortste bewijs groot is — en als dat zo is, is de
computer geen kruk maar het enige beschikbare instrument.

Het loont te vergelijken met een nabije vraag die *wel* eenvoudig is. Op de torus is het antwoord 7,
bewezen met Heawoods telargument in één bladzijde, zonder gevallen. Hoger geslacht is *eenvoudiger*
dan het vlak, omdat de telgrens daar scherp is en in het vlak niet.

## Probeer het

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.core import complete, cycle, petersen
from graphs.algorithms import chromatic_number
from graphs.planar import is_planar, degeneracy

for name, g in [('K4', complete(4)), ('C5', cycle(5)), ('petersen', petersen())]:
    print(f'{name:<9} planar={is_planar(g)!s:<6} degeneracy={degeneracy(g)} chi={chromatic_number(g)}')
"
```

```
K4        planar=True   degeneracy=3 chi=4
C5        planar=True   degeneracy=2 chi=3
petersen  planar=False  degeneracy=3 chi=3
```

`K₄` toont dat vier kleuren soms nodig zijn, dus de stelling kan niet verbeterd worden. De
Petersen-graaf toont dat het omgekeerde in de andere richting faalt: niet-vlakke grafen kunnen best
3-kleurbaar zijn, dus vlakheid is voldoende voor `χ ≤ 4` en bij lange na niet noodzakelijk.

## Oefeningen

1. Bewijs de zeskleurenstelling rechtstreeks uit `m ≤ 3n − 6`.
2. Waar precies gebruikt het vijfkleurenbewijs vlakheid? Wijs de ene stap aan.
3. Geef een vlakke graaf die precies 4 kleuren nodig heeft, anders dan `K₄`.
4. Kempes argument uit 1879 was fout. Wat gaat er, zonder het op te zoeken, mis wanneer je twee
   Kempe-verwisselingen na elkaar toepast?

Oplossingen in Bijlage E.

## Kernpunten

- Zes kleuren volgen uit 5-degeneratie, die volgt uit `m ≤ 3n − 6`. Twee regels.
- Vijf kleuren volgen uit een Kempe-ketenargument. Vlakheid wordt in precies één stap gebruikt: twee
  paden kunnen elkaar niet kruisen.
- Vier kleuren vergden 633 configuraties en een computer, en er is nog steeds geen leesbaar bewijs.
  Het is sindsdien machinaal gecontroleerd in Coq.
- De vierkleurencontrole van de verificatie bevestigt de *uitspraak* op kleine grafen. Ze is geen
  bewijsmateriaal voor de stelling, en haar als zodanig behandelen zou precies de fout zijn die deze
  verificatieaanpak wil vermijden.
- `K₄` toont dat de grens scherp is; de Petersen-graaf toont dat vlakheid verre van noodzakelijk is.
