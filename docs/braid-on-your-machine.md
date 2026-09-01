---
title: Braid on your machine
description: What the Braid daemon is for, how to run it, and what Braid writes to your disk.
---

# Braid on your machine

Braid installs two binaries. `braid` is a thin client. `braid-daemon` is the
local service it talks to. Installing them does not start the daemon.

## What needs the daemon

The daemon holds lifecycle authority. It derives braid and thread state from the
record and answers the CLI. Lifecycle state belongs to the daemon and is never
copied into the Braid home.

Commands that read or change a braid need a reachable daemon. That includes
claiming an issue, adding captured sessions to a braid, reviewing, verifying,
shipping, and asking for a braid's authoritative state.

Other commands do not. Reporting the resolved home, initializing a repository,
capturing a session, and listing what has been captured locally all work with
the daemon stopped. Asking for the version probes the daemon, reports it as
unreachable when it is not running, and still exits successfully.

So an unreachable daemon on a fresh installation is the expected state, not a
failure.

## Running the daemon

This page describes `v0.2.0-alpha.1`, the release you can install.

There is no service registration yet. No launchd or systemd unit ships with
Braid, and there is no command that starts or stops it for you. Run the
`braid-daemon` binary yourself and keep it running, under whatever process
supervision you already use. It will not come back on its own after a reboot.

The daemon takes its listener addresses and database path from a configuration
file rather than process flags. That boundary is deliberate, so a machine has
one consistent configuration rather than a set of per-invocation overrides.

The file is required. The daemon will not start without one, and the file must
set `database.path`. A relative database path resolves from the configuration
file's own directory, never from the directory you launched from. The release
archive carries `configs/orchestrator.example.yaml` as a starting point.

The packaged location on macOS is:

```
~/Library/Application Support/Braid/orchestrator.yaml
```

On Linux it resolves under `$XDG_CONFIG_HOME`, normally
`~/.config/Braid/orchestrator.yaml`.

Two listeners come up with defaults:

| Purpose | Key | Default |
| --- | --- | --- |
| CLI connections | `grpc.address` | `127.0.0.1:8080` |
| Health and metrics | `admin.address` | `127.0.0.1:9090` |

The admin listener serves liveness, readiness, and Prometheus metrics. It has no
authentication. Neither does the gRPC listener. Both are validated as loopback
addresses and rejected if you point them at a wildcard or a LAN interface.

The Review UI is off unless you configure it. It needs `visualization.address`
together with a TLS certificate and private key, set as a group, and it is
HTTPS only.

## Where Braid puts things

The Braid home is the user-global location for Braid data. It resolves in this
order:

1. an explicit application override
2. the `BRAID_HOME` environment variable
3. `<OS user home>/.braid`

An invalid override is an error rather than a fallback to the next entry.
Reporting the resolved home does not create the directory.

Entries appear as the feature that owns them needs them:

- `key.pem`, the signing key
- `inbox/` and `braids/`, for sessions captured outside a Git repository
- `daemon/braid.db`, the default daemon database
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

All of it is untracked, and Braid adds no ignore rule for it. A reflexive
`git add -A` will sweep it into a commit. Captured sessions carry prompts, agent
reasoning, and tool calls, so committing that directory publishes the contents
of your work to everyone who can read the repository.

Ignore it before you capture anything:

```
.braid/
```

Put that in `.gitignore` to share the rule, or in `.git/info/exclude` to keep it
local. The `.gitignore` entry itself is safe to commit.

An ignore rule does not affect files Git is already tracking. If `.braid/` was
committed before you added the rule, stop tracking it and commit that removal:

```
git rm -r --cached .braid
```

That leaves the files on disk and removes them from future commits. It does not
remove them from history. If the directory was already pushed, the contents are
in the history of a shared branch and an ignore rule will not retract them.
Treat anything sensitive in those captures as disclosed, and rewrite history
only with the agreement of everyone working on that branch.

Promoted evidence does not live in the working tree. It lives in signed Git
notes under `refs/notes/braid`.

## The installation receipt

The standalone installer records what it installed in a receipt. The receipt
lives outside the Braid home, in account-scoped platform state. Setting
`BRAID_HOME` does not move it and does not help locate it.
