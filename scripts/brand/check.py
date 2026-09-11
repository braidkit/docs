#!/usr/bin/env python3
"""Verify this repository's vendored brand files match scripts/brand/lock.json.

    python3 scripts/brand/check.py

Runs in CI and needs no network: everything it compares is already on disk.

WHY IT EXISTS

These files are copies, this script among them. The masters live in
braidkit/brand; running `python3 vendor.py` there refreshes them here.

Editing a copy here builds clean and passes review, and the next vendor run
reverts it. This check fails first, so the edit is visible while it is still
yours to move.

Do not fix a failure here by editing the lock. Move the change to
braidkit/brand and vendor it back.

The comparison is against the lock rather than against braidkit/brand, so this
reports an edited copy and not an out-of-date one.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

# This file lives at scripts/brand/check.py in the consuming repository, so the
# repository root is three levels up.
REPO = Path(__file__).resolve().parent.parent.parent
LOCK = Path(__file__).resolve().parent / "lock.json"


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
        print("These are copies. Move the change to braidkit/brand and vendor it")
        print("back from there, or the next vendor run overwrites you.")
        return 1
    print(f"{len(files)} vendored brand file(s) match, from brand@{lock.get('upstream','?')[:12]}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
