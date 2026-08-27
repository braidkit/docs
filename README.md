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

The marketing site owns Braid's shared brand capsule. It publishes static brand
files at:

```text
https://braidkit.io/brand/tokens.css
https://braidkit.io/brand/manifest.json
https://braidkit.io/brand/logo/...
```

The docs site imports the shared token CSS through
`docs/stylesheets/brand.css`. That adapter maps Braid tokens into MkDocs
Material variables, adds docs-specific layout styles, and keeps fallback values
so local previews still look right when the marketing site has not deployed a
new capsule yet.

MkDocs needs concrete image paths for its logo and favicon, so this repo keeps
local copies in `docs/assets/brand/logo/`. Treat those as copies from the
marketing site's `public/brand/logo/` folder, not as a new source of truth.

The deploy order matters when brand assets change:

1. Merge and deploy the marketing site change that publishes `/brand/...`.
2. Refresh local logo copies here if the image asset changed.
3. Merge the docs change that consumes the new brand asset or token.

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
