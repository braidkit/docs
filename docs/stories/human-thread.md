# Human Thread

Alice works directly in her editor, commits the change, and records the thread
outcome.

```mermaid
sequenceDiagram
  actor Alice
  participant CLI as braid CLI
  participant SDK as Braid SDK
  participant O as Orchestrator
  participant Git

  Alice->>CLI: claim issue and dispatch thread
  CLI->>O: register braid/thread/contributor
  Alice->>Git: edit files and commit
  CLI->>SDK: observe commit
  SDK->>O: WorkEvent(kind=Commit)
  SDK->>O: WorkEvent(kind=Decision)
  O->>Git: compute touched files from commit
  O->>O: assemble thread artifact
```

Example event sequence:

| User action | Event sent | Why it matters |
| --- | --- | --- |
| Alice starts work | none yet | The thread already exists from dispatch. |
| Alice commits | `Commit` | Braid can point to the git object that stores the diff. |
| Alice marks complete | `Decision` | The promote gate gets a terminal verdict. |
| Orchestrator accepts decision | no client event | Touched files are computed from git, not trusted from Alice. |

