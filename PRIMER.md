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
| Zitate | pro Grafik gemeinsam auswählen; Grafik 1: A1 + A2 (Autorentext S. 119) | Vorschlag |
| Repo-Name | `hdoku26-visuals` | Vorschlag |

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
| S2 | Grafik 1 „Ein Name, viele Orte“ | S1 | Entwurf 2026-09-22, Iteration offen |
| S3 | Grafik 2 „Zukunft: Wikibase-Konvergenz“ | S1 | offen |
| S4 | Grafik 3 „Die Nische ist der Hub“ | S1 | offen |

S3 und S4 sind unabhängig von S2 und voneinander.

---

## Teil C — Die Schritte

### S2 — Grafik 1 „Ein Name, viele Orte“

**Ziel:** Garranes als Homonymie-Fall: Karte mit vier nummerierten Orten, GND-Datensatz-Karte, vier Kandidatenkarten, zwei c't-Zitate (A1, A2).

**Abnahme:** Alle IDs/Zahlen aus `data/raw/`; Abstände gerechnet (36,6 / 87,2 km, 24 m); keine Überlappungen in DE und EN; keine Diagonalen; zweiter Lauf byte-identisch.

### S3 — Grafik 2 „Zukunft“

**Ziel:** links GND (GNDplus Z2/Z3, Geodaten-Modul P3, steuerbare Offenheit Z4), rechts föderiertes Wikibase-Ökosystem am CIIC 81 (Wikidata, FactGrid, Semantic Kompakkt, fuzzy-sl) und Semantic OSM, Mitte DNB-Wikibase seit 2019 + WikiLibrary-Manifest (P4), gemeinsames Ziel (Z6).

**Abnahme:** wie S2.

### S4 — Grafik 3 „Die Nische ist der Hub“

**Ziel:** Mini-Wissensgraph Townland Garranes (Wikidata–Logainm–OSM, GND gestrichelt „Anschluss nach Identitätsklärung“), Holy Well als zweiter Teilgraph, VGI-Band, Crossys/TRAIL 2.5 als Fundament; Z7/Z8 als geteilter Anspruch, Z9 als Schluss.

**Abnahme:** wie S2.

---

## Teil D — Offene Punkte

- Zitatauswahl für Grafik 2 und 3 (Kandidaten in `quotes.yaml`).
- Fonts: im Sandbox aus `@fontsource/fira-sans` (Latin-Subset) konvertiert; im Repo die Originaldateien aus bb-5kbc-visuals verwenden.
- Soll Lisnacaheragh in Wikidata angelegt werden (mit P227 = 1248049489)? Wäre eine Aussage für Grafik 3.
