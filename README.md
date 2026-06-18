# Braid Docs

Source for `docs.braidkit.io`.

The site is intentionally small and Markdown-first. The current focus is the
Braid protocol: entity relationships, event stories, and the `WorkEvent` model.

## Brand

The docs theme consumes the shared brand capsule from the marketing site:

```text
https://braidkit.io/brand/tokens.css
```

Local CSS in `docs/stylesheets/brand.css` maps those tokens into MkDocs
Material and keeps fallback values for local development.

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
