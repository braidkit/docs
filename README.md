# Braid Docs

Source for `docs.braidkit.io`.

The site is intentionally small and Markdown-first.

## Pre-launch state

Production currently contains only a coming-soon page. Earlier documentation
remains in this repository, but `exclude_docs` in `mkdocs.yml` prevents MkDocs
from publishing it. Re-enable pages only after their content has been reviewed
and is ready to publish.

The placeholder is intentionally excluded from search indexing through
`docs/robots.txt` and `docs/_headers`. Remove both indexing restrictions when
the reviewed documentation launches; do not remove them merely to test the
deployment mechanism.

## How Branding Works

braidkit.io is the source of truth for Braid's colors and type. It does **not**
publish them as a fetchable file — the tokens are inlined in the marketing
site's page `<style>` block, and `https://braidkit.io/brand/tokens.css` resolves
to `index.html` through the Cloudflare Pages SPA fallback (HTTP 200,
`text/html`). An `@import` of that URL is a silent no-op, so the docs keep a
local copy of the values instead.

`docs/stylesheets/brand.css` holds that copy at the top of the file: the light
tokens under `:root`, the dark tokens under `[data-md-color-scheme="slate"]`,
each annotated with the marketing-side variable it mirrors (`--bg`, `--ink`,
`--body`, `--muted`, `--faint`, `--line`, `--code-bg`, `--halo`). The rest of
the file maps those into MkDocs Material variables and adds docs layout styles.

To resync after a marketing brand change, read the `:root` and
`[data-theme=dark]` blocks in braidkit.io's served HTML and update the two token
blocks to match.

Type follows braidkit.io's monospace stack (`ui-monospace, SFMono-Regular,
Menlo, Consolas`) for the wordmark, headings, nav, and code. Long-form prose is
the one departure: it uses the system sans, which reads better at
reference-page length. No webfonts are loaded, and `theme.font` is `false` in
`mkdocs.yml` so Material does not add its own.

MkDocs needs concrete image paths for its logo and favicon, so this repo keeps
local copies in `docs/assets/brand/logo/`. Treat those as copies from the
marketing site's `public/brand/logo/` folder, not as a new source of truth.

When brand assets change, deploy the marketing site first, then refresh the
local logo copies and token blocks here.

## Local development

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Build the static site:

```sh
mkdocs build --strict
```

The build must contain the placeholder and its discovery files, and must not
contain any excluded pre-launch documentation.

## Cloudflare Pages

Use the Git integration for this repository.

```text
Build command: python -m pip install -r requirements.txt && python -m mkdocs build --strict
Build output directory: site
Production branch: main
Custom domain: docs.braidkit.io
Environment variable: PYTHON_VERSION=3.12
```

See `DEPLOYMENT.md` for project setup, verification, rollback, and recovery.
