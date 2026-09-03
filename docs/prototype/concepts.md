---
title: Braids and threads
description: Understand the core objects and lifecycle behind Braid workflows.
---

# Braids and threads

A braid represents one goal. Threads represent the human or agent contributors working toward it.

## Braid

The braid connects the issue, its goal, the contributing threads, and the evidence produced while the work moves toward review.

## Thread

Each contributor works through a thread with an explicit file scope. Disjoint scopes make parallel work easier to understand and safer to combine.

### Thread states

A thread moves from opened to working, then reaches a verification result or a human-attention boundary. Terminal results remain in the record.

## Lifecycle

The high-level lifecycle moves from claimed work through dispatch, active work, review, and promotion.

```text
claimed → dispatched → active → surfaced → promoted
```

### Intentional and discovery paths

The intentional path starts from a claimed issue. The discovery path can attach work that began before a braid was assigned.

## Evidence and derived state

Events are permanent facts after admission. Braid derives the current view from that log rather than editing state by hand.

## Human boundaries

Automated checks can verify configured conditions. Review records the human judgment about whether the change should proceed.
