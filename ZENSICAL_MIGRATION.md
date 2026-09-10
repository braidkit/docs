# Zensical migration plan

This plan keeps the current documentation design and URLs while moving the
site off Material for MkDocs in reversible stages.

## Why migrate

Material for MkDocs entered its final maintenance period in November 2025.
The maintainers will provide critical bug fixes and security updates through
November 5, 2026, while new feature development continues in Zensical:

- [Material for MkDocs end-of-life
  announcement](https://github.com/squidfunk/mkdocs-material/issues/8523)
- [Official Zensical migration guide](https://zensical.org/docs/compatibility/mkdocs/migration/)

Zensical is the successor from the same team. It reads `mkdocs.yml`, supports
the Material configuration surface, and offers a `classic` theme variant that
preserves Material's appearance and HTML structure. Its maintainers recommend
running both builders during evaluation and changing production only after
pages, navigation, search, plugins, and customizations have been compared.

## What we verified

On September 10, 2026, a disposable build of the current site was tested with
Zensical 0.0.60:

- all 17 configured pages rendered;
- strict mode passed after replacing one Python string method in a template
  with MiniJinja-compatible syntax;
- the existing Markdown extensions, stylesheets, JavaScript, navigation, and
  search configuration built successfully;
- page URLs retained their current directory-style shape.

This was a build-compatibility check, not visual approval. Desktop, mobile,
dark-mode, search, and interaction parity still need browser testing before a
production change.

Two incompatibilities were confirmed:

1. Zensical does not currently support the `hooks` setting in `mkdocs.yml`.
   Braid uses hooks to build `llms.txt`, `llms-full.txt`, and the Markdown copy
   of every page.
2. Zensical renders templates with MiniJinja, which cannot call arbitrary
   Python methods. Custom overrides must use compatible expressions, filters,
   and tests.

[Zensical 0.0.60 is classified as
alpha on PyPI](https://pypi.org/project/zensical/). Pin every evaluated and
production version rather than accepting unreviewed upgrades.

## Migration stages

### 1. Make publishing tools builder-neutral

Production remains on MkDocs.

- Keep the current hooks as thin MkDocs adapters so Cloudflare's build command
  does not change.
- Read navigation and site metadata directly from `mkdocs.yml` instead of
  importing MkDocs internals.
- Make the LLM corpus and page-Markdown publishers runnable as standalone
  commands.
- Make site contract checks independent of MkDocs internals.
- Use template syntax accepted by Jinja and MiniJinja.
- Add unit coverage for navigation, URL mapping, front matter, corpus output,
  and Markdown sidecars.

Rollback: revert this stage. The production builder and deployment settings
are unchanged.

### 2. Add a parallel Zensical build

Production still remains on MkDocs.

- Pin the evaluated Zensical version and use the `classic` theme variant.
- Add a builder-neutral build command that generates the corpus, builds the
  HTML, publishes Markdown sidecars, and runs the same contract checks.
- Run both MkDocs and Zensical in CI.
- Compare every route and generated publishing-boundary file.
- Test the home page, three-column layout, navigation, search, light and dark
  themes, mobile drawer, page outline, heading links, source links, page copy,
  previous/next controls, and persistent support link.

Rollback: remove the parallel job. MkDocs remains the production path.

### 3. Cut production over

Change production only when all exit criteria below pass.

- Make the Zensical pipeline the required CI build.
- Change the Cloudflare Pages build command to the same verified pipeline.
- Keep the pinned MkDocs toolchain available for at least several successful
  production deployments.
- Remove MkDocs only after the rollback window closes.
- Keep `mkdocs.yml`; moving to `zensical.toml` is a separate, optional change.

Rollback: restore the previous Cloudflare build command and redeploy the last
known-good MkDocs commit or Pages deployment.

## Production cutover criteria

- Both builders produce all configured page routes without warnings.
- `scripts/check_site.py` passes against the Zensical output.
- `llms.txt`, `llms-full.txt`, per-page Markdown, sitemap, robots policy, and
  response headers are present and correct.
- Search returns relevant results and keyboard behavior is unchanged.
- Desktop, tablet, and mobile screenshots show no unintended layout changes.
- Navigation, page outline, support access, heading links, Markdown actions,
  source links, theme switching, and instant navigation work as expected.
- Cloudflare preview deployment passes the checks in `DEPLOYMENT.md`.
- The MkDocs rollback command and last known-good deployment are recorded.

## Non-goals

- Redesigning the site or changing its information architecture.
- Rewriting the site in an unrelated documentation framework.
- Adopting Zensical's modern theme during the compatibility migration.
- Combining the builder change with a move to `zensical.toml`.
