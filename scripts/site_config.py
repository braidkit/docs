#!/usr/bin/env python3
"""Read the documentation structure without depending on a site builder.

MkDocs and Zensical can both read ``mkdocs.yml``. The publishing helpers only
need a small, stable subset of that file: paths, site metadata, and explicit
navigation. Keeping that interpretation here lets the generated Markdown
corpus and contract checks run under either builder.
"""

from dataclasses import dataclass
import pathlib

import yaml


ROOT = pathlib.Path(__file__).resolve().parent.parent
MKDOCS = ROOT / "mkdocs.yml"


class SiteConfigLoader(yaml.SafeLoader):
    """Safe YAML loader that preserves Python-name tags as inert strings."""


def _python_name(loader, suffix, node):
    del loader, node
    return suffix


SiteConfigLoader.add_multi_constructor(
    "tag:yaml.org,2002:python/name:",
    _python_name,
)


@dataclass(frozen=True)
class SitePage:
    """The builder-independent page fields used by publishing checks."""

    title: str
    src_uri: str
    url: str
    dest_uri: str
    is_homepage: bool


def load_site_config(path=MKDOCS):
    data = pathlib.Path(path).read_text(encoding="utf-8")
    data = yaml.load(data, Loader=SiteConfigLoader)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def split_front_matter(text):
    """Return ``(metadata, body)``; front matter is optional."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("unterminated YAML front matter")
    metadata = yaml.safe_load(text[4:end]) or {}
    if not isinstance(metadata, dict):
        raise ValueError("front matter must be a YAML mapping")
    return metadata, text[end + 5 :].lstrip("\n")


def nav_entries(config):
    """Flatten explicit navigation into ``[(label, source path)]``."""
    entries = []

    def visit(node):
        if isinstance(node, str):
            fallback = pathlib.PurePosixPath(node).stem.replace("-", " ").title()
            entries.append((fallback, node))
            return
        if isinstance(node, list):
            for item in node:
                visit(item)
            return
        if isinstance(node, dict):
            for label, target in node.items():
                if isinstance(target, str):
                    entries.append((str(label), target))
                else:
                    visit(target)
            return
        raise ValueError(f"unsupported nav entry: {node!r}")

    visit(config.get("nav", []))
    if not entries:
        raise ValueError("mkdocs.yml nav lists no pages")
    return entries


def page_route(src_uri):
    """Return the directory-style URL for a Markdown source path."""
    path = pathlib.PurePosixPath(src_uri)
    if path.name == "index.md":
        return "" if str(path.parent) == "." else str(path.parent).rstrip("/") + "/"
    return str(path.with_suffix("")) + "/"


def html_destination(src_uri, use_directory_urls=True):
    path = pathlib.PurePosixPath(src_uri)
    if path.name == "index.md":
        return str(path.with_suffix(".html"))
    if use_directory_urls:
        return str(path.with_suffix("") / "index.html")
    return str(path.with_suffix(".html"))


def site_pages(config, root=ROOT):
    """Resolve configured pages and authored titles in navigation order."""
    docs_dir = resolve_project_path(config.get("docs_dir", "docs"), root)
    directory_urls = config.get("use_directory_urls", True)
    pages = []
    for label, src_uri in nav_entries(config):
        source = docs_dir / src_uri
        if not source.is_file():
            raise ValueError(f"nav lists {src_uri}, which does not exist")
        metadata, _ = split_front_matter(source.read_text(encoding="utf-8"))
        pages.append(
            SitePage(
                title=str(metadata.get("title") or label),
                src_uri=src_uri,
                url=page_route(src_uri),
                dest_uri=html_destination(src_uri, directory_urls),
                is_homepage=src_uri == "index.md",
            )
        )
    return pages


def resolve_project_path(value, root=ROOT):
    path = pathlib.Path(value)
    return path if path.is_absolute() else pathlib.Path(root) / path
