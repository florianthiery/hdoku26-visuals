#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_02_wikibase_konvergenz.py -- where both sides are heading: Wikibase
=========================================================================

Figure 2 of the talk "Orte ohne Normdatensatz?". Figure 1 ended on the place
Garranes; figure 2 follows the object found there -- the Ogham stone CIIC 81
(Wikidata Q130529871, "location of discovery" P189 = Garranes Q69385525),
today in the Stone Corridor of University College Cork.

Three columns and a common floor:

* left  -- the GND today and next, in the words of the c't article
  (c't 19/2026, p. 120): the Garranes record from figure 1, GNDplus (Z2),
  the NFDI geodata module (P3, reported speech), controllable openness (Z4);
* middle -- the red thread (Garranes -> CIIC 81 -> UCC Cork, two ranked
  coordinates, distance computed) and the bridge: DNB trials Wikibase since
  2019 (P4), WikiLibrary Manifesto 2020 (P5), the common goal (Z6);
* right -- CIIC 81 as it already lives in a federated Wikibase ecosystem:
  every link read from the Wikidata JSON (P189, P8168, P1325, P2888, P11693,
  P4057, P14097) plus the reverse link from the fuzzy-sl Wikibase, and the
  OpenStreetMap node whose tags point back into Wikidata ("semantic OSM");
* floor -- Wikibase, Linked Open Data and CC0 as common ground, with the
  planned CrossyBase (TRAIL 2.5) on the community side.

Sources: ``wikidata/Q130529871.json``, ``wikidata/Q69385525.json``,
``osm/node_11071361392.xml``, ``manual/federation.yaml``,
``ct/quotes.yaml`` (Z2, Z4, Z6, P3, P4, P5, P6).

Writes: img/02-wikibase-konvergenz/wikibase-konvergenz.{de,en}.{svg,png}
Run standalone: ``python py/step_02_wikibase_konvergenz.py``
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET

import yaml

import hdoku26_visuals_utils as vu

OUT = vu.OUT_DIRS["02-wikibase-konvergenz"]
RAW = vu.DATA_RAW

LEFT_X, LEFT_W = 60, 500
MID_X, MID_W = 600, 530
RIGHT_X, RIGHT_W = 1170, 520
TOP_Y, PANEL_B = 50, 770
FLOOR_Y, FLOOR_H = 815, 135


# --------------------------------------------------------------------------- #
# Data
# --------------------------------------------------------------------------- #
def _wd(qid: str) -> dict:
    return json.loads((RAW / "wikidata" / f"{qid}.json").read_text(encoding="utf-8"))["entities"][qid]


def _val(entity: dict, prop: str):
    return entity["claims"][prop][0]["mainsnak"]["datavalue"]["value"]


def load() -> dict:
    stone = _wd("Q130529871")
    site = _wd("Q69385525")
    coords = {c["rank"]: c["mainsnak"]["datavalue"]["value"] for c in stone["claims"]["P625"]}
    pref, norm = coords["preferred"], coords["normal"]
    osm = ET.parse(RAW / "osm" / "node_11071361392.xml").getroot().find("node")
    tags = {t.get("k"): t.get("v") for t in osm.findall("tag")}
    fed = yaml.safe_load((RAW / "manual" / "federation.yaml").read_text(encoding="utf-8"))
    quotes = yaml.safe_load((RAW / "ct" / "quotes.yaml").read_text(encoding="utf-8"))
    sk_url = _val(stone, "P1325")
    return {
        "stone": {
            "qid": stone["id"],
            "label": stone["labels"]["en"]["value"],
            "alias": stone["aliases"]["en"][0]["value"],
            "p189": _val(stone, "P189")["id"],
            "factgrid": _val(stone, "P8168"),
            "semkompakkt": sk_url.rsplit(":", 1)[-1],
            "ogham_lod": _val(stone, "P2888").rsplit("/", 1)[-1],
            "osm_node": _val(stone, "P11693"),
            "smr": _val(stone, "P4057").rstrip("-"),
            "sketchfab": "Sketchfab",
            "p1382": _val(stone, "P1382")["id"],
            "km": vu.haversine_km(pref["latitude"], pref["longitude"],
                                  norm["latitude"], norm["longitude"]),
        },
        "site": {"qid": site["id"], "label": site["labels"]["en"]["value"]},
        "osm": {"id": osm.get("id"), "tags": tags},
        "fuzzy": fed["fuzzy_sl_Q74"],
        "quotes": quotes,
    }


# --------------------------------------------------------------------------- #
# Small layout helpers local to this figure
# --------------------------------------------------------------------------- #
def _panel(parts, x, y, w, h, colors, kicker, title):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#ffffff" '
                 f'stroke="{colors["stroke"]}" stroke-width="1.6"/>')
    parts.append(f'<path d="M {x} {y + 12} Q {x} {y} {x + 12} {y} L {x + w - 12} {y} '
                 f'Q {x + w} {y} {x + w} {y + 12} L {x + w} {y + 58} L {x} {y + 58} Z" '
                 f'fill="{colors["fill"]}"/>')
    parts.append(vu.svg_text(x + 20, y + 25, kicker, size=12.5, weight=500, color=colors["stroke"]))
    parts.append(vu.svg_text(x + 20, y + 47, title, size=17, weight=500))


