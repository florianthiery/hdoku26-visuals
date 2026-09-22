#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hdoku26_visuals_utils.py -- shared constants, palette, paths and writers
=========================================================================

Every step module imports from here rather than repeating a hex code, a
path computation or a box/arrow primitive. Forked from the sibling repo
``bb-5kbc-visuals`` (same author, same house pattern: pure Python SVG
authoring + resvg-py rasterisation, fixed 7:4 canvas, no title header or
citation footer baked in, bilingual DE/EN output, no diagonal lines).
The drawing helpers below the palette are carried over unchanged; only the
paths, the output directories and the palette are specific to this repo.

Authors: Florian Thiery (LEIZA / Research Squirrel Engineers Network)
Licence: MIT (this script) / CC BY 4.0 (the figures it produces)
"""

from __future__ import annotations

import hashlib
import math
from pathlib import Path

# --------------------------------------------------------------------------- #
# Release marker -- NOT datetime.now(). Bump by hand when the content set
# changes.
# --------------------------------------------------------------------------- #
RELEASE = "2026-09-22"

# --------------------------------------------------------------------------- #
# Paths, resolved relative to the repository root
# --------------------------------------------------------------------------- #
ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "img"
DATA_RAW = ROOT / "data" / "raw"
FONTS = ROOT / "fonts"

FONT_REGULAR = FONTS / "FiraSans-Regular.ttf"
FONT_MEDIUM = FONTS / "FiraSans-Medium.ttf"
FONT_SANS = "Fira Sans"

# --------------------------------------------------------------------------- #
# Canvas -- same fixed 7:4 slide format as bb-5kbc-visuals.
# --------------------------------------------------------------------------- #
CANVAS_W = 1750
CANVAS_H = 1000

OUT_DIRS = {
    "01-ein-name-viele-orte": IMG / "01-ein-name-viele-orte",
    "02-wikibase-konvergenz": IMG / "02-wikibase-konvergenz",
    "03-nische-hub": IMG / "03-nische-hub",
}

MARGIN_X = 60
MARGIN_TOP = 50
MARGIN_BOTTOM = 50
CONTENT_X0 = MARGIN_X
CONTENT_X1 = CANVAS_W - MARGIN_X
CONTENT_Y0 = MARGIN_TOP
CONTENT_Y1 = CANVAS_H - MARGIN_BOTTOM


def ensure_dirs() -> None:
    """Create every output directory this repo writes into. Idempotent."""
    for path in OUT_DIRS.values():
        path.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------------- #
# Palette -- one pair per "world" a mark can belong to. The story of the
# talk has three poles, and every figure colours by them consistently:
#
#   GND        -- the authority file (ochre: the bb5kbc "reference" earth tone)
#   COMMUNITY  -- community hubs: Wikidata, OpenStreetMap, and the national
#                 gazetteers reached through them (Logainm) (petrol, the
#                 bb5kbc GEO family)
#   AGGREGATOR -- GeoNames and other aggregated gazetteers (neutral grey,
#                 the bb5kbc "authority" pair)
#
# plus the bb5kbc uncertainty accent (dashed terracotta) for "no coordinate /
# location only presumed", and the pipeline "validate" pair for the c't
# quotation boxes.
# --------------------------------------------------------------------------- #
GND = {"fill": "#f3e6d6", "stroke": "#8a5a2a"}
COMMUNITY = {"fill": "#dce8ea", "stroke": "#386870"}
AGGREGATOR = {"fill": "#e8e8e8", "stroke": "#666666"}
QUOTE = {"fill": "#fff7dc", "stroke": "#7f6000"}

UNCERTAIN_STROKE = "#a03030"
UNCERTAIN_FILL = "#f5dede"

TEXT_DARK = "#2c2c2a"
TEXT_MUTED = "#5f5e5a"
LINE_NEUTRAL = "#888780"

# Basemap tones (land / sea / coastline) -- deliberately pale so the data
# marks carry the figure.
LAND_FILL = "#f4f2ec"
LAND_STROKE = "#b9b4a8"
SEA_FILL = "#f3f7f8"


def t(lang: str, de: str, en: str) -> str:
    """Pick the German or English string."""
    return de if lang == "de" else en


def fmt_num(value: float, lang: str, digits: int = 1) -> str:
    """Decimal number with the language's decimal separator (36,6 / 36.6)."""
    s = f"{value:.{digits}f}"
    return s.replace(".", ",") if lang == "de" else s


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in km (mean Earth radius 6371 km)."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


