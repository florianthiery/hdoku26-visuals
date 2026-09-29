#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_09_poseidon.py -- case study poseidon2lod: two kinds of place name
=======================================================================

The fifth and last case study on the grid recorded in PRIMER.md (A4):

  A  ``rollen``          who holds what -- and what kind of name each dataset
                         uses to say where a person was found
  B  ``ortskette``       the chain of places, with the level beside it that
                         only the GND holds
  C  ``graph-dahinter``  what hangs off the individual: a family written into a
                         label string, and a landscape that has no boundary

The pair is chosen for the *type* of the place name, not for data quality.
AITI_119 comes from the Lech valley package, whose location strings are modern
addresses, building plots, a gravel pit and an industrial estate -- names that
are a few decades old and that OpenStreetMap carries down to the house number.
RKC001 comes from the Avar-period cemetery Rákóczifalva – Bagi-földek, named
after a field: a toponym centuries old that OSM does not carry at all, sitting
in a research landscape ("MiddleTisza") for which the GND holds a whole family
of records and OSM no boundary.

Each hub therefore wins on one side, which is the point of the figure.

Inputs (all under ``data/raw/``):

* ``poseidon/spatial-coverage.csv``      counts over the 213 .janno files of the
                                         Community Archive and over the nodes of
                                         poseidon_LOD.ttl; both sources are far
                                         too large to travel in this repository
