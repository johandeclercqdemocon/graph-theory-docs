# Grafentheorie: van eerste definities tot onderzoek

Een boek dat begint bij "wat is een graaf" en eindigt bij grafenminoren en spectrale
expansie, en dat onderweg de bewijzen serieus neemt.

Dit is de Nederlandse vertaling van het Engelse boek in de hoofdmap van deze repository. De
code, de verificatie en de figuren zijn gedeeld; alleen de tekst is vertaald.

## Status van de vertaling

Deze vertaling is **in uitvoering**. Het Engelse boek is compleet; hieronder staat wat er van
vertaald is.

| Deel | Hoofdstukken | Status |
|---|---|---|
| I — Grondslagen | 1–5 | 3 van 5 vertaald |
| II — Bomen en doorlopen | 6–9 | nog niet |
| III — Afstand, samenhang, stroom | 10–14 | nog niet |
| IV — Kleuring en structuur | 15–19 | nog niet |
| V — Hardheid | 20–23 | nog niet |
| VI — Moderne grafentheorie | 24–30 | nog niet |
| VII — Grenzen | 31–32 | nog niet |
| Bijlagen | A, B, C, E | nog niet |

Vertaald:

- [Hoofdstuk 1 — Wat een graaf is](chapters/01-wat-een-graaf-is.md)
- [Hoofdstuk 2 — Representaties](chapters/02-representaties.md)
- [Hoofdstuk 3 — Graad](chapters/03-graad.md)

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

Wanneer de vertaling compleet is:

```bash
python scripts/build_pdf.py --source nl
```

Dat schrijft `graph-theory-book-nl.pdf`. Er is bewust nog geen Nederlandse PDF ingecheckt: een
PDF van drie hoofdstukken die "het boek" heet, zou verkeerd voorstellen wat er klaar is.
