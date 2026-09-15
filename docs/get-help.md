---
title: Get help
description: How to reach the Braid team while you are using the private preview.
hide:
  - footer
---

# Get help

Reach us on [Discord](https://discord.gg/gzUevjYD9) or email [hello@braidkit.io](mailto:hello@braidkit.io).

## Report a problem

Help us help you by letting us know the following when reporting a problem:

* Expected and actual behavior
* Braid version
* macOS version and architecture
* Output from `braid doctor --verbose` and `braid hooks doctor --verbose`

Run this in the repository where the problem happened. It saves your Braid version, your macOS version, and the output of both doctor commands to `braid-report.txt`.

```sh
{
  braid version
  sw_vers
  braid doctor --verbose
  braid hooks doctor --verbose
} > braid-report.txt 2>&1
```

!!! warning "The output of the Braid doctor commands contains sensitive information"
    It includes your account name in file paths and your signing key's fingerprint.
