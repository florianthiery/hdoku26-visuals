#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_10_abschluss.py -- the three closing figures
=================================================

After five case studies the talk needs a summary that is not a scorecard.
These three figures deliberately carry far less text than the case studies:
a mark, a short label, and the case study it comes from.

  A  ``arbeitsteilung``   what each of the four holds best -- twelve
                          capabilities, four columns of marks, and one line per
                          column on where it stops
  B  ``fehlende-kante``   the five gaps the case studies found, and how wide
                          each one is: four of them are one statement
  C  ``tiefe``            how far down each hub actually reaches, read off the
                          ten chains of places drawn in the case studies

Everything shown here was established in steps 05 to 09; the summary itself is
``manual/abschluss.yaml``, where every row names the case study it mirrors.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "py"))

import yaml  # noqa: E402

import hdoku26_visuals_utils as vu  # noqa: E402

RAW = vu.DATA_RAW
OUT = vu.OUT_DIRS["10-abschluss"]

GND, WD, AGG, OSM = vu.GND, vu.COMMUNITY, vu.AGGREGATOR, vu.OSM
UNC = {"fill": vu.UNCERTAIN_FILL, "stroke": vu.UNCERTAIN_STROKE}
T = vu.svg_text

COLUMNS = (("G", "GND", GND),
           ("W", "Wikidata", WD),
           ("O", "OpenStreetMap", OSM),
           ("F", None, AGG))          # label depends on the language


def _hub_label(key: str, lang: str) -> str:
    if key == "F":
        return vu.t(lang, "Fachdaten", "research data")
    return next(label for k, label, _ in COLUMNS if k == key)


