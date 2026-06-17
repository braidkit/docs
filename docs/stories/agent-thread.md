# Agent Thread

Codex works inside a Braid thread through a harness or SDK adapter.

```mermaid
sequenceDiagram
  actor User
  participant Agent as Codex
  participant SDK as Braid SDK
  participant O as Orchestrator
  participant Git

  User->>Agent: assign scoped task
  Agent->>SDK: session starts
  SDK->>O: WorkEvent(kind=AgentStart)
  SDK->>O: WorkEvent(kind=Prompt)
  Agent->>SDK: states understanding
  SDK->>O: WorkEvent(kind=IntentDeclaration)
  Agent->>SDK: runs tools
  SDK->>O: WorkEvent(kind=ToolUse)
  Agent->>SDK: observes files
  SDK->>O: WorkEvent(kind=ContextSnapshot)
  Agent->>Git: creates commit
  SDK->>O: WorkEvent(kind=Commit)
  Agent->>SDK: finishes
  SDK->>O: WorkEvent(kind=AgentEnd)
  SDK->>O: WorkEvent(kind=Decision)
```

Example event sequence:

| User or agent moment | Event sent | Why it matters |
| --- | --- | --- |
| User assigns task | `Prompt` | Reviewers can see the directive the agent received. |
| Agent starts | `AgentStart` | Captures model and instruction files loaded. |
| Agent forms intent | `IntentDeclaration` | Shows the agent's working understanding. |
| Agent calls tools | `ToolUse` | Captures tool inputs, outputs, status, and redaction flags. |
| Agent reads files | `ContextSnapshot` | Records which files shaped the work. |
| Agent commits | `Commit` | Links event stream to git state. |
| Agent exits | `AgentEnd` | Captures reason, tokens, and cost. |
| Agent decides | `Decision` | Gives the thread its terminal verdict. |

