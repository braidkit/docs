---
title: Quickstart
description: Add admin analytics to BrewGo with your coding agent, reconstruct the intent, and check the decisions against the code.
---

# Quickstart

Add a protected admin analytics page to [BrewGo](https://github.com/braidkit/brewgo),
a coffee order-ahead app. Then use Braid to understand what your agent built,
check its choices, and direct a change before you open or merge a pull request.

The storefront already exists. The exercise extends its Python/FastAPI backend,
SQLite database, and React frontend on a new branch. The orders are synthetic
and payments are simulated. You do not need to place orders.

!!! note "Draft setup dependency"
    BrewGo's repeatable sample-data setup must land on `main` before this page
    can be followed from a fresh clone. The `seed:orders` command below exists
    on the sample-data branch today. It preserves existing orders and avoids
    duplicating the synthetic history. The clone instructions remain a draft
    until that setup is published.

## Before you start

| You need | Notes |
| --- | --- |
| macOS and Git 2.25 or later | Braid's supported client platform. |
| Claude Code or Codex with subagent support | The request uses a parent and two parallel subagents. |
| Node.js 22.12 or later | BrewGo's frontend and development scripts. |
| Python 3.10 or later | BrewGo's existing API and tests. |
| Access to `braidkit/brewgo` | The sample repository is private. |

## 1. Install Braid

```sh
curl -fsSL https://braidkit.io/cli/install.sh | bash
```

Follow the prompts to sign in with GitHub and set up your coding agent.
The installer puts Braid in `~/.local/bin` and starts its local daemon.

```sh
braid auth status
braid hooks doctor
```

Braid records sessions started after setup. Open the new session in step 3,
after the feature branch is ready. Earlier sessions may not be recorded.

## 2. Prepare BrewGo

Start from the existing application on `main`:

```sh
git clone https://github.com/braidkit/brewgo.git
cd brewgo
git switch main
npm ci
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements-lock.txt
npm run seed:orders
npm run build
npm run test:api
```

The sample-data command adds 300 synthetic orders across five cafés, including
completed, cancelled, and refunded orders. Existing orders stay intact. If the
sample history is already present, running it again does not duplicate it.
The database stays local and is not committed to Git.

Create the feature branch **before starting the agent session**:

```sh
git switch -c feat/admin-analytics
```

## 3. Ask your agent to build the feature

Open a new agent session in this `brewgo` checkout. In Codex, run `/hooks`
and approve Braid's hooks when prompted. Then paste this request:

```text
Add a protected admin analytics page at /admin to BrewGo.
Extend the existing Python/FastAPI app and React frontend.
Use the saved SQLite orders. Preserve the storefront and data.

Act as the parent coordinator. First define a shared API for
admin sign-in, sign-out, and a filtered analytics summary. Then
launch two subagents in parallel in this checkout and branch:

- Backend: own backend/, including tests. Add admin accounts and
  revocable sessions separate from customer profiles. Protect
  every analytics request. Add a local command to create an admin
  that prompts for a password. Do not add default credentials.
- Frontend: own src/. Add sign-in, the summary, date-range and
  café filters, and sign-out. Handle loading, empty data, errors,
  and responses that arrive after filters change or sign-out.

Show total orders, revenue before tax, average order value, and
counts by status. Use integer cents. Define which orders count
in each metric, rounding, and date boundaries. Keep simulated
payments labeled. Use the existing dependencies.

Keep the subagents in their owned files. They should not commit
or switch branches. As parent, coordinate integration and have
the owning subagent resolve any failures.

Briefly report material choices, alternatives actually considered,
and what the checks showed. Run npm run build, npm run test:api,
and git diff --check. Fix failures and commit the completed work.
```

Wait for the parent and both subagents to finish. Follow the agent's admin setup
instructions, run `npm run dev`, and try `/admin` at `http://127.0.0.1:5173/admin`.
Check sign-in, filters, and sign-out. Confirm that the storefront still loads.

## 4. Reconstruct the intent

In a **new message** to the parent agent, ask:

```text
reconstruct the intent
```

Choose `brewgo`, the `feat/admin-analytics` branch, and the request from step 3.
Include the parent and both subagents. The implementation turn must have
finished so Braid can include it.

Braid opens the local Review UI. Keep the braid ID so later reconstructions
update the same braid.

Reconstruction uses Braid's hosted service and a third-party AI model. Captured
requests, agent replies, and code changes can be included. Keep the sample
synthetic and keep passwords out of agent messages.

## 5. Check what the agent decided

Start with **Overview**. Does the goal match your request? Does the outcome
match what you tried?

In **Workstreams**, follow the backend and frontend work separately. In **Steps**,
look at implementation, integration fixes, and checks. Then open the important
**Decisions** and inspect their linked code and evidence:

| Decision to inspect | Check against the code and tests |
| --- | --- |
| Admin access | Every analytics API request checks the admin session. A sign-in page alone is not protection. |
| Revenue and averages | Check which statuses count, whether tax is excluded, and how integer-cent averages round. |
| Date and café filters | Check timezone, start/end boundaries, and invalid input. |
| Sign-out and request races | A late response cannot restore analytics after sign-out or replace newer results. |
| API integration | Frontend and Python API use the same fields, units, and error behavior. |

An explanation can be wrong. Use the code, recorded checks, and your own app
checks to decide whether you accept each choice.

## 6. Steer a choice and review again

If you would decide something differently, return to the same parent session.
Explain the behavior you want and why. Ask the agent to make the change, run
the checks, and commit.

After that turn finishes, ask it to reconstruct the **same braid**, keeping
the original request as the starting point. The updated intent should include
the change and the reason you gave. Check it again.

## 7. Take the reviewed change to your PR

Push the code branch and open a pull request through your normal Git workflow.
If the PR already exists, update it with the reviewed commits. Local intent
review can happen before or after the PR is opened.

You can save the reconstructed braid to your own Braid account separately:

```sh
braid push <braid-id>
```

This uploads the intent and trace summary shown in the Review UI. It does
not push your Git branch. Team sharing is not enabled for this exercise;
pushing a braid is not a promise that teammates can open it.

Approval and shipping are optional during the preview. Approval records that
you understood and accepted the intent. Shipping is final and adds a signed Git
note to the commit. If you squash-merge, ship after the merge so the note is
attached to the resulting commit.

When ready, use the approval command from the intent page, then ask your agent
to "ship the braid". Keep the checkout and commit history until the braid is done.

## Troubleshooting

### Agent sandboxes

Braid's skills run `braid` through your agent, and it talks to the Braid daemon
on your machine. If your agent runs commands in a sandbox, as Codex does by
default and Claude Code does once you turn its sandbox on, the sandbox needs
network access and local binding. Without them, Braid can say you're signed out
or that the daemon isn't running when neither is true. Allow both in whichever
way suits you. Approving your agent's request to run `braid` outside the
sandbox works too.

### macOS folder access

If your repository is in Desktop, Documents, Downloads or iCloud Drive, macOS
asks whether `braid-daemon` can access that folder. Allow it, because Braid
reads your repository from there. If you chose **Don't Allow**, turn it back
on in **System Settings > Privacy & Security > Files & Folders**.

### Update Braid

Braid doesn't update itself, and an outdated install can fail to reconstruct
the intent.

```sh
braid upgrade
```

### Stop or remove Braid

To stop recording, run `braid hooks uninstall claude` or
`braid hooks uninstall codex`. To remove Braid, run `braid uninstall`.

## Need help?

Ask your agent "is Braid set up correctly?" if setup or recording looks wrong.
If a subagent is missing, check capture before accepting the record as complete.

Ask on [Discord](https://discord.gg/G3wzPsKtR) or email
[hello@braidkit.io](mailto:hello@braidkit.io).

[Build and review](build-and-review.md) will expand this exercise with full
verification steps, a CSV export follow-up, and the PR workflow.
