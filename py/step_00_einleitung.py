#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_00_einleitung.py -- two introduction figures before figures 01-03
========================================================================

They lead from the knowledge-graph part of the talk to the GND, taking the
c't article (E. Giardina, "Von Karteikarten zur KI. Bibliotheksdaten werden
zum Wissensdrehkreuz für alle", c't 19/2026, pp. 118-121) as the reference.

00a "drei-drehkreuze" -- three hubs. Left: placeholders for two article
    pictures (cover, opener; placed on the slide by hand -- third-party images
    are not embedded) and the example Konrad Zuse, namesake of the venue:
    GND Explorer graph (own screenshot), his two linked places on a schematic
    map of Germany, and a photo (Wolfgang Hunscher, CC BY-SA 3.0). Right: GND, the
    "Wikiversum" and OpenStreetMap with what the article says about the first
    two (figures from ``ct/facts.yaml``), the cooperation it describes, and
    the bridge to OSM, which the article does not mention. Bottom: three
    general quotations (E1 teaser, E2 Kett, E3 author's text).

00b "dicht-und-duenn" -- where the GND graph is dense and where it thins
    out. Top: own GND Explorer screenshots of Tim Berners-Lee and Goethe.
    Bottom left: the GND record Garranes drawn from its Turtle, every edge it
    has, and the three it does not have. Bottom right: F3, F1, F2.

Sources: ``ct/facts.yaml``, ``ct/quotes.yaml``, ``gnd/1248049489.ttl``,
``manual/places.yaml``, ``osm/*.xml`` (licence attribute).

Writes: img/00-einleitung/{drei-drehkreuze,dicht-und-duenn}.{de,en}.{svg,png}
Run standalone: ``python py/step_00_einleitung.py``
"""

from __future__ import annotations

import xml.etree.ElementTree as ET

import yaml
from rdflib import Graph, Namespace, URIRef

import hdoku26_visuals_utils as vu

OUT = vu.OUT_DIRS["00-einleitung"]
RAW = vu.DATA_RAW
GNDO = Namespace("https://d-nb.info/standards/elementset/gnd#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
GND_IRI = URIRef("https://d-nb.info/gnd/1248049489")
UNC = {"fill": vu.UNCERTAIN_FILL, "stroke": vu.UNCERTAIN_STROKE}


def _yaml(*parts):
    return yaml.safe_load(RAW.joinpath(*parts).read_text(encoding="utf-8"))


def _quote(parts, x, y, w, q, lang, *, size=16, min_h=0):
    text = q["de"] if lang == "de" else q["en"]
    who = q["speaker"] if q["speaker"] not in ("author", "indirect") else None
    src = vu.quote_source(q, lang)
    if who:
        src = f"{who} · " + src.split(" · ", 1)[-1]
    card, bottom = vu.svg_quote_card(x, y, w, text, src, lang, size=size, min_h=min_h)
    parts.append(card)
    return bottom


def _qtext(q, lang):
    return q["de"] if lang == "de" else q["en"]


def _group_size(qs, w, h, lang, max_size=30):
    return min(vu.quote_fill_size(_qtext(q, lang), w, h, lang, max_size=max_size) for q in qs)


def _quote_fill(parts, x, y, w, h, q, lang, *, size):
    src = vu.quote_source(q, lang)
    if q["speaker"] not in ("author", "indirect"):
        src = f"{q['speaker']} · " + src.split(" · ", 1)[-1]
    parts.append(vu.svg_quote_fill(x, y, w, h, _qtext(q, lang), src, lang, size=size))


def _pg(lang, page):
    return vu.t(lang, f"S. {page}", f"p. {page}")


# --------------------------------------------------------------------------- #
# 00a -- three hubs
# --------------------------------------------------------------------------- #
def _hub_card(parts, x, y, w, h, colors, kicker, title, rows, footer, *, dashed=False):
    dash = ' stroke-dasharray="7 5"' if dashed else ""
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#ffffff" '
                 f'stroke="{colors["stroke"]}" stroke-width="1.8"{dash}/>')
    parts.append(f'<path d="M {x} {y + 12} Q {x} {y} {x + 12} {y} L {x + w - 12} {y} '
                 f'Q {x + w} {y} {x + w} {y + 12} L {x + w} {y + 62} L {x} {y + 62} Z" fill="{colors["fill"]}"/>')
    parts.append(vu.svg_text(x + 18, y + 25, kicker, size=12, weight=500, color=colors["stroke"]))
    parts.append(vu.svg_text(x + 18, y + 49, title, size=19, weight=500))
    ty = y + 92
    for row in rows:
        block, ty = vu.svg_text_block(x + 18, ty, row, w - 36, size=14, line_h=19)
        parts.append(block)
        ty += 9
    parts.append(vu.svg_text(x + 18, y + h - 14, footer, size=11, color=vu.TEXT_MUTED))


def _zuse(parts, lang, x, y, w, h):
    """Konrad Zuse, whose name the venue carries and whose GND record the
    article shows (p. 119): his GND Explorer graph, the two places it links
    him to on a schematic outline of Germany, and a photo."""
    z = _yaml("manual", "zuse.yaml")
    parts.append(vu.svg_text(x, y + 12, vu.t(lang, "Beispiel Konrad Zuse – Namensgeber des Tagungsorts",
                                             "Example Konrad Zuse – namesake of the venue"),
                             size=14, weight=500, color=vu.GND["stroke"]))
    gy, gh = y + 24, 196
    parts.append(f'<rect x="{x}" y="{gy}" width="{w}" height="{gh}" rx="6" fill="#ffffff" '
                 f'stroke="{vu.LINE_NEUTRAL}" stroke-width="0.8"/>')
    parts.append(vu.svg_image_crop(x + 3, gy + 3, w - 6, gh - 6, RAW / z["graph"]["file"],
                                   tuple(z["graph"]["crop"])))
    parts.append(vu.svg_text(x + w, gy + gh + 15, vu.t(lang, "Screenshot: GND Explorer (DNB), 22.09.2026",
                                                       "Screenshot: GND Explorer (DNB), 2026-09-22"),
                             size=10.5, color=vu.TEXT_MUTED, anchor="end"))
    # photo
    py_, ph = gy + gh + 26, y + h - (gy + gh + 26)
    pw = ph * 354 / 472
    parts.append(vu.svg_image_crop(x, py_, pw, ph, RAW / z["photo"]["file"]))
    # schematic map of Germany with the two places
    import json, math
    rings = json.loads((RAW / "naturalearth" / "germany_outline.json").read_text(encoding="utf-8"))
    lon0, lon1, lat0, lat1 = 5.8, 15.1, 47.2, 55.1
    k = math.cos(math.radians(51.2))
    sc = ph / (lat1 - lat0)
    mx = x + pw + 16

    def pj(lon, lat):
        return mx + (lon - lon0) * k * sc, py_ + (lat1 - lat) * sc

    for poly in rings:
        d = "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in (pj(*pt) for pt in poly["ring"])) + " Z"
        parts.append(f'<path d="{d}" fill="{vu.LAND_FILL}" stroke="{vu.LAND_STROKE}" stroke-width="0.8"/>')
    for i, pl in enumerate(z["places"], start=1):
        px, pyy = pj(pl["lon"], pl["lat"])
        parts.append(vu.svg_marker(px, pyy, str(i), vu.GND, r=8))
    mw = (lon1 - lon0) * k * sc
    # text: the two places, photo credit
    tx = mx + mw + 16
    ty = py_ + 16
    for i, pl in enumerate(z["places"], start=1):
        parts.append(vu.svg_marker(tx + 8, ty - 4, str(i), vu.GND, r=8))
        parts.append(vu.svg_text(tx + 24, ty, f"{pl['relation'][lang]}: {pl['label']}", size=13.5))
        ty += 24
    for k, line in enumerate(vu.t(lang, ["im GND-Graphen verknüpfte Geografika", "(Karte schematisch)"],
                                  ["geographic entities linked in the GND graph", "(map schematic)"])):
        parts.append(vu.svg_text(tx, ty + 12 + k * 17, line, size=12.5, color=vu.TEXT_MUTED))
    parts.append(vu.svg_text(x, y + h + 15, z["photo"]["credit"] if lang == "de" else
                             z["photo"]["credit"].replace("Foto:", "Photo:"), size=10.5, color=vu.TEXT_MUTED))


def build_hubs(lang: str) -> list[str]:
    f = _yaml("ct", "facts.yaml")
    q = _yaml("ct", "quotes.yaml")
    osm_licence = ET.parse(RAW / "osm" / "way_935503837.xml").getroot().get("license", "")
    L = lambda e: e[lang]  # noqa: E731
    parts = [vu.svg_open(vu.t(lang, "Drei Drehkreuze: GND, Wikiversum, OpenStreetMap",
                              "Three hubs: GND, the Wiki universe, OpenStreetMap"))]

    # left, top: placeholders for the two article pictures (placed on the slide)
    img = f["article"]["images"]
    parts.append(vu.svg_image_frame(60, 50, 185, 250, vu.t(lang, "Cover", "cover"), img["cover"]["credit"]))
    parts.append(vu.svg_image_frame(265, 50, 375, 250, vu.t(lang, "Aufmacher", "opener"),
                                    f"c’t 19/2026, {_pg(lang, 118)} · {img['opener']['credit']}"))
    # left, bottom: Konrad Zuse -- GND graph, schematic map, photo
    _zuse(parts, lang, 60, 338, 580, 352)

    # right: three hubs
    top, ch = 50, 400
    gx, gw = 690, 290
    wx, ww = 1030, 290
    ox, ow = 1400, 290
    g, w = f["gnd"], f["wikidata"]
    _hub_card(parts, gx, top, gw, ch, vu.GND, vu.t(lang, "Normdatei", "authority file"), "GND",
              [L(g["records"]), L(g["persons_orgs"]), L(g["licence"]), L(g["services"]),
               vu.t(lang, "Goethe: fast 200 verknüpfte Webquellen (BEACON)",
                    "Goethe: almost 200 linked web sources (BEACON)")],
              f"c’t 19/2026, {_pg(lang, '119–120')}")
    _hub_card(parts, wx, top, ww, ch, vu.COMMUNITY, vu.t(lang, "„Kooperation mit dem Wikiversum“",
                                                           "“Cooperation with the Wiki universe”"),
              "Wikidata · Wikibase",
              [L(w["items"]), L(w["community"]), L(w["software"]),
               vu.t(lang, "offen editierbar, jede Aussage mit Rang und Beleg",
                    "openly editable, every statement with rank and reference")],
              f"c’t 19/2026, {_pg(lang, 120)}")
    _hub_card(parts, ox, top, ow, ch, vu.COMMUNITY, vu.t(lang, "im Artikel nicht erwähnt", "not in the article"),
              "OpenStreetMap",
              [vu.t(lang, "Geometrien: Punkt, Linie, Fläche", "geometries: point, line, polygon"),
               vu.t(lang, "vor Ort kartiert (source=survey)", "mapped on site (source=survey)"),
               vu.t(lang, "Tags verweisen auf Wikidata (wikidata=…)", "tags point to Wikidata (wikidata=…)"),
               "ODbL 1.0" if "odbl" in osm_licence else osm_licence],
              vu.t(lang, "Quelle: OSM-Daten dieses Vortrags", "source: OSM data of this talk"), dashed=True)
    # connectors between the cards (horizontal, double-headed)
    cy = top + ch / 2
    for x1, x2 in ((gx + gw, wx), (wx + ww, ox)):
        parts.append(f'<line x1="{x1 + 3}" y1="{cy}" x2="{x2 - 3}" y2="{cy}" stroke="{vu.ARROW_STROKE}" '
                     f'stroke-width="1.8" marker-start="url(#arrow)" marker-end="url(#arrow)"/>')
    parts.append(vu.svg_text((wx + ww + ox) / 2, cy - 12, "wikidata=", size=11.5, weight=500,
                             color=vu.COMMUNITY["stroke"], anchor="middle"))
    parts.append(vu.svg_text((wx + ww + ox) / 2, cy + 22, "P402 · P10689", size=11.5, weight=500,
                             color=vu.COMMUNITY["stroke"], anchor="middle"))

    # cooperation bar (GND + Wikiversum) and OSM bridge bar
    by, bh = top + ch + 30, 210
    parts.append(f'<rect x="{gx}" y="{by}" width="{wx + ww - gx}" height="{bh}" rx="12" fill="#f7f6f2" '
                 f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1.4"/>')
    parts.append(vu.svg_text(gx + 18, by + 28, vu.t(lang, "Kooperation, die es schon gibt",
                                                    "Cooperation that already exists"),
                             size=15, weight=500))
    ty = by + 58
    for item in f["cooperation"]:
        parts.append(vu.svg_text(gx + 18, ty, "– " + L(item), size=14))
        ty += 30
    parts.append(vu.svg_text(wx + ww - 18, by + bh - 14, f"c’t 19/2026, {_pg(lang, 120)}", size=11,
                             color=vu.TEXT_MUTED, anchor="end"))
    for x in (gx + gw / 2, wx + ww / 2):
        parts.append(vu.svg_arrow(x, top + ch + 2, x, by - 2))
    parts.append(f'<rect x="{ox}" y="{by}" width="{ow}" height="{bh}" rx="12" fill="#ffffff" '
                 f'stroke="{vu.COMMUNITY["stroke"]}" stroke-width="1.4" stroke-dasharray="7 5"/>')
    parts.append(vu.svg_text(ox + 18, by + 28, vu.t(lang, "Die Brücke zu OSM", "The bridge to OSM"),
                             size=15, weight=500, color=vu.COMMUNITY["stroke"]))
    block, _ = vu.svg_text_block(ox + 18, by + 58, vu.t(
        lang, "Wikidata hält OSM-Kennungen (P402 Relation, P10689 Way, P11693 Node), OSM-Tags zeigen zurück. "
              "Hier liegen die Geometrien – Thema der folgenden Grafiken.",
        "Wikidata holds OSM identifiers (P402 relation, P10689 way, P11693 node), OSM tags point back. "
        "This is where the geometries are – the subject of the figures that follow."),
        ow - 36, size=14, line_h=20)
    parts.append(block)
    parts.append(vu.svg_arrow(ox + ow / 2, top + ch + 2, ox + ow / 2, by - 2, stroke=vu.COMMUNITY["stroke"]))

    # article reference line, then three general quotations
    a = f["article"]
    parts.append(vu.svg_text(60, 742, f"„{a['title']}. {a['subtitle']}“" if lang == "de"
                             else f"“{a['title']}. {a['subtitle']}”", size=17, weight=500))
    parts.append(vu.svg_text(vu.CONTENT_X1, 742, f"{a['author']} · {a['issue']}, {_pg(lang, a['pages'])}",
                             size=14, color=vu.TEXT_MUTED, anchor="end"))
    qy = 764
    qw = (vu.CONTENT_X1 - 60 - 2 * 20) / 3
    qh = vu.CONTENT_Y1 - qy
    size = _group_size([q[k] for k in ("E1", "E2", "E3")], qw, qh, lang)
    for i, key in enumerate(("E1", "E2", "E3")):
        _quote_fill(parts, 60 + i * (qw + 20), qy, qw, qh, q[key], lang, size=size)

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"drei-drehkreuze.{lang}", "\n".join(parts), zoom=1.5)


# --------------------------------------------------------------------------- #
# 00b -- dense and thin
# --------------------------------------------------------------------------- #
SHOTS = [  # (file, crop, label)
    ("gnd-explorer-berners-lee.png", (70, 95, 2370, 1150), "Tim Berners-Lee"),
    ("gnd-explorer-goethe.png", (80, 105, 2440, 1150), "Johann Wolfgang von Goethe"),
]


def build_dense(lang: str) -> list[str]:
    q = _yaml("ct", "quotes.yaml")
    places = _yaml("manual", "places.yaml")
    g = Graph()
    g.parse(RAW / "gnd" / "1248049489.ttl", format="turtle")
    gid = str(g.value(GND_IRI, GNDO.gndIdentifier))
    name = str(g.value(GND_IRI, GNDO.preferredNameForThePlaceOrGeographicName))
    broader = str(g.value(GND_IRI, GNDO.broaderTermInstantial)).rsplit("/", 1)[-1]
    area = str(g.value(GND_IRI, GNDO.geographicAreaCode)).rsplit("#", 1)[-1]
    sc = str(g.value(GND_IRI, GNDO.gndSubjectCategory)).rsplit("#", 1)[-1]
    same = [str(o) for o in g.objects(GND_IRI, OWL.sameAs)]

    parts = [vu.svg_open(vu.t(lang, "Dicht und dünn: GND-Graphen im Vergleich", "Dense and thin: GND graphs compared"))]

    # top: two dense graphs, own screenshots
    top_y, top_h = 50, 420
    parts.append(vu.svg_panel(60, top_y, vu.CONTENT_X1 - 60, top_h, vu.GND,
                              vu.t(lang, "Wo die GND dicht ist", "Where the GND is dense"),
                              vu.t(lang, "Personen und ihr Werk – zwei Graphen im GND Explorer",
                                   "Persons and their work – two graphs in the GND Explorer")))
    iw = (vu.CONTENT_X1 - 60 - 60) / 2
    ih = top_h - 58 - 62
    for i, (fname, crop, label) in enumerate(SHOTS):
        ix = 80 + i * (iw + 20)
        iy = top_y + 70
        parts.append(f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="6" fill="#ffffff" '
                     f'stroke="{vu.LINE_NEUTRAL}" stroke-width="0.8"/>')
        parts.append(vu.svg_image_crop(ix + 4, iy + 4, iw - 8, ih - 8, RAW / "screenshots" / fname, crop))
        parts.append(vu.svg_text(ix, iy + ih + 22, label, size=14, weight=500))
        parts.append(vu.svg_text(ix + iw, iy + ih + 22,
                                 vu.t(lang, "Screenshot: GND Explorer (DNB), 22.09.2026",
                                      "Screenshot: GND Explorer (DNB), 2026-09-22"),
                                 size=11, color=vu.TEXT_MUTED, anchor="end"))

    # bottom left: Garranes, every edge
    by = top_y + top_h + 26
    bw = 900
    bh = vu.CONTENT_Y1 - by
    parts.append(vu.svg_panel(60, by, bw, bh, vu.GND, vu.t(lang, "Wo es dünn wird", "Where it thins out"),
                              vu.t(lang, f"GND {gid} „{name}“ – alle Kanten", f"GND {gid} “{name}” – every edge")))
    cx, cy = 60 + bw / 2 - 40, by + 58 + (bh - 58 - 50) / 2
    parts.append(vu.svg_hash_node(cx, cy, 50, name, f"GND {gid}", fill=vu.GND["fill"], stroke=vu.GND["stroke"]))
    edges = [  # (dx, dy, edge label, node label, colors)
        (0, -118, vu.t(lang, "Oberbegriff", "broader term"),
         vu.t(lang, f"Archäologische Stätte · {broader}", f"archaeological site · {broader}"), vu.GND),
        (-270, 0, vu.t(lang, "Land", "country"), vu.t(lang, f"{area} · Irland", f"{area} · Ireland"), vu.GND),
        (270, 0, vu.t(lang, "Systematik", "subject cat."), vu.t(lang, f"{sc} · Archäologie", f"{sc} · archaeology"),
         vu.GND),
        (0, 118, "owl:sameAs", "VIAF" if any("viaf" in s_ for s_ in same) else same[0], vu.AGGREGATOR),
    ]
    for dx, dy, elabel, nlabel, colors in edges:
        nx, ny = cx + dx, cy + dy
        bxw, bxh = max(170, vu.text_width(nlabel, 14) + 34), 40
        if dx == 0:
            y1 = cy - 50 if dy < 0 else cy + 50
            y2 = ny + bxh / 2 if dy < 0 else ny - bxh / 2
            parts.append(vu.svg_arrow(cx, y1, cx, y2 + (2 if dy < 0 else -2), stroke=colors["stroke"]))
            parts.append(vu.svg_text(cx + 10, (y1 + y2) / 2, elabel, size=12, color=vu.TEXT_MUTED, baseline="central"))
        else:
            x1 = cx - 50 if dx < 0 else cx + 50
            x2 = nx + bxw / 2 if dx < 0 else nx - bxw / 2
            parts.append(vu.svg_arrow(x1, cy, x2 + (2 if dx < 0 else -2), cy, stroke=colors["stroke"]))
            parts.append(vu.svg_text((x1 + x2) / 2, cy - 10, elabel, size=12, color=vu.TEXT_MUTED, anchor="middle"))
        parts.append(vu.svg_box(nx - bxw / 2, ny - bxh / 2, bxw, bxh, nlabel, fill=colors["fill"],
                                stroke=colors["stroke"]))
    parts.append(vu.svg_text(60 + bw - 20, by + 90, vu.t(lang, f"externe Links: {len(same)}",
                                                        f"external links: {len(same)}"),
                             size=16, weight=500, color=vu.GND["stroke"], anchor="end"))
    gn_id = places["geonames_3299501"]["source"].split("/")[3]
    missing = [vu.t(lang, "Koordinate", "coordinate"),
               vu.t(lang, "Link zu Wikidata · Logainm · OSM", "link to Wikidata · Logainm · OSM"),
               vu.t(lang, f"GeoNames {gn_id} nur als Text", f"GeoNames {gn_id} as text only")]
    mx, my = 80, vu.CONTENT_Y1 - 42
    parts.append(vu.svg_text(mx, my - 12, vu.t(lang, "nicht im Datensatz:", "not in the record:"), size=12.5,
                             weight=500, color=vu.UNCERTAIN_STROKE))
    for m in missing:
        chip, cw = vu.svg_chip(mx, my, m, UNC, dashed=True, size=12.5, h=26)
        parts.append(chip)
        mx += cw + 12

    # bottom right: three quotations, text filling the boxes
    qx = 60 + bw + 20
    qw = vu.CONTENT_X1 - qx
    gap = 14
    qh = (bh - 2 * gap) / 3
    size = _group_size([q[k] for k in ("F3", "F1", "F2")], qw, qh, lang, max_size=26)
    for i, key in enumerate(("F3", "F1", "F2")):
        _quote_fill(parts, qx, by + i * (qh + gap), qw, qh, q[key], lang, size=size)

    parts.append(vu.svg_close())
    return vu.write_figure(OUT, f"dicht-und-duenn.{lang}", "\n".join(parts), zoom=1.5)


def main() -> list[str]:
    vu.ensure_dirs()
    written = []
    for lang in ("de", "en"):
        written += build_hubs(lang)
        written += build_dense(lang)
    for p in written:
        print(f"  wrote {p}")
    return written


if __name__ == "__main__":
    main()
