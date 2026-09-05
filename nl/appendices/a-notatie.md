# Bijlage A — Notatie

Elk symbool dat in dit boek gebruikt wordt, met het hoofdstuk dat het invoert.

## De graaf zelf

| Symbool | Betekenis | H. |
|---|---|---|
| `G = (V, E)` | een graaf: knopenverzameling en kantenverzameling | 1 |
| `n` | aantal knopen, `\|V\|` | 1 |
| `m` | aantal kanten, `\|E\|` | 1 |
| `uv` | de kant die `u` en `v` verbindt | 1 |
| `Ḡ` | het complement | 1 |
| `G[S]` | de deelgraaf geïnduceerd op knopenverzameling `S` | 1 |
| `G − v`, `G − e` | een knoop verwijderen, een kant verwijderen | 4 |
| `G / e` | een kant samentrekken | 17 |

## Benoemde grafen

| Symbool | Betekenis | H. |
|---|---|---|
| `K_n` | volledige graaf, `n(n−1)/2` kanten | 1 |
| `P_n` | pad op `n` knopen, `n−1` kanten | 1 |
| `C_n` | cykel op `n` knopen, `n` kanten, `n ≥ 3` | 1 |
| `K_{a,b}` | volledig bipartiete graaf, `ab` kanten | 1 |
| `T(n,r)` | Turán-graaf: volledig `r`-delig, zo gelijk mogelijke delen | 27 |

## Knopen en graden

| Symbool | Betekenis | H. |
|---|---|---|
| `N(v)` | de buren van `v` | 1 |
| `deg(v)` | de graad van `v`, `\|N(v)\|` | 3 |
| `Δ(G)` | maximale graad | 3 |
| `δ(G)` | minimale graad | 3 |
| `d(G)` | degeneratie | 15 |

## Afstand en samenhang

| Symbool | Betekenis | H. |
|---|---|---|
| `d(u,v)` | afstand: lengte van een kortste `u`–`v`-pad | 4 |
| `κ(G)` | knopensamenhang | 12 |
| `λ(G)` | kantensamenhang | 12 |
| `INF` | onbereikbaar, `float("inf")` in de code | 10 |

## Optimalisatieparameters

| Symbool | Betekenis | H. |
|---|---|---|
| `χ(G)` | chromatisch getal | 15 |
| `ω(G)` | kliekgetal | 15 |
| `α(G)` | onafhankelijkheidsgetal | 21 |
| `τ(G)` | knopenoverdekkingsgetal | 21 |
| `h(G)` | Cheeger-constante / isoperimetrisch getal | 30 |
| `tw(G)` | boombreedte | 31 |

De identiteit van Gallai verbindt er twee: `α(G) + τ(G) = n` (hoofdstuk 21).

## Matrices en spectra

| Symbool | Betekenis | H. |
|---|---|---|
| `A` | adjacentiematrix | 2 |
| `D` | diagonale graadmatrix | 30 |
| `L = D − A` | de Laplaciaan | 30 |
| `λ₁ ≤ … ≤ λ_n` | eigenwaarden, oplopend | 29 |
| `λ₂` | algebraïsche samenhang, voor `L` | 30 |
| `λ` | grootste niet-triviale `\|eigenwaarde\|` — **twee definities**, zie h. 32 | 32 |

Die laatste rij is een echte valstrik. `mixing_lambda` sluit alleen `d` uit; `spectral_expansion` sluit
voor bipartiete grafen ook `−d` uit. Hoofdstuk 32 legt uit waarom het mengingslemma de eerste nodig
heeft en de Ramanujan-voorwaarde de tweede.

## Asymptotiek en kans

| Symbool | Betekenis | H. |
|---|---|---|
| `O`, `Ω`, `Θ` | boven-, onder- en scherpe asymptotische grenzen | 2 |
| `o(f)` | strikt kleinere orde dan `f` | 27 |
| `G(n,p)` | toevalsgraaf: elke kant onafhankelijk met kans `p` | 25 |
| `E[X]` | verwachting | 24 |
| **mhw** | met hoge waarschijnlijkheid: naar 1 als `n → ∞` | 25 |

## Conventies die dit boek vastlegt

Teksten verschillen hierin, en een bewijs kan er stilzwijgend van afhangen.

- **Enkelvoudig als standaard.** Geen lussen, geen herhaalde kanten, geen richtingen, tenzij een
  hoofdstuk anders zegt. Richtingen komen in hoofdstuk 10, gewichten in hoofdstuk 9.
- **De lege graaf is samenhangend.** Hij heeft nul componenten, dus dit is een conventie, gekozen zodat
  "elke graaf is de disjuncte vereniging van zijn componenten" geen uitzondering nodig heeft
  (hoofdstuk 4).
- **Boombreedte trekt er één af**, zodat bomen boombreedte 1 hebben in plaats van 2 (hoofdstuk 31).
- **Eigenwaarden staan oplopend**, dus `λ_n` is de grootste.
- `e(S,T)` telt **geordende** paren, dus een kant binnen `S ∩ T` wordt twee keer geteld — de conventie
  waarin het mengingslemma geformuleerd is (hoofdstuk 32).
