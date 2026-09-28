#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_05_ogham.py -- case study Ogham: two stones, one grid
==========================================================

Three figures, built on the case-study grid recorded in PRIMER.md (A4):

  A  ``rollen``          who holds what -- GND, Wikidata/Wikibase, OSM and the
                         subject hubs, for the findspot and for where the stone
                         stands today
  B  ``ortskette``       the chain of places behind each stone, with the GND
                         lane above it and the geometry taken from fuzzy-sl
  C  ``graph-dahinter``  the inscription as a graph that leads back to a place

The two stones are chosen to contrast: CIIC 81 (Garranes, Co. Cork) left its
findspot and stands 20.5 km away in the Stone Corridor of University College
Cork, while CIIC 178 (Coumeenoole North / Dunmore Head, Co. Kerry) was
re-erected in 1839 where it was found, so findspot and current location are
the same place.

Inputs (all under ``data/raw/``):

* ``wikidata/*.json``   the stones, sites, ringfort, townlands, baronies and
                        the headland -- ``Special:EntityData``
* ``fuzzy-sl/Q74.json``, ``Q131.json``  the fuzzy-sl Wikibase items: one
                        coordinate statement per place type, each with method,
                        certainty and source
* ``osm/*.xml``         the stones' nodes, the ringfort way, the headland node
                        and the townland relation -- OSM API 0.6 (ODbL)
* ``epidoc/*.xml``      the OG(H)AM editions; the current transliteration and
                        its underdotted (uncertain) letters are read from here
                        rather than retyped
* ``manual/ogham.yaml`` everything that is in none of those files: GND IDs,
                        the other editors' readings, the kin groups, picture
                        credits and the labels of the fuzzy-sl properties
"""

from __future__ import annotations

import json
import math
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "py"))

import yaml  # noqa: E402

import hdoku26_visuals_utils as vu  # noqa: E402

RAW = vu.DATA_RAW
OUT = vu.OUT_DIRS["05-ogham"]

GND, WD, AGG, OSM = vu.GND, vu.COMMUNITY, vu.AGGREGATOR, vu.OSM
UNC = {"fill": vu.UNCERTAIN_FILL, "stroke": vu.UNCERTAIN_STROKE}
OPEN = {"fill": "#ffffff", "stroke": vu.OPEN_STROKE}
T = vu.svg_text


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
def _wd(qid: str) -> dict:
    data = json.loads((RAW / "wikidata" / f"{qid}.json").read_text(encoding="utf-8"))
    return next(iter(data["entities"].values()))


def _fsl(qid: str) -> dict:
    data = json.loads((RAW / "fuzzy-sl" / f"{qid}.json").read_text(encoding="utf-8"))
    return next(iter(data["entities"].values()))


def _coords(entity: dict, prop: str = "P625") -> list[dict]:
    out = []
    for claim in entity["claims"].get(prop, []):
        value = claim["mainsnak"].get("datavalue", {}).get("value")
        if value:
            out.append({"lat": value["latitude"], "lon": value["longitude"],
                        "rank": claim["rank"], "claim": claim})
    return out


def _osm_tags(path: Path) -> dict:
    root = ET.parse(RAW / "osm" / path).getroot()
    element = root[0]
    tags = {t.get("k"): t.get("v") for t in element.findall("tag")}
    tags["_id"] = element.get("id")
    tags["_type"] = element.tag
    if element.get("lat"):
        tags["_lat"], tags["_lon"] = float(element.get("lat")), float(element.get("lon"))
    return tags


TEI = "{http://www.tei-c.org/ns/1.0}"


def _epidoc_reading(filename: str) -> tuple[str, list[int]]:
    """The current transliteration of an OG(H)AM edition, plus the positions of
    the letters the editors underdotted (unclear). ``<supplied>`` is rendered
    in square brackets, the way every other edition prints it."""
    root = ET.parse(RAW / "epidoc" / filename).getroot()
    div = next(d for d in root.iter(f"{TEI}div")
               if d.get("type") == "edition" and d.get("subtype") == "transliteration")

    def walk(node) -> str:
        text = node.text or ""
        for child in node:
            inner = walk(child)
            if child.tag == f"{TEI}supplied":
                inner = f"[{inner}]"
            text += inner + (child.tail or "")
        return text

    raw = re.sub(r"\s+", " ", walk(div)).strip()
    plain, unclear = "", []
    for char in unicodedata.normalize("NFD", raw):
        if char == "̣":              # combining dot below = unclear letter
            unclear.append(len(plain) - 1)
        elif unicodedata.combining(char):
            continue
        else:
            plain += char
    return plain, unclear


def load() -> dict:
    manual = yaml.safe_load((RAW / "manual" / "ogham.yaml").read_text(encoding="utf-8"))
    places = yaml.safe_load((RAW / "manual" / "places.yaml").read_text(encoding="utf-8"))
    d = {
        "m": manual,
        "places": places,
        "wd": {qid: _wd(qid) for qid in (
            "Q130529871", "Q126503090", "Q69385525", "Q85395557", "Q141591358",
            "Q104295278", "Q104309699", "Q26716192", "Q59419929", "Q20616069")},
        "fsl": {"Q74": _fsl("Q74"), "Q131": _fsl("Q131")},
        "osm": {
            "stone81": _osm_tags("node_11071361392.xml"),
            "stone178": _osm_tags("node_5145413640.xml"),
            "ringfort": _osm_tags("way_1252604956.xml"),
            "headland": _osm_tags("node_4306696347.xml"),
            "townland178": _osm_tags("relation_4250372.xml"),
        },
        "reading": {
            "ciic81": _epidoc_reading("I-COR-030.xml"),
            "ciic178": _epidoc_reading("I-KER-046.xml"),
        },
    }
    # the two fuzzy-sl coordinate statements per stone, preferred rank first
    for key, qid in (("ciic81", "Q74"), ("ciic178", "Q131")):
        pts = _coords(d["fsl"][qid], "P4")
        pts.sort(key=lambda p: 0 if p["rank"] == "preferred" else 1)
        d.setdefault("fsl_points", {})[key] = pts
    # the five sourced coordinates of the Coumeenoole Ogham Site
    site = []
    for claim in d["wd"]["Q85395557"]["claims"]["P625"]:
        value = claim["mainsnak"]["datavalue"]["value"]
        site.append({"lat": value["latitude"], "lon": value["longitude"],
                     "source": _reference_label(claim)})
    d["site178_points"] = site
    return d


def _reference_label(claim: dict) -> str:
    """Which source a coordinate statement cites, read from its references:
    an OSM node id, an SMR number or the host of the cited URL."""
    for reference in claim.get("references", []):
        snaks = reference["snaks"]
        if "P11693" in snaks:
            return "OpenStreetMap"
        if "P4057" in snaks:
            return "SMR"
        for snak in snaks.get("P854", []):
            url = snak["datavalue"]["value"]
            if "cisp" in url:
                return "CISP"
            if "ogham.celt.dias.ie" in url:
                return "Ogham in 3D"
            if "townlands.ie" in url:
                return "townlands.ie"
            if "logainm" in url:
                return "Logainm"
    return "?"


# --------------------------------------------------------------------------- #
# Figure A -- who holds what
# --------------------------------------------------------------------------- #
CHIP_STYLES = {"ok": None, "gnd": GND, "open": OPEN, "unc": UNC}


def _cell(x: float, y: float, w: float, h: float, colors: dict, status: str,
          headline: str, chips: list[tuple[str, str]]) -> str:
    parts = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="10" '
             f'fill="#ffffff" stroke="{colors["stroke"]}" stroke-width="1.2" stroke-opacity="0.6"/>']
    parts.append(vu.status_icon(x + 24, y + 24, status, UNC if status == "unc" else colors))
    parts.append(T(x + 46, y + 25, headline, size=14, weight=500, baseline="central"))
    cy = y + 46
    for label, style in chips:
        chip_colors = CHIP_STYLES[style] or colors
        markup, _ = vu.svg_chip(x + 14, cy, label, chip_colors, width=w - 28, align="start",
                                dashed=(style == "open"))
        parts.append(markup)
        cy += 28
    return "\n".join(parts)


def _fig_a(d: dict, lang: str) -> str:
    m = d["m"]
    p = [vu.svg_open(vu.t(lang, "Wer hält was: zwei Ogham-Steine",
                          "Who holds what: two Ogham stones"))]
    LX = vu.MARGIN_X
    C1, C2, CW = 250, 975, 715
    SUB = (CW - 12) / 2

    for cx, key, note_de, note_en in (
            (C1, "ciic81", "Fundort und Standort getrennt · 20,5 km",
             "findspot and current location apart · 20.5 km"),
            (C2, "ciic178", "Fundort ist Standort · 1839 wieder aufgerichtet",
             "findspot is the current location · re-erected 1839")):
        img = m["images"][key]
        crop = tuple(img["crop"]) if img["crop"] else None
        p.append(vu.svg_image_crop(cx, 50, 150, 150, RAW / "images" / img["file"], crop))
        p.append(T(cx + 170, 82, m["stones"][key][f"title_{'de' if lang == 'de' else 'en'}"],
                   size=22, weight=500))
        stone = m["stones"][key]
        p.append(T(cx + 170, 110, f"{stone['epidoc']} · CISP {stone['cisp']} · "
                                  f"lod.ogham.link {stone['ogham_lod']}", size=13,
                   color=vu.TEXT_MUTED))
        chip, _ = vu.svg_chip(cx + 170, 128, vu.t(lang, note_de, note_en), AGG, size=12.5, h=26)
        p.append(chip)
        p.append(T(cx, 214, img[f"caption_{'de' if lang == 'de' else 'en'}"] + " · " + img["credit"],
                   size=10.5, color=vu.TEXT_MUTED))

    p.append(T(C1 + 14, 248, vu.t(lang, "Fundort", "findspot"), size=15, weight=500))
    p.append(T(C1 + SUB + 26, 248, vu.t(lang, "Standort heute", "current location"),
               size=15, weight=500))
    p.append(T(C2 + 14, 248, vu.t(lang, "Fundort = Standort heute",
                                  "findspot = current location"), size=15, weight=500))
    for x0 in (C1, C2):
        p.append(f'<line x1="{x0}" y1="258" x2="{x0 + CW}" y2="258" '
                 f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')

    gnd = m["gnd"]
    osm = d["osm"]
    rows = [
        ("GND", GND, 270, 112, [
            ("up", vu.t(lang, "Ringwall, nicht der Stein", "the ringfort, not the stone"), [
                (f"GND {gnd['ringfort_garranes']} · " + vu.t(lang, "Garranes, Ringwallanlage",
                                                             "Garranes, ringfort"), "gnd"),
                (vu.t(lang, "= SMR CO084-090001- · ohne Koordinate",
                      "= SMR CO084-090001- · no coordinate"), "open"),
            ]),
            ("ok", vu.t(lang, "Körperschaft und County", "corporate body and county"), [
                (f"GND {gnd['ucc']} · University College Cork", "gnd"),
                (f"GND {gnd['county_cork']} · " + vu.t(lang, "Cork (County)", "Cork (county)"), "gnd"),
            ]),
            ("none", vu.t(lang, "kein Satz für Stein oder Ort", "no record for stone or place"), [
                (vu.t(lang, "Dunmore Head · Coumeenoole · Corkaguiny: 0 Treffer",
                      "Dunmore Head · Coumeenoole · Corkaguiny: 0 hits"), "open"),
                (f"GND {gnd['county_kerry']} · " + vu.t(lang, "Kerry (County)", "Kerry (county)"), "gnd"),
            ]),
        ]),
        (vu.t(lang, "Wikidata / Wikibase", "Wikidata / Wikibase"), WD, 390, 186, [
            ("ok", vu.t(lang, "Fundort, Ringfort, Townland", "findspot, ringfort, townland"), [
                ("P189: Q69385525 Garranes (Ogham Site)", "ok"),
                ("Q141591358 Ringfort Lisheenagreine", "ok"),
                ("Q104295278 Townland · Logainm 8299", "ok"),
                (vu.t(lang, "fuzzy-sl Q74 · Fundort, Sicherheit Low",
                      "fuzzy-sl Q74 · findspot, certainty Low"), "ok"),
            ]),
            ("ok", vu.t(lang, "Stein, Sammlung, Raum", "stone, collection, room"), [
                ("Q130529871 " + vu.t(lang, "Stein", "stone") + " · P276", "ok"),
                ("Q1574185 UCC · Q121592049 Stone Corridor", "ok"),
                (vu.t(lang, "P625 zwei Werte, gerankt", "P625 two values, ranked"), "ok"),
                (vu.t(lang, "fuzzy-sl Q74 · Ausstellungsort, High",
                      "fuzzy-sl Q74 · exhibition site, High"), "ok"),
            ]),
            ("ok", vu.t(lang, "Stein, Site, Townland", "stone, site, townland"), [
                ("Q126503090 " + vu.t(lang, "Stein", "stone") + " · P276: Q26716192 Dunmore Head", "ok"),
                ("Q85395557 Ogham Site · " + vu.t(lang, "fünf Koordinaten, je mit Quelle",
                                                  "five coordinates, each sourced"), "unc"),
                ("Q104309699 Townland · Logainm 22572", "ok"),
                (vu.t(lang, "fuzzy-sl Q131 · Fundort und Standort auf einem Punkt",
                      "fuzzy-sl Q131 · findspot and current location on one point"), "ok"),
            ]),
        ]),
        ("OpenStreetMap", OSM, 586, 158, [
            ("ok", vu.t(lang, "Ringfort und Townland als Flächen",
                        "ringfort and townland as areas"), [
                (f"way {osm['ringfort']['_id']} · fortification_type=ringfort", "ok"),
                ("relation " + str(d["wd"]["Q104295278"]["claims"]["P402"][0]["mainsnak"]
                                   ["datavalue"]["value"]) + " · Townland Garranes", "ok"),
                (vu.t(lang, "der Fundort selbst hat kein Objekt",
                      "the findspot itself has no object"), "open"),
            ]),
            ("ok", vu.t(lang, "Node im Gebäude", "node inside the building"), [
                (f"node {osm['stone81']['_id']} · indoor=yes · moved=yes", "ok"),
                ("inscription:pgl-Latn · " + osm["stone81"]["inscription:pgl-Latn"].split(" MAQI")[0], "unc"),
                (f"wikidata={osm['stone81']['wikidata']} · "
                 + vu.t(lang, "Sammel-Item, besser Q130529871",
                        "umbrella item, better Q130529871"), "unc"),
            ]),
            ("ok", vu.t(lang, "Node am Fundort", "node at the findspot"), [
                (f"node {osm['stone178']['_id']} · historic=ogham_stone · moved=no", "ok"),
                (f"inscription · ref:IE:smr {osm['stone178']['ref:IE:smr']}", "ok"),
                (f"relation {osm['townland178']['_id']} Townland · "
                 f"node {osm['headland']['_id']} An Dún Mór", "ok"),
            ]),
        ]),
        (vu.t(lang, "Fach-Hubs", "subject hubs"), AGG, 762, 158, [
            ("ok", vu.t(lang, "Gazetteer und Denkmalregister", "gazetteer and monument register"), [
                ("Logainm 8299 · An Garrán", "ok"),
                ("SMR CO084-090001- / -090002- / -090003-", "ok"),
                ("CISP GARES/1 · lod.ogham.link Y50000081", "ok"),
            ]),
            ("ok", vu.t(lang, "Register am Standort", "registers at the current location"), [
                (f"SMR {m['stones']['ciic81']['smr_stone_keeper']}", "ok"),
                (m["stones"]["ciic81"]["inventory"], "ok"),
                ("Sketchfab (b-unicycling)", "ok"),
            ]),
            ("ok", vu.t(lang, "zwei Gazetteer-Anker", "two gazetteer anchors"), [
                ("Logainm 22572 · Logainm 1394328", "ok"),
                (f"SMR {m['stones']['ciic178']['smr_stone']} · "
                 + vu.t(lang, "Fort", "fort") + f" {m['stones']['ciic178']['smr_fort']}", "ok"),
                ("CISP COUME/1 · TM 172528 · lod.ogham.link Y50000178", "ok"),
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
        p.append(_cell(C1, y + pad, SUB, h - 2 * pad, colors, *cells[0]))
        p.append(_cell(C1 + SUB + 12, y + pad, SUB, h - 2 * pad, colors, *cells[1]))
        p.append(_cell(C2, y + pad, CW, h - 2 * pad, colors, *cells[2]))

    p.append(vu.status_legend(LX, 950, [
        ("ok", vu.t(lang, "vorhanden", "present")),
        ("up", vu.t(lang, "eine Ebene höher", "one level up")),
        ("none", vu.t(lang, "fehlt", "missing")),
        ("open", vu.t(lang, "offen", "open")),
        ("unc", vu.t(lang, "unsicher oder uneinheitlich", "uncertain or inconsistent")),
    ]))
    p.append(vu.svg_close())
    return "\n".join(p)


# --------------------------------------------------------------------------- #
# Figure B -- the chain of places
# --------------------------------------------------------------------------- #
def _map(x: float, y: float, w: float, h: float, bbox: tuple, clip_id: str):
    lon0, lon1, lat0, lat1 = bbox
    k = math.cos(math.radians((lat0 + lat1) / 2))
    s = min(w / ((lon1 - lon0) * k), h / (lat1 - lat0))
    ox = x + (w - (lon1 - lon0) * k * s) / 2
    oy = y + (h - (lat1 - lat0) * s) / 2

    def project(lon: float, lat: float) -> tuple[float, float]:
        return ox + (lon - lon0) * k * s, oy + (lat1 - lat) * s

    rings = json.loads((RAW / "naturalearth" / "ireland_outline.json").read_text(encoding="utf-8"))
    parts = [f'<defs><clipPath id="{clip_id}"><rect x="{x}" y="{y}" width="{w}" height="{h}" '
             f'rx="12"/></clipPath></defs>',
             f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{vu.SEA_FILL}"/>',
             f'<g clip-path="url(#{clip_id})">']
    for poly in rings:
        path = "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in
                                 (project(*point) for point in poly["ring"])) + " Z"
        parts.append(f'<path d="{path}" fill="{vu.LAND_FILL}" stroke="{vu.LAND_STROKE}" '
                     f'stroke-width="1"/>')
    parts.append("</g>")
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="none" '
                 f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1.2"/>')
    return "\n".join(parts), project


def _fsl_mark(x: float, y: float, number: str, certainty: str) -> str:
    parts = []
    if certainty == "Low":
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="30" fill="{vu.UNCERTAIN_FILL}" '
                     f'fill-opacity="0.45" stroke="{vu.UNCERTAIN_STROKE}" stroke-width="1.6" '
                     f'stroke-dasharray="5 4"/>')
    parts.append(vu.svg_marker(x, y, number, {"fill": "#ffffff", "stroke": vu.TEXT_DARK}))
    return "\n".join(parts)


def _note(x: float, y: float, lines: list[str], anchor: str = "start") -> str:
    out = [T(x, y, lines[0], size=14, weight=500, anchor=anchor)]
    for i, line in enumerate(lines[1:]):
        out.append(T(x, y + 18 + i * 16, line, size=12, color=vu.TEXT_MUTED, anchor=anchor))
    return "\n".join(out)


def _fig_b(d: dict, lang: str) -> str:
    m, osm = d["m"], d["osm"]
    de = lang == "de"
    p = [vu.svg_open(vu.t(lang, "Ortsketten: Fundort und Standort",
                          "Chains of places: findspot and current location"))]
    MX, MW = vu.MARGIN_X, 470
    NW, NH = 186, 58
    xs = [575 + i * 226 for i in range(5)]

    # ---------------- CIIC 81
    y0 = 40
    p.append(T(MX, y0 + 16, "CIIC 81", size=20, weight=500))
    p.append(T(MX + 90, y0 + 16, vu.t(lang, "Fundort und Standort getrennt · 20,5 km",
                                      "findspot and current location apart · 20.5 km"),
               size=14, color=vu.TEXT_MUTED))
    markup, project = _map(MX, y0 + 34, MW, 372, (-9.40, -8.02, 51.58, 52.10), "map-ciic81")
    p.append(markup)
    points = d["fsl_points"]["ciic81"]
    labels = m["fuzzy_sl"]["statements"]["ciic81"]
    key_y = y0 + 300
    for i, (point, meta) in enumerate(zip(points, labels)):
        mx, my = project(point["lon"], point["lat"])
        p.append(_fsl_mark(mx, my, str(i + 1), meta["certainty"]))
        # key inside the map, so that no label crosses the frame
        p.append(vu.svg_marker(MX + 28, key_y + i * 44, str(i + 1),
                               {"fill": "#ffffff", "stroke": vu.TEXT_DARK}, r=11))
        p.append(T(MX + 48, key_y + i * 44 - 7,
                   f"{meta['place_de' if de else 'place_en']} · "
                   f"{meta['type_de' if de else 'type_en']}", size=13.5, weight=500))
        p.append(T(MX + 48, key_y + i * 44 + 11,
                   f"fuzzy-sl: {meta['certainty']} · {meta['method_de' if de else 'method_en']}",
                   size=12, color=vu.TEXT_MUTED))
    chip, _ = vu.svg_chip(MX, y0 + 416, vu.t(
        lang, "Geometrie: fuzzy-sl Q74 · Ort-Typ, Methode und Sicherheit je Koordinate",
        "geometry: fuzzy-sl Q74 · location type, method and certainty per coordinate"),
        WD, size=12)
    p.append(chip)

    lane = y0 + 44
    ry1, ry2 = y0 + 140, y0 + 312
    sy = (ry1 + ry2) / 2
    p.append(vu.case_node(xs[0], sy, NW, vu.t(lang, "Stein CIIC 81", "Stone CIIC 81"),
                          f"Q130529871 · node {osm['stone81']['_id']}",
                          {"G": "pot", "W": "ok", "O": "ok", "F": "ok"}, kind="object"))
    findspot = [
        ("Ringfort Lisheenagreine", "Q141591358 · SMR CO084-090001-",
         {"G": "ok", "W": "ok", "O": "ok", "F": "ok"}),
        (vu.t(lang, "Townland Garranes", "Townland Garranes"),
         "Q104295278 · Logainm 8299", {"G": "pot", "W": "ok", "O": "ok", "F": "ok"}),
        (vu.t(lang, "Baronie Kinalmeaky", "Barony Kinalmeaky"),
         "Q20616069 · Logainm 31", {"G": "pot", "W": "ok", "O": "ok", "F": "ok"}),
    ]
    current = [
        ("Stone Corridor", "Q121592049", {"G": "none", "W": "ok", "O": "open", "F": "none"}),
        ("University College Cork", f"Q1574185 · GND {m['gnd']['ucc']}",
         {"G": "ok", "W": "ok", "O": "open", "F": "none"}),
        (vu.t(lang, "Cork (Stadt)", "Cork (city)"), "Q36959",
         {"G": "open", "W": "ok", "O": "ok", "F": "open"}),
    ]
    for i, (title, subtitle, hubs) in enumerate(findspot):
        p.append(vu.case_node(xs[i + 1], ry1, NW, title, subtitle, hubs))
    for i, (title, subtitle, hubs) in enumerate(current):
        p.append(vu.case_node(xs[i + 1], ry2, NW, title, subtitle, hubs))
    p.append(vu.case_node(xs[4], sy, NW, vu.t(lang, "County Cork", "County Cork"),
                          f"Q162475 · GND {m['gnd']['county_cork']}",
                          {"G": "ok", "W": "ok", "O": "ok", "F": "open"}))
    p.append(vu.gnd_slot(xs[1] + NW / 2, lane, f"GND {m['gnd']['ringfort_garranes']}", "ok", ry1,
                         line_x=xs[1] + NW * 0.82))
    for i in (2, 3):
        p.append(vu.gnd_slot(xs[i] + NW / 2, lane, vu.t(lang, "GND denkbar", "GND conceivable"),
                             "pot", ry1))
    p.append(vu.gnd_slot(xs[4] + NW / 2, lane, f"GND {m['gnd']['county_cork']}", "ok", sy))
    p.append(vu.gnd_slot(xs[0] + NW / 2, lane, vu.t(lang, "GND denkbar (Objekt)",
                                                    "GND conceivable (object)"), "pot", sy))
    p.append(T(xs[0] - 12, lane + 13, "GND", size=14, weight=500, color=GND["stroke"],
               anchor="end", baseline="central"))
    for yy, number, label in ((ry1, "1", vu.t(lang, "Fundort · P189", "findspot · P189")),
                              (ry2, "2", vu.t(lang, "Standort heute · P276",
                                              "current location · P276"))):
        p.append(vu.svg_marker(xs[1] + 11, yy - 16, number, {"fill": "#ffffff",
                                                             "stroke": vu.TEXT_DARK}, r=10))
        p.append(T(xs[1] + 27, yy - 16, label, size=12.5, weight=500, baseline="central"))
    rail = xs[0] + NW + 20
    p.append(vu.svg_arrow_elbow_v(xs[0] + NW, sy + NH / 2 - 10, xs[1], ry1 + NH / 2, rail))
    p.append(vu.svg_arrow_elbow_v(xs[0] + NW, sy + NH / 2 + 10, xs[1], ry2 + NH / 2, rail))
    for row_y in (ry1, ry2):
        for i in (1, 2):
            p.append(vu.svg_arrow(xs[i] + NW, row_y + NH / 2, xs[i + 1], row_y + NH / 2))
    p.append(vu.svg_arrow_L(xs[3] + NW, ry1 + NH / 2, xs[4] + NW / 2 - 40, sy, bend="h"))
    p.append(vu.svg_arrow_L(xs[3] + NW, ry2 + NH / 2, xs[4] + NW / 2, sy + NH + 30, bend="h"))
    # the Ogham Site beside the ringfort: related in space, not linked in Wikidata
    site_y = ry1 + 118
    p.append(vu.case_node(xs[2], site_y, NW, "Garranes (Ogham Site)", "Q69385525",
                          None, h=48, kind="concept"))
    p.append(vu.svg_arrow_L(xs[1] + NW * 0.5, ry1 + NH + 30, xs[2], site_y + 24, bend="v",
                            dashed=True))
    note, _ = vu.svg_text_block(xs[3], site_y + 18, vu.t(
        lang, "räumlich verbunden, in Wikidata nicht verknüpft",
        "related in space, not linked in Wikidata"), 190, size=11.5,
        color=vu.UNCERTAIN_STROKE)
    p.append(note)

    p.append(f'<line x1="{MX}" y1="505" x2="{vu.CANVAS_W - vu.MARGIN_X}" y2="505" '
             f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')

    # ---------------- CIIC 178
    y0 = 520
    p.append(T(MX, y0 + 16, "CIIC 178", size=20, weight=500))
    p.append(T(MX + 100, y0 + 16, vu.t(lang, "Fundort ist Standort · 1839 wieder aufgerichtet",
                                       "findspot is the current location · re-erected 1839"),
               size=14, color=vu.TEXT_MUTED))
    markup, project = _map(MX, y0 + 34, MW, 322, (-10.484, -10.452, 52.1035, 52.1175), "map-ciic178")
    p.append(markup)
    stone = d["fsl_points"]["ciic178"][0]
    sx, sy2 = project(stone["lon"], stone["lat"])
    p.append(_fsl_mark(sx, sy2, "1", "Low"))
    shown = 0
    for point in d["site178_points"]:
        px, py = project(point["lon"], point["lat"])
        if abs(px - sx) < 4 and abs(py - sy2) < 4:
            continue
        p.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#ffffff" '
                 f'stroke="{vu.UNCERTAIN_STROKE}" stroke-width="1.6"/>')
        near_stone = math.hypot(px - sx, py - sy2) < 46
        dy = (-40 if near_stone else (16, -18, 34, -36)[shown % 4])
        p.append(T(px + 9, py + dy, point["source"], size=11, color=vu.UNCERTAIN_STROKE,
                   baseline="central"))
        p.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px:.1f}" y2="{py + dy:.1f}" '
                 f'stroke="{vu.UNCERTAIN_STROKE}" stroke-width="0.8"/>')
        shown += 1
    p.append(_note(MX + 16, y0 + 300, [
        vu.t(lang, "Stein: zwei fuzzy-sl-Aussagen auf einem Punkt",
             "stone: two fuzzy-sl statements on one point"),
        vu.t(lang, "Fundort: Low · Macalister 1945, 170", "findspot: Low · Macalister 1945, 170"),
        vu.t(lang, "Ausstellungsort: High · Survey vor Ort",
             "exhibition site: High · on-site survey")]))
    chip, _ = vu.svg_chip(MX, y0 + 366, vu.t(
        lang, "Ogham Site Q85395557: fünf Koordinaten mit je eigener Quelle, 586 m Spannweite",
        "Ogham Site Q85395557: five coordinates, each with its own source, 586 m apart"),
        UNC, size=12)
    p.append(chip)

    lane = y0 + 44
    ry = y0 + 150
    chain = [
        (vu.t(lang, "Stein CIIC 178", "Stone CIIC 178"),
         f"Q126503090 · node {osm['stone178']['_id']}",
         {"G": "pot", "W": "ok", "O": "ok", "F": "ok"}, "object"),
        ("An Dún Mór / Dunmore Head", "Q26716192 · Logainm 1394328",
         {"G": "pot", "W": "ok", "O": "ok", "F": "ok"}, "place"),
        (vu.t(lang, "Townland Coumeenoole North", "Townland Coumeenoole North"),
         f"Q104309699 · Logainm 22572 · rel {osm['townland178']['_id']}",
         {"G": "pot", "W": "ok", "O": "ok", "F": "ok"}, "place"),
        (vu.t(lang, "Baronie Corkaguiny", "Barony Corkaguiny"),
         "Q59419929 · Corca Dhuibhne · Logainm 91",
         {"G": "pot", "W": "ok", "O": "ok", "F": "ok"}, "place"),
        (vu.t(lang, "County Kerry", "County Kerry"), f"Q184469 · GND {m['gnd']['county_kerry']}",
         {"G": "ok", "W": "ok", "O": "ok", "F": "open"}, "place"),
    ]
    for i, (title, subtitle, hubs, kind) in enumerate(chain):
        p.append(vu.case_node(xs[i], ry, NW, title, subtitle, hubs, kind=kind))
    for i, (label, kind) in enumerate((
            (vu.t(lang, "GND denkbar (Objekt)", "GND conceivable (object)"), "pot"),
            (vu.t(lang, "GND denkbar", "GND conceivable"), "pot"),
            (vu.t(lang, "GND denkbar", "GND conceivable"), "pot"),
            (vu.t(lang, "GND denkbar", "GND conceivable"), "pot"),
            (f"GND {m['gnd']['county_kerry']}", "ok"))):
        p.append(vu.gnd_slot(xs[i] + NW / 2, lane, label, kind, ry,
                             line_x=(xs[i] + NW * 0.82) if i == 1 else None))
    p.append(T(xs[0] - 12, lane + 13, "GND", size=14, weight=500, color=GND["stroke"],
               anchor="end", baseline="central"))
    p.append(vu.svg_marker(xs[1] + 11, ry - 16, "1", {"fill": "#ffffff", "stroke": vu.TEXT_DARK},
                           r=10))
    p.append(T(xs[1] + 27, ry - 16, "P189 = P276", size=12.5, weight=500, baseline="central"))
    for i in range(4):
        p.append(vu.svg_arrow(xs[i] + NW, ry + NH / 2, xs[i + 1], ry + NH / 2))
    p.append(vu.case_node(xs[1], ry + 150, NW, "Coumeenoole North (Ogham Site)",
                          "Q85395557 · lod.ogham.link OS40000083",
                          {"G": "none", "W": "ok", "O": "none", "F": "ok"}, kind="concept"))
    p.append(vu.svg_arrow_L(xs[0] + NW / 2, ry + NH + 32, xs[1], ry + 150 + NH / 2, bend="v",
                            dashed=True, label="P189"))

    p.append(vu.svg_legend(MX, 938, [
        (vu.t(lang, "GND", "GND"), GND),
        (vu.t(lang, "Wikidata / Wikibase", "Wikidata / Wikibase"), WD),
        ("OpenStreetMap", OSM),
        (vu.t(lang, "Fach-Hubs", "subject hubs"), AGG),
    ], columns=4, col_w=190))
    p.append(_gnd_legend(vu.MARGIN_X, 972, lang))
    p.append(vu.svg_close())
    return "\n".join(p)


def _gnd_legend(x: float, y: float, lang: str) -> str:
    entries = [
        ("ok", vu.t(lang, "GND-Satz vorhanden", "GND record exists")),
        ("pot", vu.t(lang, "GND-Eintrag denkbar (GND-Planung)",
                     "GND entry conceivable (GND plans)")),
        ("check", vu.t(lang, "vermutlich vorhanden, zu prüfen", "probably exists, to be checked")),
    ]
    parts, cx = [], x
    for kind, label in entries:
        if kind == "ok":
            box = (f'<rect x="{cx:.1f}" y="{y - 9}" width="44" height="18" rx="9" '
                   f'fill="{GND["fill"]}" stroke="{GND["stroke"]}" stroke-width="1.4"/>')
        elif kind == "pot":
            box = (f'<rect x="{cx:.1f}" y="{y - 9}" width="44" height="18" rx="9" fill="#ffffff" '
                   f'stroke="{GND["stroke"]}" stroke-width="1.4" stroke-dasharray="5 3"/>')
        else:
            box = (f'<rect x="{cx:.1f}" y="{y - 9}" width="44" height="18" rx="9" fill="#ffffff" '
                   f'stroke="{vu.OPEN_STROKE}" stroke-width="1.2" stroke-dasharray="3 3"/>')
        parts.append(box)
        parts.append(T(cx + 52, y + 1, label, size=12.5, baseline="central"))
        cx += 52 + vu.text_width(label, 12.5) + 34
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# Figure C -- the graph behind the inscription
# --------------------------------------------------------------------------- #
def _inscription(x: float, y: float, text: str, unclear: list[int], *, size: float = 26) -> str:
    spans = []
    for i, char in enumerate(text):
        color = vu.UNCERTAIN_STROKE if i in unclear else vu.TEXT_DARK
        spans.append(f'<tspan fill="{color}">{vu.xml_escape(char)}</tspan>')
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{vu.FONT_SANS}" font-size="{size}" '
            f'font-weight="500" letter-spacing="1.5">{"".join(spans)}</text>')


def _scholars(x: float, y: float, items: list[dict], lang: str) -> str:
    parts = [T(x, y + 11, vu.t(lang, "gelesen von", "read by"), size=12.5, color=vu.TEXT_MUTED,
               baseline="central")]
    cx = x + (84 if lang == "de" else 62)
    for item in items:
        chip, w = vu.svg_chip(cx, y, item["name"], AGG, size=11.5)
        parts.append(chip)
        cx += w + 4
        if item.get("gnd"):
            parts.append(f'<rect x="{cx:.1f}" y="{y + 1}" width="28" height="20" rx="4" '
                         f'fill="{GND["fill"]}" stroke="{GND["stroke"]}" stroke-width="1.4"/>')
            parts.append(T(cx + 14, y + 12, "GND", size=9.5, weight=500, color=GND["stroke"],
                           anchor="middle", baseline="central"))
        else:
            parts.append(f'<rect x="{cx:.1f}" y="{y + 1}" width="28" height="20" rx="4" '
                         f'fill="#ffffff" stroke="{vu.OPEN_STROKE}" stroke-width="1.2" '
                         f'stroke-dasharray="3 2"/>')
            parts.append(T(cx + 14, y + 12, "?", size=11, weight=500, color=vu.OPEN_STROKE,
                           anchor="middle", baseline="central"))
        cx += 40
    return "\n".join(parts)


def _fig_c(d: dict, lang: str) -> str:
    m, osm = d["m"], d["osm"]
    de = lang == "de"
    p = [vu.svg_open(vu.t(lang, "Der Graph hinter der Inschrift führt zurück zum Ort",
                          "The graph behind the inscription leads back to a place"))]
    X = vu.MARGIN_X
    NW, NH = 172, 58
    xs = [X + i * 280 for i in range(6)]
    persons, words = m["persons"], m["words"]

    # ---------------- CIIC 178: the chain closes
    text, unclear = d["reading"]["ciic178"]
    p.append(T(X, 60, "CIIC 178", size=20, weight=500))
    p.append(_inscription(X + 110, 62, text, unclear))
    lx = X + 110 + vu.text_width(text, 26) * 1.12 + 26
    for label, colors in ((vu.t(lang, "OG(H)AM-Edition", "OG(H)AM edition"), AGG),
                          ("OpenStreetMap", OSM)):
        chip, w = vu.svg_chip(lx, 45, label, colors, size=12)
        p.append(chip)
        lx += w + 10
    p.append(T(X + 110, 90, vu.t(
        lang, f"„{m['readings']['translation_ciic178_de']}“ · rot: in der Edition unsicher gelesen",
        f"“{m['readings']['translation_ciic178_en']}” · red: read as unclear in the edition"),
        size=13, color=vu.TEXT_MUTED, italic=True))
    p.append(_scholars(X + 110, 104, m["scholars"]["ciic178"], lang))

    lane, top, bottom = 150, 210, 400
    p.append(vu.case_node(xs[0], top, NW, vu.t(lang, "Stein CIIC 178", "Stone CIIC 178"),
                          "Q126503090", {"G": "pot", "W": "ok", "O": "ok", "F": "ok"},
                          kind="object"))
    p.append(vu.case_node(xs[1], top, NW, "ERC", f"{persons['ERC']['wikidata']} · OP400203",
                          {"G": "none", "W": "ok", "O": "none", "F": "ok"}, kind="concept"))
    p.append(vu.case_node(xs[2], top, NW, "MAQI-ERCIAS", vu.t(lang, "OP400321 · kein Wikidata-Item",
                                                              "OP400321 · no Wikidata item"),
                          {"G": "none", "W": "open", "O": "none", "F": "ok"}, kind="concept"))
    p.append(vu.case_node(xs[3], top, NW, "DOVINIA", f"{persons['DOVINIA']['wikidata']} · OP400175",
                          {"G": "none", "W": "ok", "O": "none", "F": "ok"}, kind="concept"))
    p.append(vu.case_node(xs[4], top, NW, "Corcu Duibne", vu.t(lang, "Sippe · McManus 1991, 111",
                                                               "kin group · McManus 1991, 111"),
                          {"G": "pot", "W": "open", "O": "none", "F": "open"}, kind="concept"))
    p.append(vu.case_node(xs[5] - 30, top, 260, vu.t(lang, "Baronie Corkaguiny",
                                                     "Barony Corkaguiny"),
                          "Q59419929 · Corca Dhuibhne",
                          {"G": "pot", "W": "ok", "O": "ok", "F": "ok"}))
    p.append(vu.gnd_slot(xs[0] + NW / 2, lane, vu.t(lang, "GND denkbar (Objekt)",
                                                    "GND conceivable (object)"), "pot", top))
    p.append(vu.gnd_slot(xs[4] + NW / 2, lane, vu.t(lang, "GND denkbar", "GND conceivable"),
                         "pot", top))
    p.append(vu.gnd_slot(xs[5] - 30 + 130, lane, vu.t(lang, "GND denkbar", "GND conceivable"),
                         "pot", top))
    p.append(T(xs[0] + NW / 2 + 92, lane + 13, "GND", size=14, weight=500, color=GND["stroke"],
               baseline="central"))
    edge_labels = [
        vu.t(lang, "Inschrift nennt", "inscription names"),
        f"MAQI · {words['MAQI']['wikidata']}",
        f"MU(COI) · {words['MUCOI']['wikidata']}",
        vu.t(lang, "Sippe", "kin group"),
        vu.t(lang, "gab den Namen", "named after"),
    ]
    for i, label in enumerate(edge_labels):
        x2 = xs[i + 1] - (30 if i == 4 else 0)
        p.append(vu.svg_arrow_labeled(xs[i] + NW, top + NH / 2, x2, top + NH / 2, label,
                                      font_size=11))
    p.append(vu.case_node(xs[3], bottom, NW, vu.t(lang, "Townland", "Townland"),
                          "Coumeenoole North · Logainm 22572",
                          {"G": "pot", "W": "ok", "O": "ok", "F": "ok"}))
    p.append(vu.case_node(xs[1], bottom, NW, "An Dún Mór", vu.t(
        lang, "Promontory Fort · Logainm 1394328", "promontory fort · Logainm 1394328"),
        {"G": "pot", "W": "ok", "O": "ok", "F": "ok"}))
    p.append(vu.svg_arrow_L(xs[5] - 30 + 130, top + NH + 32, xs[3] + NW, bottom + NH / 2,
                            bend="v", label=vu.t(lang, "enthält", "contains")))
    p.append(vu.svg_arrow_labeled(xs[3], bottom + NH / 2, xs[1] + NW, bottom + NH / 2,
                                  vu.t(lang, "enthält", "contains"), font_size=11))
    p.append(vu.svg_arrow_L(xs[1], bottom + NH / 2, xs[0] + NW / 2, top + NH + 32, bend="h",
                            label=vu.t(lang, "Fundort", "findspot")))
    chip, _ = vu.svg_chip(X, bottom + 92, vu.t(
        lang, "DOVINIA führt über die Sippe zur Baronie – und die enthält den Fundort "
              "(McManus 1991, 111).",
        "DOVINIA leads through the kin group to the barony – and the barony contains the "
        "findspot (McManus 1991, 111)."), WD, size=13, h=28)
    p.append(chip)

    p.append(f'<line x1="{X}" y1="548" x2="{vu.CANVAS_W - vu.MARGIN_X}" y2="548" '
             f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')

    # ---------------- CIIC 81: the chain stays open
    y1 = 570
    text81, unclear81 = d["reading"]["ciic81"]
    p.append(T(X, y1 + 24, "CIIC 81", size=20, weight=500))
    p.append(_inscription(X + 110, y1 + 26, text81, unclear81))
    lx = X + 110 + vu.text_width(text81, 26) * 1.12 + 26
    variants = [r for r in m["readings"]["ciic81"] if r["text"] != text81]
    for variant in variants[:2]:
        chip, w = vu.svg_chip(lx, y1 + 9, f"{variant['source_de' if de else 'source_en']}: "
                                          f"{variant['text'].split(' MAQI')[0]}", UNC, size=12)
        p.append(chip)
        lx += w + 10
    chip, w = vu.svg_chip(lx, y1 + 9, "OSM: " + osm["stone81"]["inscription"].split(" MAQI")[0],
                          OSM, size=12)
    p.append(chip)
    p.append(T(X + 110, y1 + 54, vu.t(
        lang, "Macalister 1945: -AS · Gippert 1987: -OS · OSM hält den Streit im Tag fest",
        "Macalister 1945: -AS · Gippert 1987: -OS · OSM keeps the dispute in the tag"),
        size=13, color=vu.TEXT_MUTED, italic=True))
    p.append(_scholars(X + 110, y1 + 68, m["scholars"]["ciic81"], lang))

    lane2, ry = y1 + 112, y1 + 170
    p.append(vu.case_node(xs[0], ry, NW, vu.t(lang, "Stein CIIC 81", "Stone CIIC 81"),
                          "Q130529871", {"G": "pot", "W": "ok", "O": "ok", "F": "ok"},
                          kind="object"))
    p.append(vu.case_node(xs[1], ry, NW, "CASSITTAS", f"{persons['CASSITTAS']['wikidata']} · OP400067",
                          {"G": "none", "W": "ok", "O": "none", "F": "ok"}, kind="concept"))
    p.append(vu.case_node(xs[2], ry, NW, "CALLITI", f"{persons['CALLITI']['wikidata']} · OP400061",
                          {"G": "none", "W": "ok", "O": "none", "F": "ok"}, kind="concept"))
    p.append(vu.case_node(xs[3], ry, NW, "Cailtrige", vu.t(
        lang, "Ceinéal Caollaidhe · Sippe", "Ceinéal Caollaidhe · kin group"),
        {"G": "pot", "W": "open", "O": "none", "F": "open"}, kind="concept"))
    p.append(vu.case_node(xs[4], ry, NW, "Eoghanachta", vu.t(lang, "Dynastie", "dynasty"),
                          {"G": "check", "W": "open", "O": "none", "F": "open"}, kind="concept"))
    p.append(vu.gnd_slot(xs[3] + NW / 2, lane2, vu.t(lang, "GND denkbar", "GND conceivable"),
                         "pot", ry))
    p.append(vu.gnd_slot(xs[4] + NW / 2, lane2, vu.t(lang, "GND prüfen", "check the GND"),
                         "check", ry))
    for i, label in enumerate((vu.t(lang, "Inschrift nennt", "inscription names"),
                               "MAQI MUCOI", "O’Brien 2021", vu.t(lang, "Teil von", "part of"))):
        p.append(vu.svg_arrow_labeled(xs[i] + NW, ry + NH / 2, xs[i + 1], ry + NH / 2, label,
                                      font_size=11))
    ex = xs[5] - 30
    p.append(f'<rect x="{ex}" y="{ry}" width="260" height="{NH}" rx="10" fill="#ffffff" '
             f'stroke="{vu.OPEN_STROKE}" stroke-width="1.4" stroke-dasharray="6 4"/>')
    p.append(T(ex + 130, ry + NH / 2, vu.t(lang, "Ort? · kein Gebiet benannt",
                                           "place? · no territory named"),
               size=14, weight=500, color=vu.OPEN_STROKE, anchor="middle", baseline="central"))
    p.append(vu.svg_arrow(xs[4] + NW, ry + NH / 2, ex, ry + NH / 2, dashed=True))
    chip, _ = vu.svg_chip(X, ry + 96, vu.t(
        lang, "Hier bleibt die Kette offen: Die Sippe ist belegt, ein Gebiet mit Geometrie nicht.",
        "Here the chain stays open: the kin group is attested, a territory with a geometry is not."),
        OPEN, size=13, h=28, dashed=True)
    p.append(chip)

    p.append(vu.svg_legend(X, 938, [
        (vu.t(lang, "GND", "GND"), GND),
        (vu.t(lang, "Wikidata / Wikibase", "Wikidata / Wikibase"), WD),
        ("OpenStreetMap", OSM),
        (vu.t(lang, "Fach-Hubs", "subject hubs"), AGG),
    ], columns=4, col_w=190))
    p.append(_gnd_legend(X, 972, lang))
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
