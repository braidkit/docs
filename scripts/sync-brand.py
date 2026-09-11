#!/usr/bin/env python3
"""Sync this repository's copies of the shared Braid brand files.

    scripts/sync-brand.py                  pull the latest and update the copies
    scripts/sync-brand.py --check          verify the copies (CI)
    scripts/sync-brand.py --status         report whether upstream has moved
    scripts/sync-brand.py --install-hook   fail at commit time, not at CI

The hook is optional and local. Git shares one hooks directory across every
worktree and branch of a repository, so it is written to stay silent wherever
the script or the lock is absent.

WHY COPIES AT ALL

The masters live in braidkit/brand. This repository keeps its own copies rather
than a submodule, because a favicon has to be served from this site's own origin,
a submodule taxes every clone and CI run for assets that change about once a
year, and a package would only serve the JavaScript surface of a three-stack
product.

What copying costs is that nothing notices when a copy and its master come
apart. That is not hypothetical: the brand package shipped with its own token
file already stale against a consumer, because two fixes were made downstream
and never sent back. Both trees built clean and neither said a word.

So the copies stay, and brand.lock plus --check make divergence loud.

WHAT FILES AND brand.lock DO

FILES below is hand-written and says which masters this repo wants and where
they go. brand.lock sits beside this script, is generated, and records for each
file the checksum that was synced and the upstream commit it came from. The lock
is what --check reads, and it is what tells you months later where a file
actually came from.

Both live in scripts/ rather than at the repository root. A root belongs to what
this project's own tooling expects; a secondary asset sync does not earn a place
there, and the repository it syncs from is already called brand.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
LOCK = HERE / "brand.lock"
UPSTREAM = "git@github.com:braidkit/brand.git"

# What this repository vendors: master path upstream -> where it goes here.
# Edit this list; never edit a vendored file in place.
FILES = [
    # the shared token layer; tokens.css here derives from it
    ("tokens/braid-tokens.css",      "docs/stylesheets/braid-tokens.css"),

    # browser and app icons
    ("icons/icon.svg",               "docs/assets/brand/icons/icon.svg"),
    ("icons/favicon.ico",            "docs/assets/brand/icons/favicon.ico"),
    ("icons/apple-touch-icon.png",   "docs/assets/brand/icons/apple-touch-icon.png"),

    # self-hosted typefaces, so no third-party request renders text
    ("fonts/archivo-variable.woff2", "docs/assets/fonts/archivo-variable.woff2"),
    ("fonts/jetbrains-mono.woff2",   "docs/assets/fonts/jetbrains-mono.woff2"),
    ("fonts/OFL.txt",                "docs/assets/fonts/OFL.txt"),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_source() -> tuple[Path, str, bool]:
    """Find the masters. Returns (brand dir, upstream commit, is_temporary).

    A sibling checkout is used when present, because that is the common case on
    a laptop and it avoids a network round trip. CI has only this repository
    checked out, so it falls back to a shallow clone. BRAND_SOURCE overrides
    both, which is what you want when testing an unmerged change upstream.
    """
    override = os.environ.get("BRAND_SOURCE")
    if override:
        path = Path(override).resolve()
        if not (path / "tokens").is_dir():
            sys.exit(f"BRAND_SOURCE does not look like the brand repository: {path}")
        return path, describe(path), False

    sibling = REPO.parent / "brand"
    if (sibling / "tokens").is_dir():
        return sibling, describe(sibling), False

    tmp = Path(tempfile.mkdtemp(prefix="braid-brand-"))
    subprocess.run(
        ["git", "clone", "--depth", "1", "--quiet", UPSTREAM, str(tmp / "brand")],
        check=True,
    )
    return tmp / "brand", describe(tmp / "brand"), True


def describe(repo: Path) -> str:
    r = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True
    )
    return r.stdout.strip() if r.returncode == 0 else "unknown"


def load_lock() -> dict:
    return json.loads(LOCK.read_text(encoding="utf-8")) if LOCK.exists() else {}


def cmd_check() -> int:
    """Verify every copy against the lock. No network, so it is cheap in CI."""
    lock = load_lock()
    if not lock:
        print(f"no {LOCK.name} — run scripts/sync-brand.py first")
        return 2
    bad, missing = [], []
    for dst, want in sorted(lock.get("files", {}).items()):
        path = REPO / dst
        if not path.exists():
            missing.append(dst)
            continue
        got = digest(path)
        if got == want:
            print(f"  ok     {dst}")
        else:
            print(f"  EDITED {dst}")
            print(f"           locked {want[:12]}  on disk {got[:12]}")
            bad.append(dst)
    for dst in missing:
        print(f"  MISSING {dst}")
    print()
    if bad or missing:
        print(f"{len(bad) + len(missing)} of {len(lock.get('files', {}))} copies do not match brand.lock.")
        print("A vendored file was edited here instead of upstream. Move the change")
        print("to braidkit/ops brand/, then re-run scripts/sync-brand.py.")
        return 1
    print(f"{len(lock.get('files', {}))} copies match brand.lock, from brand@{lock.get('upstream','?')[:12]}.")
    return 0


def cmd_status() -> int:
    lock = load_lock()
    brand, head, tmp = resolve_source()
    try:
        locked = lock.get("upstream", "")
        print(f"  locked at   brand@{locked[:12] or '(none)'}")
        print(f"  upstream at brand@{head[:12]}")
        if locked == head:
            print("\nup to date.")
            return 0
        changed = [
            dst for src, dst in FILES
            if (brand / src).exists()
            and digest(brand / src) != lock.get("files", {}).get(dst)
        ]
        if not changed:
            print("\nupstream moved, but none of the files this repo vendors changed.")
            return 0
        print(f"\n{len(changed)} vendored file(s) changed upstream:")
        for dst in changed:
            print(f"  {dst}")
        print("\nrun scripts/sync-brand.py to update them.")
        return 1
    finally:
        if tmp:
            shutil.rmtree(brand.parent, ignore_errors=True)


def cmd_sync() -> int:
    brand, head, tmp = resolve_source()
    try:
        files, changed = {}, []
        for src, dst in FILES:
            master = brand / src
            if not master.exists():
                sys.exit(f"master missing upstream: {src}")
            target = REPO / dst
            before = digest(target) if target.exists() else None
            after = digest(master)
            if before != after:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(master, target)
                changed.append(dst)
                print(f"  updated  {dst}")
            else:
                print(f"  ok       {dst}")
            files[dst] = after

        LOCK.write_text(
            json.dumps({"upstream": head, "source": UPSTREAM, "files": files}, indent=2)
            + "\n",
            encoding="utf-8",
        )
        print()
        print(f"{len(changed)} file(s) updated, {len(files)} locked at brand@{head[:12]}.")
        if changed:
            print("Commit the changed files together with brand.lock.")
        return 0
    finally:
        if tmp:
            shutil.rmtree(brand.parent, ignore_errors=True)


HOOK = """#!/bin/sh
# Installed by scripts/sync-brand.py --install-hook.
#
# Vendored brand files are copies. Editing one here builds clean, passes review,
# and is then silently reverted by the next sync. Fail at commit time rather
# than at CI, which is after the work is already done.
#
# Git shares one hooks directory across every worktree and branch of a
# repository, so this must stay silent where it does not apply: a branch that
# predates the sync script has to remain committable.
root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
[ -f "$root/scripts/sync-brand.py" ] || exit 0
[ -f "$root/scripts/brand.lock" ] || exit 0
command -v python3 >/dev/null 2>&1 || exit 0

