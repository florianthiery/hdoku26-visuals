"""Mockups for the case-study template (Ogham): A roles, B place chain, C graph behind.
Working mock-ups for S5, not wired into main.py. Run: python tmp/s5-ogham/mock_ogham.py"""
import json, math, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "py"))
import hdoku26_visuals_utils as vu

OUT = Path(__file__).resolve().parent / "img"
RAW = vu.DATA_RAW

GND, WD, AGG = vu.GND, vu.COMMUNITY, vu.AGGREGATOR
OSM = {"fill": "#e3eed9", "stroke": "#4f7a2a"}
UNC = {"fill": vu.UNCERTAIN_FILL, "stroke": vu.UNCERTAIN_STROKE}
OPEN = {"fill": "#ffffff", "stroke": "#9a9890"}
HUBS = [("G", "GND", GND), ("W", "Wikidata", WD), ("O", "OSM", OSM), ("F", "Fach-Hubs", AGG)]
T = vu.svg_text


# ------------------------------------------------------------------ shared devices
def status_icon(cx, cy, kind, colors, r=13):
    """ok = filled + check · up = one level up · none = crossed · open = ? (to be filled) · unc = red ?"""
    s = colors["stroke"]
    if kind == "ok":
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{s}"/>'
                f'<path d="M {cx-6} {cy} L {cx-2} {cy+5} L {cx+6} {cy-5}" fill="none" stroke="#fff" '
                f'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "up":
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{s}" stroke-width="2"/>'
                f'<path d="M {cx} {cy+6} L {cx} {cy-6} M {cx-5} {cy-1} L {cx} {cy-6} L {cx+5} {cy-1}" '
                f'fill="none" stroke="{s}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "none":
        g = "#9a9890"
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{g}" stroke-width="1.6"/>'
                f'<path d="M {cx-5} {cy-5} L {cx+5} {cy+5} M {cx+5} {cy-5} L {cx-5} {cy+5}" '
                f'stroke="{g}" stroke-width="2" stroke-linecap="round"/>')
    if kind == "open":
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="#9a9890" stroke-width="1.6" '
                f'stroke-dasharray="3 3"/>' + T(cx, cy + 1, "?", size=15, weight=500, color="#9a9890",
                                                anchor="middle", baseline="central"))
    if kind == "unc":
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{vu.UNCERTAIN_FILL}" stroke="{vu.UNCERTAIN_STROKE}" '
                f'stroke-width="2"/>' + T(cx, cy + 1, "?", size=15, weight=500, color=vu.UNCERTAIN_STROKE,
                                          anchor="middle", baseline="central"))
    raise ValueError(kind)


def hub_bar(cx, y, states):
    """Four squares G W O F centred on cx: ok (hub colour) · none (faint) · open (dashed ?)."""
    w, h, gap = 26, 20, 5
    x0 = cx - (4 * w + 3 * gap) / 2
    out = []
    for i, ((letter, _, col), st) in enumerate(zip(HUBS, states)):
        x = x0 + i * (w + gap)
        if st == "ok":
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{w}" height="{h}" rx="4" fill="{col["fill"]}" '
                       f'stroke="{col["stroke"]}" stroke-width="1.4"/>')
            out.append(T(x + w / 2, y + h / 2 + 1, letter, size=11.5, weight=500, color=col["stroke"],
                         anchor="middle", baseline="central"))
        elif st == "none":
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{w}" height="{h}" rx="4" fill="#fff" '
                       f'stroke="#d3d1ca" stroke-width="1.2"/>')
            out.append(T(x + w / 2, y + h / 2 + 1, letter, size=11.5, color="#c9c7c0",
                         anchor="middle", baseline="central"))
        elif st == "pot":
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{w}" height="{h}" rx="4" fill="#fff" '
                       f'stroke="{col["stroke"]}" stroke-width="1.4" stroke-dasharray="4 2"/>')
            out.append(T(x + w / 2, y + h / 2 + 1, letter, size=11.5, weight=500, color=col["stroke"],
                         anchor="middle", baseline="central"))
        else:
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{w}" height="{h}" rx="4" fill="#fff" '
                       f'stroke="#9a9890" stroke-width="1.2" stroke-dasharray="3 2"/>')
            out.append(T(x + w / 2, y + h / 2 + 1, "?", size=12, weight=500, color="#9a9890",
                         anchor="middle", baseline="central"))
    return "\n".join(out)