* ``poseidon/*.janno``                   the two packages themselves, for
                                         everything said about the examples
* ``poseidon/poseidon_lod_excerpt.ttl``  the RDF of the two individuals and the
                                         spatial nodes they hang on
* ``wikidata/*.json``                    the places of both chains
* ``osm/boundaries-lechtal.geojson``     Kleinaitingen in the Augsburg district,
                                         the named industrial estate and the
                                         Unterer Talweg
* ``osm/boundaries-tisza.geojson``       Rákóczifalva in the Szolnok district
* ``manual/poseidon.yaml``               GND numbers with entity types, the two
                                         chains, map windows and the wording of
                                         the GND findings
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
OUT = vu.OUT_DIRS["09-poseidon"]

GND, WD, AGG, OSM = vu.GND, vu.COMMUNITY, vu.AGGREGATOR, vu.OSM
UNC = {"fill": vu.UNCERTAIN_FILL, "stroke": vu.UNCERTAIN_STROKE}
OPEN = {"fill": "#ffffff", "stroke": vu.OPEN_STROKE}
T = vu.svg_text


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
def _janno(name: str) -> list[dict]:
    with (RAW / "poseidon" / name).open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def _val(row: dict, column: str) -> str:
    value = (row.get(column) or "").strip()
    return "" if value in ("n/a", "N/A", "NA", "?") else value


def _coverage() -> dict:
    out: dict[str, int] = {}
    with (RAW / "poseidon" / "spatial-coverage.csv").open(encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            parts = next(csv.reader([line]))
            if len(parts) == 3 and parts[2].isdigit():
                out[f"{parts[0]}.{parts[1]}"] = int(parts[2])
    return out


def _rdf() -> dict:
    """Labels and outgoing links of the nodes figure C draws, read from the
    excerpt so that what the figure claims is what the RDF says."""
    from rdflib import Graph, URIRef
    from rdflib.namespace import RDFS

    graph = Graph()
    graph.parse(RAW / "poseidon" / "poseidon_lod_excerpt.ttl", format="turtle")
    arno = "http://archaeonatural.cloud/ont/"
    out: dict[str, dict] = {}
    for subject in graph.subjects(unique=True):
        label = graph.value(subject, RDFS.label)
        if label is None:
            continue
        entry = out.setdefault(str(label), {"types": set(), "links": []})
        for o in graph.objects(subject, URIRef(arno + "closeMatch")):
            entry["links"].append(str(o))
        for o in graph.objects(subject, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")):
            entry["types"].add(str(o).replace(arno, "arno:"))
    return out


def load() -> dict:
    manual = yaml.safe_load((RAW / "manual" / "poseidon.yaml").read_text(encoding="utf-8"))
    lech = _janno("2019_Mittnik_BAEurope.janno")
    avar = _janno("2024_GnecchiRuscone_AvarPedigrees.janno")

    aiti = next(r for r in lech if _val(r, "Poseidon_ID") == "AITI_119")
    rkc = next(r for r in avar if _val(r, "Poseidon_ID") == "RKC001")
    kleinaitingen = [r for r in lech
                     if _val(r, "Location") == "Kleinaitingen-Gewerbegebiet Nord"]
    # the pedigree of this package lives inside the Group_Name string
    family = sorted({_val(r, "Poseidon_ID"): _val(r, "Group_Name")
                     for r in kleinaitingen if "." in _val(r, "Group_Name")}.items())
    bagi = [r for r in avar if _val(r, "Site") == "Rákóczifalva - Bagi-földek"]

    d = {
        "m": manual,
        "cov": _coverage(),
        "rdf": _rdf(),
        "row": {"lechtal": aiti, "tisza": rkc},
        "n": {"lechtal": len(kleinaitingen), "tisza": len(bagi),
              "lech_pkg": len(lech), "avar_pkg": len(avar)},
        "family": family,
        "wd": {qid: next(iter(json.loads((RAW / "wikidata" / f"{qid}.json")
                                         .read_text(encoding="utf-8"))["entities"].values()))
               for qid in ("Q512970", "Q10414", "Q945191", "Q831079", "Q645860")},
        "geo": {"lechtal": json.loads((RAW / "osm" / "boundaries-lechtal.geojson")
                                      .read_text(encoding="utf-8")),
                "tisza": json.loads((RAW / "osm" / "boundaries-tisza.geojson")
                                    .read_text(encoding="utf-8"))},
    }
    d["point"] = {key: (float(_val(r, "Longitude")), float(_val(r, "Latitude")))
                  for key, r in d["row"].items()}
    lon1, lat1 = d["point"]["lechtal"]
    lon2, lat2 = d["point"]["tisza"]
    d["km"] = vu.haversine_km(lat1, lon1, lat2, lon2)
    return d


# --------------------------------------------------------------------------- #
# Figure A -- who holds what
# --------------------------------------------------------------------------- #
def _fig_a(d: dict, lang: str) -> str:
    m, cov, probe = d["m"], d["cov"], d["m"]["gnd_probe"]
    de = lang == "de"
    p = [vu.svg_open(vu.t(lang, "Wer hält was: zwei Arten von Ortsnamen",
                          "Who holds what: two kinds of place name"))]
    LX = vu.MARGIN_X
    C1, C2, CW = vu.CASE_C1, vu.CASE_C2, vu.CASE_CW

    for cx, key, colors in ((C1, "lechtal", OSM), (C2, "tisza", GND)):
        site = m["sites"][key]
        row = d["row"][key]
        p.append(vu.case_header(
            cx, site["title_de" if de else "title_en"],
            vu.t(lang, f"{site['individual']} · {site['package']} · {d['n'][key]} Individuen "
                       f"an diesem Ort",
                 f"{site['individual']} · {site['package']} · {d['n'][key]} individuals at "
                 f"this place"),
            site["kind_de" if de else "kind_en"], colors))

    p.append(f'<line x1="{LX}" y1="{vu.CASE_RULE_Y}" x2="{C2 + CW}" y2="{vu.CASE_RULE_Y}" '
             f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')

    lech_locs = m["lechtal_locations"]
    rows = [
        (vu.t(lang, "der Ortsname", "the place name"), AGG, 174, 168, [
            ("ok", vu.t(lang, "moderne Adressen, Baugebiete, eine Kiesgrube",
                        "modern addresses, development plots, a gravel pit"), [
                (f"{lech_locs[1][0]} · {lech_locs[1][1]}", "ok"),
                (f"{lech_locs[2][0]} · {lech_locs[2][1]}", "ok"),
                (f"{lech_locs[6][0]} · {lech_locs[6][1]}", "ok"),
                (vu.t(lang, f"{lech_locs[7][0]} (Firmengelände) · {lech_locs[8][0]}",
                      f"{lech_locs[7][0]} (a company site) · {lech_locs[8][0]}"), "ok"),
            ]),
            ("ok", vu.t(lang, "Gemeinde und Flurname, dazu eine Landschaft",
                        "municipality and field name, plus a landscape"), [
                (vu.t(lang, "Site: Rákóczifalva – Bagi-földek",
                      "Site: Rákóczifalva – Bagi-földek"), "ok"),
                (vu.t(lang, "Location: MiddleTisza — eine Forschungslandschaft",
                      "Location: MiddleTisza — a research landscape"), "ok"),
                (vu.t(lang, "sechs Schreibweisen im Archiv: MiddleTisza, UpperTisza, "
                            "Tisza region, Transtisza region …",
                      "six spellings in the archive: MiddleTisza, UpperTisza, Tisza region, "
                      "Transtisza region …"), "unc"),
            ]),
        ]),
        ("OpenStreetMap", OSM, 350, 140, [
            ("ok", vu.t(lang, "bis zur Hausnummer verzeichnet",
                        "recorded down to the house number"), [
                (m["sites"]["lechtal"]["osm_de" if de else "osm_en"], "ok"),
                (f"{m['talweg']['street']} · {m['talweg']['osm']}", "ok"),
                (vu.t(lang, f"fünf Einträge an dieser Straße: "
                            f"{' · '.join(m['talweg']['entries'])}",
                      f"five entries along that street: "
                      f"{' · '.join(m['talweg']['entries'])}"), "ok"),
            ]),
            ("none", vu.t(lang, "die Flur fehlt, die Gemeinde ist da",
                          "the field is missing, the municipality is there"), [
                (m["sites"]["tisza"]["osm_de" if de else "osm_en"], "open"),
                ("rel 1273070 Rákóczifalva · admin_level=8", "ok"),
                (vu.t(lang, "für „Mitteltheiß“ gibt es keine Grenze",
                      "there is no boundary for “Middle Tisza”"), "open"),
            ]),
        ]),
        ("GND", GND, 498, 140, [
            ("none", vu.t(lang, "für diese Namen nicht gedacht — zu Recht",
                          "not what these names are for — rightly so"), [
                (probe["gewerbegebiet_de" if de else "gewerbegebiet_en"], "open"),
                (f"Kleinaitingen · GND {m['places']['kleinaitingen']['gnd']} · gik", "gnd"),
                (vu.t(lang, f"Haunstetten zweimal: {m['places']['haunstetten']['gnd']} bis "
                            f"{m['places']['haunstetten']['ended']}, danach "
                            f"{m['places']['augsburg_haunstetten']['gnd']}",
                      f"Haunstetten twice: {m['places']['haunstetten']['gnd']} until "
                      f"{m['places']['haunstetten']['ended']}, then "
                      f"{m['places']['augsburg_haunstetten']['gnd']}"), "gnd"),
            ]),
            ("ok", vu.t(lang, "die Landschaft ist da, die Flur nicht",
                        "the landscape is there, the field is not"), [
                (vu.t(lang, f"Suche „Theiß“: {probe['theiss_hits']} Geografika · "
                            f"{probe['theiss_types_de']}",
                      f"search “Theiß”: {probe['theiss_hits']} place records · "
                      f"{probe['theiss_types_en']}"), "gnd"),
                (probe["theiss_examples_de" if de else "theiss_examples_en"], "gnd"),
                (probe["bagifoeldek_de" if de else "bagifoeldek_en"], "open"),
            ]),
        ]),
        (vu.t(lang, "Poseidon / poseidon2lod", "Poseidon / poseidon2lod"), WD, 646, 140, [
            ("none", vu.t(lang, "keine Site-Spalte — im RDF ein Blank Node",
                          "no Site column — a blank node in the RDF"), [
                (vu.t(lang, f"{d['n']['lech_pkg']} Individuen im Paket, Site leer",
                      f"{d['n']['lech_pkg']} individuals in the package, Site empty"), "open"),
                (vu.t(lang, "„Unknown Site used for transitive information flow“",
                      "“Unknown Site used for transitive information flow”"), "unc"),
                (vu.t(lang, "Place „Kleinaitingen-Gewerbegebiet Nord“ ohne arno:closeMatch",
                      "Place “Kleinaitingen-Gewerbegebiet Nord” without arno:closeMatch"),
                 "unc"),
            ]),
            ("ok", vu.t(lang, "Site vorhanden — und trotzdem nicht auflösbar",
                        "Site present — and still not resolvable"), [
                (vu.t(lang, f"{d['n']['avar_pkg']} Individuen im Paket, "
                            f"{d['n']['tisza']} an diesem Fundplatz",
                      f"{d['n']['avar_pkg']} individuals in the package, "
                      f"{d['n']['tisza']} at this findspot"), "ok"),
                (vu.t(lang, "Site und Place beide ohne arno:closeMatch",
                      "Site and Place both without arno:closeMatch"), "unc"),
                (vu.t(lang, "erst das Land trifft — auf beiden Seiten",
                      "only the country matches — on both sides"), "unc"),
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
        ("unc", vu.t(lang, "so im Datensatz", "as recorded")),
    ]))
    p.append(vu.svg_close())
    return "\n".join(p)


# --------------------------------------------------------------------------- #
# Figure B -- the chain of places
# --------------------------------------------------------------------------- #
def _fig_b(d: dict, lang: str) -> str:
    m = d["m"]
    de = lang == "de"
    p = [vu.svg_open(vu.t(lang, "Ortsketten: ein Gewerbegebiet und eine Flur",
                          "Chains of places: an industrial estate and a field"))]
    MX, MW = vu.MARGIN_X, 430
    NW, NH = 176, 58
    xs = vu.chain_xs(5, node_w=NW, x0=535)

    bands = [
        dict(key="lechtal", y0=40, map_h=340, collection="lechtal",
             outer="relation/935162", locator="relation/62622",
             extra=["way/376729440", "way/303424285"],
             locator_label=vu.t(lang, "Landkreis Augsburg", "Augsburg district"),
             inner_label_de="Gewerbegebiet Kleinaitingen (grün) in der Gemeinde",
             inner_label_en="Gewerbegebiet Kleinaitingen (green) inside the municipality",
             headline=vu.t(lang, "der Name liegt unterhalb der Verwaltung",
                           "the name sits below the administrative levels"),
             aside_from=3, note_x=767, note_w=520, note_dy=96),
        dict(key="tisza", y0=520, map_h=320, collection="tisza",
             outer="relation/1273070", locator="relation/2376095",
             extra=[],
             locator_label=vu.t(lang, "Kreis Szolnok", "Szolnok district"),
             inner_label_de="Rákóczifalva — an der Stelle der Flur liegt nichts",
             inner_label_en="Rákóczifalva — there is nothing where the field is",
             headline=vu.t(lang, "der Name liegt daneben, nicht darunter",
                           "the name sits beside the levels, not below them"),
             aside_from=4, note_x=767, note_w=620, note_dy=106, aside_dy=112),
    ]

    for band in bands:
        key, y0, map_h = band["key"], band["y0"], band["map_h"]
        site = m["sites"][key]
        collection = d["geo"][band["collection"]]
        outer = vu.geo_feature(collection, band["outer"])
        locator = vu.geo_feature(collection, band["locator"])

        title = site["title_de" if de else "title_en"]
        p.append(T(MX, y0 + 16, title, size=19, weight=500))
        p.append(T(MX + vu.text_width(title, 19) + 26, y0 + 16, band["headline"],
                   size=13, color=vu.TEXT_MUTED))

        markup, project = vu.case_map(MX, y0 + 34, MW, map_h, tuple(m["maps"][key]), f"map-{key}")
        p.append(markup)
        p.append(vu.geo_draw(outer, project, fill=vu.LAND_FILL, stroke=vu.LAND_STROKE, width=1.2))
        for osm_id in band["extra"]:
            feature = vu.geo_feature(collection, osm_id)
            named = "name" in feature["properties"]
            p.append(vu.geo_draw(feature, project, fill=OSM["fill"] if named else "#eceee7",
                           stroke=OSM["stroke"] if named else vu.LAND_STROKE,
                           width=1.4 if named else 1.0))
        px, py = project(*d["point"][key])
        p.append(vu.svg_marker(px, py, "1", {"fill": "#ffffff", "stroke": vu.TEXT_DARK}))
        p.append(vu.case_map_frame(MX, y0 + 34, MW, map_h))
        p.append(vu.case_locator(locator, MX + MW - 116, y0 + 34 + map_h - 140,
                                 102, 128, band["locator_label"],
                                 point=d["point"][key]))
        label = vu.t(lang, band["inner_label_de"], band["inner_label_en"])
        p.append(f'<rect x="{MX + 8}" y="{y0 + 46}" width="{vu.text_width(label, 11.5) + 16:.0f}" '
                 f'height="22" rx="6" fill="#ffffff" fill-opacity="0.85"/>')
        p.append(T(MX + 16, y0 + 58, label, size=11.5,
                   color=OSM["stroke"] if band["extra"] else vu.UNCERTAIN_STROKE,
                   baseline="central"))
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
                p.append(vu.gnd_slot(xs[i] + NW / 2, lane, label_text, kind, ry, h=24))
        p.append(T(xs[0] - 12, lane + 12, "GND", size=14, weight=500, color=GND["stroke"],
                   anchor="end", baseline="central"))
        for i in range(len(chain) - 1):
            p.append(vu.svg_arrow(xs[i] + NW, ry + NH / 2, xs[i + 1], ry + NH / 2))

        # ---- the level beside the chain that only the GND holds
        aside = m["aside"][key]
        source = xs[band["aside_from"]] + NW / 2
        ady = band.get("aside_dy", 132)
        p.append(vu.case_node(xs[1], ry + ady, NW + 60, aside["name_de" if de else "name_en"],
                              aside["ids_de" if de else "ids_en"], aside["hubs"],
                              kind="concept"))
        p.append(vu.svg_arrow_L(source, ry + NH + 32, xs[1] + NW + 60,
                                ry + ady + NH / 2, bend="v", dashed=True))
        note, _ = vu.svg_text_block(band["note_x"], ry + ady + band["note_dy"],
                                    aside["note_de" if de else "note_en"],
                                    band["note_w"], size=11.5, color=vu.TEXT_MUTED)
        p.append(note)

    p.append(f'<line x1="{MX}" y1="505" x2="{vu.CANVAS_W - vu.MARGIN_X}" y2="505" '
             f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')
    p.append(vu.case_legend(MX, lang))
    p.append(vu.svg_close())
    return "\n".join(p)


# --------------------------------------------------------------------------- #
# Figure C -- what hangs off the individual
# --------------------------------------------------------------------------- #
def _fig_c(d: dict, lang: str) -> str:
    m, terms = d["m"], d["m"]["terms"]
    de = lang == "de"
    aiti, rkc = d["row"]["lechtal"], d["row"]["tisza"]
    p = [vu.svg_open(vu.t(lang, "Der Graph dahinter: eine Familie im Label, eine Landschaft ohne Grenze",
                          "The graph behind it: a family in a label, a landscape without a boundary"))]
    a: list[str] = []          # the two examples are collected separately and
    b: list[str] = []          # then centred in their half by ``case_split``
    X = vu.MARGIN_X
    NW, NH = 196, 58
    # Four columns; the widest node of the last one is NW + 100 with its offset,
    # so both halves finish at the content edge.
    xs = vu.chain_xs(4, node_w=NW + 100, x0=X)

    # ---------------- Lechtal: the pedigree is packed into a string
    head = vu.t(lang, "AITI_119 · Lechtal", "AITI_119 · Lech valley")
    a.append(T(X, 58, head, size=20, weight=500))
    a.append(T(X + vu.text_width(head, 20) + 26, 58, vu.t(
        lang, "die Verwandtschaft steht als Zeichenkette im Gruppennamen — und der Fundort "
              "an einer Adresse",
        "the kinship sits in the group name as a string — and the findspot at an address"),
        size=13, color=vu.TEXT_MUTED, italic=True))
    chip, _ = vu.svg_chip(X, 74, f"¹⁴C {_val(aiti, 'Date_C14_Labnr')} · "
                                 f"{_val(aiti, 'Date_BC_AD_Start')}/{_val(aiti, 'Date_BC_AD_Stop')} · "
                                 f"Y {_val(aiti, 'Y_Haplogroup')}", AGG, size=12)
    a.append(chip)

    top, below = 150, 320
    a.append(vu.case_node(xs[0], top, NW, "AITI_119",
                          vu.t(lang, "männlich · Lechtal", "male · Lech valley"),
                          {"G": "none", "W": "none", "O": "none", "F": "ok"}, kind="object"))
    a.append(vu.case_node(xs[1], top, NW + 60, vu.t(lang, "Familie", "family"),
                          vu.t(lang, f"{len(d['family'])} Individuen im Gruppennamen",
                               f"{len(d['family'])} individuals in the group name"),
                          {"G": "none", "W": "none", "O": "none", "F": "ok"}, kind="concept"))
    a.append(vu.case_node(xs[2] + 60, top, NW, vu.t(lang, "Fundplatz", "discovery site"),
                          vu.t(lang, "Blank Node", "blank node"),
                          {"G": "none", "W": "none", "O": "none", "F": "open"}, kind="object"))
    a.append(vu.case_node(xs[3] + 60, top, NW + 40, "Gewerbegebiet Kleinaitingen",
                          "way 376729440",
                          {"G": "none", "W": "none", "O": "ok", "F": "ok"}))
    a.append(vu.svg_arrow_labeled(xs[0] + NW, top + NH / 2, xs[1], top + NH / 2,
                                  vu.t(lang, "Teil von", "part of"), font_size=11))
    a.append(vu.svg_arrow_labeled(xs[1] + NW + 60, top + NH / 2, xs[2] + 60, top + NH / 2,
                                  vu.t(lang, "gefunden an", "found at"), font_size=11))
    a.append(vu.svg_arrow_labeled(xs[2] + 60 + NW, top + NH / 2, xs[3] + 60, top + NH / 2,
                                  vu.t(lang, "liegt in", "lies in"), font_size=11))
    if d["family"]:
        sample = d["family"][0][1]
        quote, _ = vu.svg_text_block(xs[2] + 60, top + NH + 40, vu.t(
            lang, f"Der Gruppenname lautet „{sample}“. Die Verwandtschaft ist damit maschinell "
                  f"lesbar — aber als Zeichenkette, nicht als Aussage.",
            f"The group name reads “{sample}”. The kinship is machine-readable — but as a "
            f"string, not as a statement."),
            500, size=11, color=vu.UNCERTAIN_STROKE)
        a.append(quote)

    targets = []
    for i, (title, subtitle, hubs, kind) in enumerate([
            (terms["aunjetitz"]["name_de" if de else "name_en"],
             f"GND {terms['aunjetitz']['gnd']} · {terms['aunjetitz']['time']}",
             {"G": "ok", "W": "ok", "O": "none", "F": "ok"}, "concept"),
            (m["places"]["haunstetten"]["gnd"] and vu.t(lang, "Haunstetten", "Haunstetten"),
             vu.t(lang, f"GND {m['places']['haunstetten']['gnd']} → "
                        f"{m['places']['augsburg_haunstetten']['gnd']}",
                  f"GND {m['places']['haunstetten']['gnd']} → "
                  f"{m['places']['augsburg_haunstetten']['gnd']}"),
             {"G": "ok", "W": "open", "O": "ok", "F": "ok"}, "place")]):
        node_x = xs[i] + 40
        a.append(vu.case_node(node_x, below, NW, title, subtitle, hubs, kind=kind))
        targets.append(node_x + NW / 2)
    a.append(vu.case_fan(xs[0] + NW / 2, top + NH + 30, below - 22, targets,
                  vu.t(lang, "Kultur · benachbarte Fundstellen desselben Pakets",
                       "culture · neighbouring findspots of the same package")))

    # ---------------- Tisza: the landscape the GND has and OSM has not
    y1 = 496
    head = vu.t(lang, "RKC001 · Mitteltheiß", "RKC001 · Middle Tisza")
    b.append(T(X, y1 + 20, head, size=20, weight=500))
    b.append(T(X + vu.text_width(head, 20) + 26, y1 + 20, vu.t(
        lang, "hier hat der Fundplatz einen Namen — und die Landschaft darüber gibt es nur "
              "in der GND",
        "here the findspot has a name — and the landscape above it exists only in the GND"),
        size=13, color=vu.TEXT_MUTED, italic=True))
    chip, _ = vu.svg_chip(X, y1 + 36, vu.t(
        lang, f"Datierung {_val(rkc, 'Date_BC_AD_Start')}–{_val(rkc, 'Date_BC_AD_Stop')} · "
              f"Date_Type {_val(rkc, 'Date_Type')} · {d['n']['tisza']} Individuen am Fundplatz",
        f"dated {_val(rkc, 'Date_BC_AD_Start')}–{_val(rkc, 'Date_BC_AD_Stop')} · "
        f"Date_Type {_val(rkc, 'Date_Type')} · {d['n']['tisza']} individuals at the findspot"),
        AGG, size=12)
    b.append(chip)

    ry, ry2 = y1 + 112, y1 + 282
    b.append(vu.case_node(xs[0], ry, NW, "RKC001",
                          vu.t(lang, "weiblich · Awarenzeit", "female · Avar period"),
                          {"G": "none", "W": "none", "O": "none", "F": "ok"}, kind="object"))
    b.append(vu.case_node(xs[1], ry, NW + 40, "Bagi-földek",
                          vu.t(lang, "Flurname · ohne ID", "field name · no id"),
                          {"G": "none", "W": "none", "O": "none", "F": "ok"}, kind="object"))
    b.append(vu.case_node(xs[2] + 40, ry, NW, "Rákóczifalva",
                          f"Q945191 · GND {m['places']['rakoczifalva']['gnd']}",
                          {"G": "ok", "W": "ok", "O": "ok", "F": "none"}))
    b.append(vu.case_node(xs[3] + 40, ry, NW + 40,
                          vu.t(lang, "Mitteltheiß", "Middle Tisza"),
                          vu.t(lang, f"GND-Familie · {m['gnd_probe']['theiss_hits']} Treffer",
                               f"GND family · {m['gnd_probe']['theiss_hits']} hits"),
                          {"G": "ok", "W": "open", "O": "none", "F": "ok"}, kind="concept"))
    b.append(vu.svg_arrow_labeled(xs[0] + NW, ry + NH / 2, xs[1], ry + NH / 2,
                                  vu.t(lang, "gefunden auf", "found on"), font_size=11))
    b.append(vu.svg_arrow_labeled(xs[1] + NW + 40, ry + NH / 2, xs[2] + 40, ry + NH / 2,
                                  vu.t(lang, "Flur von", "field of"), font_size=11))
    b.append(vu.svg_arrow_labeled(xs[2] + 40 + NW, ry + NH / 2, xs[3] + 40, ry + NH / 2,
                                  vu.t(lang, "liegt an der", "lies on the"), font_size=11))
    note, _ = vu.svg_text_block(xs[2] + 40, ry + NH + 44, vu.t(
        lang, f"Die GND führt Theiß selbst als {m['gnd_probe']['theiss_gnd']} (gin und gik) und "
              f"dazu eine ganze Familie von Landschaften. OpenStreetMap hat dafür keine Grenze, "
              f"Wikidata kein Item, das „MiddleTisza“ entspräche.",
        f"The GND holds the Tisza itself as {m['gnd_probe']['theiss_gnd']} (gin and gik) and a "
        f"whole family of landscapes besides. OpenStreetMap has no boundary for them, Wikidata "
        f"no item matching “MiddleTisza”."),
        430, size=11, color=GND["stroke"])
    b.append(note)

    targets = []
    for i, (title, subtitle, hubs, kind) in enumerate([
            (terms["awaren"]["name_de" if de else "name_en"],
             f"GND {terms['awaren']['gnd']} · sie",
             {"G": "ok", "W": "ok", "O": "none", "F": "ok"}, "concept"),
            ("Szolnoki járás", "Q831079 · rel 2376095",
             {"G": "none", "W": "ok", "O": "ok", "F": "none"}, "place")]):
        node_x = xs[i] + 40
        b.append(vu.case_node(node_x, ry2, NW, title, subtitle, hubs, kind=kind))
        targets.append(node_x + NW / 2)
    b.append(vu.case_fan(xs[0] + NW / 2, ry + NH + 30, ry2 - 22, targets,
                  vu.t(lang, "Kultur · Verwaltung", "culture · administration")))
    homonym, _ = vu.svg_text_block(xs[0] + 40, ry2 + NH + 62,
                                   terms["awaren"]["homonym_de" if de else "homonym_en"],
                                   420, size=11, color=vu.UNCERTAIN_STROKE)
    b.append(homonym)

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
