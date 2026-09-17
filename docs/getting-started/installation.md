---
title: Installation
description: System requirements and how to install, verify, upgrade, and remove Braid on macOS.
---

# Installation

Braid installs as two binaries from one archive: `braid`, the CLI you drive, and
`braid-daemon`, the server it talks to. Both come out of the same build, so they
are version-matched by construction. The installer always installs the pair, and
refuses to commit an install whose two halves do not match.

!!! note "This is a preview"
    Braid is in preview. The installer and its releases are public, but the
    preview is unannounced and carries no support commitment. Expect breaking
    changes between releases.

## System requirements

| | |
|---|---|
| **Operating system** | macOS |
| **Architecture** | `arm64` or `amd64` |
| **Git** | 2.25 or later, on your `PATH` |
| **Shell** | bash, zsh, or fish |
| **Also required** | `curl`, `tar`, `awk`, and either `sha256sum` or `shasum` |

Both binaries are built with cgo disabled and are statically linked, so they
carry no runtime library dependency. The installer is a Bash script that stays
within the Bash 3.2 dialect macOS ships, so run it with `bash`, not `sh`.

!!! note "macOS only"
    The release pipeline can build Linux archives, but the current release does
    not publish them. macOS is the only platform you can install today. Native
    Windows support has not shipped.

## Install

```sh
curl --disable --proto '=https' --proto-redir '=https' --tlsv1.2 -fsSL \
  https://braidkit.io/cli/install.sh | bash
```

`--disable` comes first so a `~/.curlrc` you have forgotten about cannot rewrite
the request that fetches the installer. The installer applies the same flags to
its own downloads.

