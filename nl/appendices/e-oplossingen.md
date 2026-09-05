# Bijlage E — Oplossingen bij de oefeningen

Elk numeriek antwoord hier is tegen de eigen code van het boek gedraaid en niet beweerd. Waar een
oefening je iets laat zoeken, wordt één getuigenis gegeven; er bestaan er meestal meer.

---

## Hoofdstuk 1 — Wat een graaf is

**1.** `K₆` heeft `6 · 5 / 2 = 15` kanten: elk van de 6 knopen ontmoet er 5, en elke kant wordt twee
keer geteld. `complete(6).m` geeft 15.

**2.** Tel de graden op: `3 × 10 = 30`, en het handdruklemma (hoofdstuk 3) zegt dat dit `2m` is, dus
`m = 15`. Tellen is niet nodig.

**3.** `[(0,1),(1,2),(2,0)]` en `[(2,0),(0,1),(1,2)]` zijn dezelfde gelabelde graaf — de volgorde in de
kantenlijst doet er niet toe, want `E` is een verzameling. `[(0,1),(1,2),(2,3)]` op vier knopen is een
andere graaf, en `[(0,2),(2,1),(1,0)]` op drie is *weer dezelfde* graaf, want dezelfde paren zijn
verbonden.

**4.** Drie paarsgewijze kanten zijn niet te onderscheiden van drie afzonderlijke samenwerkingen tussen
twee auteurs die elkaar nooit ontmoetten. De informatie "deze drie werkten *als groep* samen" is niet uit
de driehoek terug te halen. Een **hypergraaf**, waarvan de kanten willekeurige deelverzamelingen zijn,
behoudt haar.

## Hoofdstuk 2 — Representaties

**1.** Verwacht aantal kanten `= p · C(1000,2) = 0,01 × 499500 ≈ 4995`. De matrix heeft
`1000² = 1.000.000` plaatsen, dus ongeveer 99,5% ervan is nul.

**2.** De adjacentiematrix. Driehoeken door `v` tellen betekent buurverzamelingen snijden, en met
bitmaskerrijen is dat één `&` plus een popcount — 64 knopen per machinewoord. Hoofdstuk 2 mat een winst
van factor 48 bij `p = 0,5`.

**3.** De rij is een Python-geheel getal van willekeurige precisie, dus `rows[u] >> v` schuift een getal
van 600 bits of meer en raakt elk cijfer onder `v`. Dat is `O(n)`, niet `O(1)`. De meting toonde de kloof
groeien van 1,7× bij `n = 64` tot ongeveer 6× bij `n = 16384`.

**4.** Een Python-`set` draagt ruwweg twee kilobyte overhead voordat hij iets bevat, en er zijn er `n`;
een geheel getal van 600 bits is ongeveer 100 byte. In C zou een adjacentielijst bij `p = 0,05` werkelijk
kleiner zijn — het resultaat is een feit over de containers van Python, niet over adjacentielijsten.

## Hoofdstuk 3 — Graad

**1.** Nee. Negen knopen van graad 3 geven een graadsom van 27, wat oneven is, in tegenspraak met
`Σ deg(v) = 2m`. Equivalent: het aantal knopen van oneven graad moet even zijn, en 9 is oneven.

**2.** Niet grafisch. Havel–Hakimi: verwijder de 4 en trek één af van de volgende vier plaatsen, wat
`[2, 1, 0, −1]` geeft — negatief, dus het faalt. Intuïtief moet een knoop van graad 4 in een graaf met 5
knopen aan alles grenzen, dus niets kan graad 0 hebben.

**3.** `Σ deg(v) = 3 × 10 = 30`, dus `m = 15`.

**4.** Op één knoop is er geen paar om te vergelijken, dus de conclusie is niet eens betekenisvol. De
duivenhokstap van het bewijs heeft `n` graden nodig uit een verzameling van grootte `n − 1`, en dat
vergt `n ≥ 2` om de verzameling niet-leeg te laten zijn. De verificatie geeft `None` terug voor `n < 2`
in plaats van `True`, want de stelling zegt daar niets.

## Hoofdstuk 4 — Wandelingen, paden, samenhang

**1.** In `C₅` met knopen `0..4`: de wandeling `0,1,0,1` herhaalt knopen en kanten, dus ze is geen pad.
Het pad `0,1,2` is geen cykel — het keert niet terug naar zijn start.

**2.** `(A²)_{vv} = deg(v)`. Een gesloten wandeling van lengte 2 vanuit `v` gaat naar een buur en meteen
terug, dus er is er precies één per buur.

**3.** `n − 1`, precies bereikt door de bomen (hoofdstuk 6).

**4.** Twee paden aan elkaar plakken geeft een *wandeling*, die knopen kan herhalen. Het
wandeling-naar-padlemma — een kortste wandeling tussen twee knopen herhaalt niets — zet haar terug om in
een pad. Zonder dat lemma faalt transitiviteit en is "samenhangscomponent" niet welgedefinieerd.

## Hoofdstuk 5 — Isomorfie

