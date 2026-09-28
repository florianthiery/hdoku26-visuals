# data/raw — inputs, unchanged, read-only

Everything a figure shows comes from a file in this directory. Nothing here is
written by the pipeline, and no step reaches the network.

| Path | What | Obtained |
|---|---|---|
| `wikidata/Q104295278.json` | Townland of Garranes (An Garrán), Co. Cork: coordinate, Logainm ID 8299, OSM relation 6168494 | `Special:EntityData/Q104295278.json`, 2026-09-22 |
| `wikidata/Q69385525.json` | Garranes (Ogham Site): coordinate, references (CIIC Vol. 1, townlands.ie), FactGrid | `Special:EntityData`, 2026-09-22 |
| `wikidata/Q130529871.json` | Ogham Stone UCC Stone Corridor IV (CIIC 81): two ranked coordinates, OSM node, SMR | `Special:EntityData`, 2026-09-22 |
| `wikidata/Q121840779.json` | St. Lachtain's Well, Freshford, Co. Kilkenny | `Special:EntityData`, 2026-09-22 |
| `osm/way_935503837.xml` | OSM way of St. Lachtain's Well, Freshford (`wikidata`, `name:etymology:wikidata`, `ref:IE:smr`, survey date) | OSM API 0.6, 2026-09-22 (ODbL) |
| `osm/node_11071361392.xml` | OSM node of CIIC 81 at UCC Cork (`moved_from`, `wikidata`, `ref:IE:smr`) | OSM API 0.6, 2026-09-22 (ODbL) |
| `gnd/1248049489.ttl` | GND record "Garranes" (Ringwallanlage), Turtle | GND Explorer download, 2026-09-22 (CC0) |
| `manual/places.yaml` | GeoNames 3299501, Wikidata Q31066388, GND cataloguing source, Cork orientation marker | read from the web pages, 2026-09-22; each entry names its URL |
| `manual/labels.yaml` | Labels of four QIDs referenced in `Q121840779.json` (P2175, P138, P3342) | supplied from wikidata.org, 2026-09-22 |
| `manual/vgi.yaml` | Townland of Garranes in OSM since 2016 (townlands.ie), WikiProject Holy Wells, GND record Freshford (Somerset) | web pages / GND Explorer, 2026-09-22 |
| `manual/federation.yaml` | CIIC 81 in the fuzzy-sl Wikibase (Item:Q74, two coordinates with certainty) and the planned CrossyBase | slide 18 of the DH Ireland-UK 2026 deck; approved abstract |
| `naturalearth/ireland_outline.json` | Island-of-Ireland coastline polygons, 3 decimals | Natural Earth 1:10m admin-0 (public domain) via npm `world-atlas@2.0.2` `countries-10m.json` |
| `screenshots/gnd-explorer-*.png` | GND Explorer graph views of Tim Berners-Lee, Goethe and Konrad Zuse (see `screenshots/README.md`) | taken by Florian Thiery, 2026-09-22 |
| `images/konrad-zuse-hunscher.jpg` | Photo of Konrad Zuse by Wolfgang Hunscher, Dortmund, CC BY-SA 3.0, via Wikimedia Commons | Wikimedia Commons, 2026-09-22 |
| `manual/zuse.yaml` | Zuse example: the two places linked in the GND graph (approximate positions for a schematic map), photo credit, graph crop | GND Explorer screenshot, 2026-09-22 |
| `naturalearth/germany_outline.json` | Outline of Germany, 2 decimals, for the schematic map in 00a | Natural Earth 1:10m via npm `world-atlas@2.0.2` |
| `wikidata/Q126503090.json` | Ogham stone Coumeenoole North / Dunmore Head (CIIC 178) | `Special:EntityData`, 2026-09-28 |
| `wikidata/Q85395557.json` | Coumeenoole North / Dunmore Head (Ogham Site): five coordinates, each with its own source | `Special:EntityData`, 2026-09-28 |
| `wikidata/Q141591358.json` | Ringfort Lisheenagreine, the findspot of CIIC 81: SMR CO084-090001-, OSM way | `Special:EntityData`, 2026-09-28 |
| `wikidata/Q104309699.json` | Townland Coumeenoole North (Logainm 22572, OSM relation 4250372) | `Special:EntityData`, 2026-09-28 |
| `wikidata/Q26716192.json` | Dunmore Head / An Dún Mór (Logainm 1394328, OSM node) | `Special:EntityData`, 2026-09-28 |
| `wikidata/Q59419929.json` | Barony Corkaguiny / Corca Dhuibhne | `Special:EntityData`, 2026-09-28 |
| `wikidata/Q20616069.json` | Barony Kinalmeaky | `Special:EntityData`, 2026-09-28 |
| `fuzzy-sl/Q74.json`, `Q131.json` | the two stones in the fuzzy-sl Wikibase: one coordinate statement per location type, with method, certainty and source | fuzzy-sl.wikibase.cloud, 2026-09-28 |
| `osm/node_5145413640.xml` | OSM node of CIIC 178 (`inscription`, `ref:IE:smr`, `wikidata`) | OSM API 0.6, 2026-09-28 (ODbL) |
| `osm/node_4306696347.xml` | OSM node of Dunmore Head | OSM API 0.6, 2026-09-28 (ODbL) |
| `osm/way_1252604956.xml` | OSM way of the ringfort at Garranes | OSM API 0.6, 2026-09-28 (ODbL) |
| `osm/relation_4250372.xml` | OSM relation of the townland Coumeenoole North | OSM API 0.6, 2026-09-28 (ODbL) |
| `epidoc/I-COR-030.xml`, `I-KER-046.xml` | OG(H)AM EpiDoc editions of CIIC 81 and CIIC 178; step 05 reads the current transliteration and its underdotted letters from them | [lguariento/og-h-am](https://github.com/lguariento/og-h-am) commit `0a2c7a0`, 2026-09-28 (CC BY 4.0) |
| `manual/ogham.yaml` | everything for step 05 that is in none of those files: GND IDs, the other editors' readings, kin groups, picture credits, labels of the fuzzy-sl properties | supplied by Florian Thiery, 2026-09-28 (answers in the questionnaire) |
| `images/ciic81-stone-corridor-thiery.jpg` | Stone Corridor, University College Cork | Florian Thiery, CC BY-NC-SA 4.0 |
| `images/ciic178-coumeenoole-thiery.png` | CIIC 178 on Dunmore Head | Florian Thiery, CC BY 4.0, via Wikimedia Commons |
| `ct/facts.yaml` | Figures and facts stated in the c't article (GND/Wikidata numbers, cooperation, picture credits), with page | transcribed from the article, 2026-09-22 |
| `ct/quotes.yaml` | Quotations from c't 19/2026, pp. 118–121 (E. Giardina), with page, speaker and status | transcribed from the article, 2026-09-22 |

`ct/quotes.yaml` holds short quotations only, for use with attribution. The
article PDF itself is not part of this repository.
