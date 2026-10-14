#!/usr/bin/env python3
"""Check the generated site contracts that the custom docs shell relies on.

The builder's strict mode catches invalid configuration and broken links.
These checks cover the layer above that: every navigation page must publish
HTML and Markdown, and the custom desktop/mobile shell must keep its essential
structure.
"""

import argparse
import pathlib
import sys

import yaml

from page_markdown import markdown_destination
from site_config import (
    load_site_config,
    resolve_project_path,
    site_pages,
    split_front_matter,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent
MKDOCS = ROOT / "mkdocs.yml"
SHELL_CSS = ROOT / "docs" / "stylesheets" / "shell.css"


def front_matter(text, path, errors):
    if not text.startswith("---\n"):
        errors.append(f"{path}: Markdown sidecar has no YAML front matter")
        return {}
    try:
        metadata, _ = split_front_matter(text)
    except (yaml.YAMLError, ValueError) as error:
        errors.append(f"{path}: invalid YAML front matter: {error}")
        return {}
    if not isinstance(metadata, dict):
        errors.append(f"{path}: YAML front matter must be a mapping")
        return {}
    return metadata


def require_text(text, expected, location, errors):
    if expected not in text:
        errors.append(f"{location}: missing required contract {expected!r}")


def check_site(site_dir):
    config = load_site_config(MKDOCS)
    navigation = site_pages(config, ROOT)
    errors = []

    site_url = (config.get("site_url") or "").rstrip("/")
    docs_dir = resolve_project_path(config.get("docs_dir", "docs"), ROOT)

    for page in navigation:
        html_path = site_dir / page.dest_uri
        if not html_path.is_file():
            errors.append(f"missing rendered page: {html_path.relative_to(site_dir)}")
            continue

        markdown_path = site_dir / markdown_destination(page.dest_uri)
        if not markdown_path.is_file():
            errors.append(
                f"missing Markdown source for {html_path.relative_to(site_dir)} "
                f"(expected {markdown_path.relative_to(site_dir)})"
            )
            continue

        metadata = front_matter(
            markdown_path.read_text(encoding="utf-8"),
            markdown_path.relative_to(site_dir),
            errors,
        )
        source_path = docs_dir / page.src_uri
        source_metadata = front_matter(
            source_path.read_text(encoding="utf-8"),
            page.src_uri,
            errors,
        )
        for field in ("title", "url", "description"):
            if not metadata.get(field):
                errors.append(f"{markdown_path.relative_to(site_dir)}: missing {field!r}")
        expected_title = source_metadata.get("title") or page.title
        if metadata.get("title") != expected_title:
            errors.append(
                f"{markdown_path.relative_to(site_dir)}: title is "
                f"{metadata.get('title')!r}, expected authored title {expected_title!r}"
            )
        expected_url = site_url + "/" + page.url
        if metadata.get("url") != expected_url:
            errors.append(
                f"{markdown_path.relative_to(site_dir)}: url is "
                f"{metadata.get('url')!r}, expected {expected_url!r}"
            )

    # A missing page is reported above; the shell is checked where it exists.
    shell_page = navigation[0]
    shell_path = site_dir / shell_page.dest_uri
    if shell_path.is_file():
        page_html = shell_path.read_text(encoding="utf-8")
        location = str(shell_path.relative_to(site_dir))
        source_url = (
            f"{config.get('repo_url', '').rstrip('/')}/"
            f"{config.get('edit_uri', '').lstrip('/')}"
            f"{shell_page.src_uri}"
        )
        for contract in (
            'class="md-sidebar md-sidebar--secondary"',
            'class="braid-header__help"',
            'class="md-header__option braid-theme"',
            "data-braid-pageactions",
            "data-braid-copy-markdown",
            "Get help",
            source_url,
        ):
            require_text(page_html, contract, location, errors)

    shell_css = SHELL_CSS.read_text(encoding="utf-8")
    for contract in (
        "@media screen and (min-width: 64em)",
        "@media screen and (max-width: 63.984375em)",
        ".md-sidebar--secondary:not([hidden]) ~ .md-content > .md-content__inner.md-typeset",
        ".braid-theme__option:has(:checked)",
        "margin-block-start: 160px;",
        "margin-block-start: -160px;",
    ):
        require_text(shell_css, contract, "docs/stylesheets/shell.css", errors)

    for output in ("robots.txt", "llms.txt", "llms-full.txt", "sitemap.xml"):
        if not (site_dir / output).is_file():
            errors.append(f"missing publishing-boundary output: {output}")

    if errors:
        print("Site contract check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Site contracts passed for {len(navigation)} pages")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "site_dir",
        nargs="?",
        type=pathlib.Path,
        default=ROOT / "site",
        help="rendered site directory (default: site)",
    )
    args = parser.parse_args()
    if not args.site_dir.is_dir():
        sys.exit(f"site directory does not exist: {args.site_dir}")
    raise SystemExit(check_site(args.site_dir.resolve()))


if __name__ == "__main__":
    main()
