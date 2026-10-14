---
title: Braid
description: Set up Braid, review your first change from inside your coding agent, and learn the habits, limits and data handling that matter in the private preview.
---

# Braid

Braid keeps the intent behind code written with an AI agent, and the
understanding needed to work on it. As the work happens, Braid records what was
done, what was decided, what was noticed and what was checked. People and
agents then share the same picture of what the code is for and why it is the
way it is, so reviewers, teammates and future you can pick up the work and own
it.

Braid is in private preview and changes often. If something on this page
doesn't match what you see, tell us on [Discord](https://discord.gg/gzUevjYD9).

## Set up

You need a Mac, Git 2.25 or later, Claude Code or Codex, and a GitHub account
to sign in with. Your code doesn't have to be on GitHub.

Run this in a terminal:

```sh
curl -fsSL https://braidkit.io/cli/install.sh | bash
```

Say yes when the installer offers to sign you in and to set up this machine.
On the setup screen, select your agents with ++space++ and press ++enter++.
That turns on recording and teaches your agent how to use Braid.

Then **start a new agent session**. Sessions that were already open aren't
recorded. In Codex, also run `/hooks` and approve Braid's hooks, and approve
them again whenever Codex asks. To check that everything worked, ask your agent
"is braid set up correctly?"

From here on, you stay in your agent. You don't need to learn Braid's
commands. You ask your agent in plain words.

## Your first review

A review is a page that explains what changed, what was decided and what was
checked. You read it next to the diff.

1. **Start a new branch before you describe the task.** Braid ties the work to
   the branch it happens on.
2. **Ask your agent for the change**, as you normally would.
3. **Have it commit the work.**
4. **In a new message, say "open this for review".** An agent can't review the
   message it's still answering, so this has to be a message of its own.
5. **Pick where the work started.** The agent lists your requests on this
   branch and usually suggests the one that began the task.

Building the review takes a minute or two. The agent then gives you a link to
open it in your browser.

The review page suggests a next step as a terminal command: approve the review,
then ship it. You can ignore both during the preview.

## Ask your agent

| Ask | What happens |
|---|---|
| "open this for review" | Builds a review of the work on this branch and gives you the link. |
| "push the braid to the PR" | Uploads the review and links it to your pull request. See [Share a review](#share-a-review). |
| "is braid set up correctly?" | Checks the install, the background service and recording. |
| "why wasn't my session recorded?" | Checks how Braid is hooked into your agent. |

## Habits that keep reviews accurate

| Do this | Because otherwise |
|---|---|
| Keep to one task per branch | The review mixes the tasks together. |
| Plan and build on the same branch | The planning is left out of the review. |
| Don't squash, rebase or amend before the review. Squash when you merge the PR | Braid may refuse to build the review. |
| Keep the worktree until the pull request is merged | The review can't be rebuilt from another folder. |

## Share a review

Only you can see a review you open. To show it to the people reviewing your
pull request:

1. **Install the [Braid GitHub App](https://github.com/apps/braidkit) on the
   repository.** If it belongs to an organization, an admin may have to do this.
2. **Run `braid bot enable` once, in a terminal.** It lets Braid comment on your
   pull requests. The agent won't run it for you, because it changes what leaves
   your machine. `braid bot disable` turns it off.
3. **Ask your agent to "push the braid to the PR".** It asks before the first
   upload, then uploads the review. Braid comments on the pull request with a
   link to it.

Reviewers sign in with GitHub to open the review. Anyone who can read the
repository can see it. If the repository isn't on GitHub, only you can.

## What leaves your machine

- **While you work:** nothing. Recording stays on your Mac.
- **When a review is built:** your requests, the agent's replies, what its
  tools did and the code changes go to Braid's service. The service writes the
  review with a third-party AI model.
- **When you share a review:** Braid stores the review and a summary of the
  session: your requests, the agent's replies and one line per tool call.

Braid doesn't redact anything yet. Anything the agent read or wrote, secrets
included, can end up in what's sent.

To stop recording, run `braid hooks uninstall claude` or
`braid hooks uninstall codex`. To remove Braid completely, run
`braid uninstall`.

## Known limits

- Braid runs on macOS only, and records Claude Code and Codex.
- Braid can't review work started on a detached HEAD.
- If the agent works in another repository, those changes aren't part of this
  branch's review.
- If a review fails with "review boundary is incomplete", the branch's history
  was usually rewritten, or the work's checkout or branch changed.
- If a review fails with code BRD-9001, update Braid and try again.

## Keep Braid up to date

Braid doesn't update itself, and an out-of-date install can fail every review.
Run this in a terminal, or ask your agent to run `braid upgrade --yes`:

```sh
braid upgrade
```

## Get help

Ask your agent "is braid set up correctly?" first. It runs Braid's checks and
tells you what to fix.

If that doesn't sort it out, ask on [Discord](https://discord.gg/gzUevjYD9) or
email [hello@braidkit.io](mailto:hello@braidkit.io). Tell us what you expected
and what happened. If we ask for a support file, ask your agent to "make a
Braid support dump". The file holds Braid's checks and recent logs, but no
prompts, code or credentials.
