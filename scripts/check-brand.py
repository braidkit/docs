#!/usr/bin/env python3
"""Verify this repository's vendored brand files match scripts/brand.lock.

    python3 scripts/check-brand.py

Runs in CI and needs no network: everything it compares is already on disk.

WHY IT EXISTS

These files are copies. The masters live in braidkit/brand, and a workflow there
opens a pull request here whenever they change, so nobody has to remember to
pull.

What copying costs is that editing a copy here works. It builds clean, it passes
review, and it is then silently overwritten by the next propagation. This makes
that loud instead.

Do not fix a failure here by editing the lock. Move the change to
braidkit/brand; the next propagation brings it back.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LOCK = REPO / "scripts" / "brand.lock"


def main() -> int:
    if not LOCK.exists():
        print(f"no {LOCK.relative_to(REPO)} — nothing vendored yet")
        return 0

    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    files: dict[str, str] = lock.get("files", {})
    if not files:
        print(f"{LOCK.relative_to(REPO)} lists no files")
        return 1

    bad: list[str] = []
    for dst, want in sorted(files.items()):
        path = REPO / dst
        if not path.exists():
            print(f"  MISSING {dst}")
            bad.append(dst)
            continue
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        if got == want:
            print(f"  ok      {dst}")
        else:
            print(f"  EDITED  {dst}")
            print(f"            locked {want[:12]}  on disk {got[:12]}")
            bad.append(dst)

    print()
    if bad:
        print(f"{len(bad)} of {len(files)} vendored brand file(s) do not match the lock.")
        print("These are copies. Move the change to braidkit/brand and let the")
        print("propagation workflow bring it back, or the next one overwrites you.")
        return 1
    print(f"{len(files)} vendored brand file(s) match, from brand@{lock.get('upstream','?')[:12]}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
