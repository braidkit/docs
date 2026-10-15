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

Setting up an agent also installs Braid's skills. The skills teach your agent to run Braid for you, so you
ask for what you want in plain words instead of learning Braid's commands.

Then:

- Start a new agent session. Sessions that were already open aren't recorded.
- In Codex, run `/hooks` and approve Braid's hooks, and again whenever Codex asks.

## Understand your agent's work

1. Create a local branch. Braid ties the boundary of work to a branch.
2. Have your agent make the change and commit it.
3. In a new message, ask it to "reconstruct the intent". An agent can't include
   the turn it's in.
4. Pick the request where the work started.

You get a link to the intent in a minute or two. When you're confident in the
work, you can approve it and ship the braid; see
[Finish with braid ship](#finish-with-braid-ship).

### Explore the intent

The intent gives you the context to understand the work: what it set out to
do, what was decided and why, and how the code changed. With that, you can
steer your agent where it went wrong, or approve and ship with confidence. An
AI model reconstructs the intent from what Braid recorded, so check anything
that matters against the code.

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

## What to ask your agent

Braid's skills recognise requests like these, so the exact wording doesn't
matter.

| Ask | To |
|---|---|
| "reconstruct the intent" | Understand the work on this branch |
| "ship the braid" | [Finish the braid](#finish-with-braid-ship) |
| "is braid set up correctly?" | Check the install and recording |
| "why wasn't my session recorded?" | Check Braid's hooks in your agent |

## Tips to successfully work with Braid

- One task per branch, or the intent mixes them.
- Plan and build on the same branch, or the planning is left out.
- Don't squash, rebase or amend before Braid reconstructs the intent. Squash
  when you merge.
- If your agent app gives each task its own copy of the repository (a Git
  worktree), keep that copy until you're done with the braid. Braid needs the
  folder the work happened in.

## Finish with braid ship

Approving records, signed, that you understood and accepted this intent for
this exact commit. Shipping then marks the braid done and writes the intent
onto the commit you ship from, as a signed Git note, so whoever reads that
history later can see why the code is the way it is, and who signed off.
Shipping is final: a shipped braid takes no more work.

Both are optional during the preview. The note stays in your local repository,
because shipping doesn't push it, so the value today is in understanding the
work. Neither has to wait for your pull request to merge:

1. **Approve the braid as soon as you understand the work,** ideally before
   you open or merge the pull request. Copy the approve command from the
   intent page and run it. Your agent won't approve for you.

    ```sh
    braid review <braid-id> --verdict approved
    ```

    If your agent does more work on the branch afterwards, the braid goes back
    to Active. Reconstruct the intent and approve it again.

2. **Ship when you're done with the braid.** Ask your agent to "ship the
   braid". It confirms the branch and commit with you first, because the note
   goes on the commit you have checked out.

    If you ship before you squash-merge, the note stays on your branch's commit
    and doesn't follow the squashed commit onto your default branch. To keep
    the note with the code that landed, ship after the merge, from your updated
    default branch.

## What leaves your machine

- **While you work:** nothing.
- **When the intent is reconstructed:** your requests, the agent's replies,
  its tool activity and the code changes go to Braid's service, which writes
  the intent with a third-party AI model.
- **When you ship:** the braid's record goes to Braid's service again, to write
  the intent into the note.

Nothing is redacted yet, so secrets the agent saw can be included.

To stop recording, run `braid hooks uninstall claude` or
`braid hooks uninstall codex`. To remove Braid, run `braid uninstall`.

## Troubleshooting

### Check your setup

You can ask your agent "is braid set up correctly?" It runs Braid's checks and tells
you what to fix.

### Known limitations

- Braid can't reconstruct work started on a detached HEAD.
- Changes the agent makes in another repository aren't in this branch's intent.
- "Review boundary is incomplete" usually means the history was rewritten, or
  the checkout or branch changed.
- For BRD-9001, update Braid and try again.

### Update Braid

Braid doesn't update itself, and an outdated install can fail to reconstruct
the intent.

```sh
braid upgrade
```

### Get help

Ask on [Discord](https://discord.gg/gzUevjYD9) or email
[hello@braidkit.io](mailto:hello@braidkit.io).

If we ask for a support file, ask your agent for a "Braid support dump". It
holds Braid's checks and logs, not your prompts, code or credentials.
