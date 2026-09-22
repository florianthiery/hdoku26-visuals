#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_03_nische_hub.py -- the niche is the hub
==============================================

Figure 3 of the talk "Orte ohne Normdatensatz?". The GND itself places
GNDplus as "eine Nische zwischen der großen weiten Datenwelt wie Wikidata und
den strengen, eingekasteten Normdaten der Kultureinrichtungen" (Barbara
Fischer, c't 19/2026, p. 120). This figure takes that axis as its top band
and shows what the niche of the community hubs is: not "the GND lacks
something", but identifiers converging, data attached to them, and the
people who put it there.

* top    -- Fischer's axis (Z5) with the three positions on it;
* left   -- mini knowledge graph A, Garranes: the townland item and the Ogham
  site item are not linked to each other directly -- they meet at the shared
  Logainm ID 8299 (a terminology junction in miniature); OSM relation,
  FactGrid, townlands.ie, the CIIC reference and the stone hang off them; the
  GND record (the ringfort in the same townland) is a dashed node that could
  be connected once the ringfort has an item of its own;
* right  -- mini knowledge graph B, St. Lachtain's Well, Freshford: the
  Wikidata item and the OSM way point at each other, and agree on the SMR
  number and on the saint the well is named after; plus what no authority
  file would model (what the well is said to cure, the bishop linked to it,
  22 described-by sources incl. the Schools' Collection); the GND knows only
  a Freshford in Somerset;
* bottom -- who entered the data (OSM user, date, survey), Fischer's own
  standards (Z7 excerpt, Z9), and the foundation: responsibility per
  statement -- the Crossys (NFDI4Objects TRAIL 2.5).

Sources: ``wikidata/Q104295278.json``, ``Q69385525.json``, ``Q121840779.json``,
``osm/node_11071361392.xml``, ``osm/way_935503837.xml``, ``manual/labels.yaml``,
``manual/vgi.yaml``, ``ct/quotes.yaml`` (Z5, Z7, Z9).

Writes: img/03-nische-hub/nische-hub.{de,en}.{svg,png}
Run standalone: ``python py/step_03_nische_hub.py``
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET

import yaml

import hdoku26_visuals_utils as vu

OUT = vu.OUT_DIRS["03-nische-hub"]
RAW = vu.DATA_RAW

AXIS_Y = 50
PANEL_Y, PANEL_B = 205, 725
A_X, A_W = 60, 820
B_X, B_W = 910, 780
LOW_Y, LOW_B = 745, 880
BASE_Y, BASE_B = 898, 950

UNC = {"fill": vu.UNCERTAIN_FILL, "stroke": vu.UNCERTAIN_STROKE}
DE_LABELS = {"blindness": "Blindheit", "eye infection": "Augeninfektion"}


# --------------------------------------------------------------------------- #
# Data
# --------------------------------------------------------------------------- #
def _wd(qid: str) -> dict:
    return json.loads((RAW / "wikidata" / f"{qid}.json").read_text(encoding="utf-8"))["entities"][qid]


def _vals(entity: dict, prop: str) -> list:
    out = []
    for c in entity["claims"].get(prop, []):
        v = c["mainsnak"]["datavalue"]["value"]
        out.append(v["id"] if isinstance(v, dict) and "id" in v else v)
    return out


def _ref_items(entity: dict, prop: str) -> list[str]:
    """QIDs used as 'stated in' (P248) in the references of a property."""
    seen: list[str] = []
    for c in entity["claims"].get(prop, []):
        for ref in c.get("references", []):
            for snak in ref["snaks"].get("P248", []):
                q = snak["datavalue"]["value"]["id"]
                if q not in seen:
                    seen.append(q)
    return seen


def _osm(path: str) -> dict:
    el = ET.parse(RAW / "osm" / path).getroot()[0]
    return {"type": el.tag, "id": el.get("id"), "user": el.get("user"),
            "changeset": el.get("changeset"), "date": el.get("timestamp")[:10],
            "tags": {t.get("k"): t.get("v") for t in el.findall("tag")}}


def load() -> dict:
    town, site, well = _wd("Q104295278"), _wd("Q69385525"), _wd("Q121840779")
    labels = yaml.safe_load((RAW / "manual" / "labels.yaml").read_text(encoding="utf-8"))
    vgi = yaml.safe_load((RAW / "manual" / "vgi.yaml").read_text(encoding="utf-8"))
    quotes = yaml.safe_load((RAW / "ct" / "quotes.yaml").read_text(encoding="utf-8"))
    duchas = sum(json.dumps(c).count("duchas.ie") for c in well["claims"]["P1343"])
    return {
        "town": {"qid": town["id"], "ga": town["labels"]["ga"]["value"],
                 "logainm": _vals(town, "P5097")[0], "osm_rel": _vals(town, "P402")[0]},
        "site": {"qid": site["id"], "logainm": _vals(site, "P5097")[0],
                 "factgrid": _vals(site, "P8168")[0], "townlands": _vals(site, "P973")[0],
                 "refs": _ref_items(site, "P131")},
        "well": {"qid": well["id"], "label": well["labels"]["en"]["value"],
                 "ga": well["labels"]["ga"]["value"],
                 "osm_way": _vals(well, "P10689")[0], "smr": _vals(well, "P4057")[0].rstrip("-"),
                 "named_after": _vals(well, "P138")[0], "cures": _vals(well, "P2175"),
                 "person": _vals(well, "P3342")[0], "described_by": len(well["claims"]["P1343"]),
                 "duchas_refs": duchas, "sitelinks": sorted(well["sitelinks"])},
        "node": _osm("node_11071361392.xml"),
        "way": _osm("way_935503837.xml"),
        "labels": labels, "vgi": vgi, "quotes": quotes,
    }


def _date(iso: str, lang: str) -> str:
    y, m, d = iso.split("-")
    return f"{d}.{m}.{y}" if lang == "de" else iso


# --------------------------------------------------------------------------- #
# Top: Fischer's axis
# --------------------------------------------------------------------------- #
def _axis(parts, d, lang):
    q = d["quotes"]["Z5"]
    x0, x1, y = 250, 1500, AXIS_Y + 78
    xm = (x0 + x1) / 2
    parts.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{vu.LINE_NEUTRAL}" stroke-width="2"/>')
    stops = [
        (x0, vu.GND, vu.t(lang, "„den strengen, eingekasteten Normdaten“", "“the strict, boxed-in authority data”"),
         vu.t(lang, "GND", "GND")),
        (xm, {"fill": "#ffffff", "stroke": vu.GND["stroke"]},
         vu.t(lang, "GNDplus: „eine Nische“", "GNDplus: “a niche”"), vu.t(lang, "laut DNB", "according to the DNB")),
        (x1, vu.COMMUNITY, vu.t(lang, "„der großen weiten Datenwelt wie Wikidata“", "“the big wide data world such as Wikidata”"),
         "Wikidata · OpenStreetMap"),
    ]
    for x, colors, top, below in stops:
        parts.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{colors["fill"]}" stroke="{colors["stroke"]}" '
                     f'stroke-width="2.4"/>')
        parts.append(vu.svg_text(x, y - 24, top, size=15, weight=500, anchor="middle", italic=True))
        parts.append(vu.svg_text(x, y + 32, below, size=12.5, color=vu.TEXT_MUTED, anchor="middle"))
    # our reading: the hub niche on the open side
    bx0, bx1, by = xm + 120, x1 + 150, y + 48
    parts.append(f'<path d="M {bx0} {by - 6} L {bx0} {by} L {bx1} {by} L {bx1} {by - 6}" fill="none" '
                 f'stroke="{vu.COMMUNITY["stroke"]}" stroke-width="2"/>')
    parts.append(vu.svg_text((bx0 + bx1) / 2 + 10, by + 20,
                             vu.t(lang, "Nische der Community-Hubs: die Drehscheibe, an der Kennungen zusammenlaufen",
                                  "Niche of the community hubs: the turntable where identifiers converge"),
                             size=13.5, weight=500, color=vu.COMMUNITY["stroke"], anchor="middle"))
    who = f"{q['speaker']} · " + vu.quote_source(q, lang).split(" · ", 1)[-1]
    parts.append(vu.svg_text(vu.MARGIN_X, AXIS_Y + 18, vu.t(lang, "Die Achse der DNB", "The DNB's own axis"),
                             size=12.5, weight=500, color=vu.TEXT_MUTED))
    parts.append(vu.svg_text(vu.MARGIN_X, AXIS_Y + 36, who, size=11.5, color=vu.QUOTE["stroke"]))


