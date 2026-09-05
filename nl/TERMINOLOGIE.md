# Terminologie

De Nederlandse grafentheorie kent voor verschillende begrippen meer dan één gangbare term.
Deze vertaling maakt hieronder een keuze en houdt die consequent vol. Wie een andere
voorkeur heeft, kan hier één term wijzigen en de rest van de vertaling erop nazoeken.

## Kernbegrippen

| Engels | Nederlands | Opmerking |
|---|---|---|
| graph | **graaf** | meervoud: grafen |
| vertex | **knoop** | ook gangbaar: hoekpunt, punt |
| edge | **kant** | ook gangbaar: rib, lijn |
| arc | **boog** | uitsluitend voor gerichte grafen |
| directed / undirected | **gericht / ongericht** | |
| neighbour | **buur** | |
| degree | **graad** | |
| adjacent | **aangrenzend** | |
| subgraph | **deelgraaf** | |
| induced subgraph | **geïnduceerde deelgraaf** | |
| complement | **complement** | |

## Structuur

| Engels | Nederlands |
|---|---|
| walk | **wandeling** |
| path | **pad** |
| cycle | **cykel** |
| connected | **samenhangend** |
| component | **component** |
| tree / forest | **boom / bos** |
| leaf | **blad** |
| spanning tree | **opspannende boom** |
| bipartite | **bipartiet** |
| planar | **vlak** |
| face | **vlakdeel** |
| minor | **minor** |
| treewidth | **boombreedte** |
| chordal | **koordaal** |
| chord | **koorde** |
| simplicial vertex | **simpliciale knoop** |
| perfect elimination ordering | **perfecte eliminatievolgorde** |
| hole / antihole | **gat / antigat** |
| odd hole | **oneven gat** |
| perfect graph | **perfecte graaf** |

## Optimalisatie

| Engels | Nederlands |
|---|---|
| colouring | **kleuring** |
| chromatic number | **chromatisch getal** |
| clique | **kliek** |
| independent set | **onafhankelijke verzameling** |
| vertex cover | **knopenoverdekking** |
| matching | **koppeling** |
| flow | **stroom** |
| cut | **snede** |
| shortest path | **kortste pad** |
| eigenvalue | **eigenwaarde** |
| degeneracy | **degeneratie** |
| greedy | **gulzig** |
| crown graph | **kroongraaf** |
| proper colouring | **geldige kleuring** |
| Hamiltonian | **Hamiltoniaans** |
| Eulerian circuit | **Euler-circuit** |
| closure (Bondy-Chvatal) | **afsluiting** |
| reduction | **reductie** |
| NP-hard / NP-complete | **NP-moeilijk / NP-volledig** |
| approximation ratio | **benaderingsfactor** |
| gadget | **gadget** |
| probabilistic method | **probabilistische methode** |
| linearity of expectation | **lineariteit van de verwachting** |
| union bound | **uniegrens** |
| deletion method | **verwijderingsmethode** |
| threshold | **drempel** |
| giant component | **reuzencomponent** |
| branching process | **vertakkingsproces** |
| extremal | **extremaal** |
| trace | **spoor** |
| interlacing | **verstrengeling** |
| cospectral | **cospectraal** |
| Laplacian | **Laplaciaan** |
| algebraic connectivity | **algebraïsche samenhang** |
| Cheeger constant | **Cheeger-constante** |
| relaxation | **relaxatie** |

## Wat níet vertaald is

**Eigennamen van stellingen** blijven staan: de stelling van Menger, Turán, Ramsey, Cayley,
König, Hall, Brooks, Dirac, Ore. Dat is ook de Nederlandse gewoonte.

**Alle code, alle programma-uitvoer, en alle identifiers.** Elk stuk uitvoer in dit boek is
door het programma geproduceerd; het vertalen ervan zou het onwaar maken. `is_connected`
blijft `is_connected`, en een regel als `held ch16 Konig: G is bipartite iff...` blijft
letterlijk staan, omdat dat is wat de verificatie werkelijk afdrukt.

**Vaktermen zonder ingeburgerd Nederlands equivalent**: expander, Ramanujan-graaf, minor,
NP-volledig (wel vertaald), fixed-parameter tractable (onvertaald gelaten waar het als
vakterm functioneert).

## Bewuste afwijkingen

- **`n` en `m`** blijven de aantallen knopen en kanten, zoals in het Engelse origineel en in
  de internationale literatuur.
- **Getalnotatie** volgt de Nederlandse conventie in lopende tekst (49.154 woorden), maar
  programma-uitvoer blijft onaangeraakt (`49,154`), omdat dat letterlijk is wat er verschijnt.
- **"whp"** (with high probability) wordt **"met hoge waarschijnlijkheid"**, voluit.
