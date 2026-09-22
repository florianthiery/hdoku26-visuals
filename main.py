#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py -- the single entry point of hdoku26-visuals
=====================================================

    python main.py                 all steps, in order
    python main.py --list          print steps and exit
    python main.py --only 01       one step
    python main.py --from 01       this step and everything after
    python main.py --skip 01       everything but this
    python main.py --dry-run       print the plan, run nothing
    python main.py --strict        a step that writes nothing is an error

Step modules are imported lazily, so --list and --dry-run need neither
rdflib nor resvg-py. Every step stays runnable on its own
(``python py/step_01_ein_name_viele_orte.py``).
"""

from __future__ import annotations

import argparse
import importlib
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "py"))

# (id, module, description)
STEPS: list[tuple[str, str, str]] = [
    ("01", "step_01_ein_name_viele_orte", "Garranes: one name, several places (GND vs. community hubs)"),
]


def _select(args: argparse.Namespace) -> list[tuple[str, str, str]]:
    ids = [s[0] for s in STEPS]
    for flag in ("only", "from_", "skip"):
        value = getattr(args, flag)
        if value and value not in ids:
            sys.exit(f"unknown step '{value}' -- known: {', '.join(ids)}")
    if args.only:
        return [s for s in STEPS if s[0] == args.only]
    selected = STEPS
    if args.from_:
        selected = selected[ids.index(args.from_):]
    if args.skip:
        selected = [s for s in selected if s[0] != args.skip]
    return selected


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the figures of hdoku26-visuals.")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--from", dest="from_")
    ap.add_argument("--skip")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    if args.list:
        for sid, module, desc in STEPS:
            print(f"{sid}  {module:<34} {desc}")
        return 0

    plan = _select(args)
    if args.dry_run:
        for sid, module, desc in plan:
            print(f"would run {sid}  {module}")
        return 0

    timings: list[tuple[str, float]] = []
    for sid, module, desc in plan:
        print(f"[{sid}] {desc}")
        t0 = time.perf_counter()
        written = importlib.import_module(module).main() or []
        timings.append((sid, time.perf_counter() - t0))
        if args.strict and not written:
            print(f"[{sid}] wrote nothing -- failing under --strict")
            return 1

    total = sum(t for _, t in timings) or 1.0
    print("\nstep  seconds  share")
    for sid, secs in timings:
        print(f"{sid:<5} {secs:7.2f}  {100 * secs / total:4.0f} %")
    return 0


if __name__ == "__main__":
    sys.exit(main())
