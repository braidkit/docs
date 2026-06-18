# Deploying

This site is designed for Cloudflare Pages.

Use the Git integration and these settings:

```text
Build command: mkdocs build
Build output directory: site
Production branch: main
Environment variable: PYTHON_VERSION=3.12
```

Add the custom domain:

```text
docs.braidkit.io
```

The docs stylesheet imports brand tokens from `https://braidkit.io/brand/`.
Deploy the marketing site brand capsule before merging docs changes that depend
on new shared tokens. Logo and favicon files are local copies sourced from the
same capsule so local previews do not break while the marketing deployment is
catching up.

Cloudflare Pages creates preview deployments for pull requests and rebuilds the
production site whenever `main` changes.
