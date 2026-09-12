# Working in this repository

The Braid documentation site: MkDocs with the Material theme.

## Commands

```bash
python -m pip install -r requirements.txt   # setup
python scripts/brand/check.py               # vendored brand files match the lock
python -m unittest discover -s tests -v     # tests
python -m mkdocs build --strict             # warnings are errors
python scripts/build_llms.py --check        # generated corpus is current
python scripts/check_site.py site           # site contracts, after a build
```

CI runs all five in that order.

## Files you must not edit here

`scripts/brand/`, plus these, are copies owned by
[`braidkit/brand`](https://github.com/braidkit/brand):

```
docs/stylesheets/braid-tokens.css
docs/assets/fonts/
docs/assets/brand/icons/
docs/assets/brand/logo/braid-mark-purple-512.png
```

Editing one builds clean, passes review, and is reverted the next time anyone
vendors. `scripts/brand/check.py` fails CI when it happens. Change them in
`braidkit/brand` and run `python3 vendor.py ../docs` from a checkout of it.
`scripts/brand/files` declares what this repository takes and where it goes.

## Before writing any UI

Read [`scripts/brand/DESIGN.md`](scripts/brand/DESIGN.md), the shared foundation
for the marketing site, these docs and the console.

Colours, sizes, families and radii come from `braid-tokens.css`; never write one
inline. `docs/stylesheets/tokens.css` maps those onto the names this site and
Material use, and is where docs-specific values belong.

UI lives in `docs/stylesheets/` and `overrides/`.

## Content

Adding or renaming a page means updating the nav in `mkdocs.yml` and re-running
the corpus check, which regenerates `llms.txt`.

## Personal instructions

Keep yours out of this file. Both tools read a personal layer that stacks with
this one: `~/.claude/CLAUDE.md` for Claude Code, `~/.codex/AGENTS.md` for Codex.

For notes about this repository alone, `CLAUDE.local.md` is gitignored and loads
alongside `CLAUDE.md`. Codex's `AGENTS.override.md` replaces this file rather
than adding to it, so everything above is lost while one exists.