python3 "$root/scripts/sync-brand.py" --check >/dev/null 2>&1 && exit 0
echo
python3 "$root/scripts/sync-brand.py" --check
exit 1
"""


def cmd_install_hook() -> int:
    """Fail at commit time rather than at CI, which is after the work is done."""
    r = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--git-path", "hooks"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("not a git repository")
    hooks = (REPO / r.stdout.strip()).resolve()
    hooks.mkdir(parents=True, exist_ok=True)
    path = hooks / "pre-commit"

    if path.exists() and "sync-brand.py" not in path.read_text(encoding="utf-8"):
        print(f"a pre-commit hook already exists at {path}")
        print("Leaving it alone. Add this line to it yourself:")
        print("  python3 scripts/sync-brand.py --check || exit 1")
        return 1

    path.write_text(HOOK, encoding="utf-8")
    path.chmod(0o755)
    print(f"installed {path}")
    print("Commits now fail if a vendored brand file was edited here.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true", help="verify copies against brand.lock")
    g.add_argument("--status", action="store_true", help="report whether upstream moved")
    g.add_argument("--install-hook", action="store_true",
                   help="add a pre-commit hook that runs --check")
    a = ap.parse_args()
    if a.check:
        return cmd_check()
    if a.status:
        return cmd_status()
    if a.install_hook:
        return cmd_install_hook()
    return cmd_sync()


if __name__ == "__main__":
    raise SystemExit(main())
