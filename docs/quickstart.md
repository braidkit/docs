---
title: Quickstart
description: Add a new feature to a sample coffee shop app with your coding agent, reconstruct the intent, and check the decisions against the code.
---

# Quickstart

[BrewGo](https://github.com/braidkit/brewgo) is a digital coffee shop like Starbucks. 

We are adding admin portal feature to [BrewGo](https://github.com/braidkit/brewgo) sample repository. Then use Braid to understand what your agent built,
check its choices, and direct a change before you open or merge a pull request.

Following `spec.md` in the repository, your agent adds an analytics module that reads those orders
without changing them, and a testable admin view. A parent agent gives each part to its own subagent. 

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

Follow the prompts to sign in with GitHub, add the Braidkit App and set up your coding agent.

[Screenshot-tktk]

The installer puts Braid in `~/.local/bin`.

Braid ambiently records AI Coding agent sessions automatically after installation setup. The coding sessions stay local. We will never be able to see them!

> In Codex Desktop, please trust all the hooks by going to Settings -> Hooks. In Codex CLI, run `/hooks` and approve Braid's hooks when prompted. 

## 2. Prepare BrewGo

In a terminal, clone BrewGo and create the feature branch **before starting the agent session**.


```sh
git clone https://github.com/braidkit/brewgo.git
cd brewgo
git switch -c feat/admin-analytics
```

## 3. Ask your agent to build the feature

Open a new coding agent session in this `brewgo` checkout. Then paste this prompt:

```text
use spec.md and start working on building the admin analytics dashboard feature.
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

You cannot push to `braidkit/brewgo`, so your pull request opens in a repository
of your own. You can share the intent in two ways: through Braid's skills in your
agent, or with the CLI.

=== "Skill"

    In the same coding agent session, ask:

    ```text
    create a private brewgo repository on my GitHub account, make it origin, push main, then push and raise a PR
    ```

    Your agent creates the repository with its own GitHub tools, usually the
    GitHub CLI, and points `origin` at it. Then it pushes the branch and opens
    the pull request. Braid's skills push the braid, link it to the pull request,
    and comment the intent on the PR, so your peers can read the intent where
    they review the code.

=== "CLI"

    With the [GitHub CLI](https://cli.github.com), create the repository, push
    both branches, and open the pull request:

    ```sh
    git remote remove origin
    gh repo create brewgo --private --source=. --remote=origin
    git push -u origin main
    git push -u origin feat/admin-analytics
    gh pr create --base main --fill
    ```

    Then push the braid with its ID from step 4, and the pull request number and
    URL that `gh pr create` printed. Always pass both:

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
