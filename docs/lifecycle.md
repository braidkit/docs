# Braid and thread lifecycle

A braid holds the work for one issue. A thread holds the work of one contributor
inside that braid. [How Braid works](how-braid-works.md) describes that model.
This page describes the states it produces.

Every state here is derived from the signed event log. The log is authoritative;
Braid derives state from it rather than editing state separately.

Only the event kinds named on this page move state. The events captured while an
agent works, such as prompts, reasoning, and tool calls, are evidence and never
appear as transitions.

## Braid states

A braid is in one of six states.

| State | Meaning |
| --- | --- |
| `claimed` | The braid exists for an issue. No thread has been added yet. |
| `dispatched` | Threads have been added with declared scopes. No agent has started on any of them. |
| `active` | Work has started, a thread has been attached from an existing session, or new work was added after review. The braid has not yet surfaced or reached a terminal state. |
| `surfaced` | Every thread has finished and the braid is ready to be reviewed. |
| `promoted` | The braid is finalized. Terminal. |
| `dropped` | The braid was abandoned, declined, or ended with no thread passing. Terminal. |

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
- every thread has reached a terminal state, meaning `verify_passed`,
  `verify_failed`, or `thread_dropped`
- at least one thread is in `verify_passed`
- the braid is not pending goal reconfirmation
- the braid has no unresolved scope violations

If the braid is only waiting on goal reconfirmation, the braid stays `active` and
Braid records no anomaly, because a further boundary is expected once the goal
is reconfirmed. If any other condition fails, the braid stays `active` and Braid
records an anomaly naming the condition that was not met.

A `promote` event requires the braid to be `surfaced` with no unresolved scope
violations. Otherwise the braid stays where it is and Braid records an anomaly.

## Thread states

A thread is in one of six states.

| State | Meaning |
| --- | --- |
| `opened` | The thread exists with its scope. No agent has started on it. |
| `working` | An agent has started and the thread has no verdict yet. |
| `needs_human` | A decision recorded that the thread needs human attention before it can finish. |
| `verify_passed` | A decision recorded a passing verdict. Final. |
| `verify_failed` | A decision recorded a failing verdict. The attempt ended and the thread can be reopened. |
| `thread_dropped` | The thread was abandoned. Final. |

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
event records that a thread was dropped. The state is what Braid derives from
that event.

A `decision` event carries the verdict. From `working` it records a pass, a
failure, or a need for human attention. From `needs_human` it records a pass or a
failure.

## Completed and reopenable thread states

`verify_passed` and `thread_dropped` are final. `verify_failed` ends the current
attempt but can be reopened by `agent_start`. None of these states makes the
braid terminal.

`verify_passed` and `thread_dropped` are immutable. Every thread-mutating event
on them records an anomaly and changes nothing. A `thread_dropped` event on a
thread that is already dropped does nothing at all.

An `agent_start` event is the one sanctioned reopen for `verify_failed`. A
`thread_dropped` event on `verify_passed` or `verify_failed` records an anomaly,
because a drop does not override a recorded verdict.

A failed thread stays in the braid as evidence. It does not by itself drop the
braid; the braid drops only when every thread is terminal and none has passed.

## When a braid drops on its own

A braid moves to `dropped` on its own only when it is dead: every thread is
terminal and no thread passed. A `verify_failed` thread beside a thread that is
still working, or beside a thread that passed, never drops the braid.