def _quote_card(parts, x, y, w, text, source, *, size=15, italic=True, quote_marks=True,
                colors=None, lang="de") -> float:
    """Amber quotation card sized to its text; returns its bottom y."""
    colors = colors or vu.QUOTE
    if quote_marks:
        text = f"„{text}“" if lang == "de" else f"“{text}”"
    lines = vu.wrap_lines(text, w - 40, size)
    h = 26 + len(lines) * size * 1.4 + 30
    parts.append(f'<rect x="{x}" y="{y:.1f}" width="{w}" height="{h:.1f}" rx="10" '
                 f'fill="{colors["fill"]}" stroke="{colors["stroke"]}" stroke-width="1.2"/>')
    block, _ = vu.svg_text_block(x + 20, y + 30, text, w - 40, size=size, line_h=size * 1.4,
                                 italic=italic)
    parts.append(block)
    parts.append(vu.svg_text(x + w - 18, y + h - 12, source, size=11.5, color=colors["stroke"],
                             anchor="end"))
    return y + h


def _src(q: dict, lang: str) -> str:
    who = q.get("speaker")
    if who in ("author", "indirect"):
        who = vu.t(lang, "Autorentext", "author's text") if who == "author" else \
            vu.t(lang, "indirekte Rede", "reported speech")
    page = vu.t(lang, f"S. {q['page']}", f"p. {q['page']}")
    tr = "" if lang == "de" else ", transl."
    return f"{who} · c’t 19/2026, {page}{tr}"


def _q(d, key, lang):
    q = d["quotes"][key]
    return (q["de"] if lang == "de" else q["en"]), _src(q, lang)


def _down(parts, x, y1, y2, colors):
    parts.append(vu.svg_arrow(x, y1, x, y2 - 2, stroke=colors["stroke"]))


# --------------------------------------------------------------------------- #
# Columns
# --------------------------------------------------------------------------- #
def _left(parts, d, lang):
    x, w = LEFT_X, LEFT_W
    _panel(parts, x, TOP_Y, w, PANEL_B - TOP_Y, vu.GND,
           vu.t(lang, "GND · heute und morgen", "GND · today and next"),
           vu.t(lang, "Normdatei, die sich öffnet", "An authority file opening up"))
    ix, iw = x + 20, w - 40
    # today: callback to figure 1
    y = TOP_Y + 78
    parts.append(f'<rect x="{ix}" y="{y}" width="{iw}" height="64" rx="10" fill="{vu.GND["fill"]}" '
                 f'stroke="{vu.GND["stroke"]}" stroke-width="1.2"/>')
    parts.append(vu.svg_text(ix + 16, y + 26, vu.t(lang, "heute", "today"), size=12, color=vu.GND["stroke"],
                             weight=500))
    parts.append(vu.svg_text(ix + 16, y + 48, vu.t(lang, "GND 1248049489 „Garranes“ · Name, Land, Beschreibung",
                                                   "GND 1248049489 “Garranes” · name, country, description"),
                             size=13.5))
    y += 64
    _down(parts, x + w / 2, y + 4, y + 26, vu.GND)
    y += 30
    text, src = _q(d, "Z2", lang)
    parts.append(vu.svg_text(ix, y + 12, "GNDplus", size=14, weight=500, color=vu.GND["stroke"]))
    y = _quote_card(parts, ix, y + 22, iw, text, "Jürgen Kett · " + src.split(" · ", 1)[-1], lang=lang)
    _down(parts, x + w / 2, y + 4, y + 26, vu.GND)
    y += 30
    text, src = _q(d, "P3", lang)
    parts.append(vu.svg_text(ix, y + 12, vu.t(lang, "Geodaten-Modul für die NFDI", "Geodata module for the NFDI"),
                             size=14, weight=500, color=vu.GND["stroke"]))
    y = _quote_card(parts, ix, y + 22, iw, text, src, size=13.5, italic=False, quote_marks=False,
                    colors={"fill": "#ffffff", "stroke": vu.GND["stroke"]}, lang=lang)
    y += 16
    text, src = _q(d, "Z4", lang)
    _quote_card(parts, ix, y, iw, text, "Barbara Fischer · " + src.split(" · ", 1)[-1], lang=lang)


