# tmp/ — work in progress

Material for steps that are still being designed. Nothing in `tmp/` is read
by `main.py`, and nothing here is a publishable figure. Once a step is
settled, its code moves into `py/step_NN_*.py`, its inputs into `data/raw/`,
and the corresponding folder here is deleted.

## s5-ogham/ — case study Ogham (PRIMER S5)

| Path | What |
|---|---|
| `fragebogen.md` | Open questions on the two stones (CIIC 81, CIIC 178), with what the EpiDoc editions already answer; answers go after `→` |
| `mock_ogham.py` | Mock-ups of the three case-study figures A (roles), B (place chain), C (graph behind the inscription); German only |
| `img/mock-*.de.png` | The mock-ups as rendered on 2026-09-22, kept for reference |
| `raw/epidoc/I-COR-030.xml`, `I-KER-046.xml` | OG(H)AM EpiDoc editions of CIIC 81 and CIIC 178, [lguariento/og-h-am](https://github.com/lguariento/og-h-am) commit `0a2c7a0` (2026-09-20), CC BY 4.0 |
| `raw/wikidata/Q126503090.json` | Wikidata item of the Coumeenoole stone (`Special:EntityData`, 2026-09-22), CC0 |
| `raw/fuzzy-sl/Q131.json` | fuzzy-sl Wikibase item of the Coumeenoole stone (two coordinate statements with source and certainty), 2026-09-22 |

Re-render the mock-ups (writes SVG and PNG into `tmp/s5-ogham/img/`):

    python tmp/s5-ogham/mock_ogham.py

The mock-ups hard-code their values. Cells shown dashed with a "?" are
answers still outstanding in `fragebogen.md`.