def node(x, y, w, title, sub, hubs, *, h=58, kind="place"):
    """Place/entity node: white box, kind-coded stroke, hub bar below."""
    stroke = {"place": vu.TEXT_DARK, "object": vu.TEXT_MUTED, "concept": "#7a5a9a"}[kind]
    rx = 29 if kind == "concept" else 10
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#fff" stroke="{stroke}" '
             f'stroke-width="{1.8 if kind == "place" else 1.4}"/>']
    size = 15
    while size > 11 and vu.text_width(title, size) > w - 20:
        size -= 0.5
    if sub:
        parts.append(T(x + w / 2, y + h / 2 - 8, title, size=size, weight=500, anchor="middle", baseline="central"))
        ss = 11.5
        while ss > 9 and vu.text_width(sub, ss) > w - 16:
            ss -= 0.5
        parts.append(T(x + w / 2, y + h / 2 + 12, sub, size=ss, color=vu.TEXT_MUTED, anchor="middle",
                       baseline="central"))
    else:
        parts.append(T(x + w / 2, y + h / 2, title, size=size, weight=500, anchor="middle", baseline="central"))
    if hubs:
        parts.append(hub_bar(x + w / 2, y + h + 6, hubs))
    return "\n".join(parts)


def legend_bottom(y, lang="de", with_status=True, with_bar=True, with_kinds=False):
    parts, x = [], vu.MARGIN_X
    if with_status:
        for kind, col, label in [("ok", WD, "vorhanden"), ("up", GND, "eine Ebene höher"),
                                 ("none", AGG, "fehlt"), ("open", AGG, "offen (wird ergänzt)"),
                                 ("unc", UNC, "unsicher / umstritten")]:
            parts.append(status_icon(x + 11, y, kind, col, r=10))
            parts.append(T(x + 28, y + 1, label, size=12.5, baseline="central"))
            x += 42 + vu.text_width(label, 12.5)
        x += 30
    if with_bar:
        parts.append(hub_bar(x + 62, y - 10, ["ok", "ok", "ok", "ok"]))
        parts.append(T(x + 132, y + 1, "G GND · W Wikidata/Wikibase · O OpenStreetMap · F Fach-Hubs (Logainm, SMR, CISP, TM)",
                       size=12.5, baseline="central"))
        x += 140 + vu.text_width("G GND · W Wikidata/Wikibase · O OpenStreetMap · F Fach-Hubs (Logainm, SMR, CISP, TM)", 12.5)
    if with_kinds:
        x += 30
        parts.append(f'<rect x="{x}" y="{y-9}" width="26" height="18" rx="4" fill="#fff" stroke="{vu.TEXT_DARK}" stroke-width="1.8"/>')
        parts.append(T(x + 34, y + 1, "Ort", size=12.5, baseline="central"))
        x += 70
        parts.append(f'<rect x="{x}" y="{y-9}" width="26" height="18" rx="9" fill="#fff" stroke="#7a5a9a" stroke-width="1.4"/>')
        parts.append(T(x + 34, y + 1, "Begriff / Name", size=12.5, baseline="central"))
    return "\n".join(parts)


def photo(x, y, w, h, label):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#efeee9"/>'
            + T(x + w / 2, y + h / 2, label, size=12.5, color=vu.TEXT_MUTED, anchor="middle", baseline="central"))


# ------------------------------------------------------------------ Figure A
def cell(x, y, w, h, colors, status, headline, chips):
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#fff" stroke="{colors["stroke"]}" '
             f'stroke-width="1.2" stroke-opacity="0.6"/>']
    parts.append(status_icon(x + 24, y + 24, status, UNC if status == "unc" else colors))
    parts.append(T(x + 46, y + 25, headline, size=14, weight=500, baseline="central"))
    cy = y + 46
    for label, st in chips:
        col = {"ok": colors, "open": OPEN, "unc": UNC, "gnd": GND}[st]
        m, _ = vu.svg_chip(x + 14, cy, label, col, width=w - 28, align="start", dashed=(st == "open"))
        parts.append(m)
        cy += 28
    return "\n".join(parts)


