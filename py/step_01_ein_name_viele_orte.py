#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_01_ein_name_viele_orte.py -- "Garranes": one name, several places
=======================================================================

Figure 1 of the talk "Orte ohne Normdatensatz?" (Berliner Herbsttreffen zur
Museumsdokumentation 2026). It opens on the homonymy problem with which the
c't article itself opens (Neustadt, Thomas Müller -- c't 19/2026, p. 119) and
shows it on the talk's lead example, *Garranes* in County Cork:

1. the townland of Garranes (An Garrán), with the Ogham findspot of CIIC 81
   in it -- known to Wikidata, Logainm and OpenStreetMap;
2. the ringfort Lisnacaheragh in the same townland -- the place the GND
   record 1248049489 describes ("Mittelalterliche Ringwallanlage d. 5.-6. Jh.
   in Südwestirland"), with no coordinate and no Wikidata item of its own;
3. the GeoNames locality 3299501 "Garranes" -- the cataloguing source the
   GND record names, 36.6 km from the townland;
4. the promontory fort Garranes / Dooneen Point, Wikidata Q31066388.

The point is not that the GND lacks Garranes -- it has it -- but that a name
plus an identifier without geometry and without links cannot say *which*
Garranes it means.

Sources (all under ``data/raw/``, read-only):

* ``wikidata/Q104295278.json``, ``wikidata/Q69385525.json`` -- entity JSON
  of the townland and the Ogham site (coordinates, Logainm, OSM relation);
* ``gnd/1248049489.ttl`` -- the GND record as downloaded;
* ``manual/places.yaml`` -- GeoNames 3299501, Wikidata Q31066388 and the
  GND Explorer's cataloguing-source line, read from the web pages;
* ``naturalearth/ireland_outline.json`` -- island-of-Ireland coastline from
  Natural Earth 1:10m (public domain), via the ``world-atlas`` package;
* ``ct/quotes.yaml`` -- the two c't quotations used (A1, A2).

Distances are computed here from the coordinates, not typed in.

House rules (from bb-5kbc-visuals): no title/footer baked in, no diagonal
lines, bilingual DE/EN output, deterministic SVG.

Writes: img/01-ein-name-viele-orte/ein-name-viele-orte.{de,en}.{svg,png}
Run standalone: ``python py/step_01_ein_name_viele_orte.py``
"""

from __future__ import annotations

import json
import math

import yaml
from rdflib import Graph, Namespace, URIRef

import hdoku26_visuals_utils as vu

OUT = vu.OUT_DIRS["01-ein-name-viele-orte"]
RAW = vu.DATA_RAW

GNDO = Namespace("https://d-nb.info/standards/elementset/gnd#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
GND_IRI = URIRef("https://d-nb.info/gnd/1248049489")

# Map window (WGS84) and panel geometry
LON0, LON1 = -10.35, -7.95
LAT0, LAT1 = 51.40, 52.18
MAP_X, MAP_Y, MAP_W = 60, 50, 1010
K = math.cos(math.radians((LAT0 + LAT1) / 2))           # equirectangular aspect
SCALE = MAP_W / ((LON1 - LON0) * K)                    # px per degree latitude
MAP_H = (LAT1 - LAT0) * SCALE
PX_PER_KM = SCALE / 111.32

RIGHT_X, RIGHT_W = 1110, 580
BOTTOM_Y = MAP_Y + MAP_H + 44


# --------------------------------------------------------------------------- #
# Data loading
# --------------------------------------------------------------------------- #
def _wd(qid: str) -> dict:
    data = json.loads((RAW / "wikidata" / f"{qid}.json").read_text(encoding="utf-8"))
    return data["entities"][qid]


def _claim_value(entity: dict, prop: str):
    return entity["claims"][prop][0]["mainsnak"]["datavalue"]["value"]


def load() -> dict:
    townland = _wd("Q104295278")
    site = _wd("Q69385525")
    t_coord = _claim_value(townland, "P625")
    s_coord = _claim_value(site, "P625")
    manual = yaml.safe_load((RAW / "manual" / "places.yaml").read_text(encoding="utf-8"))
    quotes = yaml.safe_load((RAW / "ct" / "quotes.yaml").read_text(encoding="utf-8"))

    g = Graph()
    g.parse(RAW / "gnd" / "1248049489.ttl", format="turtle")
    gnd = {
        "id": str(g.value(GND_IRI, GNDO.gndIdentifier)),
        "name": str(g.value(GND_IRI, GNDO.preferredNameForThePlaceOrGeographicName)),
        "info": str(g.value(GND_IRI, GNDO.biographicalOrHistoricalInformation)),
        "area": str(g.value(GND_IRI, GNDO.geographicAreaCode)).rsplit("#", 1)[-1],
        "same_as": [str(o) for o in g.objects(GND_IRI, OWL.sameAs)],
        "has_geometry": any("geosparql" in str(p) or "wgs84" in str(p)
                            for p, _ in g.predicate_objects(GND_IRI)),
    }

    geonames = manual["geonames_3299501"]
    fort = manual["wikidata_Q31066388"]
    tl = (t_coord["latitude"], t_coord["longitude"])
    return {
        "townland": {
            "qid": townland["id"],
            "label_ga": townland["labels"]["ga"]["value"],
            "lat": tl[0], "lon": tl[1],
            "logainm": _claim_value(townland, "P5097"),
            "osm_rel": _claim_value(townland, "P402"),
        },
        "site": {
            "qid": site["id"],
            "lat": s_coord["latitude"], "lon": s_coord["longitude"],
            "m_to_townland": 1000 * vu.haversine_km(*tl, s_coord["latitude"], s_coord["longitude"]),
        },
        "geonames": {**geonames, "km": vu.haversine_km(*tl, geonames["lat"], geonames["lon"])},
        "fort": {**fort, "km": vu.haversine_km(*tl, fort["lat"], fort["lon"])},
        "cork": manual["cork_city"],
        "gnd": gnd,
        "gnd_ui": manual["gnd_1248049489_ui"],
        "quotes": [quotes["A1"], quotes["A2"]],
    }


# --------------------------------------------------------------------------- #
# Drawing
# --------------------------------------------------------------------------- #
def project(lon: float, lat: float) -> tuple[float, float]:
    return (MAP_X + (lon - LON0) * K * SCALE, MAP_Y + (LAT1 - lat) * SCALE)


def _basemap(parts: list[str]) -> None:
    rings = json.loads((RAW / "naturalearth" / "ireland_outline.json").read_text(encoding="utf-8"))
    parts.append('<defs><clipPath id="mapclip">'
                 f'<rect x="{MAP_X}" y="{MAP_Y}" width="{MAP_W}" height="{MAP_H:.1f}" rx="12"/>'
                 '</clipPath></defs>')
    parts.append(f'<rect x="{MAP_X}" y="{MAP_Y}" width="{MAP_W}" height="{MAP_H:.1f}" rx="12" '
                 f'fill="{vu.SEA_FILL}"/>')
    parts.append('<g clip-path="url(#mapclip)">')
    for poly in rings:
        d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in (project(*p) for p in poly["ring"])) + " Z"
        parts.append(f'<path d="{d}" fill="{vu.LAND_FILL}" stroke="{vu.LAND_STROKE}" stroke-width="1"/>')
    parts.append("</g>")
    parts.append(f'<rect x="{MAP_X}" y="{MAP_Y}" width="{MAP_W}" height="{MAP_H:.1f}" rx="12" '
                 f'fill="none" stroke="{vu.LINE_NEUTRAL}" stroke-width="1.2"/>')


def _inset(parts: list[str], lang: str) -> None:
    """Small whole-island locator, top-left, with the map window marked."""
    rings = json.loads((RAW / "naturalearth" / "ireland_outline.json").read_text(encoding="utf-8"))
    ix, iy, iw, ih = MAP_X + 14, MAP_Y + 14, 150, 180
    lon0, lon1, lat0, lat1 = -10.8, -5.3, 51.3, 55.5
    k = math.cos(math.radians(53.4))
    s = min((iw - 16) / ((lon1 - lon0) * k), (ih - 16) / (lat1 - lat0))

    def pj(lon, lat):
        return ix + 8 + (lon - lon0) * k * s, iy + 8 + (lat1 - lat) * s

    parts.append(f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="8" fill="#ffffff" '
                 f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')
    for poly in rings:
        d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in (pj(*p) for p in poly["ring"])) + " Z"
        parts.append(f'<path d="{d}" fill="{vu.LAND_FILL}" stroke="{vu.LAND_STROKE}" stroke-width="0.8"/>')
    x0, y0 = pj(LON0, LAT1)
    x1, y1 = pj(LON1, LAT0)
    parts.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" '
                 f'fill="none" stroke="{vu.TEXT_DARK}" stroke-width="1.4"/>')
    parts.append(vu.svg_text(ix + iw - 10, iy + 20, vu.t(lang, "Irland", "Ireland"),
                             size=11.5, color=vu.TEXT_MUTED, anchor="end"))


def _scale_and_legend(parts: list[str], lang: str) -> None:
    # scale bar, bottom-right of the map
    km = 20
    bx1 = MAP_X + MAP_W - 350
    bx0 = bx1 - km * PX_PER_KM
    by = MAP_Y + MAP_H - 28
    parts.append(f'<path d="M {bx0:.1f} {by - 5:.1f} L {bx0:.1f} {by:.1f} L {bx1:.1f} {by:.1f} '
                 f'L {bx1:.1f} {by - 5:.1f}" fill="none" stroke="{vu.TEXT_DARK}" stroke-width="1.4"/>')
    parts.append(vu.svg_text((bx0 + bx1) / 2, by - 9, f"{km} km", size=11.5, anchor="middle"))

    # legend, bottom-left of the map (over the sea south of Beara)
    lx, ly = MAP_X + MAP_W - 300, MAP_Y + MAP_H - 118
    entries = [
        (vu.t(lang, "Wikidata · Logainm · OpenStreetMap", "Wikidata · Logainm · OpenStreetMap"), vu.COMMUNITY, False),
        ("GND", vu.GND, False),
        ("GeoNames", vu.AGGREGATOR, False),
        (vu.t(lang, "ohne Koordinate, Lage vermutet", "no coordinate, location presumed"),
         {"fill": vu.UNCERTAIN_FILL, "stroke": vu.UNCERTAIN_STROKE}, True),
    ]
    parts.append(f'<rect x="{lx - 12}" y="{ly - 14}" width="290" height="{len(entries) * 24 + 14}" '
                 f'rx="8" fill="#ffffff" fill-opacity="0.9" stroke="{vu.LINE_NEUTRAL}" stroke-width="0.8"/>')
    for i, (label, colors, dashed) in enumerate(entries):
        cy = ly + i * 24 + 6
        dash = ' stroke-dasharray="3 2"' if dashed else ""
        fill = "#ffffff" if dashed else colors["stroke"]
        parts.append(f'<circle cx="{lx + 6}" cy="{cy}" r="7" fill="{fill}" '
                     f'stroke="{colors["stroke"]}" stroke-width="1.6"{dash}/>')
        parts.append(vu.svg_text(lx + 22, cy + 0.5, label, size=12, baseline="central"))


def _map_marks(parts: list[str], d: dict, lang: str) -> None:
    tl, gn, fort, cork = d["townland"], d["geonames"], d["fort"], d["cork"]

    # Cork city, orientation only
    cx, cy = project(cork["lon"], cork["lat"])
    parts.append(f'<rect x="{cx - 4:.1f}" y="{cy - 4:.1f}" width="8" height="8" fill="{vu.TEXT_MUTED}"/>')
    parts.append(vu.svg_text(cx - 10, cy + 0.5, "Cork", size=13, color=vu.TEXT_MUTED, baseline="central",
                             anchor="end"))

    # 1 + 2: townland (with the Ogham site 24 m away) and the presumed ringfort
    x1, y1 = project(tl["lon"], tl["lat"])
    parts.append(f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="40" fill="{vu.UNCERTAIN_FILL}" fill-opacity="0.45" '
                 f'stroke="{vu.UNCERTAIN_STROKE}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    parts.append(vu.svg_marker(x1, y1, "1", vu.COMMUNITY))
    parts.append(vu.svg_marker(x1 - 28, y1 - 28, "2",
                               {"fill": vu.UNCERTAIN_FILL, "stroke": vu.UNCERTAIN_STROKE},
                               r=12, dashed=True))
    parts.append(vu.svg_text(x1 - 52, y1 + 6, "Garranes", size=16, weight=500, anchor="end"))
    parts.append(vu.svg_text(x1 - 52, y1 + 24, "Templemartin", size=12, color=vu.TEXT_MUTED, anchor="end"))

    # 3: GeoNames locality
    x3, y3 = project(gn["lon"], gn["lat"])
    parts.append(vu.svg_marker(x3, y3, "3", vu.AGGREGATOR))
    parts.append(vu.svg_text(x3 + 24, y3 - 4, "Garranes", size=16, weight=500))
    parts.append(vu.svg_text(x3 + 24, y3 + 15, vu.t(lang, f"{vu.fmt_num(gn['km'], lang)} km von 1",
                                                    f"{vu.fmt_num(gn['km'], lang)} km from 1"),
                             size=12.5, color=vu.TEXT_MUTED))

    # 4: promontory fort
    x4, y4 = project(fort["lon"], fort["lat"])
    parts.append(vu.svg_marker(x4, y4, "4", vu.COMMUNITY))
    parts.append(vu.svg_text(x4 + 24, y4 - 4, "Garranes", size=16, weight=500))
    parts.append(vu.svg_text(x4 + 24, y4 + 14, vu.t(lang, f"Dooneen Point · {vu.fmt_num(fort['km'], lang)} km von 1",
                                                    f"Dooneen Point · {vu.fmt_num(fort['km'], lang)} km from 1"),
                             size=12, color=vu.TEXT_MUTED))


def _gnd_card(parts: list[str], d: dict, lang: str) -> None:
    g, ui = d["gnd"], d["gnd_ui"]
    x, y, w = RIGHT_X, MAP_Y, RIGHT_W
    h = MAP_H
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h:.1f}" rx="12" fill="#ffffff" '
                 f'stroke="{vu.GND["stroke"]}" stroke-width="1.6"/>')
    parts.append(f'<path d="M {x} {y + 12} Q {x} {y} {x + 12} {y} L {x + w - 12} {y} '
                 f'Q {x + w} {y} {x + w} {y + 12} L {x + w} {y + 58} L {x} {y + 58} Z" '
                 f'fill="{vu.GND["fill"]}" stroke="none"/>')
    parts.append(vu.svg_text(x + 20, y + 26, vu.t(lang, "Was der GND-Datensatz weiß", "What the GND record says"),
                             size=12.5, color=vu.GND["stroke"], weight=500))
    parts.append(vu.svg_text(x + 20, y + 47, f"{g['name']}  ·  GND {g['id']}", size=17, weight=500))

    rows = [
        (vu.t(lang, "Entitätentyp", "Entity type"), vu.t(lang, "Gebietskörperschaft (gik)", "territorial corporate body (gik)"), None),
        (vu.t(lang, "Land", "Country"), f"{g['area']} ({vu.t(lang, 'Irland', 'Ireland')})", None),
        (vu.t(lang, "Beispiel für", "Instance of"), vu.t(lang, "Archäologische Stätte", "archaeological site"), None),
        (vu.t(lang, "Beschreibung", "Description"), vu.t(lang, f"„{g['info']}“", f"“{g['info']}”"), "2"),
        (vu.t(lang, "Quelle", "Source"), vu.t(lang, "GeoNames 3299501 (Stand 20.12.2021)",
                                              "GeoNames 3299501 (as of 20.12.2021)"), "3"),
        ("owl:sameAs", ", ".join("VIAF" if "viaf" in s else s for s in g["same_as"]), None),
        (vu.t(lang, "Koordinate", "Coordinate"),
         vu.t(lang, "keine", "none") if not g["has_geometry"] else vu.t(lang, "vorhanden", "present"), "!"),
    ]
    ry = y + 96
    label_w = 128
    for label, value, badge in rows:
        parts.append(vu.svg_text(x + 20, ry, label, size=13.5, color=vu.TEXT_MUTED))
        color = vu.UNCERTAIN_STROKE if badge == "!" else vu.TEXT_DARK
        block, ny = vu.svg_text_block(x + 20 + label_w, ry, value, w - label_w - 90, size=15,
                                      line_h=21, color=color, weight=500 if badge == "!" else 400)
        parts.append(block)
        if badge in ("2", "3"):
            colors = ({"fill": vu.UNCERTAIN_FILL, "stroke": vu.UNCERTAIN_STROKE} if badge == "2"
                      else vu.AGGREGATOR)
            parts.append(vu.svg_marker(x + w - 32, ry - 5, badge, colors, r=12, dashed=(badge == "2")))
        ry = max(ny, ry + 21) + 17
    parts.append(f'<line x1="{x + 20}" y1="{ry - 4:.1f}" x2="{x + w - 20}" y2="{ry - 4:.1f}" '
                 f'stroke="{vu.GND["stroke"]}" stroke-width="0.8" opacity="0.5"/>')
    km = vu.fmt_num(d["geonames"]["km"], lang)
    note = vu.t(lang,
                f"Die Beschreibung passt zum Ringfort bei 1, die Quelle zeigt auf 3 – "
                f"{km} km auseinander. Ohne Geometrie lässt sich das am Datensatz nicht erkennen.",
                f"The description fits the ringfort at 1, the source points to 3 – "
                f"{km} km apart. Without geometry, the record itself cannot reveal this.")
    block, _ = vu.svg_text_block(x + 20, ry + 22, note, w - 40, size=15, line_h=22, color=vu.TEXT_DARK)
    parts.append(block)
    parts.append(vu.svg_text(x + 20, y + h - 16, f"d-nb.info/gnd/{g['id']} · {vu.t(lang, 'Ersterfassung', 'created')} "
                                                 f"20.12.2021 ({ui['cataloguing_institution']})",
                             size=11, color=vu.TEXT_MUTED))


def _candidate_cards(parts: list[str], d: dict, lang: str) -> None:
    tl, site, gn, fort = d["townland"], d["site"], d["geonames"], d["fort"]
    unc = {"fill": vu.UNCERTAIN_FILL, "stroke": vu.UNCERTAIN_STROKE}
    cards = [
        ("1", vu.COMMUNITY, False, vu.t(lang, "Townland Garranes", "Townland of Garranes"),
         f"{tl['label_ga']} · " + vu.t(lang, f"Ogham-Fundstelle ({site['m_to_townland']:.0f} m)",
                                       f"Ogham findspot ({site['m_to_townland']:.0f} m)"),
         [(f"Wikidata {tl['qid']}", vu.COMMUNITY, False), (f"Wikidata {site['qid']}", vu.COMMUNITY, False),
          (f"Logainm {tl['logainm']}", vu.COMMUNITY, False), (f"OSM rel. {tl['osm_rel']}", vu.COMMUNITY, False)],
         vu.t(lang, "Bezugspunkt der Abstände", "reference point for distances")),
        ("2", unc, True, vu.t(lang, "Ringfort Lisnacaheragh", "Lisnacaheragh ringfort"),
         vu.t(lang, "5.–6. Jh., im Townland Garranes", "5th–6th c., in the townland of Garranes"),
         [(f"GND {d['gnd']['id']}", vu.GND, False),
          (vu.t(lang, "kein Wikidata-Item", "no Wikidata item"), unc, True),
          (vu.t(lang, "keine Koordinate", "no coordinate"), unc, True)],
         vu.t(lang, "Lage nur über die Beschreibung", "location only via the description")),
        ("3", vu.AGGREGATOR, False, vu.t(lang, "Garranes (Locality)", "Garranes (locality)"),
         vu.t(lang, "Quelle des GND-Datensatzes", "source of the GND record"),
         [("GeoNames 3299501", vu.AGGREGATOR, False)],
         vu.t(lang, f"{vu.fmt_num(gn['km'], lang)} km von 1", f"{vu.fmt_num(gn['km'], lang)} km from 1")),
        ("4", vu.COMMUNITY, False, "Garranes (Dooneen Point)",
         vu.t(lang, "Vorgebirgsfort", "promontory fort"),
         [(f"Wikidata {fort['source'].rsplit('/', 1)[-1]}", vu.COMMUNITY, False),
          (f"Atlas of Hillforts {fort['atlas_of_hillforts_id']}", vu.COMMUNITY, False)],
         vu.t(lang, f"{vu.fmt_num(fort['km'], lang)} km von 1", f"{vu.fmt_num(fort['km'], lang)} km from 1")),
    ]
    gap = 16
    cw = (MAP_W - 3 * gap) / 4
    ch = vu.CONTENT_Y1 - BOTTOM_Y
    for i, (num, colors, dashed, title, sub, chips, foot) in enumerate(cards):
        x = MAP_X + i * (cw + gap)
        y = BOTTOM_Y
        dash = ' stroke-dasharray="6 4"' if dashed else ""
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{ch:.1f}" rx="10" '
                     f'fill="#ffffff" stroke="{colors["stroke"]}" stroke-width="1.5"{dash}/>')
        parts.append(vu.svg_marker(x + 26, y + 28, num, colors, r=13, dashed=dashed))
        tb, ny = vu.svg_text_block(x + 48, y + 27, title, cw - 60, size=16, line_h=20, weight=500)
        parts.append(tb)
        sb, ny = vu.svg_text_block(x + 16, max(ny, y + 50) + 4, sub, cw - 32, size=13.5, line_h=18,
                                   color=vu.TEXT_MUTED)
        parts.append(sb)
        cy = ny + 10
        for label, c, dsh in chips:
            chip, _ = vu.svg_chip(x + 16, cy, label, c, dashed=dsh, size=12.5, h=25)
            parts.append(chip)
            cy += 33
        parts.append(vu.svg_text(x + 16, y + ch - 16, foot, size=13, color=vu.TEXT_MUTED, italic=True))


def _quotes(parts: list[str], d: dict, lang: str) -> None:
    x, w = RIGHT_X, RIGHT_W
    y = BOTTOM_Y
    total_h = vu.CONTENT_Y1 - BOTTOM_Y
    gap = 16
    qh = (total_h - gap) / 2
    for i, q in enumerate(d["quotes"]):
        qy = y + i * (qh + gap)
        parts.append(f'<rect x="{x}" y="{qy:.1f}" width="{w}" height="{qh:.1f}" rx="10" '
                     f'fill="{vu.QUOTE["fill"]}" stroke="{vu.QUOTE["stroke"]}" stroke-width="1.2"/>')
        text = f"„{q['de']}“" if lang == "de" else f"“{q['en']}”"
        block, _ = vu.svg_text_block(x + 22, qy + 36, text, w - 44, size=18, line_h=25, italic=True)
        parts.append(block)
        src = (f"c’t 19/2026, S. {q['page']}" if lang == "de"
               else f"c’t 19/2026, p. {q['page']} (translated)")
        parts.append(vu.svg_text(x + w - 20, qy + qh - 14, src, size=12.5, color=vu.QUOTE["stroke"],
                                 anchor="end"))


def build(lang: str = "de") -> list[str]:
    d = load()
    parts = [vu.svg_open(vu.t(lang, "Garranes: ein Name, mehrere Orte", "Garranes: one name, several places"))]
    _basemap(parts)
    _inset(parts, lang)
    _map_marks(parts, d, lang)
    _scale_and_legend(parts, lang)
    _gnd_card(parts, d, lang)
    _candidate_cards(parts, d, lang)
    _quotes(parts, d, lang)
    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"ein-name-viele-orte.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    vu.ensure_dirs()
    written = []
    for lang in ("de", "en"):
        written += build(lang)
    for p in written:
        print(f"  wrote {p}")
    return written


if __name__ == "__main__":
    main()
