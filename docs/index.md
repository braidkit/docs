---
title: Get started with Braid
description: Install Braid, try parallel subagents on BrewGo, and review their work through the intent Braid reconstructs.
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

<!-- Adapted from braidkit/braid, docs/runbooks/
live-claude-single-session-scenarios-detailed.md, Scenario 6: Parallel
Independent Subagents. That test uses a small CommonJS fixture. This exercise
uses the React/FastAPI app in braidkit/brewgo at the pinned storefront commit;
its paths and verification commands intentionally differ from the fixture. -->

BrewGo is a coffee order-ahead app with a React frontend and a FastAPI backend.
You'll add a small admin analytics page with two subagents working in parallel,
then use Braid to understand their choices and how the work fits together.

You need **Node.js 22.12 or later**, **Python 3.10 or later**, and an agent
that can launch subagents. BrewGo is currently private; ask the Braid team for
repository access before starting.

### Set up BrewGo

1. Clone it and create a branch from the storefront commit. Starting from this
   commit keeps the exercise available after later features are merged:

    ```sh
    git clone https://github.com/braidkit/brewgo.git
    cd brewgo
    git switch -c feat/admin-analytics \
      733976704cfe95136d104493fda186b2c0658b58
    ```

2. Install the dependencies and start the app:

    ```sh
    npm ci
    python3 -m venv .venv
    .venv/bin/pip install -r backend/requirements-lock.txt
    npm run dev
    ```

    Open `http://127.0.0.1:5173` and place a few sample orders to give the
    analytics something to show. Payments are simulated. Use `127.0.0.1`
    consistently so its cookies work. `npm run dev` starts the frontend on
    port 5173 and the API on port 8000. Leave it running while you work.

### Delegate the work

Start a **new agent session** in this `brewgo` checkout, on
`feat/admin-analytics`. If you use a terminal agent, open a second terminal
in `brewgo` so the app can keep running. For this exercise, keep the parent
and its subagents in the same checkout and branch. Paste this request:

```text
Add a small admin analytics page to BrewGo using two parallel subagents.

Act as the parent coordinator. Confirm the repository and branch first.
Inspect the existing React, FastAPI, and SQLite app. Before delegating, define
the admin sign-in, sign-out, and analytics APIs and their response shapes.
Give both subagents the same API contract so they can work independently.

Launch exactly two subagents concurrently in this checkout and branch.
Give them separate file ownership. Neither subagent should commit, switch
branches, create a worktree, or change the other's files.

Backend subagent:
- Own backend/ only, including its tests.
- Add admin sign-in and sign-out separate from the sample customer profiles,
  with no default credentials. Provide a local command to create an admin.
- Add a read-only summary of saved orders: total orders, revenue before tax,
  average order value, and counts by status. Keep money in integer cents.
- Require an admin session for every analytics request. Handle empty data
  and unauthorized requests. Preserve orders and the existing customer APIs.
- Add focused API tests and run npm run test:api.

Frontend subagent:
- Own src/ only.
- Add an /admin page with sign-in, summary, and sign-out using the agreed APIs.
- Show the summary with loading, empty, unauthorized, and error states.
  Keep simulated payments clearly labeled and preserve the storefront.
- Use the existing components and dependencies. Run npm run build.

As parent, coordinate and review rather than edit implementation files.
Wait for both subagents to finish. Check that each changed only its owned
files. Run npm run build, npm run test:api, and git diff --check.
Check the admin sign-in, summary, sign-out, and original ordering flow in
the browser. Fix any failures through the subagent that owns the files.
Commit the completed change with this message:
feat: add BrewGo analytics with parallel subagents
Leave the working tree clean. Report each subagent's result, the checks that
passed, and how to create the local admin account.
```

The parent coordinates and commits. The backend and frontend subagents each
own their implementation. Braid records the work as it happens; you don't
need to register each subagent yourself.

### Review the combined work

1. Wait for both subagents and the parent's reply to finish, with the change
   committed. Read [what reconstruction sends](#understand-your-agents-work),
   then send a **new message**:

    ```text
    reconstruct the intent
    ```

2. Pick the request that starts "Add a small admin analytics page to BrewGo".
   Open the intent link when it is ready.

3. Start with **Overview**. Check that the goal and outcome describe the
   admin summary you asked for. In **Workstreams**, follow the parent's
   coordination and the separate backend and frontend work. Open each
   subagent's trace to see what it was asked to do and the files it changed.

4. In **Decisions**, inspect how admin access is checked, how revenue is
   calculated, and how the UI handles failed requests. Check consequential
   claims against the linked code and test results. A reconstructed explanation
   does not establish that the implementation works.

5. Try steering the work. For example, ask the parent to have the frontend
   subagent add a retry button after a failed analytics request, if one is
   missing. Have it check and commit the change. Then reconstruct the intent
   again for the **same braid** and the same starting request. Check that the
   updated intent explains the change and retains the earlier work.

6. When you're done steering, [approve and ship](#finish-with-braid-ship) once
   you understand and accept the result.

If a subagent's work is missing, ask your agent "why wasn't my session
recorded?" before treating the review as complete. You can also
[share the intent](#share-with-the-braid-bot) on a pull request in a repository
where you have permission to open one.

## Understand your agent's work

Reconstructing the intent sends what Braid recorded, your requests, the agent's
replies and the code changes, to Braid's service, which uses a third-party AI
model. Braid currently does not redact information, so anything the agent saw
can be included.

1. Create a branch before your first request.
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

- Create the branch before your first request, and stay on it until the work
  is committed. Braid files each request under the branch it started on, so
  work begun on another branch is left out of the intent.
- One task per branch, or the intent mixes them.
- Don't squash, rebase or amend before Braid reconstructs the intent. Squash
  when you merge.
- If your agent app gives each task its own copy of the repository (a Git
  worktree), keep that copy until you're done with the braid. Braid needs the
  folder the work happened in.

## Troubleshooting

### Known limitations

- Braid is built for one developer for now. Features for teams are coming.
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

Ask on [Discord](https://discord.gg/G3wzPsKtR) or email
[hello@braidkit.io](mailto:hello@braidkit.io).

If we ask for a support file, ask your agent for a "Braid support dump". It
holds Braid's checks and logs, not your prompts, code or credentials.
