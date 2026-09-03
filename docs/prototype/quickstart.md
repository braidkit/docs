---
title: Quickstart
description: Follow a small Braid workflow from setup to review.
---

# Quickstart

This preview walks through the shape of a Braid workflow. Commands and endpoints are illustrative while the public guide is under review.

!!! note "Preview content"
    This page exists to test the documentation structure and is not release guidance.

## Before you begin

You need Braid installed, a Git repository with a remote, and access to the preview authentication service.

## Sign in

Authenticate the CLI and confirm the current identity.

```sh
braid auth login
braid auth status
```

## Initialize a repository

Run `init` once in a checkout. Braid records repository configuration without starting work or changing your code.

```sh
braid init
```

## Capture a change

Claim an issue, capture the agent session, and attach it to the braid.

```sh
braid claim 42
braid wrap codex "tighten the API validation"
braid attach <session-id> --braid <braid-id>
```

## Verify and review

Verification records a system-derived result. Review is the explicit human boundary before promotion.

```sh
braid verify <braid-id>
braid review <braid-id>
```

## Next steps

Learn how [braids and threads](concepts/work-model/core-objects/concepts.md) organize work, or see the [CLI reference](command-reference/command-groups/workflow/cli.md).
