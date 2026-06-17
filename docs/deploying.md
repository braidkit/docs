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

Cloudflare Pages creates preview deployments for pull requests and rebuilds the
production site whenever `main` changes.