**1.** Nee. `C₆` is samenhangend en twee disjuncte driehoeken niet, en samenhang blijft onder isomorfie
behouden. Geen berekening nodig.

**2.** Isomorfe grafen moeten in elke invariant overeenkomen, dus onenigheid bewijst niet-isomorfie; maar
veel niet-isomorfe grafen komen in een gegeven invariant overeen, dus overeenstemming bewijst niets.

**3.** Verfijning herkleurt een knoop met zijn eigen kleur plus de multiverzameling kleuren van zijn
buren. In een `d`-reguliere graaf begint elke knoop identiek en heeft hij `d` identieke buren, dus de
partitie is al stabiel bij ronde nul en splitst nooit.

**4.** 11. `len(all_graphs_up_to_iso(4))` geeft 11 — de rij is 1, 2, 4, 11, 34, 156 (OEIS A000088).

## Hoofdstuk 6 — Bomen

**1.** 11 kanten: een boom heeft `m = n − 1`.

**2.** Twee, bereikt door het pad `Pₙ`. Het langste-padargument toont dat beide uiteinden van een maximaal
pad bladeren zijn, dus er zijn er altijd minstens twee.

**3.** Precies één. De twee eindpunten hadden al een uniek pad ertussen, en de nieuwe kant sluit precies
dat pad tot een cykel.

**4.** Nee. `C₄` is bipartiet en heeft een cykel, dus hij is geen boom. Bipartiet is veel zwakker: het
verbiedt alleen oneven cykels.

## Hoofdstuk 7 — Opspannende bomen en de formule van Cayley

**1.** 16, en Cayley geeft `4^(4−2) = 4² = 16`. `len(spanning_trees(complete(4)))` bevestigt het.

**2.** `[1, 2]`. Verwijder het kleinste blad (0) en noteer zijn buur 1; dan is het kleinste blad 1, met
buur 2. Er blijven twee knopen over, dus we stoppen — de rij heeft lengte `n − 2 = 2`.

**3.** Dat een knoop `deg(v) − 1` keer voorkomt betekent dat een blad, met `deg = 1`, nul keer voorkomt.
De labels die in de rij ontbreken zijn dus precies de bladeren.

**4.** 1296 telt bomen op een *vaste gelabelde* knopenverzameling; 6 telt isomorfieklassen. Veel
verschillende labelingen geven dezelfde vorm — het onderscheid van hoofdstuk 5 tussen gelijkheid en
isomorfie, toegepast op tellen.

## Hoofdstuk 8 — Doorlopen

**1.** BFS. DFS is niet slechts trager — het geeft *een* pad terug, dat willekeurig veel langer kan zijn
dan het kortste. In het voorbeeld van hoofdstuk 8 bereikt DFS een aangrenzende knoop als laatste, na een
omweg van zeven kanten.

**2.** Beide zijn `O(n + m)`: elke knoop komt één keer in de wachtrij of op de stapel, en elke kant wordt
twee keer bekeken, één keer vanaf elk eindpunt. De houder verandert het aantal operaties niet, alleen
hun volgorde.

**3.** Een oneven cykel. De twee eindpunten liggen op gelijke afstand van de bron, dus de twee boompaden
plus deze kant sluiten een cykel van oneven lengte. Dit is precies het algoritme van hoofdstuk 16.

**4.** De standaardrecursielimiet van Python is 1000 frames, dus een recursieve DFS crasht op een padgraaf
van tienduizend knopen — een graaf die enkel lang is en niet groot.

## Hoofdstuk 9 — Minimale opspannende bomen

**1.** De **strikt** lichtste kant over een willekeurige snede behoort tot elke minimale opspannende boom.
"Strikt" is het dragende woord: bij gelijke gewichten zit elke gelijk gewogen kant in *een* MOB en hoeft
geen ervan in *alle* te zitten.

**2.** `C₄` met alle gewichten 1 en een koorde — of de vierknoopsgraaf `{(0,2),(0,3),(1,2),(1,3)}` met
eenheidsgewichten, die hoofdstuk 9 door uitputtend zoeken als het kleinste geval vond. Kruskal geeft
`{(0,2),(0,3),(1,2)}` en Prim vanaf knoop 1 geeft `{(0,2),(1,2),(1,3)}`, beide van gewicht 3.

**3.** Een minimaal opspannend **bos** — één boom per component. Het faalt niet; de union-find voegt
eenvoudigweg nooit over componenten heen samen.

**4.** Wanneer alle kantgewichten verschillend zijn. Dan kan geen gelijkstand optreden, geldt de
snede-eigenschap overal met striktheid, en is de MOB uniek.

## Hoofdstuk 10 — Kortste paden

**1.** De laatste stap, waar gezegd wordt dat de rest van een pad vanaf de nieuw bereikte knoop naar het
doel "er alleen bij optelt". Met een negatieve boog kan die rest het totaal verlagen, en de ongelijkheid
faalt.

**2.** `O(nm)`, tegen Dijkstra's `O(m log n)`. Het relaxeert elke boog `n − 1` keer omdat het niets kan
afhandelen: zonder niet-negativiteit is er geen knoop die het definitief kan verklaren.