def _middle(parts, d, lang):
    x, w = MID_X, MID_W
    s, site = d["stone"], d["site"]
    # red thread card
    y = TOP_Y
    h = 250
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#ffffff" '
                 f'stroke="{vu.COMMUNITY["stroke"]}" stroke-width="1.6"/>')
    parts.append(vu.svg_text(x + 20, y + 25, vu.t(lang, "Der rote Faden", "The thread"), size=12.5,
                             weight=500, color=vu.COMMUNITY["stroke"]))
    parts.append(vu.svg_text(x + 20, y + 47, vu.t(lang, "Vom Ort zum Objekt", "From the place to the object"),
                             size=17, weight=500))
    # two boxes with an orthogonal arrow
    by = y + 78
    bw = (w - 40 - 60) / 2
    parts.append(vu.svg_box(x + 20, by, bw, 64, f"{site['label'].split(' (')[0]}",
                            vu.t(lang, f"Fundort · {site['qid']}", f"findspot · {site['qid']}"),
                            fill=vu.COMMUNITY["fill"], stroke=vu.COMMUNITY["stroke"]))
    parts.append(vu.svg_box(x + 20 + bw + 60, by, bw, 64, s["alias"],
                            vu.t(lang, f"Stein · {s['qid']}", f"stone · {s['qid']}"),
                            fill=vu.COMMUNITY["fill"], stroke=vu.COMMUNITY["stroke"]))
    parts.append(vu.svg_arrow_labeled(x + 20 + bw + 60 - 2, by + 32, x + 20 + bw + 2, by + 32, "P189",
                                      font_size=11))
    km = vu.fmt_num(s["km"], lang)
    lines = [
        vu.t(lang, f"Heute in der Stone Corridor, UCC Cork – {km} km vom Fundort.",
             f"Today in the Stone Corridor, UCC Cork – {km} km from the findspot."),
        vu.t(lang, "Wikidata trägt beide Orte als Koordinaten: UCC bevorzugt (Vor-Ort-Aufnahme, "
                   "Quelle OSM), Garranes normal (georeferenziert aus der Literatur).",
             "Wikidata holds both places as coordinates: UCC preferred (on-site survey, "
             "source OSM), Garranes normal (georeferenced from the literature)."),
    ]
    ty = by + 96
    for line in lines:
        block, ty = vu.svg_text_block(x + 20, ty, line, w - 40, size=13.5, line_h=19)
        parts.append(block)
        ty += 4
    # bridge: P4 + P5, then Z6
    y = TOP_Y + h + 24
    parts.append(vu.svg_text(x, y + 12, vu.t(lang, "Die Brücke", "The bridge"), size=14, weight=500,
                             color=vu.TEXT_MUTED))
    t4, s4 = _q(d, "P4", lang)
    t5, _ = _q(d, "P5", lang)
    y = _quote_card(parts, x, y + 22, w, f"{t4} … {t5}.", s4, size=14.5, italic=False,
                    colors={"fill": "#f7f6f2", "stroke": vu.LINE_NEUTRAL}, lang=lang)
    y += 16
    t6, s6 = _q(d, "Z6", lang)
    _quote_card(parts, x, y, w, t6.rstrip("."), "Barbara Fischer · " + s6.split(" · ", 1)[-1],
                size=18, lang=lang)


