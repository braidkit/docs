# Working in this repository

The Braid documentation site. MkDocs with the Material theme, built to static
HTML and deployed to Cloudflare Pages.

## Commands

```bash
python -m pip install -r requirements.txt   # setup
python scripts/brand/check.py               # vendored brand files match the lock
python -m unittest discover -s tests -v     # tests
python -m mkdocs build --strict             # build; warnings are errors
python scripts/build_llms.py --check        # generated corpus is current
python scripts/check_site.py site           # site contracts, after a build
```

CI runs all five in that order. Run them before opening a pull request.

## Files you must not edit here

Everything under `scripts/brand/`, plus these, are copies owned by
[`braidkit/brand`](https://github.com/braidkit/brand):

```
docs/stylesheets/braid-tokens.css
docs/assets/fonts/
docs/assets/brand/icons/
docs/assets/brand/logo/braid-mark-purple-512.png
```

Editing one works locally, builds clean, passes review, and is reverted the next
time anyone vendors. `scripts/brand/check.py` fails CI when it happens.

To change one, change it in `braidkit/brand` and run `python3 vendor.py ../docs`
from a checkout of that repository. `scripts/brand/files` declares which files
this repository takes and where they go.

## Before writing any UI

Read [`scripts/brand/DESIGN.md`](scripts/brand/DESIGN.md). It is the shared
design foundation for the marketing site, these docs and the console, and it is
vendored here so it is readable without network access.

It sets what has to hold. Where it is quiet, use judgment in the direction of
what it says.

Colours, sizes, families and radii come from
`docs/stylesheets/braid-tokens.css`. Do not write a hex value or a font size
inline. `docs/stylesheets/tokens.css` maps those shared tokens onto the names
this site and the Material theme use, and is the right place for docs-specific
values.

UI in this repository lives in:

```
docs/stylesheets/    base, home, shell, fonts, tokens
overrides/           Material theme templates and partials
```

## Content

Pages are Markdown under `docs/`, with navigation in `mkdocs.yml`. Adding or
renaming a page means updating the nav and re-running the corpus check, which
regenerates `llms.txt`.

## Pull requests

One topic per branch. Say what changed and why, and what you ran to check it.