**3.** Een negatieve cykel bereikbaar vanuit de bron. Na `n − 1` ronden kan geen enkelvoudig pad meer
verbeteren, dus elke verdere verbetering vergt een wandeling die met winst meer dan `n − 1` bogen
gebruikt.

**4.** Die bestaat niet. Nog eens rond de cykel gaan verlaagt het totaal onbegrensd, dus het infimum is
`−∞` en de vraag is slecht gesteld in plaats van slechts moeilijk.

## Hoofdstuk 11 — Afstand tussen alle paren

**1.** `O(n³)`, en helemaal geen datastructuur — drie geneste lussen over een vlakke array, zonder
prioriteitswachtrij en zonder allocatie.

**2.** `k` indexeert de inductie op *welke knopen een pad mag doorkruisen*; `i` en `j` doorlopen binnen een
vaste fase. Met `i` buitenste kan `dist[0][1]` definitief worden terwijl `dist[3][1]` nog oneindig is.
Hoofdstuk 11 mat dat de kapotte versie afweek op 942 van de 4000 willekeurige digrafen terwijl ze op een
padgraaf correct was.

**3.** Die knoop ligt op een negatieve cykel. Merk op dat dit verschilt van de test van Bellman–Ford, die
vraagt of er een *bereikbaar is vanuit een gegeven bron*.

**4.** `Digraph(2, [(0,1,1)])`: `d(0,1) = 1` en `d(1,0) = ∞`. Gerichte afstand is een quasimetriek, geen
metriek.

## Hoofdstuk 12 — Samenhang en de stelling van Menger

**1.** Elk `s`–`t`-pad ontmoet de snede, en inwendig disjuncte paden kunnen geen snedeknoop delen, dus
`#paden ≤ |snede|`. Ze bewijst op zichzelf niets omdat ze geen reden geeft dat de grens bereikt wordt —
genoeg natuurlijke min-max-paren hebben een echte kloof, `ω ≤ χ` onder meer.

**2.** Zijn `s` en `t` aangrenzend, dan kan geen verzameling *andere* knopen ze scheiden, dus er is
helemaal geen `s`–`t`-knopensnede. De grootheid rechts is ongedefinieerd, niet groot.

**3.** Beide ongelijkheden kunnen strikt zijn, al niet in de eenvoudigste voorbeelden. Twee driehoeken
verbonden door een lang pad geven `δ = 2`, `λ = 1`, `κ = 1` — geverifieerd met `edge_connectivity` en
`vertex_connectivity` — dus `κ = λ < δ`. Voor `κ < λ` neem je twee kopieën van `K₄` die één knoop delen:
die snijknoop geeft `κ = 1`, terwijl `λ = 3` want je moet alle drie de kanten bij een knoop vernietigen,
en `δ = 3`.

**4.** De inwendige boog begrenst de stroom *door* de knoop op 1, dus twee paden kunnen hem niet delen —
en dat is wat de paden inwendig disjunct maakt. Kanten krijgen oneindige capaciteit omdat de stelling
knopen telt en geen kanten, en een kant mag nooit de flessenhals zijn.

## Hoofdstuk 13 — Max-stroom min-snede

**1.** Ze laten het algoritme een eerdere beslissing terugdraaien. Zonder ze kan een vroeg gulzig pad een
beter later pad blokkeren en heeft de zoektocht geen manier om te herleiden — gulzig paden duwen is dan
eenvoudigweg fout, niet slechts suboptimaal.

**2.** Met willekeurige paden en irrationale capaciteiten kan Ford–Fulkerson eeuwig doorlopen en naar een
waarde onder het maximum convergeren. Met gehele capaciteiten termineert het maar kan het tijd kosten
evenredig met de *waarde* van de stroom, wat exponentieel is in de invoergrootte. Kortste paden (BFS)
geven `O(nm²)` ongeacht.

**3.** Gehele capaciteiten geven een gehele maximale stroom, want elke vermeerdering duwt een gehele
flessenhals. Het doet ertoe omdat Menger en koppeling nodig hebben dat het antwoord een *verzameling*
paden of kanten is; een fractioneel optimum kon niet als zodanig afgelezen worden.

**4.** Niets. De capaciteit van een snede telt alleen bogen van de bronzijde naar de putzijde. In het
voorbeeld van hoofdstuk 13 loopt de boog `(3,2)` met capaciteit 9 achterwaarts over de snede en draagt ze
nul bij.

## Hoofdstuk 14 — Koppeling

**1.** Een alternerend pad — kanten afwisselend buiten en binnen `M` — waarvan beide eindpunten
ongekoppeld zijn. Omkeren verhoogt `|M|` met precies één, want het heeft één niet-koppelingskant meer dan
koppelingskanten.

**2.** `M` is maximaal dan en slechts dan als er geen `M`-vermeerderend pad bestaat. Het bewijs gebruikt
**symmetrisch verschil**: `M △ N` heeft maximale graad 2, dus zijn componenten zijn paden en even cykels,
en is `|N| > |M|` dan moet een component een vermeerderend pad zijn.