# --------------------------------------------------------------------------- #
# Deterministic writers
# --------------------------------------------------------------------------- #
def content_fingerprint(data: bytes) -> str:
    """Short, stable fingerprint for logging / --strict checks."""
    return hashlib.sha256(data).hexdigest()[:12]


def write_svg(path: Path, svg_markup: str) -> str:
    """Write SVG source deterministically: UTF-8, exactly one trailing
    newline, no injected timestamps or random ids."""
    text = svg_markup.strip("\n") + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return content_fingerprint(text.encode("utf-8"))


def write_png_from_svg(svg_path: Path, png_path: Path, *, zoom: float = 2.0) -> str:
    """Rasterise an already-written SVG file to PNG via resvg-py, in-process,
    using the vendored Fira Sans weights. White background (talk decks are
    usually put on a light slide master; transparent is available by passing
    background=None at the call site if ever needed)."""
    import resvg_py  # imported lazily so --list/--dry-run stay cheap

    png_bytes = resvg_py.svg_to_bytes(
        svg_path=str(svg_path),
        background="#ffffff",
        skip_system_fonts=True,
        font_files=[str(FONT_REGULAR), str(FONT_MEDIUM)],
        zoom=zoom,
    )
    png_path.parent.mkdir(parents=True, exist_ok=True)
    png_path.write_bytes(png_bytes)
    return content_fingerprint(png_bytes)


def write_figure(out_dir: Path, name: str, svg_markup: str, *, zoom: float = 2.0) -> list[str]:
    """Write both the .svg and the .png for one figure and return the two
    paths written, in the shape main.py expects from a step's return value."""
    svg_path = out_dir / f"{name}.svg"
    png_path = out_dir / f"{name}.png"
    write_svg(svg_path, svg_markup)
    write_png_from_svg(svg_path, png_path, zoom=zoom)
    return [str(svg_path), str(png_path)]


# --------------------------------------------------------------------------- #
# Small SVG-building helpers shared by every step_*.py. Deliberately minimal
# -- not a general diagram library, just enough that no step repeats the same
# box/arrow math or forgets to XML-escape a label.
# --------------------------------------------------------------------------- #
ARROW_STROKE = "#73726c"

# NOTE (carried over from crossy-visuals, still true here): the CSS
# `context-stroke` keyword is NOT supported by resvg -- arrowheads render
# invisible until pinned to a fixed colour.
ARROW_DEFS = (
    '<defs>'
    '<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" '
    'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
    f'<path d="M2 1L8 5L2 9" fill="none" stroke="{ARROW_STROKE}" stroke-width="1.5" '
    'stroke-linecap="round" stroke-linejoin="round"/></marker>'
    '<marker id="arrow-uncertain" viewBox="0 0 10 10" refX="8" refY="5" '
    'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
    f'<path d="M2 1L8 5L2 9" fill="none" stroke="{UNCERTAIN_STROKE}" stroke-width="1.5" '
    'stroke-linecap="round" stroke-linejoin="round"/></marker>'
    '</defs>'
)


def xml_escape(s: str) -> str:
    """Escape the five XML predefined entities. Every helper that places
    caller-supplied text into an SVG text node must run it through this."""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def text_width(s: str, size: int = 14) -> float:
    """Rough width estimate (Fira Sans is close to 0.56*size per character)."""
    return len(s) * size * 0.56


