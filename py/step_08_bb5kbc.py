#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_08_bb5kbc.py -- case study bb-5kbc: two findspots, one culture, one border
===============================================================================

The fourth case study on the grid recorded in PRIMER.md (A4):

  A  ``rollen``          who holds what -- and how far down each hub reaches on
                         either side of the German-Polish border
  B  ``ortskette``       the chain of places, with the predecessor unit beside
                         it: this is the case study in which the GND's own
                         strength, dating a place, becomes visible
  C  ``graph-dahinter``  what hangs off the findspot -- a sherd with its own
                         Wikidata item on one side, and a culture named after
                         the place on the other

Both findspots belong to the same culture (Stichbandkeramik) and lie about
500 km apart. Seelow 20 is georeferenced from the Brandenburg heritage
authority's own database (``genauigkeit_m = 0``); Jordansmühl / Jordanów
Śląski is georeferenced by reading the centre of the municipality off a
printed map of 1930 (3 000 m) -- so the whole localisation of the Polish
findspot rests on a Geografikum, which is what this talk is about.

The GND covers the German chain completely and the Polish chain only at
voivodeship level. It does, however, hold the *culture* named after
Jordansmühl, whose definition names the findspot in running text -- while the
place itself has no record. Figure C closes on that.

Inputs (all under ``data/raw/``):

* ``bb5kbc/fst_wgs84.csv``      the 540 enriched findspots; every count in
                                figure A is counted from this table