**3.** Een oneven cykel. Een alternerende wandeling kan terugkeren naar een knoop met tegengestelde
pariteit, en de zoektocht kan een vermeerderend pad niet van een lus onderscheiden. Edmonds'
bloesemalgoritme lost het op door oneven cykels samen te trekken. Het getuigenis van hoofdstuk 14 is `C₇`;
`C₃` en `C₅` leggen de fout niet bloot.

**4.** Maximale koppeling 1, minimale knopenoverdekking 2 — geverifieerd door uitputtend zoeken. Ze
verschillen omdat een driehoek niet bipartiet is, en de stelling van König bipartietheid vereist. Dit is
het kleinste tegenvoorbeeld.

## Hoofdstuk 15 — Kleuring

**1.** Een geldige kleuring verdeelt de knopen in kleurklassen, elk een onafhankelijke verzameling van
grootte hoogstens `α(G)`. `n` knopen bedekken vergt dus minstens `n / α(G)` klassen.

**2.** `C₅`: `ω = 2` (driehoekvrij) en `χ = 3` (oneven cykel). Het is de kleinste zo'n graaf — elke graaf
op hoogstens 4 knopen is perfect, zoals de uitputtende controle van hoofdstuk 19 bevestigt.

**3.** Orden de knopen volgens de degeneratie-eliminatie en tel: elke knoop heeft hoogstens `d` buren die
al geplaatst zijn wanneer hij verwijderd wordt, dus sommeren over de knopen geeft `m ≤ d · n`.

**4.** De kroongraaf op `2n = 8` knopen heeft degeneratie 3, dus de grens garandeert slechts `d + 1 = 4`
kleuren — en gulzig in de afwisselende volgorde gebruikt er precies 4. De grens wordt gerespecteerd; ze is
alleen veel zwakker dan `χ = 2`.

## Hoofdstuk 16 — Bipartiete grafen

**1.** Is hij bipartiet, dan is de grootste zijde een onafhankelijke verzameling met minstens de helft van
de knopen, en dat erft elke deelgraaf. Omgekeerd, heeft een deelgraaf geen zo'n onafhankelijke
verzameling, dan bevat die deelgraaf een oneven cykel, dus is de graaf niet bipartiet.

**2.** `⌊n²/4⌋`, bereikt door de gebalanceerde volledig bipartiete graaf `K_{⌈n/2⌉,⌊n/2⌋}`. Voor `n = 6`
is dat `K₃,₃` met 9 kanten. Dit is de stelling van Mantel (hoofdstuk 27), want bipartiete grafen zijn
driehoekvrij.

**3.** De Petersen-graaf heeft omtrek 5 en is niet bipartiet. Elke graaf die een geïnduceerde `C₅` bevat en
geen kortere cykel werkt, bijvoorbeeld `C₇`, of de vijfcykel met een hangende knoop.

**4.** Driehoekvrijheid is *lokaal* — bekijk elk drietal knopen, `O(n³)` — terwijl bipartietheid *globaal*
is, maar BFS berekent haar in `O(n + m)` omdat de niveaustructuur al het werk in één keer doet. De
goedkopere test levert de sterkere eigenschap omdat één doorloop een globale beperking voortplant.

## Hoofdstuk 17 — Vlakheid

**1.** Was elke graad minstens 6, dan `2m = Σ deg(v) ≥ 6n`, dus `m ≥ 3n`, in tegenspraak met
`m ≤ 3n − 6`.

**2.** `K₅` min een kant heeft `n = 5`, `m = 9 ≤ 3·5 − 6 = 9`, en `is_planar` bevestigt dat hij vlak is.
Eén kant weghalen is precies genoeg.

**3.** De Petersen-graaf heeft omtrek 5, dus elk vlakdeel in elke inbedding zou minstens 5 kanten nodig
hebben, wat `2m ≥ 5f` geeft. Met `n = 10`, `m = 15` dwingt Euler `f = 7` af, maar `2·15 = 30 < 35 = 5·7`.
Tegenspraak.

**4.** Eén. Een boom heeft `m = n − 1`, dus Euler geeft `f = 2 − n + (n−1) = 1` — alleen het buitenvlak.
`planar_face_count(path(5))` geeft 1.

## Hoofdstuk 18 — De vijf- en de vierkleurenstelling

**1.** `m ≤ 3n − 6` dwingt een knoop van graad hoogstens 5 af (oefening 17.1), en dat geldt voor elke
deelgraaf omdat deelgrafen van vlakke grafen vlak zijn. Vlakke grafen zijn dus 5-degeneraat, en de grens
van hoofdstuk 15 geeft `χ ≤ d + 1 = 6`.

**2.** De laatste stap, waar gezegd wordt dat een pad van `v₂` naar `v₄` het `v₁`–`v₃`-pad niet kan
kruisen. Kruisingen bestaan niet in een vlakke inbedding; dat is de enige topologische invoer in het
argument.

