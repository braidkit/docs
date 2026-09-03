---
title: Inspect a session
description: Read a captured agent session before attaching it to a braid.
---

# Inspect a session

Captured sessions stay in the local inbox so you can inspect what Braid recorded before connecting the work to a braid.

## Find the session

List the inbox from the repository where the work was captured.

```sh
braid status
```

Each row identifies the session, agent harness, capture time, and attachment state.

## Read the event stream

Render a session as a chronological account of the work.

```sh
braid show <session-id>
```

### Prompts and decisions

Prompts establish what the agent was asked to do. Decision events preserve choices and the reason an approach won.

### Attempts and verification

Attempt boundaries make abandoned approaches visible. Verification events distinguish what was checked from what was merely claimed.

## Inspect the signed envelope

Use JSON output when you need event identifiers, signatures, or machine-readable payloads.

```sh
braid show <session-id> --json
```

!!! note "Preview content"
    Field names and rendered output on this page are illustrative while the public reference is being prepared.

## Attach after inspection

When the capture belongs to an existing braid, attach it as a thread.

```sh
braid attach <session-id> --braid <braid-id>
```