def fig_a():
    p = [vu.svg_open("Mockup A – Rollen der Hubs für zwei Ogham-Steine")]
    LX, LW = vu.MARGIN_X, 170
    C1, C2, CW = 250, 975, 715          # two example columns
    SUB = (CW - 12) / 2                 # sub-columns Fundort | Standort
    rows = [("GND", GND, 262, 108), ("Wikidata / Wikibase", WD, 382, 184),
            ("OpenStreetMap", OSM, 578, 156), ("Fach-Hubs", AGG, 746, 156)]

    # header
    for cx, title, l2, l3 in [
        (C1, "CIIC 81 · Garranes / Cork", "I-COR-030 · CISP GARES/1 · lod.ogham.link Y50000081",
         "Fundort und Standort getrennt · 20,5 km"),
        (C2, "CIIC 178 · Coumeenoole North", "I-KER-046 · CISP COUME/1 · lod.ogham.link Y50000178",
         "Fundort ist Standort · 1839 wieder aufgerichtet")]:
        p.append(photo(cx, 50, 150, 150, "Foto folgt"))
        p.append(T(cx + 170, 82, title, size=22, weight=500))
        p.append(T(cx + 170, 110, l2, size=13, color=vu.TEXT_MUTED))
        m, _ = vu.svg_chip(cx + 170, 128, l3, GND if False else AGG, size=12.5, h=26)
        p.append(m)
    # sub-column headings
    p.append(T(C1 + 14, 236, "Fundort", size=15, weight=500))
    p.append(T(C1 + SUB + 26, 236, "Standort heute", size=15, weight=500))
    p.append(T(C2 + 14, 236, "Fundort = Standort heute", size=15, weight=500))
    p.append(f'<line x1="{C1}" y1="248" x2="{C1 + CW}" y2="248" stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')
    p.append(f'<line x1="{C2}" y1="248" x2="{C2 + CW}" y2="248" stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')

    data = {
        "GND": [
            ("up", "Ringwall, nicht Fundort", [("GND 1248049489 · Garranes, Ringwallanlage", "gnd"),
                                               ("ohne Koordinate, ohne Link zum Stein", "open")]),
            ("open", "UCC als Körperschaft?", [("GND-Satz UCC · zu prüfen", "open")]),
            ("open", "noch zu prüfen (F1)", [("Dunmore Head · Dún Mór · Coumeenoole · Corkaguiny", "open")]),
        ],
        "Wikidata / Wikibase": [
            ("ok", "Fundort als Item", [("P189: Q69385525 Garranes (Ogham Site)", "ok"),
                                       ("Q104295278 Townland Garranes", "ok"),
                                       ("Baronie Kinalmeaky · QID?", "open"),
                                       ("fuzzy-sl Q74 · Koordinate mit Sicherheit", "ok")]),
            ("ok", "Stein, Sammlung, Raum", [("Q130529871 Stein · P276", "ok"),
                                             ("Q1574185 University College Cork", "ok"),
                                             ("Q121592049 Stone Corridor", "ok"),
                                             ("P625 zwei Werte, gerankt", "ok")]),
            ("ok", "Stein am Ort – Fundort nur implizit", [("Q126503090 Stein · P276: Q26716194", "ok"),
                                                          ("Q85395557 Coumeenoole North / Dunmore Head (Ogham Site)", "ok"),
                                                          ("P189 fehlt · Townland Coumeenoole North · QID?", "open"),
                                                          ("fuzzy-sl Q131 · P625 preferred (OSM) = normal (Macalister)", "ok")]),
        ],
        "OpenStreetMap": [
            ("ok", "Townland als Fläche", [("Relation 6168494 · Townland Garranes", "ok"),
                                           ("Ringfort Lisheenagreine · Objekt?", "open"),
                                           ("Fundort selbst ohne Objekt", "open")]),
            ("ok", "Node im Gebäude", [("Node 11071361392 · indoor=yes", "ok"),
                                       ("moved_from · moved_to:wikidata", "ok"),
                                       ("inscription:pgl-Latn · C[A]SSITT[A/O]", "unc")]),
            ("ok", "Node am Fundort", [("Node 5145413640 · historic=ogham_stone", "ok"),
                                       ("Dún Mór / Dunmore Head · Objekt?", "open"),
                                       ("Townland-Relation Coumeenoole North · ID?", "open")]),
        ],
        "Fach-Hubs": [
            ("ok", "Gazetteer + Denkmalregister", [("Logainm 8299 · An Garrán", "ok"),
                                                   ("SMR CO084-090001- / -002- / -003-", "ok"),
                                                   ("CISP GARES/1 · Macalister 1945, 83", "ok")]),
            ("ok", "Register am Standort", [("SMR CO074-148----", "ok"),
                                            ("UCC Inv.-Nr. 4", "ok"),
                                            ("Sketchfab 3D (b-unicycling)", "ok")]),
            ("ok", "zwei Gazetteer-Anker", [("Logainm 22572 · Com Dhíneol Thuaidh", "ok"),
                                            ("Logainm 1394328 · An Dún Mór", "ok"),
                                            ("SMR KE052-059002- · CISP COUME/1 · TM 172528", "ok")]),
        ],
    }
    for name, col, y, h in rows:
        # row band + label
        p.append(f'<rect x="{LX}" y="{y}" width="{C2 + CW - LX}" height="{h}" rx="12" fill="{col["fill"]}" '
                 f'fill-opacity="0.45"/>')
        p.append(f'<rect x="{LX}" y="{y}" width="8" height="{h}" rx="3" fill="{col["stroke"]}"/>')
        lines = name.split(" / ")
        for i, ln in enumerate(lines):
            p.append(T(LX + 22, y + 30 + i * 20, ln + (" /" if i < len(lines) - 1 else ""),
                       size=16, weight=500, color=col["stroke"]))
        cells = data[name]
        pad = 8
        p.append(cell(C1, y + pad, SUB, h - 2 * pad, col, *cells[0]))
        p.append(cell(C1 + SUB + 12, y + pad, SUB, h - 2 * pad, col, *cells[1]))
        p.append(cell(C2, y + pad, CW, h - 2 * pad, col, *cells[2]))
    p.append(legend_bottom(948, with_bar=False))
    p.append(vu.svg_close())
    return "\n".join(p)


