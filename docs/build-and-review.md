---
title: Build and review
description: Planned expanded BrewGo exercise covering parallel agents, evidence checks, follow-up work, and the PR lifecycle.
draft: true
---

# Build and review

This page will expand the [Quickstart](quickstart.md). It follows one feature
from the existing BrewGo application through implementation, intent review,
a follow-up change, and the pull request workflow.

## Prepare the existing application

Check main, preserve the synthetic SQLite history, record the starting
commit, verify the application, and create the feature branch before capture.

## Coordinate backend and frontend work

Use complete parent and subagent prompts, an agreed API definition, separate
file ownership, and integration checks. Extend BrewGo's existing Python app.

## Verify the feature

Check authorization directly at the API, metric definitions against synthetic
orders, filter boundaries, request races, sign-out, and storefront behavior.

## Read the intent against its evidence

Follow Steps, Decisions, Workstreams, and Diagrams. Distinguish a recorded check
from a statement that the agent made about a check.

## Add CSV export to the same braid

Give a third subagent a bounded follow-up. Reuse the access and filter rules,
verify exported values, commit, and reconstruct the same braid.

## Review, merge, and keep the record

Cover intent review before or after opening a PR, personal cloud uploads,
approval, merge commits, signed Git notes, and shipping. Keep team-sharing
claims out until access is enabled and verified.

## Resolve capture and review problems

Check missing subagents, unfinished turns, rewritten history, candidate commits,
and preserved worktrees before retrying reconstruction.
