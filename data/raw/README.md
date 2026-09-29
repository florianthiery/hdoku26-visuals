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
| `osm/boundaries.geojson` | Areas drawn in figure B: baronies Corkaguiny (5304974) and Kinalmeaky (6408043), townlands Coumeenoole North (4250372) and Garranes (6168494), ringfort way 1252604956; coordinates rounded to 5 decimals, tags reduced to name, boundary, Logainm and Wikidata | Overpass turbo (`out geom`), 2026-09-28 (ODbL) |
| `epidoc/I-COR-030.xml`, `I-KER-046.xml` | OG(H)AM EpiDoc editions of CIIC 81 and CIIC 178; step 05 reads the current transliteration and its underdotted letters from them | [lguariento/og-h-am](https://github.com/lguariento/og-h-am) commit `0a2c7a0`, 2026-09-28 (CC BY 4.0) |
| `manual/ogham.yaml` | everything for step 05 that is in none of those files: GND IDs, the other editors' readings, kin groups, picture credits, labels of the fuzzy-sl properties | supplied by Florian Thiery, 2026-09-28 (answers in the questionnaire) |
| `images/ciic81-stone-corridor-thiery.jpg` | Stone Corridor, University College Cork | Florian Thiery, CC BY-NC-SA 4.0 |
| `images/ciic178-coumeenoole-thiery.png` | CIIC 178 on Dunmore Head | Florian Thiery, CC BY 4.0, via Wikimedia Commons |
| `wikidata/Q121842432.json`, `Q953927.json`, `Q18674069.json`, `Q60554307.json`, `Q60554717.json`, `Q180231.json`, `Q873607.json`, `Q126443484.json`, `Q126443332.json`, `Q120966194.json`, `Q126393245.json`, `Q126528008.json`, `Q126875543.json` | Step 06: St. Fiachra's Well, the two saints, the two civil parishes, County Kilkenny (with GND 4110260-5 as P227), the diocese, the WikiProject with its Holy Well Semantic Concept and the four sources it requires | `Special:EntityData`, 2026-09-28 |
| `osm/node_8515265450.xml` | OSM node of St. Fiachra's Well (`name:etymology:wikidata`, `access:conditional`, `ref:IE:smr`) | OSM API 0.6, 2026-09-28 (ODbL) |
| `osm/boundaries-kilkenny.geojson` | County Kilkenny and 25 civil parishes around the two wells; coordinates rounded to 5 decimals | Overpass turbo (`out geom`), 2026-09-28 (ODbL) |
| `sparql/holywells-concept.json`, `holywells-by-patron.json` | The two WikiProject queries (wells carrying the Holy Well Semantic Concept; wells with coordinate and patron in IE and UK). Every count in figure 06 A is counted from these files at build time | Wikidata Query Service, 2026-09-28 (CC0) |
| `manual/holywells.yaml` | Step 06: GND numbers of the saints and the county, picture credits, map windows, and the summary of the WikiProject's data model | supplied by Florian Thiery, 2026-09-28 |
| `images/holywell-lachtain-distel.png`, `holywell-fiachra-distel.png` | The two wells | Anne-Karoline Distel, CC0, via Wikimedia Commons |
| `wikidata/Q1441331.json`, `Q191897.json`, `Q12649101.json`, `Q755123.json`, `Q374096.json`, `Q148440.json`, `Q5061.json`, `Q3803.json` | Step 07: Franchthi Cave, the Argolis regional unit and the historical region of the same name, the Phlegraean Fields, Chauvet Cave, Flores, East Nusa Tenggara and the Lesser Sunda Islands | `Special:EntityData`, 2026-09-28 |
| `osm/boundaries-argolis.geojson` | Argolis regional unit (937635), municipality of Ermionida (2185768) and the Franchthi node (1221172611) | Overpass turbo (`out geom`), 2026-09-28 (ODbL) |
| `osm/boundaries-campania.geojson` | Metropolitan City of Naples (40600), Pozzuoli (40808), the Campi Flegrei caldera rim (way 1260684434) and the volcano node (4948370721, which carries `fixme=position`) | Overpass turbo (`out geom`), 2026-09-28 (ODbL) |
| `osm/boundaries-flores.geojson` | Island of Flores (7219477) and Manggarai Regency (11228382) | Overpass turbo (`out geom`), 2026-09-28 (ODbL) |
| `osm/relation_9854999.xml` | Susak, the island CI findspot 48 points at: `wikidata=Q994174`, `wikipedia=hr:Susak`, i.e. Croatia and not Greece | OSM API 0.6, 2026-09-28 (ODbL) |
| `geolod/ci_findspots.csv`, `sisal_sites.csv` | The two geo-lod tables. Every count in figure 07 A is counted from them at build time: 74 CI findspots with certainty level, spatial type and matches; 305 SISAL sites with the archaeology and identifier columns | [GeoScience-FAIRification-LOD](https://github.com/Research-Squirrel-Engineers/GeoScience-FAIRification-LOD), 2026-09-28 (CC BY 4.0) |
| `geolod/ci_findspots_excerpt.ttl`, `sisal_sites_excerpt.ttl` | The RDF of the findspots and cave sites the figures quote, so the predicates shown are read rather than typed | same repository, 2026-09-28 (CC BY 4.0) |
| `manual/geolod.yaml` | Step 07: GND numbers looked up by hand in the GND Explorer (Franchthi-Höhle 4228929-4, Argolis 4002893-8) with their entity types, the two chains of places, map windows, and the two identifier mismatches the figures point out | supplied by Florian Thiery, 2026-09-28 |
| `bb5kbc/fst_wgs84.csv` | The 540 enriched findspots of bb-5kbc with administrative units and their Wikidata, GeoNames, Getty TGN, iDAI.gazetteer and OSM identifiers. Every count in figure 08 A is counted from this table | [bb-5kbc-sites](https://github.com/Research-Squirrel-Engineers/bb-5kbc-sites), 2026-09-29 (CC BY 4.0) |
| `wikidata/Q587069.json`, `Q6181.json`, `Q1208.json`, `Q2191877.json`, `Q715974.json`, `Q54150.json` | Step 08: Seelow, Märkisch-Oderland and Brandenburg (all three with P227), gmina Jordanów Śląski and powiat wrocławski (neither with P227) and the Lower Silesian Voivodeship | `Special:EntityData`, 2026-09-29 |
| `wikidata/Q139477253.json`, `Q139477652.json` | Step 08: the two Seelow sherds, each with its own item, a photograph and P2596 culture | `Special:EntityData`, 2026-09-29 |
| `wikidata/Q139304626.json`, `Q139304635.json`, `Q486972.json`, `Q59496158.json`, `Q959782.json` | Step 08: the excavation report (grey literature, with its activity number), von Richthofen 1930, and the site-type and discovery vocabulary | `Special:EntityData`, 2026-09-29 |
| `osm/boundaries-seelow.geojson`, `boundaries-jordanow.geojson` | Seelow (1332928) in Märkisch-Oderland (318248); gmina Jordanów Śląski (3049634) in powiat wrocławski (451517) | Overpass turbo (`out geom`), 2026-09-29 (ODbL) |
| `osm/boundaries-bb-ds.geojson` | Brandenburg (62504) and województwo dolnośląskie (224457), for the locator insets | Overpass turbo (`out geom`), 2026-09-29 (ODbL) |
| `manual/bb5kbc.yaml` | Step 08: GND numbers with their entity types and dates (Seelow 4340023-1, Märkisch-Oderland 4336493-7, the two Lower Silesias 4042237-9 and 4596748-9, Stichbandkeramik 4183246-2, Jordansmühler Kultur 1231725982 with its definition), the two chains of places, and the map windows | supplied by Florian Thiery, 2026-09-29 (GND Explorer) |
| `poseidon/spatial-coverage.csv` | Derived counts over the 213 .janno files of the Poseidon Community Archive and over the spatial nodes of `poseidon_LOD.ttl` (149 MB, Git LFS). Both sources are far too large for this repository, so the counts travel instead of the inputs; the file's header records how they were made | counted 2026-09-29 from [community-archive](https://github.com/poseidon-framework/community-archive) and [poseidon2lod](https://github.com/archaeonatural-cloud/poseidon2lod) (CC BY 4.0) |
| `poseidon/2019_Mittnik_BAEurope.janno`, `2024_GnecchiRuscone_AvarPedigrees.janno` | The two packages the examples come from; everything figure 09 says about AITI_119 and RKC001 is read from them | [community-archive](https://github.com/poseidon-framework/community-archive), 2026-09-29 (CC BY 4.0) |
| `poseidon/poseidon_lod_excerpt.ttl` | The RDF of the two individuals and the spatial nodes they hang on, reduced to the statements the figures use | [poseidon2lod](https://github.com/archaeonatural-cloud/poseidon2lod), 2026-09-29 (CC BY 4.0) |
| `wikidata/Q512970.json`, `Q10414.json`, `Q945191.json`, `Q831079.json`, `Q645860.json` | Step 09: Kleinaitingen and the Augsburg district, Rákóczifalva and the Szolnok district, and the Hungarian statistical region that sits above them | `Special:EntityData`, 2026-09-29 |
| `osm/boundaries-lechtal.geojson` | Kleinaitingen (935162) in the Augsburg district (62622), the named commercial area `Gewerbegebiet Kleinaitingen` (way 376729440) and the Unterer Talweg (ways 33401827, 186888644) | Overpass turbo (`out geom`), 2026-09-29 (ODbL) |
| `osm/boundaries-tisza.geojson` | Rákóczifalva (1273070) in the Szolnok district (2376095), plus the statistical region Alföld és Észak (22793). A query for `Bagi-földek` within 3 km returned nothing, which is the finding | Overpass turbo (`out geom`), 2026-09-29 (ODbL) |
| `manual/poseidon.yaml` | Step 09: GND numbers with entity types (Theiß 4106223-1 and the 35 hits around it, Kleinaitingen 4635172-3, Haunstetten 2012911-7 → 4096014-6, Rákóczifalva 1075762995), both chains, the map windows | supplied by Florian Thiery, 2026-09-29 (GND Explorer) |
| `ct/facts.yaml` | Figures and facts stated in the c't article (GND/Wikidata numbers, cooperation, picture credits), with page | transcribed from the article, 2026-09-22 |
| `ct/quotes.yaml` | Quotations from c't 19/2026, pp. 118–121 (E. Giardina), with page, speaker and status | transcribed from the article, 2026-09-22 |

`ct/quotes.yaml` holds short quotations only, for use with attribution. The
article PDF itself is not part of this repository.
