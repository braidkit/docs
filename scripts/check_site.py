#!/usr/bin/env python3
"""Check the generated site contracts that the custom docs shell relies on.

The strict MkDocs build catches invalid configuration and broken links. These
checks cover the layer above that: every navigation page must publish HTML and
Markdown, the home page's visual and plain-text navigation must stay aligned,
and the custom desktop/mobile shell must keep its essential structure.
"""

import argparse
import pathlib
import re
import sys

import yaml
from mkdocs.config import load_config
from mkdocs.structure.files import get_files
from mkdocs.structure.nav import get_navigation
from page_markdown import markdown_destination

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
    end = text.find("\n---\n", 4)
    if end == -1:
        errors.append(f"{path}: Markdown sidecar has unterminated YAML front matter")
        return {}
    try:
        metadata = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError as error:
        errors.append(f"{path}: invalid YAML front matter: {error}")
        return {}
    if not isinstance(metadata, dict):
        errors.append(f"{path}: YAML front matter must be a mapping")
        return {}
    return metadata


def configured_home_links(config):
    home = config.extra.get("home", {})
    links = []
    for section in home.get("sections", []):
        for item in section.get("cards", []):
            links.append((item["label"], item["path"], item["description"]))
    for item in home.get("explore", {}).get("links", []):
        links.append((item["label"], item["path"], None))
    return links


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
    config = load_config(config_file=str(MKDOCS))
    navigation = get_navigation(get_files(config), config)
    errors = []
    home_links = configured_home_links(config)

    if home_links != markdown_home_links():
        errors.append(
            "home navigation differs between mkdocs.yml and docs/index.md; "
            "keep the visual cards and plain-Markdown equivalent in the same order"
        )

    navigation_paths = {page.file.src_uri for page in navigation.pages}
    for _, path, _ in home_links:
        if path not in navigation_paths:
            errors.append(f"home navigation points to {path}, which is not in MkDocs nav")

    site_url = (config.site_url or "").rstrip("/")
    for page in navigation.pages:
        html_path = site_dir / page.file.dest_uri
        if not html_path.is_file():
            errors.append(f"missing rendered page: {html_path.relative_to(site_dir)}")
            continue

        markdown_path = site_dir / markdown_destination(page.file.dest_uri)
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
        for field in ("title", "url", "description"):
            if not metadata.get(field):
                errors.append(f"{markdown_path.relative_to(site_dir)}: missing {field!r}")
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

    representative_page = next(
        (page for page in navigation.pages if not page.is_homepage),
        None,
    )
    representative = (
        site_dir / representative_page.file.dest_uri if representative_page else None
    )
    if representative and representative.is_file():
        page_html = representative.read_text(encoding="utf-8")
        location = str(representative.relative_to(site_dir))
        source_url = (
            f"{config.repo_url.rstrip('/')}/"
            f"{config.edit_uri.lstrip('/')}"
            f"{representative_page.file.src_uri}"
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

    pages_by_source = {page.file.src_uri: page for page in navigation.pages}
    for source in ("get-help.md", "changelog.md"):
        utility_page = pages_by_source.get(source)
        if not utility_page:
            errors.append(f"utility page is missing from navigation: {source}")
            continue
        utility_path = site_dir / utility_page.file.dest_uri
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

    print(f"Site contracts passed for {len(navigation.pages)} pages")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "site_dir",
        nargs="?",
        type=pathlib.Path,
        default=ROOT / "site",
        help="rendered MkDocs directory (default: site)",
    )
    args = parser.parse_args()
    if not args.site_dir.is_dir():
        sys.exit(f"site directory does not exist: {args.site_dir}")
    raise SystemExit(check_site(args.site_dir.resolve()))


if __name__ == "__main__":
    main()
