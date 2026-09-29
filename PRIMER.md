# PRIMER — hdoku26-visuals

Arbeitsplan für die Grafiken zum Vortrag „Orte ohne Normdatensatz? Wikidata und
OpenStreetMap als interdisziplinäre Community-Hub-Alternative für Geografika“
(Berliner Herbsttreffen zur Museumsdokumentation, ZIB Berlin, Mo 05.10.2026,
11:30–12:00; direkt danach Barbara Fischer, DNB, zu GND-Neuerungen).

Zu Beginn jedes Chats hochladen, am Ende zurückschreiben.

---

## Teil A — Immer gültig

### A1 Ausgangslage

| Was | Rolle |
|---|---|
| bb-5kbc-visuals | Stilvorlage: Utils, Palette, Canvas, Hausregeln — hierher kopiert, nicht referenziert |
| c't 19/2026, S. 118–121 („Von Karteikarten zur KI“) | Bezugstext für alle GND-Aussagen; Zitate in `data/raw/ct/quotes.yaml` |
| Abstract (genehmigt) | Rahmen: Community-Hubs als bewusste Gegenentscheidung zum autoritativen Vokabular; Crossys/TRAIL 2.5 als Voraussetzung |

**Befunde (geprüft 2026-09-22):**

- **Die GND hat Garranes** — GND 1248049489, Entitätentyp gik, „Irland; Archäologische Stätte“, Beschreibung „Mittelalterliche Ringwallanlage d. 5.-6. Jh. in Südwestirland“. Die frühere Annahme „Garranes hat keinen Normdatensatz“ war **falsch**. Die Frage des Vortrags ist deshalb nicht *ob*, sondern *was* ein Datensatz weiß und womit er verbunden ist.
- Der GND-Datensatz hat **keine Koordinate**, keine Zwischenebene zwischen Irland und der Stätte, als `owl:sameAs` nur VIAF. Katalogisierungsquelle laut GND Explorer: GeoNames 3299501 (nicht im Turtle-Download).
- **GeoNames 3299501** ist eine *Locality* Garranes bei 51.944, −8.270 — **36,6 km** vom Townland Garranes (Templemartin). Beschreibung (Ringwall 5.–6. Jh. = Lisnacaheragh im Townland Garranes) und Quelle zeigen räumlich auseinander.
- **Lisnacaheragh** hat **kein eigenes Wikidata-Item**. Q31066388 „Garranes“ ist ein Vorgebirgsfort am Dooneen Point, 87,2 km westlich — nicht das GND-Ringfort. Lissacresig (Q30590991) ist ein anderer Ort (Macroom, 23,5 km) und kommt nicht vor.
- Townland Garranes Q104295278: Logainm 8299, OSM-Relation 6168494. Ogham-Site Q69385525 hängt daran (24 m), Belege CIIC Vol. 1 (Q70256237) und townlands.ie (Q70851365). Die Fundstelle selbst hat **kein OSM-Objekt** (im Gelände nicht sichtbar); der Stein CIIC 81 steht heute in UCC Cork (OSM-Node 11071361392, `moved_from=Garranes, Co. Cork souterrain`).
- GND kennt „Oghamschrift“ (Sachbegriff) und Richard Rolt Brash (Person); Kinalmeaky und Templemartin: 0 Treffer. „Freshford“ in der GND ist Freshford/Somerset (7759398-4, Quelle Encarta); das irische Freshford und „Lachtain“ fehlen.
- Q30590991 (Lissacresig) trägt die falsche Commons-Kategorie „Skeagh Cairn“ — faires Gegenbeispiel: Community-Daten haben Fehler, aber sichtbar und korrigierbar.
- Netz im Autoren-Sandbox: GitHub, Wikidata, lobid, DNB-Portal gesperrt; Daten kamen als Uploads/Screenshots. Fira Sans und Natural Earth kamen über npm.

### A2 Zielbild

```
data/raw/ (Wikidata-JSON, GND-TTL, OSM-XML, manual/*.yaml, ct/quotes.yaml, Natural Earth)
      │
      ▼  python main.py   (offline, deterministisch)
py/step_NN_*.py  ──►  img/NN-*/<name>.{de,en}.{svg,png}
```

Eigenschaften:
1. Jede Zahl und jede ID in einer Grafik stammt aus einer Datei unter `data/raw/`; Abstände werden gerechnet.
2. Jedes c't-Zitat trägt Seite; Autorentext und indirekte Rede stehen nicht als Personenzitat.
3. Zwei Läufe hintereinander → `git status` sauber.
4. Diplomatischer Ton: GND wird über ihren Auftrag beschrieben, nicht über Defizite.

### A3 Querschnittsregeln

- Rohdaten unter `data/raw/`, unverändert, read-only; Produkte nach `img/`.
- Wiederverwendung heißt kopieren (Utils aus bb-5kbc-visuals), nicht referenzieren.
- Keine Uhr in der Ausgabe: `RELEASE`-Konstante, kein `datetime.now()`.
- Kein Netzzugriff in den Schritten.
- Hausregeln aus bb-5kbc-visuals: 1750×1000, Fira Sans, kein Titel/Footer eingebrannt, **keine Diagonalen**, DE+EN.
- Sprache: PRIMER deutsch, alles andere britisches Englisch; Grafiken DE und EN.
- Windows ist Referenzplattform; Befehle einzeilig für `cmd`.

### A4 Beschlusslage

