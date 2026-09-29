#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_07_geo_lod.py -- case study geo-lod: two findspots, the same grid
=======================================================================

The third case study on the grid recorded in PRIMER.md (A4), after the Ogham
stones (step 05) and the holy wells (step 06):

  A  ``rollen``          who holds what -- and what the two source datasets
                         hold about themselves, counted from their own tables
  B  ``ortskette``       the chain of places, and how far up it you have to
                         climb before a record of any kind exists
  C  ``graph-dahinter``  what hangs off the findspot: a tephra layer that ends
                         at another place 862 km away, and a speleothem series
                         whose only statement about a place is prose

The pair is chosen for the depth at which each one is anchored. Franchthi Cave
is a findspot of the Campanian Ignimbrite dataset, ``fsl:high``, linked by
``skos:closeMatch`` to both a Wikidata item and an OSM node, and it turns out
to have a GND record as well -- one that nothing in Wikidata points at. Liang
Luar is a SISAL cave site on Flores with more than 2,700 δ¹⁸O values and no
identifier of any kind, so the nearest thing that can be named is a regency
and, above that, the island.

Inputs (all under ``data/raw/``):

* ``geolod/ci_findspots.csv``        the 74 CI findspots; every count in
                                     figure A is counted from this table
* ``geolod/sisal_sites.csv``         the 305 SISAL sites with the archaeology
                                     and identifier columns
