#!/usr/bin/env python3
"""Generate llms.txt and llms-full.txt from the published documentation.

The published set is the mkdocs nav. A page that is not in the nav is not
published, so it does not belong in either file.

CI runs this before every build, so the corpus is regenerated from the pages
rather than committed. The outputs are gitignored. Nothing can drift.

Run with --check to compare without writing, which is useful locally.
"""

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"

SITE = "https://docs.braidkit.io"
INTRO = "Braid records the decisions and reasoning behind a change, from people and agents alike, and keeps that record with the code."


def nav_entries():
    """Return [(title, path)] in nav order.

    mkdocs.yml is not parsed as YAML on purpose. The config uses Python-specific
    tags that a plain yaml.safe_load rejects, and the nav is a flat list of
    "- Title: path.md" lines, so a line scan is enough and adds no dependency.
    """
    lines = MKDOCS.read_text().splitlines()
    try:
        start = lines.index("nav:")
    except ValueError:
        sys.exit("mkdocs.yml has no nav block")

    entries = []
    for line in lines[start + 1 :]:
        if line and not line[0].isspace():
            break
        match = re.match(r"\s*-\s*(.+?):\s*(\S+\.md)\s*$", line)
        if match:
            entries.append((match.group(1).strip(), match.group(2).strip()))
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
    meta = {}
    for line in text[4:end].splitlines():
        key, sep, value = line.partition(":")
        if sep and not key.startswith(" "):
            meta[key.strip()] = value.strip().strip('"').strip("'")
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


def render():
    index = [f"# Braid documentation", "", f"> {INTRO}", ""]
    full = [
        "# Braid documentation",
        "",
        f"> {INTRO}",
        "",
        "The complete text of every published page follows, in navigation order.",
        "",
    ]

    for title, path in nav_entries():
        source = DOCS / path
        if not source.exists():
            sys.exit(f"nav lists {path}, which does not exist")
        meta, body = split_front_matter(source.read_text())
        index.append(f"- [{title}]({page_url(path)}): {describe(meta, path)}")
        full.append(f"## {title}")
        full.append("")
        full.append(f"Source: {page_url(path)}")
        full.append("")
        full.append(body.rstrip())
        full.append("")

    return "\n".join(index).rstrip() + "\n", "\n".join(full).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if the committed files are stale")
    args = parser.parse_args()

    index_text, full_text = render()
    targets = [(DOCS / "llms.txt", index_text), (DOCS / "llms-full.txt", full_text)]

    if args.check:
        stale = [str(p.relative_to(ROOT)) for p, want in targets if not p.exists() or p.read_text() != want]
        if stale:
            sys.exit("stale, run scripts/build_llms.py: " + ", ".join(stale))
        print("llms.txt and llms-full.txt are current")
        return

    for path, want in targets:
        path.write_text(want)
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