# ------------------------------------------------------------------ GND lane (B and C)
def gnd_slot(cx, y, label, kind, node_top, line_x=None):
    """A GND box above a node, joined to it by a vertical line.
    kind: 'ok' (record exists, solid) · 'pot' (entry conceivable, dashed ochre) · 'check' (probably exists, unverified)."""
    w = max(118, vu.text_width(label, 11.5) + 22)
    x = cx - w / 2
    lx = cx if line_x is None else line_x
    if kind == "ok":
        box = (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="26" rx="13" fill="{GND["fill"]}" '
               f'stroke="{GND["stroke"]}" stroke-width="1.4"/>')
        line = f'<line x1="{lx}" y1="{y + 26}" x2="{lx}" y2="{node_top}" stroke="{GND["stroke"]}" stroke-width="1.6"/>'
        col = vu.TEXT_DARK
    elif kind == "pot":
        box = (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="26" rx="13" fill="#fff" '
               f'stroke="{GND["stroke"]}" stroke-width="1.4" stroke-dasharray="5 3"/>')
        line = (f'<line x1="{lx}" y1="{y + 26}" x2="{lx}" y2="{node_top}" stroke="{GND["stroke"]}" '
                f'stroke-width="1.4" stroke-dasharray="5 4"/>')
        col = GND["stroke"]
    else:
        box = (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="26" rx="13" fill="#fff" '
               f'stroke="#9a9890" stroke-width="1.2" stroke-dasharray="3 3"/>')
        line = (f'<line x1="{lx}" y1="{y + 26}" x2="{lx}" y2="{node_top}" stroke="#9a9890" '
                f'stroke-width="1.2" stroke-dasharray="3 3"/>')
        col = "#8a887f"
    return line + box + T(cx, y + 13.5, label, size=11.5, weight=500, color=col, anchor="middle", baseline="central")


def gnd_lane_label(x, y):
    return (f'<rect x="{x}" y="{y}" width="8" height="26" rx="3" fill="{GND["stroke"]}"/>'
            + T(x + 16, y + 13.5, "GND", size=14, weight=500, color=GND["stroke"], baseline="central"))


def legend_gnd(x, y):
    parts = []
    for kind, label, dx in [("ok", "GND-Satz vorhanden", 0), ("pot", "GND-Eintrag denkbar (GND-Planung)", 190),
                            ("check", "vermutlich vorhanden, zu prüfen", 460)]:
        w = 44
        if kind == "ok":
            parts.append(f'<rect x="{x + dx}" y="{y - 9}" width="{w}" height="18" rx="9" fill="{GND["fill"]}" stroke="{GND["stroke"]}" stroke-width="1.4"/>')
        elif kind == "pot":
            parts.append(f'<rect x="{x + dx}" y="{y - 9}" width="{w}" height="18" rx="9" fill="#fff" stroke="{GND["stroke"]}" stroke-width="1.4" stroke-dasharray="5 3"/>')
        else:
            parts.append(f'<rect x="{x + dx}" y="{y - 9}" width="{w}" height="18" rx="9" fill="#fff" stroke="#9a9890" stroke-width="1.2" stroke-dasharray="3 3"/>')
        parts.append(T(x + dx + w + 8, y + 1, label, size=12.5, baseline="central"))
    return "\n".join(parts)


# ------------------------------------------------------------------ Figure B
def small_map(x, y, w, h, bbox, clip_id):
    lon0, lon1, lat0, lat1 = bbox
    k = math.cos(math.radians((lat0 + lat1) / 2))
    s = min(w / ((lon1 - lon0) * k), h / (lat1 - lat0))
    ox = x + (w - (lon1 - lon0) * k * s) / 2
    oy = y + (h - (lat1 - lat0) * s) / 2

    def pj(lon, lat):
        return ox + (lon - lon0) * k * s, oy + (lat1 - lat) * s
    rings = json.loads((RAW / "naturalearth" / "ireland_outline.json").read_text(encoding="utf-8"))
    p = [f'<defs><clipPath id="{clip_id}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/></clipPath></defs>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{vu.SEA_FILL}"/>',
         f'<g clip-path="url(#{clip_id})">']
    for poly in rings:
        d = "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in (pj(*q) for q in poly["ring"])) + " Z"
        p.append(f'<path d="{d}" fill="{vu.LAND_FILL}" stroke="{vu.LAND_STROKE}" stroke-width="1"/>')
    p.append("</g>")
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="none" stroke="{vu.LINE_NEUTRAL}" stroke-width="1.2"/>')
    return "\n".join(p), pj


def fsl_mark(mx, my, num, certainty):
    """fuzzy-sl coordinate: High = marker only · Low = marker in a dashed red certainty ring."""
    out = []
    if certainty == "low":
        out.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="30" fill="{vu.UNCERTAIN_FILL}" fill-opacity="0.45" '
                   f'stroke="{vu.UNCERTAIN_STROKE}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    out.append(vu.svg_marker(mx, my, num, {"fill": "#fff", "stroke": vu.TEXT_DARK}))
    return "\n".join(out)


