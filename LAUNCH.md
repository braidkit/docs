# Minimum launch documentation

This is the writing map for the initial CLI preview, not a duplicate issue
tracker. Linear [BRA-196](https://linear.app/braidkit/issue/BRA-196) owns
workstream progress. Existing prose still needs a check against the launch
release; its presence here does not mean it is release-approved.

## The reader's path

Install → hosted sign-in → repository capture setup → make and add a change →
understand it → check and review it → complete the braid.

Quickstart owns one complete example through this path. Guides serve readers
returning to a task with their own code. Concepts explain the model; Reference
holds exact rules, configuration, and recovery information.

The sidebar has five root entries: Home, Get started, Guides, Concepts, and
Reference. Sections are collapsed unless active or opened by the reader.
Changelog remains in the header and Contact support stays at the sidebar foot.
The homepage links directly to the main tasks and troubleshooting.

## Content map

| Page | In this branch | Launch acceptance / source |
| --- | --- | --- |
| [Home](docs/index.md) | Navigation hub | Each card leads to a real page; remove outline status only when guidance is reviewed. [BRA-240](https://linear.app/braidkit/issue/BRA-240). |
| [Why Braid?](docs/why-braid.md) | Prose under review | Agree on the product story without promising complete capture or correct reconstruction. |
| [Installation](docs/getting-started/installation.md) | Existing prose; revalidate | Supported release, macOS architectures, verification, upgrades, and uninstall. Keep destructive cleanup distinct. [BRA-239](https://linear.app/braidkit/issue/BRA-239), [BRA-246](https://linear.app/braidkit/issue/BRA-246). |
| [Quickstart](docs/getting-started/quickstart.md) | Outline · Get started | One reproducible example from install and hosted sign-in through qualified Claude capture, add, intent, tests/review, and completion. Include expected results; do not end halfway with a link. [BRA-242](https://linear.app/braidkit/issue/BRA-242), [BRA-243](https://linear.app/braidkit/issue/BRA-243), [BRA-270](https://linear.app/braidkit/issue/BRA-270). |
| [Capture agent work](docs/guides/capture-agent-work.md) | Outline · Guides | Enable capture, interpret diagnostics, organize sessions, continue work, and remove hooks without deleting evidence. [BRA-242](https://linear.app/braidkit/issue/BRA-242), [BRA-269](https://linear.app/braidkit/issue/BRA-269), [BRA-229](https://linear.app/braidkit/issue/BRA-229), [BRA-234](https://linear.app/braidkit/issue/BRA-234). |
| [Understand a change](docs/guides/understand-a-change.md) | Outline · Guides | Choose evidence, consent to reconstruction, read decisions and evidence, and revisit available records. No verdict required. [BRA-228](https://linear.app/braidkit/issue/BRA-228), [BRA-259](https://linear.app/braidkit/issue/BRA-259), [BRA-88](https://linear.app/braidkit/issue/BRA-88). |
| [Review a change](docs/guides/review-a-change.md) | Outline · Guides | Check the candidate, record verification and a human verdict, handle revisions, and complete the braid. Explain Git effects and confirm the resulting record. [BRA-242](https://linear.app/braidkit/issue/BRA-242), [BRA-245](https://linear.app/braidkit/issue/BRA-245), [BRA-171](https://linear.app/braidkit/issue/BRA-171). |
| [Account and devices](docs/reference/account-and-devices.md) | Outline · Reference | Hosted browser versus CLI sessions, identity checks, another device, sign-out/revocation, and actual GitHub permissions. First sign-in stays in Quickstart. [BRA-243](https://linear.app/braidkit/issue/BRA-243). |
| [Troubleshooting](docs/troubleshooting.md) | Outline · Reference | Installation/health, authentication, daemon, missing captures, intent failures, blocked completion, missing records, and safe diagnostics. [BRA-223](https://linear.app/braidkit/issue/BRA-223), [BRA-229](https://linear.app/braidkit/issue/BRA-229). |
| [Preview status](docs/preview-status.md) | Outline | Who can use it, supported workflows/platforms/agents, limitations, applicable channel. [BRA-248](https://linear.app/braidkit/issue/BRA-248), [BRA-251](https://linear.app/braidkit/issue/BRA-251). |
| [How Braid works](docs/how-braid-works.md) | Existing prose; revalidate | Model and event boundaries. [BRA-236](https://linear.app/braidkit/issue/BRA-236). |
| [Lifecycle](docs/lifecycle.md) | Existing prose; revalidate | State names, transitions, scope and review gates agree with the release. [BRA-236](https://linear.app/braidkit/issue/BRA-236), [BRA-253](https://linear.app/braidkit/issue/BRA-253). |
| [CLI reference](docs/reference/cli.md) | Outline | Public commands and flags validated against released help, including auth requirements. [BRA-244](https://linear.app/braidkit/issue/BRA-244), [BRA-253](https://linear.app/braidkit/issue/BRA-253). |
| [Braid on your machine](docs/braid-on-your-machine.md) | Existing prose; revalidate | Daemon startup, configuration, paths, and local state. [BRA-237](https://linear.app/braidkit/issue/BRA-237). |
| [What Braid records](docs/what-braid-records.md) | Existing prose; revalidate | Capture limits, sensitive data, model-provider transmission, signing limits. [BRA-238](https://linear.app/braidkit/issue/BRA-238). |
| [Get help](docs/get-help.md) | Existing Discord link | One persistent support destination. Confirm invited-developer expectations. [BRA-251](https://linear.app/braidkit/issue/BRA-251). |
| [Changelog](docs/changelog.md) | Existing placeholder | First real release entry and channel links, without invented release notes. [BRA-247](https://linear.app/braidkit/issue/BRA-247). |

## Page boundaries and minimum scope

This map has 17 pages, including Home, Changelog, and Get help; eight are
outlines. It adds two task guides to the previous map and gives each a distinct
reader outcome. An issue does not automatically need a separate documentation page.

| Reader question | Owning page | Boundary |
| --- | --- | --- |
| How do I try Braid once? | Quickstart | One complete example, with sign-in inline and links for exceptional cases. |
| How do I manage capture on my own project? | Capture agent work | Repeatable setup, consent, diagnostics, session composition, and removal. Quickstart shows only one supported setup. |
| Why was this change made? | Understand a change | Reading goals, decisions, and evidence, including later maintenance. Generating a new explanation and reading an existing one are distinct actions. |
| Is this change ready, and how do I finish it? | Review a change | Checks, human verdicts, revisions, completion, and its Git effects. It links to state definitions instead of repeating them. |
| What are a braid and a thread? | How Braid works · Concepts | Mental model and event authority, without a command tutorial. |
| What does a state mean and what changes it? | Braid and thread lifecycle · Reference | Exact state tables and transition rules, separate from review instructions. |
| What is captured and sent? | What Braid records · Concepts | Data and trust boundaries, including coverage and signing limits; guides link here at consent points. |
| How do I manage identity or configure the local service? | Account and devices / Braid on your machine · Reference | Account/device sessions versus machine configuration, daemon operation, paths, and storage. |
| What is supported, or why did something fail? | Preview status / Troubleshooting · Reference | Known support limits versus symptom-based recovery. |

Keep upgrade, uninstall, and destructive data removal in Installation, with
separate headings and consequences. Keep release channels in Installation,
Preview status, and Changelog. Keep verification inside Review a change and
its command entry; it does not need a standalone page before BRA-245 is settled.

Do not add provider-specific pages until the supported integrations require
different instructions. Claude is the first qualification target; Codex and
Cursor do not become supported merely because their plans exist.

Defer public API reference, hosted administration, organizations, billing, SSO,
webhooks, and a large integrations catalog. Also keep infrastructure runbooks,
database migrations, and service deployment details out of the user sidebar.
They are not necessary to complete the initial developer workflow.

## Release review

The decision in [BRA-252](https://linear.app/braidkit/issue/BRA-252) is complete:
docs describe `main`, while installation remains pinned to
`v0.2.0-alpha.1`. The release gap still needs closing before public launch;
do not imply that every documented behavior is in the downloadable build.
The current source's public command surface is more authoritative than the
Braid README, which still describes hidden capture/dispatch commands.

Verify each workflow against the chosen build. Do not infer that installation
starts the daemon, creates state, or installs agent hooks. Source installation
stays out of these docs while the source repository is private.

The Linear MCP review on 2026-09-09 covered all 19 direct children of BRA-196
at inventory level and read the relevant workflow, auth, reference, privacy,
capture qualification, hook management, diagnostics, naming, and recovery
issues in detail. Source code was used to distinguish current command behavior
from issue proposals. These checks affect the writing requirements:

- Quickstart and capture guidance qualify Claude with
  [BRA-270](https://linear.app/braidkit/issue/BRA-270); Codex and Cursor do not
  block launch.
- The [September 2 Slack announcement](https://braidkit.slack.com/archives/C0B4XSQ8XU2/p1788389489917139)
  confirms hosted GitHub sign-in at `api-dev.braidkit.io`. BRA-243's earlier DNS
  diagnosis must not be repeated as a current outage. The deployment PR
  [braid#361](https://github.com/braidkit/braid/pull/361) was still open when
  checked; the source config names `api.braidkit.io`. Verify the actual launch
  origin and CLI/device flow before filling in Quickstart. Hosted sign-in
  removes the need for a separate onboarding page but not device/session help.
- Optional repository access in [braid#326](https://github.com/braidkit/braid/pull/326)
  was still open. Keep it distinct from identity login; verify permissions
  before making claims about the launch service.
- [BRA-269](https://linear.app/braidkit/issue/BRA-269) and
  [BRA-229](https://linear.app/braidkit/issue/BRA-229) are marked complete, but
  that does not replace BRA-270's full provider qualification. Their consent,
  disablement, and diagnostic requirements justify the capture guide.
- The verification defect tracked by
  [BRA-245](https://linear.app/braidkit/issue/BRA-245) must be resolved before
  asserting what the shipping gate guarantees.
- CLI reference needs generated help and CI drift detection
  ([BRA-244](https://linear.app/braidkit/issue/BRA-244)).
- [BRA-253](https://linear.app/braidkit/issue/BRA-253),
  [BRA-257](https://linear.app/braidkit/issue/BRA-257), and
  [BRA-259](https://linear.app/braidkit/issue/BRA-259) contain unsettled names.
  Current CLI source still uses `intent`, `review`, and `ship`; `ship` can
  either merge thread branches or finalize discovery work at existing HEAD.
  Use task titles and verify exact commands when writing. Do not equate
  completion with deployment, remote Git push, or hosted braid upload.
- The existing What Braid records prose needs revalidation against BRA-242's
  unsigned-inbox to daemon-signed-attached-copy model. Also verify redaction,
  authentication during local capture, and transmission timing. Do not treat
  the existing prose as the authority over the qualified implementation.
- Record retrieval deserves a section in Understand a change, not an invented
  command suite. [BRA-88](https://linear.app/braidkit/issue/BRA-88) is still a
  proposal; check actual readback support. [BRA-171](https://linear.app/braidkit/issue/BRA-171)
  requires reuse of reviewed intent during completion, so revalidate the
  existing claim that finalization necessarily sends evidence to a model.
- Public installation requires the signed/notarized macOS artifacts and
  Homebrew cask in [BRA-246](https://linear.app/braidkit/issue/BRA-246).

The outlines do not complete the linked content issues. `draft: true` labels
unfinished content; it does not restrict access. The access decision is pending.
Public launch also needs the access/indexing decision in
[BRA-250](https://linear.app/braidkit/issue/BRA-250) and the checks in
[DEPLOYMENT.md](DEPLOYMENT.md).