def load() -> dict:
    return yaml.safe_load((RAW / "manual" / "abschluss.yaml").read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# Figure A -- what each one holds best
# --------------------------------------------------------------------------- #
def _fig_a(d: dict, lang: str) -> str:
    de = lang == "de"
    p = [vu.svg_open(vu.t(lang, "Arbeitsteilung: was jedes System am besten hält",
                          "Division of labour: what each system holds best"))]
    LX, RX = vu.MARGIN_X, vu.CANVAS_W - vu.MARGIN_X
    label_x = LX + 16
    col_x = [720 + i * 200 for i in range(4)]
    source_x = RX - 16

    p.append(T(LX, 78, vu.t(lang, "Keines der vier ersetzt ein anderes.",
                            "None of the four replaces another."), size=24, weight=500))

    for (key, _, colors), cx in zip(COLUMNS, col_x):
        p.append(T(cx, 132, _hub_label(key, lang), size=15, weight=500,
                   color=colors["stroke"], anchor="middle"))
    p.append(f'<line x1="{LX}" y1="152" x2="{RX}" y2="152" '
             f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')

    row_h = 52
    y = 152
    for i, row in enumerate(d["matrix"]):
        y += row_h
        cy = y - row_h / 2
        if i % 2 == 0:
            p.append(f'<rect x="{LX}" y="{y - row_h:.0f}" width="{RX - LX}" height="{row_h}" '
                     f'rx="8" fill="#f4f3ef"/>')
        p.append(T(label_x, cy, row["de" if de else "en"], size=15, baseline="central"))
        for (key, _, colors), cx in zip(COLUMNS, col_x):
            mark = row["marks"].get(key)
            if mark == "ok":
                p.append(f'<circle cx="{cx}" cy="{cy:.1f}" r="11" fill="{colors["stroke"]}"/>')
            elif mark == "part":
                p.append(f'<circle cx="{cx}" cy="{cy:.1f}" r="9" fill="{colors["fill"]}" '
                         f'stroke="{colors["stroke"]}" stroke-width="1.6"/>')
            else:
                p.append(f'<circle cx="{cx}" cy="{cy:.1f}" r="2.5" fill="#d8d6cf"/>')
        p.append(T(source_x, cy, row["source"], size=11.5, color=vu.TEXT_MUTED,
                   anchor="end", baseline="central"))

    # where each one stops
    y += 34
    p.append(T(LX + 16, y, vu.t(lang, "Und wo es aufhört:", "And where it stops:"),
               size=13, weight=500, color=vu.TEXT_MUTED))
    y += 26
    for (key, _, colors), cx in zip(COLUMNS, [LX + 16 + i * 410 for i in range(4)]):
        limit = d["limits"][key]
        p.append(f'<rect x="{cx}" y="{y - 11}" width="6" height="22" rx="3" '
                 f'fill="{colors["stroke"]}"/>')
        p.append(T(cx + 16, y - 1, _hub_label(key, lang), size=12.5, weight=500,
                   color=colors["stroke"], baseline="central"))
        p.append(T(cx + 16, y + 16, limit["de" if de else "en"], size=12,
                   color=vu.TEXT_MUTED, baseline="central"))

    p.append(T(LX, 962, vu.t(
        lang, "ausgefüllt: hält das · offen: teilweise",
        "filled: holds it · open: in part"), size=12, color=vu.TEXT_MUTED))
    p.append(vu.svg_close())
    return "\n".join(p)


# --------------------------------------------------------------------------- #
# Figure B -- the five gaps, and how wide they are
# --------------------------------------------------------------------------- #
def _fig_b(d: dict, lang: str) -> str:
    de = lang == "de"
    p = [vu.svg_open(vu.t(lang, "Was fehlt, ist meistens eine Kante",
                          "What is missing is usually an edge"))]
    LX, RX = vu.MARGIN_X, vu.CANVAS_W - vu.MARGIN_X

    p.append(T(LX, 78, vu.t(lang, "Fünf Lücken aus fünf Fallstudien.",
                            "Five gaps from five case studies."), size=24, weight=500))

    case_x, box_x, gap, bw, bh = LX + 16, LX + 190, 118, 230, 46
    text_x = box_x + bw + gap + bw + 40
    y = 186
    for row in d["edges"]:
        record = row["kind"] == "record"
        colors = UNC if record else GND
        p.append(T(case_x, y + bh / 2, row["case"], size=13.5, weight=500,
                   color=vu.TEXT_MUTED, baseline="central"))
        left = row.get("from_de" if de else "from_en") or row["from"]
        right = row.get("to_de" if de else "to_en") or row["to"]
        p.append(vu.case_node(box_x, y, bw, left, "", kind="place", h=bh))
        p.append(vu.case_node(box_x + bw + gap, y, bw, right, "",
                              kind="concept" if record else "place", h=bh))
        p.append(vu.svg_arrow(box_x + bw, y + bh / 2, box_x + bw + gap, y + bh / 2,
                              dashed=True, marker="arrow-uncertain",
                              stroke=vu.UNCERTAIN_STROKE))
        p.append(T(box_x + bw + gap / 2, y + bh / 2 - 22, "?", size=17, weight=500,
                   color=vu.UNCERTAIN_STROKE, anchor="middle", baseline="central"))
        p.append(T(text_x, y + bh / 2, row["missing_de" if de else "missing_en"],
                   size=14.5, baseline="central"))
        chip, w = vu.svg_chip(0, 0, row["cost_de" if de else "cost_en"], colors, size=12.5, h=26)
        chip, _ = vu.svg_chip(RX - w, y + bh / 2 - 13, row["cost_de" if de else "cost_en"],
                              colors, size=12.5, h=26)
        p.append(chip)
        y += 128

    note, _ = vu.svg_text_block(LX + 16, y + 40, d["edges_note"]["de" if de else "en"],
                                1560, size=16, line_h=26)
    p.append(note)
    p.append(vu.svg_close())
    return "\n".join(p)


# --------------------------------------------------------------------------- #
# Figure C -- how far down each hub reaches
# --------------------------------------------------------------------------- #
def _fig_c(d: dict, lang: str) -> str:
    de = lang == "de"
    p = [vu.svg_open(vu.t(lang, "Tiefe der Verortung", "How far down the localisation goes"))]
    LX, RX = vu.MARGIN_X, vu.CANVAS_W - vu.MARGIN_X

    p.append(T(LX, 78, vu.t(lang, "Wie weit jedes System hinunterreicht.",
                            "How far down each system reaches."), size=24, weight=500))

    levels = d["levels"]
    axis_x0, axis_x1 = LX + 300, RX - 250
    step = (axis_x1 - axis_x0) / (len(levels) - 1)

    def level_x(level: int) -> float:
        return axis_x0 + (level - 1) * step

    # the scale, drawn once
    axis_y = 132
    for i, level in enumerate(levels):
        x = axis_x0 + i * step
        p.append(T(x, axis_y, level["de" if de else "en"], size=12, color=vu.TEXT_MUTED,
                   anchor="middle", baseline="central"))
    p.append(f'<line x1="{LX}" y1="{axis_y + 18}" x2="{RX}" y2="{axis_y + 18}" '
             f'stroke="{vu.LINE_NEUTRAL}" stroke-width="1"/>')
    for i in range(len(levels)):
        x = axis_x0 + i * step
        p.append(f'<line x1="{x:.1f}" y1="{axis_y + 30}" x2="{x:.1f}" y2="918" '
                 f'stroke="#e6e4dd" stroke-width="1"/>')

    bar_h, bar_gap, row_gap, group_gap = 9, 4, 12, 22
    y = axis_y + 40
    previous_case = None
    for row in d["depth"]:
        if previous_case is not None and row["case"] != previous_case:
            y += group_gap
        previous_case = row["case"]
        block_h = 4 * bar_h + 3 * bar_gap
        p.append(T(LX + 16, y + block_h / 2, row["label_de" if de else "label_en"],
                   size=13.5, weight=500, baseline="central"))
        p.append(T(LX + 16, y + block_h / 2 + 17, row["case"], size=11,
                   color=vu.TEXT_MUTED, baseline="central"))
        by = y
        for key, _, colors in COLUMNS:
            depth = row["depth"][key]
            x1 = level_x(depth)
            p.append(f'<rect x="{axis_x0 - 6:.1f}" y="{by}" width="{x1 - axis_x0 + 12:.1f}" '
                     f'height="{bar_h}" rx="{bar_h / 2}" fill="{colors["stroke"]}"/>')
            p.append(T(axis_x0 - 14, by + bar_h / 2, key, size=10.5, weight=500,
                       color=colors["stroke"], anchor="end", baseline="central"))
            by += bar_h + bar_gap
        note = row.get("note_de" if de else "note_en")
        if note:
            width = vu.CANVAS_W - vu.MARGIN_X - (axis_x1 + 26)
            lines = vu.wrap_lines(note, width, 11.5)
            block, _ = vu.svg_text_block(
                axis_x1 + 26, y + block_h / 2 - (len(lines) - 1) * 8 + 4, note, width,
                size=11.5, line_h=16, color=vu.TEXT_MUTED)
            p.append(block)
        y += block_h + row_gap

    p.append(vu.svg_legend(LX + 16, 886, [
        (f"G · {_hub_label('G', lang)}", GND),
        (f"W · {_hub_label('W', lang)}", WD),
        (f"O · {_hub_label('O', lang)}", OSM),
        (f"F · {_hub_label('F', lang)}", AGG),
    ], columns=4, col_w=220))
    note, _ = vu.svg_text_block(LX + 16, 948, d["depth_note"]["de" if de else "en"],
                                1500, size=14, line_h=22)
    p.append(note)
    p.append(vu.svg_close())
    return "\n".join(p)


# --------------------------------------------------------------------------- #
def build(lang: str = "de") -> list[str]:
    d = load()
    written = []
    written += vu.write_figure(OUT, f"arbeitsteilung.{lang}", _fig_a(d, lang), zoom=1.5)
    written += vu.write_figure(OUT, f"fehlende-kante.{lang}", _fig_b(d, lang), zoom=1.5)
    written += vu.write_figure(OUT, f"tiefe.{lang}", _fig_c(d, lang), zoom=1.5)
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