| Frage | Beschluss | seit |
|---|---|---|
| Drei große Grafiken zum Komplex GND vs. Wikidata/OSM | 1 Status quo („Ein Name, viele Orte“), 2 Zukunft (Wikibase-Konvergenz, GNDplus, Semantic OSM), 3 Nische = Hub | 2026-09-22 |
| Leitbeispiel | Garranes (Townland, Ogham-Site Q69385525, Stein CIIC 81 als Nebenfigur); Holy Well St. Lachtain (Q121840779) als zweites Beispiel in Grafik 3 | 2026-09-22 |
| Ton | diplomatisch | 2026-09-22 |
| Nische | Hub-Funktion, Community-Daten (VGI), Mini-Wissensgraphen Wikidata–Logainm–OSM(–GND) plus daran hängende Infos — nicht „die GND hat nichts“ | 2026-09-22 |
| bb-5kbc, geo-lod, poseidon2lod | nicht in diesen Grafiken; eigene Case-Study-Folien nach Ogham und Holy Wells | 2026-09-22 |
| Stil | wie bb-5kbc-visuals; Palette: GND ocker, Community-Hubs petrol, GeoNames grau, „ohne Koordinate“ rot gestrichelt, Zitate amber | 2026-09-22 |
| Zitate | pro Grafik gemeinsam auswählen; Grafik 1: A1 + A2 (Autorentext S. 119); Grafik 2: Z2, Z4, Z6 + P3, P4, P5, P6; Z3 verworfen (würde Ketts Worte gegen ihn wenden) | 2026-09-22 |
| Einleitung | zwei Zusatzgrafiken in `img/00-einleitung/`: 00a „Drei Drehkreuze“ (Idee A), 00b „Dicht und dünn“ (Idee B); c't-Bilder (Cover, Aufmacher, GND-Explorer-Graph) nicht im Repo, nur gestrichelte Rahmen mit Bildnachweis (00a); eigene GND-Explorer-Screenshots (Berners-Lee, Goethe) eingebettet in 00b (`data/raw/screenshots/`); in 00a statt des c't-Berners-Lee-Bilds das Beispiel Konrad Zuse (Namensgeber des Tagungsorts): eigener GND-Explorer-Screenshot, Geburts-/Sterbeort auf schematischer Deutschlandkarte, Foto W. Hunscher (CC BY-SA 3.0); Platzhalter nur als Text, ohne Rahmen; allgemeine Zitate E1–E3, F1–F3; Zahlen in `ct/facts.yaml` | 2026-09-22 |
| Zitatboxen | fester Höhe: kursiv, Schrift so groß, dass der Text die Box füllt (`svg_quote_fill`); Boxen einer Reihe teilen eine Schriftgröße (Minimum der Einzelgrößen); gilt für 00a, 00b, 01, 03 — 02 hat mitwachsende Karten | 2026-09-22 |
| Folien-Untertitel | kurze Variante: 00a „Drei Drehkreuze: GND, Wikiversum und OSM“, 00b „Dicht bei Personen, dünn bei Fundstellen“, 01 „Ohne Geometrie bleibt offen, welches Garranes gemeint ist“, 02 „Beide Seiten bewegen sich auf Wikibase zu“, 03 „Die Nische ist der Hub – und jede Aussage hat eine Quelle“ | 2026-09-22 |
| Grafik 3 | Zitate Z5 (Achse), Z7 (Auszug), Z9 (Auszug); Z8 verworfen (neben Z7 konfrontativ), Z1 nicht verwendet; OSM-Nutzernamen dürfen genannt werden (öffentlich); Lissacresig-Karte weggelassen (würde verwirren) — faires Gegenbeispiel ist der wikidata-Tag am Stein | 2026-09-22 |
| Grafik 2 rechts | der Stein CIIC 81 (Q130529871) als Beispiel der Föderation, angebunden an Garranes über P189 — der rote Faden: Ort (Grafik 1) → Objekt (Grafik 2) | 2026-09-22 |
| Repo-Name | `hdoku26-visuals` (github.com/florianthiery/hdoku26-visuals) | 2026-09-22 |
| Kennungs-Tags in Karten | alle gleich breit (volle Kartenbreite), Text linksbündig, gemeinsame Startlinie über alle Karten einer Reihe | 2026-09-22 |
| Case Studies | gleiche Bildsprache wie Grafik 1–3: Ogham (2 Steine), Holy Wells (2 Brunnen oder ein Use Case), geo-lod, bb-5kbc, poseidon2lod; Schwerpunkt immer **Geografika** | 2026-09-22 |
| Case-Study-Raster | bis zu drei Grafiken pro Case Study, über alle gleich aufgebaut, **A und B auf getrennten Folien**: **A Rollen** (Zeilen GND · Wikidata/Wikibase · OSM · Fach-Hubs, Spalten = Beispiele; Spalte geteilt in Fundort / Standort heute, bei Fundort = Standort zusammengelegt; pro Zelle ein Status-Symbol + Kennungs-Tags); **B Ortskette** (Karte + Kette Objekt → Fundort → Townland → Baronie → County, bei getrennten Orten zweite Kette über P276; GND-Zeile darüber); **C Graph dahinter** (fachliche Kette, die zum Ort zurückführt: Ogham Inschrift → Name → Sippe → Baronie; Holy Wells Heilige usw.; GND-Zeile + „gelesen von“) — den Graph dahinter gibt es bei allen Beispielen | 2026-09-22 |
| Case Studies: keine c't-Zitate | die GND erscheint dort nur als Datenzeile; Rolle von GND, Wikidata/Wikibase und OSM soll sichtbar sein | 2026-09-22 |
| Status-Vokabular | vorhanden (gefüllt, Hubfarbe) · eine Ebene höher (Pfeil, z. B. GND-Ringwall statt Stein) · fehlt (Kreuz) · offen (grau gestrichelt „?“) · unsicher/umstritten (rot „?“); Symbole als Pfade gezeichnet (Fira Sans hat kein ✓ ✗ →) | 2026-09-22 |
| Hub-Leiste | unter jedem Knoten in B und C vier Kästchen G · W · O · F (GND, Wikidata/Wikibase, OSM, Fach-Hubs wie Logainm/SMR/CISP/TM); Ort = eckiger Kasten, Begriff/Name = runder Kasten (violett) | 2026-09-22 |
| GND in B und C | eigene Zeile über den Knoten, senkrechte Linie zum Knoten: durchgezogen = Satz vorhanden · **gestrichelt ocker = Eintrag nach GND-Planung denkbar** · grau gepunktet = vermutlich vorhanden, zu prüfen; in C zusätzlich „gelesen von“ (Forschende, bei denen die GND dicht ist → Bezug zu 00b) | 2026-09-22 |
| fuzzy-sl | liefert in B die Geometrie: pro Koordinate Ort-Typ (Findspot / Exhibition Site) und Sicherheit (High = Marker, Low = roter gestrichelter Ring) mit Quelle; in A als Kennungs-Tag in der Wikibase-Zeile | 2026-09-22 |
| Farbe OSM | eigenes Grün (`#e3eed9` / `#4f7a2a`) in den Case Studies; Grafiken 00a–03 bleiben unverändert | 2026-09-22 |
| Karten in B | dürfen größer werden, solange der Rest lesbar bleibt | 2026-09-22 |
| Zwei Beispiele pro Case Study | ja, aber nur wenn sich die beiden **geografisch** unterscheiden (bei Ogham: Fundort ≠ Standort gegen Fundort = Standort); zwei gleichartige Beispiele kosten Platz ohne Aussage | 2026-09-28 |
| Karten in den Case Studies | immer mit OSM-Geometrie anreichern, nach dem Muster aus S5: nächstgrößere Einheit als Fläche, kleinere darin, Objekt als Marker — die Karte trägt genau die Ebenen, die rechts in der Kette stehen; je Case Study eine Overpass-Abfrage (`out geom`), Datei nach `data/raw/osm/`, gerundet auf 5 Nachkommastellen; gezeichnete OSM-Geometrie bekommt die ODbL-Namensnennung unter der Karte | 2026-09-28 |
| Grafik C | nur dort, wo der fachliche Graph wirklich zu einem Ort zurückführt; sonst nur A und B | 2026-09-28 |
| Drei Folien je Case Study, immer gleich gebaut | A, B und C liegen auf demselben Raster: zwei Beispielspalten bei `CASE_C1`/`CASE_C2`, Ketten mit `chain_xs(...)` bis an die Inhaltskante, Legenden unten bei `CASE_LEGEND_Y`. Der gemeinsame Teil steht seit 2026-09-29 in `hdoku26_visuals_utils.py` unter „Case-study layout contract“, nicht mehr fünfmal kopiert in den Schritten | 2026-09-29 |
| Keine Infobox unter A und C | die Zusammenfassungs-Bänder am Fuß von Grafik A und die Schluss-Chips in Grafik C sind raus; unter der letzten Zeile steht nur noch die Status-Legende. Flo spricht diese Inhalte (Abdeckungstabelle, „die GND datiert Orte“, „Kennungen machen Fehler auffindbar“) | 2026-09-29 |
| Fotos im Kopf von Grafik A | 150 × 150 links vom Titel, Bildnachweis darunter; zwei Aufnahmen desselben Orts teilen sich den Platz übereinander (Franchthi), statt ihn zu verbreitern — das Raster bleibt gleich, auch wo kein Bild steht (bb-5kbc, poseidon2lod) | 2026-09-29 |
| Legende: ganz oder gar nicht | wo eine Legende steht, stehen **beide** Zeilen — die vier Hub-Farben bei `CASE_LEGEND_Y` und die GND-Spur bei `CASE_LEGEND_Y2`, 36 px auseinander, damit sie als zwei Zeilen lesbar sind. Ein Aufruf (`case_legend`), damit keine Grafik eine halbe Legende bekommt | 2026-09-29 |
| Vertikale Aufteilung in Grafik C | die zwei Beispiele werden mit `case_split` gesetzt: der übrige Weißraum wird auf oben / Mitte / unten verteilt, außen auf `CASE_SPLIT_MARGIN` gedeckelt, so dass er sich in der Mitte um die Trennlinie sammelt statt am Fuß. Bei etwa gleich hohen Beispielen (geo-lod, poseidon2lod) landet die Linie in der Mitte; ist eines deutlich höher (Ogham), folgt sie dem Inhalt, statt hindurchzuschneiden | 2026-09-29 |
| Reihenfolge | Grafik 2, dann 3, dann die Case Studies: Ogham fertigstellen (nach dem Fragebogen), dann Holy Wells, geo-lod, bb-5kbc, poseidon2lod — jeweils erst die Daten im Detail ansehen | 2026-09-22 |

