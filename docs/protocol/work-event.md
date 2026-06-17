# WorkEvent Reference

`WorkEvent` is the canonical event emitted by Braid SDK clients.

Every event has:

- `event_id`: idempotency key and event identity.
- `braid_id`: the coordinated unit of work.
- `thread_id`: the lane inside the braid.
- `contributor`: the human or agent session that acted.
- `ts`: event time.
- `signature`: Ed25519 signature over the canonical event bytes.
- `capture_method`: whether the event came from native integration, wrapper
  markers, extraction, or human entry.
- exactly one payload kind.

Current payload kinds:

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

Canonical proto:
[`work.proto`](https://github.com/braidkit/Prototype/blob/main/api/proto/braid/work/v1/work.proto).

