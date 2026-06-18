# Payload Kinds

Every [`WorkEvent`](../protocol/work-event.md) carries exactly one payload kind.
This page catalogs the current kinds. The
[`work.proto`](https://github.com/braidkit/Prototype/blob/main/api/proto/braid/work/v1/work.proto)
remains the source of truth for field-level shape.

## Catalog

| Kind | Meaning |
| --- | --- |
| `ToolUse` | A tool request and result. |
| `Reasoning` | A contributor's own deliberation. |
| `Prompt` | A directive into an agent. |
| `IntentDeclaration` | A stated, refined, or abandoned intent. |
| `AttemptBoundary` | Start or outcome of one attempted approach. |
| `Commit` | A git commit was made. |
| `Review` | A judgment on an event, thread, contributor, braid, or commit. |
| `Decision` | The terminal verdict for a thread. |
| `AgentStart` | Agent session configuration. |
| `AgentEnd` | Agent session termination and accounting. |
| `ContextSnapshot` | Files that shaped the work. |
| `ScopeViolation` | Out-of-scope access or attempted access. |

## By purpose

### Intent &amp; reasoning

- **`Prompt`** — the directive given to an agent. Recording it lets reviewers see
  exactly what the agent was asked to do.
- **`Reasoning`** — a contributor's own deliberation, distinct from a directive
  it received.
- **`IntentDeclaration`** — a stated, refined, or abandoned intent. It can
  explicitly delegate to a sub-agent contributor.

### Action

- **`ToolUse`** — a tool request and its result. Captures tool inputs, outputs,
  status, and redaction flags.
- **`AttemptBoundary`** — the start or outcome of one attempted approach. Like
  intent, it can delegate to a sub-agent contributor.
- **`Commit`** — records that a git commit was made, linking the event stream to
  git state.

### Session lifecycle

- **`AgentStart`** — agent session configuration; captures the model and the
  instruction files loaded and considered.
- **`AgentEnd`** — session termination and accounting; captures the reason,
  tokens, and cost.
- **`ContextSnapshot`** — the files that shaped the work, as a set of file
  observations.

### Judgment

- **`Review`** — a judgment naming one or more subjects (`THREAD`,
  `CONTRIBUTOR`, `COMMIT`, or `BRAID`). See [Reviews](../concepts/reviews.md).
- **`Decision`** — the thread's terminal verdict. Carries `verdict`,
  `commit_sha`, `reason`, `evidence_event_ids`, and acknowledged
  `sub_agent_outcomes`. See [Decisions](../concepts/decisions.md).

### Safety

- **`ScopeViolation`** — records out-of-scope access, or an attempt at it, inside
  a thread that declared a scope.

## Notable fields

A few payloads carry fields worth calling out:

| Payload | Field | Note |
| --- | --- | --- |
| `Decision` | `verdict` | Pass, fail, needs human attention, or aborted. |
| `Decision` | `sub_agent_outcomes` | Rolls up what happened to delegated work. |
| `Decision` | `files_touched` | **Deprecated** — touched files come from git. |
| `Review` | subjects | One review can vouch for many subjects at once. |
| `AgentStart` | instruction files | Both *loaded* and *considered* files. |
| `ContextSnapshot` | file observations | The files that shaped the work. |

## Related

- [Events](../concepts/events.md) — the conceptual overview.
- [WorkEvent Reference](../protocol/work-event.md) — the shared envelope.
- [Entity Relations](../protocol/entity-relations.md) — how kinds relate to the
  rest of the model.