### A5 Was in welchem Chat hochgeladen wird

Das ganze Repo ohne `img/`, `.git/`, `.venv/`:

    robocopy hdoku26-visuals %TEMP%\hdoku26-bundle /E /XD .git .venv img __pycache__ & powershell Compress-Archive -Path %TEMP%\hdoku26-bundle\* -DestinationPath hdoku26-bundle.zip -Force

Dazu bei Bedarf das c't-PDF (nicht ins Repo).

---

## Teil B — Schrittübersicht

| ID | Schritt | hängt ab von | Status |
|---|---|---|---|
| S0 | Festlegungen (Grafikfolge, Leitbeispiel, Palette) | — | erledigt 2026-09-22 |
| S1 | Skelett: main.py, Utils, Daten, Lizenz | S0 | erledigt 2026-09-22 |
| S1b | Einleitungsgrafiken 00a, 00b | S1 | Entwurf 2026-09-22 |
| S2 | Grafik 1 „Ein Name, viele Orte“ | S1 | erledigt 2026-09-22 (Iteration 2: Tags) |
| S3 | Grafik 2 „Zukunft: Wikibase-Konvergenz“ | S1 | Entwurf 2026-09-22 |
| S4 | Grafik 3 „Die Nische ist der Hub“ | S1 | Entwurf 2026-09-22 |
| S5 | Case Study Ogham (2 Steine) | S1 | erledigt 2026-09-28 (Grafiken A, B, C in `img/05-ogham/`) |
| S6 | Case Study Holy Wells (2 Brunnen) | S1 | erledigt 2026-09-28 (Grafiken A, B, C in `img/06-holy-wells/`) |
| S7 | Case Study geo-lod (CI-Fundstelle, SISAL-Höhle) | S1 | erledigt 2026-09-28 (Grafiken A, B, C in `img/07-geo-lod/`) |
| S8 | Case Study bb-5kbc (Brandenburg/Westpolen) | S1 | erledigt 2026-09-29 (Grafiken A, B, C in `img/08-bb-5kbc/`) |
| S9 | Case Study poseidon2lod (aDNA) | S1 | erledigt 2026-09-29 (Grafiken A, B, C in `img/09-poseidon/`) |
| S10 | Abschluss (Arbeitsteilung, fehlende Kanten, Tiefe der Verortung) | S5–S9 | erledigt 2026-09-29 (Grafiken in `img/10-abschluss/`) |

S3–S9 hängen nur vom Skelett ab; Reihenfolge laut A4: S3, S4, dann S5–S9.

---

## Teil C — Die Schritte

### S2 — Grafik 1 „Ein Name, viele Orte“

**Ziel:** Garranes als Homonymie-Fall: Karte mit vier nummerierten Orten, GND-Datensatz-Karte, vier Kandidatenkarten, zwei c't-Zitate (A1, A2).

**Abnahme:** Alle IDs/Zahlen aus `data/raw/`; Abstände gerechnet (36,6 / 87,2 km, 24 m); keine Überlappungen in DE und EN; keine Diagonalen; zweiter Lauf byte-identisch.

#### Erledigt 2026-09-22

