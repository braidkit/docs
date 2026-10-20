---
title: Build and review BrewGo with parallel subagents
description: Delegate backend and frontend work, inspect each agent's choices in Braid, and add a follow-up feature to the same braid.
---

# Build and review BrewGo with parallel subagents

Use a parent agent to coordinate two subagents on BrewGo, a coffee order-ahead
app. One subagent builds an admin analytics API; the other builds the page that
uses it. Then use Braid to understand what each agent did, check the combined
result, and direct a follow-up change.

The finished feature is a small `/admin` page with sign-in, an order summary,
and sign-out. You will review its implementation before adding a CSV export
module through a third subagent on the same braid.

<!-- Source: braidkit/braid at 7ac66d63f8b7eeabf96d23b59bfa5d75ad422e2d,
docs/runbooks/live-claude-single-session-scenarios-detailed.md, Scenario 6:
Parallel Independent Subagents. The follow-up uses the new, separate file
ownership from orchestrator-subagent-disjoint-work-test-runbook.md, Stage 2.
Those tests use a CommonJS fixture. This guide adapts their workflow to the
React/FastAPI application in braidkit/brewgo; it does not copy fixture paths. -->

## Before you begin

| You need | Check |
| --- | --- |
| macOS and Git 2.25 or later | Braid's supported client platform. |
| Braid installed and signed in | Follow [Install Braid](../index.md#install-braid) first. |
| Claude Code or Codex with subagent support | The parent must be able to delegate two tasks concurrently. |
| Node.js 22.12 or later | Run `node --version`. |
| Python 3.10 or later | Run `python3 --version`. Use this interpreter when creating the virtual environment. |
| Access to `braidkit/brewgo` on GitHub | The sample repository is currently private. Ask the Braid team for access. |

Check Braid before starting the agent session:

```sh
braid version --json
braid auth status
braid hooks doctor
```

Resolve any sign-in or hook problem first. The version command reports the
CLI and daemon; the hook diagnostic checks the agent integration. These
checks do not prove that a future agent session will be recorded. You will
check the captured work after the implementation finishes.

Start a new agent session after setup. In Codex, run `/hooks` and approve
Braid's hooks when asked. An agent session that was already open during setup
may not be recorded.

## 1. Prepare the repository and branch

Use a fresh clone so the exercise starts with the storefront and no admin
analytics feature. The starting commit is pinned so a later merge into `main`
does not change the exercise:

```sh
git clone https://github.com/braidkit/brewgo.git
cd brewgo
git switch -c feat/admin-analytics \
  733976704cfe95136d104493fda186b2c0658b58
git status --short --branch
```

The current branch should be `feat/admin-analytics`, with no changed files.
Create this branch **before starting the agent session**. Keep the parent and
its subagents in this checkout and branch throughout the guide.

Install dependencies, then check the starting application:

```sh
npm ci
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements-lock.txt
npm run build
npm run test:api
```

Both checks should pass before you ask an agent to change the code. The API
tests use temporary databases. The app stores its local orders separately in
the ignored `backend/brewgo.db` file.

## 2. Run BrewGo and create sample orders

Start the development servers:

```sh
npm run dev
```

Open `http://127.0.0.1:5173`. The frontend runs on port 5173 and proxies API
requests to FastAPI on port 8000. Use `127.0.0.1` consistently so the session
cookies work.

Choose a cafe, add a drink, and complete the simulated checkout. Place three
orders and note each subtotal before tax. These will give you known values to
check against the new analytics page. No payment provider is contacted.

Leave the servers running. Open a second terminal in this `brewgo` checkout
for the agent and the Braid commands. You can also open the checkout in your
agent app.

## 3. Delegate backend and frontend work

The two subagents will work in separate directories. A shared API definition
lets them start together without waiting for each other's implementation.

| Agent | Owns | Responsibility |
| --- | --- | --- |
| Parent | Coordination and the combined commit | Define the API, delegate, check file ownership, and run the combined checks. |
| Backend subagent | `backend/`, including tests, except the two reserved export files | Admin accounts, sessions, read-only analytics, and API tests. |
| Frontend subagent | `src/` | Admin sign-in, summary, sign-out, and request states using the existing React components. |

Start a **new agent session** on `feat/admin-analytics`. Paste this complete
request into the parent session:

```text
Add a small admin analytics page to BrewGo using two parallel subagents.

Act as the parent coordinator. Confirm the repository root and branch first.
Work in this checkout on feat/admin-analytics. Inspect the existing React,
FastAPI, and SQLite app. Before delegating, define the request and response
shapes for admin sign-in, sign-out, and the analytics summary. Give both
subagents the same API definition so they can work independently.

Use /api/admin/session for admin session operations and
/api/admin/analytics/summary for the protected, read-only summary.
The summary must contain total orders, revenue before tax, average order
value, and counts grouped by order status. Keep money in integer cents and
status counts in a stable order. Revenue uses the subtotal of simulated-paid
orders, excluding cancelled or refunded orders; the average uses that same
set of orders and rounds to the nearest cent. Empty data returns zero totals.

Launch exactly two subagents concurrently in this checkout and branch.
Give them separate file ownership. Neither subagent should commit, switch
branches, create a worktree, or change the other's files. Use the existing
dependencies and preserve the storefront and saved orders.

Backend subagent:
- Own backend/ only, including its tests, except backend/analytics_export.py
  and backend/tests/test_analytics_export.py. Reserve those two paths for a
  later subagent; do not create or edit them in this step.
- Add admin sign-in and sign-out separate from sample customer profiles.
  Use password hashing and revocable sessions. Enforce admin access on every
  analytics request. Do not add default credentials or log passwords.
- Implement a local provisioning command:
  .venv/bin/python -m backend.admin guide-admin
  It must prompt for the password without echoing it or taking it as an
  argument. Store credentials outside tracked source files.
- Implement the agreed summary API. Handle empty data, invalid input, and
  unauthorized requests without exposing order details.
- Add focused tests for access checks, totals, status counts, rounding,
  empty data, session expiry, and sign-out. Run npm run test:api.

Frontend subagent:
- Own src/ only.
- Add /admin with sign-in, summary, and sign-out using the agreed APIs.
- Show loading, empty, unauthorized, and error states. Prevent an older
  response from replacing a newer result. Keep simulated payments labeled.
- Use the existing React components and dependencies. Run npm run build.

As parent, coordinate and review rather than edit implementation files.
Wait for both subagents to finish. Check that each changed only its owned
files. Have the responsible subagent fix any integration or test failure.
Run npm run build, npm run test:api, and git diff --check.
Commit only the completed feature and tests with this message:
feat: add BrewGo analytics with parallel subagents
Leave the working tree clean. Report each subagent's work, the API definition,
the checks that passed, and any checks that still need a person.
```

The parent should launch two subagents, wait for them, and make one combined
commit after the checks pass. Braid captures the work through the installed
agent integration; you do not need to register each subagent separately.

If a subagent needs a file outside its ownership, have the parent resolve the
scope before it edits. Keep backend and frontend ownership separate. Give
integration fixes back to the agent that owns the affected files.

## 4. Verify the application

Wait for both subagents and the parent's reply to finish. In your second
terminal, check the result:

```sh
git status --short
git log -1 --oneline
git show --stat --oneline HEAD
npm run build
npm run test:api
git diff --check
```

The working tree should be clean, and the latest commit should contain the
backend and frontend changes. The build and API tests should pass. Inspect
the changed paths to confirm that the agents stayed within their ownership.

The agents should now have created the admin provisioning command. Run it
yourself and enter a local test password at its hidden prompt:

```sh
.venv/bin/python -m backend.admin guide-admin
```

Keep that password out of agent messages and source files. Open
`http://127.0.0.1:5173/admin` and check the behavior:

| Check | Expected behavior |
| --- | --- |
| Open `/admin` while signed out | The page asks you to sign in and shows no analytics. |
| Try an incorrect password | Sign-in fails without exposing order data. |
| Sign in as `guide-admin` | The summary loads. |
| Compare the three sample orders | Revenue equals their subtotals before tax; the average uses those same orders. Their order status is `confirmed`, and payment status is `simulated_paid`. |
| Sign out and refresh `/admin` | Analytics remain unavailable until you sign in again. |
| Place another order in the storefront | The existing ordering flow still works; refresh analytics to see the updated totals. |

Also check the implementation's tests for empty data, unauthorized API access,
and failed requests. Seeing a sign-in page alone does not show that the API is
protected.

If a check fails, tell the parent what you observed. Have the owning subagent
fix it, rerun the checks, and commit before you reconstruct the intent. Keep
the commits in order and preserve their history during this guide.

## 5. Reconstruct the intent

Reconstruction sends recorded prompts, agent replies, and code changes to
Braid's service, which uses a third-party AI model. Braid currently does not
redact that information automatically. Use sample data and keep credentials
out of the captured work.

After the implementation turn finishes and every change is committed, run
this from your second terminal in `brewgo`:

```sh
braid intent
```

If more than one repository or branch is offered, choose this `brewgo`
checkout and `feat/admin-analytics`. Select the starting request beginning
"Add a small admin analytics page to BrewGo". Confirm the proposed evidence
boundary includes the parent coordination and both subagents.

Braid reconstructs the intent and opens the Review UI. Keep the braid ID from
the printed link; you will use it for the follow-up. When this guide shows
`<braid-id>`, replace it with that ID.

You can also send "reconstruct the intent" in a **new message** to the parent
and let Braid's installed skill guide you through the same process. Keep this
separate from the message that implements the feature, so the finished turn
can be included.

## 6. Review each agent's work

Start with **Overview**. Check that the goal describes the admin summary you
requested and that the outcome matches what you tested. A polished explanation
does not establish that the implementation works.

Use the views below the overview to answer different questions:

| View | What to check in this exercise |
| --- | --- |
| **Workstreams** | Follow the backend and frontend work separately. Open their traces to inspect the delegated prompts, changed files, and checks. The parent's role is coordination. |
| **Decisions** | Inspect how admin access, revenue, rounding, empty data, and request failures were handled. Open linked code for claims that affect your judgment. |
| **Steps** | Follow the work in recorded order, including failed attempts or integration fixes. |
| **Diagrams** | Use the available diagrams to understand how the page, session API, analytics, and stored orders fit together. Check them against the implementation. |

Backend code should map to the backend work, and frontend code to the
frontend work. Check that each subagent's trace includes its delegated task.
If a subagent is missing, investigate capture before treating the explanation
as complete.

Spend attention on choices with a practical consequence. For example, is
authorization enforced on the server? Does the revenue calculation use
subtotals rather than tax-inclusive totals? Does signing out revoke access?
Can a late response show data after the user signs out? Use the captured
tests and targeted code inspection to assess those choices.

Leave the braid active while you make the next change. Shipping is final.

## 7. Add a new subagent to the same braid

Now extend the feature using the two export files reserved in the first
request. Return to the **same parent session**, checkout, and branch. Paste:

```text
Continue the existing BrewGo analytics work on feat/admin-analytics.

Delegate a CSV export module to exactly one new subagent. The parent should
coordinate and verify the work rather than implement it.

The new subagent owns only:
- backend/analytics_export.py
- backend/tests/test_analytics_export.py

Implement orders_to_csv(orders), a dependency-free function accepting saved
BrewGo order dictionaries and returning CSV text. Use the standard library.
Include a stable header and the fields id, created_at, status, and total.
The total field is the existing order total in integer cents, including tax.
Preserve input order. Escape commas, quotes, carriage returns, and newlines.
Empty input returns the header only. Reject malformed input with a clear
validation error. Never mutate the input array or its order objects.

Add tests for normal and empty input, ordering, escaping, validation, and
immutability. Run the focused test and npm run test:api. Do not edit the
earlier files, change dependencies, or commit.

After the subagent finishes, verify that only those two new files changed.
Review the code and tests, run npm run test:api and git diff --check, and
commit those files with this message:
feat: add BrewGo analytics CSV export
Leave the working tree clean and report the checks that passed.
```

This adds a reusable export function and tests. Connecting it to an HTTP
endpoint or a download button would be a further change with a different
file scope.

Wait for the subagent and parent turn to finish, then check the follow-up:

```sh
git status --short
git log -2 --oneline
git diff --name-only HEAD~1 HEAD
npm run test:api
```

The latest commit should change only the two export files. Keep the earlier
implementation commits intact.

Reconstruct using the braid ID you saved, rather than starting another braid:

```sh
braid intent <braid-id>
```

In the updated review, check that the export work appears alongside the
earlier backend and frontend work, with its own prompt and two-file scope.
The explanation should include the new feature and preserve the earlier
work. The same braid now covers both stages.

## 8. Share, approve, and finish

If you want to share the intent on a pull request, use a fork or repository
where you have permission to open one. Follow
[Share with the Braid bot](../index.md#share-with-the-braid-bot), then ask the
parent to "push the braid to the PR". Sharing includes the intent and a
session summary with your prompts; review that content before sharing.

Once you understand and accept the final result, approve the candidate with
the command from the intent page:

```sh
braid review <braid-id> --verdict approved
```

Then finish the braid:

```sh
braid ship <braid-id>
```

Shipping marks it done and writes a signed Git note. If you plan to squash
merge a pull request, ship after the merge so the note lands on that commit.
You can leave the braid active while you continue experimenting.

Keep the checkout until you are done with the braid. Stop the local app with
Ctrl+C in the terminal running `npm run dev`.

## Troubleshooting

### The repository cannot be cloned

Check your GitHub sign-in and access to `braidkit/brewgo`. A private repository
can appear missing when your account cannot read it. Ask the Braid team for
access before continuing.

### An agent uses the fixture paths or the wrong test command

This guide uses BrewGo's React and FastAPI app. Backend files live in
`backend/`, frontend files in `src/`, and the test command is `npm run test:api`.
Ask the parent to recheck the pinned checkout and the prompt in this guide.

### The app does not start

Confirm your Node.js and Python versions, and that the dependencies were
installed in this clone. Check whether another process is using port 5173 or
8000. Resolve that conflict without stopping an unrelated application's
server, then retry `npm run dev`.

### The summary is empty or its numbers differ

A fresh clone has no orders. Place sample orders in the running app, then
refresh analytics. Confirm that the server uses this checkout's database.
Order `subtotal`, `tax`, and `total` values are integer cents; revenue before
tax should use `subtotal`. Payment status and order status are separate fields.

### A subagent or its changes are missing from the intent

Run these diagnostics from the exercise checkout:

```sh
braid hooks doctor
braid status --verbose
```

Check that the agent session started after hook setup, that both subagents
used the same checkout and branch, and that all implementation turns finished.
If you use Codex, confirm the hooks were approved. Ask your agent "why wasn't
my session recorded?" and preserve the checkout while investigating. Installing
hooks later does not establish that earlier work was captured.

### Reconstruction says work is not ready or its boundary is incomplete

Wait for the parent and subagents to finish. Confirm the intended changes
are committed and the working tree is clean. Check whether the branch,
checkout, or history changed during the exercise. Avoid rewriting history
to make the error disappear. If it persists, use
[Get help](../index.md#get-help) and ask your agent for a Braid support dump.
