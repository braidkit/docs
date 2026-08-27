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
| Cloudflare Pages project | `braid-docs` |
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
5. Confirm the first deployment on the generated `braid-docs.pages.dev` URL.

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

## Verify a deployment

For a preview deployment:

* open the preview URL from the pull request;
* confirm the page contains `documentation is coming soon`;
* confirm an old documentation URL returns `404`;
* confirm the response includes `X-Robots-Tag: noindex`.

For production, verify:

```sh
curl --fail --location https://docs.braidkit.io/
curl --fail https://docs.braidkit.io/robots.txt
curl --fail https://docs.braidkit.io/sitemap.xml
curl --fail https://docs.braidkit.io/llms.txt
curl --fail https://docs.braidkit.io/llms-full.txt
curl --head https://braidkit.io/docs
```

While the site is a coming-soon page, production must return
`X-Robots-Tag: noindex` and `robots.txt` must disallow crawling. Change those
settings only when reviewed documentation is ready to be published.

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