With no version selector, the installer resolves the current preview from
[`latest.txt`](https://braidkit.io/cli/latest.txt) and installs that release. To
pin an exact release instead, pass the tag:

```sh
curl --disable --proto '=https' --proto-redir '=https' --tlsv1.2 -fsSL \
  https://braidkit.io/cli/install.sh | bash -s -- --version v0.2.0-alpha.9
```

### What the installer does

1. Detects your platform and downloads only that archive and `checksums.txt`.
2. Verifies the archive against the published SHA-256 before unpacking it, then
   checks that the `braid` and `braid-daemon` inside carry the same build
   identity. It keeps backups and rolls back if anything fails.
3. Installs both binaries into `$HOME/.local/bin`.
4. Adds that directory to your `PATH` in `~/.zprofile` and `~/.bash_profile`,
   plus a fish drop-in if fish is already configured.
5. Sets up shell completion for your current shell.
6. Registers the daemon as a per-user launchd service so it starts at login, and
   starts it.
7. Writes an installation receipt recording exactly what it placed and changed.
8. Runs `braid` once so its welcome box confirms the install.

The receipt is what makes the rest of this page work: `braid upgrade` and
`braid uninstall` both act only on what the receipt records.

!!! note "What installing does not do"
    The installer never calls `sudo`. It does not sign you in, enable capture,
    or install agent hooks — those are separate, deliberate steps. It does not
    install `braid-intent`, which is a separate component the CLI does not
    require.

### Options

| Flag | Effect |
|---|---|
| `--version <tag>` | Install one exact release tag instead of the current preview. |
| `--install-dir <dir>` | Install into an absolute path other than `$HOME/.local/bin`. |
| `--no-modify-path` | Leave shell profiles untouched and print the `PATH` line to add yourself. Skips completion setup. |
| `--dry-run` | Resolve and print the plan without changing anything. |

Pass them after `-s --`, as in the pinned-version example above. Setting `CI` to
a non-empty value also skips completion setup and the welcome run.

!!! warning "The binaries are not notarized"
    They are ad-hoc signed, not signed with a Developer ID and not notarized.
    Installing with `curl` as above is unaffected, because a `curl` download
    carries no quarantine attribute. If you instead download a release archive
    in a browser, macOS will refuse to run the extracted binaries until you
    clear that attribute yourself:

    ```sh
    xattr -d com.apple.quarantine braid braid-daemon
    ```

If `braid` is not found after installing, open a new shell so the `PATH` change
takes effect, or add `$HOME/.local/bin` to `PATH` in the current one.

## Verify the installation

`braid doctor` is the check to run. It inspects the installation, your user
state, the daemon, your agent harnesses, and the current repository, and it is
read-only: it never creates a Braid home, key, receipt, configuration, or
database.

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

A closing `Result` line tallies passes, warnings, failures, and skips. Each
failure prints what is wrong and what to do about it. `[-]` marks a check that
did not apply — outside an initialized repository, the `repo` scope is skipped
rather than failed.

| Flag | Effect |
|---|---|
| `--scope <name>` | Run one scope: `all`, `install`, `user`, `daemon`, `harness`, or `repo`. |
| `--offline` | Skip every live probe. |
| `--json` | Machine-readable output. |
| `--timeout <duration>` | Per-probe timeout. Default `3s`. |

To see every individual check rather than the summary, run
`braid --verbose doctor`.

### Build identity

`braid --version` prints the build the binary was stamped with. `braid-daemon
--version` prints the same block for its half, so comparing the two is how you
confirm the pair matches:

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

`braid version` — the subcommand, not the flag — prints the client build and
then probes the running daemon:

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

Completion starts working in the next interactive shell. Nothing is cached, so
an upgraded binary serves updated completions with no further setup.

Bash completion additionally needs `bash-completion`, which Braid does not
install. On macOS a login shell reads `~/.bash_profile` rather than `~/.bashrc`,
so the installer creates a `~/.bash_profile` that sources `~/.bashrc` when you
do not already have one.

PowerShell is not set up for you. `braid completion powershell` writes a script
to standard output; add it to your `$PROFILE` yourself:

```powershell
braid completion powershell | Out-String | Invoke-Expression
```

`braid completion <shell>` only ever writes to standard output. It never writes
a file and never edits a shell profile.

## Upgrading

```sh
braid upgrade
```

Upgrade reads the installation receipt to identify how Braid was installed, then
hands the binary swap back to that installer — for a standalone install, the
`install.sh` embedded in the binary itself. It stops its own background service
for the swap and restores it afterwards, and it refuses to replace a running
daemon it does not manage.

It resolves the current release from the same
[`latest.txt`](https://braidkit.io/cli/latest.txt) pointer the installer uses,
and refuses an implicit downgrade.

| Flag | Effect |
|---|---|
| `--check` | Resolve and compare versions without installing anything. |
| `--version <tag>` | Install an exact release tag. This is the recovery and preview path. |
| `--yes` | Skip the confirmation prompt. |
| `--json` | Machine-readable output. |

There is no `--channel` flag: there is one channel.

Upgrade never acts on an installation it cannot identify. If you placed the
binaries yourself rather than using the installer, there is no receipt, and
upgrade will tell you so rather than guess.

Upgrading replaces binaries. Your Braid data is untouched.

## Uninstalling

```sh
braid uninstall
```

Uninstall removes what the receipt records, and nothing else:

- both binaries, `braid` and `braid-daemon`
- the launchd service, unregistered and then deleted
- the `PATH` and completion lines the installer added to your shell profiles,
  and any profile file it created
- the receipt itself, last

Each file is checked against the digest recorded at install time before it is
touched. If a file has changed since, uninstall reports it for you to handle
rather than deleting it. An installation it did not make is described, never
removed.

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
notes all survive, so reinstalling picks up where you left off. Your service
startup preference survives too, so a reinstall restores it.

!!! note "Agent hooks are removed separately"
    Uninstall does not touch the capture hooks Braid installed into your coding
    agents. Remove those yourself, per agent:

    ```sh
    braid hooks uninstall claude
    braid hooks uninstall codex
    braid hooks uninstall cursor
    ```

## Removing Braid data

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

Deleting `key.pem` destroys your contributor identity. Events you already signed
stay in the record signed by a key you no longer hold, and a new key means a new
contributor fingerprint.

Three things live outside the Braid home:

| Path | Holds |
|---|---|
| `~/Library/Application Support/Braid/` | The daemon's machine configuration, and the install receipt and service preference that `braid uninstall` manages. |
| `~/Library/Caches/braid/` | Coordination locks only, never state. Safe to delete. |
| Keychain, service `braid-cli-auth` | Your signed-in credentials, one entry per host. |

Your repositories hold no Braid directory. What Braid records into a repository
it records as signed Git notes under `refs/notes/braid`, which travel with the
repository rather than with your machine.

## Next steps

[Get help](../get-help.md) if something here does not work.
