# Ogham-Fallstudie – Fragen und Befunde

Zwei Steine, ein Muster: **CIIC 81 (Garranes → UCC Cork)** und **CIIC 178 (Coumeenoole North / Dunmore Head)**.

Antworten bitte direkt unter die Fragen schreiben: `→ …`, gern auch nur eine QID. Was du nicht weißt oder nicht willst, einfach leer lassen oder `skip` schreiben.

**Stand der Quellen (22.09.2026)**

- OG(H)AM-EpiDoc aus [`lguariento/og-h-am`](https://github.com/lguariento/og-h-am), Commit `0a2c7a0` vom 20.09.2026. Die beiden Dateien sind `XML/I-COR/I-COR-030.xml` (CIIC 81) und `XML/I-KER/I-KER-046.xml` (CIIC 178).
- [`LinkedOpenOgham/tei--epidoc-crosswalk`](https://github.com/LinkedOpenOgham/tei--epidoc-crosswalk), die generierten Tabellen `docs/*.csv` und `out/places.csv`.
- ogham-lod v1 (2021) aus dem Abstract-Zip.
- Wikidata-JSON zu Q126503090 und Q130529871, fuzzy-sl Q131, OSM-Node 11071361392.

---

## 0. Was sich durch das EpiDoc schon erledigt hat

| | CIIC 81 · I-COR-030 | CIIC 178 · I-KER-046 |
|---|---|---|
| Titel (ga \| en) | An Garrán \| Garranes | Com Dhíneol Thuaidh \| Coumeenoole North |
| CISP | GARES/1 | COUME/1 |
| Trismegistos | – | TM 172528 *(URL im `corresp` doppelt, s. u.)* |
| SMR des Steins | CO084-090003- | KE052-059002- |
| weitere SMR am Fundort | Ringfort *Lisheenagreine* CO084-090001-, Souterrain CO084-090002- | – |
| Logainm | 8299 (Garranes) | **22572** (Coumeenoole North) + **1394328** (An Dún Mór) |
| Fundort-Koordinate | 51.816848, −8.765479 (ITM 547221 563003) | 52.110277, −10.473175 (ITM 430623 598263) |
| Fund | 1852, Bauer bei der Kartoffelernte im Ringfort; vermutlich aus dem Souterrain | 1838 liegend auf dem Gipfel von Dunmore Head (Windele, Abell, Horgan); 1839 von Rev. J. Casey wieder aufgerichtet |
| heute | UCC Stone Corridor, Inv.-Nr. 4 (keeper Q1574185); **20,5 km** vom Fundort | „at or close to find site on Dún Mór promontory fort" |
| Material, Form, Maße | Sandstein, Pfeiler, 1,75 × 0,50 × 0,20 m | Grit, Pfeiler, 2,00 × 0,45 × 0,30 m (Cuppage 1986) |
| Transliteration | `C[A]SSITT[A]S MAQI MU[CO]I CALLITI` | `ERC MAQI MAQI-ERCIAṢ ṂỤ DOVIṆIẠ` |
| Tiefe der Auszeichnung | voll: `<persName>`, `<name nymRef>`, `<w lemma="maqqas\|muccoviias">`, Ogham-Unicode | nur Transliteration mit Unterpunkten; die Ogham-Division ist leer |
| Übersetzung | – (auskommentiert) | „of Erc son of Mac-Erce descendant? of Duibne" |
| Personen-Relation | CASSITTAS –maqqas + muccoviias→ CALLITI (Sippe) | nicht in `persons.csv`, weil kein `<persName>` |
| Wörter mit WD-QID | MAQI Q67381254 · MUCOI Q67999759 | MAQI Q67381254 · ERC Q67382360 · DOV (ohne QID) |
| Medien | Foto Nora White · Zeichnung Macalister 1945, 83 · Sketchfab von *b-unicycling* | Zeichnung Macalister 1945 (Platzhalter `example.jpg`) |
| Editor:innen | Nora White (ORCID 0000-0001-7957-651X), POC, THN | Nora White, Truc Ha Nguyen; EpiDoc-Batch von Jef Bucas (DIAS) |
| Lizenz | CC BY 4.0 | CC BY 4.0 |

Aus ogham-lod v1 (2021) kommen dazu:

- **CIIC 81:** Konzepte Q69385424 (CIIC) und Q106675512 (CISP), Site OS40000120 → Q69385525.
- **CIIC 178:** Konzepte Q70892682 (CIIC), Q106675447 (CISP) und Q106674214 (O3D), Site OS40000083 → **Q85395557**.

---

## A. Stein-Items

**A1.** Auf **Q106680733** zeigen bei CIIC 81 sowohl `wikidata=` am OSM-Node als auch P1382. Was ist das? ogham-lod v1 nennt als Konzepte Q69385424 (CIIC) und Q106675512 (CISP). Ist Q106680733 ein drittes Konzept oder ein neueres Item?
→

**A2.** Wo steht bei Coumeenoole der P2888-Link auf **Y50000178**? Q130529871 hat P2888 → Y50000081, Q126503090 hat keinen. Soll er in der Grafik als „fehlt noch" erscheinen oder ignoriert werden?
→

**A3.** Q126503090 hat **kein P189** (Fundort). Fundort und Standort fallen hier zusammen. Wie soll das modelliert werden?
- (a) P189 → Q85395557, die Ogham Site, dazu P276 → Q26716194
- (b) nur P276, der Fundort ist implizit
- (c) anders
→

**A4.** Fehlt für CIIC 81 die **Trismegistos-ID**, oder gibt es keine? Wikidata hat dafür P1958.
→

**A5.** fuzzy-sl **Q74** (CIIC 81) bitte als JSON, damit beide Steine gleich belegt sind (für Q131 liegt es schon vor).
→

## B. Sites und Townlands

**B1.** Coumeenoole North, Townland: **WD-QID** und **OSM-Relation**. Logainm 22572 steht schon im EpiDoc.
→

**B2.** **An Dún Mór / Dunmore Head** (Logainm 1394328): Ist das **Q26716194** (P276)? Gibt es dafür ein OSM-Objekt, z. B. `natural=cape` oder `historic=archaeological_site` mit `site_type=fortification`?
→

**B3.** Die **SMR des Promontory Fort** Dún Mór. Vermutlich KE052-059001-, das ist aber nur geraten.
→

**B4.** **Q85395557** (Ogham Site Coumeenoole) bitte als JSON: Koordinate, Referenzen, eventuell Logainm.
→

**B5.** Soll die Ringfort-Ebene bei Garranes rein, also Ringfort *Lisheenagreine* (SMR CO084-090001-) mit Souterrain (CO084-090002-)? Siehe Idee **I2**: Der GND-Satz 1248049489 „Garranes, Ringwallanlage" meint genau dieses Ringfort. Falls ja: Gibt es ein WD-Item oder ein OSM-Objekt für das Ringfort?
→

**B6.** **Baronien:** Kinalmeaky (Garranes) und Corkaguiny (Coumeenoole). QID und OSM-Relation, falls sie gebraucht werden (siehe **I3**).
→

## C. OpenStreetMap

**C1.** OSM-XML von **Node 5145413640** (Coumeenoole). Die Fragen dazu:
- Gibt es `inscription` bzw. `inscription:pgl-Latn`?
- Worauf zeigt `wikidata=`, auf den Stein oder auf ein Konzept?
- Gibt es `ref:IE:smr`?
→

**C2.** Bei CIIC 81 steht in `ref:IE:smr` am OSM-Node und in P4057 übereinstimmend **CO074-148----**. Das EpiDoc führt als SMR des Steins **CO084-090003-**. Lese ich das richtig: CO074-148 ist der Standort-Datensatz in Cork (UCC) und CO084-090003 der Fundort-Datensatz?
→

**C3.** Sind `url:sketchfab=https://skfb.ly/oVOIH` am OSM-Node und das Sketchfab-Modell im EpiDoc (*b-unicycling*) dasselbe Modell?
→

## D. Knowledge Graph hinter der Inschrift

**D1.** Die **Y5-Einträge** von lod.ogham.link, **Y50000081** und **Y50000178**: Turtle oder Link zum aktuellen Stand. Das Zip enthält nur die Serien Y1, Y2 und Y3 von 2021. Der Ordner `rdf/crosstable/` (Stein ↔ Lesung ↔ Wort ↔ Person) ist leer.
→

**D2.** **WD-QIDs der Personennamen**. Sie wurden als Q110897921 mit P2888 → OP… angelegt, die QIDs stehen aber nicht in `wd_persons.qs`.

| Name | ogham-lod | QID |
|---|---|---|
| CASSITTAS | OP400067 | → |
| CALLITI | OP400061 | → |
| ERC | OP400203 | → |
| MAQI-ERCIAS | OP400321 | → |
| DOVINIA | OP400175 | → |

**D3.** **Sippen und Tribus** (für die Brücke Person → Ort, siehe **I3**):
- MUCOI CALLITI → *Cailtrige* bzw. *Ceinéal Caollaidhe*, Teil der *Eoghanachta* (O'Brien 2021 nach Bhreathnach 2013). Gibt es dafür QIDs?
→
- DOVINIA(S) → *Corcu Duibne* und damit die Baronie Corkaguiny (McManus 1991, 111). Gibt es QIDs?
→

**D4.** Welche **Lesung** soll auf die Folie?
- (a) die OG(H)AM-Edition (Nora White), wie sie im EpiDoc steht
- (b) die Lesung aus Wikidata P1684
- (c) alle Lesungen nebeneinander (EpiDoc · WD · OSM · Macalister · Gippert), um die Varianz zu zeigen

Meine Empfehlung: (c) für CIIC 81, das einen echten Lesungsstreit hat, und (a) mit Unterpunkten für Coumeenoole.
→

**D5.** **Sprach-Tags** (siehe **I1**). Soll die Grafik das kommentieren, und wenn ja, wie? Ohne Wertung oder mit der Empfehlung `pgl`?
→

## E. Bilder (optional)

**E1.** Welches Foto pro Stein, mit welcher Lizenz?
- CIIC 81: dein eigenes Foto (CC BY-NC-SA 4.0), das OG(H)AM-Foto von Nora White oder ein Sketchfab-Screenshot.
- CIIC 178: eines der sechs Commons-Bilder (Kategorie „Coumeenoole Stone"). Welches, und wer ist Urheber:in?
→

**E2.** Sollen die Macalister-Zeichnungen (1945) rein? Rechtlich vermutlich frei, das wäre zu prüfen.
→

## F. GND (optional, für die Symmetrie zu Folie 14)

**F1.** GND-Explorer-Treffer für „Dunmore Head", „Dún Mór", „Coumeenoole" bzw. „Coumeenole", „Corkaguiny" und „Corcu Duibne". Ein Screenshot genügt, 0 Treffer ist auch ein Ergebnis.
→

## G. Nachtrag nach den Mockups

**G1.** Welche GND-IDs gibt es? Ein Screenshot oder die ID genügt, 0 Treffer ist auch ein Ergebnis.
Das brauche ich für die Zeile „gelesen von“ in Grafik C und für die GND-Zeile in B.

| Eintrag | GND-ID |
|---|---|
| R. A. S. Macalister | → |
| Damian McManus | → |
| Jost Gippert | → |
| Judith Cuppage | → |
| O'Brien (2021) | → |
| Eoghanachta / Eóganacht | → |
| Corcu Duibne / Corca Dhuibhne | → |
| County Cork | → |
| County Kerry | → |
| University College Cork | → |
| Sachbegriff „Ogham“ (Schrift / Inschrift) | → |

**G2.** Was bedeuten die Qualifier-Werte in fuzzy-sl Q131?
Ich habe sie nach dem Muster von Q74 gelesen, das ist aber geraten.

| Qualifier-Wert | meine Lesart | stimmt? |
|---|---|---|
| Q23 | Sicherheit *High* | → |
| Q24 | Sicherheit *Low* | → |
| Q77 | Ort-Typ *Exhibition Site* | → |
| Q17 | Ort-Typ *Findspot* | → |

Für die Karten in Grafik B bräuchte ich außerdem eine Zeile, wofür P5, P6, P7, P14, P16, P24 und P33 stehen.
→

**G3.** Welche Knoten sollen in Grafik B und C „GND denkbar“ (gestrichelt ocker) bekommen?
Im Mockup sind es: Stein, Townland, Baronie, Dún Mór, Corcu Duibne und Cailtrige.
Wenn es diplomatischer sein soll, reichen zwei bis drei davon. Welche?
→

**G4.** Gibt es für Corkaguiny = Corca Dhuibhne, benannt nach dem Stamm, eine zweite Quelle neben McManus 1991, 111?
Zum Beispiel Logainm (Baronie), eine Wikidata-Referenz oder einen Eintrag bei Ó Muraíle.
→

---

## Ideen aus dem EpiDoc

**I1. Eine Inschrift, vier Sprach-Tags.** Dieselbe Inschrift ist unterschiedlich getaggt:

| Quelle | Sprach-Tag |
|---|---|
| EpiDoc | `pgl` (Primitive Irish, `textLang mainLang="pgl-Ogam"`) |
| OSM | `inscription:pgl-Latn` |
| Wikidata, CIIC 81 | `ga` |
| Wikidata, Coumeenoole | `la` |

Wenn die Hubs dieselbe Sprache unterschiedlich benennen, ist das ein Crosswalk-Thema im Kleinen. Freundlich formuliert zeigt es: Der Standard (BCP 47 bzw. ISO 639-3 `pgl`) existiert schon, er muss nur ankommen.

**I2. Die GND liegt eine Ebene höher, nicht daneben.** Das EpiDoc nennt drei SMR-Datensätze in Garranes:

| SMR | Objekt |
|---|---|
| CO084-090001- | Ringfort *Lisheenagreine* |
| CO084-090002- | Souterrain |
| CO084-090003- | Stein |

Der GND-Satz 1248049489 „Garranes, Ringwallanlage" ist **genau dieses Ringfort**. Diplomatisch gewendet: Die GND hat den richtigen Ort, nur ohne Geometrie und ohne Brücke. Ein `P4057` bzw. `skos:closeMatch` auf CO084-090001- würde sie andocken. Das passt als versöhnlicher Schluss zu Folie 14.

**I3. Personennamen werden Ortsnamen.** Die Kette läuft von der Inschrift bis zur Verwaltungsgrenze:

> DOVINIA(S) → *Corcu Duibne* → Baronie **Corkaguiny**

Fast alle DOVINIAS-Steine liegen auf der Halbinsel Dingle (McManus 1991, 111). Hier geht der Knowledge Graph hinter der Inschrift in Geografie über, und OSM kann die Baronie als Fläche liefern. Bei CIIC 81 wäre das parallel MUCOI CALLITI → *Cailtrige* / *Eoghanachta*. Das ist die interdisziplinäre Pointe schlechthin: Sprachwissenschaft, Genealogie und Geografie in einem Graphen.

**I4. Unsicherheit ist sichtbar – in jeder Quelle anders.**

| Quelle | Wie Unsicherheit notiert wird |
|---|---|
| EpiDoc | `<supplied reason="lost">` bzw. Unterpunkte (ṢṂỤṆẠ) |
| OSM | `[A/O]` |
| Gippert 1987 | `SSI[O]TTAS` |
| fuzzy-sl | Koordinaten mit Sicherheitsgrad |
| WD | Rang (preferred / normal) |

Für die Grafik können unsichere Buchstaben in der UNCERTAIN-Farbe (rot) erscheinen. Das Tag `[A/O]` in OSM bildet damit eine wissenschaftliche Kontroverse ab.

**I5. Der Stein wandert, der Fundort bleibt.** Aus `keepers.csv` stammt der Abstand Garranes → UCC von 20,5 km. Bei Coumeenoole gilt „at or close to find site". Beides passt ins gemeinsame Muster: P189 und P276 mit Distanz.

**I6. Koordinaten stimmen, aber nicht überall.**
- Coumeenoole: EpiDoc gegen WD/fuzzy-sl **2,6 m** (praktisch identisch).
- Coumeenoole: Ogham-Site-Punkt in ogham-lod bzw. WD gegen den Stein **1,03 km**.
- Garranes: EpiDoc-Fundort gegen WD Q69385525 **267 m**.

Das Muster „Stein-Punkt ≠ Site-Punkt" taucht also in beiden Fällen auf.

**I7. Ein weiterer internationaler Hub: Trismegistos (Leuven).** TM 172528 ist ein Beleg für Internationalität über Irland hinaus. Nebenbei: Im EpiDoc ist die TM-URL im `corresp` verdoppelt. Das gehört eher als Hinweis zu Nora als auf die Folie.

**I8. Jede Aussage hat eine Quelle, bis zur Person.** Das EpiDoc bringt ORCID, `resp`, `revisionDesc` und Fundgeschichte mit Zitaten (Brash 1869, Macalister 1945, Cuppage 1986). Das ist die Brücke zu Folie 16 (Nische = Hub) und zu PROV im Crosswalk-Repo.

**I9. EpiDoc als dritte Säule neben WD und OSM.** Möglich wäre ein Dreieck *Edition (EpiDoc/OG(H)AM) – Hub (Wikidata/Wikibase) – Karte (OSM)*, verbunden über den Crosswalk nach CIDOC CRM / CRMtex (tei--epidoc-crosswalk). Crossys bleiben dabei am Rand, wie im Abstract.
