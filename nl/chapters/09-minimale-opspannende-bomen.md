# Hoofdstuk 9 — Minimale opspannende bomen

Geef de kanten gewichten en vraag om de goedkoopste opspannende boom. Twee gulzige algoritmen
lossen het op, en gulzige algoritmen werken bijna nooit — dus de interessante inhoud is de ene
eigenschap die beide correct maakt.

## De snede-eigenschap

Een **snede** is een verdeling van de knopen in twee niet-lege delen `(S, V∖S)`. Een kant
**kruist** de snede wanneer ze in elk deel één eindpunt heeft.

> **Stelling (snede-eigenschap).** Zij `(S, V∖S)` een willekeurige snede, en zij `e` een
> kruisende kant van strikt minimaal gewicht onder de kruisende kanten. Dan behoort `e` tot elke
> minimale opspannende boom.

*Bewijs.* Zij `T` een opspannende boom die `e = uv` niet bevat. `e` aan `T` toevoegen creëert
precies één cykel (het verwisselingsfeit uit hoofdstuk 6). Die cykel kruist de snede bij `e`, en
een cykel kruist elke snede een even aantal keren, dus hij kruist bij nog een kant `f ≠ e`. Nu is
`T + e − f` weer een opspannende boom, en omdat `w(e) < w(f)` door de strikte minimaliteit van
`e`, is hij strikt lichter dan `T`. Dus `T` was niet minimaal. ∎

Twee dingen in dat bewijs verdienen hun plaats. Het feit dat een cykel een snede **een even
aantal keren** kruist — loop de cykel rond en telkens als je `S` verlaat moet je terugkomen —
wordt opnieuw gebruikt in de hoofdstukken 13 en 17. En het verwisselingsfeit uit hoofdstuk 6 is
wat `T + e − f` tot een boom maakt, precies de reden waarom hoofdstuk 6 de moeite nam het te
bewijzen.

Het woord **strikt** draagt gewicht, en het weglaten ervan is de standaardfout. Delen twee
kruisende kanten het minimum, dan hoeft geen van beide in elke MOB te zitten; elk zit in *een*
MOB. De stelling zoals ze er staat is precies juist, en de versie zonder "strikt" is onwaar.

Er is een tegenhanger, op dezelfde manier bewezen:

> **Stelling (cykeleigenschap).** Is `e` de unieke zwaarste kant van een cykel, dan behoort `e`
> tot geen enkele minimale opspannende boom.

## Kruskal

Sorteer de kanten op gewicht en voeg elke kant toe tenzij ze een cykel zou sluiten.

```python
def kruskal(g):
    uf = UnionFind(g.n)
    chosen = []
    for u, v, _ in sorted(g.edges(), key=lambda e: e[2]):
        if uf.union(u, v):
            chosen.append((u, v))
    return chosen
```

*Correctheid.* Wanneer Kruskal een kant `e = uv` aanvaardt, zij `S` de verzameling knopen die al
via gekozen kanten met `u` verbonden zijn. Elke eerder bekeken kant die `(S, V∖S)` kruist werd
verworpen, en kanten worden in volgorde van gewicht bekeken, dus `e` is een kruisende kant van
minimaal gewicht. De snede-eigenschap is van toepassing. ∎

De looptijd is `O(m log m)` en zit volledig in het sorteren; de union-find-operaties zijn
effectief constant. Merk op dat Kruskal op een **onsamenhangende** graaf een minimaal opspannend
**bos** teruggeeft — één boom per component — in plaats van te falen. Dat is meestal wat je wilt,
en het is goed te weten dat je dat krijgt.

**Union-find** is de ondersteunende structuur: `find` geeft de vertegenwoordiger van een
verzameling, `union` voegt twee verzamelingen samen en meldt of ze al dezelfde waren. Met
padcompressie en samenvoegen op grootte kosten `m` operaties `O(m α(n))`, waarbij `α` de inverse
Ackermann-functie is — hoogstens 4 voor elke `n` die in het waarneembare heelal past. Dit boek
behandelt haar als constant en zegt er ronduit bij dat ze dat niet is.

## Prim

Laat één boom groeien vanuit een startknoop, en neem steeds de goedkoopste kant die hem verlaat.

```python
def prim(g, source=0):
    seen = {source}
    frontier = [(g.weight(source, x), source, x) for x in g.neighbours(source)]
    heapq.heapify(frontier)
    chosen = []
    while frontier:
        _, u, v = heapq.heappop(frontier)
        if v in seen:
            continue
        seen.add(v)
        chosen.append((min(u, v), max(u, v)))
        for x in g.neighbours(v):
            if x not in seen:
                heapq.heappush(frontier, (g.weight(v, x), v, x))
    return chosen
```

*Correctheid.* Bij elke stap is `seen` één zijde van een snede en neemt het algoritme een
kruisende kant van minimaal gewicht. De snede-eigenschap is rechtstreeks van toepassing. ∎

`O(m log n)` met een binaire heap. Anders dan Kruskal spant Prim alleen de component van de bron
— hij heeft geen manier om naar een andere te springen.

De twee algoritmen maken werkelijk verschillende keuzes over waarover ze gulzig zijn: Kruskal is
gulzig over *alle* kanten globaal, Prim over de kanten die één groeiende boom verlaten. Dat beide
werken, is de snede-eigenschap toegepast op twee verschillende families sneden.

## De MOB is niet uniek

