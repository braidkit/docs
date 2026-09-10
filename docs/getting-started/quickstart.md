---
title: Quickstart
description: Planned walkthrough from installation and hosted sign-in to capturing, understanding, reviewing, and completing your first change.
draft: true
---

# Quickstart

One small change, from setup to a completed braid. This walkthrough will use
one supported agent and show what to expect at each step.

## Before you start

<!-- State the exact Braid build, macOS and Claude versions from BRA-270.
     Choose a disposable example repository and a reproducible small change.
     Show an estimated duration only after timing the actual walkthrough.
     Related: BRA-242, BRA-252. -->

## Install Braid

<!-- Include the verified primary install path and a success check.
     Link to Installation for alternatives, upgrades, and removal.
     Do not require access to the private source repository. -->

## Sign in through your browser

<!-- Show the supported CLI-to-hosted GitHub sign-in flow and how to confirm
     the CLI registered this device. A browser session alone is not proof.
     Verify the launch origin; Slack's api-dev deployment is not production
     approval. Link Account and devices for sign-out and device management.
     Confirm auth/init/daemon ordering against the selected build. BRA-243. -->

## Set up capture for this repository

<!-- Show init, explicit Claude selection, privacy notice, provider trust if
     needed, and the configured-versus-active check. Link What Braid records
     before consent. Installation alone does not enable hooks. Explain the
     minimum daemon startup needed for later steps. BRA-59, BRA-269, BRA-270. -->

## Capture a small change

<!-- Run Claude normally on the chosen example; confirm evidence appeared.
     Do not use hidden wrap/dispatch or unsupported Codex/Cursor fallbacks. -->

## Bring the work into a braid

<!-- Demonstrate the qualified discovery/add flow, session choice, scope, and
     expected status. Keep one happy path; link Guides for composition choices.
     Distinguish the unsigned inbox from the daemon-signed attached copy. -->

## Read the explanation and evidence

<!-- Show the qualified intent boundary, transmission consent, and local braid
     view. Point out the goal, one decision, and its supporting evidence.
     Do not imply opening a saved record necessarily regenerates intent. -->

## Check and review the change

<!-- Run the example's real tests, explain any required verification record,
     inspect the exact candidate and record a verdict. Resolve BRA-245 before
     claiming what verify guarantees. Separate checks from human approval. -->

## Complete the braid

<!-- Finish the same example; do not stop the quickstart at an external link.
     Explain the actual Git effects for this discovery path: it may finalize
     at existing HEAD without creating a merge. Confirm the resulting state
     and where the record can be read. Use qualified names, not BRA-253 proposals. -->

## What next?

- [Capture agent work](../guides/capture-agent-work.md) to manage capture beyond this example.
- [Understand a change](../guides/understand-a-change.md) to inspect a braid in more detail.
- [Troubleshooting](../troubleshooting.md) if a step does not behave as expected.