def fsl_note(x, y, lines, anchor="start"):
    """Two-line fuzzy-sl statement label next to a map marker."""
    out = [T(x, y, lines[0], size=14, weight=500, anchor=anchor)]
    for i, ln in enumerate(lines[1:]):
        out.append(T(x, y + 18 + i * 16, ln, size=12, color=vu.TEXT_MUTED, anchor=anchor))
    return "\n".join(out)


def fig_b():
    p = [vu.svg_open("Mockup B – Ortskette: Fundort und Standort, mit GND-Andockpunkten und fuzzy-sl-Geometrie")]
    MX, MW = vu.MARGIN_X, 470
    NW, NH = 186, 58
    xs = [575 + i * 226 for i in range(5)]

    # ================= band 1: CIIC 81
    y0 = 40
    p.append(T(MX, y0 + 16, "CIIC 81", size=20, weight=500))
    p.append(T(MX + 90, y0 + 16, "Fundort und Standort getrennt · 20,5 km", size=14, color=vu.TEXT_MUTED))
    m, pj = small_map(MX, y0 + 34, MW, 372, (-9.02, -8.36, 51.74, 51.98), "mapb1")
    p.append(m)
    gx, gy = pj(-8.765479, 51.816848)
    ux, uy = pj(-8.49289, 51.89291)
    p.append(fsl_mark(gx, gy, "1", "low"))
    p.append(fsl_mark(ux, uy, "2", "high"))
    p.append(fsl_note(gx + 38, gy - 4, ["Garranes · Findspot", "fuzzy-sl: Low · aus Text georeferenziert"]))
    p.append(fsl_note(ux - 26, uy - 4, ["UCC Cork · Exhibition Site", "fuzzy-sl: High · Survey vor Ort"], anchor="end"))
    m, _ = vu.svg_chip(MX, y0 + 416, "Geometrie: fuzzy-sl Q74 · Ort-Typ + Sicherheit je Koordinate", WD, size=12)
    p.append(m)

    lane = y0 + 44
    ry1, ry2 = y0 + 140, y0 + 312
    p.append(gnd_lane_label(xs[0] - 4, lane) if False else "")
    # GND lane over the Fundort chain (and the stone)
    sy = (ry1 + ry2) / 2
    p.append(node(xs[0], sy, NW, "Stein CIIC 81", "Q130529871 · Node 11071361392", ["pot", "ok", "ok", "ok"], kind="object"))
    fund = [("Ringfort Lisheenagreine", "SMR CO084-090001-", ["ok", "open", "open", "ok"]),
            ("Townland Garranes", "Q104295278 · rel 6168494 · Logainm 8299", ["pot", "ok", "ok", "ok"]),
            ("Baronie Kinalmeaky", "", ["pot", "open", "open", "open"])]
    stand = [("Stone Corridor", "Q121592049", ["none", "ok", "open", "none"]),
             ("University College Cork", "Q1574185", ["check", "ok", "open", "none"]),
             ("Cork (Stadt)", "", ["check", "ok", "ok", "open"])]
    for i, (tt, ss, hb) in enumerate(fund):
        p.append(node(xs[i + 1], ry1, NW, tt, ss, hb))
    for i, (tt, ss, hb) in enumerate(stand):
        p.append(node(xs[i + 1], ry2, NW, tt, ss, hb))
    p.append(node(xs[4], sy, NW, "County Cork", "", ["check", "ok", "ok", "open"]))
    # GND slots
    p.append(gnd_slot(xs[1] + NW / 2, lane, "GND 1248049489", "ok", ry1, line_x=xs[1] + NW * 0.82))
    p.append(gnd_slot(xs[2] + NW / 2, lane, "GND denkbar", "pot", ry1))
    p.append(gnd_slot(xs[3] + NW / 2, lane, "GND denkbar", "pot", ry1))
    p.append(gnd_slot(xs[4] + NW / 2, lane, "GND prüfen", "check", sy))
    p.append(gnd_slot(xs[0] + NW / 2, lane, "GND denkbar (Objekt)", "pot", sy))
    p.append(T(xs[0] - 12, lane + 13.5, "GND", size=14, weight=500, color=GND["stroke"], anchor="end", baseline="central"))
    # row labels
    for yy, num, lab in [(ry1, "1", "Fundort · P189"), (ry2, "2", "Standort heute · P276")]:
        p.append(vu.svg_marker(xs[1] + 11, yy - 16, num, {"fill": "#fff", "stroke": vu.TEXT_DARK}, r=10))
        p.append(T(xs[1] + 27, yy - 16, lab, size=12.5, weight=500, baseline="central"))
    rail = xs[0] + NW + 20
    p.append(vu.svg_arrow_elbow_v(xs[0] + NW, sy + NH / 2 - 10, xs[1], ry1 + NH / 2, rail))
    p.append(vu.svg_arrow_elbow_v(xs[0] + NW, sy + NH / 2 + 10, xs[1], ry2 + NH / 2, rail))
    for row_y in (ry1, ry2):
        for i in (1, 2):
            p.append(vu.svg_arrow(xs[i] + NW, row_y + NH / 2, xs[i + 1], row_y + NH / 2))
    p.append(vu.svg_arrow_L(xs[3] + NW, ry1 + NH / 2, xs[4] + NW / 2 - 40, sy, bend="h"))
    p.append(vu.svg_arrow_L(xs[3] + NW, ry2 + NH / 2, xs[4] + NW / 2, sy + NH + 30, bend="h"))

    p.append(f'<line x1="{MX}" y1="505" x2="{vu.CANVAS_W - vu.MARGIN_X}" y2="505" stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')

    # ================= band 2: Coumeenoole
    y0 = 520
    p.append(T(MX, y0 + 16, "CIIC 178", size=20, weight=500))
    p.append(T(MX + 100, y0 + 16, "Fundort ist Standort · 1839 wieder aufgerichtet", size=14, color=vu.TEXT_MUTED))
    m, pj = small_map(MX, y0 + 34, MW, 322, (-10.56, -10.30, 52.05, 52.17), "mapb2")
    p.append(m)
    cx_, cy_ = pj(-10.473183, 52.110254)
    sx_, sy_ = pj(-10.458333, 52.111944)
    p.append(fsl_mark(cx_, cy_, "1", "low"))
    p.append(fsl_note(cx_ - 20, cy_ + 58, ["Dunmore Head · zwei Koordinaten, ein Punkt",
                                            "Findspot: Low · Macalister 1945, 170",
                                            "Exhibition Site: High · Survey vor Ort"]))
    p.append(vu.svg_marker(sx_, sy_, "S", {"fill": "#fff", "stroke": vu.UNCERTAIN_STROKE}, r=10, dashed=True))
    p.append(T(sx_ + 16, sy_ - 14, "Site-Punkt WD · 1,03 km", size=12, color=vu.UNCERTAIN_STROKE, baseline="central"))
    m, _ = vu.svg_chip(MX, y0 + 364, "Geometrie: fuzzy-sl Q131 · beide Aussagen mit Quelle", WD, size=12)
    p.append(m)

    lane = y0 + 44
    ry = y0 + 150
    chain = [("Stein CIIC 178", "Q126503090 · Node 5145413640", ["pot", "ok", "ok", "ok"], "object"),
             ("Promontory Fort An Dún Mór", "Q26716194? · Logainm 1394328", ["pot", "open", "open", "ok"], "place"),
             ("Townland Coumeenoole North", "Logainm 22572", ["pot", "open", "open", "ok"], "place"),
             ("Baronie Corkaguiny", "", ["pot", "open", "open", "open"], "place"),
             ("County Kerry", "Q184469", ["check", "ok", "ok", "open"], "place")]
    for i, (tt, ss, hb, kd) in enumerate(chain):
        p.append(node(xs[i], ry, NW, tt, ss, hb, kind=kd))
    for i, (lab, kd) in enumerate([("GND denkbar (Objekt)", "pot"), ("GND denkbar", "pot"), ("GND denkbar", "pot"),
                                   ("GND denkbar", "pot"), ("GND prüfen", "check")]):
        p.append(gnd_slot(xs[i] + NW / 2, lane, lab, kd, ry, line_x=(xs[i] + NW * 0.82) if i == 1 else None))
    p.append(T(xs[0] - 12, lane + 13.5, "GND", size=14, weight=500, color=GND["stroke"], anchor="end", baseline="central"))
    p.append(vu.svg_marker(xs[1] + 11, ry - 16, "1", {"fill": "#fff", "stroke": vu.TEXT_DARK}, r=10))
    p.append(T(xs[1] + 27, ry - 16, "P189 = P276", size=12.5, weight=500, baseline="central"))
    p.append(vu.svg_arrow(xs[0] + NW, ry + NH / 2, xs[1], ry + NH / 2))
    for i in (1, 2, 3):
        p.append(vu.svg_arrow(xs[i] + NW, ry + NH / 2, xs[i + 1], ry + NH / 2))
    p.append(node(xs[1], ry + 150, NW, "Ogham Site", "Q85395557 · ogham-lod OS40000083",
                  ["none", "ok", "none", "ok"], kind="concept"))
    p.append(vu.svg_arrow_L(xs[0] + NW / 2, ry + NH + 32, xs[1], ry + 150 + NH / 2, bend="v", dashed=True,
                            label="Site-Konzept"))
    p.append(legend_bottom(940, with_status=False, with_kinds=True))
    p.append(legend_gnd(MX, 972))
    p.append(vu.svg_close())
    return "\n".join(p)


