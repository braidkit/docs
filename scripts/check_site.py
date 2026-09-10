#!/usr/bin/env python3
"""Check the generated site contracts that the custom docs shell relies on.

The builder's strict mode catches invalid configuration and broken links.
These checks cover the layer above that: every navigation page must publish
HTML and Markdown, the home page's visual and plain-text navigation must stay
aligned, and the custom desktop/mobile shell must keep its essential structure.
"""

import argparse
import pathlib
import re
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
HOME_MARKDOWN = ROOT / "docs" / "index.md"
SHELL_CSS = ROOT / "docs" / "stylesheets" / "shell.css"

HOME_LINK = re.compile(
    r"^- \[(?P<label>[^]]+)]\((?P<path>[^)]+)\)(?: — (?P<description>.+))?$"
)


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


def configured_home_items(config):
    home = config.get("extra", {}).get("home", {})
    items = []
    for section in home.get("sections", []):
        items.extend(section.get("cards", []))
    items.extend(home.get("explore", {}).get("links", []))
    return items


def configured_home_links(config):
    return [
        (item["label"], item["path"], item.get("description"))
        for item in configured_home_items(config)
    ]


def markdown_home_links():
    links = []
    for line in HOME_MARKDOWN.read_text(encoding="utf-8").splitlines():
        match = HOME_LINK.match(line)
        if match:
            links.append(
                (
                    match.group("label"),
                    match.group("path"),
                    match.group("description"),
                )
            )
    return links


def require_text(text, expected, location, errors):
    if expected not in text:
        errors.append(f"{location}: missing required contract {expected!r}")


def check_site(site_dir):
    config = load_site_config(MKDOCS)
    navigation = site_pages(config, ROOT)
    errors = []
    home_links = configured_home_links(config)

    if home_links != markdown_home_links():
        errors.append(
            "home navigation differs between mkdocs.yml and docs/index.md; "
            "keep the visual cards and plain-Markdown equivalent in the same order"
        )

    navigation_paths = {page.src_uri for page in navigation}
    for _, path, _ in home_links:
        if path not in navigation_paths:
            errors.append(f"home navigation points to {path}, which is not in MkDocs nav")

    site_url = (config.get("site_url") or "").rstrip("/")
    docs_dir = resolve_project_path(config.get("docs_dir", "docs"), ROOT)
    for item in configured_home_items(config):
        source = docs_dir / item["path"]
        if not source.is_file():
            continue
        metadata = front_matter(
            source.read_text(encoding="utf-8"),
            item["path"],
            errors,
        )
        if bool(item.get("draft")) != bool(metadata.get("draft")):
            errors.append(
                f"home navigation draft state for {item['path']} differs from "
                "the page front matter"
            )

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

    home_html = (site_dir / "index.html").read_text(encoding="utf-8")
    require_text(home_html, 'class="braid-home"', "index.html", errors)
    require_text(home_html, 'class="braid-home__card"', "index.html", errors)
    require_text(home_html, 'class="braid-nav__footer"', "index.html", errors)
    require_text(home_html, "Contact support", "index.html", errors)
    if "documentation is coming soon" in home_html:
        errors.append("index.html: the coming-soon placeholder must not be published")

    representative_page = next((page for page in navigation if not page.is_homepage), None)
    representative = site_dir / representative_page.dest_uri if representative_page else None
    if representative and representative.is_file():
        page_html = representative.read_text(encoding="utf-8")
        location = str(representative.relative_to(site_dir))
        source_url = (
            f"{config.get('repo_url', '').rstrip('/')}/"
            f"{config.get('edit_uri', '').lstrip('/')}"
            f"{representative_page.src_uri}"
        )
        for contract in (
            'class="md-sidebar md-sidebar--primary"',
            'class="md-sidebar md-sidebar--secondary"',
            'class="braid-nav__footer"',
            "data-braid-pageactions",
            "data-braid-copy-markdown",
            "Contact support",
            source_url,
        ):
            require_text(page_html, contract, location, errors)
    else:
        errors.append("representative non-home shell page is missing")

    pages_by_source = {page.src_uri: page for page in navigation}
    for source in ("get-help.md", "changelog.md"):
        utility_page = pages_by_source.get(source)
        if not utility_page:
            errors.append(f"utility page is missing from navigation: {source}")
            continue
        utility_path = site_dir / utility_page.dest_uri
        utility_html = utility_path.read_text(encoding="utf-8")
        if 'class="braid-pagenav"' in utility_html:
            errors.append(
                f"{utility_path.relative_to(site_dir)}: utility pages must not "
                "render previous/next navigation"
            )

    shell_css = SHELL_CSS.read_text(encoding="utf-8")
    for contract in (
        "@media screen and (min-width: 64em)",
        "@media screen and (min-width: 64em) and (max-width: 76.234375em)",
        "@media screen and (max-width: 63.984375em)",
        ".md-sidebar--primary .md-sidebar__scrollwrap",
        "height: 100% !important;",
        '[data-md-toggle="drawer"]:checked ~ .md-container .md-sidebar--primary',
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
