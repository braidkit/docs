---
title: Review and verify
description: Verify a braid, inspect its intent, and record a human verdict.
---

# Review and verify

Braid separates automated verification from the human decision to approve a change.

## Run verification

Verification runs the configured check and records a system-derived result for the selected thread.

```sh
braid verify <braid-id>
```

### Passed verification

A passed check is evidence that the configured check succeeded. It is not a substitute for review and does not approve the change.

### Failed verification

A failed thread remains part of the record. Its evidence is not discarded, and the braid cannot treat it as a passed result.

## Prepare the review

Run review without a verdict to produce a review-ready projection of the braid.

```sh
braid review <braid-id>
```

## Record a verdict

The reviewer can approve, request changes, or block the work.

```sh
braid review <braid-id> --verdict approved
```

## Promote the braid

Promotion is the one-way boundary that merges, signs, and finalizes a surfaced braid.

```sh
braid promote <braid-id>
```