# ------------------------------------------------------------------ Figure C
def inscription(x, y, text, uncertain_idx, size=26):
    spans = []
    for i, ch in enumerate(text):
        col = vu.UNCERTAIN_STROKE if i in uncertain_idx else vu.TEXT_DARK
        spans.append(f'<tspan fill="{col}">{vu.xml_escape(ch)}</tspan>')
    return (f'<text x="{x}" y="{y}" font-family="Fira Sans" font-size="{size}" font-weight="500" '
            f'letter-spacing="1.5">{"".join(spans)}</text>')


def scholar_row(x, y, items):
    """Who read / commented the inscription -- persons, where the GND is dense."""
    out = [T(x, y + 11, "gelesen von", size=12.5, color=vu.TEXT_MUTED, baseline="central")]
    cx = x + 84
    for name, gstate in items:
        m, w = vu.svg_chip(cx, y, name, AGG, size=11.5)
        out.append(m)
        cx += w + 4
        kind = {"ok": "ok", "check": "check"}[gstate]
        if kind == "ok":
            out.append(f'<rect x="{cx}" y="{y + 1}" width="22" height="20" rx="4" fill="{GND["fill"]}" stroke="{GND["stroke"]}" stroke-width="1.4"/>')
            out.append(T(cx + 11, y + 12, "G", size=11, weight=500, color=GND["stroke"], anchor="middle", baseline="central"))
        else:
            out.append(f'<rect x="{cx}" y="{y + 1}" width="22" height="20" rx="4" fill="#fff" stroke="#9a9890" stroke-width="1.2" stroke-dasharray="3 2"/>')
            out.append(T(cx + 11, y + 12, "G?", size=10, weight=500, color="#8a887f", anchor="middle", baseline="central"))
        cx += 36
    return "\n".join(out)


