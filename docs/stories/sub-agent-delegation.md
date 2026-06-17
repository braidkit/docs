# Sub-Agent Delegation

A parent agent can delegate part of an intent or attempt to a sub-agent. The
sub-agent emits its own events, while the parent rolls the outcome into the
thread decision.

```mermaid
sequenceDiagram
  participant Parent as Parent Agent
  participant Child as Sub-Agent
  participant SDK as Braid SDK
  participant O as Orchestrator

  Parent->>SDK: starts attempt
  SDK->>O: WorkEvent(kind=AttemptBoundary STARTED)
  Parent->>SDK: delegates attempt to sub-agent
  SDK->>O: WorkEvent(kind=AttemptBoundary, delegated_to_contributor_id=child)
  Child->>SDK: session starts
  SDK->>O: WorkEvent(kind=AgentStart, contributor=child)
  Child->>SDK: explores approach
  SDK->>O: WorkEvent(kind=ToolUse)
  SDK->>O: WorkEvent(kind=AgentEnd)
  Parent->>SDK: accepts or rejects child work
  SDK->>O: WorkEvent(kind=Decision, sub_agent_outcomes=[child])
```

Key rule: sub-agent work is traced through contributor lineage and explicit
delegation fields. The parent thread decision acknowledges what happened to
that work.

