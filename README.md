# hdoku26-visuals

Figures for the talk **"Orte ohne Normdatensatz? Wikidata und OpenStreetMap als
interdisziplinäre Community-Hub-Alternative für Geografika"** — Florian Thiery
(LEIZA) with Sophie C. Schmidt, Fiona Schenk, Mattis thor Straten and Anja
Gerber, Berliner Herbsttreffen zur Museumsdokumentation, Konrad-Zuse-Zentrum
Berlin, 5 October 2026.

The figures set the GND against community hubs (Wikidata, OpenStreetMap and
the gazetteers reached through them), taking the c't article "Von Karteikarten
zur KI" (E. Giardina, c't 19/2026, pp. 118–121) as the reference for what the
GND does today and plans next. The lead example is *Garranes*, Co. Cork — the
findspot of the Ogham stone CIIC 81.

Same house pattern as
[bb-5kbc-visuals](https://github.com/Research-Squirrel-Engineers/bb-5kbc-visuals):
pure-Python SVG authoring, PNG rasterised in-process with resvg-py and the
vendored Fira Sans, a fixed 7:4 canvas (1750×1000), no title or citation
baked in, German and English versions of every figure, deterministic output.

## Figures

| # | Figure | Slide caption (DE) | Files |
|---|---|---|---|
| 00a | Three hubs — GND, Wikidata/Wikibase and OpenStreetMap as the c't article describes the first two, the cooperation between them, and the bridge to OSM the article does not mention; placeholders for cover and opener; the example Konrad Zuse (GND Explorer graph, his two places on a schematic map, photo) | Drei Drehkreuze: GND, Wikiversum und OSM | `img/00-einleitung/drei-drehkreuze.{de,en}.{svg,png}` |
| 00b | Dense and thin — GND Explorer graphs of Tim Berners-Lee and Goethe (own screenshots) above every edge of the GND record Garranes, with three quotations on why | Dicht bei Personen, dünn bei Fundstellen | `img/00-einleitung/dicht-und-duenn.{de,en}.{svg,png}` |
| 01 | Garranes: one name, several places — what the GND record says, what Wikidata/Logainm/OSM and GeoNames say, and how far apart they are | Ohne Geometrie bleibt offen, welches Garranes gemeint ist | `img/01-ein-name-viele-orte/ein-name-viele-orte.{de,en}.{svg,png}` |
| 02 | Both sides moving towards Wikibase — the GND today and next set against CIIC 81, the stone from Garranes, federated across Wikibases and OpenStreetMap | Beide Seiten bewegen sich auf Wikibase zu | `img/02-wikibase-konvergenz/wikibase-konvergenz.{de,en}.{svg,png}` |
| 03 | The niche is the hub — on the DNB's own axis, two mini knowledge graphs (Garranes, St. Lachtain's Well), who entered the data, responsibility per statement | Die Nische ist der Hub – und jede Aussage hat eine Quelle | `img/03-nische-hub/nische-hub.{de,en}.{svg,png}` |

Figure 00a contains text placeholders for two third-party pictures from the
c't article (cover, opener). These pictures are not part of
the repository; they are placed on the slide by hand, with the credit printed
under each frame.

## Build

    pip install -r requirements.txt
    python main.py

`python main.py --list` shows the steps; `--only 01`, `--from 01`,
`--skip 01`, `--dry-run` and `--strict` work as in the sibling repositories.

**Fonts:** `fonts/FiraSans-Regular.ttf` and `fonts/FiraSans-Medium.ttf`
(SIL Open Font License) are the same files as in bb-5kbc-visuals.

## Data

All inputs are under `data/raw/` and are described in
[`data/raw/README.md`](data/raw/README.md). No step accesses the network.

## Licence

Code: MIT. Figures: CC BY 4.0, except the embedded photo of Konrad Zuse in
00a (Wolfgang Hunscher, CC BY-SA 3.0, via Wikimedia Commons). Wikidata content: CC0. GND data: CC0.
OpenStreetMap data: © OpenStreetMap contributors, ODbL. Natural Earth: public
domain. Quotations from c't are short citations with attribution.
