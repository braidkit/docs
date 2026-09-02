---
title: What Braid records
description: What Braid records, how it identifies you, and when it sends data to external services.
---

# What Braid records

Braid keeps a local record of agent work. It records the prompt that starts a
captured session, along with agent messages, reasoning, tool calls, and tool
results. It can contain source code, file contents, diffs, and other data
passed to or returned from a tool.

Braid does not send that record to an external service while it captures work or
moves events to its local daemon. Today, it sends evidence only when intent
reconstruction or finalization runs with an intent endpoint configured.

## Your identity and device

Braid associates work with your account and the device that signed it. At launch,
you sign in through GitHub. GitHub identifies you to Braid; it does not give
Braid repository permissions and does not require a GitHub App installation.
Braid is designed to support additional sign-in providers later.

Each device has a local signing key. Braid uses that key to sign work events and
distinguish the device or agent session that signed them. You can use more than
one device with the same account; each retains its own signer history.

## At a glance

| Action | Where the data goes | Leaves your machine? |
| --- | --- | --- |
| Sign in | Braid's identity service | Your identity, never your work |
| Capture agent work | Local inbox | No |
| Add a captured session to a braid | Local Braid daemon, over loopback | No |
| Reconstruct intent for review | Braid's intent service, which calls a model provider | Yes, when configured |
| Finalize a braid | Braid's intent service, which calls a model provider | Yes by default, when configured |

## What Braid records

Braid records the prompt that starts a captured session, along with session
boundaries, agent messages, reasoning, and tool calls with their arguments and
results.

Some context is cooperative. Braid asks the agent to mark attempts, changes in
understanding, and final decisions in its output. Braid records those markers
only when the agent emits them.

Capture is best effort. Unsupported or malformed output, or a capture error,
can result in a partial record. Capture does not interrupt the agent.

Each record is signed with the local Braid key, so Braid can verify the event
has not changed and identify the key that signed it.

## Redaction

Braid does not redact or truncate anything yet. Tool arguments and results are
recorded as they occurred, so if an agent reads a file that holds credentials,
those values are in the record too.

The record stays on your machine until you reconstruct intent or finalize a
braid, so what it contains is yours to manage until then. Automatic redaction is
planned for a future release.

## When Braid sends data

Capture writes its record to disk and sends no part of it off your machine.
Commands that need a signed-in identity, capture among them, do contact the
Braid identity service to prove that identity. It receives your GitHub identity
and your device key, stores hashes of session tokens rather than the tokens, and
never receives your code, your prompts, or your captured work.

Adding a captured session to a braid sends its events only to the local daemon,
over loopback (`127.0.0.1:18082` by default).

Braid sends a braid's evidence off your machine only when an intent endpoint is
configured and you:

- reconstruct intent while preparing a review
- finalize a braid; this sends evidence automatically by default

The evidence includes the braid's captured events, such as prompts, agent
messages, reasoning, and tool calls with their arguments and results.
Finalization can disable this send for an individual invocation.

Braid sends no evidence when no intent endpoint is configured. The example
configuration uses Braid's hosted service, and you can point the endpoint at a
service you operate instead.

## Whose services these are

The identity service and the intent service are both Braid's own. Neither is a
third party.

The intent service reconstructs the intent behind a braid and returns it. It
stores nothing. Reconstruction needs a model, so the service passes the evidence
to a model provider, and that provider is the only third party in the path.

Braid keeps the result rather than the service keeping it. The reconstructed
intent is archived on your machine and attached to your repository's Git notes,
which is what lets someone read a braid later.

## Local services

The local daemon and local intent server are designed to run only on loopback.
They do not provide server-side user authentication. Other processes on the same
machine that can reach those ports can read captured work.