# --------------------------------------------------------------------------- #
# Panel A: Garranes -- two items meeting at one external identifier
# --------------------------------------------------------------------------- #
def _panel_a(parts, d, lang):
    t, s, node = d["town"], d["site"], d["node"]
    parts.append(vu.svg_panel(A_X, PANEL_Y, A_W, PANEL_B - PANEL_Y, vu.COMMUNITY,
                              vu.t(lang, "Mini-Wissensgraph A", "Mini knowledge graph A"),
                              vu.t(lang, "Garranes: zwei Items, eine gemeinsame Kennung",
                                   "Garranes: two items, one shared identifier")))
    ry, bh = PANEL_Y + 92, 60
    lx, lw = A_X + 20, 220
    rx, rw = A_X + 460, A_W - 480
    jx, jy, jr = A_X + 350, ry + bh / 2, 50
    parts.append(vu.svg_box(lx, ry, lw, bh, "Townland Garranes", f"{t['ga']} · {t['qid']}",
                            fill=vu.COMMUNITY["fill"], stroke=vu.COMMUNITY["stroke"]))
    parts.append(vu.svg_box(rx, ry, rw, bh, vu.t(lang, "Ogham-Fundstelle Garranes", "Ogham findspot Garranes"),
                            f"Wikidata {s['qid']}",
                            fill=vu.COMMUNITY["fill"], stroke=vu.COMMUNITY["stroke"]))
    parts.append(vu.svg_hash_node(jx, jy, jr, f"Logainm {t['logainm']}", vu.t(lang, "Treffpunkt", "meeting point"),
                                  fill="#ffffff", stroke=vu.COMMUNITY["stroke"]))
    parts.append(vu.svg_arrow_labeled(lx + lw + 2, jy, jx - jr - 3, jy, "P5097", font_size=11))
    parts.append(vu.svg_arrow_labeled(rx - 2, jy, jx + jr + 3, jy, "P5097", font_size=11))

    def rail_list(x_rail, x_chip, w_chip, y0, rows):
        last = y0 + (len(rows) - 1) * 38 + 12
        parts.append(f'<line x1="{x_rail}" y1="{ry + bh}" x2="{x_rail}" y2="{last:.1f}" '
                     f'stroke="{vu.ARROW_STROKE}" stroke-width="1.6"/>')
        for i, (pid, label, colors, reverse) in enumerate(rows):
            cy = y0 + i * 38
            mid = cy + 12
            if reverse:
                parts.append(vu.svg_arrow(x_chip - 2, mid, x_rail + 2, mid))
            else:
                parts.append(vu.svg_arrow(x_rail, mid, x_chip - 2, mid))
            parts.append(vu.svg_text(x_rail + 8, mid - 6, pid, size=10.5, weight=500, color=vu.TEXT_MUTED))
            c, _ = vu.svg_chip(x_chip, cy, label, colors, size=12, h=24, width=w_chip, align="start", pad=12)
            parts.append(c)

    y0 = ry + bh + 30
    rail_list(lx + 22, lx + 70, lw - 50, y0, [("P402", f"OSM rel. {t['osm_rel']}", vu.COMMUNITY, False)])
    parts.append(vu.svg_text(lx + 70, y0 + 46, vu.t(lang, "Townland-Fläche in OSM", "townland polygon in OSM"),
                             size=12, color=vu.TEXT_MUTED))
    refs = {"Q70256237": "CIIC Vol. 1 (1945)", "Q70851365": "Irish Townlands"}
    assert all(r in refs for r in s["refs"]), s["refs"]
    rail_list(rx + 18, rx + 72, rw - 72, y0, [
        ("P8168", f"FactGrid {s['factgrid']}", vu.COMMUNITY, False),
        ("P973", "townlands.ie", vu.COMMUNITY, False),
        *[("P248", vu.t(lang, f"Beleg: {refs[q]}", f"ref.: {refs[q]}"), vu.AGGREGATOR, False) for q in s["refs"]],
        ("P189", vu.t(lang, "Stein CIIC 81 · Q130529871", "stone CIIC 81 · Q130529871"), vu.COMMUNITY, True),
    ])
    # GND as a dashed, connectable node + the reading of the graph
    gy = PANEL_B - 20 - 78
    gx, gw = A_X + 20, 420
    parts.append(f'<rect x="{gx}" y="{gy}" width="{gw}" height="78" rx="10" fill="#ffffff" '
                 f'stroke="{vu.GND["stroke"]}" stroke-width="1.4" stroke-dasharray="6 4"/>')
    parts.append(vu.svg_text(gx + 16, gy + 24, "GND 1248049489 „Garranes“" if lang == "de"
                             else "GND 1248049489 “Garranes”", size=13.5, weight=500, color=vu.GND["stroke"]))
    block, _ = vu.svg_text_block(gx + 16, gy + 45, vu.t(
        lang, "Ringwall Lisnacaheragh im selben Townland – noch ohne eigenes Item. Anschluss: Item anlegen, P227 setzen.",
        "Lisnacaheragh ringfort in the same townland – no item of its own yet. To connect: create the item, add P227."),
        gw - 32, size=12, line_h=16)
    parts.append(block)
    block, _ = vu.svg_text_block(gx + gw + 24, gy + 22, vu.t(
        lang, "Townland und Fundstelle sind in Wikidata nicht direkt verknüpft – sie treffen sich an der "
              "nationalen Kennung Logainm 8299: eine Terminologie-Junction im Kleinen.",
        "Townland and findspot are not linked directly in Wikidata – they meet at the national identifier "
        "Logainm 8299: a terminology junction in miniature."),
        A_W - gw - 64, size=12.5, line_h=17, italic=True, color=vu.COMMUNITY["stroke"])
    parts.append(block)