def box_width(title: str, subtitle: str = "", *, min_width: float = 150, pad: float = 32) -> float:
    t = text_width(title, 14)
    s = text_width(subtitle, 12) if subtitle else 0
    return max(min_width, t + pad, s + pad)


def svg_box(x: float, y: float, w: float, h: float, title: str, subtitle: str = "",
            *, fill: str = "#f1efe8", stroke: str = "#5f5e5a", text_color: str = TEXT_DARK,
            rx: float = 10, stroke_width: float = 1.4, dashed: bool = False,
            stereotype: str = "") -> str:
    """A class/entity box. Optional ``stereotype`` renders a small
    <<crm:E27_Site>>-style line above the title, mirroring the UML
    convention already used in Abb. 3 of the working paper.

    Title and subtitle font sizes auto-shrink (down to a floor) if the
    text would otherwise overflow the box width -- layouts are tuned by
    hand for one language's word lengths, and this keeps a translated
    label (English vs. German box widths differ) from overflowing the
    box outline instead of silently looking wrong.
    """
    raw_title, raw_subtitle = title, subtitle
    title, subtitle = xml_escape(title), xml_escape(subtitle)
    dash = ' stroke-dasharray="7 5"' if dashed else ""
    parts = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
             f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"{dash}/>']
    cx = x + w / 2
    avail = w - 24

    def fit_size(text: str, base: float, floor: float) -> float:
        size = base
        while size > floor and text_width(text, size) > avail:
            size -= 0.5
        return size

    n_lines = 1 + bool(subtitle) + bool(stereotype)
    if stereotype:
        st = xml_escape(stereotype)
        st_size = fit_size(stereotype, 10.5, 8.5)
        parts.append(f'<text x="{cx:.1f}" y="{y + h/2 - 18:.1f}" text-anchor="middle" '
                      f'font-family="Fira Sans" font-size="{st_size:.1f}" font-style="italic" '
                      f'fill="{text_color}" opacity="0.72">\u00ab{st}\u00bb</text>')
    if subtitle:
        ty = y + h / 2 - 3 if stereotype else y + h / 2 - 8
        title_size = fit_size(raw_title, 14, 11)
        parts.append(f'<text x="{cx:.1f}" y="{ty:.1f}" text-anchor="middle" '
                      f'font-family="Fira Sans" font-weight="500" font-size="{title_size:.1f}" '
                      f'fill="{text_color}">{title}</text>')
        sub_size = fit_size(raw_subtitle, 11.5, 9)
        parts.append(f'<text x="{cx:.1f}" y="{ty + 20:.1f}" text-anchor="middle" '
                      f'font-family="Fira Sans" font-size="{sub_size:.1f}" fill="{text_color}" '
                      f'opacity="0.75">{subtitle}</text>')
    else:
        ty = y + h/2 + 10 if stereotype else y + h / 2
        base = "central" if not stereotype else "auto"
        title_size = fit_size(raw_title, 14, 10.5)
        parts.append(f'<text x="{cx:.1f}" y="{ty:.1f}" text-anchor="middle" '
                      f'dominant-baseline="{base}" font-family="Fira Sans" '
                      f'font-weight="500" font-size="{title_size:.1f}" fill="{text_color}">{title}</text>')
    return "\n".join(parts)


