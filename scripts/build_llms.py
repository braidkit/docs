#!/usr/bin/env python3
"""Generate llms.txt and llms-full.txt from the published documentation.

The corpus follows the configured navigation, including grouped sections and
utility pages. Draft pages are listed as outlines, but their empty bodies are
omitted.

MkDocs currently calls this module through ``on_config``. The generator itself
only reads ``mkdocs.yml`` and Markdown, so a future builder can run it directly
before building. The outputs are gitignored.

Run with --check to compare without writing, which is useful locally.
"""

import argparse
import pathlib
import sys

import yaml

from site_config import (
    load_site_config,
    nav_entries,
    page_route,
    resolve_project_path,
    split_front_matter,
)


ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"

SITE = "https://docs.braidkit.io"
INTRO = (
    "Braid records the decisions and reasoning behind a change, from people "
    "and agents alike, and keeps that record with the code."
)


def page_url(path, site_url=SITE):
    return f"{site_url.rstrip('/')}/{page_route(path)}"


def describe(meta, path):
    """Require an intentional description for every published page."""
    description = meta.get("description", "").strip()
    if not description:
        sys.exit(f"{path} has no 'description' in its front matter; add one")
    return description


def render(entries, docs_dir=DOCS, site_url=SITE):
    index = ["# Braid documentation", "", f"> {INTRO}", ""]
    full = [
        "# Braid documentation",
        "",
        f"> {INTRO}",
        "",
        "Page content follows in navigation order. Unwritten outlines are "
        "listed in llms.txt and omitted here.",
        "",
    ]

    for title, path in entries:
        source = pathlib.Path(docs_dir) / path
        if not source.exists():
            sys.exit(f"nav lists {path}, which does not exist")
        try:
            meta, body = split_front_matter(source.read_text(encoding="utf-8"))
        except (yaml.YAMLError, ValueError) as error:
            sys.exit(f"{path}: invalid YAML front matter: {error}")
        page_title = str(meta.get("title") or title)
        description = describe(meta, path)
        if meta.get("draft"):
            index.append(
                f"- [{page_title}]({page_url(path, site_url)}): "
                "Outline only; instructions have not been written."
            )
            continue
        index.append(f"- [{page_title}]({page_url(path, site_url)}): {description}")
        full.append(f"## {page_title}")
        full.append("")
        full.append(f"Source: {page_url(path, site_url)}")
        full.append("")
        full.append(body.rstrip())
        full.append("")

    return "\n".join(index).rstrip() + "\n", "\n".join(full).rstrip() + "\n"


def corpus_targets(config):
    docs_dir = resolve_project_path(config.get("docs_dir", "docs"), ROOT)
    site_url = config.get("site_url") or SITE
    index_text, full_text = render(nav_entries(config), docs_dir, site_url)
    return [
        (docs_dir / "llms.txt", index_text),
        (docs_dir / "llms-full.txt", full_text),
    ]


def write_corpus(config):
    for path, text in corpus_targets(config):
        # Live-preview servers watch the documentation directory. Rewriting an
        # unchanged generated file would trigger an endless rebuild loop.
        if path.exists() and path.read_text(encoding="utf-8") == text:
            continue
        path.write_text(text, encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")


def on_config(config):
    """Thin MkDocs adapter; other builders can call ``main`` directly."""
    write_corpus(config)
    return config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the generated files are stale",
    )
    args = parser.parse_args()

    config = load_site_config(MKDOCS)
    targets = corpus_targets(config)

    if args.check:
        stale = [
            str(path.relative_to(ROOT))
            for path, expected in targets
            if not path.exists() or path.read_text(encoding="utf-8") != expected
        ]
        if stale:
            sys.exit("stale, run scripts/build_llms.py: " + ", ".join(stale))
        print("llms.txt and llms-full.txt are current")
        return

    write_corpus(config)


if __name__ == "__main__":
    main()
