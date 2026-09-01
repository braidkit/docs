---
title: Installation
description: System requirements and how to install, verify, upgrade, and remove Braid on macOS.
---

# Installation

Braid installs as two binaries from one archive: `braid`, the CLI you drive, and
`braid-daemon`, the server it talks to. Both come out of the same build, so they
are version-matched by construction. Install them together.

!!! warning "The preview is access-gated"
    Release archives are published to
    [braidkit/braid](https://github.com/braidkit/braid/releases), which is a
    private repository. That link and every download on this page resolve only
    for a GitHub account that has been granted access to it. There is no public
    download, no `install.sh`, no Homebrew cask, and no Scoop bucket yet.

## System requirements

| | |
|---|---|
| **Operating system** | macOS |
| **Architecture** | `arm64` or `amd64` |
| **Git** | 2.25 or later, on your `PATH` |
| **Shell** | bash or zsh |

Both binaries are built with cgo disabled and are statically linked, so they
carry no runtime library dependency.

!!! note "macOS is the supported platform"
    The release pipeline builds `darwin` and `linux`, each for `amd64` and
    `arm64`. V1 install support covers macOS only. The Linux archives are
    covered below with the caveat that applies to them. Native Windows support
    has not shipped.

## Install

The current release is `v0.2.0-alpha.1`. No release is marked as latest, so
`releases/latest` does not resolve. Take the version explicitly from the
[releases page](https://github.com/braidkit/braid/releases).

The commands below use the [GitHub CLI](https://cli.github.com) because the
repository is private; run `gh auth login` first. Downloading the same files
from the releases page in a signed-in browser works too.

=== "macOS"

    ```sh
    VERSION=0.2.0-alpha.1   # no leading "v"; that is the archive naming
    ARCH=arm64              # arm64 on Apple silicon, amd64 on Intel

    gh release download "v${VERSION}" --repo braidkit/braid \
      --pattern "braid_${VERSION}_darwin_${ARCH}.tar.gz" \
      --pattern checksums.txt
    ```

    Check the archive against the published checksum before extracting it:

    ```sh
    shasum -a 256 --ignore-missing --check checksums.txt
    ```

    ```text
    braid_0.2.0-alpha.1_darwin_arm64.tar.gz: OK
    ```

    Extract, then put both binaries on your `PATH`:

    ```sh
    tar -xzf "braid_${VERSION}_darwin_${ARCH}.tar.gz"
    sudo install -m 0755 braid /usr/local/bin/braid
    sudo install -m 0755 braid-daemon /usr/local/bin/braid-daemon
    ```

=== "Linux"

    !!! note "Linux builds exist but are not part of V1 install support"
        `v0.2.0-alpha.1` carries `linux_amd64` and `linux_arm64` archives, built
        from the same sources as the macOS ones, and they install the same way.
        V1 install support is macOS only, so the Linux archives are not tested
        or supported as part of it.

    ```sh
    VERSION=0.2.0-alpha.1   # no leading "v"; that is the archive naming
    ARCH=amd64              # amd64 or arm64

    gh release download "v${VERSION}" --repo braidkit/braid \
      --pattern "braid_${VERSION}_linux_${ARCH}.tar.gz" \
      --pattern checksums.txt
    ```

    Check the archive against the published checksum before extracting it:

    ```sh
    sha256sum --ignore-missing --check checksums.txt
    ```

    ```text
    braid_0.2.0-alpha.1_linux_amd64.tar.gz: OK
    ```

    Extract, then put both binaries on your `PATH`:

    ```sh
    tar -xzf "braid_${VERSION}_linux_${ARCH}.tar.gz"
    sudo install -m 0755 braid /usr/local/bin/braid
    sudo install -m 0755 braid-daemon /usr/local/bin/braid-daemon
    ```

The archive also carries `README.md`, `LICENSE.txt`, and
`configs/orchestrator.example.yaml`, which is a starting point for the daemon's
configuration file. Nothing else is written anywhere. Installing puts two
binaries on your `PATH`. It does not start the daemon, create any Braid state,
edit a shell profile, or install agent hooks.

!!! note "`braid-intent` is a separate archive"
    The release also publishes `braid-intent_<version>_<os>_<arch>.tar.gz`. That
    is the intent reconstruction server, installed separately and not required
    to use the CLI. This page does not cover it.

## Verify the installation

`braid --version` prints the build the binary was stamped with:

```sh
braid --version
```

```text
braid v0.2.0-alpha.1 (7b2d4ef)
```

`braid version` prints the same client build in full, then probes the daemon it
is configured to reach:

```sh
braid version
```

```text
Client:
  Version:   v0.2.0-alpha.1
  Commit:    7b2d4ef
  Built:     2026-07-14T17:03:41Z
  Go:        go1.25.12
  Platform:  darwin/arm64
Server (127.0.0.1:8080):
  unreachable: context deadline exceeded
```

The client half is read from build information compiled into the binary, so it
is what tells you the install worked. The server half is a live probe. With no
daemon running it reports `unreachable` and the command still exits `0`, which
is the expected result on a fresh install rather than a failure. Add `--json`
for machine-readable output, or `--addr` to probe a specific daemon.

Confirm the server binary landed too:

```sh
command -v braid-daemon
```

```text
/usr/local/bin/braid-daemon
```

## Shell completion

`braid completion <shell>` writes a completion script to standard output for
bash, zsh, fish, or PowerShell. The command never writes a file and never
changes a shell profile. Run `braid completion <shell> --help` for that shell's
own instructions.

!!! note "Nothing is set up for you in this release"
    Installer-driven completion setup exists in the source but is in no
    published release, so `v0.2.0-alpha.1` leaves your shell profiles untouched.
    Activate completion yourself with the instructions below.

Each command below enables completion in the current shell. Saving it in a shell
profile is a separate step, described with it.

=== "Bash"

    Braid completion depends on `bash-completion`, which Braid does not install.
    Load that first, then load Braid completion in the current shell:

    ```sh
    eval "$(braid completion bash)"
    ```

    For future shells, add that line to `~/.bashrc`, after `bash-completion`
    loads. On macOS a login shell reads `~/.bash_profile` rather than
    `~/.bashrc`, so make sure whichever file controls login startup loads
    `~/.bashrc`:

    ```sh
    [ -f "$HOME/.bashrc" ] && . "$HOME/.bashrc"
    ```

=== "Zsh"

    Initialize completion only when `compdef` is not already available, which
    keeps `compinit`'s security checks in place:

    ```zsh
    autoload -Uz compinit
    if (( $+functions[compdef] )) || compinit; then
      source <(braid completion zsh)
    fi
    ```

    For future shells, add that block to `${ZDOTDIR:-$HOME}/.zshrc`.

=== "Fish"

    Load completions in the current shell:

    ```fish
    braid completion fish | source
    ```

    For future shells, add this to
    `${XDG_CONFIG_HOME:-$HOME/.config}/fish/conf.d/braid-completion.fish`:

    ```fish
    if status is-interactive
        braid completion fish | source
    end
    ```

=== "PowerShell"

    Activate completion in the current session:

    ```powershell
    braid completion powershell | Out-String | Invoke-Expression
    ```

    For future sessions, add that line to your PowerShell `$PROFILE`. The
    completion command does not edit `$PROFILE` for you.

## Upgrading

There is one channel, so upgrading is the install flow again with a newer
version. Download and verify the new archive, then overwrite both binaries in
place:

```sh
sudo install -m 0755 braid /usr/local/bin/braid
sudo install -m 0755 braid-daemon /usr/local/bin/braid-daemon
```

Upgrade the pair together. A `braid` and a `braid-daemon` from different
releases are not a supported combination. Run `braid --version` afterwards to
confirm the new build is the one being resolved on your `PATH`. Upgrading
touches binaries only and leaves your Braid data where it is.

## Uninstalling

This release has no `braid uninstall` command, so removal is manual. Remove the
two binaries you installed:

```sh
sudo rm /usr/local/bin/braid /usr/local/bin/braid-daemon
```

If you wrote a completion script to a directory on your `fpath` or to
`~/.config/fish/completions/`, delete that file too, and drop the
`source <(braid completion …)` line from your shell profile.

That is the whole removal. Braid data is separate, and nothing above deletes it.

## Removing Braid data

!!! danger "This is not part of uninstalling"
    Removing the binaries leaves your data intact so a reinstall picks up where
    you left off. Only run the commands in this section if you have decided you
    want the data gone. There is no undo, and no `braid` command performs these
    deletions for you.

`~/.braid` is your user-global Braid state. It holds the signing key at
`key.pem`, sessions captured outside a repository under `inbox/`, and braid
records under `braids/`.

```sh
rm -rf ~/.braid
```

Deleting `key.pem` destroys your contributor identity. Events you already signed
stay in the record signed by a key you no longer hold, and a new key means a new
contributor fingerprint.

`<repo>/.braid` is the per-repository directory that `braid init` creates. It
holds that repository's configuration and its local records, and there is one
per repository you have initialized:

```sh
rm -rf .braid
```

## Next steps

- [Braid on your machine](../braid-on-your-machine.md) covers the daemon and
  what Braid writes to disk.
- [How Braid works](../how-braid-works.md) covers the model.
- [Get help](../get-help.md) if something here does not work.

