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

The docs site consumes those files instead of keeping a separate copy of the
logo, colors, and type stack. In `mkdocs.yml`, the logo, favicon, and first CSS
file all point at `https://braidkit.io/brand/...`.

`docs/stylesheets/brand.css` is the local adapter layer. It maps Braid tokens
into MkDocs Material variables, adds a few docs-specific styles, and keeps
fallback values so local builds still work before the remote brand CSS loads.

The deploy order matters when brand assets change:

1. Merge and deploy the marketing site change that publishes `/brand/...`.
2. Merge the docs change that consumes the new brand asset or token.

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
