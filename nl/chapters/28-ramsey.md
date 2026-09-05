# Hoofdstuk 28 — Ramsey-theorie

Hoofdstuk 27 vroeg hoeveel kanten een structuur afdwingen. De Ramsey-theorie vraagt iets sterkers: hoe
groot moet een graaf zijn voordat **elke** 2-kleuring van zijn kanten monochromatische orde bevat. Het
antwoord is altijd "eindig", en vrijwel nooit "bekend".

## R(3,3) = 6

> **Stelling.** Elke 2-kleuring van de kanten van `K₆` bevat een monochromatische driehoek, en een of
> andere 2-kleuring van `K₅` doet dat niet.

*Bewijs.* Neem een willekeurige knoop `v` in `K₆`. Hij heeft 5 kanten, dus per duivenhokprincipe delen
er minstens 3 een kleur — zeg dat `v` rood verbonden is met `a`, `b`, `c`. Is een van `ab`, `bc`, `ac`
rood, dan vormt die kant met `v` een rode driehoek. Is er geen rood, dan is `abc` een blauwe
driehoek. ∎

Dat is het hele bewijs, en het is de vriendelijkste stelling in dit deel van het boek: één
duivenhokstap en één gevalsonderscheid. Het is ook het bekende "feestpuzzeltje" — onder elke zes
mensen zijn er drie die elkaar allemaal kennen of drie die elkaar geen van allen kennen.

Voor de ondergrens: kleur `K₅` rood op een vijfcykel en blauw op de complementaire vijfcykel. Geen van
beide kleurklassen bevat een driehoek, want `C₅` is driehoekvrij en zelfcomplementair.

Beide helften zijn uitputtend controleerbaar, en dit is een van de weinige plaatsen in deel VI waar de
verificatie een echte vraag kan afdoen in plaats van een uitspraak steekproefsgewijs te controleren:

```
  held      ch28  R(3,3) = 6: every 2-colouring of K_6 has a monochromatic triangle  (3 graphs)
```

32.768 kleuringen van `K₆`, allemaal gecontroleerd; 1.024 van `K₅`, en een tegenvoorbeeld gevonden.
Samen stellen die `R(3,3) = 6` volledig vast. **Dit is een bewijs, geen steekproef** — de zoektocht is
uitputtend over de volledige ruimte waarover de stelling kwantificeert, en het is de enige situatie in
dit boek waar een eindige berekening een stelling rechtstreeks afdoet.

## De algemene stelling

> **Stelling (Ramsey, 1930).** Voor alle `s, t` bestaat er een kleinste `R(s,t)` zodat elke 2-kleuring
> van `K_{R(s,t)}` een rode `K_s` of een blauwe `K_t` bevat.

Het bestaansbewijs geeft `R(s,t) ≤ R(s−1,t) + R(s,t−1)`, dus `R(s,s) ≤ 4^s`. De probabilistische
methode van hoofdstuk 24 geeft `R(s,s) > 2^{s/2}`.

Beide grenzen stammen uit de jaren dertig en veertig. **Het grondtal van de exponentiële functie is nog
steeds onbekend.** In tachtig jaar is de kloof tussen `√2` en `4` alleen in de termen van lagere orde
versmald — een resultaat uit 2023 verbeterde de bovengrens tot `3,993^s`, wat groot nieuws was en het
beeld niet veranderde.

## De bekende waarden

| | `t=3` | `t=4` | `t=5` | `t=6` |
|---|---|---|---|---|
| **`s=3`** | 6 | 9 | 14 | 18 |
| **`s=4`** | | 18 | 25 | 36–40 |
| **`s=5`** | | | **43–46** | 58–85 |

`R(5,5)` is onbekend. Het is bekend dat het tussen 43 en 46 ligt, en daar houdt de tabel op een tabel
te zijn.

De reden is de schaal. Beslissen of `R(5,5) = 43` betekent elke 2-kleuring van `K₄₃` controleren, en
daarvan zijn er `2^903`. Dat is geen kwestie van wachten op snellere computers: `2^903` overtreft het
aantal atomen in het waarneembare heelal tot een aanzienlijke macht. Geen denkbare berekening raakt
eraan, en er is geen beter idee gevonden.

De opmerking van Erdős is de standaardsamenvatting, en ze is niet echt een grap: eisten
buitenaardse wezens `R(5,5)` op straffe van vernietiging, dan zouden we al onze computers en wiskundigen
moeten mobiliseren om het te vinden; eisten ze `R(6,6)`, dan zouden we moeten proberen de
buitenaardse wezens te vernietigen.

