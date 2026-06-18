# Events

An event is one recorded action by one contributor inside a thread. Events are
the atoms of Braid: a braid is, at bottom, an ordered stream of signed events.

Each event is a [`WorkEvent`](../protocol/work-event.md) carrying exactly one
payload kind. The envelope names:

- the **contributor** that acted,
- the **thread** (and braid) it belongs to,
- when it happened (`ts`),
- how it was captured (`capture_method`),
- and a **signature** over the canonical event bytes.

## One event, one kind

Every event carries exactly one payload kind, chosen from a fixed set. This
keeps the stream easy to reason about: a reader never has to ask "is this a tool
call *and* a decision?" — it is always exactly one thing.

The full catalog lives in the [Payload Kinds reference](../reference/payload-kinds.md).
At a glance, kinds fall into a few groups:

| Group | Kinds |
| --- | --- |
| Intent &amp; reasoning | `Prompt`, `Reasoning`, `IntentDeclaration` |
| Action | `ToolUse`, `Commit`, `AttemptBoundary` |
| Session lifecycle | `AgentStart`, `AgentEnd`, `ContextSnapshot` |
| Judgment | `Review`, `Decision` |
| Safety | `ScopeViolation` |

## Why each event matters

The point of recording events is not bookkeeping — it is to let a future
reviewer reconstruct *what a moment of work meant*. A `Prompt` shows the
directive an agent received. An `IntentDeclaration` shows how the agent
understood it. A `ContextSnapshot` records which files shaped the work. A
`Decision` gives the thread a verdict to gate on.

The [Event Stories](../protocol/event-stories.md) and
[Walkthroughs](../stories/human-thread.md) show concrete sequences and explain
why each event helps the reader.

## What events do not carry

Events record intent, reasoning, actions, and verdicts. They do **not** carry an
authoritative list of changed files. Touched files are computed by the
orchestrator from git commit state — never trusted from a payload such as
`Decision.files_touched` (which is deprecated for this reason). See
[Decisions](decisions.md).

## Related

- [WorkEvent Reference](../protocol/work-event.md) — the envelope and its fields.
- [Capture & Provenance](../protocol/capture-and-provenance.md) — how events are
  captured and signed.
- [Payload Kinds](../reference/payload-kinds.md) — every kind and its meaning.
