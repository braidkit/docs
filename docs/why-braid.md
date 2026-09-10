---
title: Why Braid?
description: Why capturing the goals and decisions behind agent-written code helps people steer work, review changes, and own the software.
---

# Why Braid?

AI made code cheap to produce. It did not make software cheap to own. You still
need to understand why it works the way it does, what assumptions it depends
on, and what to preserve when you change it.

When people and agents work together, that understanding can be scattered
across prompts, conversations, tool output, and review comments. The code
remains after the session ends. The context behind it is harder to recover.

Two kinds of debt can accumulate as a result. **Cognitive debt** is the gap in
understanding that makes it harder to explain how the software works or what a
change will break. **Intent debt** is the loss of the goals and rationale that
should guide its evolution. You may understand what the code does without
knowing why it should do it. As more changes build on decisions nobody
remembers, that gap grows.

Braid captures evidence of that intent and understanding as people and agents
work. It uses the record to help contributors steer ongoing work, reconstruct
intent for review, and carry context forward to whoever takes ownership next.

## A diff does not tell the whole story

A diff shows what changed. It may not explain why one approach was chosen,
which alternatives failed, or what a passing check actually covered.

Those details matter when you review your own work, when a teammate reviews
it, and months later when someone needs to fix a bug or change an assumption.
Without them, a contributor may have to reconstruct the reasoning from the
code, repeat earlier experiments, or ask someone who no longer remembers.

Commit messages, pull requests, and design documents preserve what someone
chooses to write down. They do not automatically retain the experiments,
rejected approaches, and checks behind a conclusion. Capturing that context
takes deliberate effort, and a summary written afterward can leave out the
detail a future contributor needs.

Braid captures available session evidence and the decisions people and agents
explicitly record as they work. That gives the next contributor evidence to
consult alongside the PR description or commit message.

## More than a session transcript

A session transcript can contain useful context, but reading every prompt and
tool call is a lot to ask of the next contributor. Braid uses captured events
to reconstruct an account of the work: the goal, the decisions and their
recorded rationale, the approaches tried, and the checks performed. That
account links back to the evidence so a reviewer can check an explanation
against the original work and see what is missing.

Contributors can use that record throughout the work:

- **While work is happening**, question a recorded decision or redirect an
  approach before more work depends on it.
- **At review**, assess the change against its goal, examine the choices made,
  and decide what still needs checking.
- **During maintenance**, understand an unfamiliar choice and judge whether
  the original reasoning still applies.

## Returning to a change weeks later

Imagine an agent adds retries to a checkout service. Product lookups retry
after a timeout, but the call that charges a card does not.

Weeks later, another contributor wants to use one retry policy for both.
The exception looks unnecessary. But the team had found that a charge could
succeed even when its response never arrived. Their payment integration had
no protection against duplicate requests, so retrying could charge the
customer twice. The team rejected automatic retries for that call.

If that investigation and decision were captured, the later contributor can
understand the exception before removing it. They can also see what would
justify changing it: a way to retry without creating a second charge.

## A record to support human judgment

Evidence does not make a decision correct. A recorded explanation can be
incomplete, a reconstruction can misinterpret it, and a passing check only
covers what it tested. Connecting an explanation to its source makes it easier
to examine; it does not prove that the code is safe or the reasoning is sound.

People still need to evaluate the work and take responsibility for the software.

## What to expect in the private preview

Braid is in private preview. Capture is best effort, and some context depends
on what an agent explicitly contributes. A record can be partial; it is not a
complete account of everything a person or agent considered. The available
workflows are still evolving.

Start with [How Braid works](how-braid-works.md) for the model behind the
record. Read [What Braid records](what-braid-records.md) for the capture limits,
the data it can contain, and when that data leaves your machine.

[Preview status](preview-status.md) is currently an outline. It will cover v0's
supported workflows, unavailable capabilities, and known limitations.