def _right(parts, d, lang):
    x, w = RIGHT_X, RIGHT_W
    s, osm, fz = d["stone"], d["osm"], d["fuzzy"]
    _panel(parts, x, TOP_Y, w, PANEL_B - TOP_Y, vu.COMMUNITY,
           vu.t(lang, "Community-Hubs · schon heute föderiert", "Community hubs · federated today"),
           vu.t(lang, "CIIC 81 im Wikibase-Ökosystem", "CIIC 81 in the Wikibase ecosystem"))
    # hub node
    hy = TOP_Y + 76
    parts.append(vu.svg_box(x + 20, hy, w - 40, 52, f"Wikidata {s['qid']}", s["label"],
                            fill=vu.COMMUNITY["fill"], stroke=vu.COMMUNITY["stroke"], stroke_width=2))
    rail_x = x + 44
    rows = [
        ("P189", vu.t(lang, "Fundort", "findspot"), f"Wikidata {d['site']['qid']} · Garranes", vu.COMMUNITY, False),
        ("P8168", "FactGrid", f"FactGrid {s['factgrid']}", vu.COMMUNITY, False),
        ("P1325", vu.t(lang, "externe Daten", "external data"), f"Semantic Kompakkt {s['semkompakkt']}",
         vu.COMMUNITY, False),
        ("—", vu.t(lang, "verweist auf Wikidata", "links to Wikidata"),
         f"fuzzy-sl {fz['url'].rsplit(':', 1)[-1]}", vu.COMMUNITY, True),
        ("P2888", vu.t(lang, "exakt gleich", "exact match"), f"lod.ogham.link {s['ogham_lod']}",
         vu.COMMUNITY, False),
        ("P11693", vu.t(lang, "OSM-Node", "OSM node"), f"OSM node {s['osm_node']}", vu.COMMUNITY, False),
        ("P4057", "Irish SMR", f"SMR {s['smr']}", vu.AGGREGATOR, False),
        ("P14097", vu.t(lang, "3D-Modell", "3D model"), "Sketchfab (CC BY-NC-SA)", vu.AGGREGATOR, False),
    ]
    ry0 = hy + 52 + 26
    row_h = 38
    chip_x, chip_w = x + 250, w - 270
    last_y = ry0 + (len(rows) - 1) * row_h + 12
    parts.append(f'<line x1="{rail_x}" y1="{hy + 52}" x2="{rail_x}" y2="{last_y:.1f}" '
                 f'stroke="{vu.ARROW_STROKE}" stroke-width="1.6"/>')
    for i, (pid, plabel, chip, colors, reverse) in enumerate(rows):
        cy = ry0 + i * row_h
        mid = cy + 12
        if reverse:
            parts.append(vu.svg_arrow(chip_x - 2, mid, rail_x + 2, mid, dashed=True))
        else:
            parts.append(vu.svg_arrow(rail_x, mid, chip_x - 2, mid))
        parts.append(vu.svg_text(rail_x + 14, mid - 6, pid, size=11, weight=500, color=vu.TEXT_MUTED))
        parts.append(vu.svg_text(rail_x + 70, mid - 6, plabel, size=11, color=vu.TEXT_MUTED))
        c, _ = vu.svg_chip(chip_x, cy, chip, colors, size=12, h=24, width=chip_w, align="start", pad=12)
        parts.append(c)
    # semantic OSM: the node's tags point back into Wikidata
    oy = last_y + 30
    oh = PANEL_B - 16 - oy
    parts.append(f'<rect x="{x + 20}" y="{oy:.1f}" width="{w - 40}" height="{oh:.1f}" rx="10" '
                 f'fill="#ffffff" stroke="{vu.COMMUNITY["stroke"]}" stroke-width="1.2" stroke-dasharray="6 4"/>')
    parts.append(vu.svg_text(x + 36, oy + 24, vu.t(lang, f"„Semantic OSM“ · Node {osm['id']} (Tags)",
                                                   f"“Semantic OSM” · node {osm['id']} (tags)"),
                             size=13, weight=500, color=vu.COMMUNITY["stroke"]))
    ty = oy + 48
    for k in ("historic", "wikidata", "moved_to:wikidata", "moved_from", "ref:IE:smr"):
        if k in osm["tags"]:
            parts.append(vu.svg_text(x + 36, ty, k, size=12.5, color=vu.TEXT_MUTED))
            parts.append(vu.svg_text(x + 200, ty, osm["tags"][k], size=12.5, weight=500))
            ty += 21
    # the OSM wikidata tag points to a different item than the one used here
    if osm["tags"].get("wikidata") and osm["tags"]["wikidata"] != s["qid"]:
        ty += 10
        parts.append(f'<line x1="{x + 36}" y1="{ty - 12:.1f}" x2="{x + w - 36}" y2="{ty - 12:.1f}" '
                     f'stroke="{vu.COMMUNITY["stroke"]}" stroke-width="0.8" opacity="0.5"/>')
        note = vu.t(lang,
                    f"Der wikidata-Tag zeigt auf {osm['tags']['wikidata']}, nicht auf {s['qid']}. "
                    f"In Wikidata sind beide nur über P1382 „teilweise übereinstimmend“ verbunden – "
                    f"eine Verknüpfung, die dokumentiert werden will.",
                    f"The wikidata tag points to {osm['tags']['wikidata']}, not to {s['qid']}. "
                    f"In Wikidata the two are only linked via P1382 “partially coincident with” – "
                    f"a link that needs documenting.")
        block, _ = vu.svg_text_block(x + 36, ty + 8, note, w - 72, size=12.5, line_h=17,
                                     color=vu.TEXT_DARK)
        parts.append(block)


