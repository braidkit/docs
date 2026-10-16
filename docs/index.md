---
title: Get started with Braid
description: Install Braid, understand your agent's work through the intent Braid reconstructs, and what to know during the private preview.
---

# Get started with Braid

Braid keeps the intent behind code written with an AI agent, and the
understanding needed to work on it. As the work happens, Braid records what was
done, what was decided, what was noticed and what was checked. People and
agents then share the same picture of what the code is for and why it is the
way it is, so reviewers, teammates and future you can pick up the work and own
it.

## Before you start

| You need | Notes |
|---|---|
| **macOS** | Linux and Windows aren't supported yet. |
| **Git 2.25 or later** | On your `PATH`. |
| **A Git repository** | Braid works on local branches. It doesn't need a remote. |
| **Claude Code or Codex** | The agents Braid records. |
| **A GitHub account** | You sign in with it. Your code can be hosted anywhere. |

## Install Braid

```sh
curl -fsSL https://braidkit.io/cli/install.sh | bash
```

The installer puts `braid` and `braid-daemon` in `~/.local/bin`, adds that to
your `PATH`, and starts the daemon as a login service. It never uses `sudo`.
Accept its prompts to sign in and to set up your agents.

When it finishes, start a new agent session, because sessions that were already
open aren't recorded. In Codex, also run `/hooks` and approve Braid's hooks,
and again whenever Codex asks.

!!! tip "Braid's skills do the work"
    Setting up an agent also installs Braid's skills, so you ask your agent in
    plain words instead of learning Braid's commands:

    | Ask | To |
    |---|---|
    | "reconstruct the intent" | [Understand the work](#understand-your-agents-work) on this branch |
    | "push the braid to the PR" | [Share the intent](#share-with-the-braid-bot) on your pull request |
    | "ship the braid" | [Finish the braid](#finish-with-braid-ship) |
    | "is braid set up correctly?" | Check the install and recording |
    | "why wasn't my session recorded?" | Check Braid's hooks in your agent |

## Try it on a sample project

[Haberdash](https://github.com/braidkit/haberdash) is a small order service
with one open issue: orders fail when the catalog service times out. The fix
looks small, but a retry in the wrong place charges a card twice.

First, look at [a finished intent](SHOWCASE_URL) built from four requests: a
plan, one pushback, the build and a follow-up. Its **Decisions** show each
choice, what it rejected and why, and the test that covers it.

Then make your own, with Python 3.9 or newer:

1. Clone Haberdash and create a branch:

    ```sh
    git clone https://github.com/braidkit/haberdash
    cd haberdash
    git switch -c fix/catalog-retries
    ```

2. Start a new agent session in `haberdash` and ask it to "read ISSUE.md and
   propose a plan, without changing any code yet".
3. Push back on one part you'd decide differently, such as where the retries
   live or how long an order may wait.
4. Ask it to build the plan, keep the tests green and commit.
5. In a new message, ask it to "reconstruct the intent", and pick the request
   from step 2.
6. In **Decisions**, find your pushback and the approach it replaced. Check
   that the code does what each decision says, above all for payment timeouts.
7. [Approve and ship](#finish-with-braid-ship) the braid.

The steps are the same on your own repository, except that you can also
[share the intent](#share-with-the-braid-bot) on your pull request.

## Understand your agent's work

Reconstructing the intent sends what Braid recorded, your requests, the agent's
replies and the code changes, to Braid's service, which uses a third-party AI
model. Braid currently does not redact information, so anything the agent saw
can be included.

1. Create a branch before your first request. Braid groups the work by branch.
2. Have your agent make the change and commit it.
3. In a new message, ask it to "reconstruct the intent". It can't include the
   message it's still answering.
4. Pick the request where the work started.

You get a link to the intent in a minute or two.

### Explore the intent

The intent gives you the context to understand the work: what it set out to
do, what was decided and why, and how the code changed. With that, you can
steer your agent where it went wrong, or [approve and ship](#finish-with-braid-ship)
with confidence. An AI model reconstructs the intent, so check anything that
matters against the code.

Start with the **Overview**: the goal, the outcome so far and why this
direction. If the goal isn't what you asked for, tell your agent before going
further.

Then explore the work in whichever way suits you, using the tabs below the
Overview:

| Tab | Shows the work |
|---|---|
| **Steps** | In the order it happened |
| **Decisions** | By the choices the agent made |
| **Workstreams** | By agent session, including subagents |

In each, open an item to see what was accepted and what was rejected and why,
the code it affected, and the agent trace behind it. Code and traces open in
the side panel.

**Diagrams** shows how the change fits together: a component diagram of the
parts it touched and a sequence diagram of how they call each other. Press `?`
for keyboard shortcuts.

## Share with the Braid bot

The intent is private until you share it. The Braid bot shares it on your pull
request: it comments with a brief of the intent and a link to the full page,
which anyone who can read the repository can open after signing in with GitHub.
Sharing uploads the intent and a summary of the session, including your
prompts. Please exercise care when sharing intent.

To turn the bot on:

1. Install the [Braid GitHub App](https://github.com/apps/braidkit) on the
   repository.
2. Run `braid bot enable`, once. It covers every repository, and your agent
   won't run it for you. `braid bot disable` turns it off.

Then ask your agent to "push the braid to the PR".

## Finish with braid ship

Approving signs that you understood and accepted the intent. Shipping marks the
braid done and writes the intent onto your commit as a signed Git note. Both
are optional during the preview, and neither has to wait for your pull request
to merge.

1. **Approve** once you understand the work, with the command from the intent
   page:

    ```sh
    braid review <braid-id> --verdict approved
    ```

2. **Ship** by asking your agent to "ship the braid". Shipping is final. If you
   squash-merge, ship after the merge so the note lands on the squashed commit.

## Tips for working with Braid

- One task per branch, or the intent mixes them.
- Plan and build on the same branch, or the planning is left out.
- Don't squash, rebase or amend before Braid reconstructs the intent. Squash
  when you merge.
- If your agent app gives each task its own copy of the repository (a Git
  worktree), keep that copy until you're done with the braid. Braid needs the
  folder the work happened in.

## Troubleshooting

### Known limitations

- Braid can't reconstruct work started on a detached HEAD.
- Changes the agent makes in another repository aren't in this branch's intent.
- "Review boundary is incomplete" usually means the history was rewritten, or
  the checkout or branch changed.

### Update Braid

Braid doesn't update itself, and an outdated install can fail to reconstruct
the intent.

```sh
braid upgrade
```

### Stop or remove Braid

To stop recording, run `braid hooks uninstall claude` or
`braid hooks uninstall codex`. To remove Braid, run `braid uninstall`.

### Get help

Ask on [Discord](https://discord.gg/gzUevjYD9) or email
[hello@braidkit.io](mailto:hello@braidkit.io).

If we ask for a support file, ask your agent for a "Braid support dump". It
holds Braid's checks and logs, not your prompts, code or credentials.