def svg_hash_node(cx: float, cy: float, r: float, title: str, subtitle: str = "",
                   *, fill: str = "#dce8ea", stroke: str = "#386870",
                   text_color: str = TEXT_DARK) -> str:
    """A shared/deduplicated concept node (Regel 2/3: one node per distinct
    value, e.g. a Gemeinde or a Kulturgruppe). Drawn as a double-ring circle
    -- deliberately distinct from a plain entity box, to make "this node is
    shared across many Fundstelle rows" visible at a glance.

    Title and subtitle are auto-fit to the circle's usable chord width:
    font size shrinks first (down to a floor), and the subtitle wraps to a
    second line if it still doesn't fit even at the floor size -- fixes the
    text overflowing the stroke on longer labels (e.g. "shared ·
    bundesland_{hash}"), which a fixed font size cannot cover for every
    language/label-length combination.
    """
    raw_title, raw_subtitle = title, subtitle
    title, subtitle = xml_escape(title), xml_escape(subtitle)
    avail = 2 * (r - 14)
    parts = [
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="2"/>',
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r - 6:.1f}" fill="none" '
        f'stroke="{stroke}" stroke-width="1" opacity="0.55"/>',
    ]

    def fit_size(text: str, base: float, floor: float) -> float:
        size = base
        while size > floor and text_width(text, size) > avail:
            size -= 0.5
        return size

    if subtitle:
        title_size = fit_size(raw_title, 13, 11)
        parts.append(f'<text x="{cx:.1f}" y="{cy - 4:.1f}" text-anchor="middle" '
                      f'font-family="Fira Sans" font-weight="500" font-size="{title_size:.1f}" '
                      f'fill="{text_color}">{title}</text>')
        sub_size = fit_size(raw_subtitle, 10.5, 8)
        if text_width(raw_subtitle, sub_size) <= avail or " " not in raw_subtitle:
            parts.append(f'<text x="{cx:.1f}" y="{cy + 14:.1f}" text-anchor="middle" '
                          f'font-family="Fira Sans" font-size="{sub_size:.1f}" fill="{text_color}" '
                          f'opacity="0.75">{subtitle}</text>')
        else:
            # still too wide even at the floor size -- wrap at the space
            # closest to the middle of the string so both halves balance
            words = raw_subtitle.split(" ")
            best_i, best_diff = 1, float("inf")
            for i in range(1, len(words)):
                left, right = " ".join(words[:i]), " ".join(words[i:])
                diff = abs(text_width(left, sub_size) - text_width(right, sub_size))
                if diff < best_diff:
                    best_i, best_diff = i, diff
            line1, line2 = " ".join(words[:best_i]), " ".join(words[best_i:])
            line1_size = fit_size(line1, sub_size, 7.5)
            line2_size = fit_size(line2, sub_size, 7.5)
            parts.append(f'<text x="{cx:.1f}" y="{cy + 11:.1f}" text-anchor="middle" '
                          f'font-family="Fira Sans" font-size="{line1_size:.1f}" fill="{text_color}" '
                          f'opacity="0.75">{xml_escape(line1)}</text>')
            parts.append(f'<text x="{cx:.1f}" y="{cy + 25:.1f}" text-anchor="middle" '
                          f'font-family="Fira Sans" font-size="{line2_size:.1f}" fill="{text_color}" '
                          f'opacity="0.75">{xml_escape(line2)}</text>')
    else:
        title_size = fit_size(raw_title, 13, 10)
        parts.append(f'<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" '
                      f'dominant-baseline="central" font-family="Fira Sans" '
                      f'font-weight="500" font-size="{title_size:.1f}" fill="{text_color}">{title}</text>')
    return "\n".join(parts)


def svg_authority_badge(cx: float, cy: float, label: str, *, r: float = 15,
                         fill: str = "#e8e8e8", stroke: str = "#666666") -> str:
    """Small hexagonal badge for an external authority (Wikidata QID,
    GeoNames, TGN, iDAI.gazetteer, OSM relation, Perio.do)."""
    import math
    pts = []
    for i in range(6):
        ang = math.pi / 6 + i * math.pi / 3
        pts.append(f"{cx + r * math.cos(ang):.1f},{cy + r * math.sin(ang):.1f}")
    label = xml_escape(label)
    return (
        f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>\n'
        f'<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" dominant-baseline="central" '
        f'font-family="Fira Sans" font-weight="500" font-size="9.5" fill="{TEXT_DARK}">{label}</text>'
    )


def svg_arrow(x1: float, y1: float, x2: float, y2: float, *, stroke: str = ARROW_STROKE,
              dashed: bool = False, marker: str = "arrow") -> str:
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="1.6"{dash} marker-end="url(#{marker})"/>')


