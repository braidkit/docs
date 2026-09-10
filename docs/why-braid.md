---
title: Why Braid?
description: Why preserving the decisions behind agent-written code helps people review, maintain, and take ownership of the software.
---

# Why Braid?

Writing code is only part of owning software. You also need to understand why
it works the way it does, what assumptions it depends on, and what to preserve
when you change it.

When people and agents work together, that understanding can be scattered
across prompts, conversations, tool output, and review comments. The code
remains after the session ends. The context behind it is harder to recover.

Braid exists to preserve that context with the work, so the next person or
agent has a place to start.

## A diff does not tell the whole story

A diff shows what changed. It may not explain why one approach was chosen,
which alternatives failed, or what a passing check actually covered.

Those details matter during review. They also matter months later, when someone
needs to fix a bug or change an assumption. Without them, a contributor may
have to reconstruct the reasoning from the code, repeat earlier experiments,
or ask someone who no longer remembers.

Commit messages, pull requests, and design documents can preserve this
understanding. Braid complements them by recording evidence while the work is
happening, including the decisions and observations contributed along the way.

## Returning to a change weeks later

Imagine an agent adds retries to a request handler. The final code retries
some failures but deliberately excludes one operation.

Weeks later, another contributor wants to simplify the handler. The exception
looks unnecessary. But during the original work, the team found that retrying
that operation could create a duplicate transaction. They tried a broader
retry policy, rejected it, and checked the narrower behavior.

If those decisions and checks were captured, the later contributor can consult
the record to understand the exception before removing it. They can also see
what still needs to be checked if the operation has changed.

This is the kind of continuity Braid is intended to support: carrying the
understanding behind a change forward to the people who maintain it.

## A record to support human judgment

Braid keeps a record of captured agent work and the events contributed by
people and agents. That record can include prompts, agent messages, tool calls,
decisions, and checks. It provides evidence for understanding how a change
came about.

Evidence does not make a decision correct. A recorded explanation can be
incomplete, and a passing check only covers what it tested. Signing a record
helps establish which key signed it and whether it has changed; it does not
prove the code is safe or the reasoning is sound.

The purpose is to help reviewers and future contributors make informed
decisions. People still need to evaluate the work and take responsibility for
the software.

## What to expect in the private preview

Braid is in private preview. Capture is best effort, and some context depends
on what an agent explicitly contributes. A record can be partial; it is not a
complete account of everything a person or agent considered. The available
workflows are still evolving.

Start with [How Braid works](how-braid-works.md) for the model behind the
record. Read [What Braid records](what-braid-records.md) for the capture limits,
the data it can contain, and when that data leaves your machine.
