# FAQ

Common questions about the Braid model. For field-level detail, the
[`work.proto`](https://github.com/braidkit/Prototype/blob/main/api/proto/braid/work/v1/work.proto)
is the source of truth.

## How is Braid different from git?

Git records *what changed*. Braid records *who did it, what they considered, and
what was vouched for* — the surrounding accountability that git does not capture.
The two are complementary: Braid links its event stream to git via `Commit`
events and derives touched files from git commit state.

## Does Braid replace my code review tool?

No. Braid models review as first-class, signed [`Review`](../concepts/reviews.md)
events that can vouch for one event, thread, contributor, commit, or whole braid.
Event-level review is the precise audit case; promotion will usually care about
thread, commit, or braid-level review. How that surfaces in a review UI is a
product concern layered on top of the protocol.

## What is the difference between a braid and a thread?

A [braid](../concepts/braids.md) is one coordinated unit of work (e.g. an issue).
A [thread](../concepts/threads.md) is one lane inside it, usually scoped to a
path or pull request. A braid can contain several threads worked in parallel.

## Why is a contributor a "session" and not a person?

Because accountability follows the acting session, not just an identity. Two
Codex sessions in the same thread are two [contributors](../concepts/contributors.md).
This is also how sub-agents are modeled — a parent sets
`spawned_by_contributor_id` on the child.

## How are sub-agents tracked?

Through contributor lineage and explicit delegation. `IntentDeclaration` and
`AttemptBoundary` can delegate to a sub-agent, and the parent thread's
[`Decision`](../concepts/decisions.md) acknowledges sub-agent outcomes instead of
each sub-agent emitting its own terminal thread decision. See
[Sub-agent delegation](../stories/sub-agent-delegation.md).

## Can the system trust which files a contributor says it touched?

No. `Decision.files_touched` is deprecated. The orchestrator computes touched
files from git commit state rather than trusting a self-reported list. See
[Decisions](../concepts/decisions.md).

## How do I know an event is genuine?

Each event is signed with **Ed25519** over its canonical-JSON encoding, so
tampering is detectable and each event is attributable to a key. Events also
record a `capture_method` so you can tell a natively captured event from a
reconstructed or hand-entered one. See
[Capture & Provenance](../protocol/capture-and-provenance.md).

## What gets checked before work is promoted?

The orchestrator's promote gate checks that the thread has a
[decision](../concepts/decisions.md), that a [review](../concepts/reviews.md)
vouches for it, and that thread scopes are disjoint — then it merges and signs a
braid-level provenance note. See
[Review and promote](../stories/review-and-promote.md).

## Where is the canonical definition of an event?

In the proto:
[`Prototype/api/proto/braid/work/v1/work.proto`](https://github.com/braidkit/Prototype/blob/main/api/proto/braid/work/v1/work.proto).
These docs explain the model; they do not invent protocol facts. See
[Keeping Docs Current](../keeping-docs-current.md).