def svg_arrow_elbow(x1: float, y1: float, x2: float, y2: float, rail_y: float,
                     *, stroke: str = ARROW_STROKE, dashed: bool = False,
                     marker: str = "arrow", label: str = "", label_color: str = TEXT_DARK,
                     font_size: int = 11) -> str:
    """Right-angle routed connector: down/up from the source to a shared
    horizontal ``rail_y``, across, then down/up into the target. For
    long-distance connections that would otherwise cut diagonally through
    unrelated boxes -- give each such connection its own ``rail_y`` so
    parallel long-haul lines stack as distinct horizontal tracks instead
    of crossing. An optional ``label`` sits centred on the horizontal
    (rail) segment, the part of the path with the most free space."""
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    path = (f'M {x1:.1f} {y1:.1f} L {x1:.1f} {rail_y:.1f} '
            f'L {x2:.1f} {rail_y:.1f} L {x2:.1f} {y2:.1f}')
    parts = [f'<path d="{path}" fill="none" stroke="{stroke}" stroke-width="1.6"{dash} '
             f'marker-end="url(#{marker})"/>']
    if label:
        lx = (x1 + x2) / 2
        parts.append(f'<text x="{lx:.1f}" y="{rail_y - 8:.1f}" text-anchor="middle" '
                     f'font-family="Fira Sans" font-weight="500" font-size="{font_size}" '
                     f'fill="{label_color}">{xml_escape(label)}</text>')
    return "\n".join(parts)


def svg_arrow_elbow_v(x1: float, y1: float, x2: float, y2: float, rail_x: float,
                       *, stroke: str = ARROW_STROKE, dashed: bool = False,
                       marker: str = "arrow", label: str = "", label_color: str = TEXT_DARK,
                       font_size: int = 11) -> str:
    """Like :func:`svg_arrow_elbow` but routed via a shared *vertical*
    rail (horizontal, then vertical, then horizontal) -- for skirting
    around the side of a container instead of under a whole diagram, or
    for a multi-target fan-out where the targets share an x that's too
    crowded (with other boxes) to land a vertical segment on directly --
    route the vertical run through a clear rail_x in the gap before that
    column instead, then one short final hop into the actual edge. An
    optional ``label`` sits on the vertical (rail) segment, which is
    usually the one part of the path unique to this connection."""
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    path = (f'M {x1:.1f} {y1:.1f} L {rail_x:.1f} {y1:.1f} '
            f'L {rail_x:.1f} {y2:.1f} L {x2:.1f} {y2:.1f}')
    parts = [f'<path d="{path}" fill="none" stroke="{stroke}" stroke-width="1.6"{dash} '
             f'marker-end="url(#{marker})"/>']
    if label:
        ly = (y1 + y2) / 2
        parts.append(f'<text x="{rail_x + text_width(label, font_size) / 2 + 8:.1f}" y="{ly:.1f}" '
                     f'text-anchor="middle" dominant-baseline="central" font-family="Fira Sans" '
                     f'font-weight="500" font-size="{font_size}" fill="{label_color}">{xml_escape(label)}</text>')
    return "\n".join(parts)


