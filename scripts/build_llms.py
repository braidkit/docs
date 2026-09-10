#!/usr/bin/env python3
"""Generate llms.txt and llms-full.txt from the published documentation.

The corpus follows the mkdocs nav, including grouped sections and utility
pages. Draft pages are listed as outlines, but their empty bodies are omitted.

MkDocs runs this as a pre-build hook, so local, CI, and Cloudflare builds all
regenerate the corpus from the pages. The outputs are gitignored.

Run with --check to compare without writing, which is useful locally.
"""

import argparse
import pathlib
import sys

import yaml
from mkdocs.config import load_config
from mkdocs.structure.files import get_files
from mkdocs.structure.nav import get_navigation

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"

SITE = "https://docs.braidkit.io"
INTRO = "Braid records the decisions and reasoning behind a change, from people and agents alike, and keeps that record with the code."


def nav_entries(config):
    """Return ``[(title, source path)]`` from MkDocs' parsed navigation.

    Letting MkDocs interpret its own config keeps this generator compatible
    with nested sections and every navigation form MkDocs supports. It also
    means the corpus uses the same resolved titles and order as the site.
    """
    files = get_files(config)
    navigation = get_navigation(files, config)
    entries = [(page.title, page.file.src_uri) for page in navigation.pages]
    if not entries:
        sys.exit("mkdocs.yml nav lists no pages")
    return entries


def split_front_matter(text):
    """Return (metadata, body). Front matter is optional."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    meta = yaml.safe_load(text[4:end]) or {}
    if not isinstance(meta, dict):
        raise ValueError("front matter must be a YAML mapping")
    return meta, text[end + 5 :].lstrip("\n")


def page_url(path):
    if path == "index.md":
        return SITE + "/"
    return f"{SITE}/{path[:-3]}/"


def describe(meta, path):
    """Every published page must carry its own description.

    Guessing one from the body produced HTML fragments and half sentences, and
    this text is what an agent reads to decide whether to fetch the page. A
    missing description is a build failure so it gets written deliberately.
    """
    description = meta.get("description", "").strip()
    if not description:
        sys.exit(f"{path} has no 'description' in its front matter; add one")
    return description


def render(entries):
    index = [f"# Braid documentation", "", f"> {INTRO}", ""]
    full = [
        "# Braid documentation",
        "",
        f"> {INTRO}",
        "",
        "Page content follows in navigation order. Unwritten outlines are listed in llms.txt and omitted here.",
        "",
    ]

    for title, path in entries:
        source = DOCS / path
        if not source.exists():
            sys.exit(f"nav lists {path}, which does not exist")
        try:
            meta, body = split_front_matter(source.read_text())
        except (yaml.YAMLError, ValueError) as error:
            sys.exit(f"{path}: invalid YAML front matter: {error}")
        page_title = str(meta.get("title") or title)
        description = describe(meta, path)
        if meta.get("draft"):
            index.append(f"- [{page_title}]({page_url(path)}): Outline only; instructions have not been written.")
            continue
        index.append(f"- [{page_title}]({page_url(path)}): {description}")
        full.append(f"## {page_title}")
        full.append("")
        full.append(f"Source: {page_url(path)}")
        full.append("")
        full.append(body.rstrip())
        full.append("")

    return "\n".join(index).rstrip() + "\n", "\n".join(full).rstrip() + "\n"


def write_corpus(config):
    index_text, full_text = render(nav_entries(config))
    for path, text in [(DOCS / "llms.txt", index_text), (DOCS / "llms-full.txt", full_text)]:
        # MkDocs watches the documentation directory in serve mode. Rewriting
        # an unchanged generated file causes a filesystem event, which starts
        # another build and an endless live-reload loop.
        if path.exists() and path.read_text() == text:
            continue
        path.write_text(text)
        print(f"wrote {path.relative_to(ROOT)}")


def on_config(config):
    """Write discovery files before MkDocs collects documentation files."""
    write_corpus(config)
    return config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if the generated files are stale")
    args = parser.parse_args()

    config = load_config(config_file=str(MKDOCS))
    index_text, full_text = render(nav_entries(config))
    targets = [(DOCS / "llms.txt", index_text), (DOCS / "llms-full.txt", full_text)]

    if args.check:
        stale = [str(p.relative_to(ROOT)) for p, want in targets if not p.exists() or p.read_text() != want]
        if stale:
            sys.exit("stale, run scripts/build_llms.py: " + ", ".join(stale))
        print("llms.txt and llms-full.txt are current")
        return

    write_corpus(config)


if __name__ == "__main__":
    main()