## Het patroon voorbij grafen

De stelling van Ramsey is één geval van een algemeen verschijnsel: **volledige wanorde is onmogelijk.**
Elke voldoend grote structuur bevat een grote geordende deelstructuur, wat "geordend" in die context ook
betekent.

- **Van der Waerden:** elke 2-kleuring van `{1, …, N}` bevat een monochromatische rekenkundige rij van
  lengte `k`, voor `N` groot genoeg.
- **Szemerédi:** elke deelverzameling van de gehele getallen met positieve bovendichtheid bevat
  willekeurig lange rekenkundige rijen.
- **Green–Tao:** de priemgetallen bevatten willekeurig lange rekenkundige rijen — ondanks dichtheid
  nul, zodat Szemerédi niet rechtstreeks van toepassing is.
- **Hales–Jewett:** hoogdimensionaal boter-kaas-en-eieren kan niet in remise eindigen.

Ze delen alle dezelfde vorm, en ze delen alle hetzelfde gebrek: de grenzen zijn astronomisch slecht. De
oorspronkelijke grens van Van der Waerden was niet primitief recursief. Het regelmatigheidslemma van
Szemerédi — het hoofdinstrument — heeft grenzen die torens van exponenten zijn, en Gowers bewees dat dat
noodzakelijk is en geen artefact.

**Ramsey-achtige stellingen vertellen je dat een structuur bestaat en geven je geen enkele manier om
haar te vinden.** Dat is dezelfde klacht die hoofdstuk 24 over de probabilistische methode uitte, en dat
is geen toeval: de ondergrenzen zijn probabilistisch en de bovengrenzen Ramsey-achtig, en geen van beide
is constructief.

## Probeer het

```bash
python -c "
import sys, time; sys.path.insert(0, '.')
from graphs.extremal import ramsey_holds, ramsey_counterexample
t0 = time.perf_counter()
print('every colouring of K_6 has a mono triangle:', ramsey_holds(6, 3, 3))
witness = ramsey_counterexample(5, 3, 3)
print('K_5 counterexample exists:                 ', witness is not None)
print('   its red edges:', sorted(witness.edges()))
print(f'   ({time.perf_counter() - t0:.1f}s for 32768 + 1024 colourings)')
"
```

```
every colouring of K_6 has a mono triangle: True
K_5 counterexample exists:                  True
   its red edges: [(0, 3), (0, 4), (1, 2), (1, 4), (2, 3)]
   (0.5s for 32768 + 1024 colourings)
```

Een halve seconde doet `R(3,3)` af. Die aanpak opschalen naar `R(5,5)` zou `2^903` kleuringen vergen, en
het verschil tussen die twee getallen is de volledige moeilijkheid van het vak.

## Oefeningen

1. Bewijs `R(3,3) ≤ 6` met het duivenhokargument, in je eigen woorden.
2. Toon aan dat het tegenvoorbeeld op `K₅` werkelijk geen monochromatische driehoek heeft, door beide
   kleurklassen na te gaan.
3. Gebruik `R(s,t) ≤ R(s−1,t) + R(s,t−1)` om `R(3,4) ≤ 10` af te leiden. (De werkelijke waarde is 9.)
4. Waarom kan geen berekening `R(5,5)` door uitputtend zoeken afdoen? Geef het aantal kleuringen.

Oplossingen in Bijlage E.

## Kernpunten

- `R(3,3) = 6`, bewijsbaar met één duivenhokstap, en hier afgedaan door uitputtend zoeken over alle
  32.768 kleuringen — de enige plaats in dit boek waar een eindige berekening *een bewijs is*.
- `2^{s/2} < R(s,s) < 4^s`, beide grenzen uit de jaren dertig en veertig, en het grondtal is na tachtig
  jaar nog steeds onbekend.
- Van `R(5,5)` is alleen bekend dat het in `[43, 46]` ligt. Het door zoeken afdoen vergt `2^903`
  kleuringen, dus het zal niet door zoeken afgedaan worden.
- Het algemene patroon — Van der Waerden, Szemerédi, Green–Tao — is dat volledige wanorde onmogelijk is.
  Ze hebben alle astronomisch slechte grenzen, en aantoonbaar zo.
- Net als de probabilistische methode bewijst de Ramsey-theorie bestaan en biedt ze geen constructie.