def svg_arrow_L(x1: float, y1: float, x2: float, y2: float, *, bend: str = "h",
                 stroke: str = ARROW_STROKE, dashed: bool = False,
                 marker: str | None = "arrow", label: str = "", label_color: str = TEXT_DARK,
                 font_size: int = 11) -> str:
    """Single-corner orthogonal connector -- the house default for any
    connection whose source and target aren't already aligned on one
    axis (house rule from 2026-09-15: no diagonal lines anywhere).
    ``bend="h"`` leaves the source horizontally first (at y1) then turns
    to y2; ``bend="v"`` leaves vertically first (at x1) then turns to
    x2. Pick whichever keeps the corner out of any box that isn't the
    source or target -- for a fan-out from one box's side, that is
    usually the bend that matches the side the arrow exits from (bottom
    edge -> "v", right edge -> "h"). An optional ``label`` sits on the
    longer of the two segments, offset perpendicular to it so the line
    still reads through cleanly. If ``x1==x2`` or ``y1==y2`` already,
    this degrades to a single straight segment (no dead corner).
    ``marker=None`` omits the arrowhead entirely -- for legs that
    converge with another connector on the same point, where two
    arrowheads would collide into an "X"; give the *last* short hop
    into the actual target its own arrowhead instead (see
    step_05_uncertainty_markers.py for the pattern)."""
    if x1 == x2 or y1 == y2:
        path = f'M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}'
        seg_mid = ((x1 + x2) / 2, (y1 + y2) / 2)
        vertical = x1 == x2
    elif bend == "h":
        path = f'M {x1:.1f} {y1:.1f} L {x2:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}'
        long_horizontal = abs(x2 - x1) >= abs(y2 - y1)
        seg_mid = ((x1 + x2) / 2, y1) if long_horizontal else (x2, (y1 + y2) / 2)
        vertical = not long_horizontal
    else:
        path = f'M {x1:.1f} {y1:.1f} L {x1:.1f} {y2:.1f} L {x2:.1f} {y2:.1f}'
        long_vertical = abs(y2 - y1) >= abs(x2 - x1)
        seg_mid = (x1, (y1 + y2) / 2) if long_vertical else ((x1 + x2) / 2, y2)
        vertical = long_vertical
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    marker_attr = f' marker-end="url(#{marker})"' if marker else ""
    parts = [f'<path d="{path}" fill="none" stroke="{stroke}" stroke-width="1.6"{dash}{marker_attr}/>']
    if label:
        lx, ly = seg_mid
        if vertical:
            lx += text_width(label, font_size) / 2 + 10
        else:
            ly -= 10
        parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" dominant-baseline="central" '
                     f'font-family="Fira Sans" font-weight="500" font-size="{font_size}" '
                     f'fill="{label_color}">{xml_escape(label)}</text>')
    return "\n".join(parts)


