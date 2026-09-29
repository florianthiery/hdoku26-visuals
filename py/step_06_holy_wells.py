#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_06_holy_wells.py -- case study Holy Wells: two wells, the same grid
=======================================================================

Three figures on the grid recorded in PRIMER.md (A4), the same one step 05
uses for the Ogham stones:

  A  ``rollen``          who holds what -- GND, Wikidata/Wikibase, OSM and the
                         subject hubs, plus what the community wrote down for
                         itself in the WikiProject
  B  ``ortskette``       the chain of places: well, civil parish, county, with
                         the diocese beside it as a place that is not
                         administrative at all
  C  ``graph-dahinter``  the saint behind the well, and how far the chain
                         reaches: to a cure and a local abbot, or to a GND
                         record and a cult in France

The two wells are chosen for their geometry: St. Lachtain's Well is an area in
OSM (a walled enclosure, linked through P10689), St. Fiachra's Well is a point
(a node, P11693). That difference is why the second well appears in a query
for P11693 and the first does not.

Inputs (all under ``data/raw/``):

* ``wikidata/*.json``       the two wells, the two saints, the two civil
                            parishes, the county, the diocese, the WikiProject
                            and its concept, and the four sources
* ``osm/way_935503837.xml``, ``osm/node_8515265450.xml``  the two objects
* ``osm/boundaries-kilkenny.geojson``  county and civil parishes, from
                            Overpass (``out geom``)
* ``sparql/holywells-*.json``  the two WikiProject queries; every count in
                            figure A is counted from them at build time
* ``manual/holywells.yaml``  GND numbers, picture credits, map windows and the
                            summary of the WikiProject's own data model
"""

from __future__ import annotations

import json
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "py"))

import yaml  # noqa: E402

import hdoku26_visuals_utils as vu  # noqa: E402

RAW = vu.DATA_RAW
OUT = vu.OUT_DIRS["06-holy-wells"]

GND, WD, AGG, OSM = vu.GND, vu.COMMUNITY, vu.AGGREGATOR, vu.OSM
UNC = {"fill": vu.UNCERTAIN_FILL, "stroke": vu.UNCERTAIN_STROKE}
OPEN = {"fill": "#ffffff", "stroke": vu.OPEN_STROKE}
T = vu.svg_text


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
def _osm_tags(filename: str) -> dict:
    root = ET.parse(RAW / "osm" / filename).getroot()
    element = root[0]
    tags = {t.get("k"): t.get("v") for t in element.findall("tag")}
    tags["_id"], tags["_type"] = element.get("id"), element.tag
    if element.get("lat"):
        tags["_lat"], tags["_lon"] = float(element.get("lat")), float(element.get("lon"))
    return tags


def _counts() -> dict:
    """Every number in figure A, counted from the two WikiProject queries."""
    by_patron = json.loads(
        (RAW / "sparql" / "holywells-by-patron.json").read_text(encoding="utf-8")
    )["results"]["bindings"]
    concept = json.loads(
        (RAW / "sparql" / "holywells-concept.json").read_text(encoding="utf-8")
    )["results"]["bindings"]

    items: dict[str, set[str]] = {}
    genders: dict[str, set[str]] = {}
    for row in by_patron:
        qid = row["item"]["value"].rsplit("/", 1)[-1]
        have = items.setdefault(qid, set())
        for key in ("osm", "smrId", "p708", "img"):
            if key in row:
                have.add(key)
        genders.setdefault(qid, set()).add(row["genderLabel"]["value"])
    return {
        "wells": len(items),
        "osm": sum(1 for v in items.values() if "osm" in v),
        "smr": sum(1 for v in items.values() if "smrId" in v),
        "diocese": sum(1 for v in items.values() if "p708" in v),
        "image": sum(1 for v in items.values() if "img" in v),
        "female": sum(1 for v in genders.values() if "female" in v),
        "male": sum(1 for v in genders.values() if "female" not in v),
        "concept": len({r["item"]["value"] for r in concept}),
    }


def load() -> dict:
    manual = yaml.safe_load((RAW / "manual" / "holywells.yaml").read_text(encoding="utf-8"))
    qids = ("Q121840779", "Q121842432", "Q18674069", "Q953927", "Q60554307", "Q60554717",
            "Q180231", "Q873607", "Q126443484", "Q126443332")
    d = {
        "m": manual,
        "wd": {qid: vu.load_wikidata(qid) for qid in qids},
        "osm": {"lachtain": _osm_tags("way_935503837.xml"),
                "fiachra": _osm_tags("node_8515265450.xml")},
        "geo": json.loads((RAW / "osm" / "boundaries-kilkenny.geojson").read_text(encoding="utf-8")),
        "counts": _counts(),
    }
    for key, qid in (("lachtain", "Q121840779"), ("fiachra", "Q121842432")):
        entity = d["wd"][qid]
        value = entity["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]
        d.setdefault("point", {})[key] = (value["longitude"], value["latitude"])
        d.setdefault("sources", {})[key] = len(entity["claims"].get("P1343", []))
    return d


def _parish_features(d: dict, logainm: str) -> list[dict]:
    """Every OSM relation carrying this Logainm reference. Freshford is mapped
    as two of them (the parish has a detached part), and Wikidata's P402 names
    only one -- so the figure draws what the gazetteer reference says, and says
    where the single link points."""
    return [f for f in d["geo"]["features"]
            if f["properties"].get("boundary") == "civil_parish"
            and f["properties"].get("logainm:ref") == logainm]


# --------------------------------------------------------------------------- #
# Figure A -- who holds what
# --------------------------------------------------------------------------- #
def _fig_a(d: dict, lang: str) -> str:
    m, osm, c = d["m"], d["osm"], d["counts"]
    de = lang == "de"
    p = [vu.svg_open(vu.t(lang, "Wer hält was: zwei heilige Quellen",
                          "Who holds what: two holy wells"))]
    LX = vu.MARGIN_X
    C1, C2, CW = vu.CASE_C1, vu.CASE_C2, vu.CASE_CW

    for cx, key, note_de, note_en in (
            (C1, "lachtain", m["wells"]["lachtain"]["geometry_de"],
             m["wells"]["lachtain"]["geometry_en"]),
            (C2, "fiachra", m["wells"]["fiachra"]["geometry_de"],
             m["wells"]["fiachra"]["geometry_en"])):
        img = m["images"][key]
        well = m["wells"][key]
        p.append(vu.case_header(
            cx, well["title_de" if de else "title_en"],
            f"{well['wikidata']} · SMR {well['smr']} · {well['inventory']}",
            vu.t(lang, note_de, note_en), AGG,
            image=RAW / "images" / img["file"], crop=img["crop"],
            caption=img["caption_de" if de else "caption_en"] + " · " + img["credit"]))

    p.append(f'<line x1="{C1}" y1="{vu.CASE_RULE_Y_IMG}" x2="{C2 + CW}" '
             f'y2="{vu.CASE_RULE_Y_IMG}" stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')

    rows = [
        ("GND", GND, 250, 112, [
            ("none", vu.t(lang, "nichts zum Brunnen, nichts zum Heiligen",
                          "nothing on the well, nothing on the saint"), [
                (vu.t(lang, "Lachtín mac Tarbín: 0 Treffer", "Lachtín mac Tarbín: 0 hits"), "open"),
                (f"County Kilkenny · GND {m['county']['gnd']} · "
                 + vu.t(lang, "in Wikidata über P227", "linked from Wikidata via P227"), "gnd"),
            ]),
            ("ok", vu.t(lang, "der Heilige ist da", "the saint is there"), [
                (f"Fiacrius · GND {m['saints']['fiacre']['gnd']} · P227", "gnd"),
                (vu.t(lang, "für den Brunnen selbst: kein Satz",
                      "for the well itself: no record"), "open"),
            ]),
        ]),
        (vu.t(lang, "Wikidata / Wikibase", "Wikidata / Wikibase"), WD, 370, 186, [
            ("ok", vu.t(lang, "Brunnen, Heilwirkung, Belege", "well, cure, references"), [
                ("Q121840779 · P31 Holy Well Semantic Concept", "ok"),
                (vu.t(lang, "P2175 Blindheit · Augenentzündung",
                      "P2175 blindness · eye infection"), "ok"),
                (vu.t(lang, f"P1343 {d['sources']['lachtain']} Belege · P3342 William Kinsella",
                      f"P1343 {d['sources']['lachtain']} references · P3342 William Kinsella"), "ok"),
                (vu.t(lang, "P10689 OSM-Way · P625 aus OSM",
                      "P10689 OSM way · P625 from OSM"), "ok"),
            ]),
            ("ok", vu.t(lang, "Brunnen, Festtage, Belege", "well, feast days, references"), [
                ("Q121842432 · P31 Holy Well Semantic Concept", "ok"),
                (vu.t(lang, "P841 zwei Festtage · P973 Grabungsberichte",
                      "P841 two feast days · P973 excavation reports"), "ok"),
                (vu.t(lang, f"P1343 {d['sources']['fiachra']} Belege · P2186 Wiki Loves Monuments",
                      f"P1343 {d['sources']['fiachra']} references · P2186 Wiki Loves Monuments"), "ok"),
                (vu.t(lang, "P11693 OSM-Node · P625", "P11693 OSM node · P625"), "ok"),
            ]),
        ]),
        ("OpenStreetMap", OSM, 566, 176, [
            ("ok", vu.t(lang, "Fläche mit Mauer", "an area with a wall"), [
                (f"way {osm['lachtain']['_id']} · place_of_worship=holy_well", "ok"),
                (f"name:etymology:wikidata={osm['lachtain']['name:etymology:wikidata']}", "ok"),
                (f"alt_name={osm['lachtain']['alt_name']} · name:ga={osm['lachtain']['name:ga']}", "ok"),
                (vu.t(lang, "Civil Parish Freshford: zwei Relationen, eine Logainm-Nummer",
                      "civil parish Freshford: two relations, one Logainm number"), "unc"),
            ]),
            ("ok", vu.t(lang, "Punkt mit Zugangszeiten", "a point with opening times"), [
                (f"node {osm['fiachra']['_id']} · natural=spring", "ok"),
                (f"name:etymology:wikidata={osm['fiachra']['name:etymology:wikidata']}", "ok"),
                (vu.t(lang, "access:conditional · service_times (Novene)",
                      "access:conditional · service_times (novena)"), "ok"),
            ]),
        ]),
        (vu.t(lang, "Fach-Hubs", "subject hubs"), AGG, 758, 148, [
            ("ok", vu.t(lang, "Denkmalregister und Erhebung", "monument register and survey"), [
                (f"SMR {m['wells']['lachtain']['smr']}", "ok"),
                (m["wells"]["lachtain"]["inventory"], "ok"),
                (m["project"]["sources_de" if de else "sources_en"], "ok"),
            ]),
            ("ok", vu.t(lang, "Denkmalregister und Grabung", "monument register and excavation"), [
                (f"SMR {m['wells']['fiachra']['smr']}", "ok"),
                (m["wells"]["fiachra"]["inventory"], "ok"),
                ("excavations.ie · Kilkenny Archaeological Society", "ok"),
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
    ]))
    p.append(vu.svg_close())
    return "\n".join(p)


# --------------------------------------------------------------------------- #
# Figure B -- the chain of places
# --------------------------------------------------------------------------- #
def _fig_b(d: dict, lang: str) -> str:
    m, osm = d["m"], d["osm"]
    de = lang == "de"
    p = [vu.svg_open(vu.t(lang, "Ortsketten: Brunnen, Pfarrei, County",
                          "Chains of places: well, civil parish, county"))]
    MX, MW = vu.MARGIN_X, 470
    NW, NH = 196, 58
    xs = vu.chain_xs(4, node_w=NW)

    bands = [
        ("lachtain", 40, 372, "way", vu.t(lang, "Fläche in OSM · P10689", "an area in OSM · P10689")),
        ("fiachra", 520, 322, "node", vu.t(lang, "Punkt in OSM · P11693", "a point in OSM · P11693")),
    ]
    for key, y0, map_h, kind, note in bands:
        well = m["wells"][key]
        parish = well["parish"]
        p.append(T(MX, y0 + 16, well["title_de" if de else "title_en"], size=20, weight=500))
        p.append(T(MX + 330, y0 + 16, note, size=14, color=vu.TEXT_MUTED))

        markup, project = vu.case_map(MX, y0 + 34, MW, map_h, tuple(m["maps"][key]), f"map-{key}")
        p.append(markup)
        p.append(vu.geo_draw(vu.geo_feature(d["geo"], "relation/285980"), project,
                       fill=vu.LAND_FILL, stroke=vu.LAND_STROKE, width=1.0))
        for feature in d["geo"]["features"]:
            if feature["properties"].get("boundary") == "civil_parish":
                p.append(vu.geo_draw(feature, project, fill="none", stroke=vu.LAND_STROKE, width=0.8))
        parts_of_parish = _parish_features(d, parish["logainm"])
        for feature in parts_of_parish:
            p.append(vu.geo_draw(feature, project, fill=OSM["fill"], stroke=OSM["stroke"], width=1.4))
        px, py = project(*d["point"][key])
        p.append(vu.svg_marker(px, py, "1", {"fill": "#ffffff", "stroke": vu.TEXT_DARK}))
        p.append(vu.case_map_frame(MX, y0 + 34, MW, map_h))
        p.append(vu.case_locator(vu.geo_feature(d["geo"], "relation/285980"),
                                 MX + MW - 116, y0 + 34 + map_h - 140, 102, 128,
                                 m["county"]["name"], point=d["point"][key]))
        p.append(T(MX + 14, y0 + 58, vu.t(
            lang, f"Civil Parish {parish['name']} (grün) in den Pfarreien von Kilkenny",
            f"civil parish {parish['name']} (green) among the parishes of Kilkenny"),
            size=11.5, color=OSM["stroke"]))
        if len(parts_of_parish) > 1:
            ids = " · ".join(f["properties"]["@id"].split("/")[-1] for f in parts_of_parish)
            note, _ = vu.svg_text_block(MX + 14, y0 + 78, vu.t(
                lang, f"zwei OSM-Relationen mit derselben Logainm-Nummer {parish['logainm']} "
                      f"({ids}); P402 in Wikidata nennt nur {parish['osm']}",
                f"two OSM relations carry the same Logainm number {parish['logainm']} "
                f"({ids}); P402 in Wikidata names only {parish['osm']}"),
                300, size=11, color=vu.UNCERTAIN_STROKE)
            p.append(note)
        p.append(T(MX + MW, y0 + map_h + 52, vu.t(
            lang, "Flächen: © OpenStreetMap-Mitwirkende, ODbL",
            "areas: © OpenStreetMap contributors, ODbL"),
            size=10.5, color=vu.TEXT_MUTED, anchor="end", baseline="central"))

        lane, ry = y0 + 44, y0 + 150
        chain = [
            (vu.t(lang, "Brunnen", "well") + f" · {well['title_de' if de else 'title_en'].split(' · ')[0]}",
             f"{well['wikidata']} · SMR {well['smr']}",
             {"G": "none", "W": "ok", "O": "ok", "F": "ok"}, "object"),
            (f"Civil Parish {parish['name']}",
             f"{parish['wikidata']} · Logainm {parish['logainm']} · rel {parish['osm']}",
             {"G": "pot", "W": "ok", "O": "ok", "F": "ok"}, "place"),
            (m["county"]["name"],
             f"{m['county']['wikidata']} · GND {m['county']['gnd']} · rel {m['county']['osm']}",
             {"G": "ok", "W": "ok", "O": "ok", "F": "ok"}, "place"),
            (vu.t(lang, "Irland", "Ireland"), "Q27",
             {"G": "ok", "W": "ok", "O": "ok", "F": "ok"}, "place"),
        ]
        for i, (title, subtitle, hubs, node_kind) in enumerate(chain):
            p.append(vu.case_node(xs[i], ry, NW, title, subtitle, hubs, kind=node_kind))
        p.append(vu.gnd_slot(xs[0] + NW / 2, lane, vu.t(lang, "GND denkbar (Objekt)",
                                                        "GND conceivable (object)"), "pot", ry))
        p.append(vu.gnd_slot(xs[1] + NW / 2, lane, vu.t(lang, "GND denkbar", "GND conceivable"),
                             "pot", ry))
        p.append(vu.gnd_slot(xs[2] + NW / 2, lane, f"GND {m['county']['gnd']}", "ok", ry))
        p.append(T(xs[0] - 12, lane + 13, "GND", size=14, weight=500, color=GND["stroke"],
                   anchor="end", baseline="central"))
        for i in range(3):
            p.append(vu.svg_arrow_labeled(xs[i] + NW, ry + NH / 2, xs[i + 1], ry + NH / 2,
                                          "P131", font_size=11))
        # the diocese: a place that is not administrative
        p.append(vu.case_node(xs[1], ry + 132, NW, m["diocese"]["name_de" if de else "name_en"],
                              f"{m['diocese']['wikidata']} · P708",
                              {"G": "open", "W": "ok", "O": "none", "F": "ok"}, kind="concept"))
        p.append(vu.svg_arrow_L(xs[0] + NW / 2, ry + NH + 32, xs[1], ry + 132 + NH / 2,
                                bend="v", dashed=True))
        note_markup, _ = vu.svg_text_block(xs[2], ry + 132 + 14, vu.t(
            lang, "kirchliche Einteilung, keine Verwaltungsgrenze — in OSM gibt es sie nicht",
            "a church division, not an administrative boundary — OSM does not carry it"),
            230, size=11.5, color=vu.TEXT_MUTED)
        p.append(note_markup)

    p.append(f'<line x1="{MX}" y1="505" x2="{vu.CANVAS_W - vu.MARGIN_X}" y2="505" '
             f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')
    p.append(vu.case_legend(MX, lang))
    p.append(vu.svg_close())
    return "\n".join(p)


# --------------------------------------------------------------------------- #
# Figure C -- the saint behind the well
# --------------------------------------------------------------------------- #
def _fig_c(d: dict, lang: str) -> str:
    m, osm = d["m"], d["osm"]
    de = lang == "de"
    p = [vu.svg_open(vu.t(lang, "Der Graph hinter dem Brunnen: der Heilige und sein Ort",
                          "The graph behind the well: the saint and his place"))]
    X = vu.MARGIN_X
    NW, NH = 196, 58
    # Four columns, the last one wider: both halves end at the content edge.
    xs = vu.chain_xs(4, node_w=NW + 60, x0=X)
    a: list[str] = []          # the two examples are collected separately
    b: list[str] = []          # and centred by ``case_split``

    # ---------------- Lachtain: the chain stays local, and it closes
    a.append(T(X, 58, "St. Lachtain's Well", size=20, weight=500))
    a.append(T(X + 250, 58, vu.t(
        lang, "Tobar Lachtain · der Name trägt den Heiligen, OSM hält ihn als Etymologie fest",
        "Tobar Lachtain · the name carries the saint, and OSM records him as the etymology"),
        size=13, color=vu.TEXT_MUTED, italic=True))
    chip, _ = vu.svg_chip(X, 74, f"OSM way {osm['lachtain']['_id']} · "
                                 f"name:etymology:wikidata={osm['lachtain']['name:etymology:wikidata']}",
                          OSM, size=12)
    a.append(chip)

    top, below = 150, 320
    a.append(vu.case_node(xs[0], top, NW, vu.t(lang, "Brunnen", "well"), "Q121840779",
                          {"G": "none", "W": "ok", "O": "ok", "F": "ok"}, kind="object"))
    a.append(vu.case_node(xs[1], top, NW, "Lachtín mac Tarbín", "Q18674069",
                          {"G": "none", "W": "ok", "O": "ok", "F": "open"}, kind="concept"))
    a.append(vu.case_node(xs[2], top, NW, "Civil Parish Freshford", "Q60554307 · Achadh Úr",
                          {"G": "pot", "W": "ok", "O": "ok", "F": "ok"}))
    a.append(vu.svg_arrow_labeled(xs[0] + NW, top + NH / 2, xs[1], top + NH / 2,
                                  vu.t(lang, "benannt nach · P138", "named after · P138"),
                                  font_size=11))
    a.append(vu.svg_arrow_labeled(xs[1] + NW, top + NH / 2, xs[2], top + NH / 2,
                                  vu.t(lang, "Abt von", "abbot of"), font_size=11))
    a.append(T(xs[1] + NW + 6, top - 12, vu.t(
        lang, "aus der Beschreibung, nicht als Aussage",
        "from the description, not a statement"), size=10.5, color=vu.UNCERTAIN_STROKE))
    ex = xs[3]
    a.append(f'<rect x="{ex}" y="{top}" width="{NW + 60}" height="{NH}" rx="10" fill="#ffffff" '
             f'stroke="{vu.OPEN_STROKE}" stroke-width="1.4" stroke-dasharray="6 4"/>')
    a.append(T(ex + (NW + 60) / 2, top + NH / 2 - 8, vu.t(lang, "GND: 0 Treffer", "GND: 0 hits"),
               size=14, weight=500, color=vu.OPEN_STROKE, anchor="middle", baseline="central"))
    a.append(T(ex + (NW + 60) / 2, top + NH / 2 + 12,
               m["saints"]["lachtain"]["reach_de" if de else "reach_en"], size=11,
               color=vu.OPEN_STROKE, anchor="middle", baseline="central"))
    a.append(vu.svg_arrow_elbow(xs[1] + NW / 2, top, ex + (NW + 60) / 2, top,
                                top - 34, dashed=True,
                                label=vu.t(lang, "in der GND gesucht", "looked up in the GND")))
    # the parish contains the well again: the chain closes
    a.append(vu.svg_arrow_elbow(xs[2] + NW / 2, top + NH + 30, xs[0] + NW / 2, top + NH + 30,
                                top + NH + 52,
                                label=vu.t(lang, "enthält den Brunnen", "contains the well")))
    # what the well is said to cure, and who paid for it
    cures = [(vu.t(lang, "Blindheit", "blindness"), "Q10874 · P2175",
              {"G": "open", "W": "ok", "O": "none", "F": "none"}),
             (vu.t(lang, "Augenentzündung", "eye infection"), "Q21925570 · P2175",
              {"G": "open", "W": "ok", "O": "none", "F": "none"}),
             ("William Kinsella", "Q64735653 · P3342",
              {"G": "open", "W": "ok", "O": "none", "F": "ok"})]
    targets = []
    for i, (title, subtitle, hubs) in enumerate(cures):
        node_x = xs[i + 1] - 40
        a.append(vu.case_node(node_x, below, NW, title, subtitle, hubs, kind="concept"))
        targets.append(node_x + NW / 2)
    a.append(vu.case_fan(xs[0] + NW / 2, top + NH + 30, below - 22, targets,
                  vu.t(lang, "heilt · P2175 · bedeutende Person · P3342",
                       "cures · P2175 · significant person · P3342")))

    # ---------------- Fiachra: the chain reaches the GND and France
    y1 = 476
    b.append(T(X, y1 + 20, "St. Fiachra's Well", size=20, weight=500))
    b.append(T(X + 250, y1 + 20, vu.t(
        lang, "derselbe Bau, andere Reichweite: der Patron wird international verehrt",
        "the same kind of structure, a different reach: the patron is venerated internationally"),
        size=13, color=vu.TEXT_MUTED, italic=True))
    chip, _ = vu.svg_chip(X, y1 + 36, f"OSM node {osm['fiachra']['_id']} · "
                                      f"name:etymology:wikidata={osm['fiachra']['name:etymology:wikidata']}",
                          OSM, size=12)
    b.append(chip)

    ry, ry2 = y1 + 112, y1 + 282
    b.append(vu.case_node(xs[0], ry, NW, vu.t(lang, "Brunnen", "well"), "Q121842432",
                          {"G": "none", "W": "ok", "O": "ok", "F": "ok"}, kind="object"))
    b.append(vu.case_node(xs[1], ry, NW, "Fiacre", "Q953927 · P227",
                          {"G": "ok", "W": "ok", "O": "ok", "F": "ok"}, kind="concept"))
    b.append(vu.case_node(xs[2], ry, NW, "Fiacrius", f"GND {m['saints']['fiacre']['gnd']}",
                          {"G": "ok", "W": "ok", "O": "none", "F": "none"}, kind="concept"))
    b.append(vu.case_node(xs[3], ry, NW + 60, vu.t(lang, "Irland und Frankreich",
                                                   "Ireland and France"),
                          m["saints"]["fiacre"]["gnd_countries"],
                          {"G": "ok", "W": "ok", "O": "ok", "F": "open"}))
    b.append(vu.svg_arrow_labeled(xs[0] + NW, ry + NH / 2, xs[1], ry + NH / 2,
                                  vu.t(lang, "benannt nach · P138", "named after · P138"),
                                  font_size=11))
    b.append(vu.svg_arrow_labeled(xs[1] + NW, ry + NH / 2, xs[2], ry + NH / 2, "P227",
                                  font_size=11))
    b.append(vu.svg_arrow_labeled(xs[2] + NW, ry + NH / 2, xs[3], ry + NH / 2,
                                  vu.t(lang, "Länderbezug", "country link"), font_size=11))
    second = [(vu.t(lang, "Festtage", "feast days"), "P841 · 2×",
               {"G": "none", "W": "ok", "O": "none", "F": "none"}, "concept"),
              (vu.t(lang, "Civil Parish Kilferagh", "civil parish Kilferagh"),
               "Q60554717 · Sheastown", {"G": "pot", "W": "ok", "O": "ok", "F": "ok"}, "place")]
    targets = []
    for i, (title, subtitle, hubs, kind) in enumerate(second):
        node_x = xs[i + 1] - 40
        b.append(vu.case_node(node_x, ry2, NW, title, subtitle, hubs, kind=kind))
        targets.append(node_x + NW / 2)
    b.append(vu.case_fan(xs[0] + NW / 2, ry + NH + 30, ry2 - 22, targets,
                  vu.t(lang, "gefeiert an · P841 · liegt in · P131",
                       "celebrated on · P841 · located in · P131")))

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
