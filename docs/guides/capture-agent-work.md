---
title: Capture agent work
description: Planned guide to enabling capture, organizing sessions into braids, checking coverage, and removing hooks.
draft: true
---

# Capture agent work

Use this guide to set up or change capture in a repository and choose which
sessions belong in a braid. For a first example, follow
[Quickstart](../getting-started/quickstart.md).

## Choose a supported agent

<!-- Use BRA-270's qualified versions and coverage. Claude is the first target;
     Codex and Cursor need their own qualification. Link Preview status. -->

## Enable capture for a repository

<!-- Explain provider configuration, per-repository consent, provider trust,
     and explicit setup or Skip. Link What Braid records before enabling.
     Distinguish binary installation from hook setup. BRA-59, BRA-269. -->

## Confirm capture is working

<!-- Explain detection, configuration, enablement, and observed health using
     read-only diagnostics. A healthy agent or checksum is not proof of full
     coverage. Distinguish unknown, degraded, and unsupported. BRA-229. -->

## Add sessions to a braid

<!-- Show discovery, selection, a new versus existing braid, inferred scope,
     and cancellation. Cover multiple sessions only where qualified. BRA-228.
     Explain unsigned local capture and the daemon-signed bound copy. BRA-242. -->

## Continue working after adding a session

<!-- Explain when new events become available, supported resume/idle boundaries,
     and when intent requires a stable boundary. No fake termination or readiness
     bypasses. BRA-233, BRA-234, BRA-270. Link Troubleshooting for failures. -->

## Disable capture or remove hooks

<!-- Cover selected-repository disablement, last-repository cleanup, preserved
     evidence, unrelated provider settings, and any in-flight boundary. BRA-269.
     Keep data deletion in Installation, separate from capture removal. -->

Continue with [Understand a change](understand-a-change.md).
