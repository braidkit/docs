# Decisions

A decision is a thread's terminal verdict.

`Decision.verdict` tells the orchestrator whether a thread passed, failed, needs
human attention, or aborted. `Decision.reason` explains non-passing outcomes,
and `Decision.evidence_event_ids` points back to supporting events.

Touched files are not trusted from the decision payload. The orchestrator
computes them from git commit state.

