# Bijlage C — Verder lezen

Waar je heen gaat voor elk deel van dit boek, en waar elke bron werkelijk goed in is.

## Algemene naslagwerken

**Diestel, *Graph Theory*.** Het standaard moderne tekstboek voor gevorderden, en degene om te bezitten
als je er één bezit. Volledig en streng over samenhang, minoren, extremale theorie en het
Robertson–Seymour-programma. Vrij beschikbaar via de site van de auteur. → Delen I–IV, VII

**Bondy en Murty, *Graph Theory*.** Breder en vriendelijker dan Diestel, met meer algoritmische inhoud
en een grote voorraad oefeningen. → Delen I–V

**West, *Introduction to Graph Theory*.** De toegankelijkste van de drie, en de beste bron van
uitgewerkte voorbeelden als de bewijzen in dit boek te snel gingen. → Delen I–IV

## Per onderwerp

**Alon en Spencer, *The Probabilistic Method*.** Hét boek over het onderwerp van hoofdstuk 24, en het
gaat ver voorbij wat dit boek behandelt — het lokale lemma van Lovász, martingaalconcentratie,
entropiemethoden, en de tweedemomentargumenten waarnaar hoofdstuk 26 alleen gebaarde. → H. 24–26, 28

**Bollobás, *Random Graphs*.** Het naslagwerk voor de hoofdstukken 25 en 26. Drempels, het kritieke
venster bij `c = 1`, en het `Θ(n^{2/3})`-gedrag dat dit boek alleen vermeldde. → H. 25, 26

**Bollobás, *Extremal Graph Theory*.** Turán-achtige problemen in de diepte, inclusief de bipartiete
gevallen waar Erdős–Stone zwijgt. → H. 27

**Graham, Rothschild en Spencer, *Ramsey Theory*.** Van der Waerden, Hales–Jewett, en het algemene
programma "volledige wanorde is onmogelijk". → H. 28

**Godsil en Royle, *Algebraic Graph Theory*.** De grondige behandeling van de hoofdstukken 29 en 30 —
verstrengeling, sterk reguliere grafen, en het materiaal over automorfismegroepen dat dit boek volledig
oversloeg. → H. 29, 30

**Chung, *Spectral Graph Theory*.** Opgebouwd rond de **genormaliseerde** Laplaciaan
`L = I − D^{−1/2} A D^{−1/2}`, die dit boek niet gebruikte en die het juiste object is voor irreguliere
grafen. → H. 30

**Spielman, collegenotities over spectrale en algebraïsche grafentheorie.** Vrij beschikbaar, modern, en
de helderste route naar de ongelijkheid van Cheeger en spectraal clusteren. → H. 30, 32

**Hoory, Linial en Wigderson, "Expander graphs and their applications"** (*Bulletin of the AMS*, 2006).
Een overzichtsartikel, en het beste startpunt voor hoofdstuk 32. → H. 32

## Algoritmen

**Cormen, Leiserson, Rivest en Stein, *Introduction to Algorithms*.** Het naslagwerk voor alles in deel
III. Het max-stroomnetwerk in hoofdstuk 13 komt daarvandaan. → H. 8–14

**Williamson en Shmoys, *The Design of Approximation Algorithms*.** De eerste helft van hoofdstuk 23,
naar behoren: LP-afronding, primaal-duaal, en de onbenaderbaarheidsresultaten die hier alleen geciteerd
werden. Vrij beschikbaar. → H. 23

**Cygan e.a., *Parameterized Algorithms*.** De tweede helft van hoofdstuk 23. Begrensde zoekbomen,
kernelisatie, boombreedte-DP naar behoren gedaan — inclusief het dynamisch programmeren dat hoofdstuk 31
beschreef maar niet implementeerde. Vrij beschikbaar. → H. 23, 31

**Kleinberg en Tardos, *Algorithm Design*.** De beste uitleg die er is over waarom stroomreducties
werken, als de tabel met coderingen in hoofdstuk 13 aanvoelde als een lijst trucs. → H. 13

## Wat dit boek bewust oversloeg

Elk hiervan is een echt gat, geen vergetelheid:

- **Hopcroft–Tarjan-vlakheidstest** in `O(n)`. Hoofdstuk 17 doorzoekt in plaats daarvan
  rotatiesystemen, wat exponentieel is en zichtbaar de stelling zelf.
- **Edmonds' bloesemalgoritme** voor algemene koppeling. Hoofdstuk 14 geeft alleen het bipartiete geval
  en toont waar het breekt.
- **Het algoritme van Johnson** voor alle-parenkortstepaden met negatieve bogen op ijle grafen.
  Hoofdstuk 11 beschrijft de herwegingstruc zonder haar te implementeren.
- **Boombreedte-DP** achter de stelling van Courcelle. Hoofdstuk 31 zegt waarom.
- **De genormaliseerde Laplaciaan**, het juiste spectrale object voor irreguliere grafen.
- **Gerichte grafentheorie** voorbij kortste paden en stroom: sterke samenhang, toernooien, en de
  gerichte tegenhangers van het grootste deel van de delen IV–VI.

## De vierkleurenstelling

Een eigen vermelding waard, aangezien hoofdstuk 18 haar niet kon bewijzen.

- De oorspronkelijke artikelen van Appel en Haken uit 1976, en de vereenvoudiging uit 1997 van
  Robertson, Sanders, Seymour en Thomas, die het aantal configuraties van 1936 tot 633 terugbracht.
- **Gonthier, "Formal Proof — The Four-Color Theorem"** (*Notices of the AMS*, 2008), over de volledig
  machinaal gecontroleerde Coq-versie. Het interessantste van de drie om te lezen, omdat het gaat over
  wat het betekent dat een bewijs geverifieerd is in plaats van begrepen.

## Open problemen uit dit boek

Vermeld in de hoofdstukken, en alle nog open:

- `R(5,5)`, waarvan alleen bekend is dat het in `[43, 46]` ligt. → H. 28
- Het probleem van Zarankiewicz: het extremale getal voor bipartiete `H`. → H. 27
- Het reconstructievermoeden: een graaf op `≥ 3` knopen wordt bepaald door de multiverzameling van zijn
  knoop-verwijderde deelgrafen. Open sinds 1942, en gênant eenvoudig te formuleren. → H. 5
- Of grafenisomorfie in `P` zit. → H. 5
- Een kliek van grootte `(1+ε) log₂ n` vinden in een toevalsgraaf, terwijl we precies weten hoe groot
  het antwoord is. → H. 25
- `P` tegenover `NP`. → H. 22

## Reeksen

De aantallen in dit boek komen uit de OEIS, en ertegen controleren is de goedkoopst mogelijke
verificatie van een opsommer:

- **A000088** — grafen op `n` knopen op isomorfie na: 1, 2, 4, 11, 34, 156, 1044. → H. 5
- **A000272** — gelabelde bomen, `n^(n−2)`: 1, 1, 3, 16, 125, 1296. → H. 7