**3.** De graaf `K₄` met één knoop verdubbeld — bijvoorbeeld `K₅` min één kant — heeft `χ = 4` en is vlak,
zoals hierboven geverifieerd. Elke vlakke triangulatie die `K₄` bevat werkt ook.

**4.** Na de eerste Kempe-verwisseling zijn de kleuren van de buren van `v` veranderd, dus de configuratie
die de tweede verwisseling rechtvaardigde hoeft niet meer te gelden. De twee verwisselingen kunnen op
elkaar inwerken: de ene uitvoeren kan de belemmering hercreëren die de andere moest wegnemen. Kempe nam
onafhankelijkheid aan en Heawood vond het geval waarin dat faalt.

## Hoofdstuk 19 — Perfecte en koordale grafen

**1.** `C₅` heeft geen driehoek, dus `ω = 2`. Hij is een oneven cykel, dus 2 kleuren zijn onmogelijk en 3
volstaan, wat `χ = 3` geeft. De uitputtende routines van het boek geven precies dit.

**2.** De knopen van een intervalgraaf zijn intervallen, aangrenzend wanneer ze overlappen. Neem in een
cykel van lengte ≥ 4 het interval met het meest linkse rechteruiteinde; zijn twee cykelburen overlappen het
allebei, dus ze overlappen elkaar — een koorde.

**3.** Omdat de klasse **erfelijk** moet zijn om bruikbaar te zijn, en erfelijke klassen zijn precies die
welke door verboden geïnduceerde deelgrafen definieerbaar zijn. Alleen `χ(G) = ω(G)` eisen laat `C₅` plus
een disjuncte `K₃` toe, die `χ = ω = 3` heeft en toch de canonieke imperfecte graaf bevat.

**4.** `P₄` (het pad op 4 knopen) is zelfcomplementair, en hij is perfect — zelfs koordaal, dus de
stelling van hoofdstuk 19 is van toepassing. `C₅` is de zelfcomplementaire graaf die *niet* perfect is.

## Hoofdstuk 20 — Hamiltoniciteit

**1.** Een Hamiltoniaanse cykel in een bipartiete graaf wisselt tussen de zijden, dus hij bezoekt er
evenveel van elk — wat `a = b` afdwingt. Omgekeerd heeft `K_{a,a}` met `a ≥ 2` een voor de hand liggende
alternerende cykel. `is_hamiltonian(complete_bipartite(2,3))` is `False` en `(3,3)` is `True`.

**2.** Een Hamiltoniaanse cykel geeft twee inwendig disjuncte paden tussen elk paar, dus de graaf is
2-samenhangend per Menger (hoofdstuk 12), en een 2-samenhangende graaf heeft geen snijknoop.

**3.** Is elke graad minstens `n/2`, dan heeft elk tweetal knopen graadsom minstens `n`, dus de hypothese
van Ore geldt. Uitputtend zoeken geeft het kleinste voorbeeld dat aan Ore voldoet en niet aan Dirac: op 5
knopen, kanten `{(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,3)}` met graadrij `[3,3,3,3,2]`. Knoop 4 heeft
graad `2 < 5/2`, dus Dirac faalt; elk niet-aangrenzend paar sommeert nog altijd tot minstens 5, dus Ore
geldt — en de graaf is inderdaad Hamiltoniaans.

**4.** `k` knopen uit een Hamiltoniaanse graaf verwijderen breekt de cykel in hoogstens `k` bogen, dus er
blijven hoogstens `k` componenten over. De ster `K₁,₃` faalt hieraan: verwijder het middelpunt en er
blijven drie componenten over uit één verwijdering, dus hij is niet Hamiltoniaans.

## Hoofdstuk 21 — Klieken, onafhankelijke verzamelingen, overdekkingen

**1.** `C₆`: `α = 3`, `τ = 3`, `α + τ = 6 = n`. `ω = 2`, want `C₆` is driehoekvrij.

**2.** `C₅` heeft `ω = 2` en `α = 2`, dus `ω · α = 4 < 5 = n`. Dit is het kleinste tegenvoorbeeld; elke
graaf op hoogstens 4 knopen voldoet aan de ongelijkheid.

**3.** `τ(G)` is gelijk aan de grootte van een maximale koppeling, per de stelling van König (hoofdstuk 14).

**4.** Het complement van een ijle graaf is dicht: `m = O(n)` wordt `Θ(n²)`. Een algoritme waarvan de
looptijd van `m` afhangt vertraagt dus met een factor `n`, ook al is de reductie zelf polynomiaal. De
complexiteitstheorie rekent de reductie als goedkoop; je processor niet.

## Hoofdstuk 22 — NP-moeilijkheid

**1.** Herleid een bekend moeilijke `A` **naar** `B`. Dat toont dat `B` oplossen `A` zou oplossen, dus `B`
erft de moeilijkheid van `A`. `B` naar `A` herleiden toont slechts dat `B` niet moeilijker is dan iets
moeilijks, en dat geldt ook voor elk probleem in `P`.

