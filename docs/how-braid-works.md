# How Braid works

Braid exists to preserve the intent and cognitive model of code. It does so by keeping a record of the activities taking place as the work is done via an AI Agent. Braid will record signed events describing the actions taken, decisions made, observations recorded, and checks performed. Braid further derives the work's state from the events so that humans and agents have a shared, verifiable understanding of the intent and cognitive model of the code that was produced. This enables reviewers, other contributors, and future you to further engage with the work and take ownership of the code.

This page describes the model. [Braid and thread lifecycle](lifecycle.md)
describes the states that model produces.

## Braids, threads, and contributors

A braid holds the work for one issue. A thread holds the work of one contributor
inside that braid. A contributor is a person or an agent.

Each thread has a scope, which is the set of files that thread holds. Scopes must
be disjoint. Two threads in the same braid cannot hold the same file. Braid
checks this when a thread is added.

## The event log is the source of truth

Braid derives braid state, thread state, violations, and anomalies from the event
log. It keeps no second copy of that state to edit. The same events in the same
order produce the same result on every replay. The record is permanent, and
nothing in it is removed.

## Signed events

Each event is signed. Its envelope carries a signing payload, signature, public key, event ID, and the braid and thread it addresses. When Braid receives an event, it verifies that the public key matches the claimed contributor ID and that the signature covers the event before storing it. It also checks the event's kind against the contributor it is attributed to, because some kinds are accepted only from a human contributor.

Only some event kinds move state. They are `braid_started`, `thread_dispatched`,
`thread_attached`, `agent_start`, `decision`, `thread_dropped`,
`goal_reconfirmed`, `review_boundary_reached`, `promote`, `dismiss`,
`abort_requested`, `scope_violation`, and `scope_violation_resolved`.

The events captured while an agent works, such as prompts, reasoning, and tool
calls, are not in that list. They are evidence. They stay in the record and they
never move braid or thread state.

## How Braid derives state

Braid derives the current state of a braid and its threads by replaying the
events in its record. Given the same record, it always derives the same state.

### Admitting events

Before Braid adds an event to the record, it checks the event's envelope,
authentication, and integrity. It rejects an event for:

- a bad signature
- an identity mismatch
- a malformed envelope
- missing braid or thread addressing
- a duplicate event id
- an action the contributor has no authority to record

A rejected event is never recorded and never contributes to derived state.
Because it was never recorded, a later valid event carrying the same event id
can still be admitted.

Envelope validation runs first and reports its own separate failures.

### Interpreting the record

Once Braid admits an event, it is a true fact about what happened. While deriving
state, Braid does not reject it. It can:

- advance the derived state
- change nothing, when the braid has already reached a terminal state
- replay events in their logical sequence, so events that arrive out of order
  still produce the same state
- record an anomaly, when a well formed event does not fit the current state

An anomaly leaves the event in the log and leaves the derived state unchanged.
The derived view never overrules the log it comes from.

## The two gates

### Gate 1, scope disjointness

Gate 1 applies when a thread is added. The new thread's scope must be disjoint
from the scope of every thread that already holds one. On an overlap Braid
records a scope violation and the thread is not added. A scope that cannot be
validated, such as one naming an absolute path or a path outside the repository,
fails the same gate.

A `scope_violation_resolved` event is the only thing that clears a violation.
Braid accepts that event from a human contributor only, so an agent cannot
dismiss the gate that constrains it.

An unresolved violation blocks the braid from surfacing for review and from being
promoted.

### Gate 2, goal reconfirmation

Gate 2 applies when a thread is dropped. Dropping a thread shrinks the braid's
scope, so Braid marks the braid as pending goal reconfirmation. While that mark
is set the braid cannot surface for review. A `goal_reconfirmed` event clears it.