def fig_c():
    p = [vu.svg_open("Mockup C – Der Graph hinter der Inschrift führt zurück zum Ort")]
    X = vu.MARGIN_X
    NW, NH = 172, 58
    xs = [X + i * 280 for i in range(6)]

    # ================= Coumeenoole: the loop closes
    p.append(T(X, 60, "CIIC 178", size=20, weight=500))
    txt = "ERC MAQI MAQI-ERCIAS MU DOVINIA"
    d = txt.index("DOVINIA")
    unc = {txt.index("S MU"), txt.index("MU D"), txt.index("MU D") + 1, d + 4, d + 6}
    p.append(inscription(X + 110, 62, txt, unc))
    lx = X + 110 + len(txt) * 26 * 0.62 + 30
    for lab, col in [("EpiDoc pgl", AGG), ("OSM pgl-Latn · ?", OPEN), ("Wikidata la", UNC)]:
        m, w = vu.svg_chip(lx, 45, lab, col, size=12, dashed=(col is OPEN))
        p.append(m)
        lx += w + 10
    p.append(T(X + 110, 90, "„of Erc son of Mac-Erce descendant? of Duibne“ · rot: in der Edition unsicher gelesen",
               size=13, color=vu.TEXT_MUTED, italic=True))
    p.append(scholar_row(X + 110, 104, [("Macalister 1945", "check"), ("Cuppage 1986", "check"),
                                        ("McManus 1991", "check"), ("White (OG(H)AM) · ORCID", "check")]))

    lane, top, bot = 150, 210, 400
    p.append(node(xs[0], top, NW, "Stein CIIC 178", "Q126503090", ["pot", "ok", "ok", "ok"], kind="object"))
    p.append(node(xs[1], top, NW, "ERC", "OP400203 · Wort ERC Q67382360", ["none", "open", "none", "ok"], kind="concept"))
    p.append(node(xs[2], top, NW, "MAQI-ERCIAS", "OP400321", ["none", "open", "none", "ok"], kind="concept"))
    p.append(node(xs[3], top, NW, "DOVINIA", "OP400175", ["none", "open", "none", "ok"], kind="concept"))
    p.append(node(xs[4], top, NW, "Corcu Duibne", "Sippe / Tribus", ["pot", "open", "none", "open"], kind="concept"))
    p.append(node(xs[5] - 30, top, 260, "Baronie Corkaguiny", "Corca Dhuibhne", ["pot", "open", "open", "open"]))
    p.append(gnd_slot(xs[4] + NW / 2, lane, "GND denkbar", "pot", top))
    p.append(gnd_slot(xs[5] - 30 + 130, lane, "GND denkbar", "pot", top))
    p.append(gnd_slot(xs[0] + NW / 2, lane, "GND denkbar (Objekt)", "pot", top))
    p.append(T(xs[0] + NW / 2 + 90, lane + 13.5, "GND", size=14, weight=500, color=GND["stroke"], baseline="central"))
    labels = ["Inschrift nennt", "MAQI · Q67381254", "MU(COI) · Q67999759", "Sippe", "Name"]
    for i in range(5):
        x2 = xs[i + 1] - (30 if i == 4 else 0)
        p.append(vu.svg_arrow_labeled(xs[i] + NW, top + NH / 2, x2, top + NH / 2, labels[i], font_size=11))
    p.append(node(xs[3], bot, NW, "Townland", "Coumeenoole North · Logainm 22572", ["pot", "open", "open", "ok"]))
    p.append(node(xs[1], bot, NW, "An Dún Mór", "Promontory Fort · Logainm 1394328", ["pot", "open", "open", "ok"]))
    bx = xs[5] - 30 + 130
    p.append(vu.svg_arrow_L(bx, top + NH + 32, xs[3] + NW, bot + NH / 2, bend="v", label="enthält"))
    p.append(vu.svg_arrow_labeled(xs[3], bot + NH / 2, xs[1] + NW, bot + NH / 2, "enthält", font_size=11))
    p.append(vu.svg_arrow_L(xs[1], bot + NH / 2, xs[0] + NW / 2, top + NH + 32, bend="h", label="Fundort"))
    m, _ = vu.svg_chip(X, bot + 92, "DOVINIA führt über die Sippe zur Baronie – und die enthält den Fundort (McManus 1991, 111).",
                       WD, size=13, h=28)
    p.append(m)

    p.append(f'<line x1="{X}" y1="548" x2="{vu.CANVAS_W - vu.MARGIN_X}" y2="548" stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')

    # ================= CIIC 81: the chain stays open
    y1 = 570
    p.append(T(X, y1 + 24, "CIIC 81", size=20, weight=500))
    txt2 = "CASSITTAS MAQI MUCOI CALLITI"
    p.append(inscription(X + 110, y1 + 26, txt2, {1, 8, 17, 18}))
    lx = X + 110 + len(txt2) * 26 * 0.62 + 30
    for lab, col in [("EpiDoc pgl", AGG), ("OSM pgl-Latn · C[A]SSITT[A/O]", UNC), ("Wikidata ga", UNC)]:
        m, w = vu.svg_chip(lx, y1 + 9, lab, col, size=12)
        p.append(m)
        lx += w + 10
    p.append(T(X + 110, y1 + 54, "Macalister 1945: -AS · Gippert 1987: -OS · OSM hält den Streit im Tag fest",
               size=13, color=vu.TEXT_MUTED, italic=True))
    p.append(scholar_row(X + 110, y1 + 68, [("Macalister 1945", "check"), ("Gippert 1987", "check"),
                                            ("McManus 2004", "check"), ("O’Brien 2021", "check")]))
    lane2, ry = y1 + 112, y1 + 170
    p.append(node(xs[0], ry, NW, "Stein CIIC 81", "Q130529871", ["pot", "ok", "ok", "ok"], kind="object"))
    p.append(node(xs[1], ry, NW, "CASSITTAS", "OP400067", ["none", "open", "none", "ok"], kind="concept"))
    p.append(node(xs[2], ry, NW, "CALLITI", "OP400061", ["none", "open", "none", "ok"], kind="concept"))
    p.append(node(xs[3], ry, NW, "Cailtrige", "Ceinéal Caollaidhe · Sippe", ["pot", "open", "none", "open"], kind="concept"))
    p.append(node(xs[4], ry, NW, "Eoghanachta", "Dynastie", ["check", "open", "none", "open"], kind="concept"))
    p.append(gnd_slot(xs[3] + NW / 2, lane2, "GND denkbar", "pot", ry))
    p.append(gnd_slot(xs[4] + NW / 2, lane2, "GND prüfen", "check", ry))
    labels2 = ["Inschrift nennt", "MAQI MUCOI", "O’Brien 2021", "Teil von"]
    for i in range(4):
        p.append(vu.svg_arrow_labeled(xs[i] + NW, ry + NH / 2, xs[i + 1], ry + NH / 2, labels2[i], font_size=11))
    ex = xs[5] - 30
    p.append(f'<rect x="{ex}" y="{ry}" width="260" height="{NH}" rx="10" fill="#fff" stroke="#9a9890" '
             f'stroke-width="1.4" stroke-dasharray="6 4"/>')
    p.append(T(ex + 130, ry + NH / 2, "Ort? · kein Gebiet benannt", size=14, weight=500,
               color="#9a9890", anchor="middle", baseline="central"))
    p.append(vu.svg_arrow(xs[4] + NW, ry + NH / 2, ex, ry + NH / 2, dashed=True))
    m, _ = vu.svg_chip(X, ry + 96, "Hier bleibt die Kette offen: Die Sippe ist belegt, ein Gebiet mit Geometrie nicht.",
                       OPEN, size=13, h=28, dashed=True)
    p.append(m)
    p.append(legend_bottom(930, with_status=False, with_kinds=True))
    p.append(legend_gnd(X, 962))
    p.append(vu.svg_close())
    return "\n".join(p)



if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [("mock-a-rollen", fig_a), ("mock-b-ortskette", fig_b), ("mock-c-graph-dahinter", fig_c)]:
        vu.write_figure(OUT, name + ".de", fn(), zoom=1.0)
        print(name)