- Iteration 1 committed (github.com/florianthiery/hdoku26-visuals).
- Iteration 2: Kennungs-Tags gleich breit und linksbündig (`svg_chip(width=, align="start")`), gemeinsame Startlinie der Tags über alle vier Karten.

### S3 — Grafik 2 „Zukunft“

**Ziel:** links GND (GNDplus Z2, Geodaten-Modul P3, steuerbare Offenheit Z4), rechts föderiertes Wikibase-Ökosystem am CIIC 81 (Wikidata, FactGrid, Semantic Kompakkt, fuzzy-sl) und Semantic OSM, Mitte roter Faden Garranes → CIIC 81 und die Brücke (P4, P5, Z6), Boden: Wikibase · LOD · CC0.

**Abnahme:** wie S2.

#### Entwurf 2026-09-22

- Alle Verknüpfungen rechts aus `Q130529871.json` gelesen (P189, P8168, P1325, P2888, P11693, P4057, P14097); fuzzy-sl Q74 als Rückverweis (gestrichelt) aus `manual/federation.yaml`.
- Befund: Der OSM-Tag `wikidata=Q106680733` zeigt nicht auf Q130529871; in Wikidata nur über P1382 „teilweise übereinstimmend“ verbunden — in der Grafik als Hinweis vermerkt, Überleitung zu Grafik 3 (Junctions dokumentieren).

### S4 — Grafik 3 „Die Nische ist der Hub“

**Ziel:** Mini-Wissensgraph Townland Garranes (Wikidata–Logainm–OSM, GND gestrichelt „Anschluss nach Identitätsklärung“), Holy Well als zweiter Teilgraph, VGI-Band, Crossys/TRAIL 2.5 als Fundament; Z7/Z8 als geteilter Anspruch, Z9 als Schluss.

**Abnahme:** wie S2.

#### Entwurf 2026-09-22

- Befund: Townland Q104295278 und Ogham-Site Q69385525 sind in Wikidata **nicht direkt verknüpft** (Site-P131 nennt Kinalmeaky, Templemartin, Munster, Cork — nicht das Townland). Beide tragen Logainm 8299 → in der Grafik als Treffpunkt/Junction gezeigt.
- Holy Well: Wikidata und OSM verweisen gegenseitig aufeinander (P10689 ↔ `wikidata=`), SMR und Namensgeber stimmen in beiden überein; 22 P1343-Belege, einer davon mit zwei dúchas.ie-URLs.
- Labels für P2175/P138/P3342 in `manual/labels.yaml` (von Florian geliefert).
- Test-Schrift (Latin-Subset) hat keine Pfeilglyphen — in Grafiken keine ⇄/←/→ als Text verwenden.

### S5 — Case Study Ogham

**Ziel:** Grafiken A, B, C nach dem Case-Study-Raster (A4) für CIIC 81 (Fundort Garranes ≠ Standort UCC Cork, 20,5 km) und CIIC 178 Coumeenoole North / Dunmore Head (Q126503090; Fundort = Standort, 1839 wieder aufgerichtet).

**Abnahme:** wie S2; zusätzlich alle Werte aus Dateien in `data/raw/` statt fest im Code.

#### Erledigt 2026-09-28

- `py/step_05_ogham.py` baut drei Grafiken nach DE und EN: `rollen`, `ortskette`, `graph-dahinter`.
- Gemeinsame Bausteine liegen jetzt in den Utils (`status_icon`, `hub_bar`, `case_node`, `gnd_slot`, `status_legend`) und gelten ab hier für alle Case Studies; OSM hat eine eigene Farbe (`vu.OSM`), 00a–03 bleiben unverändert.
- Alle Werte aus Dateien: Wikidata-JSONs, fuzzy-sl Q74/Q131, vier neue OSM-XML, die beiden EpiDoc-Editionen und `manual/ogham.yaml` (Antworten aus dem Fragebogen).
- Die aktuelle Lesung und die unsicher gelesenen Buchstaben (rot) werden aus dem EpiDoc gelesen (kombinierender Punkt unter dem Buchstaben), nicht abgetippt.
- Fundort von CIIC 81 in der Kette ist das Ringfort Lisheenagreine (Q141591358, GND 1248049489); die Ogham Site Q69385525 steht als räumlich verbundener Knoten daneben, in Wikidata sind beide nicht verknüpft.
- Karten in Grafik B: Natural Earth 1:10m löst Dunmore Head in keiner Zoomstufe auf. Deshalb kommen die Flächen aus OSM (`osm/boundaries.geojson`, Overpass): Baronie als Landfläche, Townland darin, dazu ein Irland-Inset mit markiertem Kartenfenster. Gezeichnete OSM-Geometrie heißt Namensnennung: „© OpenStreetMap-Mitwirkende, ODbL“ steht unter jeder Karte.
- Befund für Grafik B: Die Ogham Site Q85395557 trägt fünf Koordinaten mit je eigener Quelle (OSM, CISP, Ogham in 3D, SMR, townlands.ie), Spannweite 586 m. Die Quelle jedes Punktes wird aus den Referenzen der Aussage gelesen.
- Dunmore Head ist Q26716192; das in P276 von Q126503090 verwendete Q26716194 ist falsch (Auskunft Florian, Fragebogen B2).
- `tmp/s5-ogham/` ist damit erledigt und wird beim Anwenden des Patches gelöscht.

#### Mockups 2026-09-22

- Arbeitsstand in `tmp/s5-ogham/` (siehe `tmp/README.md`): Fragebogen, Mockup-Skript, gerenderte Mockups, Rohdaten (EpiDoc, Q126503090, fuzzy-sl Q131).
- Quellen neu: OG(H)AM-EpiDoc (`lguariento/og-h-am`, I-COR-030 = CIIC 81, I-KER-046 = CIIC 178), `LinkedOpenOgham/tei--epidoc-crosswalk` (Tabellen `docs/*.csv`), ogham-lod v1 (Abstract-Zip).
- Befunde: EpiDoc nennt für Garranes das Ringfort *Lisheenagreine* (SMR CO084-090001-) — genau der GND-Satz 1248049489 „Ringwallanlage“ → GND „eine Ebene höher“, nicht daneben. Coumeenoole hat zwei Logainm-Anker (22572 Townland, 1394328 An Dún Mór). SMR CIIC 81: EpiDoc CO084-090003- (Fundort) vs. Wikidata/OSM CO074-148---- (Standort?). Sprach-Tags der Inschrift uneinheitlich: EpiDoc `pgl`, OSM `pgl-Latn`, Wikidata `ga` (CIIC 81) bzw. `la` (CIIC 178). Q126503090 ohne P189 und ohne P2888. Site-Punkt vs. Stein: 1,03 km (CIIC 178), EpiDoc-Fundort vs. WD-Site 267 m (CIIC 81).
- Kette DOVINIA → Corcu Duibne → Baronie Corkaguiny (Corca Dhuibhne) belegt über McManus 1991, 111 (zitiert im EpiDoc); auf CIIC 178 sind MU und N unsicher gelesen → rot. CIIC 81: CALLITI → Cailtrige → Eoghanachta, ohne Gebiet → Kette bleibt offen.
- Nächster Schritt: Fragebogen auswerten, Bilder (je eins pro Stein mit Lizenz) einbinden, Werte nach `data/raw/` (YAML), `py/step_05_ogham.py` mit DE/EN, Mockups in `tmp/` löschen.

