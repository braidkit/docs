# Documentation site operations

This is for the Braid team member who manages the Cloudflare account and GitHub
deployment settings for `docs.braidkit.io`. It covers site setup, verification,
and recovery; it is not a guide for writing documentation.

Record the Cloudflare account and people with production access in the team's
infrastructure inventory. Do not put credentials or API tokens in this
repository.

## Deployment inventory

| Setting | Value |
| --- | --- |
| Source repository | `braidkit/docs` |
| Cloudflare Pages project | `braid-docs-site` |
| Production branch | `main` |
| Build command | `python -m pip install -r requirements.txt && python -m mkdocs build --strict` |
| Build output | `site` |
| Python | `3.12` |
| Production domain | `docs.braidkit.io` |
| Marketing redirect | `https://braidkit.io/docs` → `https://docs.braidkit.io/` |

## Create the Pages project

1. In the existing Braid Cloudflare account, create a Pages project connected
   to the `braidkit/docs` GitHub repository.
2. Use `main` as the production branch and the build settings in the inventory
   above. No framework preset or Pages Functions are required.
3. Keep automatic production and preview deployments enabled. Cloudflare will
   build non-production branches as previews.
4. Require the GitHub `mkdocs build` check before merging to `main`.
5. Confirm the first deployment on the generated `braid-docs-site.pages.dev` URL.

Cloudflare's build is a second build from the same commit; GitHub Actions is the
required pre-merge quality gate. The deployment page identifies the source
commit that produced each Cloudflare build.

## Attach the production domain

1. In the Pages project, add `docs.braidkit.io` under Custom domains.
2. Let Cloudflare create the proxied DNS record in the existing `braidkit.io`
   zone. Do not create only a standalone CNAME without first attaching the
   custom domain to the Pages project.
3. Wait for the domain and certificate to become active.
4. Deploy the marketing repository change that redirects `/docs` and `/docs/`
   to the canonical documentation domain.

## Private review before public launch

The launch branch builds the full navigation, existing pages, and explicit
outlines. Merging it no longer means the writing is complete.

**Access control must be configured separately before deploying content that
must stay private.** Neither `draft: true`, `robots.txt`, nor `noindex`
prevents access. The docs source repository is public and is outside a website
access gate.

Available approaches:

- A shared password checked at the server before any static file is served.
  The secret belongs in Cloudflare, never in HTML, JavaScript sent to the
  browser, or Git. Authentication must fail closed when unconfigured or when
  the Functions allowance is exhausted.
- Cloudflare Access with approved reviewer identities. If using the Pages
  preview-access switch, extend it to the production Pages hostname and custom
  domain; the switch alone does not protect both.
- Public but unindexed documentation, only if that exposure is an explicit
  product decision. This is not a private preview.

Gate all of `docs.braidkit.io`, `braid-docs-site.pages.dev`, and
`*.braid-docs-site.pages.dev`. Existing immutable preview deployments need
coverage too; a gate added only to a new deployment does not protect them.
Do not describe the site as private until anonymous checks below pass.

Official references:
[Pages preview access](https://developers.cloudflare.com/pages/configuration/preview-deployments/),
[custom-domain access caveats](https://developers.cloudflare.com/pages/platform/known-issues/),
and [Functions fail-open behavior](https://developers.cloudflare.com/pages/functions/routing/).

## Verify a deployment

For a preview deployment:

* open the preview URL from the pull request;
* confirm Home shows the configured task cards and grouped navigation;
* confirm every outline shows its status notice;
* confirm support is available once at the foot of the sidebar;
* confirm search, deep links, dark mode, and mobile navigation work;
* confirm the response includes `X-Robots-Tag: noindex`.

For an access-controlled deployment, anonymous requests must be challenged or
denied on every hostname, including these paths:

```sh
curl --head https://docs.braidkit.io/
curl --head https://docs.braidkit.io/why-braid/
curl --head https://docs.braidkit.io/search/search_index.json
curl --head https://docs.braidkit.io/llms.txt
curl --head https://docs.braidkit.io/llms-full.txt
curl --head https://docs.braidkit.io/sitemap.xml
curl --head https://docs.braidkit.io/stylesheets/home.css
curl --head https://docs.braidkit.io/404.html
```

Repeat against the production Pages hostname and an existing preview URL.
Test valid and invalid credentials, not just the home-page login prompt.
After signing in, verify the content checks above and compare the deployed
commit with the intended PR/main commit.

## Open the docs publicly

1. Complete the writing and release checks in [LAUNCH.md](LAUNCH.md).
2. Remove `draft: true` only from reviewed pages; hide unfinished pages if they
   are deferred from launch.
3. Verify the deployed build, then remove the chosen access gate deliberately.
4. Resolve the indexing policy in
   [BRA-250](https://linear.app/braidkit/issue/BRA-250). If indexing is approved,
   update `docs/robots.txt` and `docs/_headers` together.
5. Verify public HTML, search, sitemap, and both agent-readable files, plus the
   marketing redirect at `https://braidkit.io/docs`.

## Roll back

1. Open the Pages project's Deployments list.
2. Find the most recent known-good production deployment.
3. Use its actions menu and choose **Rollback to this deployment**.
4. Repeat the production verification above.
5. Revert or fix the source change in Git so the next `main` deployment does
   not reintroduce the failure.

Preview deployments are not rollback targets.

## Recover DNS or project configuration

If the custom domain stops resolving:

1. Confirm `docs.braidkit.io` remains attached under the Pages project's Custom
   domains.
2. Confirm the proxied DNS record points to the project's `pages.dev` hostname.
3. Restore the custom-domain association through Pages before editing DNS by
   hand.
4. Confirm TLS becomes active, then repeat the production verification.

If a build starts failing, compare the Pages settings to the deployment
inventory, inspect the failed build log, and reproduce with
`python -m mkdocs build --strict` locally before changing production settings.
