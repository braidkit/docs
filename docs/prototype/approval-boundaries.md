---
title: Approval boundaries
description: Understand where automated evidence ends and human judgment begins.
---

# Approval boundaries

Braid keeps automated checks and human approval separate. That boundary makes it clear what the system verified and what a reviewer decided.

## Verification is evidence

A successful check means the configured command passed for the recorded work. It does not establish that the goal was correct or the change should ship.

!!! note "System-derived result"
    Verification records the outcome of a configured check. Braid presents that evidence without expanding what the check proves.

## Review is judgment

Reviewers evaluate the goal, implementation, tradeoffs, and available evidence before recording a verdict.

!!! warning "Approval remains explicit"
    A passed verification result never creates an approval automatically. Promotion still requires the review boundary to be satisfied.

## Blocked work

A reviewer can block work when the available evidence is incomplete or the change should not proceed.

!!! danger "Do not bypass the boundary"
    Treat missing review evidence as unresolved work, not as permission to promote a change through another path.

## A calm failure path

Requested changes and failed checks stay attached to the braid. The next contributor can understand the failure without losing the earlier work.

!!! tip "Preserve the useful failure"
    Record what failed and why. A clear rejected approach is valuable evidence for the next attempt.