### S6 — Case Study Holy Wells

**Ziel:** St. Lachtain's Well, Freshford (Q121840779) gegen St. Fiachra's Well, Sheastown (Q121842432), 17 km auseinander, nach demselben WikiProject-Modell erfasst.

**Abnahme:** wie S2.

#### Erledigt 2026-09-28

- `py/step_06_holy_wells.py` baut `rollen`, `ortskette`, `graph-dahinter` in DE und EN; alle Zahlen in Grafik A werden beim Bauen aus `sparql/holywells-*.json` gezählt.
- Geografischer Kontrast: Lachtain hängt über P10689 an einem OSM-**Way** (Fläche), Fiachra über P11693 an einem **Node** (Punkt). Deshalb fehlt Lachtain in einer Abfrage, die nur P11693 kennt.
- GND: Lachtín mac Tarbín 0 Treffer; Fiacre dagegen GND 131380958 („Fiacrius", gest. 670, Länderbezug XA-IE und XA-FR), in Wikidata bereits als P227 verlinkt — ebenso County Kilkenny mit GND 4110260-5. Erste Case Study mit vorhandener GND-Verknüpfung.
- Befund: Die Civil Parish Freshford liegt in OSM in **zwei** Relationen (5330881, 5331080), beide mit `logainm:ref=1295`; P402 in Wikidata nennt nur die kleinere, der Brunnen liegt in der größeren. Die Karte zeichnet deshalb alle Relationen mit passender Logainm-Nummer.
- Die Diözese Ossory steht in B als Ebene daneben: kirchliche Einteilung, in OSM nicht vorhanden.
- In C ist die Kante „Abt von Freshford" rot vermerkt, weil sie nur in der Wikidata-Beschreibung steht, nicht als Aussage.

### S7 — Case Study geo-lod

**Ziel:** CI-Fundstelle 45 (Franchthi-Höhle, Argolis) gegen SISAL-Standort 104 (Liang Luar, Flores) — dieselbe Fragestellung wie S5/S6, nur ist der Kontrast hier die **Tiefe der Verortung**, nicht die Geometrie.

**Abnahme:** wie S2.

#### Erledigt 2026-09-28

- `py/step_07_geo_lod.py` baut `rollen`, `ortskette`, `graph-dahinter` in DE und EN; alle Kennzahlen in Grafik A werden beim Bauen aus `geolod/ci_findspots.csv` und `geolod/sisal_sites.csv` gezählt, die RDF-Prädikate in Grafik C werden aus den beiden `*_excerpt.ttl` gelesen.
- **Hauptbefund:** Die Franchthi-Höhle **hat** einen GND-Satz — 4228929-4, Entitätentyp `gin`, Systematik 19.1b Physische Geografie *und* 16.3 Archäologie, seit 2021 unverändert, ohne Koordinate. Q1441331 trägt aber kein P227. Der Satz existiert und ist aus Wikidata nicht erreichbar; das ist die kleinere und leichter zu schließende der beiden Lücken. Eignet sich als Live-Demo im Vortrag.
- Liang Luar: 0 GND-Treffer, kein QID, kein OSM-Objekt — verankert erst über Kabupaten Manggarai (Q14143, rel 11228382) und die Insel Flores (Q148440, GND 4098001-7, rel 7219477), darüber Ost-Nusa-Tenggara (Q5061, GND 5059700-0).
- Ebene daneben (Gegenstück zur Diözese in S6): in Griechenland die **historische Landschaft Argolis** (Q12649101) — Wikidata trennt sie vom Regionalbezirk, die GND hält beides in einem Satz (4002893-8, `gik` *und* `gin`). In Indonesien die **Kleinen Sundainseln** (Q3803, GND 4290172-8) — GND-Satz vorhanden, OSM ohne Relation, Wikidata ohne P402.
- **Befund zu den Identifikatoren:** Zwei Fehler im CI-Datensatz sind nur auffindbar, *weil* dort IDs stehen. Fundstelle 22 (Phlegräische Felder) verlinkt OSM-Node 10879170567 — das ist „Crvena stijena" in Montenegro (`wikidata=Q121418883`); die Methodenangabe derselben Zeile nennt den richtigen Node 4948370721, und die Koordinate der Zeile trifft ihn auch. Fundstelle 48 heißt „Susak Island (Greece)", ihre beiden Identifikatoren und ihre Koordinate liegen aber in Kroatien. Das trägt Grafik A als eigenes Band — Selbstkritik am eigenen Datensatz, nicht an der GND.
- **Offen / an Flo:** `arch_note` zu Liang Luar sagt „Type site for Homo floresiensis". Typuslokalität ist nach Literaturlage Liang Bua, eine andere Höhle im selben Kabupaten. Die Grafik behauptet dazu nichts, sondern markiert die Kante rot und sagt, dass die Aussage ohne QID von außen nicht prüfbar ist.
- **Offen / an Flo:** `sisal_sites.ttl` und `sisal_sites.csv` widersprechen sich bei den Probenzahlen (Liang Luar 4625 gegen 2715 δ¹⁸O, Chauvet 210 gegen 187). Die Grafik schreibt deshalb „über 2 700", was unter beiden Lesarten stimmt.
- OSM-Flächen kommen aus drei `is_in`-Overpass-Abfragen; die Ringe sind mit Douglas-Peucker ausgedünnt (0,0004° bzw. 0,0012°) und auf 5 Nachkommastellen gerundet, damit die GeoJSONs im Repo klein bleiben.

### S8 — Case Study bb-5kbc

**Ziel:** Seelow 20 (Brandenburg) gegen Jordansmühl / Jordanów Śląski (Niederschlesien) — dieselbe Kultur (Stichbandkeramik), 254 km auseinander, und zwei völlig verschiedene Verortungswege.

**Abnahme:** wie S2.

#### Erledigt 2026-09-29

- `py/step_08_bb5kbc.py` baut `rollen`, `ortskette`, `graph-dahinter` in DE und EN; die Abdeckungszahlen in Grafik A werden beim Bauen aus `bb5kbc/fst_wgs84.csv` über **verschiedene Orte** (nicht über Fundstellen) gezählt.
- **Hauptbefund:** Die GND hat keinen Satz zu Jordanów Śląski und keinen zu Jordansmühl — aber sie hat die **Jordansmühler Kultur** (GND 1231725982, saz, v4300–v3900, Synonym Jordanów-Kultur), deren Definition lautet: „… Begriff 1906 von Hans Seger nach dem niederschlesischen Fundort Jordansmühl eingeführt". Der Ortsname überlebt in der GND also nur im Definitionstext eines Sachbegriffs — als Fließtext, nicht als Verknüpfung, und ohne dass es den Ort selbst gäbe. Das ist der Schluss von Grafik C.
- **Zweiter Befund, und der freundlichste des ganzen Vortrags:** Die GND kann etwas, das weder OSM noch Wikidata systematisch können — **Orte datieren**. 4336493-7 (Märkisch-Oderland) beginnt 1992 und nennt Bad Freienwalde, Seelow und Strausberg als Vorgänger; Niederschlesien gibt es zweimal, als preußische Provinz 4042237-9 (1919–1938, 1941–1945) und als heutige Woiwodschaft 4596748-9. Eine Suche nach „Seelow" liefert denselben Namen als gik, giv, giz, gin und gir. Diese historischen Einheiten stehen in Grafik B als Ebene daneben — das Gegenstück zur Diözese (S6) und zur historischen Argolis (S7), diesmal zeitlich statt räumlich.
- **Dritter Befund:** Der GND-Satz zu Seelow trägt eine Koordinate, **Quelle GeoNames**. Der Datenfluss von den Community-Hubs in die GND existiert also bereits; der Vortrag schlägt nichts Neues vor, sondern beschreibt, was schon passiert.
- Abdeckung über verschiedene Orte: Gemeindeebene DE 239 Orte / TGN 42 / iDAI 2 / OSM 108; PL 74 Orte / TGN 0 / iDAI 0 / OSM 64. Kreisebene DE 37/13/1/17, PL 45/0/0/38. Getty TGN und iDAI.gazetteer enden an der Grenze, OSM trägt beide Seiten und auf der polnischen anteilig besser.
- Kartenbefund in Grafik B: Jordansmühl und Dankwitz/Dankowice liegen auf **derselben Koordinate**, Gleinitz/Glinica 2 km daneben — alle drei „Mittelpunkt der Gemeinde". Drei Fundstellen, ein Punkt; die Umkehrung von Grafik 01.
- Grafik C reicht auf deutscher Seite **unter** die Fundstelle: zwei Scherben mit eigenen Wikidata-Items (Q139477253, Q139477652, mit Foto und P2596 Kultur) und darüber die Denkmalnummer „Bodendenkmal Seelow 2" samt Aktivitätsnummer GV 2001:186/9g — eine eindeutige Ortskennung, die nur innerhalb des Landesdenkmalamts gilt.
- **Offen / an Flo:** Das CSV zitiert „Völker 2002", das Wikidata-Item Q139304626 nennt 2003 als Erscheinungsjahr. Die Grafik schreibt „Völker 2003" nach dem Item.
- **Offen / an Flo:** Q2191877 (Gmina Jordanów Śląski) trägt **zwei** P625-Koordinaten. In Grafik A als „im Datensatz vermerkt" markiert, nicht bewertet.
- **Hinweis, kein Folieninhalt:** Bolko von Richthofen, Autor der Karte von 1930, war ein Vertreter der völkisch-nationalistischen Vorgeschichtsforschung der Zwischenkriegszeit und in den deutsch-polnischen Grenzdebatten aktiv. Die Grafiken nennen nur Autor, Titel und Jahr; falls im Publikum jemand nachfragt, ist der Kontext hiermit notiert.
- OSM-Flächen aus drei `is_in`-Overpass-Abfragen, Ringe mit Douglas-Peucker ausgedünnt (0,0004° für Kreis- und Gemeindeebene, 0,002° für die beiden Locator-Umrisse) und auf 5 Nachkommastellen gerundet.

### S9 — Case Study poseidon2lod

**Ziel:** AITI_119 aus dem Lechtal gegen RKC001 aus Rákóczifalva – Bagi-földek. Der Kontrast ist die **Art des Ortsnamens**, nicht die Datenqualität: moderne Adresse gegen Flurname. Jeder Hub gewinnt auf einer Seite.

**Abnahme:** wie S2.

#### Erledigt 2026-09-29

- `py/step_09_poseidon.py` baut `rollen`, `ortskette`, `graph-dahinter` in DE und EN. Die Korpuszahlen stehen in `poseidon/spatial-coverage.csv`, weil weder das Community Archive (213 Pakete) noch `poseidon_LOD.ttl` (149 MB, Git LFS) ins Repo passen; der Kopf der Datei hält fest, wie gezählt wurde.
- **Der Chiasmus, empirisch belegt:** OSM führt `way/376729440` mit `landuse=commercial` und dem Namen **„Gewerbegebiet Kleinaitingen"** sowie den **Unteren Talweg** als benannte Straße — an ihr hängen fünf Ortsangaben desselben Pakets mit Hausnummern. Eine Abfrage nach **„Bagi-földek"** im 3-km-Umkreis liefert dagegen **null Objekte**. Umgekehrt hat die **GND 35 Geografika zur Theiß** (gik 15, gin 7, giz 7, giv 1, giw 1), darunter Theiß-Gebiet, Obere Theiß, Theißwinkel und die ungarischen Formen **Tiszamente** und **Tiszántúl** — genau die Art von Landschaft, die „MiddleTisza" meint, und OSM hat für keine davon eine Grenze. „Bagi-földek": 0 GND-Treffer.
- **Zeitmodellierung, zum zweiten Mal:** Sieben Fundstellen des Lech-Pakets liegen in **Haunstetten**. Die GND führt es zweimal — 2012911-7 bis 30.06.1972 als eigene Gemeinde, danach 4096014-6 als Augsburg-Haunstetten mit Überordnung Augsburg. GeoNames hat für beide dieselbe ID 2909053. Das steht in Grafik B als Ebene daneben, wie der Landkreis Seelow in S8.
- **Was das nachträgliche Verknüpfen leistet** (aus `poseidon_LOD.ttl` gezählt): `arno:DiscoverySite` 0 von 3292 verknüpft, `arno:Site` 355 von 955, `arno:Place` 984 von 2968, `arno:Country` 146 von 147 — und das einzige Land ohne Treffer heißt **„BotswanaOrNamibia"**. Beide Beispiele enden auf Länderebene, aber aus verschiedenen Gründen: links fehlt die Site-Spalte im Paket ganz (im RDF ein Blank Node „Unknown Site"), rechts ist der Site-Knoten da und nicht auflösbar.
- Grafik C: links steckt die Verwandtschaft als Zeichenkette im `Group_Name` (`…brother.AITI_119.brother.AITI_86.son.AITI_87`) — maschinenlesbar, aber als String, nicht als Aussage. Rechts führt die Kette über die Flur zur Gemeinde und daneben zur Theiß-Familie der GND.
- **Befund fürs Repo, nicht für die Folie:** Die Länder-QIDs in `poseidon_LOD.ttl` sind überwiegend nicht die Standard-Items — Germany Q41304 statt Q183, Hungary Q16410 statt Q28, Poland Q171348 statt Q36, Greece Q11772 statt Q41, USA Q229623 statt Q30 und weitere; richtig sind China Q148, Mongolei Q711, Tschechien Q213. Ursache ist vermutlich die Annahme in `queryWikidata.py`, es könne keine zwei Länder mit demselben Label geben — das stimmt für gegenwärtige Staaten, nicht für Wikidata mit seinen historischen Vorgängern. Ein zusätzlicher Filter auf `P31 wd:Q6256` sollte es beheben.
- **Offen / an Flo:** `owl:sameAs` kommt in den 149 MB genau zweimal vor; die Modellierung setzt konsequent auf `arno:closeMatch`. Das ist als bewusste Entscheidung im README begründet und in Grafik A entsprechend neutral dargestellt.
- Karten diesmal kleinräumig (3 × 2,5 km bzw. Gemeindeausschnitt), weil die Fallstudie von der Art des Namens handelt und die nur im Nahbereich sichtbar ist. Locator sind Landkreis Augsburg und Kreis Szolnok. Die Bundesland-Ebene war über `is_in` nicht zu bekommen (Overpass-Timeout) und wird nicht gebraucht.

