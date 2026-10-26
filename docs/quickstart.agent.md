# Braid Quickstart: instructions for a coding agent

You are a coding agent, such as Claude Code or Codex, running on the user's Mac.
Follow these instructions to run the Braid Quickstart for the user, with as
little manual work for them as possible.

Braid records the work that a coding agent does and reconstructs the intent
behind it: the goal, the decisions, and the checks. In this Quickstart, an agent
adds admin analytics to BrewGo, a sample coffee shop app, and the user reviews
the intent in Braid's Review UI.

The full guide for people is at <https://docs.braidkit.io/quickstart/>.

## Rules

- Run every command yourself. Ask the user only at the checkpoints below.
- Never ask for, type, or store a password, token, or key. Sign-in uses a code
  that the user approves in their browser.
- Do not use `sudo`, and do not change system settings.
- If a step fails, stop. Tell the user what failed and what they can do. Do not
  guess around a failure.
- Keep the user informed in one or two short lines per step.

## What the user does

Tell the user these checkpoints before you start:

1. Approve the Braid sign-in code in their browser.
2. In Codex only, approve Braid's hooks: `/hooks` in Codex CLI, or
   **Settings > Hooks** in the Codex app.
3. Approve your requests to use the network and to run commands, if their agent
   settings ask for approval.
4. Open a second agent session in `~/brewgo` and paste the prompt that you give
   them. Braid records only the sessions that start after its capture is on, so
   the feature cannot be built in this session.
5. In that session, send `reconstruct the intent` as a new message after the
   build. Braid reviews only finished turns.
6. Review the intent in the Review UI.

## Part 1: set up, in this session

### 1. Check the Mac

```sh
sw_vers -productVersion
git --version
node --version
```

Braid needs macOS. BrewGo's analytics need Node.js 22.13 or later, because they
use the built-in `node:sqlite` module. If Node.js is older or missing, stop and
ask the user to install Node.js 22.13 or later.

### 2. Install Braid

```sh
curl -fsSL https://braidkit.io/cli/install.sh | bash
```

Braid installs to `~/.local/bin`. This shell does not have the new `PATH` yet,
so call Braid as `~/.local/bin/braid` for the rest of this session. Without a
terminal, the installer does not sign in. The next steps do that.

### 3. Sign in

```sh
~/.local/bin/braid auth login
```

It prints a link and a code, and opens the browser. Show both to the user, then
wait for the command to finish while they approve the code. Allow up to ten
minutes. If the sign-in asks the user to install the Braid GitHub App, tell them
to install it for all repositories, or at least for the `brewgo` repository that
Part 2 creates.

### 4. Set up this Mac and turn on capture

```sh
~/.local/bin/braid init
~/.local/bin/braid hooks install claude
~/.local/bin/braid hooks doctor
```

Use `codex` instead of `claude` in the second command if you are Codex. In
Codex, ask the user to approve Braid's hooks now. Show the result of
`braid hooks doctor`. If it reports a problem, stop.

### 5. Get BrewGo

```sh
git clone https://github.com/braidkit/brewgo.git ~/brewgo
cd ~/brewgo
git switch -c feat/admin-analytics
test -f spec.md && test -f backend/brewgo.db && echo "BrewGo is ready"
```

Clone to `~/brewgo`. A folder outside Desktop, Documents, and Downloads avoids a
macOS prompt about folder access. BrewGo already has the build instructions in
`spec.md` and 300 sample orders in `backend/brewgo.db`, so there is nothing else
to install. If `~/brewgo` already exists, ask the user whether to reuse it.

### 6. Hand off to the second session

Tell the user to open a new session in `~/brewgo`, for example with
`cd ~/brewgo && claude` or `cd ~/brewgo && codex`, and to paste the prompt in
Part 2. Show them the prompt exactly as written. Then stop: the rest happens in
the new session.

## Part 2: the prompt for the second session

```text
You are in BrewGo for the Braid Quickstart, on the feat/admin-analytics branch.

1. Use spec.md and start working on building the admin analytics dashboard
   feature. Follow spec.md exactly, including its checks and its commit.
2. When the commit is done and the tree is clean, stop. Ask me to send
   "reconstruct the intent" as a new message, because Braid reviews only
   finished turns.
3. When I send it, reconstruct the intent and open the Review UI. Tell me to
   follow step 5 of https://docs.braidkit.io/quickstart/ to read the overview,
   the steps, the decisions, the workstreams, the diagrams, and the trace.
4. When I say the review is done, ask whether to share it. If I agree: create a
   private brewgo repository on my GitHub account, make it origin, push main,
   then push and raise a PR. Braid comments the intent on the PR when the Braid
   GitHub App is installed on that repository.
```

## If something goes wrong

- **Braid says the user is signed out, or the daemon is not running:** your
  sandbox may block the network or local connections. Ask the user to allow
  them, or to approve running `braid` outside the sandbox.
- **`braid` is not found:** use `~/.local/bin/braid`.
- **`braid hooks doctor` reports a problem:** show its output to the user and
  stop.
- **No captured work when the user asks to reconstruct the intent:** the build
  ran in a session that started before capture was on. Start a new session in
  `~/brewgo` and run the Part 2 prompt again.
- **The pull request has no intent comment:** the Braid GitHub App is not
  installed on the new repository. Ask the user to add the repository in the
  App's settings at <https://github.com/apps/braidkit/installations/new>.
