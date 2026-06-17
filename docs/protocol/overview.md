# Protocol Overview

Braid records work as a stream of signed `WorkEvent` messages.

The model has three levels:

- **Braid**: one unit of coordinated work, such as one issue.
- **Thread**: one lane inside a braid, usually tied to a scope or PR.
- **Event**: one recorded action by one contributor inside a thread.

Each event names the contributor that acted, the thread it belongs to, when it
happened, how it was captured, and exactly one payload kind.

```mermaid
flowchart LR
  Braid[Braid<br/>one coordinated task]
  ThreadA[Thread A<br/>human lane]
  ThreadB[Thread B<br/>agent lane]
  Event1[WorkEvent<br/>Prompt]
  Event2[WorkEvent<br/>ToolUse]
  Event3[WorkEvent<br/>Decision]

  Braid --> ThreadA
  Braid --> ThreadB
  ThreadB --> Event1
  ThreadB --> Event2
  ThreadB --> Event3
```

The proto is the source of truth for the wire contract. These docs explain the
shape and intent of that contract.