**2.** Zonder tegenstrijdigheidskanten kon een onafhankelijke verzameling `x` uit de driehoek van de ene
clausule kiezen en `¬x` uit die van een andere. De gekozen literalen kwamen dan met geen enkele
consistente toekenning overeen, dus de (⟸)-richting faalt.

**3.** Zonder de driehoeken kon een onafhankelijke verzameling van grootte `k` verschillende literalen uit
één clausule nemen en geen uit een andere, waardoor die clausule onvervuld blijft. De driehoeken zijn wat
precies één literaal per clausule afdwingt.

**4.** Nee. `NP`-moeilijkheid is een uitspraak over het slechtste geval over *alle* invoeren. Beperken tot
bipartiete invoer is een ander probleem, en dat het eenvoudig is zegt niets over het algemene — dit is het
derde antwoord uit de lijst van hoofdstuk 23.

## Hoofdstuk 23 — Leven met hardheid

**1.** Het algoritme voegt beide eindpunten toe van elke kant die het neemt, en het neemt `|M|` kanten, dus
het geeft precies `2|M|` knopen terug. Dat `M` **maximaal** is betekent dat er geen kant bij kan, dus elke
kant van `G` raakt een gekoppelde knoop — en dat is precies wat het resultaat tot een overdekking maakt.

**2.** Eén kant: `OPT = 1` en de heuristiek geeft beide eindpunten, dus 2. Algemener elke perfecte
koppeling op `2k` knopen zonder andere kanten.

**3.** Voor `n = 10⁶` en `k = 10`: `2^k(n+m) ≈ 1024 · 10⁶ ≈ 10⁹` operaties, tegen `n^k = 10⁶⁰`. De eerste
is in seconden klaar; de tweede overtreft het aantal atomen in het waarneembare heelal.

**4.** De equivalentie van hoofdstuk 21 behoudt *exacte* antwoorden, geen *parameters*. Een
knopenoverdekking van grootte `k` komt overeen met een onafhankelijke verzameling van grootte `n − k`, dus
de kleine parameter aan de ene kant wordt een enorme aan de andere. Geparametriseerde complexiteit is
gevoelig voor welke grootheid `k` heet, en de reductie behoudt haar niet.

## Hoofdstuk 24 — De probabilistische methode

**1.** Kleur elke knoop onafhankelijk rood of blauw met kans 1/2; elke kant steekt over met kans 1/2; per
lineariteit van de verwachting is het verwachte aantal oversteken `m/2`; een of andere uitkomst haalt
minstens het gemiddelde. Onafhankelijkheid wordt nergens gebruikt — lineariteit geldt hoe dan ook, en de
kantgebeurtenissen zijn werkelijk gecorreleerd wanneer kanten een knoop delen.

**2.** Richt elke kant willekeurig. Elk van de `n!` knoopordeningen is een Hamiltoniaans pad met kans
`2^{−(n−1)}`, dus het verwachte aantal is `n!/2^{n−1}`, en een of ander toernooi haalt minstens het
gemiddelde.

**3.** Neem elke knoop onafhankelijk met kans `p` op. Het verwachte aantal overlevende knopen is `pn` en
van overlevende kanten `p²m`. Verwijder één eindpunt per overlevende kant: de rest is onafhankelijk en
heeft verwachte grootte `pn − p²m`. Optimaliseren bij `p = n/(2m)` geeft `n²/(4m)`.

**4.** De snedegrens laat zich ontrandomiseren met voorwaardelijke verwachtingen omdat de verwachting
*lokaal* berekend en vergeleken kan worden, knoop voor knoop. Voor Ramsey is er geen bekende manier om de
voorwaardelijke verwachting van "geen monochromatische `K_k`" efficiënt te evalueren, dus de gulzige stap
is niet te zetten.

## Hoofdstuk 25 — Toevalsgrafen

**1.** `E[driehoeken] = C(n,3)p³ ≈ n³p³/6`. Dit gaat naar nul wanneer `p ≪ 1/n` en naar oneindig wanneer
`p ≫ 1/n`, dus de drempel is `1/n`.

**2.** Een variabele kan een groot gemiddelde hebben en toch bijna altijd nul zijn, als ze af en toe
reusachtig is — bijvoorbeeld een variabele gelijk aan `n²` met kans `1/n` en anders nul heeft gemiddelde
`n` en is meestal nul. Dat uitsluiten vergt de variantie.

**3.** Een gegeven knoop is geïsoleerd wanneer geen van zijn `n − 1` mogelijke kanten verschijnt, met kans
`(1−p)^{n−1}`; vermenigvuldig met `n`. Met `p = c ln n / n` wordt dit `≈ n^{1−c}`, wat bij `c = 1` naar een
constante gaat.

**4.** In `G(n, 1/2)` heeft elke gelabelde graaf op `n` knopen dezelfde kans `2^{−C(n,2)}`, dus de
verdeling is uniform. Een eigenschap die met kans naar 1 geldt, geldt dus voor een fractie van alle grafen
die naar 1 gaat.

## Hoofdstuk 26 — De reuzencomponent

