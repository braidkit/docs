---
title: Account and devices
description: Planned reference for hosted sign-in, CLI sessions, registered devices, and credential revocation.
draft: true
---

# Account and devices

For your first sign-in, follow [Quickstart](../getting-started/quickstart.md).
This reference will cover account access and managing devices afterward.

## Hosted sign-in and CLI sessions

<!-- Explain the hosted browser flow and the CLI/device session it authorizes.
     Confirm the launch origin and invitation requirements. BRA-243 predates
     the api-dev announcement; do not repeat its old DNS finding as current. -->

## Check your current identity

<!-- Document status, expiry, and selecting the intended service. Link the
     hosted screen for browser interaction instead of duplicating its UI.
     Verify any no-browser option; do not invent a second authentication flow. -->

## Use another device

<!-- Distinguish a shared account from each device's session and signing key.
     Sign-in must not imply work is synchronized across devices. -->

## Sign out or revoke a device

<!-- Distinguish local sign-out, remote revocation, and removing captured data. -->

## GitHub permissions

<!-- Confirm identity-only permissions versus optional repository authorization
     against the qualified release. braidkit/braid#326 is separate work.
     Link What Braid records for evidence handling and signing guarantees. -->

For expired sessions or sign-in failures, see [Troubleshooting](../troubleshooting.md).