def svg_arrow_labeled(x1: float, y1: float, x2: float, y2: float, label: str,
                       *, stroke: str = ARROW_STROKE, label_color: str = TEXT_DARK,
                       above: bool = True, offset: float | None = None,
                       dashed: bool = False, marker: str = "arrow",
                       font_size: int = 12) -> str:
    """Straight arrow with a label offset perpendicular to its actual
    direction (works for steep/vertical arrows too, not just horizontal
    ones), growing with label width for steep arrows so the line never
    cuts through the text. Ported from crossy-visuals after two rounds of
    fixes there -- see that repo's PRIMER.md S4/S6 if the reasoning is
    ever needed again."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy_dir = x2 - x1, y2 - y1
    length = (dx ** 2 + dy_dir ** 2) ** 0.5 or 1.0
    steep = abs(dy_dir) > abs(dx)
    if offset is None:
        offset = text_width(label, font_size) / 2 + 10 if steep else 14
    perp_x, perp_y = dy_dir / length, -dx / length
    if not above:
        perp_x, perp_y = -perp_x, -perp_y
    tx, ty = mx + perp_x * offset, my + perp_y * offset
    return (
        svg_arrow(x1, y1, x2, y2, stroke=stroke, dashed=dashed, marker=marker)
        + f'\n<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="middle" '
        f'dominant-baseline="central" font-family="Fira Sans" font-weight="500" '
        f'font-size="{font_size}" fill="{label_color}">{xml_escape(label)}</text>'
    )


def svg_dashed_container(x: float, y: float, w: float, h: float, label: str,
                          *, stroke: str = LINE_NEUTRAL) -> str:
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="16" '
            f'fill="none" stroke="{stroke}" stroke-width="1.5" stroke-dasharray="6 5"/>\n'
            f'<text x="{x + 16:.1f}" y="{y + 26:.1f}" font-family="Fira Sans" '
            f'font-weight="500" font-size="13" fill="{stroke}">{xml_escape(label)}</text>')


def svg_legend(x: float, y: float, entries: list[tuple[str, dict]], *, box: float = 16,
               gap: float = 8, row_h: float = 24, columns: int = 1,
               col_w: float = 220) -> str:
    """A small colour-key legend: one swatch + label per entry, grouped into
    ``columns`` columns of ``col_w`` px each."""
    parts = []
    for i, (label, colors) in enumerate(entries):
        col, row = i // ((len(entries) + columns - 1) // columns or 1), i % ((len(entries) + columns - 1) // columns or 1)
        ex = x + col * col_w
        ey = y + row * row_h
        parts.append(f'<rect x="{ex:.1f}" y="{ey:.1f}" width="{box}" height="{box}" rx="3" '
                      f'fill="{colors["fill"]}" stroke="{colors["stroke"]}" stroke-width="1.4"/>')
        parts.append(f'<text x="{ex + box + gap:.1f}" y="{ey + box/2:.1f}" '
                      f'dominant-baseline="central" font-family="Fira Sans" font-size="12" '
                      f'fill="{TEXT_DARK}">{xml_escape(label)}</text>')
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# Canvas open/close. No title header, no source-citation footer (revision
# 2026-09-10b): these are general-purpose diagram assets, not self-captioned
# slides -- whatever places one (a slide master, a figure environment, a
# poster column) supplies its own title and citation. ``title_for_a11y``
# still goes into an invisible <title> element for accessibility/tooling.
# --------------------------------------------------------------------------- #
def svg_open(title_for_a11y: str) -> str:
    return (
        f'<svg width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
        f'<title>{xml_escape(title_for_a11y)}</title>\n'
        f'<rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" fill="#ffffff"/>\n'
        f'{ARROW_DEFS}\n'
    )


def svg_close() -> str:
    return "</svg>\n"


# --------------------------------------------------------------------------- #
# Text and small-mark helpers added in this repo (not in bb-5kbc-visuals).
# --------------------------------------------------------------------------- #
def svg_text(x: float, y: float, s: str, *, size: float = 13, weight: int = 400,
             color: str = TEXT_DARK, anchor: str = "start", italic: bool = False,
             baseline: str = "auto", opacity: float = 1.0) -> str:
    """One line of text. ``weight`` 400 or 500 (the two vendored cuts)."""
    style = ' font-style="italic"' if italic else ""
    op = f' opacity="{opacity}"' if opacity != 1.0 else ""
    wt = ' font-weight="500"' if weight >= 500 else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" dominant-baseline="{baseline}" '
            f'font-family="Fira Sans" font-size="{size}"{wt}{style}{op} fill="{color}">'
            f'{xml_escape(s)}</text>')


def wrap_lines(s: str, max_width: float, size: float) -> list[str]:
    """Greedy word wrap against the rough Fira Sans width estimate."""
    lines: list[str] = []
    current = ""
    for word in s.split():
        trial = f"{current} {word}".strip()
        if current and text_width(trial, size) > max_width:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def svg_text_block(x: float, y: float, s: str, max_width: float, *, size: float = 13,
                   line_h: float | None = None, **kw) -> tuple[str, float]:
    """Wrapped paragraph; returns (markup, y of the line after the block)."""
    line_h = line_h or size * 1.35
    parts = []
    for i, line in enumerate(wrap_lines(s, max_width, size)):
        parts.append(svg_text(x, y + i * line_h, line, size=size, **kw))
    return "\n".join(parts), y + len(parts) * line_h


def svg_chip(x: float, y: float, label: str, colors: dict, *, size: float = 11.5,
             h: float = 22, dashed: bool = False, pad: float = 10,
             width: float | None = None, align: str = "middle") -> tuple[str, float]:
    """A rounded identifier chip ("Wikidata Q104295278"); returns (markup, width).

    ``width`` fixes the chip width (so a column of chips lines up); by default
    it hugs the label. ``align="start"`` sets the label flush left at ``pad``.
    """
    w = width if width is not None else text_width(label, size) + 2 * pad
    dash = ' stroke-dasharray="4 3"' if dashed else ""
    tx = x + pad if align == "start" else x + w / 2
    markup = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h/2:.1f}" '
              f'fill="{colors["fill"]}" stroke="{colors["stroke"]}" stroke-width="1.2"{dash}/>\n'
              + svg_text(tx, y + h / 2 + 0.5, label, size=size, weight=500,
                         anchor=align, baseline="central"))
    return markup, w


def svg_marker(cx: float, cy: float, number: str, colors: dict, *, r: float = 14,
               dashed: bool = False) -> str:
    """Numbered map/card marker: filled with the world's stroke colour, white number."""
    dash = ' stroke-dasharray="4 3"' if dashed else ""
    fill = "#ffffff" if dashed else colors["stroke"]
    text_col = colors["stroke"] if dashed else "#ffffff"
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" '
            f'stroke="{colors["stroke"]}" stroke-width="2"{dash}/>\n'
            + svg_text(cx, cy + 0.5, number, size=r * 1.05, weight=500, color=text_col,
                       anchor="middle", baseline="central"))