Hier is het misverstand waarvoor dit hoofdstuk bestaat. "De" minimale opspannende boom suggereert
dat er één is. Er is precies één minimaal **gewicht**; er kunnen vele bomen zijn die het bereiken.

De verificatie registreert dit als een stelling waarvan verwacht wordt dat ze weerlegd wordt:

```
  refuted   ch 9  Kruskal and Prim always choose the same edges  (5 graphs)
  held      ch 9  Kruskal and Prim both achieve the true minimum weight  (91 graphs)
```

De tweede regel is de stelling; de eerste is het misverstand, en het wordt weerlegd in plaats van
bewezen.

Die controle aan de praat krijgen vergde een correctie die het optekenen waard is. Bij de eerste
poging kwamen de gewichten uit `1..20`, en de twee algoritmen waren het eens op **alle 79
grafen** — de bewering hield stand, en zag eruit als een stelling. Met gewichten uit `1..2`, zodat
gelijke gewichten vaak voorkomen, waren ze het oneens op **66 van de 3000**. Gelijke gewichten
zijn het hele mechanisme, en een willekeurige familie zonder gelijke gewichten kan het verschijnsel
helemaal niet zien. Zijn alle gewichten verschillend, dan *is* de MOB werkelijk uniek — een gevolg
van de snede-eigenschap met haar striktheid intact.

```python
from graphs.weighted import WeightedGraph
from graphs.mst import kruskal, prim, brute_force_mst, spanning_trees

wg = WeightedGraph(5, [(0,1,1), (0,2,3), (1,2,2), (1,3,6), (2,3,4), (3,4,5), (2,4,7)])
print(sorted(kruskal(wg)))                  # [(0, 1), (1, 2), (2, 3), (3, 4)]
print(brute_force_mst(wg)[1])               # 12
print(len(spanning_trees(wg.graph)))        # 21
```

Eenentwintig opspannende bomen, één van gewicht 12, en beide algoritmen vinden hem.

## Verificatie zonder circulariteit

Kruskal tegen Prim controleren zou alleen vaststellen dat twee van mijn gulzige implementaties het
eens zijn — wat ze kunnen zijn terwijl ze allebei fout zijn, want ze delen dezelfde redenering rond
de snede-eigenschap en dezelfde auteur. Daarom somt de verificatie **elke** opspannende boom op en
neemt ze de goedkoopste:

```python
def brute_force_mst(g):
    best = None
    for tree in spanning_trees(g.graph):
        w = g.subgraph_weight(tree)
        if best is None or w < best[1]:
            best = (tree, w)
    return best
```

`C(m, n−1)` deelverzamelingen, dus het is begrensd op zeven knopen. Dat volstaat: een fout in een
gulzig algoritme laat zich op kleine grafen zien, want de gulzige keuze is lokaal fout of helemaal
niet.

## Probeer het

Kijk hoe de twee algoritmen het oneens zijn over de boom terwijl ze het eens zijn over het gewicht:

```bash
python -c "
import sys; sys.path.insert(0, '.')
from graphs.weighted import WeightedGraph
from graphs.mst import kruskal, prim
# C_4 with every weight 1, so every spanning tree is minimum
g = WeightedGraph(4, [(0,2,1),(0,3,1),(1,2,1),(1,3,1)])
k = sorted(kruskal(g))
p = sorted((min(u,v), max(u,v)) for u,v in prim(g, source=1))
print('kruskal:', k, 'weight', g.subgraph_weight(k))
print('prim:   ', p, 'weight', g.subgraph_weight(p))
print('same weight:', g.subgraph_weight(k) == g.subgraph_weight(p), '  same edges:', k == p)
"
```

```
kruskal: [(0, 2), (0, 3), (1, 2)] weight 3
prim:    [(0, 2), (1, 2), (1, 3)] weight 3
same weight: True   same edges: False
```

Verschillende bomen, identieke kosten. Beide zijn minimale opspannende bomen; geen van beide is
*de* minimale opspannende boom.

Vier knopen is het kleinste geval waarop dit kan gebeuren, gevonden door uitputtend zoeken en niet
door te gissen — en de eerste twee grafen die ik gokte gaven beide algoritmen die het eens waren.

## Oefeningen

1. Formuleer de snede-eigenschap, en zeg welk woord erin het gewicht draagt.
2. Geef een graaf met twee verschillende minimale opspannende bomen van gelijk gewicht.
3. Wat geeft Kruskal terug wanneer de invoergraaf onsamenhangend is?
4. Onder welke voorwaarde is de minimale opspannende boom uniek?

Oplossingen in Bijlage E.

## Kernpunten

- De snede-eigenschap is het hele onderwerp: de strikt lichtste kant over een willekeurige snede
  zit in elke MOB. Beide algoritmen zijn gevolgen ervan.
- "Strikt" is geen versiering. Zonder dat woord is de stelling onwaar, en met gelijke gewichten
  houdt de MOB op uniek te zijn.
- Kruskal is globaal gulzig en geeft een bos op onsamenhangende invoer; Prim is gulzig vanuit één
  groeiende boom en spant alleen de component van de bron.
- Union-find kost `O(α(n))` per operatie, wat niet constant is en hoogstens 4.
- Verschillende gewichten ⟹ unieke MOB. Gelijke gewichten ⟹ vele. Een willekeurige testfamilie met
  breed gespreide gewichten laat je dit nooit zien: 0 meningsverschillen op 79 grafen bij gewichten
  `1..20`, 66 op 3000 bij gewichten `1..2`.
