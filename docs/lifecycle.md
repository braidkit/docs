---
title: Braid and thread lifecycle
description: The braid and thread states, the events that move between them, and the rules for terminal states and automatic drops.
---

# Braid and thread lifecycle

A braid holds the work for one issue. A thread holds the work of one contributor
inside that braid. [How Braid works](how-braid-works.md) describes that model.
This page describes the states it produces.

Every state here is derived from the signed event log. No state is stored or
edited separately from that log.

Only the event kinds named on this page move state. The events captured while an
agent works, such as prompts, reasoning, and tool calls, are evidence and never
appear as transitions.

## Braid states

A braid is in one of six states: `claimed`, `dispatched`, `active`, `surfaced`,
`promoted`, or `dropped`.

| From | Event | To |
| --- | --- | --- |
| no braid yet | `braid_started` | `claimed` |
| no braid yet | `thread_attached` | `active` |
| `claimed` | `thread_dispatched` | `dispatched` |
| `claimed` | `thread_attached` | `active` |
| `dispatched` | `agent_start` | `active` |
| `dispatched` | `thread_attached` | `active` |
| `active` | `review_boundary_reached` | `surfaced` |
| `surfaced` | `promote` | `promoted` |
| `surfaced` | `dismiss` | `dropped` |
| `surfaced` | `thread_dispatched` or `thread_attached` | `active` |
| any non-terminal | `abort_requested` | `dropped` |

`claimed` and `dispatched` are optional. They belong to the intentional path,
where the braid is declared before the work starts. On the discovery path the
first `thread_attached` event creates the braid directly in `active`.

`promoted` and `dropped` are terminal. An admitted event on a terminal braid
stays in the log and changes nothing.

## When a braid can surface

A `review_boundary_reached` event moves a braid from `active` to `surfaced` only
when all of the following hold:

- the braid has at least one thread
- every thread is in a terminal state
- at least one thread is in `verify_passed`
- the braid is not pending goal reconfirmation
- the braid has no unresolved scope violations

If the braid is only waiting on goal reconfirmation, the braid stays `active` and
Braid records nothing, because a further boundary is expected once the goal is
reconfirmed. If any other condition fails, the braid stays `active` and Braid
records an anomaly naming the condition that was not met.

A `promote` event requires the braid to be `surfaced` with no unresolved scope
violations. Otherwise the braid stays where it is and Braid records an anomaly.

## Thread states

A thread is in one of six states: `opened`, `working`, `needs_human`,
`verify_passed`, `verify_failed`, or `thread_dropped`.

The table below is normative. A thread-mutating event that matches no row records
an anomaly and leaves the thread's state unchanged.

| From | Event | To |
| --- | --- | --- |
| `opened` | `agent_start` | `working` |
| `opened` | `thread_dropped` | `thread_dropped` |
| `working` | `decision` | `verify_passed`, `verify_failed`, or `needs_human` |
| `working` | `thread_dropped` | `thread_dropped` |
| `needs_human` | `agent_start` | `working` |
| `needs_human` | `decision` | `verify_passed` or `verify_failed` |
| `needs_human` | `thread_dropped` | `thread_dropped` |
| `verify_failed` | `agent_start` | `working` |

The `thread_dropped` event and the `thread_dropped` state share one name. The
event is what a contributor records. The state is what the thread derives from
it.

A `decision` event carries the verdict. From `working` it records a pass, a
failure, or a need for human attention. From `needs_human` it records a pass or a
failure.

## Terminal thread states

`verify_passed`, `verify_failed`, and `thread_dropped` are terminal at the thread
level only. A terminal thread does not make the braid terminal.

`verify_passed` and `thread_dropped` are immutable. Every thread-mutating event
on them records an anomaly and changes nothing. A `thread_dropped` event on a
thread that is already dropped does nothing at all.

`verify_failed` has the one sanctioned reopen. An `agent_start` event moves it
back to `working` so the work can be retried. A `thread_dropped` event on
`verify_passed` or `verify_failed` records an anomaly, because a drop does not
override a recorded verdict.

A failed thread stays in the braid as evidence. It never drops the braid on its
own.

## When a braid drops on its own

A braid moves to `dropped` on its own only when it is dead: every thread is
terminal and no thread passed. A `verify_failed` thread beside a thread that is
still working, or beside a thread that passed, never drops the braid.
