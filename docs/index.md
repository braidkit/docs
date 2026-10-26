---
title: Overview
description: Understand what is Braid, how and why to review the intent behind a change.
---

# Overview

Git records what changed in your code. Braid records why it changed: what you
asked your coding agent for, the decisions it made, and the checks it ran.
So you, your reviewers, and future you can recall the reasons, not only the code.

You keep working in your coding agent. Braid ambiently tracks everything. When the
change is ready, ask your agent to **reconstruct the intent** and review the result.

[Try it on Quickstart →](quickstart.md){ .md-button }

## Why Braid?

> Nobody reads code anymore!

It is true, no one reads code anymore, but it is not because they don't want to! They are unable to comprehend large chunks of code written by agents. As humans, we have limited mental bandwidth, however, we still want to steer the agent, own direction and outcome that agents are producing. 

To continue scale with the AI agent output, we need to understand and consciously guide the agent to success. 

Braid precisely does this, by being your ambient monitor of the agent. reconstructs the intent behind your work, the agent’s choices, and its checks to the code. You can follow the work, question a decision, and steer the next change. Keep building without losing the high-level system context.

Because of which you develop: 

1. Own understanding of what you want to merge/ship. 
2. Help make knowledge transfer in the team easy. 
3. Easier to rehydrate the coding loop again, when you want to retrieve the same change at a later time. 

![Without Braid, understanding of a change drops at each handover: the reviewer starts over from the diff, and the organisation starts over from git blame. With Braid, the traces, decisions, and intent captured while the agent works stay with the change for every reader.](assets/overview/why-braid.png#only-light)
![Without Braid, understanding of a change drops at each handover: the reviewer starts over from the diff, and the organisation starts over from git blame. With Braid, the traces, decisions, and intent captured while the agent works stay with the change for every reader.](assets/overview/why-braid-dark.png#only-dark)

## Where Braid fits in your current workflow?

Your prompt in the coding agent session is the start. An agent may delegate parts of it to another sub-agent, change code, run checks, and revise its approach. The final diff shows the code changes;
the session also contains the context behind them say the issue from GitHub, or a document from Notion.

[![Codex or Claude Code reads context such as Notion, Linear, or Google Docs during the session. On your machine, Braid captures the sessions, records the intent, and opens it in a local review UI, where you inspect and steer the agent. You can push the intent to the GitHub PR as a comment.](assets/overview/braid-fits.png#only-light)](assets/overview/braid-fits.png)
[![Codex or Claude Code reads context such as Notion, Linear, or Google Docs during the session. On your machine, Braid captures the sessions, records the intent, and opens it in a local review UI, where you inspect and steer the agent. You can push the intent to the GitHub PR as a comment.](assets/overview/braid-fits-dark.png#only-dark)](assets/overview/braid-fits-dark.png)

## Understand what your agent has done

Reconstruct the intent after the agent has finished and committed changes. Braid uses
the captured work and code changes to explain the goal, the outcome, the
decisions, and the steps that led there.

Open a decision to see the code it affected and the agent trace behind it.
Check the explanation against that evidence before you accept the change.

If you would make a different choice, tell your agent what to change and why.
Have it commit, then reconstruct the same braid again. Review the updated
intent before moving on.

## Make your peers easily understand your code

Once you are satisfied with the agent's work you can push the same intent doc from the coding agent session to Braid cloud. Braid would also comment the intent on the PR so that your peers or their agents trying to understand will have full context of the change you are trying to merge. 

This helps in building a shared understanding of any change, big or small! 

## Choose your next step

- [Quickstart](quickstart.md): add a feature to BrewGo and review the agent's work.

Need help? Ask on [Discord](https://discord.gg/G3wzPsKtR) or email
[hello@braidkit.io](mailto:hello@braidkit.io).