# --------------------------------------------------------------------------- #
# Panel and quotation card (introduced with figure 03; figure 02 keeps its own
# local copies so its output stays byte-identical).
# --------------------------------------------------------------------------- #
def svg_panel(x: float, y: float, w: float, h: float, colors: dict, kicker: str, title: str,
              *, head_h: float = 58) -> str:
    """White panel with a tinted header strip (kicker line + title line)."""
    return "\n".join([
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#ffffff" '
        f'stroke="{colors["stroke"]}" stroke-width="1.6"/>',
        f'<path d="M {x} {y + 12} Q {x} {y} {x + 12} {y} L {x + w - 12} {y} '
        f'Q {x + w} {y} {x + w} {y + 12} L {x + w} {y + head_h} L {x} {y + head_h} Z" '
        f'fill="{colors["fill"]}"/>',
        svg_text(x + 20, y + 25, kicker, size=12.5, weight=500, color=colors["stroke"]),
        svg_text(x + 20, y + 47, title, size=17, weight=500),
    ])


def quote_source(q: dict, lang: str) -> str:
    """'Barbara Fischer · c’t 19/2026, S. 120' -- speaker resolved from quotes.yaml."""
    who = q.get("speaker")
    if who == "author":
        who = t(lang, "Autorentext", "author's text")
    elif who == "indirect":
        who = t(lang, "indirekte Rede", "reported speech")
    page = t(lang, f"S. {q['page']}", f"p. {q['page']}")
    tr = "" if lang == "de" else ", transl."
    return f"{who} · c’t 19/2026, {page}{tr}"


def svg_quote_card(x: float, y: float, w: float, text: str, source: str, lang: str, *,
                   size: float = 15, italic: bool = True, quote_marks: bool = True,
                   colors: dict | None = None, min_h: float = 0) -> tuple[str, float]:
    """Quotation card sized to its text; returns (markup, bottom y)."""
    colors = colors or QUOTE
    if quote_marks:
        text = f"„{text}“" if lang == "de" else f"“{text}”"
    lines = wrap_lines(text, w - 40, size)
    h = max(min_h, 26 + len(lines) * size * 1.4 + 30)
    block, _ = svg_text_block(x + 20, y + 30, text, w - 40, size=size, line_h=size * 1.4, italic=italic)
    return "\n".join([
        f'<rect x="{x}" y="{y:.1f}" width="{w}" height="{h:.1f}" rx="10" '
        f'fill="{colors["fill"]}" stroke="{colors["stroke"]}" stroke-width="1.2"/>',
        block,
        svg_text(x + w - 18, y + h - 12, source, size=11.5, color=colors["stroke"], anchor="end"),
    ]), y + h
