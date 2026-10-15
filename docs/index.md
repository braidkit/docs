---
title: Braid
description: Install Braid, review your first change from your coding agent, and what to know during the private preview.
---

# Braid

Braid keeps the intent behind code written with an AI agent, and the
understanding needed to work on it. As the work happens, Braid records what was
done, what was decided, what was noticed and what was checked. People and
agents then share the same picture of what the code is for and why it is the
way it is, so reviewers, teammates and future you can pick up the work and own
it.

Braid is in private preview and changes often. If something here is out of
date, tell us on [Discord](https://discord.gg/gzUevjYD9).

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

Then:

- Start a new agent session. Sessions that were already open aren't recorded.
- In Codex, run `/hooks` and approve Braid's hooks, and again whenever Codex
  asks.
- If `braid` isn't found, open a new shell.

## Check your setup

Ask your agent "is braid set up correctly?" It runs Braid's checks and tells
you what to fix.

From here on, you work through your agent.

## Review your first change

1. Create a branch before your first request. Braid ties work to its branch.
2. Have your agent make the change and commit it.
3. In a new message, ask it to "open this for review". An agent can't review the
   turn it's in.
4. Pick the request where the work started.

You get a link to the review in a minute or two. Ignore the approve and ship
commands on the review page for now.

## What to ask your agent

| Ask | To |
|---|---|
| "open this for review" | Build a review of this branch |
| "push the braid to the PR" | [Share the review](#share-a-review) on your pull request |
| "is braid set up correctly?" | Check the install and recording |
| "why wasn't my session recorded?" | Check Braid's hooks in your agent |

## Get better reviews

- One task per branch, or the review mixes them.
- Plan and build on the same branch, or the planning is left out.
- Don't squash, rebase or amend before the review. Squash when you merge.
- Keep the worktree until the pull request is merged.

## Share a review

Reviews are private until you share them. First:

1. Install the [Braid GitHub App](https://github.com/apps/braidkit) on the
   repository.
2. Run `braid bot enable`, once. Your agent won't run it for you.

Then ask your agent to "push the braid to the PR". Braid comments on the pull
request with a link. Anyone who can read the repository can open it after
signing in with GitHub.

## What leaves your machine

- **While you work:** nothing.
- **When a review is built:** your requests, the agent's replies, its tool
  activity and the code changes go to Braid's service, which writes the review
  with a third-party AI model.
- **When you share:** Braid stores the review and a summary of the session.

Nothing is redacted yet, so secrets the agent saw can be included.

To stop recording, run `braid hooks uninstall claude` or
`braid hooks uninstall codex`. To remove Braid, run `braid uninstall`.

## Known limitations

- No reviews of work started on a detached HEAD.
- Changes the agent makes in another repository aren't in this branch's review.
- "Review boundary is incomplete" usually means the history was rewritten, or
  the checkout or branch changed.
- For BRD-9001, update Braid and try again.

## Update Braid

Braid doesn't update itself, and an outdated install can fail reviews.

```sh
braid upgrade
```

## Get help

Ask on [Discord](https://discord.gg/gzUevjYD9) or email
[hello@braidkit.io](mailto:hello@braidkit.io).

If we ask for a support file, ask your agent for a "Braid support dump". It
holds Braid's checks and logs, not your prompts, code or credentials.
