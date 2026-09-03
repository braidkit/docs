---
title: Signed events
description: Learn how signed events form the durable evidence behind a braid.
---

# Signed events

Every accepted event becomes part of the braid's append-only evidence record.

## Event envelope

The envelope identifies the event, contributor, braid, thread, sequence, payload type, and signature.

## Admission

Ingest is the boundary where malformed, misaddressed, duplicated, or incorrectly signed events are rejected.

### Signature validation

The signature binds the event payload to the contributor identity and registered device key.

### Authority validation

Event-specific rules constrain who can assert a particular fact. An agent cannot record a human-only decision.

## Derived state

After admission, an event is permanent evidence. Braid derives lifecycle state from the ordered log and records mismatches as anomalies rather than rewriting history.

## Replay

Replay presents the record for later review, debugging, or handoff.

```sh
braid replay <braid-id>
```

## Trust boundary

Signatures prove which registered key produced an event and whether the payload changed. They do not prove that every statement inside the payload is true.