**1.** `β = 1 − e^{−1,5β}` itereren convergeert naar `β ≈ 0,5828`. De gemeten grootste component bij
`c = 1,5, n = 400` was `0,581` van de graaf — overeenstemming tot ongeveer drie duizendsten.

**2.** De benadering neemt aan dat elke nieuw bereikte knoop `≈ n` onverkende mogelijke buren heeft. Zodra
een constante fractie verkend is, daalt dat aantal wezenlijk, het effectieve gemiddelde nageslacht zakt
onder `c`, en de groei vertraagt — en dat is wat de reuzencomponent bij `βn` stopt in plaats van bij `n`.

**3.** Twee componenten van grootte `εn` hebben `ε²n²` mogelijke kanten ertussen. Bij `p = c/n` is de kans
dat er geen verschijnt `(1 − c/n)^{ε²n²} ≈ e^{−cε²n}`, wat naar nul gaat. Ze zouden dus vrijwel zeker
verbonden zijn, in tegenspraak met dat het verschillende componenten zijn.

**4.** `c < 1` betekent `R₀ < 1`: elk geval brengt gemiddeld minder dan één nieuw geval voort, en de
uitbraak dooft uit. De op één na grootste component komt overeen met de grootste van de kleine
zelfbeperkende clusters — de lokale uitbraken die nooit epidemieën werden.

## Hoofdstuk 27 — Extremale grafentheorie

**1.** `K₂,₃` heeft 6 kanten, is driehoekvrij (bipartiet), en `n²/4 = 6,25`, dus hij haalt de grens zo
scherp als een geheel getal bij `n = 5` kan.

**2.** Het aantal kanten is `Σ_{i<j} aᵢaⱼ`, wat bij vaste som `Σaᵢ = n` gemaximaliseerd wordt wanneer de
delen zo gelijk mogelijk zijn. Een knoop van een groter naar een kleiner deel verplaatsen verhoogt de
producttermen strikt — het standaard convexiteitsargument, hetzelfde dat Cauchy–Schwarz codeert.

**3.** `χ(K₃) = 3`, `χ(K₄) = 4`, `χ(Petersen) = 3` — alle drie bevestigd met `chromatic_number`. Dus `K₃`
en de Petersen-graaf delen `r = 2` en geven dezelfde hoofdterm `(1 − 1/2)n²/2 = n²/4`; `K₄` heeft `r = 3`
en geeft `n²/3`. De Petersen-graaf heeft tien knopen en vijftien kanten tegen de drie en drie van de
driehoek, en een van beide verbieden kost asymptotisch hetzelfde — wat het hele punt van de stelling is.

**4.** Is `χ(H) = 2`, dan is `r = 1` en is de hoofdterm `(1 − 1/1)n²/2` nul, dus Erdős–Stone reduceert tot
`o(n²)` en bepaalt niets over de werkelijke orde. Die vinden is het probleem van Zarankiewicz, in het
algemeen open.

## Hoofdstuk 28 — Ramsey-theorie

**1.** Neem een willekeurige knoop van `K₆`. Zijn 5 kanten dragen 2 kleuren, dus minstens 3 delen er een —
zeg dat `v` rood verbonden is met `a, b, c`. Is een van `ab, bc, ac` rood, dan geeft die kant met `v` een
rode driehoek; is er geen rood, dan is `abc` een blauwe driehoek.

**2.** Het getuigenis heeft rode kanten `{(0,3),(0,4),(1,2),(1,4),(2,3)}`, en dat is een vijfcykel. Zijn
complement is eveneens een vijfcykel. `C₅` is driehoekvrij, dus geen van beide kleurklassen bevat een
driehoek — geverifieerd met `canonical` tegen `cycle(5)` in beide richtingen.

**3.** `R(2,4) = 4` (met 2 aan de ene kant volstaat één kant van die kleur, dus je hebt alleen genoeg
knopen nodig om 4 onderling niet-aangrenzende af te dwingen), en `R(3,3) = 6`. De recursie geeft
`R(3,4) ≤ 4 + 6 = 10`. De werkelijke waarde is 9.

**4.** `K₄₃` heeft `C(43,2) = 903` kanten, elk onafhankelijk rood of blauw, wat `2^903` kleuringen geeft.
Dat ligt ver buiten elke denkbare berekening — het aantal atomen in het waarneembare heelal is ongeveer
`2^266`.

## Hoofdstuk 29 — Spectrale grafentheorie

**1.** `A(K_n) = J − I` met `J` overal enen. `J` heeft eigenwaarden `n` (één keer) en `0` (`n−1` keer), dus
`A` heeft `n − 1` één keer en `−1` met multipliciteit `n − 1`. Voor `K₄` geeft de oplosser
`[−1, −1, −1, 3]`.

**2.** `Σλᵢ² = spoor(A²)`, en `(A²)_{vv}` telt gesloten wandelingen van lengte 2 vanuit `v`, en dat is
`deg(v)`. Sommeren geeft `Σ deg(v) = 2m`.

