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
| `ct/facts.yaml` | Figures and facts stated in the c't article (GND/Wikidata numbers, cooperation, picture credits), with page | transcribed from the article, 2026-09-22 |
| `ct/quotes.yaml` | Quotations from c't 19/2026, pp. 118–121 (E. Giardina), with page, speaker and status | transcribed from the article, 2026-09-22 |

`ct/quotes.yaml` holds short quotations only, for use with attribution. The
article PDF itself is not part of this repository.
