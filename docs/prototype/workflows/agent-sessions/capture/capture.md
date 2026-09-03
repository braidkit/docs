---
title: Capture agent work
description: Capture a coding-agent session as evidence attached to a Braid workflow.
---

# Capture agent work

Braid can wrap a supported coding agent and preserve its session as structured work evidence.

## Start a captured session

Use `braid wrap` in the repository where the work will happen.

```sh
braid wrap codex "add validation to the import path"
```

The adapter starts the agent with the appropriate provider arguments and records the resulting events in the local inbox.

## Inspect captured sessions

List captures with `status`, then inspect one session with `show`.

```sh
braid status
braid show <session-id>
```

### Machine-readable output

Use `--json` when another tool needs the full event envelope.

```sh
braid show <session-id> --json
```

## Attach the session

Attaching connects the capture to an existing braid as a thread.

```sh
braid attach <session-id> --braid <braid-id>
```

## What remains local

Captured sessions remain in the repository inbox until they are attached or deliberately cleaned up. Braid does not silently purge them.
