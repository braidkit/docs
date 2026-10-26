# Braid Docs

Source for [docs.braidkit.io](https://docs.braidkit.io), built with MkDocs
Material and Braid's documentation shell.

## Current scope

The draft has two pages: Overview (`docs/index.md`) and Quickstart
(`docs/quickstart.md`).

Merging the site structure and opening the docs publicly are separate steps.
The site currently sends `noindex` headers and disallows crawling, but those
are **not access control**. Before deploying unfinished docs, configure and
verify the chosen access gate on the custom domain and all Pages hostnames.
The GitHub repository is public; website authentication does not hide its
Markdown source. See [DEPLOYMENT.md](DEPLOYMENT.md).

## Local development

Run these commands from the checkout you edit:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve --dev-addr 127.0.0.1:8919
```

Open [the local preview](http://127.0.0.1:8919/). Saving a Markdown file rebuilds
the site and refreshes the browser. A server watches only its own checkout;
another clone or worktree will not reflect your edits.

Verify a change:

```sh
python -m unittest discover -s tests -v
mkdocs build --strict
python scripts/build_llms.py --check
python scripts/check_site.py site
git diff --check
```

## Write a page

Every published page needs YAML frontmatter with a title and description.
Quote values containing a colon followed by a space:

```yaml
---
title: Quickstart
description: "Your first change: from setup to completion."
---
```

Verify commands against the current Braid release before publishing them.
Record release applicability and authoritative sources for operational pages.

Pages are listed under `nav` in `mkdocs.yml`, and the row above each article
links them in that order. Ask before adding one, as [AGENTS.md](AGENTS.md)
says. The header's Get help link comes from `extra.support`.

## Agent-readable docs

`scripts/build_llms.py` runs before every build, including Cloudflare.
It generates ignored `docs/llms.txt` and `docs/llms-full.txt` from nav pages:

- descriptions and YAML frontmatter are validated;
- grouped navigation retains its reading order;
- unchanged outputs are not rewritten, avoiding a live-reload loop.

These files contain documentation content and must be covered by the same
access gate as the HTML.

The corpus generator, page-Markdown publisher, and site contract checker read
the shared project configuration without importing MkDocs internals. MkDocs
still invokes the publishers through thin hook adapters; they can also run as
standalone commands for another builder.

## Branding and layout

- `braid-tokens.css`: the shared tokens, vendored from `braidkit/brand`.
- `docs/stylesheets/tokens.css`: maps those onto the names this site and Material use.
- `fonts.css`: locally hosted fonts; see [FONTS.md](FONTS.md).
- `base.css`: article typography, tables, code, buttons.
- `shell.css`: header, page actions, outline, previous/next, two-column layout.
- `overrides/`: focused Material template overrides.

The tokens, typefaces, icons and the header mark are copies owned by
[`braidkit/brand`](https://github.com/braidkit/brand). Change them there, not
here. The design rules they implement are `DESIGN.md` in that repository, and
[AGENTS.md](AGENTS.md) covers the rest of working here.

Nothing is fetched at runtime; every asset is served from this site's own
origin.

Keep structural desktop rules inside their desktop media query. Below it,
Material's own layout runs untouched, and desktop rules leaking into it have
broken navigation before.

## Deployment

Cloudflare Pages project: `braid-docs-site`. Production follows `main`.

```text
Build command: python -m pip install -r requirements.txt && python -m mkdocs build --strict
Build output directory: site
Environment variable: PYTHON_VERSION=3.12
Custom domain: docs.braidkit.io
```

CI checks the build, corpus, expected page outputs, and custom shell contracts.
A successful build does not establish that the deployed site is private or
that the writing is ready to launch. Follow [DEPLOYMENT.md](DEPLOYMENT.md) for
access verification, public launch, and rollback.

## Builder migration

Material for MkDocs is in its final maintenance period. Production remains on
the pinned MkDocs and Material versions while Zensical compatibility is added
and verified in reversible stages. See
[ZENSICAL_MIGRATION.md](ZENSICAL_MIGRATION.md) for the evidence, constraints,
cutover criteria, and rollback plan.
