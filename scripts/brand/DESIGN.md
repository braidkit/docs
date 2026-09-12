# Braid Design Foundation

What we intend Braid to look and sound like, so the marketing site, the docs and
the console stay in sync and read as one brand.

Colours, sizes, families and radii live in
[`tokens/braid-tokens.css`](tokens/braid-tokens.css). Take them from there, and
if one is missing, add it there rather than writing a value inline.

## What we are trying to achieve

- A reader can tell where a piece of text came from without being told.
- Nothing on screen claims more than the evidence behind it establishes.
- The same idea looks the same on every surface.
- What was rejected stays as visible as what shipped.

## How it should feel

Like a well-kept record. Plain, exact, unhurried. Closer to a logbook or a
transcript than to a dashboard or a pitch.

Confidence should come from precision rather than polish. Nothing should look
more certain than it is, and nothing should be decorated to seem more
trustworthy than the evidence makes it.

## Three kinds of information

Text is treated by where it came from, not by who typed it.

| Origin | What it is | What can go wrong |
| --- | --- | --- |
| **Authored** | A person wrote it. Headings, prose, button labels. | It can be wrong, and revising it changes no fact |
| **Captured** | Emitted and signed as it happened. Ids, timestamps, commands, paths, digests, exit codes. | The signature proves it was not altered, not that it is true |
| **Reconstructed** | A model inferred it from captured events. Intent summaries, rationale, approach narratives. | It reads like fact and is a guess |

A reader should be able to tell these apart at a glance, before reading a word
of them. Which typefaces do that is a decision in the token file. What matters
here is that the distinction survives whatever is chosen.

Reconstruction is the one worth most care, because it reads like human prose and
borrows the record's authority without earning it. So a reconstruction is marked
wherever it appears, with an edge down its left side and a line naming what it
was derived from.

```
│ The charge call was left without retries because a charge can
│ succeed even when its response never arrives.
│ Reconstructed from 11 events · e:7a3c1f0, e:51b0c4d · not signed
```

Citing event ids does not make a sentence captured. Captured text is emitted by
the system; a reconstruction cites captured text but is written by a model.

## Type

One scale at two densities: a reading density for marketing and docs, a tighter
one for the console. Same roles either way.

Size floors are accessibility commitments rather than preferences. The smallest
tier is for annotation, so nothing a reader needs in order to act belongs there.

Emphasis comes from size, space and position before it comes from weight.

## Colour

One interaction colour. It carries links, focus, the primary action and the
current item, so that colour comes to mean "you can act here" rather than
"this is important".

Four state meanings, kept away from the brand hue so a problem is never the most
on-brand thing on screen. These words mean the same thing on all three surfaces.

| State | Means |
| --- | --- |
| Signed | The signature verified. Not a claim about the content. |
| Promoted | Threads folded together and the record sealed. |
| Attention | A person is needed, or evidence is absent. |
| Blocked | The claim contradicts its events, or the system could not proceed. |

Colour alone should not carry a state. Pair it with words, and distinguish
missing evidence from a failure, because a gap means unknown rather than wrong.

## Shape and layout

Square by default. Radius is meaningful rather than decorative, so a control
takes a small one and a panel takes none.

Depth comes from an offset shadow or a hairline. Surfaces read as paper rather
than as glass.

Layout is asymmetric rather than centred. The recurring composition is a main
column of argument with a narrower column beside it carrying the evidence that
supports it.

Cards are for repeated items rather than a default container.

## Motion

Short, and mostly a change of opacity or colour. Movement should explain
something, such as where a new row came from. A record that animates for
atmosphere looks authored.

One moment is worth building: hovering a claim dims everything except the lines
it cites. That demonstrates the product rather than decorating it.

## Saying what the evidence supports

Copy is where a surface most easily overclaims, and all three surfaces have to
agree about what a word means. These pairs describe the same evidence, one
accurately and one not.

| When | Say | Not |
| --- | --- | --- |
| A signature verified | Signature verified | Verified change |
| Only an agent reported it | Agent reported 41 tests passed. No independent check is recorded. | Tests passed |
| Nothing was captured | No evidence recorded | Failed · This did not happen |
| A signature did not verify | The signature could not be verified | The signature is invalid |
| Sources disagree | Evidence conflicts | Braid determined |
| Capture may have gaps | Capture is best effort | Complete record |
| A model inferred it | Reconstructed from 11 events | The reasoning was |

`Signed` means the signature verified, not correct or checked or approved.
`Verified` takes an object: a signature or a check, never a change. Words like
trusted, secure, tamper-proof and guaranteed need to name exactly what was
established, or they are doing the overclaiming for you.

Buttons name the durable outcome, so "Record approval" rather than "Submit".

Errors say what failed, why if known, whether anything was recorded, and what to
do next.

> Couldn't record approval. This device's signing key is unavailable. No event
> was written. Reconnect the device and try again.

Shared wording, so the surfaces agree: "workstream" in product copy for the unit
of work a person follows, "thread" only in protocol and developer docs for the
underlying stream; "Decision needed" rather than "Human judgment"; "Changes"
rather than "Diff" in navigation.

## Evidence on screen

Identifiers, timestamps and digests are most of what Braid shows, so how they
read is part of the brand rather than a detail.

- Two values a reviewer might compare are rendered identically, or they cannot tell whether they are equal.
- Timestamps carry an absolute value somewhere, because a record is read months later when "Tuesday" means nothing.
- A truncated identifier keeps the whole value reachable, because a digest cut short is not a digest.
- Signature state reads as words, not an icon on its own.

## Rejected work is content

Agents report the approaches they tried and abandoned, and the alternatives they
weighed, alongside the one they kept. Keeping that visible is the point, so it
sits beside what shipped rather than behind a disclosure.

Dropped work is shown as considered rather than as wrong, and carries enough
provenance for a reader to go back to the events it came from.

## Accessibility

WCAG 2.2 AA is the floor on every surface, and it is a floor rather than a
target. The failure that matters most here is state carried by colour alone,
because this product is mostly states.

## Open

Worked examples. The visual rules above need a rendered page rather than prose:
an edge, a provenance line and the main-and-evidence composition are hard to
picture from a description.
