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
    The release pipeline builds `darwin` only. `v0.1.0-alpha.1` also carries
    Linux archives, covered below with the caveat that applies to them. Native
    Windows support has not shipped.

## Install

The current release is `v0.1.0-alpha.1`. Every release is created as a draft and
none is marked as latest, so `releases/latest` does not resolve. Take the
version explicitly from the
[releases page](https://github.com/braidkit/braid/releases).

The commands below use the [GitHub CLI](https://cli.github.com) because the
repository is private; run `gh auth login` first. Downloading the same files
from the releases page in a signed-in browser works too.

=== "macOS"

    ```sh
    VERSION=0.1.0-alpha.1   # no leading "v"; that is the archive naming
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
    braid_0.1.0-alpha.1_darwin_arm64.tar.gz: OK
    ```

    Extract, then put both binaries on your `PATH`:

    ```sh
    tar -xzf "braid_${VERSION}_darwin_${ARCH}.tar.gz"
    sudo install -m 0755 braid /usr/local/bin/braid
    sudo install -m 0755 orchestrator /usr/local/bin/braid-daemon
    ```

=== "Linux"

    !!! warning "Linux is not part of V1 install support"
        `v0.1.0-alpha.1` carries `linux_amd64` and `linux_arm64` archives and
        they install and run the same way. The release pipeline no longer
        builds them, so a later release may have no Linux archive at all.
        Restoring Linux to the build matrix is tracked as post-V1 work.

    ```sh
    VERSION=0.1.0-alpha.1   # no leading "v"; that is the archive naming
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
    braid_0.1.0-alpha.1_linux_amd64.tar.gz: OK
    ```

    Extract, then put both binaries on your `PATH`:

    ```sh
    tar -xzf "braid_${VERSION}_linux_${ARCH}.tar.gz"
    sudo install -m 0755 braid /usr/local/bin/braid
    sudo install -m 0755 orchestrator /usr/local/bin/braid-daemon
    ```

!!! note "The archive still names the server binary `orchestrator`"
    `braid-daemon` is the name it ships under from the next release. Installing
    it under that name now makes the upgrade a plain overwrite, and nothing
    resolves the server by filename, so the rename costs nothing.

The archive also carries a copy of the repository `README.md`. Nothing else is
written anywhere: installing puts two binaries on your `PATH`, does not start
the daemon, and does not install agent hooks.

## Verify the installation

`braid --version` prints the build the binary was stamped with:

```sh
braid --version
```

```text
braid v0.1.0-alpha.1 (01fb0e8)
```

`braid version` prints the same client build in full, then probes the daemon it
is configured to reach:

```sh
braid version
```

```text
Client:
  Version:   v0.1.0-alpha.1
  Commit:    01fb0e8
  Built:     2026-07-14T17:03:41Z
  Go:        go1.25.12
  Platform:  darwin/arm64
Server (localhost:8080):
  unreachable: context deadline exceeded
```

The client half is read from build information compiled into the binary, so it
is what tells you the install worked. The server half is a live probe. With no
daemon running it reports `unreachable` and the command still exits `0`, which
is the expected result on a fresh install rather than a failure. Add `--json`
for machine-readable output, or `--addr` to probe a specific daemon.

The server binary in this release takes no `--version` flag, so confirm it
landed by looking for it on your `PATH`:

```sh
command -v braid-daemon
```

```text
/usr/local/bin/braid-daemon
```

## Shell completion

`braid completion <shell>` writes a completion script to standard output for
bash, zsh, fish, or PowerShell. Run `braid completion <shell> --help` for that
shell's full instructions.

=== "Bash"

    Load completions in the current shell:

    ```sh
    source <(braid completion bash)
    ```

    Add that line to `~/.bashrc` to load them in every new session.

=== "Zsh"

    If completion is not enabled in your environment yet, enable it once:

    ```sh
    echo "autoload -U compinit; compinit" >> ~/.zshrc
    ```

    Load completions in the current shell:

    ```sh
    source <(braid completion zsh)
    ```

    To load them for every new session, write the script into a directory on
    your `fpath` and start a new shell:

    ```sh
    # Linux
    braid completion zsh > "${fpath[1]}/_braid"

    # macOS, Homebrew zsh
    braid completion zsh > $(brew --prefix)/share/zsh/site-functions/_braid
    ```

=== "Fish"

    Load completions in the current shell:

    ```fish
    braid completion fish | source
    ```

    To load them for every new session:

    ```fish
    braid completion fish > ~/.config/fish/completions/braid.fish
    ```

## Upgrading

There is one channel, so upgrading is the install flow again with a newer
version. Download and verify the new archive, then overwrite both binaries in
place:

```sh
sudo install -m 0755 braid /usr/local/bin/braid
sudo install -m 0755 orchestrator /usr/local/bin/braid-daemon
```

From the release after `v0.1.0-alpha.1` the extracted server binary is itself
named `braid-daemon`, so the second line loses its rename.

Upgrade the pair together. A `braid` and a `braid-daemon` from different
releases are not a supported combination. Run `braid --version` afterwards to
confirm the new build is the one being resolved on your `PATH`. Upgrading
touches binaries only and leaves your Braid data where it is.

## Uninstalling

Remove the two binaries you installed:

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

- [Quickstart](quickstart.md) — claim work and walk a braid through to a decision
- [Concepts at a Glance](concepts-at-a-glance.md) — the vocabulary in one page
