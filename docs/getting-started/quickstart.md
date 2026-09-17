---
title: Quickstart
description: Install Braid, sign in, set up capture, and take one small change through to a completed braid.
---

# Quickstart

One small change, from install to a completed braid. This walkthrough uses one
supported agent and shows what to expect at each step.

## Before you start

You need all of these:

| | |
|---|---|
| **macOS** | Braid does not run on Linux or Windows yet. |
| **Git** | 2.25 or later. |
| **A Git repository** | Braid works on a branch in your local repository. It does not need a remote. |
| **Committed work** | Braid ships from committed history. `braid ship` refuses a dirty working tree. |
| **A GitHub account** | Braid signs you in through GitHub. Your repository does not have to be hosted there. |
| **Claude Code** | The agent Braid captures today. |

Braid also lists Codex on its capture screen, but Codex is not supported yet.
Cursor is unavailable in this build.

See [Installation](../reference/installation.md) for the architectures, shells,
and command-line tools the installer needs.

## Install Braid

```sh
curl -fsSL https://braidkit.io/cli/install.sh | sh
```

This installs `braid` and `braid-daemon` into `$HOME/.local/bin`, adds that
directory to your `PATH`, sets up shell completion, and starts the daemon as a
per-user service that runs at login.

## Sign in

The installer offers to sign you in, through GitHub. To do it later instead:

```sh
braid auth login
```

## Set up capture for this repository

The installer then offers to initialize this machine and choose which agents
Braid captures. Select Claude Code. To do it later instead:

```sh
braid init
```

## Check your setup

```sh
braid doctor
```

Every category should pass.

## Capture a small change

*Not yet written.*

## Bring the work into a braid

*Not yet written.*

## Read the explanation and evidence

*Not yet written.*

## Check and review the change

*Not yet written.*

## Complete the braid

*Not yet written.*

## What next?

- [Capture agent work](../guides/capture-agent-work.md) to manage capture beyond this example.
- [Understand a change](../guides/understand-a-change.md) to inspect a braid in more detail.
- [Troubleshooting](../troubleshooting.md) if a step does not behave as expected.
