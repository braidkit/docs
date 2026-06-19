# Glossary

Quick definitions for the terms used across these docs. Each links to fuller
treatment where it exists.

#### AgentStart / AgentEnd

The lifecycle events for an agent session. `AgentStart` captures the model and
instruction files; `AgentEnd` captures the termination reason, tokens, and cost.
See [Payload Kinds](payload-kinds.md).

#### AttemptBoundary

A `WorkEvent` kind marking the start or outcome of one attempted approach. Can
delegate an attempt to a sub-agent contributor.

#### Braid

One coordinated unit of work, such as a GitHub issue. Contains one or more
threads. See [Braids](../concepts/braids.md).

#### Capture method

How an event was captured: native integration, wrapper markers, extraction, or
human entry. See [Capture & Provenance](../protocol/capture-and-provenance.md).

#### Commit

A `WorkEvent` kind recording that a git commit was made, linking the event
stream to git state.

#### ContextSnapshot

A `WorkEvent` kind recording the files that shaped the work, as a set of file
observations.

#### Contributor

One human or agent *session* acting inside a thread. Session-shaped: two sessions
are two contributors. A parent can spawn a sub-agent via
`spawned_by_contributor_id`. See [Contributors](../concepts/contributors.md).

#### Decision

A thread's terminal verdict — pass, fail, needs human attention, or aborted —
with a reason and evidence. See [Decisions](../concepts/decisions.md).

#### Ed25519

The signature scheme used to sign each event over its canonical bytes, making
the stream tamper-evident. See [Capture & Provenance](../protocol/capture-and-provenance.md).

#### Event

One recorded action by one contributor — a signed `WorkEvent` with exactly one
payload kind. See [Events](../concepts/events.md).

#### IntentDeclaration

A `WorkEvent` kind for a stated, refined, or abandoned intent. Can delegate to a
sub-agent contributor.

#### Orchestrator

The component that registers braids/threads/contributors, assembles thread
artifacts, runs the promote gate, computes touched files from git, and signs
braid-level provenance.

#### Promote gate

The check the orchestrator runs before merging: it verifies decisions, review,
and disjoint thread scopes. See [Review and promote](../stories/review-and-promote.md).

#### Prompt

A `WorkEvent` kind recording a directive given to an agent.

#### Reasoning

A `WorkEvent` kind recording a contributor's own deliberation.

#### Review

A judgment on one or more subjects (`EVENT`, `THREAD`, `CONTRIBUTOR`, `COMMIT`,
`BRAID`). Review is itself work. See [Reviews](../concepts/reviews.md).

#### Scope

The declared boundary of a thread's work. Out-of-scope access is recorded as a
`ScopeViolation`. The gate requires thread scopes to be disjoint before
promotion.

#### ScopeViolation

A `WorkEvent` kind recording out-of-scope access or an attempt at it.

#### Sub-agent

A contributor spawned by another contributor. Traced through contributor lineage
and explicit delegation fields. See
[Sub-agent delegation](../stories/sub-agent-delegation.md).

#### Thread

One lane of work inside a braid, usually with a declared scope and one or more
contributors. See [Threads](../concepts/threads.md).

#### ToolUse

A `WorkEvent` kind capturing a tool request and result, including inputs,
outputs, status, and redaction flags.

#### WorkEvent

The canonical event emitted by Braid SDK clients. Every `WorkEvent` carries the
shared envelope plus exactly one payload kind. See
[WorkEvent Reference](../protocol/work-event.md).
