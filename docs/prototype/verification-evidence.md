---
title: Verification evidence
description: See what Braid records when a configured check runs.
---

# Verification evidence

Verification turns the configured check into durable evidence associated with a thread.

## Choose the scope

Run a check for the thread whose work you intend to verify.

```sh
braid verify <braid-id> --thread <thread-id>
```

## Recorded outcome

The result captures whether the check passed, failed, or could not run, together with the event that established the outcome.

### Passed

The configured command completed successfully for the selected work.

### Failed

The check ran and returned a failing result. The thread remains visible as evidence and can be reopened for another attempt.

### Needs human attention

The system could not make the next decision without input from a person.

## What verification does not prove

Verification is limited to the configured check. It does not infer product intent, security guarantees, or reviewer approval.