* ``wikidata/*.json``           the places of both chains, the two sherds, the
                                two publications and the two vocabulary items
* ``osm/boundaries-seelow.geojson``, ``-jordanow.geojson``, ``-bb-ds.geojson``
                                district and municipality areas plus the two
                                federal-state/voivodeship outlines
* ``manual/bb5kbc.yaml``        GND numbers with their entity types and dates,
                                the two chains, map windows and the wording of
                                the GND definition quoted in figure C
"""

from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "py"))

import yaml  # noqa: E402

import hdoku26_visuals_utils as vu  # noqa: E402

RAW = vu.DATA_RAW
OUT = vu.OUT_DIRS["08-bb-5kbc"]

GND, WD, AGG, OSM = vu.GND, vu.COMMUNITY, vu.AGGREGATOR, vu.OSM
UNC = {"fill": vu.UNCERTAIN_FILL, "stroke": vu.UNCERTAIN_STROKE}
OPEN = {"fill": "#ffffff", "stroke": vu.OPEN_STROKE}
T = vu.svg_text

LEVELS = ("GEMEINDE", "KREIS", "BUNDESLAND", "LAND")


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
def _rows() -> list[dict]:
    with (RAW / "bb5kbc" / "fst_wgs84.csv").open(encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def _coverage(rows: list[dict]) -> dict:
    """How far down each hub reaches, per level and per country -- counted over
    *distinct places*, not over findspots, so that a village with twenty
    findspots does not count twenty times."""
    column = {"GEMEINDE": "gemeinde", "KREIS": "kreis", "BUNDESLAND": "bundesland",
              "LAND": "land"}
    out: dict[str, dict[str, dict[str, int]]] = {}
    for level in LEVELS:
        out[level] = {}
        for country in ("Deutschland", "Polen"):
            selected = [r for r in rows if r["land"] == country]
            def places(suffix: str) -> set[str]:
                return {r[column[level]] for r in selected if r[f"{level}_{suffix}"].strip()}
            out[level][country] = {
                "n": len(places("QID")),
                "tgn": len(places("TGN")),
                "idai": len(places("IDAI")),
                "osm": len(places("OSM_Relation")),
                "geonames": len(places("GeoNames")),
            }
    return out


def _totals(rows: list[dict]) -> dict:
    de = [r for r in rows if r["land"] == "Deutschland"]
    pl = [r for r in rows if r["land"] == "Polen"]
    methods: dict[str, int] = {}
    for r in rows:
        methods[r["methode"]] = methods.get(r["methode"], 0) + 1
    return {
        "n": len(rows), "de": len(de), "pl": len(pl),
        "sbk": sum(1 for r in rows if r["kultur"] == "SBK"),
        "methods": methods,
        "exact": sum(1 for r in rows if r["genauigkeit_m"] == "0"),
        "centroid": sum(1 for r in rows if r["methode"] == "Mittelpunkt der Gemeinde"),
        "sherds": sum(1 for r in rows if r["sherd"].strip()),
        "perio": sum(1 for r in rows if r["dating_perio.do"].strip()),
    }


def load() -> dict:
    manual = yaml.safe_load((RAW / "manual" / "bb5kbc.yaml").read_text(encoding="utf-8"))
    rows = _rows()
    by_cat: dict[str, list[dict]] = {}
    for r in rows:
        by_cat.setdefault(r["katalognr"], []).append(r)

    seelow = next(r for r in rows if r["katalognr"] == "55005" and r["gemeinde"] == "Seelow")
    jordan = next(r for r in rows if r["fst_name"].startswith("Jordansmühl"))
    same_point = [r for r in rows
                  if r["gemeinde"] == jordan["gemeinde"]
                  and (r["wgs84_x"], r["wgs84_y"]) == (jordan["wgs84_x"], jordan["wgs84_y"])]
    nearby = [r for r in rows
              if r["gemeinde"] == jordan["gemeinde"] and r not in same_point]

    d = {
        "m": manual,
        "rows": rows,
        "row": {"seelow": seelow, "jordansmuehl": jordan},
        "same_point": same_point,
        "nearby": nearby,
        "cov": _coverage(rows),
        "tot": _totals(rows),
        "wd": {qid: vu.load_wikidata(qid) for qid in
               ("Q587069", "Q6181", "Q1208", "Q2191877", "Q715974", "Q54150",
                "Q139304626", "Q139304635", "Q139477253", "Q139477652",
                "Q486972", "Q59496158", "Q959782")},
        "geo": {"seelow": vu.load_geojson("boundaries-seelow"),
                "jordanow": vu.load_geojson("boundaries-jordanow"),
                "wide": vu.load_geojson("boundaries-bb-ds")},
    }
    d["point"] = {key: (float(r["wgs84_x"]), float(r["wgs84_y"]))
                  for key, r in d["row"].items()}
    d["km"] = vu.haversine_km(d["point"]["seelow"][1], d["point"]["seelow"][0],
                              d["point"]["jordansmuehl"][1], d["point"]["jordansmuehl"][0])
    return d


def _p227(entity: dict) -> str | None:
    claims = entity["claims"].get("P227")
    return claims[0]["mainsnak"]["datavalue"]["value"] if claims else None


# --------------------------------------------------------------------------- #
# Figure A -- who holds what
# --------------------------------------------------------------------------- #
def _fig_a(d: dict, lang: str) -> str:
    m, cov, tot = d["m"], d["cov"], d["tot"]
    se, jo = d["row"]["seelow"], d["row"]["jordansmuehl"]
    probe, terms = m["gnd_probe"], m["terms"]
    de = lang == "de"
    p = [vu.svg_open(vu.t(lang, "Wer hält was: zwei Fundstellen derselben Kultur, zwei Länder",
                          "Who holds what: two findspots of one culture, two countries"))]
    LX = vu.MARGIN_X
    C1, C2, CW = vu.CASE_C1, vu.CASE_C2, vu.CASE_CW

    for cx, site, row, note_de, note_en, colors in (
            (C1, m["sites"]["seelow"], se, site_note := None, None, WD),
            (C2, m["sites"]["jordansmuehl"], jo, None, None, OPEN)):
        p.append(vu.case_header(
            cx, site["title_de" if de else "title_en"],
            vu.t(lang, f"Katalognr. {row['katalognr']} · {row['kultur']} · "
                       f"{row['fundstellenart']} · {row['quellen_typ']}",
                 f"catalogue no. {row['katalognr']} · {row['kultur']} · "
                 f"{row['fundstellenart']} · {row['quellen_typ']}"),
            vu.t(lang, f"{site['claim_de']} · ±{row['genauigkeit_m']} m",
                 f"{site['claim_en']} · ±{row['genauigkeit_m']} m"), colors))

    p.append(f'<line x1="{LX}" y1="{vu.CASE_RULE_Y}" x2="{C2 + CW}" y2="{vu.CASE_RULE_Y}" '
             f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')

    rows = [
        ("GND", GND, 174, 140, [
            ("ok", vu.t(lang, "die Kette ist durchgehend verzeichnet",
                        "the chain is recorded all the way up"), [
                (vu.t(lang, "Seelow · GND 4340023-1 · gik · Koordinate im Satz, Quelle GeoNames",
                      "Seelow · GND 4340023-1 · gik · coordinate in the record, source GeoNames"),
                 "gnd"),
                (vu.t(lang, "Märkisch-Oderland · GND 4336493-7 · gik + giv · Beginn 1992",
                      "Märkisch-Oderland · GND 4336493-7 · gik + giv · from 1992"), "gnd"),
                (vu.t(lang, "Brandenburg · GND 4007955-7 — alle drei in Wikidata über P227",
                      "Brandenburg · GND 4007955-7 — all three linked from Wikidata via P227"),
                 "gnd"),
            ]),
            ("none", vu.t(lang, "der Ort fehlt, der Begriff ist da",
                          "the place is missing, the term is not"), [
                (vu.t(lang, probe["jordanow_de"], probe["jordanow_en"]), "open"),
                (vu.t(lang, f"{terms['jordanow']['name_de']} · GND {terms['jordanow']['gnd']} · "
                            f"nennt den Fundort im Definitionstext",
                      f"{terms['jordanow']['name_en']} · GND {terms['jordanow']['gnd']} · "
                      f"names the findspot in its definition"), "gnd"),
                (vu.t(lang, "Woiwodschaft Niederschlesien · GND 4596748-9 — erst drei Ebenen höher",
                      "Lower Silesian Voivodeship · GND 4596748-9 — only three levels up"), "gnd"),
            ]),
        ]),
        (vu.t(lang, "Wikidata / Wikibase", "Wikidata / Wikibase"), WD, 322, 168, [
            ("ok", vu.t(lang, "bis unter die Fundstelle: zwei Scherben mit eigenem Item",
                        "below the findspot: two sherds with items of their own"), [
                ("Q587069 · P227 · P402 rel 1332928 · P1667 TGN 1037726", "ok"),
                (vu.t(lang, f"Q139477253 · Q139477652 · P2596 Kultur · P18 Foto auf Commons",
                      f"Q139477253 · Q139477652 · P2596 culture · P18 photo on Commons"), "ok"),
                (vu.t(lang, f"Grabungsbericht {m['publications']['voelker']['wikidata']} · "
                            f"{m['sites']['seelow']['activity']}",
                      f"excavation report {m['publications']['voelker']['wikidata']} · "
                      f"{m['sites']['seelow']['activity']}"), "ok"),
                (vu.t(lang, "Fundstellenart Q486972 · Entdeckung Q959782 — beide mit P227",
                      "site type Q486972 · discovery Q959782 — both carry P227"), "ok"),
            ]),
            ("ok", vu.t(lang, "die Gemeinde ist da, darüber wird es dünn",
                        "the municipality is there, above it things thin out"), [
                ("Q2191877 · P402 rel 3049634 · GeoNames 7531990", "ok"),
                (vu.t(lang, "kein P227, kein TGN — weder bei der Gemeinde noch beim Powiat",
                      "no P227, no TGN — neither for the gmina nor for the powiat"), "open"),
                (vu.t(lang, "zwei P625-Koordinaten am selben Item",
                      "two P625 coordinates on the same item"), "unc"),
                (vu.t(lang, f"von Richthofen 1930 · {m['publications']['richthofen']['wikidata']} · "
                            f"{m['publications']['richthofen']['kind_de']}",
                      f"von Richthofen 1930 · {m['publications']['richthofen']['wikidata']} · "
                      f"{m['publications']['richthofen']['kind_en']}"), "ok"),
            ]),
        ]),
        ("OpenStreetMap", OSM, 498, 140, [
            ("ok", vu.t(lang, "drei Ebenen, drei Relationen", "three levels, three relations"), [
                ("rel 1332928 Seelow · admin_level=8", "ok"),
                ("rel 318248 Märkisch-Oderland · admin_level=6", "ok"),
                ("rel 62504 Brandenburg · admin_level=4", "ok"),
            ]),
            ("ok", vu.t(lang, "genauso vollständig — ohne GND und ohne TGN",
                        "just as complete — without a GND or a TGN id"), [
                ("rel 3049634 gmina Jordanów Śląski · admin_level=7", "ok"),
                ("rel 451517 powiat wrocławski · admin_level=6", "ok"),
                ("rel 224457 województwo dolnośląskie · admin_level=4", "ok"),
            ]),
        ]),
        (vu.t(lang, "Fachdaten", "research data"), AGG, 646, 140, [
            ("ok", vu.t(lang, "Behördendatenbank, auf Anfrage",
                        "an authority database, on request"), [
                (f"{se['quelle_georef']} · {se['methode']}", "ok"),
                (vu.t(lang, f"drei ¹⁴C-Daten · {se['dating_certainty_start']} · perio.do",
                      f"three ¹⁴C dates · {se['dating_certainty_start']} · perio.do"), "ok"),
                (vu.t(lang, f"„{se['methodenbeschr']}“",
                      f"“{m['sites']['seelow']['method_en']}”"), "unc"),
            ]),
            ("ok", vu.t(lang, "gedruckte Karte, Mittelpunkt der Gemeinde",
                        "a printed map, centre of the municipality"), [
                (f"{jo['quelle_georef']} · {jo['methode']}", "ok"),
                (vu.t(lang, f"Datierung {jo['dating_start']} bis {jo['dating_end']} · perio.do",
                      f"dated {jo['dating_start']} to {jo['dating_end']} · perio.do"), "ok"),
                (vu.t(lang, f"„{jo['methodenbeschr']}“",
                      f"“{m['sites']['jordansmuehl']['method_en']}”"), "unc"),
            ]),
        ]),
    ]

    for name, colors, y, h, cells in rows:
        p.append(f'<rect x="{LX}" y="{y}" width="{C2 + CW - LX}" height="{h}" rx="12" '
                 f'fill="{colors["fill"]}" fill-opacity="0.45"/>')
        p.append(f'<rect x="{LX}" y="{y}" width="8" height="{h}" rx="3" fill="{colors["stroke"]}"/>')
        for i, line in enumerate(name.split(" / ")):
            suffix = " /" if i < len(name.split(" / ")) - 1 else ""
            p.append(T(LX + 22, y + 30 + i * 20, line + suffix, size=16, weight=500,
                       color=colors["stroke"]))
        pad = 8
        p.append(vu.case_cell(C1, y + pad, CW, h - 2 * pad, colors, *cells[0]))
        p.append(vu.case_cell(C2, y + pad, CW, h - 2 * pad, colors, *cells[1]))

    p.append(vu.status_legend(LX, vu.CASE_LEGEND_Y, [
        ("ok", vu.t(lang, "vorhanden", "present")),
        ("none", vu.t(lang, "fehlt", "missing")),
        ("open", vu.t(lang, "offen", "open")),
        ("unc", vu.t(lang, "im Datensatz vermerkt", "recorded in the dataset")),
    ]))
    p.append(vu.svg_close())
    return "\n".join(p)


# --------------------------------------------------------------------------- #
# Figure B -- the chain of places
# --------------------------------------------------------------------------- #
def _fig_b(d: dict, lang: str) -> str:
    m = d["m"]
    de = lang == "de"
    p = [vu.svg_open(vu.t(lang, "Ortsketten über eine Grenze hinweg — und über die Zeit",
                          "Chains of places across a border — and across time"))]
    MX, MW = vu.MARGIN_X, 470
    NW, NH = 196, 58
    xs = vu.chain_xs(4, node_w=NW)

    bands = [
        dict(key="seelow", y0=40, map_h=342, collection="seelow", wide="relation/62504",
             outer="relation/318248", inner="relation/1332928",
             locator_label="Brandenburg",
             inner_label_de="Seelow (grün) im Landkreis Märkisch-Oderland",
             inner_label_en="Seelow (green) in the Märkisch-Oderland district",
             aside_from=2, note_x=1305, note_w=355, note_dy=4,
             headline=vu.t(lang, "auf jeder Ebene verzeichnet",
                           "recorded at every level")),
        dict(key="jordansmuehl", y0=520, map_h=322, collection="jordanow",
             wide="relation/224457",
             outer="relation/451517", inner="relation/3049634",
             locator_label=vu.t(lang, "Niederschlesien", "Lower Silesia"),
             inner_label_de="Gmina Jordanów Śląski (grün) im Powiat wrocławski",
             inner_label_en="Gmina Jordanów Śląski (green) in the powiat wrocławski",
             aside_from=3, note_x=825, note_w=560, note_dy=104, aside_dy=112,
             headline=vu.t(lang, "erst die Woiwodschaft hat einen GND-Satz",
                           "only the voivodeship has a GND record")),
    ]

    for band in bands:
        key, y0, map_h = band["key"], band["y0"], band["map_h"]
        site = m["sites"][key]
        collection = d["geo"][band["collection"]]
        outer = vu.geo_feature(collection, band["outer"])
        inner = vu.geo_feature(collection, band["inner"])
        wide = vu.geo_feature(d["geo"]["wide"], band["wide"])

        title = site["title_de" if de else "title_en"]
        p.append(T(MX, y0 + 16, title, size=19, weight=500))
        p.append(T(MX + vu.text_width(title, 19) + 26, y0 + 16, band["headline"],
                   size=13.5, color=vu.TEXT_MUTED))

        markup, project = vu.case_map(MX, y0 + 34, MW, map_h, tuple(m["maps"][key]), f"map-{key}")
        p.append(markup)
        p.append(vu.geo_draw(outer, project, fill=vu.LAND_FILL, stroke=vu.LAND_STROKE, width=1.2))
        p.append(vu.geo_draw(inner, project, fill=OSM["fill"], stroke=OSM["stroke"], width=1.4))
        px, py = project(*d["point"][key])
        p.append(vu.svg_marker(px, py, "1", {"fill": "#ffffff", "stroke": vu.TEXT_DARK}))
        # the Polish side carries two more findspots of the same gmina, one of
        # them on exactly the same coordinate -- that is the point of this map
        if key == "jordansmuehl":
            for r in d["nearby"]:
                nx, ny = project(float(r["wgs84_x"]), float(r["wgs84_y"]))
                p.append(vu.svg_marker(nx, ny, "3", {"fill": "#ffffff", "stroke": vu.TEXT_MUTED},
                                       r=12))
            p.append(vu.svg_marker(px - 17, py + 17, "2", {"fill": "#ffffff",
                                                           "stroke": vu.TEXT_DARK}, r=12))
        p.append(vu.case_map_frame(MX, y0 + 34, MW, map_h))
        p.append(vu.case_locator(wide, MX + MW - 116, y0 + 34 + map_h - 140,
                                 102, 128, band["locator_label"],
                                 point=d["point"][key]))
        label = vu.t(lang, band["inner_label_de"], band["inner_label_en"])
        p.append(f'<rect x="{MX + 8}" y="{y0 + 46}" width="{vu.text_width(label, 11.5) + 16:.0f}" '
                 f'height="22" rx="6" fill="#ffffff" fill-opacity="0.82"/>')
        p.append(T(MX + 16, y0 + 58, label, size=11.5, color=OSM["stroke"], baseline="central"))
        if key == "jordansmuehl":
            text = vu.t(
                lang, "1 und 2 liegen auf derselben Koordinate, 3 zwei Kilometer daneben — "
                      "alle drei „Mittelpunkt der Gemeinde“.",
                "1 and 2 sit on the same coordinate, 3 two kilometres away — all three "
                "“centre of the municipality”.")
            lines = vu.wrap_lines(text, 296, 11)
            p.append(f'<rect x="{MX + 10}" y="{y0 + 72}" width="312" '
                     f'height="{len(lines) * 15 + 12}" rx="6" fill="#ffffff" fill-opacity="0.88"/>')
            note, _ = vu.svg_text_block(MX + 16, y0 + 88, text, 296, size=11, line_h=15,
                                        color=vu.UNCERTAIN_STROKE)
            p.append(note)
        p.append(T(MX + MW, y0 + map_h + 52, vu.t(
            lang, "Flächen: © OpenStreetMap-Mitwirkende, ODbL",
            "areas: © OpenStreetMap contributors, ODbL"),
            size=10.5, color=vu.TEXT_MUTED, anchor="end", baseline="central"))

        # ---- the chain
        lane, ry = y0 + 44, y0 + 150
        chain = m["chain"][key]
        for i, node in enumerate(chain):
            p.append(vu.chain_node(node, lang, xs[i], ry, NW))
            slot = node.get("gnd_slot")
            if slot:
                label_text, kind = slot
                if "|" in label_text:
                    label_text = vu.t(lang, *label_text.split("|"))
                p.append(vu.gnd_slot(xs[i] + NW / 2, lane, label_text, kind, ry))
        p.append(T(xs[0] - 12, lane + 13, "GND", size=14, weight=500, color=GND["stroke"],
                   anchor="end", baseline="central"))
        for i in range(len(chain) - 1):
            p.append(vu.svg_arrow_labeled(xs[i] + NW, ry + NH / 2, xs[i + 1], ry + NH / 2,
                                          "P131", font_size=11))

        # ---- the predecessor beside the chain: a place that only the GND holds
        aside = m["aside"][key]
        source = xs[band["aside_from"]] + NW / 2
        ady = band.get("aside_dy", 132)
        p.append(vu.case_node(xs[1], ry + ady, NW + 40, aside["name_de" if de else "name_en"],
                              aside["ids_de" if de else "ids_en"], aside["hubs"],
                              kind="concept"))
        p.append(vu.svg_arrow_L(source, ry + NH + 32, xs[1] + NW + 40,
                                ry + ady + NH / 2, bend="v", dashed=True))
        note_markup, _ = vu.svg_text_block(band["note_x"], ry + ady + band["note_dy"],
                                           aside["note_de" if de else "note_en"],
                                           band["note_w"], size=11.5, color=vu.TEXT_MUTED)
        p.append(note_markup)

    p.append(f'<line x1="{MX}" y1="505" x2="{vu.CANVAS_W - vu.MARGIN_X}" y2="505" '
             f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')
    p.append(vu.case_legend(MX, lang))
    p.append(vu.svg_close())
    return "\n".join(p)


# --------------------------------------------------------------------------- #
# Figure C -- what hangs off the findspot
# --------------------------------------------------------------------------- #
def _fig_c(d: dict, lang: str) -> str:
    m = d["m"]
    de = lang == "de"
    se, jo = d["row"]["seelow"], d["row"]["jordansmuehl"]
    terms, pubs = m["terms"], m["publications"]
    p = [vu.svg_open(vu.t(lang, "Der Graph dahinter: die Scherbe und der Ortsname",
                          "The graph behind it: the sherd and the place name"))]
    X = vu.MARGIN_X
    NW, NH = 196, 58
    # Four columns; the lower chain's last node carries a +40 offset, so the
    # spacing is figured with that width and both halves reach the edge.
    xs = vu.chain_xs(4, node_w=NW + 40, x0=X)
    a: list[str] = []          # the two examples are collected separately
    b: list[str] = []          # and centred by ``case_split``

    # ---------------- Seelow: down to the sherd, and back up to a monument id
    head = vu.t(lang, "Seelow 20 · Katalognr. 55005", "Seelow 20 · catalogue no. 55005")
    a.append(T(X, 58, head, size=20, weight=500))
    a.append(T(X + vu.text_width(head, 20) + 26, 58, vu.t(
        lang, "die Kette reicht unter die Fundstelle — und endet oben bei einer Nummer, "
              "die nur die Behörde führt",
        "the chain reaches below the findspot — and ends at a number only the authority "
        "keeps"), size=13, color=vu.TEXT_MUTED, italic=True))
    chip, _ = vu.svg_chip(X, 74, vu.t(
        lang, f"{se['quelle_georef']} · {se['methodenbeschr']}",
        f"{se['quelle_georef']} · {m['sites']['seelow']['method_en']}"), AGG, size=12)
    a.append(chip)

    top, below = 150, 320
    sherd = m["sherds"][0]
    a.append(vu.case_node(xs[0], top, NW, vu.t(lang, "Scherbe", "sherd"), sherd["wikidata"],
                          {"G": "none", "W": "ok", "O": "none", "F": "ok"}, kind="object"))
    a.append(vu.case_node(xs[1], top, NW, vu.t(lang, "Fundstelle Seelow 20", "findspot Seelow 20"),
                          vu.t(lang, "Katalognr. 55005 · kein QID",
                               "catalogue no. 55005 · no QID"),
                          {"G": "none", "W": "none", "O": "none", "F": "ok"}, kind="object"))
    a.append(vu.case_node(xs[2], top, NW, m["sites"]["seelow"]["monument_de" if de
                                                              else "monument_en"],
                          m["sites"]["seelow"]["activity"],
                          {"G": "open", "W": "none", "O": "none", "F": "ok"}, kind="concept"))
    a.append(vu.case_node(xs[3], top, NW, vu.t(lang, "Seelow", "Seelow"),
                          "Q587069 · GND 4340023-1",
                          {"G": "ok", "W": "ok", "O": "ok", "F": "ok"}))
    a.append(vu.svg_arrow_labeled(xs[0] + NW, top + NH / 2, xs[1], top + NH / 2,
                                  vu.t(lang, "aus", "from"), font_size=11))
    a.append(vu.svg_arrow_labeled(xs[1] + NW, top + NH / 2, xs[2], top + NH / 2,
                                  vu.t(lang, "erfasst als", "recorded as"), font_size=11))
    a.append(vu.svg_arrow_labeled(xs[2] + NW, top + NH / 2, xs[3], top + NH / 2,
                                  vu.t(lang, "liegt in", "located in"), font_size=11))
    note, _ = vu.svg_text_block(xs[2] - 6, top + NH + 46, vu.t(
        lang, f"Die Denkmalnummer und die Aktivitätsnummer {m['sites']['seelow']['activity']} "
              f"identifizieren den Ort eindeutig — aber nur innerhalb des Landesdenkmalamts. "
              f"Die Grabung gab es, weil {m['sites']['seelow']['occasion_de']} gebaut wurde.",
        f"The monument number and the activity number {m['sites']['seelow']['activity']} "
        f"identify the place unambiguously — but only inside the heritage authority. The "
        f"excavation happened because {m['sites']['seelow']['occasion_en']} was built."),
        290, size=11, color=vu.UNCERTAIN_STROKE)
    a.append(note)

    targets = []
    for i, (title, subtitle, hubs, kind) in enumerate([
            (terms["sbk"]["name_de" if de else "name_en"],
             f"{terms['sbk']['wikidata']} · GND {terms['sbk']['gnd']}",
             {"G": "ok", "W": "ok", "O": "none", "F": "ok"}, "concept"),
            (vu.t(lang, "Grabungsbericht", "excavation report"),
             f"{pubs['voelker']['wikidata']} · {pubs['voelker']['short']}",
             {"G": "none", "W": "ok", "O": "none", "F": "ok"}, "concept")]):
        node_x = xs[i] + 40
        a.append(vu.case_node(node_x, below, NW, title, subtitle, hubs, kind=kind))
        targets.append(node_x + NW / 2)
    a.append(vu.case_fan(xs[0] + NW / 2, top + NH + 30, below - 22, targets,
                  vu.t(lang, "Kultur · P2596 · belegt in",
                       "culture · P2596 · documented in")))

    # ---------------- Jordansmühl: the name survives as a term, not as a place
    y1 = 496
    head = vu.t(lang, "Jordansmühl / Jordanów Śląski · Katalognr. 7",
                "Jordansmühl / Jordanów Śląski · catalogue no. 7")
    b.append(T(X, y1 + 20, head, size=20, weight=500))
    b.append(T(X + vu.text_width(head, 20) + 26, y1 + 20, vu.t(
        lang, "hier trägt der Ortsname eine ganze Kultur — und hat selbst keinen Satz",
        "here the place name carries a whole culture — and has no record of its own"),
        size=13, color=vu.TEXT_MUTED, italic=True))
    chip, _ = vu.svg_chip(X, y1 + 36, vu.t(
        lang, f"{jo['quelle_georef']} · {jo['methodenbeschr']}",
        f"{jo['quelle_georef']} · {m['sites']['jordansmuehl']['method_en']}"), AGG, size=12)
    b.append(chip)

    ry, ry2 = y1 + 112, y1 + 282
    b.append(vu.case_node(xs[0], ry, NW, vu.t(lang, "Fundstelle", "findspot"),
                          vu.t(lang, "Katalognr. 7 · kein QID", "catalogue no. 7 · no QID"),
                          {"G": "none", "W": "none", "O": "none", "F": "ok"}, kind="object"))
    b.append(vu.case_node(xs[1], ry, NW + 40, vu.t(lang, "Ortsname Jordansmühl",
                                                   "the name Jordansmühl"),
                          vu.t(lang, "deutsch vor 1945 · heute Jordanów Śląski",
                               "German before 1945 · today Jordanów Śląski"),
                          {"G": "open", "W": "ok", "O": "ok", "F": "ok"}, kind="concept"))
    b.append(vu.case_node(xs[2], ry, NW + 40, terms["jordanow"]["name_de" if de else "name_en"],
                          f"GND {terms['jordanow']['gnd']} · saz · {terms['jordanow']['time']}",
                          {"G": "ok", "W": "open", "O": "none", "F": "ok"}, kind="concept"))
    b.append(vu.case_node(xs[3] + 40, ry, NW, vu.t(lang, "Gmina Jordanów Śląski",
                                                   "Gmina Jordanów Śląski"),
                          "Q2191877 · rel 3049634",
                          {"G": "none", "W": "ok", "O": "ok", "F": "ok"}))
    b.append(vu.svg_arrow_labeled(xs[0] + NW, ry + NH / 2, xs[1], ry + NH / 2,
                                  vu.t(lang, "heißt nach", "named after"), font_size=11))
    b.append(vu.svg_arrow_labeled(xs[1] + NW + 40, ry + NH / 2, xs[2], ry + NH / 2,
                                  vu.t(lang, "benennt, Seger 1906", "names, Seger 1906"),
                                  font_size=11))
    # the gap between these two boxes is too narrow for a label on the arrow --
    # the wording goes above it, where there is white space
    b.append(vu.svg_arrow(xs[2] + NW + 40, ry + NH / 2, xs[3] + 40, ry + NH / 2,
                          dashed=True, marker="arrow-uncertain",
                          stroke=vu.UNCERTAIN_STROKE))
    b.append(T((xs[2] + NW + 40 + xs[3] + 40) / 2, ry - 10,
               vu.t(lang, "nur im Definitionstext", "only in the definition text"),
               size=11, weight=500, color=vu.UNCERTAIN_STROKE, anchor="middle"))
    quote, _ = vu.svg_text_block(xs[2] - 6, ry + NH + 46,
                                 terms["jordanow"]["definition_de" if de else "definition_en"],
                                 420, size=11.5, italic=True, color=GND["stroke"])
    b.append(quote)
    note2, _ = vu.svg_text_block(xs[2] - 6, ry + NH + 112,
                                 terms["jordanow"]["note_de" if de else "note_en"],
                                 420, size=11, color=vu.UNCERTAIN_STROKE)
    b.append(note2)

    targets = []
    for i, (title, subtitle, hubs, kind, nw) in enumerate([
            (pubs["richthofen"]["short"],
             f"{pubs['richthofen']['wikidata']} · "
             f"{pubs['richthofen']['kind_short_de' if de else 'kind_short_en']}",
             {"G": "none", "W": "ok", "O": "none", "F": "ok"}, "concept", NW + 64),
            (m["aside"]["jordansmuehl"]["name_de" if de else "name_en"],
             m['aside']['jordansmuehl']['ids_de' if de else 'ids_en'],
             {"G": "ok", "W": "open", "O": "none", "F": "none"}, "concept", NW)]):
        node_x = xs[i] + 40
        b.append(vu.case_node(node_x, ry2, nw, title, subtitle, hubs, kind=kind))
        targets.append(node_x + nw / 2)
    b.append(vu.case_fan(xs[0] + NW / 2, ry + NH + 30, ry2 - 22, targets,
                  vu.t(lang, "verortet aus · Karte 2 von", "georeferenced from · map 2 of")))

    p.append(vu.case_split(a, b))
    p.append(vu.case_legend(X, lang))
    p.append(vu.svg_close())
    return "\n".join(p)


# --------------------------------------------------------------------------- #
def build(lang: str = "de") -> list[str]:
    d = load()
    written = []
    written += vu.write_figure(OUT, f"rollen.{lang}", _fig_a(d, lang), zoom=1.5)
    written += vu.write_figure(OUT, f"ortskette.{lang}", _fig_b(d, lang), zoom=1.5)
    written += vu.write_figure(OUT, f"graph-dahinter.{lang}", _fig_c(d, lang), zoom=1.5)
    return written


def main() -> list[str]:
    vu.ensure_dirs()
    written = []
    for lang in ("de", "en"):
        written += build(lang)
    for path in written:
        print(f"  wrote {path}")
    return written


if __name__ == "__main__":
    main()
