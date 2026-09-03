---
title: Overview
description: A short introduction to Braid and the documentation.
---

# Overview

Braid captures the work behind a software change so the next person can understand what was intended, how the work was done, and what was verified.

## What Braid records

A braid connects a goal to the people and agents working on it. As work happens, Braid preserves decisions, attempts, verification results, and the evidence needed for review.

### Work as evidence

The record is produced by the work itself. Reviewers can follow claims back to the events that support them instead of reconstructing the story from a diff.

### Intent that survives handoff

The goal and rationale remain available when a change is reviewed, inherited, or revisited during an incident.

## A typical workflow

1. Initialize Braid in a Git repository.
2. Claim an issue and dispatch scoped threads.
3. Capture an agent session and attach it to the braid.
4. Verify the result and prepare it for review.
5. Record the human verdict and promote the change.

## Where to go next

Use the [quickstart](quickstart.md) for a guided path, or read about [braids and threads](concepts/work-model/core-objects/concepts.md) before running commands.
