---
title: What Braid records
description: What Braid captures about your work, where it is stored, and the points at which it leaves your machine.
---

# What Braid records

Read this before pointing Braid at a codebase you care about. It covers what
Braid captures, where that lands, and the points at which it leaves your
machine.

## Contributor identity

GitHub proves the person. A local Ed25519 key proves the device. Braid issues
its own opaque session tokens.

The stable identity is GitHub's numeric user ID. A Braid user ID is an opaque
alphanumeric value such as `usr_008J4CT4ANK7F24SNAXWSQFEZW`. GitHub usernames,
email addresses, names, and avatars are stored as current profile data only, so
a renamed GitHub account is still the same Braid user.

A contributor fingerprint is derived from a signing key and identifies the
contributor instance that signed an event. It is not the Braid user ID. One
Braid user can hold several device keys, each with its own fingerprint.

The GitHub App is used only to identify and authenticate the person. It does not
require a repository permission or an App installation.

## Device credentials

Registering a device links its key to the signed-in Braid user and proves the
device holds the matching private key. Later sessions for that device are tied
to that key.

Revoking a device revokes every session tied to it. Revoking the GitHub App
authorization revokes every Braid session for that GitHub identity.

## What a signed work event contains

Each event carries:

- an event ID
- the braid ID and the thread ID it belongs to
- the contributor instance that acted
- the time the action happened
- the capture method
- exactly one payload
- an Ed25519 signature

The signing key is at `~/.braid/key.pem`. To sign, the client clears the
signature field, renders the rest as Protobuf JSON using proto field names and
enum strings with unset fields omitted, canonicalizes that JSON with RFC 8785,
hashes it with SHA-256, and signs the digest. The signature covers every other
field in the event. An event with an invalid signature is rejected.

## What is captured while an agent works

The payloads include tool use, agent reasoning, prompts, intent declarations,
attempt boundaries, commits, reviews, decisions, agent start and end, context
snapshots, and scope violations. Lifecycle transitions are also events.

Tool arguments and tool results are recorded as they occurred. The schema
reserves fields for marking a tool argument or result as redacted or truncated,
and nothing sets them today, so no redaction happens. A captured prompt, a
captured tool call, and a captured result can therefore contain source code,
file contents, diffs, and anything else passed to or returned from a tool.

## What leaves your machine

There are three points to know about, and they are different.

**Capture writes to disk only.** While an agent runs, each event is signed with
your local key and appended to a file in the local inbox. Capture opens no
network connection.

**Adding a session to a braid sends its events to the local daemon.** The
captured events are drained over a loopback gRPC connection, by default
`127.0.0.1:18082`. They stay on the machine.

**Intent reconstruction sends a braid's evidence to a model provider.** The
evidence is that braid's captured events, which includes the prompts, the
reasoning, and the tool calls with their arguments and results. It is sent to
the configured intent endpoint, and that service invokes a model provider. This
is the point at which captured work leaves the machine.

Two things trigger it:

- asking for intent to be reconstructed for a braid while preparing a review
- finalizing a braid, which sends the evidence automatically by default when an
  endpoint is configured

The second is worth restating. Finalizing a braid sends its evidence without a
separate confirmation step. It can be turned off per invocation, and it is
skipped when no endpoint is configured.

There is no endpoint compiled into Braid. Until a machine configuration sets
one, nothing is sent and the finalize step skips it. The example configuration
Braid ships sets it to Braid's hosted server, so a machine set up from that
example does send evidence there. The endpoint can point at a service you run
instead.

**The identity service does not receive your work.** It stores user, provider
identity, device, session, transaction, and audit records, and it stores hashes
of session tokens rather than the tokens. It does not receive source code,
diffs, prompts, Braid work records, or reconstructed intent.

**The local surfaces have no user authentication.** The daemon and the intent
server have no server-side user authentication and are meant to stay on
loopback. Anything else running on the machine that can reach those ports can
read captured work.

## Losing the signing key

Events already signed with a lost key stay in the record and their signatures
stay valid. They remain attributed to a key you no longer hold.

A new key produces a new contributor fingerprint, so work signed after the loss
is attributed to a different contributor instance than work signed before it.
