---
title: Braid
description: What Braid is, how to install it, how to review your first change, and where to get help.
---

# Braid

Braid keeps the intent behind code written with an AI agent, and the
understanding needed to work on it. As the work happens, Braid records what was
done, what was decided, what was noticed and what was checked. People and
agents then share the same picture of what the code is for and why it is the
way it is, so reviewers, teammates and future you can pick up the work and own
it.

Braid is in private preview and changes often. This page covers only what you
need to get going. For anything else, the CLI is the reference, because it
always matches the version you have installed:

```sh
braid --help
braid <command> --help
```

## Before you start

| | |
|---|---|
| **macOS** | Braid does not run on Linux or Windows yet. |
| **Git** | 2.25 or later. |
| **A local Git repository** | Braid works on a branch. It does not need a remote. |
| **A GitHub account** | You sign in to Braid with GitHub. Your repository does not have to be hosted there. |
| **Claude Code** | The agent Braid captures today. |

## Install and set up

```sh
curl -fsSL https://braidkit.io/cli/install.sh | sh
```

The installer puts `braid` and `braid-daemon` in `$HOME/.local/bin`, starts
the daemon, and offers to sign you in and set up capture. Choose Claude Code
when it asks which agents to capture. If you skip either step, run them
yourself later:

```sh
braid auth login
braid init
```

Then check that everything works:

```sh
braid doctor
```

## Review your first change

1. **Work on a branch with Claude Code** as you normally would. Braid captures
   the session in the background.
2. **Commit the work.** Braid reviews committed history.
3. **Rebuild the intent.**

    ```sh
    braid intent
    ```

    Braid gathers the captured work on this branch, rebuilds the intent and
    opens it in the Review UI. Read the intent alongside the diff.

4. **Record your verdict** with the braid ID that `braid intent` printed:

    ```sh
    braid review <braid-id> --verdict approved
    ```

    If you want the agent to change something first, use
    `--verdict requested-changes`. A `blocked` verdict is final.

To show the intent to the people reviewing your pull request, run
`braid push <braid-id>`. Pushing sends the intent to the Braid server, and the
intent can quote your prompts. To finish an approved braid, run
`braid ship <braid-id>`. Shipping cannot be undone, so read
`braid ship --help` first.

## When something goes wrong

Run `braid doctor`. If capture seems to be missing, run `braid hooks doctor`.
Both name the failing check and what to do about it.

## Get help

Ask on [Discord](https://discord.gg/gzUevjYD9), or email
[hello@braidkit.io](mailto:hello@braidkit.io).

When you report a problem, tell us what you expected and what happened. Then
run this in the repository where it happened, and attach `braid-report.txt`:

```sh
{
  braid version
  sw_vers
  braid doctor --verbose
  braid hooks doctor --verbose
} > braid-report.txt 2>&1
```

!!! warning "The report contains sensitive information"
    It includes your account name in file paths and your signing key's
    fingerprint.