# --------------------------------------------------------------------------- #
# Panel B: St. Lachtain's Well -- Wikidata and OSM pointing at each other
# --------------------------------------------------------------------------- #
def _panel_b(parts, d, lang):
    w_, way, lab = d["well"], d["way"], d["labels"]
    parts.append(vu.svg_panel(B_X, PANEL_Y, B_W, PANEL_B - PANEL_Y, vu.COMMUNITY,
                              vu.t(lang, "Mini-Wissensgraph B", "Mini knowledge graph B"),
                              vu.t(lang, "St. Lachtain’s Well: Wikidata und OSM verweisen aufeinander",
                                   "St. Lachtain’s Well: Wikidata and OSM point at each other")))
    hy = PANEL_Y + 76
    parts.append(vu.svg_box(B_X + 20, hy, B_W - 40, 50, f"Wikidata {w_['qid']}",
                            f"{w_['label']} · {w_['ga']}",
                            fill=vu.COMMUNITY["fill"], stroke=vu.COMMUNITY["stroke"], stroke_width=2))
    rail = B_X + 44
    chip_x, chip_w = B_X + 250, B_W - 270

    def lbl(q):
        name = lab[q]["label"]
        return DE_LABELS.get(name, name) if lang == "de" else name

    both = vu.t(lang, "auch im OSM-Tag", "also in the OSM tag")
    tags = way["tags"]
    rows = [
        ("P10689", vu.t(lang, "OSM-Way", "OSM way"), f"OSM way {w_['osm_way']}",
         vu.t(lang, "wikidata=" + tags["wikidata"], "wikidata=" + tags["wikidata"]), True),
        ("P4057", "Irish SMR", f"SMR {w_['smr']}",
         both if tags.get("ref:IE:smr", "").rstrip("-") == w_["smr"] else "", False),
        ("P138", vu.t(lang, "Namensgeber", "named after"), f"{lab[w_['named_after']]['label']}",
         both if tags.get("name:etymology:wikidata") == w_["named_after"] else "", False),
        ("P2175", vu.t(lang, "heilt (Überlieferung)", "said to cure"), ", ".join(lbl(q) for q in w_["cures"]),
         "", False),
        ("P3342", vu.t(lang, "Person", "person"), vu.t(lang, f"{lab[w_['person']]['label']}, Bischof von Ossory",
                                                        f"{lab[w_['person']]['label']}, bishop of Ossory"), "", False),
        ("P1343", vu.t(lang, "beschrieben in", "described by"),
         vu.t(lang, f"{w_['described_by']} Quellen, u. a. dúchas.ie", f"{w_['described_by']} sources, incl. dúchas.ie"),
         vu.t(lang, "mit Seitenangaben", "with page numbers"), False),
        ("", vu.t(lang, "Medien", "media"), "Wikimedia Commons · Wikipedia (en) · Sketchfab",
         vu.t(lang, "Commons, Sketchfab auch in OSM", "Commons, Sketchfab also in OSM")
         if {"wikimedia_commons", "url:sketchfab"} <= set(tags) else "", False),
    ]
    y0 = hy + 50 + 26
    last = y0 + (len(rows) - 1) * 40 + 12
    parts.append(f'<line x1="{rail}" y1="{hy + 50}" x2="{rail}" y2="{last:.1f}" '
                 f'stroke="{vu.ARROW_STROKE}" stroke-width="1.6"/>')
    for i, (pid, plabel, chip, note, bidi) in enumerate(rows):
        cy = y0 + i * 40
        mid = cy + 12
        if bidi:
            parts.append(f'<line x1="{rail + 2}" y1="{mid}" x2="{chip_x - 2}" y2="{mid}" stroke="{vu.ARROW_STROKE}" '
                         f'stroke-width="1.6" marker-start="url(#arrow)" marker-end="url(#arrow)"/>')
        else:
            parts.append(vu.svg_arrow(rail, mid, chip_x - 2, mid))
        parts.append(vu.svg_text(rail + 12, mid - 6, pid, size=10.5, weight=500, color=vu.TEXT_MUTED))
        parts.append(vu.svg_text(rail + 66, mid - 6, plabel, size=10.5, color=vu.TEXT_MUTED))
        c, cw = vu.svg_chip(chip_x, cy, chip, vu.COMMUNITY, size=12, h=24, width=chip_w, align="start", pad=12)
        parts.append(c)
        if note:
            parts.append(vu.svg_text(chip_x + chip_w - 12, mid + 0.5, note, size=10.5, color=vu.COMMUNITY["stroke"],
                                     anchor="end", baseline="central", italic=True))
    # GND side
    gnd = d["vgi"]["gnd_freshford"]
    gy = PANEL_B - 20 - 60
    parts.append(f'<rect x="{B_X + 20}" y="{gy}" width="{B_W - 40}" height="60" rx="10" fill="#ffffff" '
                 f'stroke="{vu.GND["stroke"]}" stroke-width="1.4" stroke-dasharray="6 4"/>')
    parts.append(vu.svg_text(B_X + 36, gy + 24, vu.t(lang, f"GND {gnd['gnd']} „Freshford“: {gnd['info']}",
                                                     f"GND {gnd['gnd']} “Freshford”: place in Somerset"),
                             size=13, weight=500, color=vu.GND["stroke"]))
    parts.append(vu.svg_text(B_X + 36, gy + 44, vu.t(lang, "Das irische Freshford und „Lachtain“: kein Treffer.",
                                                     "The Irish Freshford and “Lachtain”: no match."),
                             size=12.5))


