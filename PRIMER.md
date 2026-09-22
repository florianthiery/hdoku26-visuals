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
| S5 | Case Study Ogham (2 Steine) | S1 | Mockups 2026-09-22 (`tmp/s5-ogham/`), wartet auf Fragebogen |
| S6 | Case Study Holy Wells (2 Brunnen) | S1 | offen |
| S7 | Case Study geo-lod (SISAL-Höhlen, CI-Tephra) | S1 | offen |
| S8 | Case Study bb-5kbc (Brandenburg/Westpolen) | S1 | offen |
| S9 | Case Study poseidon2lod (aDNA) | S1 | offen |

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

#### Mockups 2026-09-22

- Arbeitsstand in `tmp/s5-ogham/` (siehe `tmp/README.md`): Fragebogen, Mockup-Skript, gerenderte Mockups, Rohdaten (EpiDoc, Q126503090, fuzzy-sl Q131).
- Quellen neu: OG(H)AM-EpiDoc (`lguariento/og-h-am`, I-COR-030 = CIIC 81, I-KER-046 = CIIC 178), `LinkedOpenOgham/tei--epidoc-crosswalk` (Tabellen `docs/*.csv`), ogham-lod v1 (Abstract-Zip).
- Befunde: EpiDoc nennt für Garranes das Ringfort *Lisheenagreine* (SMR CO084-090001-) — genau der GND-Satz 1248049489 „Ringwallanlage“ → GND „eine Ebene höher“, nicht daneben. Coumeenoole hat zwei Logainm-Anker (22572 Townland, 1394328 An Dún Mór). SMR CIIC 81: EpiDoc CO084-090003- (Fundort) vs. Wikidata/OSM CO074-148---- (Standort?). Sprach-Tags der Inschrift uneinheitlich: EpiDoc `pgl`, OSM `pgl-Latn`, Wikidata `ga` (CIIC 81) bzw. `la` (CIIC 178). Q126503090 ohne P189 und ohne P2888. Site-Punkt vs. Stein: 1,03 km (CIIC 178), EpiDoc-Fundort vs. WD-Site 267 m (CIIC 81).
- Kette DOVINIA → Corcu Duibne → Baronie Corkaguiny (Corca Dhuibhne) belegt über McManus 1991, 111 (zitiert im EpiDoc); auf CIIC 178 sind MU und N unsicher gelesen → rot. CIIC 81: CALLITI → Cailtrige → Eoghanachta, ohne Gebiet → Kette bleibt offen.
- Nächster Schritt: Fragebogen auswerten, Bilder (je eins pro Stein mit Lizenz) einbinden, Werte nach `data/raw/` (YAML), `py/step_05_ogham.py` mit DE/EN, Mockups in `tmp/` löschen.

### S6–S9 — weitere Case Studies

**Ziel:** Grafiken nach dem Case-Study-Raster (A4), Umfang je nach Beispiel (A + B, C wo der Graph dahinter zum Ort zurückführt): Holy Wells (u. a. St. Lachtain's Well Q121840779; Heilige statt Inschrift), geo-lod, bb-5kbc, poseidon2lod.

**Quellen:**
- S6 Holy Wells: WikiProject auf Wikidata (Doku) und OSM-Objekte; Entity-JSON/OSM-XML der gewählten Brunnen.
- S7 geo-lod: https://github.com/Research-Squirrel-Engineers/GeoScience-FAIRification-LOD
- S8 bb-5kbc: https://github.com/Research-Squirrel-Engineers/bb-5kbc-sites
- S9 poseidon2lod: https://github.com/archaeonatural-cloud/poseidon2lod mit Ontologie https://github.com/archaeonatural-cloud/archaeonatural-ontology

Die GitHub-Repos erzeugen die LOD/RDF-Daten und lassen sich im Sandbox direkt klonen.

**Abnahme:** wie S2.

---

## Teil D — Offene Punkte

- Zitatauswahl für Grafik 2 und 3 (Kandidaten in `quotes.yaml`).
- Fonts: im Sandbox aus `@fontsource/fira-sans` (Latin-Subset) konvertiert; im Repo die Originaldateien aus bb-5kbc-visuals verwenden.
- S5: Fragebogen `tmp/s5-ogham/fragebogen.md` (A–G) beantworten; v. a. Townland Coumeenoole North (QID, OSM-Relation), OSM-Node 5145413640, Q106680733, GND-IDs (G1), fuzzy-sl-Qualifier (G2), Auswahl „GND denkbar“ (G3).
- Soll Lisnacaheragh in Wikidata angelegt werden (mit P227 = 1248049489)? Wäre eine Aussage für Grafik 3.
