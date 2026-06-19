# Review and Promote

Review is itself work. A reviewer emits a `Review` event that says what was
examined and what verdict they reached.

```mermaid
sequenceDiagram
  actor Bob
  participant CLI as braid CLI
  participant O as Orchestrator
  participant Git

  Bob->>CLI: review braid
  CLI->>O: fetch thread artifacts
  Bob->>CLI: approves selected subjects
  CLI->>O: WorkEvent(kind=Review)
  O->>O: gate checks decisions, review, and disjoint scopes
  O->>Git: promote/merge
  O->>O: sign braid-level provenance note
```

Example review subjects:

| Subject kind | Example |
| --- | --- |
| `EVENT` | Bob reviews one specific `WorkEvent`, such as a risky tool use. |
| `THREAD` | Bob approves one thread's final artifact. |
| `CONTRIBUTOR` | Bob reviews all work by a specific agent session. |
| `COMMIT` | Bob approves a git commit. |
| `BRAID` | Bob approves the coordinated work as a whole. |
