---
title: Quickstart
description: Add a new feature to a sample coffee shop app with your coding agent, reconstruct the intent, and check the decisions against the code.
---

# Quickstart

[BrewGo](https://github.com/braidkit/brewgo) is a digital coffee shop like starbucks. 

We are adding admin analytics to [BrewGo](https://github.com/braidkit/brewgo). Then use Braid to understand what your agent built,
check its choices, and direct a change before you open or merge a pull request.

The storefront already exists, and BrewGo comes with 300 synthetic orders in its SQLite database.
Following `spec.md` in the repository, your agent adds an analytics module that reads those orders
without changing them, and a testable admin view. A parent agent gives each part to its own subagent.
Payments are simulated.

## Before you start

| You need | Notes |
| --- | --- |
| macOS and Git 2.25 or later | Braid's supported client platform. |
| Claude Code or Codex with subagent support | The spec uses a parent and two parallel subagents. |
| Node.js 22.13 or later | The analytics module reads SQLite with Node's built-in `node:sqlite`. |
## 1. Install Braid

```sh
curl -fsSL https://braidkit.io/cli/install.sh | bash
```

Follow the prompts to sign in with GitHub and set up your coding agent.

[Screenshot-tktk]

The installer puts Braid in `~/.local/bin`.

Braid records AI Coding agent sessions automatically after installation setup. 

> In Codex CLI, run `/hooks` and approve Braid's hooks when prompted. In Codex Desktop, please trust all the hooks by going to Settings -> Hooks.

## 2. Prepare BrewGo

In a terminal, clone BrewGo and create the feature branch **before starting the agent session**.
A fresh clone is on `main`:

```sh
git clone https://github.com/braidkit/brewgo.git
cd brewgo
git switch -c feat/admin-analytics
```

## 3. Ask your agent to build the feature

Open a new coding agent session in this `brewgo` checkout. Then paste this prompt:

```text
use spec.md and start working on building the admin analytics dashboard feature
```

Wait for the parent and both subagents to finish. 

## 4. Reconstruct the intent

You can reconstruct the intent in two ways: through Braid's skill in your agent,
or with the CLI.

=== "Skill"

    In the same coding agent session, send a new message:

    ```text
    reconstruct the intent
    ```

=== "CLI"

    In a terminal, in your `brewgo` checkout, run:

    ```sh
    braid intent
    ```

    Braid finds the captured work on the current branch and asks which prompt to
    include.

Braid opens the local intent review UI. 

[screenshot-tktk]

## 5. Understand what the agent did through Braid

Start with **Overview**. Does the goal match your request? Does the outcome
match with what you are thinking?

[screenshot-tktk]

In **Workstreams**, follow the backend and frontend work separately. In **Steps**,
look at implementation, integration fixes, and checks. Then open the important
**Decisions** and inspect their linked code and evidence:

| Decision to inspect | Check against the code and tests |
| --- | --- |
| Admin access | Only an admin request gets analytics. Any other request gets a 403 before the orders are read. |
| Revenue and averages | Cancelled and refunded orders count in the total but not in revenue or the average. Check how the average rounds. |
| Malformed orders | The agent defines a rule for an order with a missing status or a non-integer total. Such an order must not change revenue or the average. |
| Read-only data | The SQLite orders are read and never changed. Check the before-and-after hash of `brewgo.db` that the agent reports. |
| Stale responses | In the admin view, an older response, including a failed one, cannot replace a newer result. |

An explanation can be wrong. Use the code, the recorded checks, and the test
results to decide whether you accept each choice.

## 6. Share the Intent with your peers

You cannot push to `braidkit/brewgo`, so first move your work to a repository of
your own:

1. On GitHub, [create a new repository](https://github.com/new) named `brewgo`,
   public or private. Leave it empty: do not add a README, license, or `.gitignore`.
2. In a terminal, in your `brewgo` checkout, point `origin` at it and push `main`.
   Replace `<your-username>` with your GitHub username:

    ```sh
    git remote set-url origin https://github.com/<your-username>/brewgo.git
    git push -u origin main
    ```

Your pull request opens in this repository.

You can share the intent in two ways: through Braid's skills in your agent, or
with the CLI.

=== "Skill"

    In the same coding agent session, ask:

    ```text
    push and raise a PR
    ```

    Your agent pushes the branch and opens the pull request. Braid's skills then
    push the braid and link it to the pull request, and Braid comments the intent
    on the PR, so your peers can read the intent where they review the code.

    Your agent opens the pull request with its own GitHub tools, usually the
    GitHub CLI. If it has none, use the CLI method.

=== "CLI"

    Push the branch:

    ```sh
    git push -u origin feat/admin-analytics
    ```

    Open the pull request on GitHub from the link that `git push` prints. Then
    push the braid with its ID from step 4, and the pull request number and URL.
    Always pass both:

    ```sh
    braid push <braid-id> --pr-number <number> --pr-url <pull-request-url>
    ```

    To upload the intent without a pull request, run `braid push <braid-id>`.

Braid comments on a pull request when the Braid GitHub App is installed on its
repository. If you installed the App for selected repositories only, add your new
`brewgo` repository in the [Braid App's settings](https://github.com/apps/braidkit/installations/new).

## Troubleshooting

### Agent permissions

Braid's skills run `braid` through your agent. If your agent runs commands in a sandbox, as Codex does by
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

![The macOS dialog: "braid-daemon" would like to access files in your Documents folder, with Don't Allow and Allow buttons.](assets/quickstart/macos-folder-access.png){ width="302" }

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

Ask on [Discord](https://discord.gg/G3wzPsKtR) or email
[hello@braidkit.io](mailto:hello@braidkit.io).
