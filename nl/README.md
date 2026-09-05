# Grafentheorie: van eerste definities tot onderzoek

Een boek dat begint bij "wat is een graaf" en eindigt bij grafenminoren en spectrale
expansie, en dat onderweg de bewijzen serieus neemt.

Dit is de Nederlandse vertaling van het Engelse boek in de hoofdmap van deze repository. De
code, de verificatie en de figuren zijn gedeeld; alleen de tekst is vertaald.

## Status van de vertaling

Deze vertaling is **compleet**: alle 32 hoofdstukken en alle vier de bijlagen, inclusief de 128
uitgewerkte oplossingen.

| Deel | Hoofdstukken | Status |
|---|---|---|
| I — Grondslagen | 1–5 | **compleet** |
| II — Bomen en doorlopen | 6–9 | **compleet** |
| III — Afstand, samenhang, stroom | 10–14 | **compleet** |
| IV — Kleuring en structuur | 15–19 | **compleet** |
| V — Hardheid | 20–23 | **compleet** |
| VI — Moderne grafentheorie | 24–30 | **compleet** |
| VII — Grenzen | 31–32 | **compleet** |
| Bijlagen | A, B, C, E | **compleet** |

Vertaald:

- [Hoofdstuk 1 — Wat een graaf is](chapters/01-wat-een-graaf-is.md)
- [Hoofdstuk 2 — Representaties](chapters/02-representaties.md)
- [Hoofdstuk 3 — Graad](chapters/03-graad.md)
- [Hoofdstuk 4 — Wandelingen, paden, samenhang](chapters/04-wandelingen-en-samenhang.md)
- [Hoofdstuk 5 — Isomorfie](chapters/05-isomorfie.md)
- [Hoofdstuk 6 — Bomen](chapters/06-bomen.md)
- [Hoofdstuk 7 — Opspannende bomen en de formule van Cayley](chapters/07-opspannende-bomen.md)
- [Hoofdstuk 8 — Doorlopen](chapters/08-doorlopen.md)
- [Hoofdstuk 9 — Minimale opspannende bomen](chapters/09-minimale-opspannende-bomen.md)
- [Hoofdstuk 10 — Kortste paden](chapters/10-kortste-paden.md)
- [Hoofdstuk 11 — Afstand tussen alle paren](chapters/11-alle-paren.md)
- [Hoofdstuk 12 — Samenhang en de stelling van Menger](chapters/12-menger.md)
- [Hoofdstuk 13 — Max-stroom min-snede](chapters/13-max-stroom.md)
- [Hoofdstuk 14 — Koppeling](chapters/14-koppeling.md)
- [Hoofdstuk 15 — Kleuring](chapters/15-kleuring.md)
- [Hoofdstuk 16 — Bipartiete grafen](chapters/16-bipartiet.md)
- [Hoofdstuk 17 — Vlakheid](chapters/17-vlakheid.md)
- [Hoofdstuk 18 — De vijf- en de vierkleurenstelling](chapters/18-vier-kleuren.md)
- [Hoofdstuk 19 — Perfecte en koordale grafen](chapters/19-perfecte-grafen.md)
- [Hoofdstuk 20 — Hamiltoniciteit](chapters/20-hamiltoniciteit.md)
- [Hoofdstuk 21 — Klieken, onafhankelijke verzamelingen, overdekkingen](chapters/21-klieken-en-overdekkingen.md)
- [Hoofdstuk 22 — NP-moeilijkheid](chapters/22-np-moeilijkheid.md)
- [Hoofdstuk 23 — Leven met hardheid](chapters/23-benaderen.md)
- [Hoofdstuk 24 — De probabilistische methode](chapters/24-probabilistische-methode.md)
- [Hoofdstuk 25 — Toevalsgrafen](chapters/25-toevalsgrafen.md)
- [Hoofdstuk 26 — De reuzencomponent](chapters/26-reuzencomponent.md)
- [Hoofdstuk 27 — Extremale grafentheorie](chapters/27-extremaal.md)
- [Hoofdstuk 28 — Ramsey-theorie](chapters/28-ramsey.md)
- [Hoofdstuk 29 — Spectrale grafentheorie](chapters/29-spectraal.md)
- [Hoofdstuk 30 — De Laplaciaan](chapters/30-laplaciaan.md)
- [Hoofdstuk 31 — Minoren en boombreedte](chapters/31-minoren-en-boombreedte.md)
- [Hoofdstuk 32 — Expanders, en waar je hierna heen gaat](chapters/32-expanders.md)

Bijlagen:

- [Bijlage A — Notatie](appendices/a-notatie.md)
- [Bijlage B — Woordenlijst](appendices/b-woordenlijst.md)
- [Bijlage C — Verder lezen](appendices/c-verder-lezen.md)
- [Bijlage E — Oplossingen bij de oefeningen](appendices/e-oplossingen.md)

De volledige Engelse tekst staat in [`../chapters/`](../chapters/) en
[`../appendices/`](../appendices/).

## Terminologie

De Nederlandse grafentheorie kent voor verschillende begrippen meer dan één gangbare term.
[TERMINOLOGIE.md](TERMINOLOGIE.md) legt de keuzes vast — graaf, knoop, kant, wandeling,
opspannende boom, kleuring — zodat ze consequent blijven en zodat wie een andere voorkeur
heeft, precies weet wat er te wijzigen valt.

## Wat níet vertaald is, en waarom

**Alle code en alle programma-uitvoer blijft in het Engels.** Elk stuk uitvoer in dit boek is
door het programma geproduceerd en tegen de werkelijkheid gecontroleerd; het vertalen ervan
zou het onwaar maken. Een regel als

```
  held      ch 3  Havel-Hakimi agrees with brute-force realisability  (52 graphs)
```

staat er zoals `scripts/verify_theorems.py` hem werkelijk afdrukt. Hetzelfde geldt voor
identifiers: `is_connected` blijft `is_connected`, want zo heet de functie.

Dat is dezelfde regel die het hele boek volgt, nu toegepast op de vertaling: **wat gemeten is,
wordt niet herschreven.**

## De PDF bouwen

```bash
python scripts/build_pdf.py --source nl
```

Dat schrijft `graph-theory-book-nl.pdf`, die in deze repository staat naast de Engelse.
