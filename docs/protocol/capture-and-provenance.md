# Capture & Provenance

Every [`WorkEvent`](work-event.md) records *how* it was captured and is signed so
the record is tamper-evident. Together these two fields — `capture_method` and
`signature` — let a reviewer judge how much to trust each event.

## Capture methods

The `capture_method` field says where an event came from. Not all events are
equally direct: some are emitted by a native integration as work happens, others
are reconstructed after the fact or typed in by a person. Recording the method
keeps that distinction visible instead of pretending every event is equally
authoritative.

| Capture method | Meaning |
| --- | --- |
| Native integration | The event came directly from an integrated tool or harness as the work happened. |
| Wrapper markers | The event was captured from markers emitted by a wrapper around the tool. |
| Extraction | The event was reconstructed by extracting it from logs or other artifacts after the fact. |
| Human entry | A person entered the event by hand. |

!!! tip "Why it matters"
    A `Decision` captured by native integration carries different weight than one
    reconstructed by extraction. Surfacing `capture_method` lets reviewers and
    gates treat events with the skepticism they deserve.

## Signatures

Each event carries a `signature`: an **Ed25519** signature over the canonical
event bytes. Because the signature covers the canonical serialization, any change
to the event after signing is detectable — the stream is tamper-evident, and each
event can be attributed to the key that produced it.

## Provenance through lineage

Provenance is not only per-event. The protocol carries lineage so that work can
be traced across sessions:

- A [contributor](../concepts/contributors.md) records who spawned it via
  `spawned_by_contributor_id`, modeling sub-agents.
- `IntentDeclaration` and `AttemptBoundary` can explicitly delegate to a
  sub-agent contributor.
- A thread's [`Decision`](../concepts/decisions.md) acknowledges sub-agent
  outcomes rather than each sub-agent emitting its own terminal thread decision.

When work is promoted, the orchestrator computes touched files from git commit
state and signs a **braid-level provenance note** — see
[Review and promote](../stories/review-and-promote.md).

## What is *not* trusted

Provenance deliberately excludes self-reported file lists. `Decision.files_touched`
is deprecated; the orchestrator derives touched files from git, not from what a
contributor claims. See [Decisions](../concepts/decisions.md).

## Related

- [WorkEvent Reference](work-event.md) — the envelope, including `capture_method`
  and `signature`.
- [Entity Relations](entity-relations.md) — the lineage edges between
  contributors, intents, attempts, and decisions.
