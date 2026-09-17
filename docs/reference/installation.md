---
title: Installation
description: System requirements, install options, and how to verify, upgrade, and remove Braid on macOS.
---

# Installation

Braid installs as two binaries from one archive: `braid`, the CLI you drive, and
`braid-daemon`, the server it talks to. Both come out of the same build, so they
are version-matched by construction. The installer installs the pair together.

!!! note "This is a preview"
    Braid is in preview. Expect breaking changes between releases.

## System requirements

| | |
|---|---|
| **Operating system** | macOS |
| **Architecture** | `arm64` or `amd64` |
| **Git** | 2.25 or later, on your `PATH` |
| **Shell** | bash, zsh, or fish, for `PATH` and completion setup |
| **Also required** | `curl`, `tar`, `awk`, and either `sha256sum` or `shasum` |

This covers installing. Using Braid also needs a GitHub repository, a GitHub
account, and Claude Code; see [Quickstart](../getting-started/quickstart.md).

!!! note "macOS only"
    The release pipeline can build Linux archives, but the current release does
    not publish them. macOS is the only platform you can install today. Native
    Windows support has not shipped.

## Install

```sh
curl -fsSL https://braidkit.io/cli/install.sh | sh
```

With no version selector, the installer resolves the current preview from
[`latest.txt`](https://braidkit.io/cli/latest.txt) and installs that release. To
pin an exact release instead, pass the tag:

```sh
curl -fsSL https://braidkit.io/cli/install.sh | sh -s -- --version <tag>
```

### What it changes

- `braid` and `braid-daemon` in `$HOME/.local/bin`
- `PATH` in `~/.zprofile` and `~/.bash_profile`, plus a fish drop-in if fish is
  configured
- Shell completion for your current shell
- A per-user launchd service that starts the daemon at login

!!! note "What installing does not do"
    The installer never calls `sudo`, and enables no capture on its own. Signing
    in and choosing which agents Braid captures happen in
    [Quickstart](../getting-started/quickstart.md). It does not install `braid-intent`, which is a
    separate component the CLI does not require.

### Options

| Flag | Effect |
|---|---|
| `--version <tag>` | Install one exact release tag instead of the current preview. |
| `--install-dir <dir>` | Install into an absolute path other than `$HOME/.local/bin`. |
| `--no-modify-path` | Leave shell profiles untouched and print the `PATH` line to add yourself. Skips completion setup. |
| `--dry-run` | Resolve and print the plan without changing anything. |

Pass them after `-s --`. Setting `CI` to a non-empty value skips completion
setup, the welcome run, and the sign-in prompts.

!!! warning "If you download a release archive in a browser"
    The binaries are not notarized, so macOS refuses to run them after a browser
    download. Clear the quarantine attribute before running them:

    ```sh
    xattr -d com.apple.quarantine braid braid-daemon
    ```

If `braid` is not found after installing, open a new shell so the `PATH` change
takes effect, or add `$HOME/.local/bin` to `PATH` in the current one.

## Verify the installation

`braid doctor` checks the installation, your user state, the daemon, your agent
harnesses, and the current repository. It changes nothing.

```sh
braid doctor
```

```text
BRAID / DOCTOR
────────────────────────────────────────────────────────────────────────────────
Doctor summary (to see every check, run braid --verbose doctor)
[✓] installation
[✓] user
[✓] daemon
[✓] harness
[-] repo  global capture does not require repository initialization
```

Each failure prints what is wrong and what to do about it. `[-]` marks a check
that did not apply, not a problem.

| Flag | Effect |
|---|---|
| `--scope <name>` | Run one scope: `all`, `install`, `user`, `daemon`, `harness`, or `repo`. |
| `--offline` | Skip every live probe. |
| `--json` | Machine-readable output. |
| `--timeout <duration>` | Per-probe timeout. Default `3s`. |

To see every individual check rather than the summary, run
`braid --verbose doctor`.

### Build identity

Compare `braid --version` with `braid-daemon --version` to confirm the pair
matches:

```sh
braid --version
```

```text
braid:
  Version:   v0.2.0-alpha.9
  Commit:    a68ba53ce85d2aaf2b5c8ca3744828feccd9e8e5
  Built:     2026-09-17T07:28:24Z
  Go:        go1.25.13
  Platform:  darwin/arm64
```

`braid version` prints the client build and probes the running daemon:

```sh
braid version
```

```text
Client:
  Version:   v0.2.0-alpha.9
  Commit:    a68ba53ce85d2aaf2b5c8ca3744828feccd9e8e5
  Built:     2026-09-17T07:28:24Z
  Go:        go1.25.13
  Platform:  darwin/arm64
Server (127.0.0.1:18082):
  Version:   v0.2.0-alpha.9
  Commit:    a68ba53ce85d2aaf2b5c8ca3744828feccd9e8e5
  Built:     2026-09-17T07:28:24Z
```

With no daemon reachable, the server half reports `unreachable` and the command
still exits `0`. Add `--json` for machine-readable output, or `--addr` to probe
a specific daemon.

## Shell completion

The installer configures completion for the shell you were using when you ran
it, by adding a startup line that calls the installed binary:

| Shell | File the installer edits |
|---|---|
| bash | `~/.bashrc` |
| zsh | `${ZDOTDIR:-$HOME}/.zshrc` |
| fish | `${XDG_CONFIG_HOME:-$HOME/.config}/fish/conf.d/braid-completion.fish` |

Completion starts working in the next interactive shell.

Bash completion also needs `bash-completion`, which Braid does not install.

PowerShell is not set up for you. `braid completion powershell` writes a script
to standard output; add it to your `$PROFILE` yourself:

```powershell
braid completion powershell | Out-String | Invoke-Expression
```

## Manage your installation

### Upgrade

```sh
braid upgrade
```

Upgrade installs the current release, stopping and restarting the background
service around the swap. It will not downgrade you.

| Flag | Effect |
|---|---|
| `--check` | Resolve and compare versions without installing anything. |
| `--version <tag>` | Install an exact release tag. This is the recovery and preview path. |
| `--yes` | Skip the confirmation prompt. |
| `--json` | Machine-readable output. |

If you placed the binaries yourself rather than using the installer, upgrade
reports that it cannot identify the installation and stops.

Upgrading replaces binaries. Your Braid data is untouched.

### Uninstall

```sh
braid uninstall
```

Uninstall removes what the receipt records, and nothing else:

- both binaries, `braid` and `braid-daemon`
- the launchd service, unregistered and then deleted
- the `PATH` and completion lines the installer added to your shell profiles,
  and any profile file it created
- the receipt itself, last

If a file has changed since install, uninstall reports it instead of deleting
it. An installation it did not make is reported, never removed.

| Flag | Effect |
|---|---|
| `--dry-run` | Print the removal plan and change nothing. |
| `--yes` | Skip the confirmation prompt. |

Run the plan first if you want to see the exact list:

```sh
braid uninstall --dry-run
```

**Braid data is never removed by uninstalling.** Your Braid home, the daemon's
configuration and database, captured sessions, logs, Git configuration, and Git
notes all survive, so reinstalling picks up where you left off.

!!! note "Agent hooks are removed separately"
    Uninstall does not touch the capture hooks Braid installed into your coding
    agents. Remove those yourself, per agent:

    ```sh
    braid hooks uninstall claude
    braid hooks uninstall codex
    braid hooks uninstall cursor
    ```

### Remove Braid data

!!! danger "This is not part of uninstalling"
    Removing Braid leaves your data intact on purpose. Only run the commands in
    this section if you have decided you want the data gone. There is no undo,
    and no `braid` command performs these deletions for you.

`~/.braid` is your user-global Braid state — the Braid home. It holds the
signing key at `key.pem`, captured sessions under `inbox/`, braid records under
`braids/`, and the daemon's database at `daemon/braid.db`. Run `braid home` to
confirm the path first, since `BRAID_HOME` can move it:

```sh
braid home
rm -rf ~/.braid
```

Deleting `key.pem` destroys your contributor identity. A new key means a new
contributor fingerprint.

Three things live outside the Braid home:

| Path | Holds |
|---|---|
| `~/Library/Application Support/Braid/` | The daemon's machine configuration, and the install receipt and service preference that `braid uninstall` manages. |
| `~/Library/Caches/braid/` | Coordination locks only, never state. Safe to delete. |
| Keychain, service `braid-cli-auth` | Your signed-in credentials, one entry per host. |

Your repositories hold no Braid directory. Braid records into a repository as
signed Git notes under `refs/notes/braid`.

## Next steps

[Quickstart](../getting-started/quickstart.md) takes one small change from install to a completed
braid. [Get help](../get-help.md) if something here does not work.