# --------------------------------------------------------------------------- #
# Bottom: people, Fischer's standards, the foundation
# --------------------------------------------------------------------------- #
def _bottom(parts, d, lang):
    node, way, vg = d["node"], d["way"], d["vgi"]
    x, w = A_X, A_W
    parts.append(f'<rect x="{x}" y="{LOW_Y}" width="{w}" height="{LOW_B - LOW_Y}" rx="12" fill="#ffffff" '
                 f'stroke="{vu.COMMUNITY["stroke"]}" stroke-width="1.4"/>')
    parts.append(vu.svg_text(x + 20, LOW_Y + 26, vu.t(lang, "Wer die Daten einträgt (Volunteered Geographic Information)",
                                                     "Who puts the data there (volunteered geographic information)"),
                             size=13.5, weight=500, color=vu.COMMUNITY["stroke"]))
    tl = vg["townland_garranes_osm"]
    rows = [
        (vu.t(lang, "OSM-Node CIIC 81", "OSM node CIIC 81"), node["user"],
         f"{_date(node['date'], lang)} · source={node['tags'].get('source', '')}"),
        (vu.t(lang, "OSM-Way St. Lachtain’s Well", "OSM way St. Lachtain’s Well"), way["user"],
         f"{_date(way['date'], lang)} · survey {_date(way['tags']['survey:date'], lang)}"),
        (vu.t(lang, "Townland Garranes in OSM", "Townland of Garranes in OSM"), tl["user"],
         vu.t(lang, f"seit {_date(tl['added'], lang)}", f"since {_date(tl['added'], lang)}")),
        (vg["wikiproject_holywells"]["label"], "Wikidata", "Citizen Science"),
    ]
    for i, (what, who, when) in enumerate(rows):
        cx = x + 20 + (i % 2) * (w / 2)
        cy = LOW_Y + 56 + (i // 2) * 40
        parts.append(vu.svg_text(cx, cy, what, size=12.5, color=vu.TEXT_MUTED))
        parts.append(vu.svg_text(cx, cy + 18, f"{who} · {when}", size=13.5, weight=500))

    # Fischer's standards
    bx = B_X
    q7, q9 = d["quotes"]["Z7"], d["quotes"]["Z9"]
    z7 = vu.t(lang, "… Es geht schlicht um Verantwortung und Vertrauen.",
              "… It is simply about responsibility and trust.")
    z9 = vu.t(lang, "Man muss immer wissen, woher die Daten stammen", "You always have to know where the data comes from")
    half = (B_W - 16) / 2
    qsize = min(vu.quote_fill_size(t_, half, LOW_B - LOW_Y, lang, max_size=26) for t_ in (z7, z9))
    for i, (text, q) in enumerate(((z7, q7), (z9, q9))):
        src = f"{q['speaker']} · " + vu.quote_source(q, lang).split(" · ", 1)[-1]
        parts.append(vu.svg_quote_fill(bx + i * (half + 16), LOW_Y, half, LOW_B - LOW_Y, text, src, lang,
                                       size=qsize))

    # foundation
    parts.append(f'<rect x="{vu.MARGIN_X}" y="{BASE_Y}" width="{vu.CONTENT_X1 - vu.MARGIN_X}" '
                 f'height="{BASE_B - BASE_Y}" rx="10" fill="#f4f3ef" stroke="{vu.LINE_NEUTRAL}" stroke-width="1.4"/>')
    parts.append(vu.svg_text(vu.MARGIN_X + 20, BASE_Y + 27, vu.t(
        lang, "Verantwortung pro Aussage: jede Verknüpfung mit Quelle, Methode und Person – dokumentiert in den Crossys (NFDI4Objects TRAIL 2.5)",
        "Responsibility per statement: every link with source, method and person – documented in the Crossys (NFDI4Objects TRAIL 2.5)"),
        size=15, weight=500, baseline="central"))
    parts.append(vu.svg_text(vu.CONTENT_X1 - 20, BASE_Y + 27, vu.t(
        lang, "Pflegefall: wikidata=Q106680733 am Stein (Grafik 2)",
        "needs care: wikidata=Q106680733 on the stone (fig. 2)"),
        size=12, color=vu.UNCERTAIN_STROKE, anchor="end", baseline="central", italic=True))


def build(lang: str = "de") -> list[str]:
    d = load()
    parts = [vu.svg_open(vu.t(lang, "Die Nische ist der Hub", "The niche is the hub"))]
    _axis(parts, d, lang)
    _panel_a(parts, d, lang)
    _panel_b(parts, d, lang)
    _bottom(parts, d, lang)
    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"nische-hub.{lang}", "\n".join(parts), zoom=1.5)


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
