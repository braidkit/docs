# Entity Relations

This chart shows the core protocol entities and their relationships.

```mermaid
erDiagram
  BRAID ||--o{ THREAD : contains
  THREAD ||--o{ CONTRIBUTOR : has
  CONTRIBUTOR ||--o{ CONTRIBUTOR : spawns
  THREAD ||--o{ WORK_EVENT : records
  CONTRIBUTOR ||--o{ WORK_EVENT : emits

  WORK_EVENT ||--o| TOOL_USE : kind
  WORK_EVENT ||--o| REASONING : kind
  WORK_EVENT ||--o| PROMPT : kind
  WORK_EVENT ||--o| INTENT_DECLARATION : kind
  WORK_EVENT ||--o| ATTEMPT_BOUNDARY : kind
  WORK_EVENT ||--o| COMMIT : kind
  WORK_EVENT ||--o| REVIEW : kind
  WORK_EVENT ||--o| DECISION : kind
  WORK_EVENT ||--o| AGENT_START : kind
  WORK_EVENT ||--o| AGENT_END : kind
  WORK_EVENT ||--o| CONTEXT_SNAPSHOT : kind
  WORK_EVENT ||--o| SCOPE_VIOLATION : kind

  AGENT_START ||--o{ INSTRUCTION_FILE : loaded
  AGENT_START ||--o{ INSTRUCTION_FILE : considered
  CONTEXT_SNAPSHOT ||--o{ FILE_OBSERVATION : includes
  REVIEW ||--o{ REVIEW_SUBJECT : reviews
  DECISION ||--o{ SUB_AGENT_OUTCOME : acknowledges

  INTENT_DECLARATION }o--o| CONTRIBUTOR : delegates_to
  ATTEMPT_BOUNDARY }o--o| CONTRIBUTOR : delegates_to
  DECISION }o--o| COMMIT : points_to

  BRAID {
    string braid_id
  }

  THREAD {
    string thread_id
    string braid_id
  }

  CONTRIBUTOR {
    string contributor_id
    enum kind
    string handle
    string version
    string job
    string spawned_by_contributor_id
  }

  WORK_EVENT {
    string event_id
    string braid_id
    string thread_id
    Contributor contributor
    timestamp ts
    bytes signature
    enum capture_method
    oneof kind
  }

  DECISION {
    enum verdict
    string commit_sha
    repeated sub_agent_outcomes
    string reason
    repeated evidence_event_ids
    repeated files_touched_deprecated
  }

  REVIEW_SUBJECT {
    enum kind
    string id
  }

  SUB_AGENT_OUTCOME {
    string contributor_id
    string final_reason
    bool work_kept
    string notes
  }
```

Important edges:

- A thread can have multiple contributors.
- A contributor can spawn another contributor, which models sub-agents.
- Intent and attempts can explicitly delegate to a sub-agent contributor.
- A top-level decision acknowledges sub-agent outcomes instead of each
  sub-agent emitting its own terminal thread decision.
- `Decision.files_touched` is deprecated. The orchestrator computes touched
  files from git commit state.

