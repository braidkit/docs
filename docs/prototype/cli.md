---
title: CLI commands
description: A compact reference to the Braid command-line interface.
---

# CLI commands

Use this page to find the command that matches the stage of work you are in.

## Setup and identity

| Command | Purpose |
| --- | --- |
| `braid auth` | Sign in and manage the current identity |
| `braid init` | Initialize Braid in the current repository |
| `braid home` | Show the resolved Braid home directory |
| `braid version` | Show client and server build information |

## Capture and organize work

| Command | Purpose |
| --- | --- |
| `braid claim` | Claim an issue as a braid |
| `braid dispatch` | Add scoped contributor threads |
| `braid wrap` | Run and capture a coding-agent session |
| `braid attach` | Attach a captured session to a braid |
| `braid status` | Show inbox captures or current braid state |
| `braid show` | Display captured events for a session |

## Review and finish

| Command | Purpose |
| --- | --- |
| `braid verify` | Run the configured check and record its result |
| `braid review` | Prepare a review or record a human verdict |
| `braid promote` | Merge, sign, and finalize a surfaced braid |
| `braid replay` | Replay signed provenance from the event log |

## Global options

Use `--verbose` for a complete error cause chain and debug logging. Use `--no-banner` for script-friendly output.

## Command help

Every command provides built-in help.

```sh
braid <command> --help
```
