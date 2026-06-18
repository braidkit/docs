# Braid Docs

Source for `docs.braidkit.io`.

The site is intentionally small and Markdown-first. The current focus is the
Braid protocol: entity relationships, event stories, and the `WorkEvent` model.

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

## Cloudflare Pages

Use the Git integration for this repository.

```text
Build command: mkdocs build
Build output directory: site
Production branch: main
Custom domain: docs.braidkit.io
Environment variable: PYTHON_VERSION=3.12
```
