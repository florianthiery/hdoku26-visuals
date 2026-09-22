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

| # | Figure | Files |
|---|---|---|
| 01 | Garranes: one name, several places — what the GND record says, what Wikidata/Logainm/OSM and GeoNames say, and how far apart they are | `img/01-ein-name-viele-orte/ein-name-viele-orte.{de,en}.{svg,png}` |
| 02 | Both sides moving towards Wikibase — the GND today and next (GNDplus, NFDI geodata module) set against CIIC 81, the stone from Garranes, as it already lives in a federated Wikibase ecosystem and in OpenStreetMap | `img/02-wikibase-konvergenz/wikibase-konvergenz.{de,en}.{svg,png}` |

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

Code: MIT. Figures: CC BY 4.0. Wikidata content: CC0. GND data: CC0.
OpenStreetMap data: © OpenStreetMap contributors, ODbL. Natural Earth: public
domain. Quotations from c't are short citations with attribution.
