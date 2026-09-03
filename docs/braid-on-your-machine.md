---
title: Braid on your machine
description: What the Braid daemon is for, how to run it, and what Braid writes to your disk.
---

# Braid on your machine

Braid installs two binaries.

`braid` is the command line tool. You run it to capture an agent session, add
that session to a braid, ask for a braid's state, and record a review. It writes
captured sessions and local records to disk itself.

`braid-daemon` is a local background service. It derives the state of every
braid and thread from the signed event log, keeps that state in a database on
your machine, and serves the Review UI. It is the authority on lifecycle state.
When the CLI cannot reach it, commands that can fall back to their local records
do so, and say when they have.

## What needs the daemon

Lifecycle state lives in the daemon.

Commands that read or change a braid need a reachable daemon: claiming an
issue, adding captured sessions to a braid, reviewing, verifying, shipping,
and asking for a braid's authoritative state.

Other commands do not: reporting the resolved home, initializing a repository,
capturing a session, and listing what has been captured locally. Asking for
the version probes the daemon, reports it as unreachable when it is not
running, and still exits successfully.

An unreachable daemon on a fresh installation is expected. It is not a
failure.

## Running the daemon

Today, the daemon needs to start up manually by running the `braid-daemon` binary.

The daemon reads its listener addresses and database path from a
configuration file, not from process flags.

The file is optional. With no file present the daemon starts on built-in
defaults. On macOS, the default location is:

```
~/Library/Application Support/Braid/orchestrator.yaml
```

On Linux, it is `$XDG_CONFIG_HOME/Braid/orchestrator.yaml`, normally
`~/.config/Braid/orchestrator.yaml`.

The daemon opens three loopback listeners:

| Purpose | Key | Default |
| --- | --- | --- |
| CLI connections | `grpc.address` | `127.0.0.1:18082` |
| Review UI | `visualization.address` | `127.0.0.1:18446` |
| Health and metrics | `admin.address` | `127.0.0.1:19092` |

The admin listener serves liveness, readiness, and Prometheus metrics. The other
two carry the CLI's traffic and the Review UI.

These listeners do not provide user authentication and stay on loopback. The
daemon refuses to bind them anywhere else, and it still verifies signatures on
submitted work events.

Any other process on your machine that can reach these ports can read your
captured work. The same is true of a local intent server if you run one.

The database is `<braid home>/daemon/braid.db` unless `database.path`
overrides it. A relative override resolves from the configuration file's own
directory.

## Where Braid puts things

The Braid home is the user-global location for Braid data. It resolves in
this order:

1. an explicit application override
2. the `BRAID_HOME` environment variable
3. `<OS user home>/.braid`

An invalid override is an error rather than a fallback to the next entry.
Reporting the resolved home does not create the directory.

Entries appear as the feature that owns them needs them:

- `key.pem`, the signing key
- `inbox/` and `braids/`, for sessions captured outside a Git repository
- `daemon/braid.db`, the daemon's database. It owns this file, so nothing else
  writes it and editing it by hand is not supported.
- `auth-*` files and their locks, for file-backed session state
- `home-version`, the layout marker

Default authentication secrets live in the operating system credential store,
outside the Braid home. `<braid home>/config.yaml` is reserved for a future
layout and is not the daemon configuration file today.

## What Braid writes into a repository

An initialized repository has a `.braid/` directory inside the working tree:

- `config.yaml`, the repository configuration
- `pubkey.txt`, your signing key fingerprint
- `inbox/<session>/`, sessions captured in this repository
- `braids/`, evidence added to a braid

Braid adds no ignore rule for `.braid/`, and everything in it starts
untracked. A reflexive `git add -A` will sweep it into a commit.

!!! warning

    Captured sessions carry prompts, agent reasoning, and tool calls.
    Committing `.braid/` publishes the contents of your work to everyone who
    can read the repository.

Ignore it before you capture anything:

```
.braid/
```

Put that in `.gitignore` to share the rule, or in `.git/info/exclude` to keep
it local. The `.gitignore` entry itself is safe to commit.

An ignore rule does not affect files Git is already tracking. If `.braid/`
was committed before you added the rule, stop tracking it and commit that
removal:

```
git rm -r --cached .braid
```

That leaves the files on disk and removes them from future commits. It does
not remove them from history. If the directory was already pushed, the
contents are in the history of a shared branch, and an ignore rule will not
retract them. Treat anything sensitive in those captures as disclosed.
Rewrite history only with the agreement of everyone working on that branch.

Promoted evidence does not live in the working tree. It lives in signed Git
notes under `refs/notes/braid`.

## The installation receipt

The standalone installer records what it installed in a receipt. The receipt
lives outside the Braid home, in account-scoped platform state. Setting
`BRAID_HOME` does not move it and does not help locate it.