* ``geolod/*_excerpt.ttl``           the RDF the two figures quote from, so
                                     the predicates shown are read, not typed
* ``wikidata/*.json``                the items of both chains
* ``osm/boundaries-argolis.geojson`` Argolis, Ermionida and the cave node
* ``osm/boundaries-campania.geojson``Naples, Pozzuoli and the caldera rim
* ``osm/boundaries-flores.geojson``  Flores and the Manggarai regency
* ``osm/relation_9854999.xml``       Susak, as the evidence for the country
                                     mismatch noted in figure A
* ``manual/geolod.yaml``             GND numbers from the GND Explorer, map
                                     windows and the labels of everything that
                                     has no Wikidata JSON of its own
"""

from __future__ import annotations

import csv
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
OUT = vu.OUT_DIRS["07-geo-lod"]

GND, WD, AGG, OSM = vu.GND, vu.COMMUNITY, vu.AGGREGATOR, vu.OSM
UNC = {"fill": vu.UNCERTAIN_FILL, "stroke": vu.UNCERTAIN_STROKE}
OPEN = {"fill": "#ffffff", "stroke": vu.OPEN_STROKE}
T = vu.svg_text


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
def _ci_counts(rows: list[dict]) -> dict:
    """Everything figure A says about the CI dataset, counted from the table."""
    levels: dict[str, int] = {}
    types: set[str] = set()
    for row in rows:
        key = row["certainty"].replace("fsl:", "")
        levels[key] = levels.get(key, 0) + 1
        for spatial in row["spatialtype"].split(";"):
            spatial = spatial.strip()
            if spatial:
                types.add(spatial)
    return {
        "n": len(rows),
        "levels": levels,
        "types": len(types),
        "wikidata": sum(1 for r in rows if "wikidata.org" in r["relatedto"]),
        "osm": sum(1 for r in rows if "openstreetmap.org" in r["relatedto"]),
        "both": sum(1 for r in rows
                    if "wikidata.org" in r["relatedto"] and "openstreetmap.org" in r["relatedto"]),
        "geonames": sum(1 for r in rows if "geonames" in r["relatedto"]),
    }


def _sisal_counts(rows: list[dict]) -> dict:
    arch = [r for r in rows if r["isArchaeologicalSite"] == "true"]
    return {
        "n": len(rows),
        "arch": len(arch),
        "linked": sum(1 for r in arch if r["wikidata_qid"] and r["osm_id"]),
        "unesco": sum(1 for r in rows if r["isUNESCO"] == "yes"),
    }


def _wkt_point(wkt: str) -> tuple[float, float]:
    """(lon, lat) from a ``POINT(lon lat)`` literal, with or without a CRS."""
    inner = wkt[wkt.index("(") + 1:wkt.index(")")]
    lon, lat = inner.split()
    return float(lon), float(lat)


def _ttl_values(path: Path) -> dict[str, dict[str, list[str]]]:
    """Predicate -> object lists per subject, read with rdflib so that what the
    figures print is what the RDF says (short names, prefixes resolved back)."""
    from rdflib import Graph

    graph = Graph()
    graph.parse(path, format="turtle")
    prefixes = {str(ns): pfx for pfx, ns in graph.namespaces()}

    def short(term) -> str:
        text = str(term)
        for uri, pfx in sorted(prefixes.items(), key=lambda kv: -len(kv[0])):
            if uri and text.startswith(uri):
                return f"{pfx}:{text[len(uri):]}"
        return text

    from rdflib.term import URIRef

    out: dict[str, dict[str, list[str]]] = {}
    for s, p, o in graph:
        out.setdefault(short(s), {}).setdefault(short(p), []).append(
            short(o) if isinstance(o, URIRef) else str(o))
    for subject in out.values():
        for values in subject.values():
            values.sort()
    return out


def load() -> dict:
    manual = yaml.safe_load((RAW / "manual" / "geolod.yaml").read_text(encoding="utf-8"))
    ci_rows = list(csv.DictReader((RAW / "geolod" / "ci_findspots.csv").open(encoding="utf-8")))
    sisal_rows = list(csv.DictReader((RAW / "geolod" / "sisal_sites.csv").open(encoding="utf-8")))
    by_id = {int(r["id"]): r for r in ci_rows}
    sisal_by_id = {int(r["sisal_site_id"]): r for r in sisal_rows}

    susak = ET.parse(RAW / "osm" / "relation_9854999.xml").getroot()[0]
    susak_tags = {t.get("k"): t.get("v") for t in susak.findall("tag")}

    d = {
        "m": manual,
        "ci": _ci_counts(ci_rows),
        "sisal": _sisal_counts(sisal_rows),
        "ci_row": {45: by_id[45], 22: by_id[22], 48: by_id[48]},
        "sisal_row": {104: sisal_by_id[104], 77: sisal_by_id[77]},
        "wd": {qid: vu.load_wikidata(qid) for qid in ("Q1441331", "Q191897", "Q12649101", "Q755123",
                                         "Q148440", "Q5061", "Q3803", "Q374096")},
        "geo": {"argolis": vu.load_geojson("boundaries-argolis"),
                "campania": vu.load_geojson("boundaries-campania"),
                "flores": vu.load_geojson("boundaries-flores")},
        "ttl": {"ci": _ttl_values(RAW / "geolod" / "ci_findspots_excerpt.ttl"),
                "sisal": _ttl_values(RAW / "geolod" / "sisal_sites_excerpt.ttl")},
        "susak": susak_tags,
    }
    d["point"] = {
        "franchthi": _wkt_point(by_id[45]["wkt"]),
        "campi": _wkt_point(by_id[22]["wkt"]),
        "liangluar": _wkt_point(sisal_by_id[104]["wkt"]),
    }
    lon1, lat1 = d["point"]["franchthi"]
    lon2, lat2 = d["point"]["campi"]
    d["tephra_km"] = vu.haversine_km(lat1, lon1, lat2, lon2)
    return d


# --------------------------------------------------------------------------- #
# Figure A -- who holds what
# --------------------------------------------------------------------------- #
def _fig_a(d: dict, lang: str) -> str:
    m, ci, sisal = d["m"], d["ci"], d["sisal"]
    site_a, site_b = m["sites"]["franchthi"], m["sites"]["liangluar"]
    probe = m["gnd_probe"]
    de = lang == "de"
    p = [vu.svg_open(vu.t(lang, "Wer hält was: zwei Fundstellen aus zwei Fachdatensätzen",
                          "Who holds what: two findspots from two research datasets"))]
    LX = vu.MARGIN_X
    C1, C2, CW = vu.CASE_C1, vu.CASE_C2, vu.CASE_CW

    headers = [
        (C1, site_a["title_de" if de else "title_en"],
         f"{site_a['dataset_de' if de else 'dataset_en']} · {site_a['wikidata']} · {site_a['osm']}",
         vu.t(lang, "fsl:high · in jede Richtung verlinkt",
              "fsl:high · linked in every direction"), WD),
        (C2, site_b["title_de" if de else "title_en"],
         vu.t(lang, f"{site_b['dataset_de']} · kein QID · kein OSM-Objekt · keine GND-Nummer",
              f"{site_b['dataset_en']} · no QID · no OSM object · no GND number"),
         site_b["note_de" if de else "note_en"], OPEN),
    ]
    for (cx, title, ids, note, colors), key in zip(headers, ("franchthi", "liangluar")):
        shots = [(RAW / "images" / s["file"], s["crop"]) for s in m["images"][key]]
        p.append(vu.case_header(cx, title, ids, note, colors, images=shots,
                                caption=m["captions"][key]["de" if de else "en"]))

    p.append(f'<line x1="{LX}" y1="{vu.CASE_RULE_Y_IMG}" x2="{C2 + CW}" '
             f'y2="{vu.CASE_RULE_Y_IMG}" stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')

    rows = [
        ("GND", GND, vu.CASE_ROW_TOP_IMG, 140, [
            ("ok", vu.t(lang, "der Ort ist da — die Verknüpfung fehlt",
                        "the place is there — the link is not"), [
                (f"{site_a['gnd_label']} · GND {site_a['gnd']} · {site_a['gnd_type']} "
                 f"({vu.t(lang, site_a['gnd_type_de'], site_a['gnd_type_en'])})", "gnd"),
                (vu.t(lang,
                      "GND-Systematik " + " · ".join(site_a["gnd_systematik_de"]),
                      "GND classification " + " · ".join(site_a["gnd_systematik_en"])), "gnd"),
                (vu.t(lang, f"{site_a['wikidata']} hat kein P227 — aus Wikidata ist der Satz "
                            f"nicht erreichbar",
                      f"{site_a['wikidata']} carries no P227 — the record cannot be reached "
                      f"from Wikidata"), "unc"),
            ]),
            ("none", vu.t(lang, "kein Satz, auch keiner daneben",
                          "no record, and none beside it either"), [
                (vu.t(lang, f"Liang Luar: {probe['liangluar_hits']} Treffer",
                      f"Liang Luar: {probe['liangluar_hits']} hits"), "open"),
                (vu.t(lang, f"Manggarai: {probe['manggarai_note_de']}",
                      f"Manggarai: {probe['manggarai_note_en']}"), "open"),
                (vu.t(lang, "Flores · GND 4098001-7 — erst zwei Ebenen höher",
                      "Flores · GND 4098001-7 — only two levels up"), "gnd"),
            ]),
        ]),
        (vu.t(lang, "Wikidata / Wikibase", "Wikidata / Wikibase"), WD, vu.CASE_ROW_TOP_IMG + 148, 168, [
            ("ok", vu.t(lang, "Item mit Koordinate, Denkmalnummer und OSM-Verweis",
                        "an item with a coordinate, a monument number and an OSM link"), [
                (f"{site_a['wikidata']} · P625 "
                 + vu.fmt_num(d["point"]["franchthi"][1], lang, 4) + " / "
                 + vu.fmt_num(d["point"]["franchthi"][0], lang, 4), "ok"),
                ("P11693 OSM node 1221172611 · P131 Q616733", "ok"),
                (f"P2186 {site_a['heritage_id']} · P276 Q1549738", "ok"),
                (vu.t(lang, "P227 wäre die eine fehlende Aussage",
                      "P227 would be the one missing statement"), "open"),
            ]),
            ("none", vu.t(lang, "kein Item — die Kette beginnt erst darüber",
                          "no item — the chain only starts above it"), [
                (vu.t(lang, "Liang Luar: kein QID in SISAL v3",
                      "Liang Luar: no QID in SISAL v3"), "open"),
                ("Q14143 Kabupaten Manggarai · rel 11228382", "ok"),
                ("Q148440 Flores · P402 rel 7219477 · P227 4098001-7", "ok"),
                (vu.t(lang, "Q5061 Ost-Nusa-Tenggara · P402 rel 2396778 · P227",
                      "Q5061 East Nusa Tenggara · P402 rel 2396778 · P227"), "ok"),
            ]),
        ]),
        ("OpenStreetMap", OSM, vu.CASE_ROW_TOP_IMG + 324, 140, [
            ("ok", vu.t(lang, "Punkt mit Typangabe und Rückverweis",
                        "a point with a type and a link back"), [
                ("node 1221172611 · historic=archaeological_site", "ok"),
                ("archaeological_site=settlement · name:en=Franchthi Cave", "ok"),
                (vu.t(lang, "wikidata=Q1441331 — die Rückrichtung steht im Tag",
                      "wikidata=Q1441331 — the way back is in the tag"), "ok"),
            ]),
            ("none", vu.t(lang, "die Höhle selbst fehlt, der Rahmen ist da",
                          "the cave itself is missing, the frame around it is not"), [
                (vu.t(lang, "kein Objekt zur Höhle", "no object for the cave"), "open"),
                ("rel 11228382 Manggarai · admin_level=5", "ok"),
                ("rel 7219477 Flores · place=island", "ok"),
            ]),
        ]),
        (vu.t(lang, "Fachdaten", "research data"), AGG, vu.CASE_ROW_TOP_IMG + 472, 140, [
            ("ok", vu.t(lang, "belegt, datiert, und mit Methode versehen",
                        "referenced, dated, and with its method recorded"), [
                ("geolod:hasCertaintyLevel fsl:high · fsl:Cave + fsl:ArchaeologicalSite", "ok"),
                ("skos:closeMatch → Q1441331 + OSM node 1221172611", "ok"),
                (f"{m['sources']['ci_de' if de else 'ci_en']} · fsl:Georeferencing · ORCID", "ok"),
            ]),
            ("ok", vu.t(lang, "dichter belegt als die meisten — nur eben ohne ID",
                        "better documented than most — only without an identifier"), [
                (vu.t(lang, f"über 2 700 δ¹⁸O-Werte · {site_b['elevation_m']} m ü. NN",
                      f"more than 2,700 δ¹⁸O values · {site_b['elevation_m']} m a.s.l."), "ok"),
                ("isArchaeologicalSite · Hominin Site", "ok"),
                (vu.t(lang, f"{sisal['linked']} von {sisal['arch']} archäologischen "
                            f"SISAL-Standorten haben QID und OSM-ID",
                      f"{sisal['linked']} of {sisal['arch']} archaeological SISAL sites have a "
                      f"QID and an OSM id"), "open"),
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
        ("unc", vu.t(lang, "zu prüfen", "to be checked")),
    ]))
    p.append(vu.svg_close())
    return "\n".join(p)


# --------------------------------------------------------------------------- #
# Figure B -- the chain of places
# --------------------------------------------------------------------------- #
def _fig_b(d: dict, lang: str) -> str:
    m = d["m"]
    de = lang == "de"
    p = [vu.svg_open(vu.t(lang, "Ortsketten: wie weit hinauf, bis etwas verzeichnet ist",
                          "Chains of places: how far up before anything is recorded"))]
    MX, MW = vu.MARGIN_X, 470
    NW, NH = 196, 58
    xs = vu.chain_xs(4, node_w=NW)

    bands = [
        dict(key="franchthi", y0=40, map_h=342, collection="argolis",
             outer="relation/937635", inner="relation/2185768",
             locator_label=vu.t(lang, "Argolis", "Argolis"),
             inner_label_de="Gemeinde Ermionida (grün) im Regionalbezirk Argolis",
             inner_label_en="municipality of Ermionida (green) in the Argolis regional unit",
             headline=vu.t(lang, "verlinkt bis auf die Höhle hinunter",
                           "linked all the way down to the cave"),
             marker=vu.t(lang, "Höhle", "cave")),
        dict(key="liangluar", y0=520, map_h=322, collection="flores",
             outer="relation/7219477", inner="relation/11228382",
             locator_label=vu.t(lang, "Flores", "Flores"),
             inner_label_de="Kabupaten Manggarai (grün) auf der Insel Flores",
             inner_label_en="Manggarai regency (green) on the island of Flores",
             headline=vu.t(lang, "erst zwei Ebenen höher verzeichnet",
                           "only recorded two levels further up"),
             marker=vu.t(lang, "Höhle", "cave")),
    ]

    for band in bands:
        key, y0, map_h = band["key"], band["y0"], band["map_h"]
        site = m["sites"][key]
        collection = d["geo"][band["collection"]]
        outer = vu.geo_feature(collection, band["outer"])
        inner = vu.geo_feature(collection, band["inner"])

        p.append(T(MX, y0 + 16, site["title_de" if de else "title_en"], size=20, weight=500))
        p.append(T(MX + 370, y0 + 16, band["headline"], size=13.5, color=vu.TEXT_MUTED))

        markup, project = vu.case_map(MX, y0 + 34, MW, map_h, tuple(m["maps"][key]), f"map-{key}")
        p.append(markup)
        p.append(vu.geo_draw(outer, project, fill=vu.LAND_FILL, stroke=vu.LAND_STROKE, width=1.2))
        p.append(vu.geo_draw(inner, project, fill=OSM["fill"], stroke=OSM["stroke"], width=1.4))
        px, py = project(*d["point"][key])
        p.append(vu.svg_marker(px, py, "1", {"fill": "#ffffff", "stroke": vu.TEXT_DARK}))
        p.append(vu.case_map_frame(MX, y0 + 34, MW, map_h))
        # bottom-right, so that the in-map key above it keeps the full width
        p.append(vu.case_locator(outer, MX + MW - 116, y0 + 34 + map_h - 140,
                                 102, 128, band["locator_label"],
                                 point=d["point"][key]))
        backdrop_w = vu.text_width(vu.t(lang, band["inner_label_de"], band["inner_label_en"]),
                                   11.5) + 16
        p.append(f'<rect x="{MX + 8}" y="{y0 + 46}" width="{backdrop_w:.0f}" height="22" rx="6" '
                 f'fill="#ffffff" fill-opacity="0.82"/>')
        p.append(T(MX + 16, y0 + 58, vu.t(lang, band["inner_label_de"], band["inner_label_en"]),
                   size=11.5, color=OSM["stroke"], baseline="central"))
        p.append(T(MX + MW, y0 + map_h + 52, vu.t(
            lang, "Flächen: © OpenStreetMap-Mitwirkende, ODbL",
            "areas: © OpenStreetMap contributors, ODbL"),
            size=10.5, color=vu.TEXT_MUTED, anchor="end", baseline="central"))

        # ---- the chain itself
        lane, ry = y0 + 44, y0 + 150
        chain = m["chain"][key]
        for i, node in enumerate(chain):
            p.append(vu.chain_node(node, lang, xs[i], ry, NW))
            slot = node.get("gnd_slot")
            if slot:
                label, kind = slot
                if "|" in label:
                    label = vu.t(lang, *label.split("|"))
                p.append(vu.gnd_slot(xs[i] + NW / 2, lane, label, kind, ry))
        p.append(T(xs[0] - 12, lane + 13, "GND", size=14, weight=500, color=GND["stroke"],
                   anchor="end", baseline="central"))
        for i in range(len(chain) - 1):
            p.append(vu.svg_arrow_labeled(xs[i] + NW, ry + NH / 2, xs[i + 1], ry + NH / 2,
                                          "P131", font_size=11))

        # ---- the place beside the chain that is not administrative
        aside = m["aside"][key]
        p.append(vu.case_node(xs[1], ry + 132, NW, aside["name_de" if de else "name_en"],
                              aside["ids"], aside["hubs"], kind="concept"))
        p.append(vu.svg_arrow_L(xs[0] + NW / 2, ry + NH + 32, xs[1], ry + 132 + NH / 2,
                                bend="v", dashed=True))
        note_markup, _ = vu.svg_text_block(xs[2], ry + 132 + 12,
                                           aside["note_de" if de else "note_en"],
                                           330, size=11.5, color=vu.TEXT_MUTED)
        p.append(note_markup)

    # the one red note of this figure: a record that exists and is not reachable
    site_a = m["sites"]["franchthi"]
    note, _ = vu.svg_text_block(xs[0], 436, vu.t(
        lang, f"Der GND-Satz {site_a['gnd']} zur Höhle ist seit {site_a['gnd_changed'][:4]} "
              f"unverändert — {site_a['wikidata']} verweist nicht darauf, und der Satz selbst "
              f"trägt keine Koordinate. Die Verknüpfung ist die kleinere Lücke von beiden.",
        f"The GND record {site_a['gnd']} for the cave has not changed since "
        f"{site_a['gnd_changed'][:4]} — {site_a['wikidata']} does not point at it, and the record "
        f"itself carries no coordinate. Of the two gaps, the link is the smaller one."),
        1090, size=12, color=vu.UNCERTAIN_STROKE)
    p.append(note)

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
    p = [vu.svg_open(vu.t(lang, "Der Graph dahinter: von der Fundstelle zurück zu einem Ort",
                          "The graph behind it: from the findspot back to a place"))]
    X = vu.MARGIN_X
    NW, NH = 196, 58
    xs = vu.chain_xs(5, node_w=NW, x0=X)
    a: list[str] = []          # the two examples are collected separately
    b: list[str] = []          # and centred by ``case_split``
    t2 = m["tephra"]

    # ---------------- Franchthi: the chain ends at another place, 862 km away
    a.append(T(X, 58, vu.t(lang, "Franchthi-Höhle · Fundstelle 45", "Franchthi Cave · findspot 45"),
               size=20, weight=500))
    a.append(T(X + 330, 58, vu.t(
        lang, "die Tephra führt von einem Ort zum anderen — und der zweite ist selbst eine "
              "Fundstelle desselben Datensatzes",
        "the tephra leads from one place to another — and the second is itself a findspot of the "
        "same dataset"), size=13, color=vu.TEXT_MUTED, italic=True))
    ci45 = d["ttl"]["ci"]["ci:cisite_45"]
    chip, _ = vu.svg_chip(
        X, 74,
        "geolod:hasCertaintyLevel " + " ".join(ci45["geolod:hasCertaintyLevel"])
        + " · geolod:hasSpatialType " + " + ".join(ci45["geolod:hasSpatialType"]),
        AGG, size=12)
    a.append(chip)

    top, below = 150, 320
    a.append(vu.case_node(xs[0], top, NW, vu.t(lang, "Franchthi-Höhle", "Franchthi Cave"),
                          "Q1441331 · node 1221172611",
                          {"G": "ok", "W": "ok", "O": "ok", "F": "ok"}, kind="object"))
    a.append(vu.case_node(xs[1], top, NW, vu.t(lang, "Tephra-Lage", "tephra layer"),
                          vu.t(lang, "Campanian Ignimbrite", "Campanian Ignimbrite"),
                          {"G": "none", "W": "ok", "O": "none", "F": "ok"}, kind="concept"))
    a.append(vu.case_node(xs[2], top, NW, vu.t(lang, "Eruption", "eruption"),
                          vu.t(lang, "ca. 39 000 Jahre vor heute", "ca. 39,000 years ago"),
                          {"G": "none", "W": "ok", "O": "none", "F": "ok"}, kind="concept"))
    a.append(vu.case_node(xs[3], top, NW + 60, t2["target"]["name_de" if de else "name_en"],
                          f"{t2['target']['wikidata']} · GND {t2['target']['gnd']}",
                          {"G": "ok", "W": "ok", "O": "ok", "F": "ok"}))
    a.append(vu.svg_arrow_labeled(xs[0] + NW, top + NH / 2, xs[1], top + NH / 2,
                                  vu.t(lang, "enthält", "contains"), font_size=11))
    a.append(vu.svg_arrow_labeled(xs[1] + NW, top + NH / 2, xs[2], top + NH / 2,
                                  vu.t(lang, "stammt aus", "comes from"), font_size=11))
    a.append(vu.svg_arrow_labeled(xs[2] + NW, top + NH / 2, xs[3], top + NH / 2,
                                  vu.t(lang, "Quelle", "source"), font_size=11))
    a.append(T(xs[3] + (NW + 60) / 2, top - 16, vu.t(
        lang, f"{vu.fmt_num(d['tephra_km'], lang, 0)} km entfernt · im selben Datensatz "
              f"Fundstelle {t2['target']['ci_id']}",
        f"{vu.fmt_num(d['tephra_km'], lang, 0)} km away · findspot {t2['target']['ci_id']} of the "
        f"same dataset"), size=11.5, weight=500, anchor="middle"))

    # the second findspot's own entry is where the identifier mismatch sits
    a.append(vu.case_node(xs[3], below, NW + 60, vu.t(lang, "was dort verlinkt ist",
                                                      "what is linked there"),
                          f"{t2['target']['osm_way']} · {t2['target']['osm_node']}",
                          kind="object"))
    a.append(vu.svg_arrow_L(xs[3] + (NW + 60) / 2, top + NH + 30, xs[3] + (NW + 60) / 2,
                            below, bend="v", dashed=True))
    mismatch, _ = vu.svg_text_block(xs[3] - 8, below + NH + 26, vu.t(
        lang, f"im Datensatz steht Node {t2['mismatch_node']} — {t2['mismatch_node_is_de']}; "
              f"die Koordinate der Zeile trifft dagegen genau den richtigen Node.",
        f"the dataset names node {t2['mismatch_node']} — {t2['mismatch_node_is_en']}; the "
        f"coordinate in the same row, however, lands exactly on the correct node."),
        280, size=11, color=vu.UNCERTAIN_STROKE)
    a.append(mismatch)

    # what the findspot is anchored in, below
    anchors = [(vu.t(lang, "Gemeinde Ermionida", "Municipality of Ermionida"), "Q616733 · P131",
                {"G": "none", "W": "ok", "O": "ok", "F": "none"}, "place"),
               (vu.t(lang, "Argolis", "Argolis"), "Q191897 · GND 4002893-8",
                {"G": "ok", "W": "ok", "O": "ok", "F": "ok"}, "place")]
    targets = []
    for i, (title, subtitle, hubs, kind) in enumerate(anchors):
        node_x = xs[i] + 40
        a.append(vu.case_node(node_x, below, NW, title, subtitle, hubs, kind=kind))
        targets.append(node_x + NW / 2)
    a.append(vu.case_fan(xs[0] + NW / 2, top + NH + 30, below - 22, targets,
                  vu.t(lang, "liegt in · P131", "located in · P131")))

    # ---------------- Liang Luar: the chain ends in prose
    y1 = 496
    b.append(T(X, y1 + 20, vu.t(lang, "Liang Luar · SISAL-Standort 104",
                                "Liang Luar · SISAL site 104"), size=20, weight=500))
    b.append(T(X + 330, y1 + 20, vu.t(
        lang, "dieselbe Struktur, nur endet hier jede Kante an einem Satz statt an einer ID",
        "the same structure — only here every edge ends in a sentence instead of an identifier"),
        size=13, color=vu.TEXT_MUTED, italic=True))
    site104 = d["ttl"]["sisal"]["geolod:Cave_site_0104"]
    elevation = site104["geolod:elevation_m"][0].split(".")[0]
    chip, _ = vu.svg_chip(X, y1 + 36, vu.t(
        lang, f"geolod:Cave · geolod:elevation_m {elevation} · "
              f"kein skos:closeMatch, kein owl:sameAs",
        f"geolod:Cave · geolod:elevation_m {elevation} · "
        f"no skos:closeMatch, no owl:sameAs"), AGG, size=12)
    b.append(chip)

    ry, ry2 = y1 + 112, y1 + 282
    b.append(vu.case_node(xs[0], ry, NW, "Liang Luar", vu.t(lang, "SISAL 104 · ohne ID",
                                                            "SISAL 104 · no identifier"),
                          {"G": "none", "W": "none", "O": "none", "F": "ok"}, kind="object"))
    b.append(vu.case_node(xs[1], ry, NW, vu.t(lang, "Speläothem", "speleothem"),
                          vu.t(lang, "über 2 700 δ¹⁸O-Werte", "more than 2,700 δ¹⁸O values"),
                          {"G": "none", "W": "ok", "O": "none", "F": "ok"}, kind="concept"))
    b.append(vu.case_node(xs[2], ry, NW, vu.t(lang, "Klimakurve", "climate record"),
                          vu.t(lang, "datiert, publiziert", "dated, published"),
                          {"G": "none", "W": "ok", "O": "none", "F": "ok"}, kind="concept"))
    b.append(vu.case_node(xs[3], ry, NW + 60, "Homo floresiensis",
                          vu.t(lang, "aus arch_note, ohne Identifikator",
                               "from arch_note, without an identifier"),
                          {"G": "open", "W": "open", "O": "none", "F": "ok"},
                          kind="concept"))
    b.append(vu.svg_arrow_labeled(xs[0] + NW, ry + NH / 2, xs[1], ry + NH / 2,
                                  vu.t(lang, "liefert", "yields"), font_size=11))
    b.append(vu.svg_arrow_labeled(xs[1] + NW, ry + NH / 2, xs[2], ry + NH / 2,
                                  vu.t(lang, "datiert zu", "dated into"), font_size=11))
    b.append(vu.svg_arrow_labeled(xs[2] + NW, ry + NH / 2, xs[3], ry + NH / 2,
                                  vu.t(lang, "Kontext für", "context for"), font_size=11,
                                  dashed=True, marker="arrow-uncertain",
                                  stroke=vu.UNCERTAIN_STROKE, label_color=vu.UNCERTAIN_STROKE))
    claim, _ = vu.svg_text_block(xs[3] - 8, ry + NH + 46, vu.t(
        lang, "„Type site for Homo floresiensis“ steht als Freitext im Datensatz. Ohne QID lässt "
              "sich diese Aussage von außen weder bestätigen noch widerlegen — genau das, was "
              "oben bei den Fundstellen 22 und 48 die IDs geleistet haben.",
        "“Type site for Homo floresiensis” sits in the dataset as free text. Without a QID the "
        "statement can neither be confirmed nor refuted from outside — which is exactly what the "
        "identifiers did for findspots 22 and 48 above."),
        300, size=11, color=vu.UNCERTAIN_STROKE)
    b.append(claim)

    second = [(vu.t(lang, "Kabupaten Manggarai", "Manggarai Regency"), "Q14143 · rel 11228382",
               {"G": "none", "W": "ok", "O": "ok", "F": "none"}, "place"),
              (vu.t(lang, "Insel Flores", "Flores Island"), "Q148440 · GND 4098001-7",
               {"G": "ok", "W": "ok", "O": "ok", "F": "ok"}, "place")]
    targets = []
    for i, (title, subtitle, hubs, kind) in enumerate(second):
        node_x = xs[i] + 40
        b.append(vu.case_node(node_x, ry2, NW, title, subtitle, hubs, kind=kind))
        targets.append(node_x + NW / 2)
    b.append(vu.case_fan(xs[0] + NW / 2, ry + NH + 30, ry2 - 22, targets,
                  vu.t(lang, "verortet über die Koordinate, nicht über eine Aussage",
                       "placed by its coordinate, not by a statement")))

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
