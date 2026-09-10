#!/usr/bin/env python3
"""Publish each rendered page's Markdown source alongside its HTML.

The page shell links to these and the copy control fetches them, which is what
lets a reader hand a whole page to a model without scraping the rendered HTML
back into prose.

Conventions here follow what the major documentation sites already do rather
than inventing a scheme:

  - Front matter carries `title`, `url`, and `description`, the field set
    Mintlify emits (docs.claude.com). The `url` is what tells a model where the
    page came from, so a pasted page stays traceable to its source.
  - A page served at `/why-braid/` publishes its source at `/why-braid.md`,
    which is what Linear and Mintlify serve. Cloudflare uses
    `/why-braid/index.md` instead; we follow the former.
  - The content type is `text/markdown`, set in `docs/_headers`.

MkDocs runs this as a hook. `on_page_markdown` sees each page's body after the
front matter has been parsed into `page.meta`, so what ships is prose only, and
the front matter written here is rebuilt from the page's own metadata.
`on_post_build` writes the files, because the site directory is not populated
until the build has finished.
"""

import pathlib

import yaml

# src_uri -> (destination path relative to site_dir, file text).
# Rebuilt every build; `mkdocs serve` reuses the process across rebuilds, so it
# is cleared on each pre-build rather than accumulating deleted pages.
_pages: dict[str, tuple[str, str]] = {}


def on_pre_build(config):
    _pages.clear()


def _yaml_scalar(value):
    """Render a quoted YAML scalar, including control characters, safely."""
    return yaml.safe_dump(
        str(value),
        allow_unicode=True,
        default_style='"',
        width=10**9,
    ).strip()


def markdown_destination(dest_uri):
    """Return the path this page's Markdown is written to.

    A page built to `why-braid/index.html` is served at `/why-braid/` and its
    source at `/why-braid.md`. The site root keeps `index.md`, since it has no
    directory name to hoist.
    """
    stem = dest_uri[: -len(".html")]
    if stem.endswith("/index"):
        stem = stem[: -len("/index")]
    return stem + ".md"


def on_page_markdown(markdown, page, config, files):
    """Capture the body. Returning None leaves the rendered page untouched."""
    dest = page.file.dest_uri
    if not dest.endswith(".html"):
        return None

    metadata = page.meta or {}
    authored_title = metadata.get("title") or page.title
    front = ["---", f"title: {_yaml_scalar(authored_title)}"]
    site_url = (config.get("site_url") or "").rstrip("/")
    if site_url:
        front.append(f"url: {_yaml_scalar(site_url + '/' + page.url)}")
    description = metadata.get("description", "")
    if description:
        front.append(f"description: {_yaml_scalar(description)}")
    front.append("---")

    text = "\n".join(front) + "\n\n" + markdown.strip() + "\n"
    _pages[page.file.src_uri] = (markdown_destination(dest), text)
    return None


def on_post_build(config):
    site_dir = pathlib.Path(config["site_dir"])
    for dest_uri, text in _pages.values():
        target = site_dir / dest_uri
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
