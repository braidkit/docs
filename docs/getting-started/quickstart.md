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
| **A GitHub repository** | Braid works on a project tracked in a repository hosted on GitHub. |
| **A GitHub account** | Signing in to Braid goes through GitHub. |
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

When the install finishes, it asks:

```text
Sign in to Braid now? [y/N]
```

Answer `y`. Braid prints a URL and a one-time code. Open
<https://github.com/login/device>, enter the code, and complete GitHub
authentication.

To sign in later instead:

```sh
braid auth login
```

## Set up capture for this repository

Next, the installer asks:

```text
Initialize Braid for this machine? [y/N]
```

Answer `y`. Braid sets up your machine identity and opens the agent capture
screen:

```text
  AGENT          CAPTURE SETUP
────────────────────────────────────────────────────────────────────────────────

> [ ] Claude Code    Enabled
> [ ] Codex          Available
> [-] Cursor         Unavailable in this build
```

Move with the arrow keys or `j`/`k`, select with Space, and confirm with Enter.
Nothing is captured unless you select it here.

To initialize later instead:

```sh
braid init
```

## Check your setup

```sh
braid doctor
```

Every category should pass. `[-]` marks a check that did not apply, not a
problem. Each failure prints what is wrong and what to do about it.

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