def _floor(parts, lang):
    x, w = LEFT_X, vu.CONTENT_X1 - LEFT_X
    y, h = FLOOR_Y, FLOOR_H
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#f4f3ef" '
                 f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1.4"/>')
    for cx, colors in ((LEFT_X + LEFT_W / 2, vu.GND), (MID_X + MID_W / 2, vu.QUOTE),
                       (RIGHT_X + RIGHT_W / 2, vu.COMMUNITY)):
        parts.append(vu.svg_arrow(cx, PANEL_B + 2 if cx != MID_X + MID_W / 2 else PANEL_B + 2,
                                  cx, y - 2, stroke=colors["stroke"]))
    parts.append(vu.svg_text(x + w / 2, y + 42, vu.t(lang, "Gemeinsamer Boden: Wikibase · Linked Open Data · CC0",
                                                     "Common ground: Wikibase · Linked Open Data · CC0"),
                             size=21, weight=500, anchor="middle"))
    parts.append(vu.svg_text(LEFT_X + 20, y + 84, vu.t(lang, "GND: CC0, SPARQL, Wikibase-Erprobung seit 2019",
                                                       "GND: CC0, SPARQL, trialling Wikibase since 2019"),
                             size=14, color=vu.GND["stroke"], weight=500))
    parts.append(vu.svg_text(LEFT_X + 20, y + 106, vu.t(lang, "c’t 19/2026, S. 120", "c’t 19/2026, p. 120"),
                             size=11.5, color=vu.TEXT_MUTED))
    parts.append(vu.svg_text(vu.CONTENT_X1 - 20, y + 84,
                             vu.t(lang, "Wikidata (CC0) · FactGrid · Semantic Kompakkt · fuzzy-sl",
                                  "Wikidata (CC0) · FactGrid · Semantic Kompakkt · fuzzy-sl"),
                             size=14, color=vu.COMMUNITY["stroke"], weight=500, anchor="end"))
    parts.append(vu.svg_text(vu.CONTENT_X1 - 20, y + 106,
                             vu.t(lang, "+ CrossyBase (geplant, NFDI4Objects TRAIL 2.5)",
                                  "+ CrossyBase (planned, NFDI4Objects TRAIL 2.5)"),
                             size=12.5, color=vu.COMMUNITY["stroke"], anchor="end"))


def build(lang: str = "de") -> list[str]:
    d = load()
    parts = [vu.svg_open(vu.t(lang, "Beide Seiten bewegen sich auf Wikibase zu",
                              "Both sides are moving towards Wikibase"))]
    _left(parts, d, lang)
    _middle(parts, d, lang)
    _right(parts, d, lang)
    _floor(parts, lang)
    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"wikibase-konvergenz.{lang}", "\n".join(parts), zoom=1.5)


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