**3.** `n(−λ_min)/(d − λ_min) = 10 · 2/(3 + 2) = 4`, en `α(Petersen) = 4` per uitputtend zoeken. De grens
is precies scherp.

**4.** Het spectrum is een invariant, dus isomorfe grafen delen het en een verschil weerlegt isomorfie.
Maar cospectrale niet-isomorfe grafen bestaan — `K₁,₄` en `C₄ + K₁` geven beide `{−2, 0, 0, 0, 2}` — dus
overeenstemming stelt niets vast.

## Hoofdstuk 30 — De Laplaciaan

**1.** `xᵀDx = Σ_v deg(v)x_v²` en `xᵀAx = 2Σ_{uv∈E} x_u x_v`. Aftrekken en per kant hergroeperen geeft
`Σ_{uv∈E}(x_u² + x_v² − 2x_u x_v) = Σ_{uv∈E}(x_u − x_v)²`. Een som van kwadraten is niet-negatief, dus `L`
is positief semidefiniet.

**2.** `L(K₃)` heeft eigenwaarden `{0, 3, 3}`. Rij en kolom 0 schrappen laat `[[2, −1], [−1, 2]]` over met
determinant `3`, en `K₃` heeft inderdaad 3 opspannende bomen — één voor elke weggelaten kant. Cayley is het
ermee eens: `3^{3−2} = 3`.

**3.** Elke rij van `L` sommeert tot nul, want de diagonaalplaats `deg(v)` wordt opgeheven door de
`deg(v)` plaatsen `−1`. Dus `L · 1 = 0`, wat de al-enen-vector tot eigenvector met eigenwaarde 0 maakt.

**4.** Hoe moeilijk de graaf in tweeën te knippen is. `P₄` valt uiteen door één kant te verwijderen; `K₄`
is helemaal niet goedkoop te splitsen. De ongelijkheid van Cheeger maakt dit precies, door het
isoperimetrisch getal `h(G)` tussen `λ₂/2` en `√(2Δλ₂)` in te sluiten.

## Hoofdstuk 31 — Minoren en boombreedte

**1.** Eén zak met alle vier de knopen: breedte `4 − 1 = 3`. Er bestaat geen betere, want elke kant moet
binnen een zak liggen, en de kanten van `K₄` dwingen elk zakkenstelsel dat ze overdekt om alle vier de
knopen samen te bevatten — een kliek belandt altijd in één zak.

**2.** Zodat bomen boombreedte 1 hebben in plaats van 2. De decompositie van een boom heeft zakken van
grootte 2 (één per kant), en er één aftrekken laat de conventie overeenkomen met de intuïtie dat bomen het
eenvoudigste niet-triviale geval zijn.

**3.** Verwerk het rooster kolom voor kolom: elke zak bevat de twee knopen van één kolom plus de twee van
de volgende, dus zakken hebben grootte hoogstens 3 en de breedte is 2. `treewidth(grid(2,n))` geeft 2 voor
`n = 2, 3, 4`.

**4.** Het `k × k`-rooster, met boombreedte `k` en vlak. Het doet ertoe omdat begrensde boombreedte via de
stelling van Courcelle lineaire-tijdalgoritmen geeft en vlakheid alleen niet — dus de twee beperkingen
zijn werkelijk onafhankelijk en vlakke problemen blijven moeilijk.

## Hoofdstuk 32 — Expanders, en waar je hierna heen gaat

**1.** Omdat expansie een eigenschap van een groeiende familie is, en `h(Cₙ) = 4/n → 0`. Je kunt een cykel
altijd met twee kanten doorknippen, hoe groot hij ook wordt, dus de verhouding tussen rand en grootte
verdwijnt. Eén `C₆` die als "Ramanujan" gerapporteerd wordt zegt niets over de familie.

**2.** `d = 3` en de niet-triviale eigenwaarden zijn `1` en `−2`, dus `λ = 2`. De Ramanujan-grens is
`2√(d−1) = 2√2 ≈ 2,828`, en `2 ≤ 2,828`.

**3.** Een bipartiete graaf heeft `−d` in zijn spectrum juist *omdat* hij bipartiet is, dus die behouden
zou elke bipartiete graaf brandmerken als slechte expander om een reden die niets met samenhang te maken
heeft — vandaar dat de Ramanujan-voorwaarde haar laat vallen. Het mengingslemma moet haar behouden: in
`K₃,₃` geeft `S = {0}` en `T = {1}` aan dezelfde zijde `e(S,T) = 0` tegen een verwachte `0,5`, en met `−3`
uitgesloten zou de grens `0` zijn.

**4.** Trek een willekeurige `d`-reguliere graaf en begrens, met de uniegrens, de kans dat een of andere
verzameling van hoogstens `n/2` knopen een kleine rand heeft; het aantal slechte verzamelingen weegt niet
op tegen hoe onwaarschijnlijk elke afzonderlijk is. Dat bewijst dat de familie bestaat zonder er een te
noemen — dezelfde kloof als bij de Ramsey-ondergrens in hoofdstuk 28, en het duurde tot 1988 en
getaltheorie om haar expliciet te dichten.