### S10 — Abschluss

**Ziel:** Drei Grafiken, die die fünf Fallstudien zusammenfassen, ohne sie zu wiederholen — bewusst textarm, weil die Fallstudien selbst schon dicht sind.

**Abnahme:** wie S2.

#### Erledigt 2026-09-29

- `py/step_10_abschluss.py` baut `arbeitsteilung`, `fehlende-kante` und `tiefe` in DE und EN. Alle Werte stehen in `manual/abschluss.yaml`; jede Zeile nennt im Feld `source` die Fallstudie, die sie belegt. Es kommen keine neuen Daten dazu.
- **Arbeitsteilung:** zwölf Fähigkeiten gegen vier Spalten, nur Punkte statt Text. Die GND gewinnt Zeit am Ort, Namensvarianten, Landschaft und Begriffe; OSM Fläche, alles unterhalb der Verwaltung, gleiche Tiefe über Grenzen und Aktualität; Wikidata die Kante, den Beleg am Einzelfakt und alles, was kein Ort ist; die Fachdaten die Fachtiefe. Darunter eine Zeile je Spalte, wo es aufhört — das nimmt der Grafik die Spitze.
- **Fehlende Kante:** fünf Lücken, vier davon eine Aussage weit (P227 bei Franchthi, der OSM-Tag bei CIIC 81, P402 bei Freshford, das Mapping von „MiddleTisza"), eine braucht wirklich einen Normdatensatz (Jordanów Śląski). Schlusssatz: der Fluss läuft schon in beide Richtungen, die Koordinate im GND-Satz zu Seelow stammt aus GeoNames.
- **Tiefe der Verortung:** fünf Stufen von Land bis Einzelobjekt, zehn Beispiele, je vier Balken. Abgelesen aus den Ortsketten der Fallstudien. Befund: die Fachdaten reichen fast immer am tiefsten, weil sie die Fundstelle *sind*; die GND ist nicht flach, sondern **ungleichmäßig** — einmal bis zum Denkmal (Ringfort Garranes), einmal bis zur Höhle selbst (Franchthi), dreimal nur bis zum Land.
- **Offen / an Flo:** Die Tiefenwerte in `abschluss.yaml` sind aus den Grafiken B der Fallstudien abgelesen und dort doppelt gehalten. Wenn sich an einer Ortskette etwas ändert, muss die Tabelle nachgezogen werden; das Feld `source` sagt jeweils wo.

### S11 — Vereinheitlichung der fünf Fallstudien

**Erledigt 2026-09-29.** Kein neuer Inhalt, nur ein gemeinsames Raster:

- Der bis dahin fünfmal kopierte Code steht jetzt in `py/hdoku26_visuals_utils.py` unter „Case-study layout contract“: `case_header`, `case_cell`, `case_row`, `case_map`, `case_locator`, `case_fan`, `geo_*`, `hub_legend`, `gnd_slot_legend`, `chain_xs` sowie `load_wikidata`, `load_geojson` und `chain_node`. Die Zahlen des Rasters (`CASE_C1`, `CASE_C2`, `CASE_CW`, `CASE_ROW_TOP`, `CASE_ROW_TOP_IMG`, `CASE_RULE_Y`, `CASE_LEGEND_Y`) sind der Vertrag; die Schritte 05–09 rechnen nicht mehr selbst.
- Die Infoboxen am Fuß von A und die Schluss-Chips in C sind entfernt.
- Ketten in B und C laufen mit `chain_xs(...)` bis an die Inhaltskante, statt rechts Platz zu lassen.
- Grafik 07 A hat jetzt Fotos: Franchthi-Höhle innen (Efi tsif) über den Funden (Zde), beide CC BY-SA 4.0 via Wikimedia Commons; Liang Luar mit Team (Garry K Smith, CC0). Zuschnitte und Nachweise in `manual/geolod.yaml`.
- `img/00`–`img/03` und `img/10` bleiben byteweise unverändert; 05–09 sind neu gebaut.
- **Offen / an Flo:** In den EN-Grafiken von S8 stehen einige Feldwerte des Datensatzes unübersetzt (`quelle_georef`, `methode`, `kultur`, `fundstellenart`, `quellen_typ`) — gewollt, weil es Zitate aus den Daten sind; falls das stören soll, geht eine englische Kurzform.

### S12 — Legende, Weißraum, letzte Engstellen

**Erledigt 2026-09-29.** Zweiter Durchgang über dieselben fünfzehn Grafiken:

- **Legende vollständig und mit Luft.** `case_legend` setzt beide Zeilen; vorher hatte Grafik C mancher Fallstudie nur die Hub-Farben. Zeile 1 bei 944, Zeile 2 bei 980 (vorher 24 px Abstand, jetzt 36).
- **`case_split`.** Grafik C jeder Fallstudie sammelt ihre zwei Beispiele in zwei Listen; `case_split` misst beide mit `svg_y_span`, verteilt den Weißraum und setzt die Trennlinie dazwischen. Damit ist der leere Streifen über der Legende weg.
- **Engstellen.** poseidon2lod C: die Homonym-Notiz lag auf der Hub-Leiste der Awaren. bb-5kbc C: „Ortsname Jordansmühl“ war breiter als sein Knoten. Ogham B: der ODbL-Nachweis klebte am Chip der zweiten Karte. bb-5kbc B und poseidon2lod B: die Notiz neben der GND-Nebenebene reichte in die Legende — dort ist jetzt `aside_dy` je Band einstellbar.
- Geprüft: kein Textelement in einer der fünfzehn Grafiken kommt der Legende näher als 10 px; `img/00`–`img/03` und `img/10` bleiben unverändert.
- **Nachtrag S12b:** Zwei Grafiken nutzten die Breite noch nicht: geo-lod C rechnete mit fünf Spalten, zeichnete aber nur vier (die Kette endete bei 1396 statt 1690), und Ogham C lief mit dem letzten Knoten bei 1748 über die Marge hinaus. Beide rechnen jetzt mit der Breite des letzten Knotens. Automatisch nachgemessen: alle zwanzig B- und C-Grafiken enden bei 1690.

### S7–S9 — weitere Case Studies

**Ziel:** Grafiken nach dem Case-Study-Raster (A4), Umfang je nach Beispiel (A + B, C wo der Graph dahinter zum Ort zurückführt): Holy Wells (u. a. St. Lachtain's Well Q121840779; Heilige statt Inschrift), geo-lod, bb-5kbc, poseidon2lod.

**Beispielpaare (Vorschlag vom 2026-09-28, vor dem Zeichnen jeweils an den Daten prüfen):**

| Schritt | Beispiel 1 | Beispiel 2 | Kontrast | OSM-Flächen für die Karte |
|---|---|---|---|---|
| S6 Holy Wells | St. Lachtain's Well (Q121840779): Wikidata, OSM-Way, SMR, dúchas, Namenspatron | ein Brunnen, den praktisch nur OSM und dúchas kennen | Wer hält den Ort überhaupt? | Brunnen, Townland, Civil Parish |
| S7 geo-lod | CI-Fundstelle 45 Franchthi-Höhle (Q1441331, OSM-Node 1221172611, `fsl:high`) | SISAL-Standort 104 Liang Luar (kein QID, kein OSM-Objekt) | wie tief reicht die Verortung — bis auf die Höhle oder erst bis zur Insel | Gemeinde Ermionida in Argolis; Kabupaten Manggarai auf Flores |
| S8 bb-5kbc | Seelow 20 (Katalognr. 55005), SBK-Siedlung, aus den BLDAM-Denkmaldaten, ±0 m | Jordansmühl / Jordanów Śląski (Katalognr. 7), SBK, „Mittelpunkt der Gemeinde“ aus einer Karte von 1930, ±3000 m | GND-Satz und Gemeinde auf der einen, anderes nationales Register auf der anderen Seite — Internationalität wird gezeigt, nicht behauptet | Gemeinde bzw. Gmina, Staatsgrenze |
| S9 poseidon2lod | AITI_119, Lechtal: der Fundort heißt nach einem Gewerbegebiet | RKC001, Rákóczifalva – Bagi-földek: der Fundort heißt nach einer Flur | welche **Art** von Ortsname den Fundort benennt — und welcher Hub ihn führt | Gemeinde, Gewerbegebiet, Straße; Gemeinde, Kreis |

Grafik C ist bei S6 gesetzt (Heiliger, Patrozinium, Kirche — bei Personen ist die GND dicht, die Kette trifft sie also von der anderen Seite) und bei S8 wahrscheinlich; bei S7 und S9 erst nach einem Blick in die Daten entscheiden.

**Quellen:**
- S7 geo-lod: https://github.com/Research-Squirrel-Engineers/GeoScience-FAIRification-LOD
- S8 bb-5kbc: https://github.com/Research-Squirrel-Engineers/bb-5kbc-sites
- S9 poseidon2lod: https://github.com/archaeonatural-cloud/poseidon2lod mit Ontologie https://github.com/archaeonatural-cloud/archaeonatural-ontology

Die GitHub-Repos erzeugen die LOD/RDF-Daten und lassen sich im Sandbox direkt klonen.

**Abnahme:** wie S2.

---

## Teil D — Offene Punkte

- Zitatauswahl für Grafik 2 und 3 (Kandidaten in `quotes.yaml`).
- Fonts: im Sandbox aus `@fontsource/fira-sans` (Latin-Subset) konvertiert; im Repo die Originaldateien aus bb-5kbc-visuals verwenden.
- Offen aus S5: MAQI-ERCIAS hat kein Wikidata-Item; Cailtrige, Eoghanachta und Corcu Duibne haben weder QID noch GND-Satz; der OSM-Tag `wikidata=Q106680733` am CIIC 81 sollte auf Q130529871 zeigen, der Tag am CIIC 178 (`Q70892682`) auf Q126503090; P276 von Q126503090 zeigt auf das falsche Dunmore-Head-Item.
- Soll Lisnacaheragh in Wikidata angelegt werden (mit P227 = 1248049489)? Wäre eine Aussage für Grafik 3.
