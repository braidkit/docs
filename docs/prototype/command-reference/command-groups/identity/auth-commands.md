---
title: Authentication commands
description: Sign in, inspect the current identity, and manage registered devices.
---

# Authentication commands

Authentication connects the local signing key to a Braid identity through GitHub Device Flow.

## Login

```sh
braid auth login
```

Use `--no-browser` on a headless machine to print the verification URL and user code.

## Status

```sh
braid auth status
```

Status validates the current remote session and displays the resolved identity and device fingerprint.

## Devices

```sh
braid auth devices
```

List the credentials registered to the current user before revoking a lost or retired device.

## Revoke a device

```sh
braid auth revoke <credential-id>
```

Revocation ends every active session bound to that device credential.

## Logout

```sh
braid auth logout
```

Logging out revokes the current session and removes its local credential.
