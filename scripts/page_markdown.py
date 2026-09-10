#!/usr/bin/env python3
"""Publish each page's authored Markdown alongside its rendered HTML.

The page shell links to these files so readers can copy or open the original
Markdown without reconstructing it from HTML. MkDocs currently calls
``on_post_build`` as a compatibility adapter. The same publisher can run
directly after any builder that reads ``mkdocs.yml``.
"""

import argparse
import pathlib

import yaml

from site_config import (
    load_site_config,
    resolve_project_path,
    site_pages,
    split_front_matter,
)


ROOT = pathlib.Path(__file__).resolve().parent.parent
MKDOCS = ROOT / "mkdocs.yml"


def _yaml_scalar(value):
    """Render a quoted YAML scalar, including control characters, safely."""
    return yaml.safe_dump(
        str(value),
        allow_unicode=True,
        default_style='"',
        width=10**9,
    ).strip()


def markdown_destination(dest_uri):
    """Return the Markdown sidecar path for a rendered HTML destination."""
    stem = dest_uri[: -len(".html")]
    if stem.endswith("/index"):
        stem = stem[: -len("/index")]
    return stem + ".md"


def render_sidecar(page, source_text, site_url):
    """Render one authored Markdown page with portable source metadata."""
    metadata, markdown = split_front_matter(source_text)
    authored_title = metadata.get("title") or page.title
    front = ["---", f"title: {_yaml_scalar(authored_title)}"]
    site_url = (site_url or "").rstrip("/")
    if site_url:
        front.append(f"url: {_yaml_scalar(site_url + '/' + page.url)}")
    description = metadata.get("description", "")
    if description:
        front.append(f"description: {_yaml_scalar(description)}")
    front.append("---")
    return "\n".join(front) + "\n\n" + markdown.strip() + "\n"


def publish_markdown(config, site_dir=None):
    """Write sidecars for every configured navigation page."""
    docs_dir = resolve_project_path(config.get("docs_dir", "docs"), ROOT)
    output_dir = pathlib.Path(site_dir) if site_dir else resolve_project_path(
        config.get("site_dir", "site"), ROOT
    )
    for page in site_pages(config, ROOT):
        source = docs_dir / page.src_uri
        target = output_dir / markdown_destination(page.dest_uri)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            render_sidecar(
                page,
                source.read_text(encoding="utf-8"),
                config.get("site_url"),
            ),
            encoding="utf-8",
        )


def on_post_build(config):
    """Thin MkDocs adapter; other builders can call ``main`` directly."""
    publish_markdown(config)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "site_dir",
        nargs="?",
        type=pathlib.Path,
        help="rendered site directory (default: site_dir from mkdocs.yml)",
    )
    args = parser.parse_args()
    publish_markdown(load_site_config(MKDOCS), args.site_dir)


if __name__ == "__main__":
    main()
