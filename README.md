# Braid Docs

Source for [docs.braidkit.io](https://docs.braidkit.io), built with MkDocs
Material and Braid's documentation shell.

## Current scope

The launch branch contains the documentation home, existing concept and
installation pages, and clearly marked outlines for launch guidance.
An outline is a writing brief, not a working tutorial or a shipped feature.
See [LAUNCH.md](LAUNCH.md) for the minimum content set and its Linear sources.

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
draft: true
---
```

`draft: true` displays an outline notice and labels links on the home page.
It does **not** hide the page or protect access. Replace the outline with
reviewed guidance and remove that field when it is ready.

Keep commands out of outlines until verified against the applicable release.
Record release applicability and authoritative sources for operational pages.
Writing prompts live in HTML comments so the preview shows the heading
structure without invented instructions.

Add pages to `nav` in `mkdocs.yml`. The sidebar uses four collapsible groups:
Get started, Guides, Concepts, and Reference. The active group expands by default;
other groups can be opened when needed.
Get help and Changelog stay in the build/navigation data for validation and
discovery, but their links appear in the support footer and section switcher
rather than twice in the sidebar.

Quickstart owns one complete first example, including hosted sign-in. Guides
cover recurring tasks: capture, understanding a change, and review. Concepts
explain the model and evidence; Reference holds exact commands, states, machine
configuration, account/device details, troubleshooting, and preview limits.
See `LAUNCH.md` for page boundaries, writing requirements, and source issues.

Home-page navigation is defined under `extra.home` in `mkdocs.yml` and rendered
by `overrides/home.html`. `docs/index.md` carries the same links for readers of
the agent corpus; `scripts/check_site.py` fails when the two drift apart.

## Agent-readable docs

`scripts/build_llms.py` runs before every build, including Cloudflare.
It generates ignored `docs/llms.txt` and `docs/llms-full.txt` from nav pages:

- descriptions and YAML frontmatter are validated;
- grouped navigation retains its reading order;
- outlines appear in the index as unwritten and are omitted from the full text;
- unchanged outputs are not rewritten, avoiding a live-reload loop.

These files and the search index contain documentation content and must be
covered by the same access gate as the HTML.

The corpus generator, page-Markdown publisher, and site contract checker read
the shared project configuration without importing MkDocs internals. MkDocs
still invokes the publishers through thin hook adapters; they can also run as
standalone commands for another builder.

## Branding and layout

- `braid-tokens.css`: the shared tokens, vendored from `braidkit/brand`.
- `docs/stylesheets/tokens.css`: maps those onto the names this site and Material use.
- `fonts.css`: locally hosted fonts; see [FONTS.md](FONTS.md).
- `base.css`: article typography, tables, code, callouts.
- `shell.css`: header, navigation, search, outline, responsive drawer.
- `home.css`: navigation cards and outline notices.
- `overrides/`: focused Material template overrides.

The tokens, typefaces, icons and the header mark are copies owned by
[`braidkit/brand`](https://github.com/braidkit/brand). Change them there, not
here. The design rules they implement are `DESIGN.md` in that repository, and
[AGENTS.md](AGENTS.md) covers the rest of working here.

Nothing is fetched at runtime; every asset is served from this site's own
origin.

Keep structural desktop rules inside their desktop media query. Material owns
the mobile drawer and its label/checkbox controls; replacing those controls
or leaking desktop layout into the drawer has previously broken navigation.

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
that an outline is ready to launch. Follow [DEPLOYMENT.md](DEPLOYMENT.md) for
access verification, public launch, and rollback.

## Builder migration

Material for MkDocs is in its final maintenance period. Production remains on
the pinned MkDocs and Material versions while Zensical compatibility is added
and verified in reversible stages. See
[ZENSICAL_MIGRATION.md](ZENSICAL_MIGRATION.md) for the evidence, constraints,
cutover criteria, and rollback plan.
